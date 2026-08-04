from sqlalchemy import Column, Integer, ForeignKey, CHAR
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid
from app.models.product import Product


class OrderItem(BaseModel):
    """Order item model for order details"""
    __tablename__ = "order_items"

    quantity = Column(Integer, nullable=False, default=1)
    # We'll add more fields like price_at_purchase, etc. later

    # Foreign keys
    product_id = Column(CHAR(32), ForeignKey("products.id"), nullable=False)

    # Relationships
    product = relationship("Product", back_populates="order_items")

    def __repr__(self):
        return f"<OrderItem(id={self.id}, product_id='{self.product_id}', quantity={self.quantity})>"