from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.review import Review


class ReviewRepository(BaseRepository[Review]):
    def __init__(self, db: AsyncSession):
        super().__init__(Review, db)

    async def get_by_product(self, product_id: str, skip: int = 0, limit: int = 100) -> List[Review]:
        result = await self.db.execute(
            select(Review)
            .where(Review.product_id == product_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Review]:
        result = await self.db.execute(
            select(Review)
            .where(Review.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_approved_reviews(self, product_id: str, skip: int = 0, limit: int = 100) -> List[Review]:
        result = await self.db.execute(
            select(Review)
            .where(Review.product_id == product_id)
            .where(Review.is_approved == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_recent_reviews(self, skip: int = 0, limit: int = 100) -> List[Review]:
        result = await self.db.execute(
            select(Review)
            .order_by(Review.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()