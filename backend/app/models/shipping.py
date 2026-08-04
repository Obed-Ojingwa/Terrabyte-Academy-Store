from sqlalchemy import Column, Integer, ForeignKey, CHAR, DateTime, Enum, Numeric, String, Text
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid
import enum

from app.models.order import Order
from app.models.address import Address


class ShippingStatusEnum(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    RETURNED = "returned"
    LOST = "lost"
    DAMAGED = "damaged"


class ShippingMethodEnum(enum.Enum):
    STANDARD = "standard"
    EXPRESS = "express"
    OVERNIGHT = "overnight"
    SAME_DAY = "same_day"
    INTERNATIONAL = "international"
    FREE = "free"
    PICKUP = "pickup"


class Shipping(BaseModel):
    """Shipping model for tracking shipments"""
    __tablename__ = "shippings"

    # Shipping details
    shipping_method = Column(Enum(ShippingMethodEnum), nullable=False)
    shipping_cost = Column(Numeric(10, 2), nullable=False, default=0.00)
    tracking_number = Column(String(100), unique=True, nullable=True, index=True)
    carrier = Column(String(100), nullable=True)  # e.g., "UPS", "FedEx", "USPS", "DHL"
    estimated_delivery_date = Column(DateTime(timezone=True), nullable=True)
    actual_delivery_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum(ShippingStatusEnum), default=ShippingStatusEnum.PENDING, nullable=False)

    # Timestamps
    shipped_at = Column(DateTime(timezone=True), nullable=True)
    delivered_at = Column(DateTime(timezone=True), nullable=True)

    # Foreign keys
    order_id = Column(CHAR(32), ForeignKey("orders.id"), nullable=False)
    shipping_address_id = Column(CHAR(32), ForeignKey("addresses.id"), nullable=False)

    # Relationships
    order = relationship("Order", back_populates="shipping")
    shipping_address = relationship("Address")

    def __repr__(self):
        return f"<Shipping(id={self.id}, tracking_number='{self.tracking_number}', status='{self.status.value}')>"