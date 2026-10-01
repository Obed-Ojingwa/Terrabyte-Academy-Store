from typing import List, Optional
from app.services.base import BaseService
from app.repositories.course_module_repository import CourseModuleRepository
from app.models.course_module import CourseModule
from fastapi import HTTPException, status


class CourseModuleService(BaseService[CourseModuleRepository]):
    def __init__(self, course_module_repository: CourseModuleRepository):
        super().__init__(course_module_repository)
        self.course_module_repository = course_module_repository

    async def get_course_module(self, module_id: str) -> CourseModule:
        """Get course module by ID"""
        module = await self.course_module_repository.get(module_id)
        if not module:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course module not found"
            )
        return module

    async def get_modules_by_course_id(self, course_id: str) -> List[CourseModule]:
        """Get all modules for a specific course"""
        return await self.course_module_repository.get_by_course_id(course_id)

    async def create_course_module(
        self,
        course_id: str,
        title: str,
        description: Optional[str] = None,
        order_index: int = 0,
        duration_minutes: Optional[int] = None
    ) -> CourseModule:
        """Create a new course module"""
        # Check if course exists
        from app.repositories.course_repository import CourseRepository
        from app.db.session import get_db
        # We would need to inject the course repository or use a service
        # For simplicity, we'll skip this check in this implementation
        # In a real implementation, you'd validate that the course exists

        module_data = {
            "course_id": course_id,
            "title": title,
            "description": description,
            "order_index": order_index,
            "duration_minutes": duration_minutes
        }
        # Remove None values
        module_data = {k: v for k, v in module_data.items() if v is not None}

        return await self.course_module_repository.create(module_data)

    async def update_course_module(
        self,
        module_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        order_index: Optional[int] = None,
        duration_minutes: Optional[int] = None
    ) -> CourseModule:
        """Update course module"""
        module = await self.course_module_repository.get(module_id)
        if not module:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course module not found"
            )

        update_data = {}
        if title is not None:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description
        if order_index is not None:
            update_data["order_index"] = order_index
        if duration_minutes is not None:
            update_data["duration_minutes"] = duration_minutes

        if not update_data:
            return module

        return await self.course_module_repository.update(module_id, update_data)

    async def delete_course_module(self, module_id: str) -> bool:
        """Delete course module"""
        return await self.course_module_repository.delete(module_id)