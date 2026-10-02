from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, Table, CHAR
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid
from app.models.user import User


# Association table for blog post and blog tag
blog_post_tags = Table(
    'blog_post_tags',
    BaseModel.metadata,
    Column('blog_post_id', CHAR(32), ForeignKey('blog_posts.id'), primary_key=True),
    Column('blog_tag_id', CHAR(32), ForeignKey('blog_tags.id'), primary_key=True)
)


class BlogPost(BaseModel):
    """Blog post model for content management"""
    __tablename__ = "blog_posts"

    title = Column(String(200), nullable=False, index=True)
    slug = Column(String(200), unique=True, nullable=False, index=True)
    excerpt = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    featured_image = Column(String(500), nullable=True)
    status = Column(String(20), default='draft', nullable=False)  # draft, published, archived
    is_featured = Column(Boolean, default=False, nullable=False)
    views_count = Column(Integer, default=0, nullable=False)
    published_at = Column(DateTime(timezone=True), nullable=True)

    # Foreign keys
    author_id = Column(CHAR(32), ForeignKey("users.id"), nullable=False)

    # Relationships
    author = relationship("User", back_populates="blog_posts")
    tags = relationship("BlogTag", secondary=blog_post_tags, back_populates="blog_posts")
    comments = relationship("BlogComment", back_populates="blog_post", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<BlogPost(id={self.id}, title='{self.title}', status='{self.status}')>"