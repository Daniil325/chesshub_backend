from typing import Any
from uuid import UUID
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.course.entities import Answer, Course, Lesson, Question, Test
from src.domain.course.protocols import (
    AnswerRepo,
    CourseRepo,
    LessonRepo,
    QuestionRepo,
    TestRepo,
)
from src.infra.database.sqla_repo import SqlHelper


class SqlAnswerRepo(SqlHelper, AnswerRepo):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Answer)


class SqlQuestionRepo(SqlHelper, QuestionRepo):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Question)

    async def get_by_test(self, test_id: UUID) -> list[Question]: ...


class SqlTestRepo(SqlHelper, TestRepo):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Test)


class SqlLessonRepo(SqlHelper, LessonRepo):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Lesson)


class SqlCourseRepo(SqlHelper, CourseRepo):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Course)
