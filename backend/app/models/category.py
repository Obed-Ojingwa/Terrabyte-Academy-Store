from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer, CHAR
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .product import Product
    from .service import Service  # We'll create this later


class Category(BaseModel):
    """Category model for products and services"""
    __tablename__ = "categories"

    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    parent_id = Column(CHAR(32), ForeignKey("categories.id"), nullable=True)
    slug = Column(String(200), unique=True, nullable=False, index=True)
    icon_url = Column(String(500), nullable=True)
    image_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)

    # Self-referential relationships (using string references to avoid circular imports)
    parent = relationship("Category", remote_side="[Category.id]", back_populates="children")
    children = relationship("Category", back_populates="parent")

    # Relationships with products and services (using string references)
    products = relationship("Product", back_populates="category")
    services = relationship("Service", back_populates="category")  # Will be defined in service.py

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}', slug='{self.slug}')>"