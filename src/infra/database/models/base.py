from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Table, Uuid
from sqlalchemy.orm import composite, registry, relationship

from src.domain.article.entities import (
    Article,
    ArticleReaction,
    ArticleTag,
    Category,
    Tag,
)
from src.domain.user.entities import User
from src.domain.user.value_objects import FullUserName

mapper_registry = registry()
metadata = mapper_registry.metadata


article_table = Table(
    "article",
    metadata,
    Column("id", Uuid, primary_key=True),
    Column("title", String, nullable=False),
    Column("content", JSON),
    Column("category_id", Uuid, ForeignKey("category.id")),
    Column("preview", String),
    Column("pub_date", DateTime, nullable=False),
    Column("views", Integer, nullable=False, default=0),
)

category_table = Table(
    "category",
    metadata,
    Column("id", Uuid, primary_key=True),
    Column("name", String, nullable=False),
)

tag_table = Table(
    "tag",
    metadata,
    Column("id", Uuid, primary_key=True),
    Column("name", String, nullable=False),
)

article_tag_table = Table(
    "article_tag",
    metadata,
    Column("article_id", Uuid, ForeignKey("article.id"), primary_key=True),
    Column("tag_id", Uuid, ForeignKey("tag.id"), primary_key=True),
)

article_reaction_table = Table(
    "article_reaction",
    metadata,
    Column("id", Uuid, primary_key=True),
    Column("article_id", Uuid, ForeignKey("article.id")),
    Column("reaction", Integer, nullable=False),
)

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
        "full_name": composite(FullUserName, user_table.c.name, user_table.c.surname)
    },
)


mapper_registry.map_imperatively(Tag, tag_table)
mapper_registry.map_imperatively(
    Category,
    category_table,
    properties={"category_info": relationship(Article, back_populates="penis")},
)
mapper_registry.map_imperatively(
    Article,
    article_table,
    properties={"penis": relationship(Category, back_populates="category_info")},
)
mapper_registry.map_imperatively(ArticleReaction, article_reaction_table)
mapper_registry.map_imperatively(ArticleTag, article_tag_table)
