from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.service_review_service import ServiceReviewService
from app.repositories.service_review_repository import ServiceReviewRepository
from app.schemas.service_review import ServiceReviewCreate, ServiceReviewUpdate, ServiceReviewInDB, ServiceReviewWithUser, ServiceReviewWithService
from app.api.v1.deps import get_current_active_user
from app.models.user import User


router = APIRouter()


def get_service_review_repository(db: AsyncSession = Depends(get_db)) -> ServiceReviewRepository:
    return ServiceReviewRepository(db)


def get_service_review_service(service_review_repo: ServiceReviewRepository = Depends(get_service_review_repository)) -> ServiceReviewService:
    return ServiceReviewService(service_review_repo)


@router.post("/", response_model=ServiceReviewInDB, status_code=status.HTTP_201_CREATED)
async def create_service_review(
    service_review_in: ServiceReviewCreate,
    service_review_service: ServiceReviewService = Depends(get_service_review_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new service review.
    """
    return await service_review_service.create_service_review(service_review_in)


@router.get("/", response_model=List[ServiceReviewInDB])
async def read_service_reviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service_id: Optional[str] = None,
    service_review_service: ServiceReviewService = Depends(get_service_review_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve service reviews.
    """
    if service_id:
        return await service_review_service.get_by_service(service_id, skip=skip, limit=limit)
    # For getting all service reviews, we'd need a different method
    # For now, we'll return an empty list or implement a general method
    return []


@router.get("/service/{service_id}", response_model=List[ServiceReviewInDB])
async def read_service_reviews_by_service(
    service_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service_review_service: ServiceReviewService = Depends(get_service_review_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve service reviews for a specific service.
    """
    return await service_review_service.get_by_service(service_id, skip=skip, limit=limit)


@router.get("/approved/{service_id}", response_model=List[ServiceReviewInDB])
async def read_approved_service_reviews(
    service_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service_review_service: ServiceReviewService = Depends(get_service_review_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve approved service reviews for a specific service.
    """
    return await service_review_service.get_approved_service_reviews(service_id, skip=skip, limit=limit)


@router.get("/recent", response_model=List[ServiceReviewInDB])
async def read_recent_service_reviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service_review_service: ServiceReviewService = Depends(get_service_review_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve recent service reviews.
    """
    return await service_review_service.get_recent_service_reviews(skip=skip, limit=limit)


@router.get("/{service_review_id}", response_model=ServiceReviewInDB)
async def read_service_review(
    service_review_id: str,
    service_review_service: ServiceReviewService = Depends(get_service_review_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific service review by ID.
    """
    return await service_review_service.get(service_review_id)


@router.put("/{service_review_id}", response_model=ServiceReviewInDB)
async def update_service_review(
    service_review_id: str,
    service_review_in: ServiceReviewUpdate,
    service_review_service: ServiceReviewService = Depends(get_service_review_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a service review.
    """
    return await service_review_service.update_service_review(service_review_id, service_review_in)


@router.delete("/{service_review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service_review(
    service_review_id: str,
    service_review_service: ServiceReviewService = Depends(get_service_review_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a service review.
    """
    await service_review_service.delete_service_review(service_review_id)
    return None