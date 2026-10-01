from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.course_enrollment import CourseEnrollment, EnrollmentStatusEnum


class CourseEnrollmentRepository(BaseRepository[CourseEnrollment]):
    def __init__(self, db: AsyncSession):
        super().__init__(CourseEnrollment, db)

    async def get_by_user_id(self, user_id: str) -> List[CourseEnrollment]:
        """Get all enrollments for a specific user"""
        result = await self.db.execute(
            select(CourseEnrollment)
            .where(CourseEnrollment.user_id == user_id)
        )
        return result.scalars().all()

    async def get_by_course_id(self, course_id: str) -> List[CourseEnrollment]:
        """Get all enrollments for a specific course"""
        result = await self.db.execute(
            select(CourseEnrollment)
            .where(CourseEnrollment.course_id == course_id)
        )
        return result.scalars().all()

    async def get_by_user_and_course(self, user_id: str, course_id: str) -> Optional[CourseEnrollment]:
        """Get enrollment for a specific user and course"""
        result = await self.db.execute(
            select(CourseEnrollment)
            .where(
                and_(
                    CourseEnrollment.user_id == user_id,
                    CourseEnrollment.course_id == course_id
                )
            )
        )
        return result.scalar_one_or_none()

    async def get_active_enrollments(self, skip: int = 0, limit: int = 100) -> List[CourseEnrollment]:
        """Get active enrollments"""
        result = await self.db.execute(
            select(CourseEnrollment)
            .where(CourseEnrollment.status == EnrollmentStatusEnum.ACTIVE)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_completed_enrollments(self, skip: int = 0, limit: int = 100) -> List[CourseEnrollment]:
        """Get completed enrollments"""
        result = await self.db.execute(
            select(CourseEnrollment)
            .where(CourseEnrollment.status == EnrollmentStatusEnum.COMPLETED)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()