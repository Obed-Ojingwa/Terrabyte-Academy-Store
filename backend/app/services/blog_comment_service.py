from app.services.base import BaseService
from app.repositories.blog_comment_repository import BlogCommentRepository
from app.schemas.blog_comment import BlogCommentCreate, BlogCommentUpdate, BlogCommentInDB, BlogCommentWithAuthor, BlogCommentWithReplies
from app.models.blog_comment import BlogComment
from typing import List, Optional
from fastapi import HTTPException, status


class BlogCommentService(BaseService[BlogCommentRepository]):
    def __init__(self, blog_comment_repository: BlogCommentRepository):
        super().__init__(blog_comment_repository)
        self.repository = blog_comment_repository

    async def get(self, blog_comment_id: str) -> BlogCommentInDB:
        blog_comment = await self.repository.get(blog_comment_id)
        if not blog_comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Blog comment not found"
            )
        return BlogCommentInDB.from_orm(blog_comment)

    async def get_by_blog_post(self, blog_post_id: str, skip: int = 0, limit: int = 100) -> List[BlogCommentInDB]:
        blog_comments = await self.repository.get_by_blog_post(blog_post_id, skip=skip, limit=limit)
        return [BlogCommentInDB.from_orm(blog_comment) for blog_comment in blog_comments]

    async def get_by_author(self, author_id: str, skip: int = 0, limit: int = 100) -> List[BlogCommentInDB]:
        blog_comments = await self.repository.get_by_author(author_id, skip=skip, limit=limit)
        return [BlogCommentInDB.from_orm(blog_comment) for blog_comment in blog_comments]

    async def get_approved_comments(self, blog_post_id: str, skip: int = 0, limit: int = 100) -> List[BlogCommentInDB]:
        blog_comments = await self.repository.get_approved_comments(blog_post_id, skip=skip, limit=limit)
        return [BlogCommentInDB.from_orm(blog_comment) for blog_comment in blog_comments]

    async def get_root_comments(self, blog_post_id: str, skip: int = 0, limit: int = 100) -> List[BlogCommentInDB]:
        blog_comments = await self.repository.get_root_comments(blog_post_id, skip=skip, limit=limit)
        return [BlogCommentInDB.from_orm(blog_comment) for blog_comment in blog_comments]

    async def get_recent_comments(self, skip: int = 0, limit: int = 100) -> List[BlogCommentInDB]:
        blog_comments = await self.repository.get_recent_comments(skip=skip, limit=limit)
        return [BlogCommentInDB.from_orm(blog_comment) for blog_comment in blog_comments]

    async def create_blog_comment(self, blog_comment_in: BlogCommentCreate) -> BlogCommentInDB:
        blog_comment = await self.repository.create(blog_comment_in.dict())
        return BlogCommentInDB.from_orm(blog_comment)

    async def update_blog_comment(self, blog_comment_id: str, blog_comment_in: BlogCommentUpdate) -> BlogCommentInDB:
        blog_comment = await self.repository.get(blog_comment_id)
        if not blog_comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Blog comment not found"
            )

        update_data = blog_comment_in.dict(exclude_unset=True)
        updated_blog_comment = await self.repository.update(blog_comment_id, update_data)
        return BlogCommentInDB.from_orm(updated_blog_comment)

    async def delete_blog_comment(self, blog_comment_id: str) -> bool:
        blog_comment = await self.repository.get(blog_comment_id)
        if not blog_comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Blog comment not found"
            )
        return await self.repository.delete(blog_comment_id)