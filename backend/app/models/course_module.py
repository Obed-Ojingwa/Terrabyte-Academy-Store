from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, CHAR, Integer
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid
from datetime import datetime


class CourseModule(BaseModel):
    """Course module model for structuring course content"""
    __tablename__ = "course_modules"

    # Module details
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, nullable=False)  # Order within course
    duration_minutes = Column(Integer, nullable=True)  # Estimated duration in minutes

    # Timestamps
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign keys
    course_id = Column(CHAR(32), ForeignKey("courses.id"), nullable=False)

    # Relationships
    course = relationship("Course", back_populates="modules")
    lessons = relationship("CourseLesson", back_populates="module", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<CourseModule(id={self.id}, title='{self.title}', course_id='{self.course_id}')>"