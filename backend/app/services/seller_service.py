from app.services.base import BaseService
from app.repositories.seller_repository import SellerRepository
from app.repositories.user_repository import UserRepository
from app.services.role_service import RoleService
from app.services.email_service import EmailService
from app.schemas.seller import SellerCreate, SellerUpdate, SellerInDB, SellerRegistration, SellerApproval
from app.models.seller import Seller
from app.models.user import User
from app.core.security import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
import secrets
from datetime import datetime, timedelta


class SellerService(BaseService[SellerRepository]):
    def __init__(self, seller_repository: SellerRepository, user_repository: UserRepository, 
                 role_service: RoleService, email_service: EmailService = None):
        super().__init__(seller_repository)
        self.user_repository = user_repository
        self.role_service = role_service
        self.email_service = email_service or EmailService()

    async def register_seller(self, seller_in: SellerRegistration) -> dict:
        # Check if user already exists
        existing_user = await self.user_repository.get_by_email(seller_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash password
        hashed_password = get_password_hash(seller_in.password)

        # Create user
        user_data = {
            "email": seller_in.email,
            "password_hash": hashed_password,
            "is_active": True,
            # role_id will be set after we create the seller role
        }
        user = await self.user_repository.create(user_data)

        # Generate email verification token
        verification_token = secrets.token_urlsafe(32)
        verification_expires = datetime.utcnow() + timedelta(hours=1)

        # Update user with verification token
        await self.user_repository.update(user.id, {
            "email_verification_token": verification_token,
            "email_verification_expires": verification_expires
        })

        # Send verification email
        await self.email_service.send_verification_email(user.email, verification_token)

        # Get or create seller role
        try:
            seller_role = await self.role_service.get_role_by_name("seller")
        except HTTPException:
            # If the role doesn't exist, create it
            seller_role = await self.role_service.create_role(
                name="seller",
                description="Seller role for users who sell products",
                permissions='["read:own_products", "write:own_products", "read:own_orders", "read:shop_analytics"]',
                is_active=True
            )

        # Assign the seller role to the user
        await self.user_repository.assign_role(user.id, seller_role.id)

        # Create seller profile
        seller_data = SellerCreate(
            user_id=user.id,
            store_name=seller_in.store_name,
            store_description=seller_in.store_description,
            logo_url=seller_in.logo_url,
            banner_url=seller_in.banner_url,
            payout_email=seller_in.payout_email,
            payout_method=seller_in.payout_method,
            payout_details=seller_in.payout_details
        )

        seller = await self.repository.create(seller_data.dict())

        # Create a profile for the user
        from app.models.profile import Profile
        profile = Profile(
            user_id=user.id,
            first_name=seller_in.first_name,
            last_name=seller_in.last_name
        )
        self.user_repository.db.add(profile)
        await self.user_repository.db.commit()
        await self.user_repository.db.refresh(profile)

        return {
            "user": user,
            "seller": seller,
            "verification_token": verification_token
        }

    async def get_seller_by_user_id(self, user_id: str) -> Optional[Seller]:
        return await self.repository.get_by_user_id(user_id)

    async def get_seller_by_id(self, seller_id: str) -> Optional[Seller]:
        return await self.repository.get_by_id(seller_id)

    async def update_seller(self, seller_id: str, seller_in: SellerUpdate) -> Optional[Seller]:
        seller_data = seller_in.dict(exclude_unset=True)
        if seller_data:
            updated_seller = await self.repository.update(seller_id, seller_data)
            return updated_seller
        return None

    async def get_pending_approvals(self) -> list:
        return await self.repository.get_pending_approvals()

    async def get_approved_sellers(self) -> list:
        return await self.repository.get_approved_sellers()

    async def approve_seller(self, seller_id: str, approved_by: str) -> Optional[Seller]:
        await self.repository.approve_seller(seller_id, approved_by)
        return await self.repository.get_by_id(seller_id)

    async def update_sales_and_earnings(self, seller_id: str, sales_amount: float, earnings_amount: float) -> None:
        await self.repository.update_sales_and_earnings(seller_id, sales_amount, earnings_amount)
