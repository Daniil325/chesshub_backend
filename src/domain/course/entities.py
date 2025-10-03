from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Self

from src.domain.base import Entity, datetime_factory


@dataclass
class Course(Entity):
    name: str
    subtitle: str
    description: dict[str, Any]
    author_id: str
    preview: str | None = None
    pub_date: datetime = field(default_factory=datetime_factory)
    price: int = 0

    @classmethod
    def create(
        cls,
        id: str,
        name: str,
        subtitle: str,
        description: dict[str, Any],
        author_id: str,
        price: int = 0,
        preview: str | None = None
    ) -> Self:
        inst = cls(id, name, subtitle, description, author_id, preview, price)
        inst.name = name
        inst.subtitle = subtitle
        inst.description = description
        inst.author_id = author_id
        inst.preview = preview
        inst.price = price
        inst.pub_date = datetime.utcnow()
        return inst


@dataclass
class Lesson(Entity):
    name: str
    course_id: str
    content: dict[str, Any]
    test_id: str | None = None
    
    @classmethod
    def create(cls, id: str, name: str, course_id: str, content: dict[str, Any], test_id: str | None = None):
        inst = cls(id, name, course_id, content, test_id)
        inst.name = name
        inst.content = content
        inst.course_id = course_id
        inst.test_id = test_id
        return inst


@dataclass
class Test(Entity):
    name: str
    min_score: int = 0
    time_limit: int = 0

    @classmethod
    def create(cls, id: str, name: str, min_score: int = 0, time_limit: int = 0):
        inst = cls(id, name, min_score, time_limit)
        return inst


@dataclass
class Question(Entity):
    name: str
    test_id: str

    @classmethod
    def create(cls, id: str, name: str, test_id: str) -> Self:
        inst = cls(id, name, test_id)
        return inst


@dataclass
class Answer(Entity):
    text: str
    question_id: str
    is_right: bool

    @classmethod
    def create(cls, id: str, name: str, test_id: str) -> Self:
        inst = cls(id, name, test_id)
        return inst


@dataclass
class Result(Entity):
    user_id: str
    test_id: str
    passing_time: datetime = field(default_factory=datetime_factory)
