from typing import List, Optional
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.order import Order


class OrderRepository(BaseRepository[Order]):
    def __init__(self, db: AsyncSession):
        super().__init__(Order, db)

    async def get_by_user_id(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Order]:
        """Get orders for a specific user"""
        result = await self.db.execute(
            select(Order)
            .where(Order.user_id == user_id)
            .order_by(desc(Order.created_at))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_recent_orders(
        self,
        limit: int = 50
    ) -> List[Order]:
        """Get recent orders (for admin/dashboard use)"""
        result = await self.db.execute(
            select(Order)
            .order_by(desc(Order.created_at))
            .limit(limit)
        )
        return result.scalars().all()

    async def get_orders_by_status(
        self,
        status: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Order]:
        """Get orders by status"""
        result = await self.db.execute(
            select(Order)
            .where(Order.status == status)
            .order_by(desc(Order.created_at))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def update_order_status(
        self,
        order_id: str,
        status: str
    ) -> Optional[Order]:
        """Update order status"""
        order = await self.get(order_id)
        if order:
            order.status = status
            # Update relevant timestamp based on status
            from datetime import datetime
            now = datetime.utcnow()
            if status == "shipped":
                order.shipped_at = now
            elif status == "delivered":
                order.delivered_at = now
            elif status == "cancelled":
                order.cancelled_at = now

            await self.db.commit()
            await self.db.refresh(order)
            return order
        return None