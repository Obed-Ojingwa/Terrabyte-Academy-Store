from sqlalchemy import Column, DateTime, ForeignKey, String, Text, CHAR, Boolean
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid
from datetime import datetime


class Cart(BaseModel):
    """Shopping cart model for anonymous and authenticated users"""
    __tablename__ = "carts"

    # Cart identifier for anonymous users (session-based)
    session_id = Column(String(255), nullable=True, index=True)

    # Link to user for authenticated users (nullable for anonymous carts)
    user_id = Column(CHAR(32), ForeignKey("users.id"), nullable=True, index=True)

    # Cart status
    is_active = Column(Boolean, default=True, nullable=False)
    is_checked_out = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="cart")
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Cart(id={self.id}, user_id={self.user_id}, session_id={self.session_id})>"