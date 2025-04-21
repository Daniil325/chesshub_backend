from typing import Any, TypeVar
from uuid import UUID, uuid4

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

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
