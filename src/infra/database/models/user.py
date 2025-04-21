from sqlalchemy import JSON, Column, String, Table, Uuid
from sqlalchemy.orm import composite

from src.domain.user.value_objects import FullUserName
from src.domain.user.entities import User

from .base import metadata, mapper_registry

user_table = Table(
    "user",
    metadata,
    Column("id", Uuid, primary_key=True),
    Column("name", String, nullable=False),
    Column("surname", String, nullable=False),
    Column("username", String, nullable=False),
    Column("password", String, nullable=False),
    Column("email", String, nullable=False),
    Column("profile_photo", String),
    Column("lichess_data", JSON),
    Column("chesscom_data", JSON),
    Column("role", String, nullable=False),
)

mapper_registry.map_imperatively(
    User,
    user_table,
    properties={
        "full_name": composite(
            FullUserName, user_table.c.name, user_table.c.surname
        )
    }
)
