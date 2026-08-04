from sqlalchemy import Column, Integer, ForeignKey, CHAR, DateTime, Enum, Numeric, String, Text
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid
import enum

from app.models.user import User
from app.models.address import Address
from app.models.order_item import OrderItem


class OrderStatusEnum(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class Order(BaseModel):
    """Order model representing a customer's order"""
    __tablename__ = "orders"

    # Order details
    order_number = Column(String(20), unique=True, nullable=False, index=True)
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.PENDING, nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False, default=0.00)
    tax_amount = Column(Numeric(10, 2), nullable=False, default=0.00)
    shipping_amount = Column(Numeric(10, 2), nullable=False, default=0.00)
    discount_amount = Column(Numeric(10, 2), nullable=False, default=0.00)
    total_amount = Column(Numeric(10, 2), nullable=False, default=0.00)
    currency = Column(String(3), nullable=False, default="USD")
    notes = Column(Text, nullable=True)

    # Timestamps
    placed_at = Column(DateTime(timezone=True), nullable=True)
    shipped_at = Column(DateTime(timezone=True), nullable=True)
    delivered_at = Column(DateTime(timezone=True), nullable=True)
    cancelled_at = Column(DateTime(timezone=True), nullable=True)

    # Foreign keys
    user_id = Column(CHAR(32), ForeignKey("users.id"), nullable=False)
    billing_address_id = Column(CHAR(32), ForeignKey("addresses.id"), nullable=False)
    shipping_address_id = Column(CHAR(32), ForeignKey("addresses.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="orders")
    billing_address = relationship("Address", foreign_keys=[billing_address_id])
    shipping_address = relationship("Address", foreign_keys=[shipping_address_id])
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="order", cascade="all, delete-orphan")
    shipping = relationship("Shipping", back_populates="order", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Order(id={self.id}, order_number='{self.order_number}', status='{self.status.value}')>"