from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.coupon import Coupon
from datetime import datetime

class CouponRepository(BaseRepository[Coupon]):
    def __init__(self, db: AsyncSession):
        super().__init__(Coupon, db)

    async def get_by_code(self, code: str) -> Optional[Coupon]:
        result = await self.db.execute(
            select(Coupon).where(Coupon.code == code)
        )
        return result.scalar_one_or_none()

    async def get_active_coupons(self, skip: int = 0, limit: int = 100) -> List[Coupon]:
        now = datetime.utcnow()
        result = await self.db.execute(
            select(Coupon)
            .where(
                and_(
                    Coupon.is_active == True,
                    Coupon.starts_at <= now if Coupon.starts_at is not None else True,
                    Coupon.expires_at >= now if Coupon.expires_at is not None else True,
                )
            )
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()