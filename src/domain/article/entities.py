from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Self
from uuid import UUID

from src.domain.base import Entity, datetime_factory


@dataclass
class Tag(Entity):
    name: str

    @classmethod
    def create(
        cls,
        id: str,
        name: str,
    ) -> Self:
        inst = cls(id, name)
        inst.name = name
        return inst


@dataclass
class Article(Entity):
    title: str
    content: dict[str, Any]
    category_id: str
    author_id: str
    preview: str | None = None
    pub_date: datetime = field(default_factory=datetime_factory)
    views: int = 0

    @classmethod
    def create(
        cls,
        id: UUID,
        title: str,
        content: dict[str, Any],
        category_id: str,
        author_id: str,
        preview: str | None = None,
    ) -> Self:
        inst = cls(id, title, content, category_id, author_id, preview)
        inst.title = title
        inst.content = content
        inst.category_id = category_id
        inst.preview = preview
        inst.author_id = author_id
        inst.views = 0
        inst.pub_date = datetime.utcnow()
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
        inst = cls(id, name)
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
        inst.article_id = article_id
        return inst


class Reaction(Enum):
    DISLIKE = -1
    LIKE = 1


@dataclass
class ArticleReaction(Entity):
    article_id: str
    reaction: Reaction

    @classmethod
    def create(cls, id: UUID, article_id: str, reaction: Reaction) -> Self:
        inst = cls(id, article_id, reaction)
        inst.id = id
        return inst
    
    
@dataclass
class Comment(Entity):
    author_id: str
    article_id: str
    text: str
    
    @classmethod
    def create(cls, id: str, author_id: str, article_id: str, text: str):
        inst = cls(id, author_id, article_id, text)
        return inst
