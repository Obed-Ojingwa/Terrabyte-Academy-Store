from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.blog_comment import BlogComment


class BlogCommentRepository(BaseRepository[BlogComment]):
    def __init__(self, db: AsyncSession):
        super().__init__(BlogComment, db)

    async def get_by_blog_post(self, blog_post_id: str, skip: int = 0, limit: int = 100) -> List[BlogComment]:
        result = await self.db.execute(
            select(BlogComment)
            .where(BlogComment.blog_post_id == blog_post_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_author(self, author_id: str, skip: int = 0, limit: int = 100) -> List[BlogComment]:
        result = await self.db.execute(
            select(BlogComment)
            .where(BlogComment.author_id == author_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_approved_comments(self, blog_post_id: str, skip: int = 0, limit: int = 100) -> List[BlogComment]:
        result = await self.db.execute(
            select(BlogComment)
            .where(BlogComment.blog_post_id == blog_post_id)
            .where(BlogComment.is_approved == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_root_comments(self, blog_post_id: str, skip: int = 0, limit: int = 100) -> List[BlogComment]:
        result = await self.db.execute(
            select(BlogComment)
            .where(BlogComment.blog_post_id == blog_post_id)
            .where(BlogComment.parent_id.is_(None))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_recent_comments(self, skip: int = 0, limit: int = 100) -> List[BlogComment]:
        result = await self.db.execute(
            select(BlogComment)
            .order_by(BlogComment.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()