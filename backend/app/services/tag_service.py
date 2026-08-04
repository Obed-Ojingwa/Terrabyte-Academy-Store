from app.services.base import BaseService
from app.repositories.tag_repository import TagRepository
from app.schemas.tag import TagCreate, TagInDB
from app.models.tag import Tag
from typing import List, Optional
from fastapi import HTTPException, status

class TagService(BaseService[TagRepository]):
    def __init__(self, tag_repository: TagRepository):
        super().__init__(tag_repository)
        self.repository = tag_repository

    async def get(self, tag_id: str) -> TagInDB:
        tag = await self.repository.get(tag_id)
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found"
            )
        return TagInDB.from_orm(tag)

    async def get_tag_by_slug(self, slug: str) -> TagInDB:
        tag = await self.repository.get_by_slug(slug)
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found"
            )
        return TagInDB.from_orm(tag)

    async def get_active_tags(self, skip: int = 0, limit: int = 100) -> List[TagInDB]:
        tags = await self.repository.get_active_tags(skip=skip, limit=limit)
        return [TagInDB.from_orm(tag) for tag in tags]

    async def create_tag(self, tag_in: TagCreate) -> TagInDB:
        tag = await self.repository.create(tag_in.dict())
        return TagInDB.from_orm(tag)

    async def update_tag(self, tag_id: str, tag_in: TagCreate) -> TagInDB:
        tag = await self.repository.get(tag_id)
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found"
            )

        update_data = tag_in.dict(exclude_unset=True)
        updated_tag = await self.repository.update(tag_id, update_data)
        return TagInDB.from_orm(updated_tag)

    async def delete_tag(self, tag_id: str) -> bool:
        tag = await self.repository.get(tag_id)
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found"
            )
        return await self.repository.delete(tag_id)