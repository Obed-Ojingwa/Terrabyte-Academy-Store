from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.repositories.role_repository import RoleRepository
from app.services.role_service import RoleService
from app.core.config import settings
from app.models.user import User
from app.models.role import Role


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get current user from JWT token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user_repo = UserRepository(db)
    user = await user_repo.get(user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Get current active user
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_admin_user(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get current admin user. Raises 403 if user is not an admin.
    """
    if current_user.role_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have a role assigned"
        )

    # Get the user's role to check if it's admin
    role_repo = RoleRepository(db)
    role_service = RoleService(role_repo)
    user_role = await role_service.get_role_by_id(current_user.role_id)

    if user_role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have admin privileges"
        )
    return current_user


async def get_current_seller_user(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get current seller user. Raises 403 if user is not a seller.
    """
    if current_user.role_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have a role assigned"
        )

    # Get the user's role to check if it's seller
    role_repo = RoleRepository(db)
    role_service = RoleService(role_repo)
    user_role = await role_service.get_role_by_id(current_user.role_id)

    if user_role.name != "seller":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have seller privileges"
        )
    return current_user


async def get_current_customer_user(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get current customer user. Raises 403 if user is not a customer.
    """
    if current_user.role_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have a role assigned"
        )

    # Get the user's role to check if it's customer
    role_repo = RoleRepository(db)
    role_service = RoleService(role_repo)
    user_role = await role_service.get_role_by_id(current_user.role_id)

    if user_role.name != "customer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have customer privileges"
        )
    return current_user