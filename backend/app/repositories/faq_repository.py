from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.faq import FAQ


class FAQRepository(BaseRepository[FAQ]):
    def __init__(self, db: AsyncSession):
        super().__init__(FAQ, db)

    async def get_by_category(self, category_id: str, skip: int = 0, limit: int = 100) -> List[FAQ]:
        result = await self.db.execute(
            select(FAQ)
            .where(FAQ.category_id == category_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_active_faqs(self, skip: int = 0, limit: int = 100) -> List[FAQ]:
        result = await self.db.execute(
            select(FAQ)
            .where(FAQ.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_featured_faqs(self, skip: int = 0, limit: int = 100) -> List[FAQ]:
        result = await self.db.execute(
            select(FAQ)
            .where(FAQ.is_featured == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_popular_faqs(self, skip: int = 0, limit: int = 100) -> List[FAQ]:
        result = await self.db.execute(
            select(FAQ)
            .order_by(FAQ.views_count.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()