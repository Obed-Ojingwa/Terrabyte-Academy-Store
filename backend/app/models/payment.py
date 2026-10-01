from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, CHAR, Enum
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid
import enum
from datetime import datetime


class PaymentStatusEnum(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class Payment(BaseModel):
    """Payment model for order payments"""
    __tablename__ = "payments"

    # Payment details
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), nullable=False, default="USD")
    status = Column(Enum(PaymentStatusEnum), default=PaymentStatusEnum.PENDING, nullable=False)
    payment_method = Column(String(50), nullable=False)  # credit_card, paypal, etc.
    transaction_id = Column(String(255), unique=True, nullable=True, index=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    paid_at = Column(DateTime(timezone=True), nullable=True)

    # Foreign keys
    order_id = Column(CHAR(32), ForeignKey("orders.id"), nullable=False)

    # Relationships
    order = relationship("Order", back_populates="payments")

    def __repr__(self):
        return f"<Payment(id={self.id}, order_id='{self.order_id}', amount={self.amount}, status='{self.status.value}')>"