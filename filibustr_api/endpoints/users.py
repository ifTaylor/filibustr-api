from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import DatabaseManager
from ..libraries.users import UserManager
from ..libraries.users.user_auth import (
    hash_password,
    verify_password,
    create_access_token,
)
from ..libraries.users.user_tables import UserORM, UserPreferencesORM
from ..libraries.users.user_models import (
    UserCreateModel,
    UserUpdateModel,
    UserOutModel,
    UserLoginModel,
    UserPreferencesModel
)

router = APIRouter()
user_manager = UserManager(DatabaseManager)


@router.post("/", response_model=UserOutModel)
async def create_user(
    user: UserCreateModel,
    db: AsyncSession = Depends(DatabaseManager.get_session),
):
    result = await db.execute(select(UserORM).where(UserORM.username == user.username))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_pw = hash_password(user.password)
    new_user = UserORM(
        username=user.username,
        email=str(user.email),
        hashed_password=hashed_pw,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.put("/me", response_model=UserOutModel)
async def update_me(
    updates: UserUpdateModel,
    current_user: UserORM = Depends(user_manager.get_current_user()),
    db: AsyncSession = Depends(DatabaseManager.get_session),
):
    # Only allow self-update
    user = current_user

    if updates.username:
        user.username = updates.username
    if updates.email:
        user.email = str(updates.email)
    if updates.password:
        user.hashed_password = hash_password(updates.password)

    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/me")
async def delete_me(
    current_user: UserORM = Depends(user_manager.get_current_user()),
    db: AsyncSession = Depends(DatabaseManager.get_session),
):
    await db.delete(current_user)
    await db.commit()
    return JSONResponse(content={"detail": "User deleted"})


@router.post("/login")
async def login(
    user: UserLoginModel,
    db: AsyncSession = Depends(DatabaseManager.get_session),
):
    result = await db.execute(select(UserORM).where(UserORM.username == user.username))
    db_user = result.scalar_one_or_none()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_data = {"sub": db_user.username}
    access_token = create_access_token(
        data=token_data,
        expires_delta=timedelta(minutes=30)
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserOutModel)
async def read_users_me(
    current_user: UserORM = Depends(user_manager.get_current_user())
):
    return current_user

@router.get("/preferences", response_model=UserPreferencesModel)
async def get_preferences(
    current_user: UserORM = Depends(user_manager.get_current_user()),
):
    prefs = current_user.preferences
    if not prefs:
        raise HTTPException(status_code=404, detail="Preferences not set")
    return prefs


@router.post("/preferences", response_model=UserPreferencesModel)
async def set_preferences(
    new_prefs: UserPreferencesModel,
    current_user: UserORM = Depends(user_manager.get_current_user()),
    db: AsyncSession = Depends(DatabaseManager.get_session),
):
    prefs = current_user.preferences

    if prefs is None:
        prefs = UserPreferencesORM(
            user_id=current_user.id,
            **new_prefs.dict()
        )
        db.add(prefs)
    else:
        for field, value in new_prefs.dict().items():
            setattr(prefs, field, value)

    await db.commit()
    await db.refresh(prefs)
    return prefs

