from sqlalchemy import Column, String, Boolean, DateTime, CHAR, Text
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid
from app.models.user import User


class Wishlist(BaseModel):
    """Wishlist model for user wishlists"""
    __tablename__ = "wishlists"

    # Wishlist details
    name = Column(String(255), nullable=False, default="My Wishlist")
    description = Column(Text, nullable=True)
    is_default = Column(Boolean, default=False, nullable=False)

    # Foreign keys
    user_id = Column(CHAR(32), ForeignKey("users.id"), nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="wishlists")
    wishlist_items = relationship("WishlistItem", back_populates="wishlist", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Wishlist(id={self.id}, user_id='{self.user_id}', name='{self.name}')>"