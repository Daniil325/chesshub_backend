from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Self

from src.domain.base import Entity, datetime_factory


class ReactionType(Enum):
    DISLIKE = -1
    LIKE = 1


class ArticleStatus(Enum):
    PUBLISHED = "published"
    DRAFT = "draft"
    BLOCKED = "blocked"


@dataclass
class Category(Entity):
    name: str

    @classmethod
    def create(
        cls,
        name: str,
    ) -> Self:
        inst = cls(name)
        inst.name = name
        return inst


@dataclass
class UserReaction:
    id: int
    user_id: str
    article_id: str
    reaction_type: ReactionType
    created_at: datetime = field(default_factory=datetime_factory)

    @classmethod
    def create(
        cls,
        user_id: str,
        article_id: str,
        reaction_type: ReactionType,
        created_at: datetime,
    ) -> Self:
        inst = cls(id, user_id, article_id, reaction_type, created_at)
        return inst


@dataclass
class Article(Entity):
    title: str
    content: dict[str, Any]
    user_id: str
    status: str
    created_at: datetime = field(default_factory=datetime_factory)
    preview: str | None = None
    updated_at: datetime = field(default_factory=datetime_factory)
    views: int = 0

    @classmethod
    def create(
        cls,
        title: str,
        content: dict[str, Any],
        user_id: str,
        status: str,
        created_at: datetime,
        preview: str | None = None,
    ) -> Self:
        inst = cls(id, title, content, user_id, status, preview, created_at)
        inst.updated_at = datetime.utcnow()
        inst.views = 0
        return inst


@dataclass
class Comment:
    id: int
    user_id: str
    article_id: str
    text: str
    created_at: datetime = field(default_factory=datetime_factory)
    updated_at: datetime = field(default_factory=datetime_factory)

    @classmethod
    def create(
        cls, user_id: str, article_id: str, text: str, created_at: datetime
    ) -> Self:
        inst = cls(id, user_id, article_id, text, created_at)
        inst.updated_at = datetime.utcnow()
        return inst
