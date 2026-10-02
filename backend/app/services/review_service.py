from app.services.base import BaseService
from app.repositories.review_repository import ReviewRepository
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewInDB, ReviewWithUser, ReviewWithProduct
from app.models.review import Review
from typing import List, Optional
from fastapi import HTTPException, status


class ReviewService(BaseService[ReviewRepository]):
    def __init__(self, review_repository: ReviewRepository):
        super().__init__(review_repository)
        self.repository = review_repository

    async def get(self, review_id: str) -> ReviewInDB:
        review = await self.repository.get(review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found"
            )
        return ReviewInDB.from_orm(review)

    async def get_by_product(self, product_id: str, skip: int = 0, limit: int = 100) -> List[ReviewInDB]:
        reviews = await self.repository.get_by_product(product_id, skip=skip, limit=limit)
        return [ReviewInDB.from_orm(review) for review in reviews]

    async def get_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[ReviewInDB]:
        reviews = await self.repository.get_by_user(user_id, skip=skip, limit=limit)
        return [ReviewInDB.from_orm(review) for review in reviews]

    async def get_approved_reviews(self, product_id: str, skip: int = 0, limit: int = 100) -> List[ReviewInDB]:
        reviews = await self.repository.get_approved_reviews(product_id, skip=skip, limit=limit)
        return [ReviewInDB.from_orm(review) for review in reviews]

    async def get_recent_reviews(self, skip: int = 0, limit: int = 100) -> List[ReviewInDB]:
        reviews = await self.repository.get_recent_reviews(skip=skip, limit=limit)
        return [ReviewInDB.from_orm(review) for review in reviews]

    async def create_review(self, review_in: ReviewCreate) -> ReviewInDB:
        review = await self.repository.create(review_in.dict())
        return ReviewInDB.from_orm(review)

    async def update_review(self, review_id: str, review_in: ReviewUpdate) -> ReviewInDB:
        review = await self.repository.get(review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found"
            )

        update_data = review_in.dict(exclude_unset=True)
        updated_review = await self.repository.update(review_id, update_data)
        return ReviewInDB.from_orm(updated_review)

    async def delete_review(self, review_id: str) -> bool:
        review = await self.repository.get(review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found"
            )
        return await self.repository.delete(review_id)