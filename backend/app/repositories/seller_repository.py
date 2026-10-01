from app.repositories.base import BaseRepository
from app.models.seller import Seller
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from sqlalchemy import select, update
import uuid
from datetime import datetime


class SellerRepository(BaseRepository[Seller]):
    def __init__(self, db: AsyncSession):
        super().__init__(Seller, db)

    async def get_by_user_id(self, user_id: str) -> Optional[Seller]:
        result = await self.db.execute(
            select(Seller).where(Seller.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, id: str) -> Optional[Seller]:
        result = await self.db.execute(
            select(Seller).where(Seller.id == id)
        )
        return result.scalar_one_or_none()

    async def get_pending_approvals(self) -> List[Seller]:
        result = await self.db.execute(
            select(Seller).where(Seller.is_approved == False)
        )
        return result.scalars().all()

    async def get_approved_sellers(self) -> List[Seller]:
        result = await self.db.execute(
            select(Seller).where(Seller.is_approved == True)
        )
        return result.scalars().all()

    async def approve_seller(self, seller_id: str, approved_by: str) -> None:
        await self.db.execute(
            update(Seller)
            .where(Seller.id == seller_id)
            .values(is_approved=True, approval_date=datetime.utcnow(), approved_by=approved_by)
        )
        await self.db.commit()

    async def update_sales_and_earnings(self, seller_id: str, sales_amount: float, earnings_amount: float) -> None:
        # Get current seller to update totals
        seller = await self.get_by_id(seller_id)
        if seller:
            new_total_sales = float(seller.total_sales) + sales_amount
            new_total_earnings = float(seller.total_earnings) + earnings_amount
            await self.db.execute(
                update(Seller)
                .where(Seller.id == seller_id)
                .values(total_sales=new_total_sales, total_earnings=new_total_earnings)
            )
            await self.db.commit()
