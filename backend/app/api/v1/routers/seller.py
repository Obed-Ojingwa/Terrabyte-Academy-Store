from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.seller_service import SellerService
from app.repositories.seller_repository import SellerRepository
from typing import List, Optional
from fastapi import Query
from app.services.product_service import ProductService
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate, ProductInDB
from app.repositories.user_repository import UserRepository
from app.services.role_service import RoleService
from app.services.email_service import EmailService
from app.schemas.seller import SellerCreate, SellerUpdate, SellerInDB, SellerRegistration, SellerApproval
from app.schemas.user import UserInDB
from app.api.v1.deps import get_current_active_user, get_current_admin_user, get_current_seller_user
from app.models.user import User


def get_seller_repository(db: AsyncSession = Depends(get_db)) -> SellerRepository:
    return SellerRepository(db)


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_role_repository(db: AsyncSession = Depends(get_db)):  # Import here to avoid circular imports
    from app.repositories.role_repository import RoleRepository
    return RoleRepository(db)


def get_product_repository(db: AsyncSession = Depends(get_db)) -> ProductRepository:
    return ProductRepository(db)


def get_product_service(product_repo: ProductRepository = Depends(get_product_repository)) -> ProductService:
    return ProductService(product_repo)

def get_role_service(role_repo: RoleRepository = Depends(get_role_repository)) -> RoleService:
    from app.services.role_service import RoleService
    return RoleService(role_repo)


def get_email_service() -> EmailService:
    from app.services.email_service import EmailService
    return EmailService()


def get_seller_service(
    seller_repo: SellerRepository = Depends(get_seller_repository),
    user_repo: UserRepository = Depends(get_user_repository),
    role_service: RoleService = Depends(get_role_service),
    email_service: EmailService = Depends(get_email_service)
) -> SellerService:
    return SellerService(seller_repo, user_repo, role_service, email_service)


router = APIRouter()


@router.post("/register", response_model=dict)
async def register_seller(
    seller_in: SellerRegistration,
    seller_service: SellerService = Depends(get_seller_service)
):
    """
    Register a new seller
    """
    result = await seller_service.register_seller(seller_in)
    return {
        "message": "Seller registered successfully. Please check your email for verification.",
        "user_id": result["user"].id,
        "seller_id": result["seller"].id
    }


@router.get("/pending-approvals", response_model=list[SellerInDB])
async def get_pending_seller_approvals(
    current_admin: User = Depends(get_current_admin_user),
    seller_service: SellerService = Depends(get_seller_service)
):
    """
    Get all sellers pending approval (admin only)
    """
    sellers = await seller_service.get_pending_approvals()
    return sellers


@router.post("/approve", response_model=SellerInDB)
async def approve_seller(
    approval_in: SellerApproval,
    current_admin: User = Depends(get_current_admin_user),
    seller_service: SellerService = Depends(get_seller_service)
):
    """
    Approve or reject a seller (admin only)
    """
    if approval_in.approve:
        seller = await seller_service.approve_seller(approval_in.seller_id, approval_in.approved_by)
        if not seller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller not found"
            )
        return seller
    else:
        # For rejection, we could delete the seller or just leave them unapproved
        # For now, we'll just leave them unapproved
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rejection not implemented yet"
        )


@router.get("/me", response_model=SellerInDB)
async def get_current_seller_info(
    current_seller: User = Depends(get_current_seller_user),
    seller_service: SellerService = Depends(get_seller_service)
):
    """
    Get current seller's information
    """
    seller = await seller_service.get_seller_by_user_id(current_seller.id)
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seller profile not found"
        )
    return seller


@router.put("/me", response_model=SellerInDB)
async def update_current_seller(
    seller_in: SellerUpdate,
    current_seller: User = Depends(get_current_seller_user),
    seller_service: SellerService = Depends(get_seller_service)
):
    """
    Update current seller's information
    """
    seller = await seller_service.get_seller_by_user_id(current_seller.id)
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seller profile not found"
        )
    
    updated_seller = await seller_service.update_seller(seller.id, seller_in)
    if not updated_seller:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update seller"
        )
    return updated_seller


@router.get("/dashboard")
async def get_seller_dashboard(
    current_seller: User = Depends(get_current_seller_user),
    seller_service: SellerService = Depends(get_seller_service)
):
    """
    Get seller dashboard information
    """
    seller = await seller_service.get_seller_by_user_id(current_seller.id)
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seller profile not found"
        )
    
    # TODO: Get actual product count, order count, etc. from database
    # For now, return basic info
    return {
        "seller": seller,
        "stats": {
            "total_products": 0,  # Placeholder
            "active_products": 0,  # Placeholder
            "total_orders": 0,     # Placeholder
            "pending_orders": 0,   # Placeholder
            "total_sales": float(seller.total_sales),
            "total_earnings": float(seller.total_earnings)
        }
    }


