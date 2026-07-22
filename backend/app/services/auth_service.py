from app.services.base import BaseService
from app.repositories.user_repository import UserRepository
from app.services.role_service import RoleService
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
    def __init__(self, user_repository: UserRepository, role_service: RoleService):
        # We need to initialize the base class with the user repository
        super().__init__(user_repository)
        self.role_service = role_service

    async def register_user(self, user_in: UserCreate) -> User:
        # Check if user already exists
        existing_user = await self.repository.get_by_email(user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash password
        hashed_password = get_password_hash(user_in.password)

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

        # Log the verification token (in a real app, send an email)
        print(f"Email verification token for {user.email}: {verification_token}")

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