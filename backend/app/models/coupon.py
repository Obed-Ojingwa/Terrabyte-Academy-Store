from sqlalchemy import Column, String, Boolean, DateTime, Enum, Numeric, Integer, CHAR, Text
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid
import enum


class DiscountTypeEnum(enum.Enum):
    PERCENTAGE = "percentage"
    FIXED_AMOUNT = "fixed_amount"
    FREE_SHIPPING = "free_shipping"


class Coupon(BaseModel):
    """Coupon model for discounts and promotions"""
    __tablename__ = "coupons"

    # Coupon details
    code = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    discount_type = Column(Enum(DiscountTypeEnum), nullable=False)
    discount_value = Column(Numeric(10, 2), nullable=False)  # Percentage or fixed amount
    minimum_purchase = Column(Numeric(10, 2), nullable=False, default=0.00)
    maximum_discount = Column(Numeric(10, 2), nullable=True)  # For percentage discounts

    # Usage limits
    usage_limit = Column(Integer, nullable=True)  # Total usage limit
    usage_count = Column(Integer, nullable=False, default=0)
    usage_limit_per_user = Column(Integer, nullable=True, default=1)  # Per user limit

    # Validity period
    starts_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)

    # Applicability
    applies_to_all_products = Column(Boolean, nullable=False, default=True)
    # We could add relationships to specific products/categories if needed

    # Status
    is_active = Column(Boolean, nullable=False, default=True)

    # Relationships (optional: track usage)
    # usage_records = relationship("CouponUsage", back_populates="coupon")

    def __repr__(self):
        return f"<Coupon(id={self.id}, code='{self.code}', type='{self.discount_type.value}', value={self.discount_value})>"