@router.get("/analytics")
async def get_seller_analytics(
    current_seller: User = Depends(get_current_seller_user),
    seller_service: SellerService = Depends(get_seller_service)
):
    """
    Get seller sales analytics and earnings reporting
    """
    seller = await seller_service.get_seller_by_user_id(current_seller.id)
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seller profile not found"
        )
    
    # TODO: Implement actual analytics from orders and order items
    # For now, return placeholder data
    return {
        "seller_id": seller.id,
        "store_name": seller.store_name,
        "analytics": {
            "total_sales": float(seller.total_sales),
            "total_earnings": float(seller.total_earnings),
            "average_order_value": 0.0,  # Placeholder
            "sales_by_month": [],        # Placeholder
            "top_selling_products": [],  # Placeholder
            "earnings_by_month": [],     # Placeholder
            "commission_rate": float(seller.commission_rate)
        }
    }

# Product management endpoints for sellers
@router.post("/products", response_model=ProductInDB, status_code=status.HTTP_201_CREATED)
async def create_seller_product(
    product_in: ProductCreate,
    product_service: ProductService = Depends(get_product_service),
    current_seller: User = Depends(get_current_seller_user),
    seller_service: SellerService = Depends(get_seller_service)
):
    """
    Create a new product for the current seller
    """
    # Get the seller's seller ID
    seller = await seller_service.get_seller_by_user_id(current_seller.id)
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seller profile not found"
        )
    
    # Set the seller_id on the product
    product_data = product_in.dict()
    product_data["seller_id"] = seller.id
    
    # Create the product
    product_in_with_seller = ProductCreate(**product_data)
    return await product_service.create_product(product_in_with_seller)


@router.get("/products", response_model=List[ProductInDB])
async def get_seller_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    active_only: bool = True,
    current_seller: User = Depends(get_current_seller_user),
    seller_service: SellerService = Depends(get_seller_service),
    product_service: ProductService = Depends(get_product_service)
):
    """
    Get products belonging to the current seller
    """
    # Get the seller's seller ID
    seller = await seller_service.get_seller_by_user_id(current_seller.id)
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seller profile not found"
        )
    
    # TODO: Implement get_products_by_seller method in ProductService
    # For now, we'll get all products and filter (not efficient but works for now)
    # In a real implementation, we'd add a method to ProductRepository to get by seller_id
    all_products = await product_service.get_active_products(skip=0, limit=1000)  # Get a large number
    seller_products = [p for p in all_products if p.seller_id == seller.id]
    
    # Apply pagination
    paginated_products = seller_products[skip:skip+limit]
    return paginated_products


@router.get("/products/{product_id}", response_model=ProductInDB)
async def get_seller_product(
    product_id: str,
    current_seller: User = Depends(get_current_seller_user),
    seller_service: SellerService = Depends(get_seller_service),
    product_service: ProductService = Depends(get_product_service)
):
    """
    Get a specific product belonging to the current seller
    """
    # Get the seller's seller ID
    seller = await seller_service.get_seller_by_user_id(current_seller.id)
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seller profile not found"
        )
    
    # Get the product
    product = await product_service.repository.get(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Verify the product belongs to the current seller
    if product.seller_id != seller.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Product does not belong to the current seller"
        )
    
    return product


@router.put("/products/{product_id}", response_model=ProductInDB)
async def update_seller_product(
    product_id: str,
    product_in: ProductUpdate,
    current_seller: User = Depends(get_current_seller_user),
    seller_service: SellerService = Depends(get_seller_service),
    product_service: ProductService = Depends(get_product_service)
):
    """
    Update a product belonging to the current seller
    """
    # Get the seller's seller ID
    seller = await seller_service.get_seller_by_user_id(current_seller.id)
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seller profile not found"
        )
    
    # Get the product
    product = await product_service.repository.get(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Verify the product belongs to the current seller
    if product.seller_id != seller.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Product does not belong to the current seller"
        )
    
    # Update the product
    updated_product = await product_service.update_product(product_id, product_in)
    if not updated_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return updated_product


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_seller_product(
    product_id: str,
    current_seller: User = Depends(get_current_seller_user),
    seller_service: SellerService = Depends(get_seller_service),
    product_service: ProductService = Depends(get_product_service)
):
    """
    Delete a product belonging to the current seller
    """
    # Get the seller's seller ID
    seller = await seller_service.get_seller_by_user_id(current_seller.id)
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seller profile not found"
        )
    
    # Get the product
    product = await product_service.repository.get(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Verify the product belongs to the current seller
    if product.seller_id != seller.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Product does not belong to the current seller"
        )
    
    # Delete the product
    success = await product_service.delete_product(product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return None
