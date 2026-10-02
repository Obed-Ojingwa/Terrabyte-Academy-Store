from app.services.base import BaseService
from app.repositories.service_review_repository import ServiceReviewRepository
from app.schemas.service_review import ServiceReviewCreate, ServiceReviewUpdate, ServiceReviewInDB, ServiceReviewWithUser, ServiceReviewWithService
from app.models.service_review import ServiceReview
from typing import List, Optional
from fastapi import HTTPException, status


class ServiceReviewService(BaseService[ServiceReviewRepository]):
    def __init__(self, service_review_repository: ServiceReviewRepository):
        super().__init__(service_review_repository)
        self.repository = service_review_repository

    async def get(self, service_review_id: str) -> ServiceReviewInDB:
        service_review = await self.repository.get(service_review_id)
        if not service_review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service review not found"
            )
        return ServiceReviewInDB.from_orm(service_review)

    async def get_by_service(self, service_id: str, skip: int = 0, limit: int = 100) -> List[ServiceReviewInDB]:
        service_reviews = await self.repository.get_by_service(service_id, skip=skip, limit=limit)
        return [ServiceReviewInDB.from_orm(service_review) for service_review in service_reviews]

    async def get_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[ServiceReviewInDB]:
        service_reviews = await self.repository.get_by_user(user_id, skip=skip, limit=limit)
        return [ServiceReviewInDB.from_orm(service_review) for service_review in service_reviews]

    async def get_approved_service_reviews(self, service_id: str, skip: int = 0, limit: int = 100) -> List[ServiceReviewInDB]:
        service_reviews = await self.repository.get_approved_service_reviews(service_id, skip=skip, limit=limit)
        return [ServiceReviewInDB.from_orm(service_review) for service_review in service_reviews]

    async def get_recent_service_reviews(self, skip: int = 0, limit: int = 100) -> List[ServiceReviewInDB]:
        service_reviews = await self.repository.get_recent_service_reviews(skip=skip, limit=limit)
        return [ServiceReviewInDB.from_orm(service_review) for service_review in service_reviews]

    async def create_service_review(self, service_review_in: ServiceReviewCreate) -> ServiceReviewInDB:
        service_review = await self.repository.create(service_review_in.dict())
        return ServiceReviewInDB.from_orm(service_review)

    async def update_service_review(self, service_review_id: str, service_review_in: ServiceReviewUpdate) -> ServiceReviewInDB:
        service_review = await self.repository.get(service_review_id)
        if not service_review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service review not found"
            )

        update_data = service_review_in.dict(exclude_unset=True)
        updated_service_review = await self.repository.update(service_review_id, update_data)
        return ServiceReviewInDB.from_orm(updated_service_review)

    async def delete_service_review(self, service_review_id: str) -> bool:
        service_review = await self.repository.get(service_review_id)
        if not service_review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service review not found"
            )
        return await self.repository.delete(service_review_id)