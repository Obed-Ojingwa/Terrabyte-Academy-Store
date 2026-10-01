from typing import List, Optional
from app.services.base import BaseService
from app.repositories.course_enrollment_repository import CourseEnrollmentRepository
from app.models.course_enrollment import CourseEnrollment, EnrollmentStatusEnum
from fastapi import HTTPException, status
import datetime


class CourseEnrollmentService(BaseService[CourseEnrollmentRepository]):
    def __init__(self, course_enrollment_repository: CourseEnrollmentRepository):
        super().__init__(course_enrollment_repository)
        self.course_enrollment_repository = course_enrollment_repository

    async def get_course_enrollment(self, enrollment_id: str) -> CourseEnrollment:
        """Get course enrollment by ID"""
        enrollment = await self.course_enrollment_repository.get(enrollment_id)
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course enrollment not found"
            )
        return enrollment

    async def get_enrollments_by_user_id(self, user_id: str) -> List[CourseEnrollment]:
        """Get all enrollments for a specific user"""
        return await self.course_enrollment_repository.get_by_user_id(user_id)

    async def get_enrollments_by_course_id(self, course_id: str) -> List[CourseEnrollment]:
        """Get all enrollments for a specific course"""
        return await self.course_enrollment_repository.get_by_course_id(course_id)

    async def get_enrollment_by_user_and_course(self, user_id: str, course_id: str) -> Optional[CourseEnrollment]:
        """Get enrollment for a specific user and course"""
        return await self.course_enrollment_repository.get_by_user_and_course(user_id, course_id)

    async def get_active_enrollments(self, skip: int = 0, limit: int = 100) -> List[CourseEnrollment]:
        """Get active enrollments"""
        return await self.course_enrollment_repository.get_active_enrollments(skip=skip, limit=limit)

    async def get_completed_enrollments(self, skip: int = 0, limit: int = 100) -> List[CourseEnrollment]:
        """Get completed enrollments"""
        return await self.course_enrollment_repository.get_completed_enrollments(skip=skip, limit=limit)

    async def create_course_enrollment(
        self,
        user_id: str,
        course_id: str
    ) -> CourseEnrollment:
        """Create a new course enrollment"""
        # Check if user exists
        from app.models.user import User
        from app.repositories.user_repository import UserRepository
        # We would need to inject the user repository or use a service
        # For simplicity, we'll skip this check in this implementation
        # In a real implementation, you'd validate that the user exists

        # Check if course exists
        from app.repositories.course_repository import CourseRepository
        from app.db.session import get_db
        # We would need to inject the course repository or use a service
        # For simplicity, we'll skip this check in this implementation
        # In a real implementation, you'd validate that the course exists

        # Check if the user is already enrolled in this course
        existing_enrollment = await self.course_enrollment_repository.get_by_user_and_course(user_id, course_id)
        if existing_enrollment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already enrolled in this course"
            )

        enrollment_data = {
            "user_id": user_id,
            "course_id": course_id
        }
        return await self.course_enrollment_repository.create(enrollment_data)

    async def update_course_enrollment(
        self,
        enrollment_id: str,
        status: Optional[EnrollmentStatusEnum] = None,
        final_grade: Optional[float] = None,
        certificate_issued: Optional[bool] = None
    ) -> CourseEnrollment:
        """Update course enrollment"""
        enrollment = await self.course_enrollment_repository.get(enrollment_id)
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course enrollment not found"
            )

        update_data = {}
        if status is not None:
            update_data["status"] = status.value
        if final_grade is not None:
            update_data["final_grade"] = final_grade
        if certificate_issued is not None:
            update_data["certificate_issued"] = certificate_issued

        if not update_data:
            return enrollment

        return await self.course_enrollment_repository.update(enrollment_id, update_data)

    async def delete_course_enrollment(self, enrollment_id: str) -> bool:
        """Delete course enrollment"""
        return await self.course_enrollment_repository.delete(enrollment_id)