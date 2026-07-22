from app.repositories.base import BaseRepository
from app.models.user import User
from app.models.role import Role
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from sqlalchemy import select, insert, update
from app.models.user_role import user_role
import uuid
from datetime import datetime, timedelta


class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_role(self, role_name: str) -> List[User]:
        result = await self.db.execute(
            select(User)
            .join(user_role, User.id == user_role.c.user_id)
            .join(Role, user_role.c.role_id == Role.id)
            .where(Role.name == role_name)
        )
        return result.scalars().all()

    async def get_by_verification_token(self, token: str) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.email_verification_token == token)
        )
        return result.scalar_one_or_none()

    async def assign_role(self, user_id: str, role_id: str) -> None:
        stmt = insert(user_role).values(user_id=user_id, role_id=role_id)
        await self.db.execute(stmt)
        await self.db.commit()

    async def verify_email(self, user_id: str) -> None:
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(email_verified=True, email_verification_token=None, email_verification_expires=None)
        )
        await self.db.commit()