from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import registry, relationship

from src.domain.entities import (
    Article,
    ArticleStatus,
    ReactionType,
    UserReaction,
    Category,
    Comment,
)


mapper_registry = registry()
metadata = mapper_registry.metadata


class ArticleInDb(Article):
    categories: list[Category]


# описание таблиц

article_table = Table(
    "article",
    metadata,
    Column("id", Uuid(as_uuid=False, native_uuid=True), primary_key=True),
    Column("title", String, nullable=False),
    Column("content", JSON),
    Column("user_id", Uuid(as_uuid=False, native_uuid=True), nullable=True),
    Column(
        "status",
        Enum(ArticleStatus, native_enum=True),
        nullable=False,
        server_default="DRAFT",
    ),
    Column("preview", String),
    Column("views", Integer, nullable=False, default=0),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
    Column("updated_at", DateTime, nullable=False, server_default=func.now()),
)

category_table = Table(
    "category",
    metadata,
    Column("id", Uuid, primary_key=True),
    Column("name", String, nullable=False, unique=True),
)


comment_table = Table(
    "comment",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Uuid(as_uuid=False, native_uuid=True), nullable=False),
    Column(
        "article_id",
        Uuid(as_uuid=False, native_uuid=True),
        ForeignKey("article.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("text", Text, nullable=False),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
    Column("updated_at", DateTime, nullable=False, server_default=func.now()),
)

user_reaction_table = Table(
    "user_reaction",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Uuid(as_uuid=False, native_uuid=True), nullable=False),
    Column(
        "article_id",
        Uuid(as_uuid=False, native_uuid=True),
        ForeignKey("article.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "reaction_type",
        Enum(ReactionType, native_enum=True),
        nullable=False,
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
    UniqueConstraint("article_id", "user_id", name="uix_post_user"),
)

article_category_table = Table(
    "article_category",
    metadata,
    Column(
        "article_id",
        Uuid(as_uuid=False, native_uuid=True),
        ForeignKey("article.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "category_id",
        Uuid(as_uuid=False, native_uuid=True),
        ForeignKey("category.id", ondelete="RESTRICT"),
        primary_key=True,
    ),
)

# маппинг
mapper_registry.map_imperatively(
    Category,
    category_table,
    properties={
        "articles": relationship(
            ArticleInDb, secondary=article_category_table, back_populates="categories"
        ),
    },
)

mapper_registry.map_imperatively(
    Comment,
    comment_table,
    properties={"article": relationship(ArticleInDb, back_populates="comments")},
)

mapper_registry.map_imperatively(
    ArticleInDb,
    article_table,
    properties={
        "categories": relationship(
            Category, secondary=article_category_table, back_populates="articles"
        ),
        "comments": relationship(Comment, back_populates="article"),
        "reactions": relationship(UserReaction, back_populates="article"),
    },
)

mapper_registry.map_imperatively(
    UserReaction,
    user_reaction_table,
    properties={"article": relationship(ArticleInDb, back_populates="reactions")},
)
