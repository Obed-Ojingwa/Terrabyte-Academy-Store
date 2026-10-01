from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.shipping import Shipping


class ShippingRepository(BaseRepository[Shipping]):
    def __init__(self, db: AsyncSession):
        super().__init__(Shipping, db)

    async def get_by_order_id(self, order_id: str) -> Optional[Shipping]:
        """Get shipping information for a specific order"""
        result = await self.db.execute(
            select(Shipping)
            .where(Shipping.order_id == order_id)
        )
        return result.scalar_one_or_none()

    async def get_by_tracking_number(self, tracking_number: str) -> Optional[Shipping]:
        """Get shipping by tracking number"""
        result = await self.db.execute(
            select(Shipping)
            .where(Shipping.tracking_number == tracking_number)
        )
        return result.scalar_one_or_none()