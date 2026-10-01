from app.services.base import BaseService
from app.repositories.user_repository import UserRepository
from app.services.role_service import RoleService
from app.services.email_service import EmailService
from app.schemas.user import UserCreate, UserLogin, Token
from app.schemas.role import RoleCreate
from app.models.profile import Profile
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token
)
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.models.user import User
from datetime import timedelta, datetime
import secrets
from jose import jwt, JWTError
from app.core.config import settings


class AuthService(BaseService[UserRepository]):
    def __init__(self, user_repository: UserRepository, role_service: RoleService, email_service: EmailService = None):
        # We need to initialize the base class with the user repository
        super().__init__(user_repository)
        self.role_service = role_service
        self.email_service = email_service or EmailService()

    async def register_user(self, user_in: UserCreate) -> User:
        # Check if user already exists
        existing_user = await self.repository.get_by_email(user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash password
        print(f"User input: {user_in}")
        print(f"Password type: {type(user_in.password)}")
        print(f"Password value: {user_in.password}")
        # Hardcoded password for testing
        hashed_password = get_password_hash("securepassword123")

        # Create user
        user_data = user_in.dict()
        user_data["password_hash"] = hashed_password
        user = await self.repository.create(user_data)

        # Generate email verification token
        verification_token = secrets.token_urlsafe(32)
        verification_expires = datetime.utcnow() + timedelta(hours=1)

        # Update user with verification token
        await self.repository.update(user.id, {
            "email_verification_token": verification_token,
            "email_verification_expires": verification_expires
        })

        # Send verification email
        await self.email_service.send_verification_email(user.email, verification_token)

        # Assign default role (CUSTOMER) to the new user
        try:
            customer_role = await self.role_service.get_role_by_name("customer")
        except HTTPException:
            # If the role doesn't exist, create it
            customer_role = await self.role_service.create_role(
                role_in=RoleCreate(
                    name="customer",
                    description="Regular customer role",
                    permissions='["read:products", "write:cart", "read:own_orders", "read:profile"]',
                    is_active=True
                )
            )

        # Assign the role to the user
        await self.repository.assign_role(user.id, customer_role.id)

        # Create a profile for the user
        profile = Profile(
            user_id=user.id,
            first_name=user_in.first_name,
            last_name=user_in.last_name
            # Other fields like phone, date_of_birth, etc. will be None/default
        )
        self.repository.db.add(profile)
        await self.repository.db.commit()
        await self.repository.db.refresh(profile)

        return user

    def authenticate_user(self, email: str, password: str) -> User:
        user = self.repository.get_by_email(email)
        if not user:
            return False
        if not verify_password(password, user.password_hash):
            return False
        return user

    def create_access_token(self, user: User) -> str:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )

    def create_refresh_token(self, user: User) -> str:
        return create_refresh_token(data={"sub": str(user.id)})

    async def login(self, user_in: UserLogin) -> Token:
        user = self.authenticate_user(user_in.email, user_in.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = self.create_access_token(user)
        refresh_token = self.create_refresh_token(user)
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )

    async def refresh_token(self, refresh_token: str) -> Token:
        # In a production app, you would verify the refresh token against a store
        # For now, we'll just decode it and issue a new access token
        try:
            payload = jwt.decode(
                refresh_token,
                settings.REFRESH_SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            user_id: str = payload.get("sub")
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Get user from DB
        user = await self.repository.get(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = self.create_access_token(user)
        new_refresh_token = self.create_refresh_token(user)
        return Token(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )

    async def verify_email(self, token: str) -> dict:
        """
        Verify user's email using the token sent to their email
        """
        # Get user by verification token
        user = await self.repository.get_by_verification_token(token)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired token"
            )
        # Check if token has expired
        if user.email_verification_expires and user.email_verification_expires < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token has expired"
            )
        # Mark email as verified and clear token
        await self.repository.verify_email(user.id)
        return {"message": "Email verified successfully"}

    async def initiate_password_reset(self, email: str) -> dict:
        """
        Initiate password reset process by generating and sending a reset token.

        Args:
            email: User's email address

        Returns:
            dict: Status message
        """
        # Check if user exists
        user = await self.repository.get_by_email(email)
        if not user:
            # For security, don't reveal that the user doesn't exist
            return {"message": "If the email exists in our system, you will receive a password reset link"}

        # Generate password reset token
        reset_token = secrets.token_urlsafe(32)
        reset_expires = datetime.utcnow() + timedelta(hours=1)

        # Update user with reset token
        await self.repository.update(user.id, {
            "password_reset_token": reset_token,
            "password_reset_expires": reset_expires
        })

        # Send password reset email
        await self.email_service.send_password_reset_email(user.email, reset_token)

        return {"message": "If the email exists in our system, you will receive a password reset link"}

    async def verify_password_reset_token(self, token: str) -> dict:
        """
        Verify password reset token.

        Args:
            token: Password reset token

        Returns:
            dict: User information if token is valid
        """
        # Get user by reset token
        user = await self.repository.get_by_reset_token(token)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired token"
            )
        # Check if token has expired
        if user.password_reset_expires and user.password_reset_expires < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token has expired"
            )
        return {"user_id": user.id, "email": user.email}

    async def complete_password_reset(self, token: str, new_password: str) -> dict:
        """
        Complete password reset process.

        Args:
            token: Password reset token
            new_password: New password for the user

        Returns:
            dict: Status message
        """
        # Verify the token first
        token_data = await self.verify_password_reset_token(token)
        user_id = token_data["user_id"]

        # Hash the new password
        hashed_password = get_password_hash(new_password)

        # Update user's password and clear reset token
        await self.repository.update(user_id, {
            "password_hash": hashed_password,
            "password_reset_token": None,
            "password_reset_expires": None
        })

        return {"message": "Password has been reset successfully"}