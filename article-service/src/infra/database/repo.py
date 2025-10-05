from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import Category, Comment, UserReaction
from src.domain.base import Entity
from ..protocols import AbstractRepository


class SQLAlchemyHelper(AbstractRepository):
    def __init__(self, session: AsyncSession, model: Entity) -> None:
        self.session = session
        # mapped model from mapping.py
        self.model = model

    @staticmethod
    def new_id() -> UUID:
        # TODO use uuid7
        return uuid4()

    async def insert(self, item: dict[str, Any]) -> None:
        self.session.add(item)

    async def update(self, id: str, changes: dict[str, Any]) -> None:
        stmt = update(self.model).where(self.model.id == id).values(**changes)
        await self.session.execute(stmt)

    async def delete(self, id: str) -> None:
        stmt = delete(self.model).where(self.model.id == id)
        await self.session.execute(stmt)


class SQLCategoryRepo(SQLAlchemyHelper):
    def __init__(self, session):
        super().__init__(session, Category)


class SQLCommentRepo(SQLAlchemyHelper):
    def __init__(self, session):
        super().__init__(session, Comment)


class SQLUserReactionRepo(SQLAlchemyHelper):
    def __init__(self, session):
        super().__init__(session, UserReaction)
