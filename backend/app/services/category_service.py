from app.services.base import BaseService
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryInDB
from app.models.category import Category
from typing import List, Optional
from fastapi import HTTPException, status

class CategoryService(BaseService[CategoryRepository]):
    def __init__(self, category_repository: CategoryRepository):
        super().__init__(category_repository)
        self.repository = category_repository

    async def get(self, category_id: str) -> CategoryInDB:
        category = await self.repository.get(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        return CategoryInDB.from_orm(category)

    async def get_category_by_slug(self, slug: str) -> CategoryInDB:
        category = await self.repository.get_by_slug(slug)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        return CategoryInDB.from_orm(category)

    async def get_active_categories(self, skip: int = 0, limit: int = 100) -> List[CategoryInDB]:
        categories = await self.repository.get_active_categories(skip=skip, limit=limit)
        return [CategoryInDB.from_orm(category) for category in categories]

    async def get_root_categories(self, skip: int = 0, limit: int = 100) -> List[CategoryInDB]:
        categories = await self.repository.get_root_categories(skip=skip, limit=limit)
        return [CategoryInDB.from_orm(category) for category in categories]

    async def create_category(self, category_in: CategoryCreate) -> CategoryInDB:
        category = await self.repository.create(category_in.dict())
        return CategoryInDB.from_orm(category)

    async def update_category(self, category_id: str, category_in: CategoryUpdate) -> CategoryInDB:
        category = await self.repository.get(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )

        update_data = category_in.dict(exclude_unset=True)
        updated_category = await self.repository.update(category_id, update_data)
        return CategoryInDB.from_orm(updated_category)

    async def delete_category(self, category_id: str) -> bool:
        category = await self.repository.get(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        return await self.repository.delete(category_id)