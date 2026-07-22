from app.repositories.base import BaseRepository
from app.models.role import Role
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from sqlalchemy import select


class RoleRepository(BaseRepository[Role]):
    def __init__(self, db: AsyncSession):
        super().__init__(Role, db)

    async def get_by_name(self, name: str) -> Optional[Role]:
        result = await self.execute(
            select(Role).where(Role.name == name)
        )
        return result.scalar_one_or_none()

    async def get_active_roles(self) -> List[Role]:
        result = await self.execute(
            select(Role).where(Role.is_active == True)
        )
        return result.scalars().all()