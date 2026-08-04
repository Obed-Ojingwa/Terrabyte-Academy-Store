from sqlalchemy import Column, Integer, ForeignKey, CHAR, DateTime
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid

from app.models.product import Product


class Inventory(BaseModel):
    """Inventory model for tracking product stock levels"""
    __tablename__ = "inventory"

    # Inventory details
    quantity_on_hand = Column(Integer, nullable=False, default=0)
    reserved_quantity = Column(Integer, nullable=False, default=0)  # Items reserved in carts but not yet purchased
    reorder_point = Column(Integer, nullable=False, default=5)  # When to reorder
    reorder_quantity = Column(Integer, nullable=False, default=50)  # How much to reorder

    # Timestamps
    last_restocked_at = Column(DateTime(timezone=True), nullable=True)
    last_checked_at = Column(DateTime(timezone=True), nullable=True)

    # Foreign keys
    product_id = Column(CHAR(32), ForeignKey("products.id"), nullable=False, unique=True, index=True)

    # Relationships
    product = relationship("Product", back_populates="inventory")

    @property
    def available_quantity(self):
        """Calculate available quantity (what's actually available for sale)"""
        return max(0, self.quantity_on_hand - self.reserved_quantity)

    def __repr__(self):
        return f"<Inventory(id={self.id}, product_id='{self.product_id}', quantity_on_hand={self.quantity_on_hand})>"