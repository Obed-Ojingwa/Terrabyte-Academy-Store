from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.tag import Tag

class TagRepository(BaseRepository[Tag]):
    def __init__(self, db: AsyncSession):
        super().__init__(Tag, db)

    async def get_by_slug(self, slug: str) -> Optional[Tag]:
        result = await self.db.execute(select(Tag).where(Tag.slug == slug))
        return result.scalar_one_or_none()

    async def get_active_tags(self, skip: int = 0, limit: int = 100) -> List[Tag]:
        result = await self.db.execute(
            select(Tag)
            .where(Tag.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()