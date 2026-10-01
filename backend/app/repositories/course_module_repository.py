from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.course_module import CourseModule


class CourseModuleRepository(BaseRepository[CourseModule]):
    def __init__(self, db: AsyncSession):
        super().__init__(CourseModule, db)

    async def get_by_course_id(self, course_id: str) -> List[CourseModule]:
        """Get all modules for a specific course"""
        result = await self.db.execute(
            select(CourseModule)
            .where(CourseModule.course_id == course_id)
            .order_by(CourseModule.order_index)
        )
        return result.scalars().all()

    async def get_by_id_and_course(self, module_id: str, course_id: str) -> Optional[CourseModule]:
        """Get a specific module by ID and course ID"""
        result = await self.db.execute(
            select(CourseModule)
            .where(
                and_(
                    CourseModule.id == module_id,
                    CourseModule.course_id == course_id
                )
            )
        )
        return result.scalar_one_or_none()