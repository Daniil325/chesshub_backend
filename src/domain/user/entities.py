from dataclasses import dataclass
from enum import Enum, auto

from .value_objects import FullUserName
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
    full_name: FullUserName
    username: str
    password: str
    email: str
    profile_photo: str | None = None
    lichess_data: RatingData | None = None
    chesscom_data: RatingData | None = None
    role: Role
