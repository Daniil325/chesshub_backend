from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Self

from src.domain.base import Entity, datetime_factory


@dataclass
class Article(Entity):
    title: str
    content: dict[str, Any]
    category_id: str
    preview: str | None = None
    pud_date: datetime = field(default_factory=datetime_factory)
    views: int = 0

    @classmethod
    def create(
        cls,
        id: str,
        title: str,
        content: dict[str, Any],
        category_id: str,
        preview: str | None = None,
    ) -> Self:
        inst = cls(id, title, content, category_id, preview)
        inst.title = title
        inst.content = content
        inst.category_id = category_id
        inst.preview = preview
        inst.views = 0
        inst.pud_date = datetime.utcnow()
        return inst


@dataclass
class Category(Entity):
    name: str

    @classmethod
    def create(
        cls,
        id: str,
        name: str,
    ) -> Self:
        inst = cls(id)
        inst.name = name
        return inst


@dataclass
class Tag(Entity):
    name: str

    @classmethod
    def create(
        cls,
        id: str,
        name: str,
    ) -> Self:
        inst = cls(id)
        inst.name = name
        return inst


@dataclass
class ArticleTag:
    tag_id: str
    article_id: str

    @classmethod
    def create(
        cls,
        tag_id: str,
        article_id: str,
    ) -> Self:
        inst = cls(tag_id, article_id)
        inst.tag_id = tag_id
        inst.article_id = tag_id
        return inst


class Reaction(Enum):
    DISLIKE = -1
    LIKE = 1


@dataclass
class ArticleReaction(Entity):
    article_id: str
    reaction: Reaction

    @classmethod
    def create(cls, id: str, article_id: str, reaction: Reaction) -> Self:
        inst = cls(article_id, reaction)
        inst.id = id
        return inst
