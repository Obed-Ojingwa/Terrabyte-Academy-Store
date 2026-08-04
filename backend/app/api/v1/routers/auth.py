from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository
from app.services.role_service import RoleService
from app.repositories.role_repository import RoleRepository
from app.schemas.user import UserCreate, UserLogin, Token, UserInDB
from app.api.v1.deps import get_current_active_user
from app.models.user import User

router = APIRouter()


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_role_repository(db: AsyncSession = Depends(get_db)) -> RoleRepository:
    return RoleRepository(db)


def get_role_service(role_repo: RoleRepository = Depends(get_role_repository)) -> RoleService:
    return RoleService(role_repo)


def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
    role_service: RoleService = Depends(get_role_service)
) -> AuthService:
    return AuthService(user_repo, role_service)


@router.post("/register", response_model=Token)
async def register(
    user_in: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Register a new user
    """
    user = await auth_service.register_user(user_in)
    access_token = auth_service.create_access_token(user)
    refresh_token = auth_service.create_refresh_token(user)
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Login user and return JWT tokens
    """
    user_login = UserLogin(email=form_data.username, password=form_data.password)
    token = await auth_service.login(user_login)
    return token


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Refresh access token using refresh token
    """
    token = await auth_service.refresh_token(refresh_token)
    return token


@router.get("/verify-email")
async def verify_email(
    token: str,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Verify user's email using the token sent to their email
    """
    result = await auth_service.verify_email(token)
    return result


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_active_user)
):
    """
    Logout user (client-side token removal)
    """
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserInDB)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user information
    """
    return current_user