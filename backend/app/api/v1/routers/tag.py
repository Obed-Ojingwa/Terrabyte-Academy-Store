from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.tag_service import TagService
from app.repositories.tag_repository import TagRepository
from app.schemas.tag import TagCreate, TagInDB
from app.api.v1.deps import get_current_active_user
from app.models.user import User

router = APIRouter()


def get_tag_repository(db: AsyncSession = Depends(get_db)) -> TagRepository:
    return TagRepository(db)


def get_tag_service(tag_repo: TagRepository = Depends(get_tag_repository)) -> TagService:
    return TagService(tag_repo)


@router.post("/", response_model=TagInDB, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_in: TagCreate,
    tag_service: TagService = Depends(get_tag_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new tag.
    """
    return await tag_service.create_tag(tag_in)


@router.get("/", response_model=List[TagInDB])
async def read_tags(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    active_only: bool = True,
    tag_service: TagService = Depends(get_tag_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve tags.
    """
    if active_only:
        return await tag_service.get_active_tags(skip=skip, limit=limit)
    # For getting all tags (including inactive), we'd need a different method
    # For now, we'll just get active ones
    return await tag_service.get_active_tags(skip=skip, limit=limit)


@router.get("/{tag_id}", response_model=TagInDB)
async def read_tag(
    tag_id: str,
    tag_service: TagService = Depends(get_tag_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve a tag by ID.
    """
    tag = await tag_service.get(tag_id)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )
    return tag


@router.get("/slug/{slug}", response_model=TagInDB)
async def read_tag_by_slug(
    slug: str,
    tag_service: TagService = Depends(get_tag_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve a tag by slug.
    """
    tag = await tag_service.get_tag_by_slug(slug)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )
    return tag


@router.put("/{tag_id}", response_model=TagInDB)
async def update_tag(
    tag_id: str,
    tag_in: TagCreate,
    tag_service: TagService = Depends(get_tag_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a tag.
    """
    tag = await tag_service.update_tag(tag_id, tag_in)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )
    return tag


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    tag_id: str,
    tag_service: TagService = Depends(get_tag_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a tag.
    """
    success = await tag_service.delete_tag(tag_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )
    return None