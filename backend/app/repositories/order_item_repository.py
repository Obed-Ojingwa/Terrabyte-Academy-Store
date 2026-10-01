from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.order_item import OrderItem


class OrderItemRepository(BaseRepository[OrderItem]):
    def __init__(self, db: AsyncSession):
        super().__init__(OrderItem, db)

    async def get_by_order_id(self, order_id: str) -> List[OrderItem]:
        """Get all items for a specific order"""
        result = await self.db.execute(
            select(OrderItem)
            .where(OrderItem.order_id == order_id)
        )
        return result.scalars().all()

    async def get_by_product_id(self, product_id: str) -> List[OrderItem]:
        """Get all order items for a specific product"""
        result = await self.db.execute(
            select(OrderItem)
            .where(OrderItem.product_id == product_id)
        )
        return result.scalars().all()