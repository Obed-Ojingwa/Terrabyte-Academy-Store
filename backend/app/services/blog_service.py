from app.services.base import BaseService
from app.repositories.blog_repository import BlogRepository
from app.schemas.blog_post import BlogPostCreate, BlogPostUpdate, BlogPostInDB, BlogPostWithAuthor, BlogPostWithTags
from app.models.blog_post import BlogPost
from typing import List, Optional
from fastapi import HTTPException, status


class BlogService(BaseService[BlogRepository]):
    def __init__(self, blog_repository: BlogRepository):
        super().__init__(blog_repository)
        self.repository = blog_repository

    async def get(self, blog_post_id: str) -> BlogPostInDB:
        blog_post = await self.repository.get(blog_post_id)
        if not blog_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Blog post not found"
            )
        return BlogPostInDB.from_orm(blog_post)

    async def get_by_slug(self, slug: str) -> BlogPostInDB:
        blog_post = await self.repository.get_by_slug(slug)
        if not blog_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Blog post not found"
            )
        return BlogPostInDB.from_orm(blog_post)

    async def get_by_author(self, author_id: str, skip: int = 0, limit: int = 100) -> List[BlogPostInDB]:
        blog_posts = await self.repository.get_by_author(author_id, skip=skip, limit=limit)
        return [BlogPostInDB.from_orm(blog_post) for blog_post in blog_posts]

    async def get_published_posts(self, skip: int = 0, limit: int = 100) -> List[BlogPostInDB]:
        blog_posts = await self.repository.get_published_posts(skip=skip, limit=limit)
        return [BlogPostInDB.from_orm(blog_post) for blog_post in blog_posts]

    async def get_featured_posts(self, skip: int = 0, limit: int = 100) -> List[BlogPostInDB]:
        blog_posts = await self.repository.get_featured_posts(skip=skip, limit=limit)
        return [BlogPostInDB.from_orm(blog_post) for blog_post in blog_posts]

    async def create_blog_post(self, blog_post_in: BlogPostCreate) -> BlogPostInDB:
        blog_post = await self.repository.create(blog_post_in.dict())
        return BlogPostInDB.from_orm(blog_post)

    async def update_blog_post(self, blog_post_id: str, blog_post_in: BlogPostUpdate) -> BlogPostInDB:
        blog_post = await self.repository.get(blog_post_id)
        if not blog_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Blog post not found"
            )

        update_data = blog_post_in.dict(exclude_unset=True)
        updated_blog_post = await self.repository.update(blog_post_id, update_data)
        return BlogPostInDB.from_orm(updated_blog_post)

    async def delete_blog_post(self, blog_post_id: str) -> bool:
        blog_post = await self.repository.get(blog_post_id)
        if not blog_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Blog post not found"
            )
        return await self.repository.delete(blog_post_id)