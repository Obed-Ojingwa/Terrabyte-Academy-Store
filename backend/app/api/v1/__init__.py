from fastapi import APIRouter
from app.api.v1.routers import auth, category, cart, order, product, tag, seller, blog, review, service_review, faq, testimonial, blog_comment

api_router = APIRouter()

# Include routers
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(category.router, prefix="/categories", tags=["categories"])
api_router.include_router(cart.router, prefix="/cart", tags=["cart"])
api_router.include_router(order.router, prefix="/order", tags=["order"])
api_router.include_router(product.router, prefix="/products", tags=["products"])
api_router.include_router(tag.router, prefix="/tags", tags=["tags"])
api_router.include_router(seller.router, prefix="/sellers", tags=["sellers"])
api_router.include_router(blog.router, prefix="/blog", tags=["blog"])
api_router.include_router(review.router, prefix="/reviews", tags=["reviews"])
api_router.include_router(service_review.router, prefix="/service-reviews", tags=["service-reviews"])
api_router.include_router(faq.router, prefix="/faqs", tags=["faqs"])
api_router.include_router(testimonial.router, prefix="/testimonials", tags=["testimonials"])
api_router.include_router(blog_comment.router, prefix="/blog-comments", tags=["blog-comments"])
