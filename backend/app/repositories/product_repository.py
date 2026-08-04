from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.product import Product

class ProductRepository(BaseRepository[Product]):
    def __init__(self, db: AsyncSession):
        super().__init__(Product, db)

    async def get_by_sku(self, sku: str) -> Optional[Product]:
        result = await self.db.execute(select(Product).where(Product.sku == sku))
        return result.scalar_one_or_none()

    async def get_active_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        result = await self.db.execute(
            select(Product)
            .where(Product.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_products_by_category(self, category_id: str, skip: int = 0, limit: int = 100) -> List[Product]:
        result = await self.db.execute(
            select(Product)
            .where(
                and_(
                    Product.category_id == category_id,
                    Product.is_active == True
                )
            )
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_featured_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        result = await self.db.execute(
            select(Product)
            .where(
                and_(
                    Product.is_featured == True,
                    Product.is_active == True
                )
            )
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_featured_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        result = await self.db.execute(
            select(Product)
            .where(and_(Product.is_featured == True, Product.is_active == True))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()