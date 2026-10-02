from app.services.base import BaseService
from app.repositories.testimonial_repository import TestimonialRepository
from app.schemas.testimonial import TestimonialCreate, TestimonialUpdate, TestimonialInDB, TestimonialWithUser, TestimonialWithProduct, TestimonialWithService
from app.models.testimonial import Testimonial
from typing import List, Optional
from fastapi import HTTPException, status


class TestimonialService(BaseService[TestimonialRepository]):
    def __init__(self, testimonial_repository: TestimonialRepository):
        super().__init__(testimonial_repository)
        self.repository = testimonial_repository

    async def get(self, testimonial_id: str) -> TestimonialInDB:
        testimonial = await self.repository.get(testimonial_id)
        if not testimonial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Testimonial not found"
            )
        return TestimonialInDB.from_orm(testimonial)

    async def get_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[TestimonialInDB]:
        testimonials = await self.repository.get_by_user(user_id, skip=skip, limit=limit)
        return [TestimonialInDB.from_orm(testimonial) for testimonial in testimonials]

    async def get_by_product(self, product_id: str, skip: int = 0, limit: int = 100) -> List[TestimonialInDB]:
        testimonials = await self.repository.get_by_product(product_id, skip=skip, limit=limit)
        return [TestimonialInDB.from_orm(testimonial) for testimonial in testimonials]

    async def get_by_service(self, service_id: str, skip: int = 0, limit: int = 100) -> List[TestimonialInDB]:
        testimonials = await self.repository.get_by_service(service_id, skip=skip, limit=limit)
        return [TestimonialInDB.from_orm(testimonial) for testimonial in testimonials]

    async def get_active_testimonials(self, skip: int = 0, limit: int = 100) -> List[TestimonialInDB]:
        testimonials = await self.repository.get_active_testimonials(skip=skip, limit=limit)
        return [TestimonialInDB.from_orm(testimonial) for testimonial in testimonials]

    async def get_featured_testimonials(self, skip: int = 0, limit: int = 100) -> List[TestimonialInDB]:
        testimonials = await self.repository.get_featured_testimonials(skip=skip, limit=limit)
        return [TestimonialInDB.from_orm(testimonial) for testimonial in testimonials]

    async def get_recent_testimonials(self, skip: int = 0, limit: int = 100) -> List[TestimonialInDB]:
        testimonials = await self.repository.get_recent_testimonials(skip=skip, limit=limit)
        return [TestimonialInDB.from_orm(testimonial) for testimonial in testimonials]

    async def create_testimonial(self, testimonial_in: TestimonialCreate) -> TestimonialInDB:
        testimonial = await self.repository.create(testimonial_in.dict())
        return TestimonialInDB.from_orm(testimonial)

    async def update_testimonial(self, testimonial_id: str, testimonial_in: TestimonialUpdate) -> TestimonialInDB:
        testimonial = await self.repository.get(testimonial_id)
        if not testimonial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Testimonial not found"
            )

        update_data = testimonial_in.dict(exclude_unset=True)
        updated_testimonial = await self.repository.update(testimonial_id, update_data)
        return TestimonialInDB.from_orm(updated_testimonial)

    async def delete_testimonial(self, testimonial_id: str) -> bool:
        testimonial = await self.repository.get(testimonial_id)
        if not testimonial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Testimonial not found"
            )
        return await self.repository.delete(testimonial_id)