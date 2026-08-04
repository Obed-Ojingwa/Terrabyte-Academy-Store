from sqlalchemy import Column, Integer, ForeignKey, CHAR
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid
from app.models.product import Product


class CartItem(BaseModel):
    """Cart item model for shopping cart"""
    __tablename__ = "cart_items"

    quantity = Column(Integer, nullable=False, default=1)

    # Foreign keys
    product_id = Column(CHAR(32), ForeignKey("products.id"), nullable=False)

    # Relationships
    product = relationship("Product", back_populates="cart_items")

    def __repr__(self):
        return f"<CartItem(id={self.id}, product_id='{self.product_id}', quantity={self.quantity})>"