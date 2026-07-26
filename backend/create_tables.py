#!/usr/bin/env python3
"""
Script to create database tables directly using SQLAlchemy
"""
from app.db.base import Base
from app.models import user, profile, role, category, product, product_image, product_tag, tag, address, seller  # noqa
from app.core.config import settings
from sqlalchemy import create_engine

def create_tables():
    # Create engine
    engine = create_engine(settings.DATABASE_URL)

    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()