from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.testimonial_service import TestimonialService
from app.repositories.testimonial_repository import TestimonialRepository
from app.schemas.testimonial import TestimonialCreate, TestimonialUpdate, TestimonialInDB, TestimonialWithUser, TestimonialWithProduct, TestimonialWithService
from app.api.v1.deps import get_current_active_user
from app.models.user import User


router = APIRouter()


def get_testimonial_repository(db: AsyncSession = Depends(get_db)) -> TestimonialRepository:
    return TestimonialRepository(db)


def get_testimonial_service(testimonial_repo: TestimonialRepository = Depends(get_testimonial_repository)) -> TestimonialService:
    return TestimonialService(testimonial_repo)


@router.post("/", response_model=TestimonialInDB, status_code=status.HTTP_201_CREATED)
async def create_testimonial(
    testimonial_in: TestimonialCreate,
    testimonial_service: TestimonialService = Depends(get_testimonial_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new testimonial.
    """
    return await testimonial_service.create_testimonial(testimonial_in)


@router.get("/", response_model=List[TestimonialInDB])
async def read_testimonials(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    user_id: Optional[str] = None,
    product_id: Optional[str] = None,
    service_id: Optional[str] = None,
    active_only: bool = True,
    testimonial_service: TestimonialService = Depends(get_testimonial_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve testimonials.
    """
    if user_id:
        return await testimonial_service.get_by_user(user_id, skip=skip, limit=limit)
    if product_id:
        return await testimonial_service.get_by_product(product_id, skip=skip, limit=limit)
    if service_id:
        return await testimonial_service.get_by_service(service_id, skip=skip, limit=limit)
    if active_only:
        return await testimonial_service.get_active_testimonials(skip=skip, limit=limit)
    # For getting all testimonials, we'd need a different method
    # For now, we'll return active ones if active_only is True, otherwise empty list
    return await testimonial_service.get_active_testimonials(skip=skip, limit=limit) if active_only else []


@router.get("/featured", response_model=List[TestimonialInDB])
async def read_featured_testimonials(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    testimonial_service: TestimonialService = Depends(get_testimonial_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve featured testimonials.
    """
    return await testimonial_service.get_featured_testimonials(skip=skip, limit=limit)


@router.get("/recent", response_model=List[TestimonialInDB])
async def read_recent_testimonials(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    testimonial_service: TestimonialService = Depends(get_testimonial_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve recent testimonials.
    """
    return await testimonial_service.get_recent_testimonials(skip=skip, limit=limit)


@router.get("/{testimonial_id}", response_model=TestimonialInDB)
async def read_testimonial(
    testimonial_id: str,
    testimonial_service: TestimonialService = Depends(get_testimonial_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific testimonial by ID.
    """
    return await testimonial_service.get(testimonial_id)


@router.put("/{testimonial_id}", response_model=TestimonialInDB)
async def update_testimonial(
    testimonial_id: str,
    testimonial_in: TestimonialUpdate,
    testimonial_service: TestimonialService = Depends(get_testimonial_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a testimonial.
    """
    return await testimonial_service.update_testimonial(testimonial_id, testimonial_in)


@router.delete("/{testimonial_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_testimonial(
    testimonial_id: str,
    testimonial_service: TestimonialService = Depends(get_testimonial_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a testimonial.
    """
    await testimonial_service.delete_testimonial(testimonial_id)
    return None