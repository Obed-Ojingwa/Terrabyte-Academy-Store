from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.training_category import TrainingCategory


class TrainingCategoryRepository(BaseRepository[TrainingCategory]):
    def __init__(self, db: AsyncSession):
        super().__init__(TrainingCategory, db)

    async def get_by_name(self, name: str) -> Optional[TrainingCategory]:
        """Get training category by name"""
        result = await self.db.execute(
            select(TrainingCategory)
            .where(TrainingCategory.name == name)
        )
        return result.scalar_one_or_none()

    async def get_active_categories(self, skip: int = 0, limit: int = 100) -> List[TrainingCategory]:
        """Get active training categories"""
        result = await self.db.execute(
            select(TrainingCategory)
            .where(TrainingCategory.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()