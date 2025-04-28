from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from src.domain.base import Entity, datetime_factory


@dataclass
class Course(Entity):
    name: str
    description: dict[str, Any]
    author_id: str
    pub_date: datetime = field(default_factory=datetime_factory)
    price: int = 0


@dataclass
class Lesson(Entity):
    name: str
    course_id: str
    content: dict[str, Any]
    test_id: str | None = None


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
