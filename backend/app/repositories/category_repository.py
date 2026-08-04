from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.category import Category

class CategoryRepository(BaseRepository[Category]):
    def __init__(self, db: AsyncSession):
        super().__init__(Category, db)

    async def get_by_slug(self, slug: str) -> Optional[Category]:
        result = await self.db.execute(select(Category).where(Category.slug == slug))
        return result.scalar_one_or_none()

    async def get_active_categories(self, skip: int = 0, limit: int = 100) -> List[Category]:
        result = await self.db.execute(
            select(Category)
            .where(Category.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_root_categories(self, skip: int = 0, limit: int = 100) -> List[Category]:
        result = await self.db.execute(
            select(Category)
            .where(Category.parent_id.is_(None))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()