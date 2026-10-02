from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.faq_service import FAQService
from app.repositories.faq_repository import FAQRepository
from app.schemas.faq import FAQCreate, FAQUpdate, FAQInDB, FAQWithCategory
from app.api.v1.deps import get_current_active_user
from app.models.user import User


router = APIRouter()


def get_faq_repository(db: AsyncSession = Depends(get_db)) -> FAQRepository:
    return FAQRepository(db)


def get_faq_service(faq_repo: FAQRepository = Depends(get_faq_repository)) -> FAQService:
    return FAQService(faq_repo)


@router.post("/", response_model=FAQInDB, status_code=status.HTTP_201_CREATED)
async def create_faq(
    faq_in: FAQCreate,
    faq_service: FAQService = Depends(get_faq_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new FAQ.
    """
    return await faq_service.create_faq(faq_in)


@router.get("/", response_model=List[FAQInDB])
async def read_faqs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category_id: Optional[str] = None,
    active_only: bool = True,
    faq_service: FAQService = Depends(get_faq_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve FAQs.
    """
    if category_id:
        return await faq_service.get_by_category(category_id, skip=skip, limit=limit)
    if active_only:
        return await faq_service.get_active_faqs(skip=skip, limit=limit)
    # For getting all FAQs, we'd need a different method
    # For now, we'll return active ones if active_only is True, otherwise empty list
    return await faq_service.get_active_faqs(skip=skip, limit=limit) if active_only else []


@router.get("/featured", response_model=List[FAQInDB])
async def read_featured_faqs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    faq_service: FAQService = Depends(get_faq_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve featured FAQs.
    """
    return await faq_service.get_featured_faqs(skip=skip, limit=limit)


@router.get("/popular", response_model=List[FAQInDB])
async def read_popular_faqs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    faq_service: FAQService = Depends(get_faq_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve popular FAQs.
    """
    return await faq_service.get_popular_faqs(skip=skip, limit=limit)


@router.get("/{faq_id}", response_model=FAQInDB)
async def read_faq(
    faq_id: str,
    faq_service: FAQService = Depends(get_faq_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific FAQ by ID.
    """
    return await faq_service.get(faq_id)


@router.put("/{faq_id}", response_model=FAQInDB)
async def update_faq(
    faq_id: str,
    faq_in: FAQUpdate,
    faq_service: FAQService = Depends(get_faq_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update an FAQ.
    """
    return await faq_service.update_faq(faq_id, faq_in)


@router.delete("/{faq_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_faq(
    faq_id: str,
    faq_service: FAQService = Depends(get_faq_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete an FAQ.
    """
    await faq_service.delete_faq(faq_id)
    return None