from sqlalchemy import Column, Integer, ForeignKey, CHAR, DateTime, Enum, Numeric, String, Text, Boolean
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid
import enum

from app.models.order import Order


class PaymentStatusEnum(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"
    CANCELLED = "cancelled"


class PaymentMethodEnum(enum.Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    STRIPE = "stripe"
    BANK_TRANSFER = "bank_transfer"
    CASH_ON_DELIVERY = "cash_on_delivery"
    WALLET = "wallet"


class Payment(BaseModel):
    """Payment model for processing payments"""
    __tablename__ = "payments"

    # Payment details
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), nullable=False, default="USD")
    status = Column(Enum(PaymentStatusEnum), default=PaymentStatusEnum.PENDING, nullable=False)
    method = Column(Enum(PaymentMethodEnum), nullable=False)
    payment_gateway = Column(String(100), nullable=True)  # e.g., "stripe", "paypal", etc.
    transaction_id = Column(String(255), unique=True, nullable=True, index=True)  # Gateway transaction ID
    gateway_response = Column(Text, nullable=True)  # Store raw gateway response for debugging
    failure_reason = Column(Text, nullable=True)

    # Timestamps
    processed_at = Column(DateTime(timezone=True), nullable=True)

    # Foreign keys
    order_id = Column(CHAR(32), ForeignKey("orders.id"), nullable=False)

    # Relationships
    order = relationship("Order", back_populates="payments")

    def __repr__(self):
        return f"<Payment(id={self.id}, amount='{self.amount}', status='{self.status.value}', method='{self.method.value}')>"