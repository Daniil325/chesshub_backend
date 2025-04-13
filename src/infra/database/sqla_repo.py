from typing import Any, TypeVar
from uuid import UUID, uuid4

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.article.entities import (
    Article,
    ArticleReaction,
    ArticleTag,
    Category,
    Tag,
)
from src.domain.article.protocols import ArticleRepo, ArticleTagRepo, TagRepo

T = TypeVar("T")


class SqlHelper[T]:

    def __init__(self, session: AsyncSession, model) -> None:
        self.session = session
        self.model = model

    @staticmethod
    def new_id() -> UUID:
        # TODO use uuid7
        return uuid4()

    async def get_all(self) -> list[T]:
        stmt = select(self.model)
        return (await self.session.execute(stmt)).scalars()

    async def get(self, id: UUID) -> T | None:
        stmt = select(self.model).where(self.model.id == id)
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def add(self, item: T) -> None:
        print(item, "писька")
        try:
            self.session.add(item)
            await self.session.commit()
            await self.session.refresh(item)
        except Exception:
            await self.session.rollback()
            raise

    async def update(self, id: UUID, changes: dict[str, Any]) -> None:
        stmt = update(self.model).where(self.model.id == id).values(**changes)
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete(self, id: UUID) -> None:
        stmt = delete(self.model).where(self.model.id == id)
        await self.session.execute(stmt)
        await self.session.commit()


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
