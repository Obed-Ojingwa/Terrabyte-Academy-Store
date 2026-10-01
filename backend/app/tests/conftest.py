import asyncio
import pytest
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.main import app as fastapi_app
from app.db.session import get_db
from app.db.base import Base
import app.models  # noqa: F401

# Test database URL - using SQLite for simplicity
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def db() -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh database session for each test."""
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    async with TestingSessionLocal() as session:
        yield session

    # Drop tables after test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client(db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client with database override."""

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        try:
            yield db
        finally:
            await db.close()

    fastapi_app.dependency_overrides[get_db] = override_get_db

    # Use ASGITransport to wrap the app
    from httpx import ASGITransport

    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    fastapi_app.dependency_overrides.clear()


# Sample user data for tests
@pytest.fixture
def test_user_data():
    return {
        "email": "test@example.com",
        "password": "securepassword123",
        "first_name": "Test",
        "last_name": "User"
    }


@pytest.fixture
def test_user():
    from app.models.user import User
    return User(
        email="test@example.com",
        password_hash="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # hash of "secret"
        is_active=True,
        email_verified=True
    )


@pytest.fixture
def mock_email_service():
    """Fixture for a mocked email service."""
    from unittest.mock import MagicMock
    return MagicMock()