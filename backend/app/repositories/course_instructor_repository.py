from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.course_instructor import CourseInstructor


class CourseInstructorRepository(BaseRepository[CourseInstructor]):
    def __init__(self, db: AsyncSession):
        super().__init__(CourseInstructor, db)

    async def get_by_course_id(self, course_id: str) -> List[CourseInstructor]:
        """Get all instructors for a specific course"""
        result = await self.db.execute(
            select(CourseInstructor)
            .where(CourseInstructor.course_id == course_id)
        )
        return result.scalars().all()

    async def get_by_instructor_id(self, instructor_id: str) -> List[CourseInstructor]:
        """Get all course assignments for a specific instructor"""
        result = await self.db.execute(
            select(CourseInstructor)
            .where(CourseInstructor.instructor_id == instructor_id)
        )
        return result.scalars().all()

    async def get_by_course_and_instructor(self, course_id: str, instructor_id: str) -> Optional[CourseInstructor]:
        """Get specific course-instructor assignment"""
        result = await self.db.execute(
            select(CourseInstructor)
            .where(
                and_(
                    CourseInstructor.course_id == course_id,
                    CourseInstructor.instructor_id == instructor_id
                )
            )
        )
        return result.scalar_one_or_none()