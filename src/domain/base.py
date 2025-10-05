from abc import ABC, abstractmethod
from datetime import UTC, datetime
from dataclasses import dataclass
from typing import Any, TypeVar
from uuid import UUID


@dataclass
class Entity:
    id: UUID

    def __eq__(self, other) -> bool:
        if not isinstance(other, Entity):
            return False
        return self.__class__ == other.__class__ and self.id == other.id


def datetime_factory():
    return datetime.now(tz=UTC)


class Singleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    
T = TypeVar("T")
    
    
class BaseRepo(ABC):
    
    @abstractmethod
    def new_id(self) -> str: ...

    @abstractmethod
    async def add(self, item: T) -> None: ...

    @abstractmethod
    async def get(self, id: str) -> T | None: ...

    @abstractmethod
    async def update(self, id: str, changes: dict[str, Any]) -> None: ...

    @abstractmethod
    async def delete(self, id: str) -> None: ...
