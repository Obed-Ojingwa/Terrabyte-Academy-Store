from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer, CHAR
from sqlalchemy.orm import relationship
from app.db.base import BaseModel


class ProductImage(BaseModel):
    """Product image model"""
    __tablename__ = "product_images"

    product_id = Column(CHAR(32), ForeignKey("products.id"), nullable=False)
    url = Column(String(500), nullable=False)
    alt_text = Column(String(255), nullable=True)
    is_primary = Column(Boolean, default=False, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)

    # Relationship
    product = relationship("Product", back_populates="images")

    def __repr__(self):
        return f"<ProductImage(id={self.id}, product_id={self.product_id}, url='{self.url}')>"