from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.payment import Payment


class PaymentRepository(BaseRepository[Payment]):
    def __init__(self, db: AsyncSession):
        super().__init__(Payment, db)

    async def get_by_order_id(self, order_id: str) -> List[Payment]:
        """Get all payments for a specific order"""
        result = await self.db.execute(
            select(Payment)
            .where(Payment.order_id == order_id)
        )
        return result.scalars().all()

    async def get_by_transaction_id(self, transaction_id: str) -> Optional[Payment]:
        """Get payment by transaction ID"""
        result = await self.db.execute(
            select(Payment)
            .where(Payment.transaction_id == transaction_id)
        )
        return result.scalar_one_or_none()