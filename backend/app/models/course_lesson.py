from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, CHAR, Integer
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid
from datetime import datetime


class CourseLesson(BaseModel):
    """Course lesson model for individual lessons within modules"""
    __tablename__ = "course_lessons"

    # Lesson details
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    content_type = Column(String(50), nullable=False)  # video, text, quiz, assignment
    content_url = Column(String(500), nullable=True)   # URL to content (video, document, etc.)
    content_text = Column(Text, nullable=True)         # Direct text content
    order_index = Column(Integer, nullable=False)      # Order within module
    duration_minutes = Column(Integer, nullable=True)  # Estimated duration in minutes
    is_required = Column(Boolean, default=True, nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign keys
    module_id = Column(CHAR(32), ForeignKey("course_modules.id"), nullable=False)

    # Relationships
    module = relationship("CourseModule", back_populates="lessons")

    def __repr__(self):
        return f"<CourseLesson(id={self.id}, title='{self.title}', module_id='{self.module_id}')>"