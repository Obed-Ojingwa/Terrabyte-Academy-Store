from sqlalchemy import Column, Text, Boolean, DateTime, ForeignKey, CHAR
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid
from app.models.user import User
from app.models.blog_post import BlogPost


class BlogComment(BaseModel):
    """Blog comment model for commenting on blog posts"""
    __tablename__ = "blog_comments"

    content = Column(Text, nullable=False)
    is_approved = Column(Boolean, default=False, nullable=False)
    is_spam = Column(Boolean, default=False, nullable=False)

    # Foreign keys
    blog_post_id = Column(CHAR(32), ForeignKey("blog_posts.id"), nullable=False)
    author_id = Column(CHAR(32), ForeignKey("users.id"), nullable=False)
    parent_id = Column(CHAR(32), ForeignKey("blog_comments.id"), nullable=True)  # For replies

    # Relationships
    blog_post = relationship("BlogPost", back_populates="comments")
    author = relationship("User")
    replies = relationship("BlogComment", backref=db.backref("parent", remote_side=[id]))

    def __repr__(self):
        return f"<BlogComment(id={self.id}, blog_post_id='{self.blog_post_id}', author_id='{self.author_id}')>"