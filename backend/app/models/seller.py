from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Numeric, Integer, CHAR
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .product import Product
    from .user import User


class Seller(BaseModel):
    """Seller model for users who sell products"""
    __tablename__ = "sellers"

    user_id = Column(CHAR(32), ForeignKey("users.id"), nullable=False, unique=True)
    store_name = Column(String(200), nullable=False)
    store_description = Column(Text, nullable=True)
    logo_url = Column(String(500), nullable=True)
    banner_url = Column(String(500), nullable=True)
    is_approved = Column(Boolean, default=False, nullable=False)
    approval_date = Column(DateTime(timezone=True), nullable=True)
    approved_by = Column(CHAR(32), ForeignKey("users.id"), nullable=True)
    commission_rate = Column(Numeric(5, 4), default=0.10, nullable=False)  # 10% default
    payout_email = Column(String(255), nullable=True)
    payout_method = Column(String(50), nullable=True)  # bank_account, paypal, etc.
    payout_details = Column(Text, nullable=True)  # JSON string for encrypted details
    total_sales = Column(Numeric(15, 2), default=0.00, nullable=False)
    total_earnings = Column(Numeric(15, 2), default=0.00, nullable=False)
    rating_average = Column(Numeric(3, 2), default=0.00, nullable=False)
    review_count = Column(Integer, default=0, nullable=False)

    # Relationships
    user = relationship("User", back_populates="seller", foreign_keys=[user_id])
    approver = relationship("User", foreign_keys=[approved_by])
    products = relationship("Product", back_populates="seller")

    def __repr__(self):
        return f"<Seller(id={self.id}, user_id={self.user_id}, store_name='{self.store_name}')>"