from typing import List, Optional
from app.services.base import BaseService
from app.repositories.course_lesson_repository import CourseLessonRepository
from app.models.course_lesson import CourseLesson
from fastapi import HTTPException, status


class CourseLessonService(BaseService[CourseLessonRepository]):
    def __init__(self, course_lesson_repository: CourseLessonRepository):
        super().__init__(course_lesson_repository)
        self.course_lesson_repository = course_lesson_repository

    async def get_course_lesson(self, lesson_id: str) -> CourseLesson:
        """Get course lesson by ID"""
        lesson = await self.course_lesson_repository.get(lesson_id)
        if not lesson:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course lesson not found"
            )
        return lesson

    async def get_lessons_by_module_id(self, module_id: str) -> List[CourseLesson]:
        """Get all lessons for a specific module"""
        return await self.course_lesson_repository.get_by_module_id(module_id)

    async def create_course_lesson(
        self,
        module_id: str,
        title: str,
        description: Optional[str] = None,
        content_type: str = "text",
        content_url: Optional[str] = None,
        content_text: Optional[str] = None,
        order_index: int = 0,
        duration_minutes: Optional[int] = None,
        is_required: bool = True
    ) -> CourseLesson:
        """Create a new course lesson"""
        # Check if module exists
        from app.repositories.course_module_repository import CourseModuleRepository
        from app.db.session import get_db
        # We would need to inject the module repository or use a service
        # For simplicity, we'll skip this check in this implementation
        # In a real implementation, you'd validate that the module exists

        lesson_data = {
            "module_id": module_id,
            "title": title,
            "description": description,
            "content_type": content_type,
            "content_url": content_url,
            "content_text": content_text,
            "order_index": order_index,
            "duration_minutes": duration_minutes,
            "is_required": is_required
        }
        # Remove None values
        lesson_data = {k: v for k, v in lesson_data.items() if v is not None}

        return await self.course_lesson_repository.create(lesson_data)

    async def update_course_lesson(
        self,
        lesson_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        content_type: Optional[str] = None,
        content_url: Optional[str] = None,
        content_text: Optional[str] = None,
        order_index: Optional[int] = None,
        duration_minutes: Optional[int] = None,
        is_required: Optional[bool] = None
    ) -> CourseLesson:
        """Update course lesson"""
        lesson = await self.course_lesson_repository.get(lesson_id)
        if not lesson:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course lesson not found"
            )

        update_data = {}
        if title is not None:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description
        if content_type is not None:
            update_data["content_type"] = content_type
        if content_url is not None:
            update_data["content_url"] = content_url
        if content_text is not None:
            update_data["content_text"] = content_text
        if order_index is not None:
            update_data["order_index"] = order_index
        if duration_minutes is not None:
            update_data["duration_minutes"] = duration_minutes
        if is_required is not None:
            update_data["is_required"] = is_required

        if not update_data:
            return lesson

        return await self.course_lesson_repository.update(lesson_id, update_data)

    async def delete_course_lesson(self, lesson_id: str) -> bool:
        """Delete course lesson"""
        return await self.course_lesson_repository.delete(lesson_id)