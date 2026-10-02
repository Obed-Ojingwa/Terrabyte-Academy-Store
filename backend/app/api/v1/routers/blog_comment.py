from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.blog_comment_service import BlogCommentService
from app.repositories.blog_comment_repository import BlogCommentRepository
from app.schemas.blog_comment import BlogCommentCreate, BlogCommentUpdate, BlogCommentInDB, BlogCommentWithAuthor, BlogCommentWithReplies
from app.api.v1.deps import get_current_active_user
from app.models.user import User


router = APIRouter()


def get_blog_comment_repository(db: AsyncSession = Depends(get_db)) -> BlogCommentRepository:
    return BlogCommentRepository(db)


def get_blog_comment_service(blog_comment_repo: BlogCommentRepository = Depends(get_blog_comment_repository)) -> BlogCommentService:
    return BlogCommentService(blog_comment_repo)


@router.post("/", response_model=BlogCommentInDB, status_code=status.HTTP_201_CREATED)
async def create_blog_comment(
    blog_comment_in: BlogCommentCreate,
    blog_comment_service: BlogCommentService = Depends(get_blog_comment_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new blog comment.
    """
    return await blog_comment_service.create_blog_comment(blog_comment_in)


@router.get("/", response_model=List[BlogCommentInDB])
async def read_blog_comments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    blog_post_id: Optional[str] = None,
    approved_only: bool = True,
    blog_comment_service: BlogCommentService = Depends(get_blog_comment_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve blog comments.
    """
    if blog_post_id:
        if approved_only:
            return await blog_comment_service.get_approved_comments(blog_post_id, skip=skip, limit=limit)
        else:
            return await blog_comment_service.get_by_blog_post(blog_post_id, skip=skip, limit=limit)
    # For getting all blog comments, we'd need a different method
    # For now, we'll return an empty list or implement a general method
    return []


@router.get("/approved/{blog_post_id}", response_model=List[BlogCommentInDB])
async def read_approved_blog_comments(
    blog_post_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    blog_comment_service: BlogCommentService = Depends(get_blog_comment_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve approved blog comments for a specific blog post.
    """
    return await blog_comment_service.get_approved_comments(blog_post_id, skip=skip, limit=limit)


@router.get("/root/{blog_post_id}", response_model=List[BlogCommentInDB])
async def read_root_blog_comments(
    blog_post_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    blog_comment_service: BlogCommentService = Depends(get_blog_comment_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve root blog comments (top-level comments) for a specific blog post.
    """
    return await blog_comment_service.get_root_comments(blog_post_id, skip=skip, limit=limit)


@router.get("/recent", response_model=List[BlogCommentInDB])
async def read_recent_blog_comments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    blog_comment_service: BlogCommentService = Depends(get_blog_comment_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve recent blog comments.
    """
    return await blog_comment_service.get_recent_comments(skip=skip, limit=limit)


@router.get("/{blog_comment_id}", response_model=BlogCommentInDB)
async def read_blog_comment(
    blog_comment_id: str,
    blog_comment_service: BlogCommentService = Depends(get_blog_comment_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific blog comment by ID.
    """
    return await blog_comment_service.get(blog_comment_id)


@router.put("/{blog_comment_id}", response_model=BlogCommentInDB)
async def update_blog_comment(
    blog_comment_id: str,
    blog_comment_in: BlogCommentUpdate,
    blog_comment_service: BlogCommentService = Depends(get_blog_comment_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a blog comment.
    """
    return await blog_comment_service.update_blog_comment(blog_comment_id, blog_comment_in)


@router.delete("/{blog_comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog_comment(
    blog_comment_id: str,
    blog_comment_service: BlogCommentService = Depends(get_blog_comment_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a blog comment.
    """
    await blog_comment_service.delete_blog_comment(blog_comment_id)
    return None