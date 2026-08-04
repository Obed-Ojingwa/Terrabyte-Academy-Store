"""
Tests for the authentication API endpoints.
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient, db: AsyncSession):
    """Test user registration endpoint."""
    # Arrange
    user_data = {
        "email": "newuser@example.com",
        "password": "securepassword123",
        "first_name": "New",
        "last_name": "User"
    }

    # Act
    response = await client.post("/api/v1/auth/register", json=user_data)

    # Debug: print response if not successful
    if response.status_code != 200:
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.json()}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data  # Depending on your implementation

    # Verify user was created in database
    from sqlalchemy import select
    result = await db.execute(select(User).where(User.email == user_data["email"]))
    db_user = result.scalar_one_or_none()
    assert db_user is not None
    assert db_user.email == user_data["email"]
    assert db_user.is_active == True


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient, db: AsyncSession):
    """Test registration fails with duplicate email."""
    # Arrange - Create a user first
    existing_user = User(
        email="duplicate@example.com",
        password_hash="hashed_password",
        is_active=True
    )
    db.add(existing_user)
    await db.commit()

    # Attempt to register with same email
    user_data = {
        "email": "duplicate@example.com",
        "password": "anotherpassword",
        "first_name": "Duplicate",
        "last_name": "User"
    }

    # Act
    response = await client.post("/api/v1/auth/register", json=user_data)

    # Assert
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient, db: AsyncSession):
    """Test user login endpoint."""
    # Arrange - Create a user
    user = User(
        email="login@example.com",
        password_hash="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # bcrypt hash of "secret"
        is_active=True
    )
    db.add(user)
    await db.commit()

    # Act
    login_data = {
        "username": "login@example.com",  # OAuth2PasswordRequestForm uses "username"
        "password": "secret"
    }
    response = await client.post("/api/v1/auth/login", data=login_data)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient, db: AsyncSession):
    """Test login fails with invalid credentials."""
    # Arrange - Create a user
    user = User(
        email="login@example.com",
        password_hash="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # bcrypt hash of "secret"
        is_active=True
    )
    db.add(user)
    await db.commit()

    # Act
    login_data = {
        "username": "login@example.com",
        "password": "wrongpassword"
    }
    response = await client.post("/api/v1/auth/login", data=login_data)

    # Assert
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


@pytest.mark.asyncio
async def test_refresh_token(client: AsyncClient, db: AsyncSession):
    """Test token refresh endpoint."""
    # This test would require creating a user, logging in to get a refresh token,
    # then using that token to get a new access token.
    # For simplicity, we're testing the endpoint structure.

    # First, create and login a user to get a refresh token
    user = User(
        email="refreshtest@example.com",
        password_hash="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # bcrypt hash of "secret"
        is_active=True
    )
    db.add(user)
    await db.commit()

    # Login to get tokens
    login_data = {
        "username": "refreshtest@example.com",
        "password": "secret"
    }
    login_response = await client.post("/api/v1/auth/login", data=login_data)
    assert login_response.status_code == 200
    tokens = login_response.json()
    refresh_token = tokens["refresh_token"]

    # Now use the refresh token
    response = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_verify_email_endpoint(client: AsyncClient, db: AsyncSession):
    """Test email verification endpoint."""
    # This would require creating a user with a verification token
    # For now, we'll test that the endpoint exists and returns appropriate errors

    # Test with invalid token
    response = await client.get("/api/v1/auth/verify-email?token=invalid-token")
    assert response.status_code == 400
    assert "Invalid or expired token" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_current_user_info(client: AsyncClient, db: AsyncSession):
    """Test getting current user info endpoint."""
    # First, create and login a user to get an access token
    user = User(
        email="currentuser@example.com",
        password_hash="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # bcrypt hash of "secret"
        is_active=True
    )
    db.add(user)
    await db.commit()

    # Login to get token
    login_data = {
        "username": "currentuser@example.com",
        "password": "secret"
    }
    login_response = await client.post("/api/v1/auth/login", data=login_data)
    assert login_response.status_code == 200
    tokens = login_response.json()
    access_token = tokens["access_token"]

    # Now get user info
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "currentuser@example.com"
    assert data["is_active"] == True


@pytest.mark.asyncio
async def test_get_current_user_info_unauthorized(client: AsyncClient):
    """Test getting current user info without authentication."""
    # Act
    response = await client.get("/api/v1/auth/me")

    # Assert
    assert response.status_code == 401  # Unauthorized


@pytest.mark.asyncio
async def test_logout(client: AsyncClient):
    """Test logout endpoint."""
    # The logout endpoint is primarily for client-side token removal
    # but we can test that it returns successfully

    # Act
    response = await client.post("/api/v1/auth/logout")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully logged out"