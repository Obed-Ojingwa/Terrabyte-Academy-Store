from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.coupon_service import CouponService
from app.repositories.coupon_repository import CouponRepository
from app.schemas.coupon import CouponCreate, CouponUpdate, CouponInDB
from app.models.user import User
from app.api.v1.deps import get_current_active_user, get_current_admin_user

router = APIRouter()


def get_coupon_repository(db: AsyncSession = Depends(get_db)) -> CouponRepository:
    return CouponRepository(db)


def get_coupon_service(
    coupon_repo: CouponRepository = Depends(get_coupon_repository)
) -> CouponService:
    return CouponService(coupon_repo)


# Coupon endpoints (admin only)
@router.post("/", response_model=CouponInDB, status_code=status.HTTP_201_CREATED)
async def create_coupon(
    coupon_in: CouponCreate,
    coupon_service: CouponService = Depends(get_coupon_service),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Create a new coupon. Only accessible by admin users.
    """
    return await coupon_service.create(coupon_in)


@router.get("/", response_model=List[CouponInDB])
async def read_coupons(
    skip: int = Query(0, description="Number of coupons to skip"),
    limit: int = Query(100, description="Maximum number of coupons to return"),
    coupon_service: CouponService = Depends(get_coupon_service),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Retrieve coupons. Only accessible by admin users.
    """
    return await coupon_service.get_active_coupons(skip, limit)


@router.get("/{coupon_id}", response_model=CouponInDB)
async def read_coupon(
    coupon_id: str,
    coupon_service: CouponService = Depends(get_coupon_service),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Get a specific coupon by ID. Only accessible by admin users.
    """
    return await coupon_service.get(coupon_id)


@router.put("/{coupon_id}", response_model=CouponInDB)
async def update_coupon(
    coupon_id: str,
    coupon_in: CouponUpdate,
    coupon_service: CouponService = Depends(get_coupon_service),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Update a coupon. Only accessible by admin users.
    """
    return await coupon_service.update(coupon_id, coupon_in)


@router.delete("/{coupon_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_coupon(
    coupon_id: str,
    coupon_service: CouponService = Depends(get_coupon_service),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Delete a coupon. Only accessible by admin users.
    """
    await coupon_service.delete(coupon_id)
    return None


# Public endpoint to validate a coupon (no authentication required for validation)
@router.post("/validate", response_model=dict)
async def validate_coupon(
    code: str = Query(..., description="Coupon code to validate"),
    user_id: Optional[str] = Query(None, description="User ID for per-user usage limits"),
    purchase_amount: float = Query(0.0, description="Purchase amount to validate against"),
    coupon_service: CouponService = Depends(get_coupon_service)
):
    """
    Validate a coupon and calculate the discount amount.
    This endpoint is public and does not require authentication.
    """
    is_valid, error_message, discount_amount = await coupon_service.validate_coupon(
        code, user_id, purchase_amount
    )
    return {
        "valid": is_valid,
        "error": error_message,
        "discount_amount": discount_amount
    }