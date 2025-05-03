from dataclasses import dataclass
from enum import Enum, auto

from src.domain.base import Entity


class Role(Enum):
    USER = auto()
    ADMIN = auto()


@dataclass
class RatingData:
    bullet: int
    blitz: int
    rapid: int
    classic: int


@dataclass
class User(Entity):
    name: str
    surname: str
    username: str
    password: str
    email: str
    role: Role
    profile_photo: str | None = None
    lichess_data: RatingData | None = None
    chesscom_data: RatingData | None = None
    
    @classmethod
    def create(cls, id, name: str, surname: str, username: str, password: str, email: str, role: str = "USER"):
        inst = cls(id, name, surname, username, password, email, role)
        inst.role = "USER"
        return inst
