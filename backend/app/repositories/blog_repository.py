from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.blog_post import BlogPost


class BlogRepository(BaseRepository[BlogPost]):
    def __init__(self, db: AsyncSession):
        super().__init__(BlogPost, db)

    async def get_by_slug(self, slug: str) -> Optional[BlogPost]:
        result = await self.db.execute(select(BlogPost).where(BlogPost.slug == slug))
        return result.scalar_one_or_none()

    async def get_by_author(self, author_id: str, skip: int = 0, limit: int = 100) -> List[BlogPost]:
        result = await self.db.execute(
            select(BlogPost)
            .where(BlogPost.author_id == author_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_published_posts(self, skip: int = 0, limit: int = 100) -> List[BlogPost]:
        result = await self.db.execute(
            select(BlogPost)
            .where(BlogPost.status == "published")
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_featured_posts(self, skip: int = 0, limit: int = 100) -> List[BlogPost]:
        result = await self.db.execute(
            select(BlogPost)
            .where(BlogPost.is_featured == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()