from sqlalchemy import Column, CHAR, ForeignKey, Table
from app.db.base import BaseModel
import uuid


# Association table for product and product_tag
product_tag = Table(
    'product_tag',
    BaseModel.metadata,
    Column('product_id', CHAR(32), ForeignKey('products.id'), primary_key=True),
    Column('tag_id', CHAR(32), ForeignKey('tags.id'), primary_key=True)
)