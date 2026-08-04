from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.product_service import ProductService
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate, ProductInDB
from app.api.v1.deps import get_current_active_user
from app.models.user import User

router = APIRouter()


def get_product_repository(db: AsyncSession = Depends(get_db)) -> ProductRepository:
    return ProductRepository(db)


def get_product_service(product_repo: ProductRepository = Depends(get_product_repository)) -> ProductService:
    return ProductService(product_repo)


@router.post("/", response_model=ProductInDB, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_in: ProductCreate,
    product_service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new product.
    """
    return await product_service.create_product(product_in)


@router.get("/", response_model=List[ProductInDB])
async def read_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    active_only: bool = True,
    product_service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve products.
    """
    if active_only:
        return await product_service.get_active_products(skip=skip, limit=limit)
    # For getting all products (including inactive), we'd need a different method
    # For now, we'll just get active ones
    return await product_service.get_active_products(skip=skip, limit=limit)


@router.get("/{product_id}", response_model=ProductInDB)
async def read_product(
    product_id: str,
    product_service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve a product by ID.
    """
    # We don't have a get_by_id method in ProductService yet, but we can use get_by_sku for now
    # Actually, let's get by ID using the repository directly through the service
    product = await product_service.repository.get(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return ProductInDB.from_orm(product)


@router.get("/sku/{sku}", response_model=ProductInDB)
async def read_product_by_sku(
    sku: str,
    product_service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve a product by SKU.
    """
    product = await product_service.get_product_by_sku(sku)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


@router.get("/category/{category_id}", response_model=List[ProductInDB])
async def read_products_by_category(
    category_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    product_service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve products by category.
    """
    products = await product_service.get_products_by_category(category_id, skip=skip, limit=limit)
    return products


@router.get("/featured/", response_model=List[ProductInDB])
async def read_featured_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    product_service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve featured products.
    """
    return await product_service.get_featured_products(skip=skip, limit=limit)


@router.put("/{product_id}", response_model=ProductInDB)
async def update_product(
    product_id: str,
    product_in: ProductUpdate,
    product_service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a product.
    """
    product = await product_service.update_product(product_id, product_in)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: str,
    product_service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a product.
    """
    success = await product_service.delete_product(product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return None


@router.post("/{product_id}/image", response_model=dict)
async def upload_product_image(
    product_id: str,
    file: UploadFile = File(...),
    product_service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Upload an image for a product.
    Note: This is a placeholder for image upload functionality.
    Actual implementation would integrate with Supabase Storage in later milestones.
    """
    # Verify product exists
    product = await product_service.repository.get(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    # In a real implementation, we would:
    # 1. Validate the file type and size
    # 2. Upload the file to Supabase Storage
    # 3. Create a ProductImage record linked to the product
    # 4. Return the image URL

    # For now, we'll just return a placeholder response
    return {
        "message": "Image upload endpoint placeholder",
        "product_id": product_id,
        "filename": file.filename,
        "content_type": file.content_type
    }