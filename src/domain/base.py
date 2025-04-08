from datetime import UTC, datetime
from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Entity:
    id: str = field(default_factory=uuid4, kw_only=True)

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
