from sqlalchemy import Column, String, Text, Integer, Float, Boolean, DateTime, ForeignKey, JSON, CHAR
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid
from app.models.category import Category
from app.models.seller import Seller
from app.models.inventory import Inventory
from .product_tag import product_tag


class Product(BaseModel):
    """Product model for the e-commerce store"""
    __tablename__ = "products"

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    short_description = Column(String(500), nullable=True)
    sku = Column(String(100), unique=True, nullable=False, index=True)
    price = Column(Float, nullable=False)
    compare_at_price = Column(Float, nullable=True)
    cost_price = Column(Float, nullable=True)
    tax_code = Column(String(50), nullable=True)
    weight = Column(Float, nullable=True)  # Weight in kg
    dimensions = Column(JSON, nullable=True)  # {length, width, height} in cm
    stock_quantity = Column(Integer, nullable=False, default=0)
    track_quantity = Column(Boolean, default=True, nullable=False)
    allow_backorder = Column(Boolean, default=False, nullable=False)
    low_stock_threshold = Column(Integer, default=5, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    is_featured = Column(Boolean, default=False, nullable=False, index=True)
    requires_shipping = Column(Boolean, default=True, nullable=False)
    is_digital = Column(Boolean, default=False, nullable=False)
    meta_title = Column(String(60), nullable=True)
    meta_description = Column(String(160), nullable=True)

    # Foreign keys
    seller_id = Column(CHAR(32), ForeignKey("sellers.id"), nullable=False)
    category_id = Column(CHAR(32), ForeignKey("categories.id"), nullable=False)

    # Relationships
    seller = relationship("Seller", back_populates="products")
    category = relationship("Category", back_populates="products")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary=product_tag, back_populates="products")
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")
    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
    wishlist_items = relationship("WishlistItem", back_populates="product")
    inventory = relationship("Inventory", back_populates="product", uselist=False, cascade="all, delete-orphan")
    testimonials = relationship("Testimonial", back_populates="product", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', sku='{self.sku}')>"