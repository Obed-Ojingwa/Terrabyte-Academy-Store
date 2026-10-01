from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.cart_item import CartItem


class CartItemRepository(BaseRepository[CartItem]):
    def __init__(self, db: AsyncSession):
        super().__init__(CartItem, db)

    async def get_by_cart_id(self, cart_id: str) -> List[CartItem]:
        """Get all items for a specific cart"""
        result = await self.db.execute(
            select(CartItem)
            .where(CartItem.cart_id == cart_id)
        )
        return result.scalars().all()

    async def get_by_product_id(self, product_id: str) -> List[CartItem]:
        """Get all cart items for a specific product"""
        result = await self.db.execute(
            select(CartItem)
            .where(CartItem.product_id == product_id)
        )
        return result.scalars().all()

    async def get_by_cart_and_product(
        self,
        cart_id: str,
        product_id: str
    ) -> Optional[CartItem]:
        """Get a specific cart item by cart and product IDs"""
        result = await self.db.execute(
            select(CartItem)
            .where(
                and_(
                    CartItem.cart_id == cart_id,
                    CartItem.product_id == product_id
                )
            )
        )
        return result.scalar_one_or_none()