from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, CHAR, Text
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid
from datetime import datetime


class Shipping(BaseModel):
    """Shipping model for order shipping"""
    __tablename__ = "shipping"

    # Shipping details
    service = Column(String(100), nullable=False)  # e.g., "Standard", "Express", "Overnight"
    cost = Column(Numeric(10, 2), nullable=False, default=0.00)
    tracking_number = Column(String(255), nullable=True, unique=True, index=True)
    tracking_url = Column(String(500), nullable=True)

    # Address information (denormalized for simplicity)
    address_line_1 = Column(String(255), nullable=False)
    address_line_2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=False)
    state_province = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    shipped_at = Column(DateTime(timezone=True), nullable=True)
    delivered_at = Column(DateTime(timezone=True), nullable=True)

    # Foreign keys
    order_id = Column(CHAR(32), ForeignKey("orders.id"), nullable=False)

    # Relationships
    order = relationship("Order", back_populates="shipping")

    def __repr__(self):
        return f"<Shipping(id={self.id}, order_id='{self.order_id}', service='{self.service}', tracking_number='{self.tracking_number}')>"