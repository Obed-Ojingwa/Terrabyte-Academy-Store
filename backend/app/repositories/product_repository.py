from typing import List, Optional
from sqlalchemy import select, and_, or_
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

    async def search_products(
        self,
        search_term: Optional[str] = None,
        category_id: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        is_featured: Optional[bool] = None,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Product]:
        """
        Search products with various filters.

        Args:
            search_term: Term to search in name and description
            category_id: Filter by category ID
            min_price: Minimum price filter
            max_price: Maximum price filter
            is_featured: Filter by featured status
            is_active: Filter by active status
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Product objects matching the criteria
        """
        query = select(Product)

        # Apply search term filter
        if search_term:
            search_pattern = f"%{search_term}%"
            query = query.where(
                or_(
                    Product.name.ilike(search_pattern),
                    Product.description.ilike(search_pattern)
                )
            )

        # Apply category filter
        if category_id:
            query = query.where(Product.category_id == category_id)

        # Apply price range filters
        if min_price is not None:
            query = query.where(Product.price >= min_price)
        if max_price is not None:
            query = query.where(Product.price <= max_price)

        # Apply featured filter
        if is_featured is not None:
            query = query.where(Product.is_featured == is_featured)

        # Apply active filter
        if is_active is not None:
            query = query.where(Product.is_active == is_active)

        # Apply pagination
        query = query.offset(skip).limit(limit)

        result = await self.db.execute(query)
        return result.scalars().all()