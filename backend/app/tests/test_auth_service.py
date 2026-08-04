"""
Tests for the authentication service.
"""
import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

from app.services.auth_service import AuthService
from app.schemas.user import UserCreate, UserLogin
from app.models.user import User, UserRole
from app.core.security import create_access_token, create_refresh_token


@pytest.fixture
def mock_user_repo():
    """Fixture for a mocked user repository."""
    return AsyncMock()


@pytest.fixture
def mock_role_service():
    """Fixture for a mocked role service."""
    return AsyncMock()


@pytest.fixture
def auth_service(mock_user_repo, mock_role_service):
    """Fixture for an AuthService instance with mocked dependencies."""
    return AuthService(user_repository=mock_user_repo, role_service=mock_role_service)


@pytest.fixture
def sample_user_data():
    """Fixture for sample user data."""
    return UserCreate(
        email="test@example.com",
        password="securepassword123",
        first_name="Test",
        last_name="User"
    )


@pytest.mark.asyncio
async def test_register_user_success(auth_service, mock_user_repo, mock_role_service, sample_user_data):
    """Test successful user registration."""
    # Arrange
    mock_user_repo.get_by_email.return_value = None  # No existing user

    # Mock role service to return a customer role
    customer_role = MagicMock()
    customer_role.id = "customer-role-id"
    mock_role_service.get_role_by_name.return_value = customer_role

    # Mock user creation
    created_user = User(
        id="test-user-id",
        email=sample_user_data.email,
        is_active=True,
        role_id="customer-role-id"
    )
    mock_user_repo.create.return_value = created_user

    # Act
    result = await auth_service.register_user(sample_user_data)

    # Assert
    assert result.email == sample_user_data.email
    assert result.is_active == True
    assert result.role_id == "customer-role-id"

    # Verify that the user repository was called correctly
    mock_user_repo.get_by_email.assert_called_once_with(sample_user_data.email)
    mock_user_repo.create.assert_called_once()
    mock_user_repo.update.assert_called()  # For setting verification token
    mock_role_service.get_role_by_name.assert_called_once_with("customer")
    mock_user_repo.assign_role.assert_called_once_with(
        created_user.id, customer_role.id
    )


@pytest.mark.asyncio
async def test_register_user_email_already_exists(auth_service, mock_user_repo, sample_user_data):
    """Test registration fails when email already exists."""
    # Arrange
    existing_user = User(email=sample_user_data.email, password_hash="hashed")
    mock_user_repo.get_by_email.return_value = existing_user

    # Act & Assert
    with pytest.raises(Exception) as excpt.raises(
        Exception,  # In the actual code, this raises HTTPException
        match="Email already registered"
    ):
        await auth_service.register_user(sample_user_data)

    # Assert
    mock_user_repo.get_by_email.assert_called_once_with(sample_user_data.email)
    mock_user_repo.create.assert_not_called()


@pytest.mark.asyncio
async def test_authenticate_user_success(auth_service, mock_user_repo):
    """Test successful user authentication."""
    # Arrange
    email = "test@example.com"
    password = "correct_password"
    hashed_password = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # bcrypt hash of "secret"

    mock_user = User(
        id="test-user-id",
        email=email,
        password_hash=hashed_password,
        is_active=True
    )
    mock_user_repo.get_by_email.return_value = mock_user

    # We need to mock the verify_password function
    with patch("app.services.auth_service.verify_password") as mock_verify:
        mock_verify.return_value = True

        # Act
        result = await auth_service.authenticate_user(email, password)

        # Assert
        assert result == mock_user
        mock_user_repo.get_by_email.assert_called_once_with(email)
        mock_verify.assert_called_once_with(password, hashed_password)


@pytest.mark.asyncio
async def test_authenticate_user_invalid_password(auth_service, mock_user_repo):
    """Test authentication fails with incorrect password."""
    # Arrange
    email = "test@example.com"
    password = "wrong_password"
    hashed_password = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # bcrypt hash

    mock_user = User(
        id="test-user-id",
        email=email,
        password_hash=hashed_password,
        is_active=True
    )
    mock_user_repo.get_by_email.return_value = mock_user

    # Mock verify_password to return False
    with patch("app.services.auth_service.verify_password") as mock_verify:
        mock_verify.return_value = False

        # Act
        result = await auth_service.authenticate_user(email, password)

        # Assert
        assert result is False
        mock_user_repo.get_by_email.assert_called_once_with(email)
        mock_verify.assert_called_once_with(password, hashed_password)


@pytest.mark.asyncio
async def test_authenticate_user_not_found(auth_service, mock_user_repo):
    """Test authentication fails when user doesn't exist."""
    # Arrange
    email = "nonexistent@example.com"
    password = "any_password"
    mock_user_repo.get_by_email.return_value = None

    # Act
    result = await auth_service.authenticate_user(email, password)

    # Assert
    assert result is False
    mock_user_repo.get_by_email.assert_called_once_with(email)


