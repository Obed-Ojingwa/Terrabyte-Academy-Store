from typing import List, Optional
from app.services.base import BaseService
from app.repositories.training_category_repository import TrainingCategoryRepository
from app.models.training_category import TrainingCategory
from fastapi import HTTPException, status


class TrainingCategoryService(BaseService[TrainingCategoryRepository]):
    def __init__(self, training_category_repository: TrainingCategoryRepository):
        super().__init__(training_category_repository)
        self.training_category_repository = training_category_repository

    async def get_training_category(self, category_id: str) -> TrainingCategory:
        """Get training category by ID"""
        category = await self.training_category_repository.get(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Training category not found"
            )
        return category

    async def get_training_category_by_name(self, name: str) -> TrainingCategory:
        """Get training category by name"""
        category = await self.training_category_repository.get_by_name(name)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Training category not found"
            )
        return category

    async def get_active_training_categories(self, skip: int = 0, limit: int = 100) -> List[TrainingCategory]:
        """Get active training categories"""
        return await self.training_category_repository.get_active_categories(skip=skip, limit=limit)

    async def create_training_category(self, name: str, description: Optional[str] = None) -> TrainingCategory:
        """Create a new training category"""
        # Check if category with this name already exists
        existing_category = await self.training_category_repository.get_by_name(name)
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Training category with this name already exists"
            )

        category_data = {
            "name": name,
            "description": description
        }
        return await self.training_category_repository.create(category_data)

    async def update_training_category(self, category_id: str, name: Optional[str] = None, description: Optional[str] = None) -> TrainingCategory:
        """Update training category"""
        category = await self.training_category_repository.get(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Training category not found"
            )

        update_data = {}
        if name is not None:
            # Check if another category with this name already exists
            if name != category.name:
                existing_category = await self.training_category_repository.get_by_name(name)
                if existing_category:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Training category with this name already exists"
                    )
            update_data["name"] = name
        if description is not None:
            update_data["description"] = description

        if not update_data:
            return category

        return await self.training_category_repository.update(category_id, update_data)

    async def delete_training_category(self, category_id: str) -> bool:
        """Delete training category"""
        return await self.training_category_repository.delete(category_id)