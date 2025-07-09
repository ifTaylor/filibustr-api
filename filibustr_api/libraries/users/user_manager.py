from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..users.user_auth import decode_access_token
from ..users.user_tables import UserORM


class UserManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.auth_scheme = HTTPBearer()

    def get_current_user(self):
        async def dependency(
            credentials: HTTPAuthorizationCredentials = Depends(self.auth_scheme),
            db: AsyncSession = Depends(self.db_manager.get_session),
        ):
            token = credentials.credentials
            payload = decode_access_token(token)
            if payload is None:
                raise HTTPException(status_code=401, detail="Invalid or expired token")

            username = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="Invalid token payload")

            stmt = (
                select(UserORM)
                .options(selectinload(UserORM.preferences))
                .where(UserORM.username == username)
            )
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            return user

        return dependency
