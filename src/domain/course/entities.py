from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Self

from src.domain.base import Entity, datetime_factory


@dataclass
class Course(Entity):
    name: str
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
        description: dict[str, Any],
        author_id: str,
        price: int = 0,
        preview: str | None = None
    ) -> Self:
        inst = cls(id, name, description, author_id, preview, price)
        inst.name = name
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
    min_score: int
    time_limit: int | None = None


@dataclass
class Question(Entity):
    name: str
    test_id: str


@dataclass
class Answer(Entity):
    text: str
    question_id: str
    is_right: bool


@dataclass
class Result(Entity):
    user_id: str
    test_id: str
    passing_time: datetime = field(default_factory=datetime_factory)
