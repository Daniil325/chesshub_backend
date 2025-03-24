from typing import Any, TypeVar
from uuid import UUID, uuid4

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class SqlHelper[T]:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @staticmethod
    def new_id() -> UUID:
        # TODO use uuid7
        return uuid4()

    async def get_all(self) -> list[T]:
        stmt = select(T)
        return (await self.session.execute(stmt)).scalars()

    async def get(self, id: UUID) -> T | None:
        stmt = select(T).where(T.id == id)
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def create(self, item: T) -> None:
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)

    async def update(self, changes: dict[str, Any], id: UUID) -> None:
        stmt = update(T).where(T.id == id).values(**changes)
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete(self, id: UUID) -> None:
        stmt = delete(T).where(T.id == id)
        await self.session.execute(stmt)
        await self.session.commit()


class TagRepo(SqlHelper):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

class CategoryRepo(SqlHelper):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

class ArticleTagRepo(SqlHelper):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

class ArticalReactionRepo(SqlHelper):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
