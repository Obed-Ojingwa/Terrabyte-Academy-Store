from sqlalchemy import Column, String, Text, Integer
from sqlalchemy.orm import relationship
from app.db.base import BaseModel


class BlogTag(BaseModel):
    """Blog tag model for categorizing blog posts"""
    __tablename__ = "blog_tags"

    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    color = Column(String(7), nullable=True)  # Hex color code for UI
    usage_count = Column(Integer, default=0, nullable=False)

    # Relationships
    blog_posts = relationship("BlogPost", secondary="blog_post_tags", back_populates="tags")

    def __repr__(self):
        return f"<BlogTag(id={self.id}, name='{self.name}')>"