from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.blog_service import BlogService
from app.repositories.blog_repository import BlogRepository
from app.schemas.blog_post import BlogPostCreate, BlogPostUpdate, BlogPostInDB, BlogPostWithAuthor, BlogPostWithTags
from app.api.v1.deps import get_current_active_user
from app.models.user import User


router = APIRouter()


def get_blog_repository(db: AsyncSession = Depends(get_db)) -> BlogRepository:
    return BlogRepository(db)


def get_blog_service(blog_repo: BlogRepository = Depends(get_blog_repository)) -> BlogService:
    return BlogService(blog_repo)


@router.post("/", response_model=BlogPostInDB, status_code=status.HTTP_201_CREATED)
async def create_blog_post(
    blog_post_in: BlogPostCreate,
    blog_service: BlogService = Depends(get_blog_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new blog post.
    """
    return await blog_service.create_blog_post(blog_post_in)


@router.get("/", response_model=List[BlogPostInDB])
async def read_blog_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    published_only: bool = True,
    blog_service: BlogService = Depends(get_blog_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve blog posts.
    """
    if published_only:
        return await blog_service.get_published_posts(skip=skip, limit=limit)
    # For getting all blog posts (including drafts), we'd need a different method
    # For now, we'll just get published ones
    return await blog_service.get_published_posts(skip=skip, limit=limit)


@router.get("/featured", response_model=List[BlogPostInDB])
async def read_featured_blog_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    blog_service: BlogService = Depends(get_blog_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve featured blog posts.
    """
    return await blog_service.get_featured_posts(skip=skip, limit=limit)


@router.get("/{blog_post_id}", response_model=BlogPostInDB)
async def read_blog_post(
    blog_post_id: str,
    blog_service: BlogService = Depends(get_blog_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific blog post by ID.
    """
    return await blog_service.get(blog_post_id)


@router.get("/slug/{slug}", response_model=BlogPostInDB)
async def read_blog_post_by_slug(
    slug: str,
    blog_service: BlogService = Depends(get_blog_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific blog post by slug.
    """
    return await blog_service.get_by_slug(slug)


@router.put("/{blog_post_id}", response_model=BlogPostInDB)
async def update_blog_post(
    blog_post_id: str,
    blog_post_in: BlogPostUpdate,
    blog_service: BlogService = Depends(get_blog_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a blog post.
    """
    return await blog_service.update_blog_post(blog_post_id, blog_post_in)


@router.delete("/{blog_post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog_post(
    blog_post_id: str,
    blog_service: BlogService = Depends(get_blog_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a blog post.
    """
    await blog_service.delete_blog_post(blog_post_id)
    return None


@router.get("/author/{author_id}", response_model=List[BlogPostInDB])
async def read_blog_posts_by_author(
    author_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    blog_service: BlogService = Depends(get_blog_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve blog posts by author.
    """
    return await blog_service.get_by_author(author_id, skip=skip, limit=limit)