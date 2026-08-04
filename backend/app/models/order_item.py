from sqlalchemy import Column, Integer, ForeignKey, CHAR, Numeric
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid
from app.models.product import Product


class OrderItem(BaseModel):
    """Order item model for order details"""
    __tablename__ = "order_items"

    quantity = Column(Integer, nullable=False, default=1)
    price_at_purchase = Column(Numeric(10, 2), nullable=False)  # Price at time of purchase

    # Foreign keys
    product_id = Column(CHAR(32), ForeignKey("products.id"), nullable=False)
    order_id = Column(CHAR(32), ForeignKey("orders.id"), nullable=False)

    # Relationships
    product = relationship("Product", back_populates="order_items")
    order = relationship("Order", back_populates="order_items")

    def __repr__(self):
        return f"<OrderItem(id={self.id}, product_id='{self.product_id}', quantity={self.quantity})>"