from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..libraries.users import UserManager
from ..libraries.users.user_tables import UserORM
from ..database import DatabaseManager
from ..libraries.forum.forum_models import (
    ForumThreadCreateModel,
    ForumThreadOutModel,
    ForumPostCreateModel,
    ForumPostOutModel
)
from ..libraries.forum.forum_tables import ForumThreadORM, ForumPostORM

router = APIRouter(prefix="/forum")
user_manager = UserManager(DatabaseManager())


@router.post("/threads", response_model=ForumThreadOutModel)
async def create_thread(
    thread: ForumThreadCreateModel,
    current_user: UserORM = Depends(user_manager.get_current_user()),
    db: AsyncSession = Depends(DatabaseManager.get_session),
):
    new_thread = ForumThreadORM(title=thread.title, creator_id=current_user.id)
    db.add(new_thread)
    await db.commit()
    await db.refresh(new_thread)
    return new_thread


@router.get("/threads", response_model=list[ForumThreadOutModel])
async def list_threads(
    db: AsyncSession = Depends(DatabaseManager.get_session),
):
    result = await db.execute(select(ForumThreadORM))
    return result.scalars().all()


@router.post("/posts", response_model=ForumPostOutModel)
async def create_post(
    post: ForumPostCreateModel,
    current_user: UserORM = Depends(user_manager.get_current_user()),
    db: AsyncSession = Depends(DatabaseManager.get_session),
):
    new_post = ForumPostORM(
        content=post.content,
        thread_id=post.thread_id,
        author_id=current_user.id,
    )
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post


@router.get("/threads/{thread_id}/posts", response_model=list[ForumPostOutModel])
async def list_posts(
    thread_id: int,
    db: AsyncSession = Depends(DatabaseManager.get_session),
):
    result = await db.execute(
        select(ForumPostORM).where(ForumPostORM.thread_id == thread_id)
    )
    return result.scalars().all()
