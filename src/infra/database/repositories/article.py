from typing import Any
from uuid import UUID
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.article.protocols import ArticleRepo, ArticleTagRepo, TagRepo
from src.infra.database.sqla_repo import SqlHelper
from src.domain.article.entities import (
    Article,
    ArticleReaction,
    ArticleTag,
    Category,
    Tag,
)


class SqlTagRepo(SqlHelper, TagRepo):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Tag)


class SqlCategoryRepo(SqlHelper):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Category)


class SqlArticleTagRepo(SqlHelper, ArticleTagRepo):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ArticleTag)

    async def get(self, tag_id: UUID, article_id: UUID):
        stmt = select(self.model).where(
            self.model.tag_id == tag_id and self.model.article_id == article_id
        )
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def update(
        self, tag_id: UUID, article_id: UUID, changes: dict[str, Any]
    ) -> None:
        print("ssss", tag_id, article_id)
        stmt = (
            update(self.model)
            .where(self.model.tag_id == tag_id and self.model.article_id == article_id)
            .values(**changes)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete(self, tag_id: UUID, article_id: UUID) -> None:
        stmt = delete(self.model).where(
            self.model.tag_id == tag_id and self.model.article_id == article_id
        )
        await self.session.execute(stmt)
        await self.session.commit()


class SqlArticleReactionRepo(SqlHelper):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ArticleReaction)


class SqlArticleRepo(SqlHelper, ArticleRepo):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Article)

    async def get_by_category(self, category_id: str) -> list[Article]:
        stmt = select(Article).where(Article.category_id == category_id)
        return (await self.session.execute(stmt)).scalars()

    async def get_by_author(self, author_id: str) -> list[Article]:
        stmt = select(Article).where(Article.author_id == author_id)
        return (await self.session.execute(stmt)).scalars()
