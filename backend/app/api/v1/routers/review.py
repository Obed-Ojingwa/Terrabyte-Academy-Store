from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.review_service import ReviewService
from app.repositories.review_repository import ReviewRepository
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewInDB, ReviewWithUser, ReviewWithProduct
from app.api.v1.deps import get_current_active_user
from app.models.user import User


router = APIRouter()


def get_review_repository(db: AsyncSession = Depends(get_db)) -> ReviewRepository:
    return ReviewRepository(db)


def get_review_service(review_repo: ReviewRepository = Depends(get_review_repository)) -> ReviewService:
    return ReviewService(review_repo)


@router.post("/", response_model=ReviewInDB, status_code=status.HTTP_201_CREATED)
async def create_review(
    review_in: ReviewCreate,
    review_service: ReviewService = Depends(get_review_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new review.
    """
    return await review_service.create_review(review_in)


@router.get("/", response_model=List[ReviewInDB])
async def read_reviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    product_id: Optional[str] = None,
    review_service: ReviewService = Depends(get_review_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve reviews.
    """
    if product_id:
        return await review_service.get_by_product(product_id, skip=skip, limit=limit)
    # For getting all reviews, we'd need a different method
    # For now, we'll return an empty list or implement a general method
    return []


@router.get("/product/{product_id}", response_model=List[ReviewInDB])
async def read_reviews_by_product(
    product_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    review_service: ReviewService = Depends(get_review_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve reviews for a specific product.
    """
    return await review_service.get_by_product(product_id, skip=skip, limit=limit)


@router.get("/approved/{product_id}", response_model=List[ReviewInDB])
async def read_approved_reviews(
    product_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    review_service: ReviewService = Depends(get_review_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve approved reviews for a specific product.
    """
    return await review_service.get_approved_reviews(product_id, skip=skip, limit=limit)


@router.get("/recent", response_model=List[ReviewInDB])
async def read_recent_reviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    review_service: ReviewService = Depends(get_review_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve recent reviews.
    """
    return await review_service.get_recent_reviews(skip=skip, limit=limit)


@router.get("/{review_id}", response_model=ReviewInDB)
async def read_review(
    review_id: str,
    review_service: ReviewService = Depends(get_review_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific review by ID.
    """
    return await review_service.get(review_id)


@router.put("/{review_id}", response_model=ReviewInDB)
async def update_review(
    review_id: str,
    review_in: ReviewUpdate,
    review_service: ReviewService = Depends(get_review_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a review.
    """
    return await review_service.update_review(review_id, review_in)


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_id: str,
    review_service: ReviewService = Depends(get_review_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a review.
    """
    await review_service.delete_review(review_id)
    return None