from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.category_service import CategoryService
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryInDB, CategoryWithChildren
from app.api.v1.deps import get_current_active_user
from app.models.user import User

router = APIRouter()


def get_category_repository(db: AsyncSession = Depends(get_db)) -> CategoryRepository:
    return CategoryRepository(db)


def get_category_service(category_repo: CategoryRepository = Depends(get_category_repository)) -> CategoryService:
    return CategoryService(category_repo)


@router.post("/", response_model=CategoryInDB, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_in: CategoryCreate,
    category_service: CategoryService = Depends(get_category_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new category.
    """
    return await category_service.create_category(category_in)


@router.get("/", response_model=List[CategoryInDB])
async def read_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    active_only: bool = True,
    category_service: CategoryService = Depends(get_category_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve categories.
    """
    if active_only:
        return await category_service.get_active_categories(skip=skip, limit=limit)
    # For getting all categories (including inactive), we'd need a different method
    # For now, we'll just get active ones
    return await category_service.get_active_categories(skip=skip, limit=limit)


@router.get("/root", response_model=List[CategoryInDB])
async def read_root_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category_service: CategoryService = Depends(get_category_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve root categories (those without a parent).
    """
    return await category_service.get_root_categories(skip=skip, limit=limit)


@router.get("/{category_id}", response_model=CategoryInDB)
async def read_category(
    category_id: str,
    category_service: CategoryService = Depends(get_category_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific category by ID.
    """
    return await category_service.get(category_id)


@router.get("/slug/{slug}", response_model=CategoryInDB)
async def read_category_by_slug(
    slug: str,
    category_service: CategoryService = Depends(get_category_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific category by slug.
    """
    return await category_service.get_category_by_slug(slug)


@router.put("/{category_id}", response_model=CategoryInDB)
async def update_category(
    category_id: str,
    category_in: CategoryUpdate,
    category_service: CategoryService = Depends(get_category_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a category.
    """
    return await category_service.update_category(category_id, category_in)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: str,
    category_service: CategoryService = Depends(get_category_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a category.
    """
    await category_service.delete_category(category_id)
    return None


@router.get("/{category_id}/children", response_model=List[CategoryWithChildren])
async def read_category_children(
    category_id: str,
    category_service: CategoryService = Depends(get_category_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get children of a specific category.
    """
    # This would require a method in the service to get children with their children
    # For now, we'll return an empty list or implement a simple version
    return []