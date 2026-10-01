from typing import List, Optional
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.course import Course, CourseLevelEnum


class CourseRepository(BaseRepository[Course]):
    def __init__(self, db: AsyncSession):
        super().__init__(Course, db)

    async def get_by_title(self, title: str) -> Optional[Course]:
        """Get course by title"""
        result = await self.db.execute(
            select(Course)
            .where(Course.title == title)
        )
        return result.scalar_one_or_none()

    async def get_active_courses(self, skip: int = 0, limit: int = 100) -> List[Course]:
        """Get active courses"""
        result = await self.db.execute(
            select(Course)
            .where(Course.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_courses_by_category(self, category_id: str, skip: int = 0, limit: int = 100) -> List[Course]:
        """Get courses by category"""
        result = await self.db.execute(
            select(Course)
            .where(Course.category_id == category_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_courses_by_level(self, level: CourseLevelEnum, skip: int = 0, limit: int = 100) -> List[Course]:
        """Get courses by level"""
        result = await self.db.execute(
            select(Course)
            .where(Course.level == level)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_featured_courses(self, skip: int = 0, limit: int = 100) -> List[Course]:
        """Get featured courses"""
        result = await self.db.execute(
            select(Course)
            .where(Course.is_featured == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

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
        """
        Search courses with various filters.

        Args:
            search_term: Term to search in title and description
            category_id: Filter by category ID
            level: Filter by course level
            min_price: Minimum price filter
            max_price: Maximum price filter
            is_active: Filter by active status
            is_featured: Filter by featured status
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Course objects matching the criteria
        """
        query = select(Course)

        # Apply search term filter
        if search_term:
            search_pattern = f"%{search_term}%"
            query = query.where(
                or_(
                    Course.title.ilike(search_pattern),
                    Course.description.ilike(search_pattern)
                )
            )

        # Apply category filter
        if category_id:
            query = query.where(Course.category_id == category_id)

        # Apply level filter
        if level:
            query = query.where(Course.level == level)

        # Apply price range filters
        if min_price is not None:
            query = query.where(Course.price >= min_price)
        if max_price is not None:
            query = query.where(Course.price <= max_price)

        # Apply active filter
        if is_active is not None:
            query = query.where(Course.is_active == is_active)

        # Apply featured filter
        if is_featured is not None:
            query = query.where(Course.is_featured == is_featured)

        # Apply pagination
        query = query.offset(skip).limit(limit)

        result = await self.db.execute(query)
        return result.scalars().all()