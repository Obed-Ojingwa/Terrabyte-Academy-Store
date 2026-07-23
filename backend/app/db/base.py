from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Column, DateTime, CHAR
import uuid

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True

    id = Column(CHAR(32), primary_key=True, default=lambda: uuid.uuid4().hex, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())