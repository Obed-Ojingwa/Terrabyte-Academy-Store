from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.service_review import ServiceReview


class ServiceReviewRepository(BaseRepository[ServiceReview]):
    def __init__(self, db: AsyncSession):
        super().__init__(ServiceReview, db)

    async def get_by_service(self, service_id: str, skip: int = 0, limit: int = 100) -> List[ServiceReview]:
        result = await self.db.execute(
            select(ServiceReview)
            .where(ServiceReview.service_id == service_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[ServiceReview]:
        result = await self.db.execute(
            select(ServiceReview)
            .where(ServiceReview.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_approved_service_reviews(self, service_id: str, skip: int = 0, limit: int = 100) -> List[ServiceReview]:
        result = await self.db.execute(
            select(ServiceReview)
            .where(ServiceReview.service_id == service_id)
            .where(ServiceReview.is_approved == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_recent_service_reviews(self, skip: int = 0, limit: int = 100) -> List[ServiceReview]:
        result = await self.db.execute(
            select(ServiceReview)
            .order_by(ServiceReview.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()