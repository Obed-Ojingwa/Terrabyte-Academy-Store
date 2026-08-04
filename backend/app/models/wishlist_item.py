from sqlalchemy import Column, Integer, ForeignKey, CHAR
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid
from app.models.product import Product


class WishlistItem(BaseModel):
    """Wishlist item model for user wishlists"""
    __tablename__ = "wishlist_items"

    # We'll add more fields like added_at, etc. later

    # Foreign keys
    product_id = Column(CHAR(32), ForeignKey("products.id"), nullable=False)

    # Relationships
    product = relationship("Product", back_populates="wishlist_items")

    def __repr__(self):
        return f"<WishlistItem(id={self.id}, product_id='{self.product_id}')>"