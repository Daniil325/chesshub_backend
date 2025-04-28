from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from src.domain.course.entities import Answer, Course, Lesson, Question, Result, Test


class CourseRepo(ABC):
    
    @abstractmethod
    def new_id(self) -> str: ...

    @abstractmethod
    async def add(self, item: Course) -> None: ...

    @abstractmethod
    async def get(self, id: UUID) -> Course | None: ...

    @abstractmethod
    async def update(self, id: UUID, changes: dict[str, Any]) -> None: ...

    @abstractmethod
    async def delete(self, id: UUID) -> None: ...
    
    
class LessonRepo(ABC):
    
    @abstractmethod
    def new_id(self) -> str: ...

    @abstractmethod
    async def add(self, item: Lesson) -> None: ...

    @abstractmethod
    async def get(self, id: UUID) -> Lesson | None: ...

    @abstractmethod
    async def update(self, id: UUID, changes: dict[str, Any]) -> None: ...

    @abstractmethod
    async def delete(self, id: UUID) -> None: ...
    
    
class TestRepo(ABC):
    
    @abstractmethod
    def new_id(self) -> str: ...

    @abstractmethod
    async def add(self, item: Test) -> None: ...

    @abstractmethod
    async def get(self, id: UUID) -> Test | None: ...

    @abstractmethod
    async def update(self, id: UUID, changes: dict[str, Any]) -> None: ...

    @abstractmethod
    async def delete(self, id: UUID) -> None: ...
    
    
class QuestionRepo(ABC):
    
    @abstractmethod
    def new_id(self) -> str: ...

    @abstractmethod
    async def add(self, item: Question) -> None: ...

    @abstractmethod
    async def get(self, id: UUID) -> Question | None: ...

    @abstractmethod
    async def update(self, id: UUID, changes: dict[str, Any]) -> None: ...

    @abstractmethod
    async def delete(self, id: UUID) -> None: ...
    
    
class AnswerRepo(ABC):
    
    @abstractmethod
    def new_id(self) -> str: ...

    @abstractmethod
    async def add(self, item: Answer) -> None: ...

    @abstractmethod
    async def get(self, id: UUID) -> Answer | None: ...

    @abstractmethod
    async def update(self, id: UUID, changes: dict[str, Any]) -> None: ...

    @abstractmethod
    async def delete(self, id: UUID) -> None: ...
    
    
class ResultRepo(ABC):
    
    @abstractmethod
    def new_id(self) -> str: ...

    @abstractmethod
    async def add(self, item: Result) -> None: ...

    @abstractmethod
    async def get(self, id: UUID) -> Result | None: ...

    @abstractmethod
    async def update(self, id: UUID, changes: dict[str, Any]) -> None: ...

    @abstractmethod
    async def delete(self, id: UUID) -> None: ...