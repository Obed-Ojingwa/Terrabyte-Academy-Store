from fastapi import APIRouter
from app.api.v1.routers import auth, category, product, tag

api_router = APIRouter()

# Include routers
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(category.router, prefix="/categories", tags=["categories"])
api_router.include_router(product.router, prefix="/products", tags=["products"])
api_router.include_router(tag.router, prefix="/tags", tags=["tags"])