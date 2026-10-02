from app.services.base import BaseService
from app.repositories.faq_repository import FAQRepository
from app.schemas.faq import FAQCreate, FAQUpdate, FAQInDB, FAQWithCategory
from app.models.faq import FAQ
from typing import List, Optional
from fastapi import HTTPException, status


class FAQService(BaseService[FAQRepository]):
    def __init__(self, faq_repository: FAQRepository):
        super().__init__(faq_repository)
        self.repository = faq_repository

    async def get(self, faq_id: str) -> FAQInDB:
        faq = await self.repository.get(faq_id)
        if not faq:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="FAQ not found"
            )
        return FAQInDB.from_orm(faq)

    async def get_by_category(self, category_id: str, skip: int = 0, limit: int = 100) -> List[FAQInDB]:
        faqs = await self.repository.get_by_category(category_id, skip=skip, limit=limit)
        return [FAQInDB.from_orm(faq) for faq in faqs]

    async def get_active_faqs(self, skip: int = 0, limit: int = 100) -> List[FAQInDB]:
        faqs = await self.repository.get_active_faqs(skip=skip, limit=limit)
        return [FAQInDB.from_orm(faq) for faq in faqs]

    async def get_featured_faqs(self, skip: int = 0, limit: int = 100) -> List[FAQInDB]:
        faqs = await self.repository.get_featured_faqs(skip=skip, limit=limit)
        return [FAQInDB.from_orm(faq) for faq in faqs]

    async def get_popular_faqs(self, skip: int = 0, limit: int = 100) -> List[FAQInDB]:
        faqs = await self.repository.get_popular_faqs(skip=skip, limit=limit)
        return [FAQInDB.from_orm(faq) for faq in faqs]

    async def create_faq(self, faq_in: FAQCreate) -> FAQInDB:
        faq = await self.repository.create(faq_in.dict())
        return FAQInDB.from_orm(faq)

    async def update_faq(self, faq_id: str, faq_in: FAQUpdate) -> FAQInDB:
        faq = await self.repository.get(faq_id)
        if not faq:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="FAQ not found"
            )

        update_data = faq_in.dict(exclude_unset=True)
        updated_faq = await self.repository.update(faq_id, update_data)
        return FAQInDB.from_orm(updated_faq)

    async def delete_faq(self, faq_id: str) -> bool:
        faq = await self.repository.get(faq_id)
        if not faq:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="FAQ not found"
            )
        return await self.repository.delete(faq_id)