from typing import List, Optional
from app.services.base import BaseService
from app.repositories.course_repository import CourseRepository
from app.repositories.training_category_repository import TrainingCategoryRepository
from app.models.course import Course, CourseLevelEnum
from app.models.user import User
from fastapi import HTTPException, status
import datetime


class CourseService(BaseService[CourseRepository]):
    def __init__(
        self,
        course_repository: CourseRepository,
        training_category_repository: TrainingCategoryRepository
    ):
        super().__init__(course_repository)
        self.course_repository = course_repository
        self.training_category_repository = training_category_repository

    async def get_course(self, course_id: str) -> Course:
        """Get course by ID"""
        course = await self.course_repository.get(course_id)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        return course

    async def get_course_by_title(self, title: str) -> Course:
        """Get course by title"""
        course = await self.course_repository.get_by_title(title)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        return course

    async def get_active_courses(self, skip: int = 0, limit: int = 100) -> List[Course]:
        """Get active courses"""
        return await self.course_repository.get_active_courses(skip=skip, limit=limit)

    async def get_courses_by_category(self, category_id: str, skip: int = 0, limit: int = 100) -> List[Course]:
        """Get courses by category"""
        return await self.course_repository.get_courses_by_category(category_id, skip=skip, limit=limit)

    async def get_courses_by_level(self, level: CourseLevelEnum, skip: int = 0, limit: int = 100) -> List[Course]:
        """Get courses by level"""
        return await self.course_repository.get_courses_by_level(level, skip=skip, limit=limit)

    async def get_featured_courses(self, skip: int = 0, limit: int = 100) -> List[Course]:
        """Get featured courses"""
        return await self.course_repository.get_featured_courses(skip=skip, limit=limit)

    async def search_courses(
        self,
        search_term: Optional[str] = None,
        category_id: Optional[str] = None,
        level: Optional[CourseLevelEnum] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        is_active: Optional[bool] = None,
        is_featured: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Course]:
        """Search courses with various filters"""
        return await self.course_repository.search_courses(
            search_term=search_term,
            category_id=category_id,
            level=level,
            min_price=min_price,
            max_price=max_price,
            is_active=is_active,
            is_featured=is_featured,
            skip=skip,
            limit=limit
        )

    async def create_course(
        self,
        title: str,
        description: str,
        category_id: str,
        level: CourseLevelEnum,
        duration_weeks: int,
        price: float,
        short_description: Optional[str] = None,
        duration_hours: Optional[int] = None,
        discount_price: Optional[float] = None,
        is_featured: bool = False,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        registration_start: Optional[datetime] = None,
        registration_end: Optional[datetime] = None,
        instructor_id: Optional[str] = None
    ) -> Course:
        """Create a new course"""
        # Check if category exists
        category = await self.training_category_repository.get(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Training category not found"
            )

        # Check if instructor exists (if provided)
        if instructor_id:
            # In a real implementation, we'd check if the user exists and is an instructor
            # For now, we'll just check if the user exists
            from app.models.user import User
            from app.repositories.user_repository import UserRepository
            # We would need to inject the user repository or use a service
            # For simplicity, we'll skip this check in this implementation
            pass

        # Check if course with this title already exists
        existing_course = await self.course_repository.get_by_title(title)
        if existing_course:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Course with this title already exists"
            )

        course_data = {
            "title": title,
            "description": description,
            "short_description": short_description,
            "category_id": category_id,
            "level": level.value,
            "duration_weeks": duration_weeks,
            "duration_hours": duration_hours,
            "price": price,
            "discount_price": discount_price,
            "is_featured": is_featured,
            "start_date": start_date,
            "end_date": end_date,
            "registration_start": registration_start,
            "registration_end": registration_end,
            "instructor_id": instructor_id
        }
        # Remove None values
        course_data = {k: v for k, v in course_data.items() if v is not None}

        return await self.course_repository.create(course_data)

    async def update_course(
        self,
        course_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        short_description: Optional[str] = None,
        category_id: Optional[str] = None,
        level: Optional[CourseLevelEnum] = None,
        duration_weeks: Optional[int] = None,
        duration_hours: Optional[int] = None,
        price: Optional[float] = None,
        discount_price: Optional[float] = None,
        is_featured: Optional[bool] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        registration_start: Optional[datetime] = None,
        registration_end: Optional[datetime] = None,
        instructor_id: Optional[str] = None
    ) -> Course:
        """Update course"""
        course = await self.course_repository.get(course_id)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )

        # Check if category exists (if provided)
        if category_id is not None:
            category = await self.training_category_repository.get(category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Training category not found"
                )

        # Check if another course with this title already exists (if title is being changed)
        if title is not None and title != course.title:
            existing_course = await self.course_repository.get_by_title(title)
            if existing_course:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Course with this title already exists"
                )

        update_data = {}
        if title is not None:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description
        if short_description is not None:
            update_data["short_description"] = short_description
        if category_id is not None:
            update_data["category_id"] = category_id
        if level is not None:
            update_data["level"] = level.value
        if duration_weeks is not None:
            update_data["duration_weeks"] = duration_weeks
        if duration_hours is not None:
            update_data["duration_hours"] = duration_hours
        if price is not None:
            update_data["price"] = price
        if discount_price is not None:
            update_data["discount_price"] = discount_price
        if is_featured is not None:
            update_data["is_featured"] = is_featured
        if start_date is not None:
            update_data["start_date"] = start_date
        if end_date is not None:
            update_data["end_date"] = end_date
        if registration_start is not None:
            update_data["registration_start"] = registration_start
        if registration_end is not None:
            update_data["registration_end"] = registration_end
        if instructor_id is not None:
            update_data["instructor_id"] = instructor_id

        if not update_data:
            return course

        return await self.course_repository.update(course_id, update_data)

    async def delete_course(self, course_id: str) -> bool:
        """Delete course"""
        return await self.course_repository.delete(course_id)