@pytest.mark.asyncio
async def test_create_access_token(auth_service):
    """Test access token creation."""
    # Arrange
    user = User(id="test-user-id", email="test@example.com")

    # Act
    token = auth_service.create_access_token(user)

    # Assert
    assert isinstance(token, str)
    assert len(token) > 0
    # Note: In a real test, we would decode and verify the token


@pytest.mark.asyncio
async def test_create_refresh_token(auth_service):
    """Test refresh token creation."""
    # Arrange
    user = User(id="test-user-id", email="test@example.com")

    # Act
    token = auth_service.create_refresh_token(user)

    # Assert
    assert isinstance(token, str)
    assert len(token) > 0
    # Note: In a real test, we would decode and verify the token


@pytest.mark.asyncio
async def test_login_success(auth_service, mock_user_repo):
    """Test successful login."""
    # Arrange
    user_login = UserLogin(email="test@example.com", password="password123")
    mock_user = User(
        id="test-user-id",
        email=user_login.email,
        password_hash="hashed_password",
        is_active=True
    )
    mock_user_repo.get_by_email.return_value = mock_user

    # Mock authenticate_user to return the user
    with patch.object(AuthService, 'authenticate_user', return_value=mock_user):
        # Mock token creation methods
        with patch.object(AuthService, 'create_access_token', return_value="access-token"):
            with patch.object(AuthService, 'create_refresh_token', return_value="refresh-token"):

                # Act
                result = await auth_service.login(user_login)

                # Assert
                assert hasattr(result, 'access_token')
                assert hasattr(result, 'refresh_token')
                assert result.token_type == "bearer"
                assert result.access_token == "access-token"
                assert result.refresh_token == "refresh-token"


@pytest.mark.asyncio
async def test_login_invalid_credentials(auth_service, mock_user_repo):
    """Test login fails with invalid credentials."""
    # Arrange
    user_login = UserLogin(email="test@example.com", password="wrongpassword")
    mock_user_repo.get_by_email.return_value = None  # User not found

    # Act & Assert
    with pytest.raises(Exception) as exc_info:  # Should be HTTPException
        await auth_service.login(user_login)

    # Assert that it's an authentication error
    assert "Incorrect email or password" in str(exc_info.value)


@pytest.mark.asyncio
async def test_refresh_token_success(auth_service, mock_user_repo):
    """Test successful token refresh."""
    # Arrange
    refresh_token = "valid-refresh-token"
    user_id = "test-user-id"

    # Mock the JWT decode
    with patch("app.services.auth_service.jwt.decode") as mock_decode:
        mock_decode.return_value = {"sub": user_id}

        # Mock user retrieval
        mock_user = User(id=user_id, email="test@example.com")
        mock_user_repo.get.return_value = mock_user

        # Mock token creation
        with patch.object(AuthService, 'create_access_token', return_value="new-access-token"):
            with patch.object(AuthService, 'create_refresh_token', return_value="new-refresh-token"):

                # Act
                result = await auth_service.refresh_token(refresh_token)

                # Assert
                assert hasattr(result, 'access_token')
                assert hasattr(result, 'refresh_token')
                assert result.token_type == "bearer"
                assert result.access_token == "new-access-token"
                assert result.refresh_token == "new-refresh-token"


@pytest.mark.asyncio
async def test_verify_email_success(auth_service, mock_user_repo):
    """Test successful email verification."""
    # Arrange
    token = "valid-verification-token"
    user_id = "test-user-id"

    # Mock user retrieval by verification token
    mock_user = User(
        id=user_id,
        email="test@example.com",
        email_verification_token=token,
        email_verification_expires=datetime.utcnow() + timedelta(hours=1)
    )
    mock_user_repo.get_by_verification_token.return_value = mock_user

    # Act
    result = await auth_service.verify_email(token)

    # Assert
    assert result == {"message": "Email verified successfully"}
    mock_user_repo.get_by_verification_token.assert_called_once_with(token)
    mock_user_repo.verify_email.assert_called_once_with(user_id)


@pytest.mark.asyncio
async def test_verify_email_invalid_token(auth_service, mock_user_repo):
    """Test email verification fails with invalid token."""
    # Arrange
    token = "invalid-token"
    mock_user_repo.get_by_verification_token.return_value = None

    # Act & Assert
    with pytest.raises(Exception) as exc_info:  # Should be HTTPException
        await auth_service.verify_email(token)

    # Assert that it's an invalid token error
    assert "Invalid or expired token" in str(exc_info.value)


@pytest.mark.asyncio
async def test_verify_email_expired_token(auth_service, mock_user_repo):
    """Test email verification fails with expired token."""
    # Arrange
    token = "expired-token"
    user_id = "test-user-id"

    # Mock user with expired token
    mock_user = User(
        id=user_id,
        email="test@example.com",
        email_verification_token=token,
        email_verification_expires=datetime.utcnow() - timedelta(hours=1)  # Expired
    )
    mock_user_repo.get_by_verification_token.return_value = mock_user

    # Act & Assert
    with pytest.raises(Exception) as exc_info:  # Should be HTTPException
        await auth_service.verify_email(token)

    # Assert that it's an expired token error
    assert "Token has expired" in str(exc_info.value)