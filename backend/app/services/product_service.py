from typing import List, Optional
from app.services.base import BaseService
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate, ProductInDB
from app.models.product import Product
from fastapi import HTTPException, status

class ProductService(BaseService[ProductRepository]):
    def __init__(self, product_repository: ProductRepository):
        super().__init__(product_repository)
        self.repository = product_repository

    async def get(self, product_id: str) -> ProductInDB:
        product = await self.repository.get(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return ProductInDB.from_orm(product)

    async def get_product_by_sku(self, sku: str) -> ProductInDB:
        product = await self.repository.get_by_sku(sku)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return ProductInDB.from_orm(product)

    async def get_active_products(self, skip: int = 0, limit: int = 100) -> List[ProductInDB]:
        products = await self.repository.get_active_products(skip=skip, limit=limit)
        return [ProductInDB.from_orm(product) for product in products]

    async def get_products_by_category(self, category_id: str, skip: int = 0, limit: int = 100) -> List[ProductInDB]:
        products = await self.repository.get_products_by_category(category_id, skip=skip, limit=limit)
        return [ProductInDB.from_orm(product) for product in products]

    async def get_featured_products(self, skip: int = 0, limit: int = 100) -> List[ProductInDB]:
        products = await self.repository.get_featured_products(skip=skip, limit=limit)
        return [ProductInDB.from_orm(product) for product in products]

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
    ) -> List[ProductInDB]:
        products = await self.repository.search_products(
            search_term=search_term,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            is_featured=is_featured,
            is_active=is_active,
            skip=skip,
            limit=limit
        )
        return [ProductInDB.from_orm(product) for product in products]

    async def create_product(self, product_in: ProductCreate) -> ProductInDB:
        product = await self.repository.create(product_in.dict())
        return ProductInDB.from_orm(product)

    async def update_product(self, product_id: str, product_in: ProductUpdate) -> ProductInDB:
        product = await self.repository.get(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        update_data = product_in.dict(exclude_unset=True)
        updated_product = await self.repository.update(product_id, update_data)
        return ProductInDB.from_orm(updated_product)

    async def delete_product(self, product_id: str) -> bool:
        product = await self.repository.get(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return await self.repository.delete(product_id)