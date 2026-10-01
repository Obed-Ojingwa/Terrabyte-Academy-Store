from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.course_lesson import CourseLesson


class CourseLessonRepository(BaseRepository[CourseLesson]):
    def __init__(self, db: AsyncSession):
        super().__init__(CourseLesson, db)

    async def get_by_module_id(self, module_id: str) -> List[CourseLesson]:
        """Get all lessons for a specific module"""
        result = await self.db.execute(
            select(CourseLesson)
            .where(CourseLesson.module_id == module_id)
            .order_by(CourseLesson.order_index)
        )
        return result.scalars().all()

    async def get_by_id_and_module(self, lesson_id: str, module_id: str) -> Optional[CourseLesson]:
        """Get a specific lesson by ID and module ID"""
        result = await self.db.execute(
            select(CourseLesson)
            .where(
                and_(
                    CourseLesson.id == lesson_id,
                    CourseLesson.module_id == module_id
                )
            )
        )
        return result.scalar_one_or_none()