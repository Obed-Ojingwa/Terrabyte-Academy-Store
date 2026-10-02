from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.base import BaseSchema
from datetime import datetime
from app.models.coupon import DiscountTypeEnum


class CouponBase(BaseSchema):
    code: str = Field(max_length=50)
    description: Optional[str] = None
    discount_type: DiscountTypeEnum
    discount_value: float
    minimum_purchase: float = 0.0
    maximum_discount: Optional[float] = None
    usage_limit: Optional[int] = None
    usage_count: int = 0
    usage_limit_per_user: int = 1
    starts_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    applies_to_all_products: bool = True
    is_active: bool = True


class CouponCreate(CouponBase):
    pass


class CouponUpdate(BaseSchema):
    code: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    discount_type: Optional[DiscountTypeEnum] = None
    discount_value: Optional[float] = None
    minimum_purchase: Optional[float] = None
    maximum_discount: Optional[float] = None
    usage_limit: Optional[int] = None
    usage_count: Optional[int] = None
    usage_limit_per_user: Optional[int] = None
    starts_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    applies_to_all_products: Optional[bool] = None
    is_active: Optional[bool] = None


class CouponInDB(CouponBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CouponWithUsage(CouponInDB):
    # We could add usage records if we had a coupon usage model
    pass

    class Config:
        orm_mode = True