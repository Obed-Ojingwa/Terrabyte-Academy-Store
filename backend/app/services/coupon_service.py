from typing import List, Optional
from app.services.base import BaseService
from app.repositories.coupon_repository import CouponRepository
from app.schemas.coupon import CouponCreate, CouponUpdate, CouponInDB
from app.models.coupon import Coupon, DiscountTypeEnum
from fastapi import HTTPException, status
from datetime import datetime

class CouponService(BaseService[CouponRepository]):
    def __init__(self, coupon_repository: CouponRepository):
        super().__init__(coupon_repository)
        self.repository = coupon_repository

    async def get(self, coupon_id: str) -> CouponInDB:
        coupon = await self.repository.get(coupon_id)
        if not coupon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Coupon not found"
            )
        return CouponInDB.from_orm(coupon)

    async def get_by_code(self, code: str) -> CouponInDB:
        coupon = await self.repository.get_by_code(code)
        if not coupon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Coupon not found"
            )
        return CouponInDB.from_orm(coupon)

    async def get_active_coupons(self, skip: int = 0, limit: int = 100) -> List[CouponInDB]:
        coupons = await self.repository.get_active_coupons(skip, limit)
        return [CouponInDB.from_orm(c) for c in coupons]

    async def create(self, coupon_in: CouponCreate) -> CouponInDB:
        # Check if coupon code already exists
        existing_coupon = await self.repository.get_by_code(coupon_in.code)
        if existing_coupon:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coupon with this code already exists"
            )
        coupon_data = coupon_in.dict()
        created_coupon = await self.repository.create(coupon_data)
        return CouponInDB.from_orm(created_coupon)

    async def update(self, coupon_id: str, coupon_in: CouponUpdate) -> CouponInDB:
        coupon = await self.repository.get(coupon_id)
        if not coupon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Coupon not found"
            )
        update_data = coupon_in.dict(exclude_unset=True)
        # If code is being updated, check for uniqueness
        if "code" in update_data:
            existing_coupon = await self.repository.get_by_code(update_data["code"])
            if existing_coupon and existing_coupon.id != coupon_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Coupon with this code already exists"
                )
        updated_coupon = await self.repository.update(coupon_id, update_data)
        if not updated_coupon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Coupon not found"
            )
        return CouponInDB.from_orm(updated_coupon)

    async def delete(self, coupon_id: str) -> bool:
        coupon = await self.repository.get(coupon_id)
        if not coupon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Coupon not found"
            )
        return await self.repository.delete(coupon_id)

    async def validate_coupon(
        self,
        code: str,
        user_id: Optional[str] = None,
        purchase_amount: float = 0.0
    ) -> tuple[bool, Optional[str], float]:
        """
        Validate a coupon for a given user and purchase amount.
        Returns a tuple of (is_valid, error_message, discount_amount)
        """
        coupon = await self.repository.get_by_code(code)
        if not coupon:
            return False, "Coupon not found", 0.0

        if not coupon.is_active:
            return False, "Coupon is not active", 0.0

        now = datetime.utcnow()
        if coupon.starts_at and coupon.starts_at > now:
            return False, "Coupon is not yet active", 0.0
        if coupon.expires_at and coupon.expires_at < now:
            return False, "Coupon has expired", 0.0

        if purchase_amount < coupon.minimum_purchase:
            return False, f"Minimum purchase amount of {coupon.minimum_purchase} not met", 0.0

        # TODO: Check usage limits per user and total usage limit
        # For now, we'll skip these checks as they require additional tables or fields.
        # We would need to track coupon usage per user and total usage.

        # Calculate discount amount
        discount_amount = 0.0
        if coupon.discount_type == DiscountTypeEnum.PERCENTAGE:
            discount_amount = purchase_amount * (coupon.discount_value / 100)
            if coupon.maximum_discount and discount_amount > coupon.maximum_discount:
                discount_amount = coupon.maximum_discount
        elif coupon.discount_type == DiscountTypeEnum.FIXED_AMOUNT:
            discount_amount = coupon.discount_value
            if discount_amount > purchase_amount:
                discount_amount = purchase_amount
        elif coupon.discount_type == DiscountTypeEnum.FREE_SHIPPING:
            # For free shipping, we would need to know the shipping cost.
            # For now, we'll set discount to 0 and handle it elsewhere.
            discount_amount = 0.0

        return True, None, discount_amount