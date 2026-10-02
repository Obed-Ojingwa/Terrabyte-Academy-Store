from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.testimonial import Testimonial


class TestimonialRepository(BaseRepository[Testimonial]):
    def __init__(self, db: AsyncSession):
        super().__init__(Testimonial, db)

    async def get_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Testimonial]:
        result = await self.db.execute(
            select(Testimonial)
            .where(Testimonial.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_product(self, product_id: str, skip: int = 0, limit: int = 100) -> List[Testimonial]:
        result = await self.db.execute(
            select(Testimonial)
            .where(Testimonial.product_id == product_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_service(self, service_id: str, skip: int = 0, limit: int = 100) -> List[Testimonial]:
        result = await self.db.execute(
            select(Testimonial)
            .where(Testimonial.service_id == service_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_active_testimonials(self, skip: int = 0, limit: int = 100) -> List[Testimonial]:
        result = await self.db.execute(
            select(Testimonial)
            .where(Testimonial.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_featured_testimonials(self, skip: int = 0, limit: int = 100) -> List[Testimonial]:
        result = await self.db.execute(
            select(Testimonial)
            .where(Testimonial.is_featured == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_recent_testimonials(self, skip: int = 0, limit: int = 100) -> List[Testimonial]:
        result = await self.db.execute(
            select(Testimonial)
            .order_by(Testimonial.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()