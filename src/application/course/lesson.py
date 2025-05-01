from dataclasses import dataclass
from typing import Any

from src.domain.course.entities import Lesson
from src.domain.course.protocols import LessonRepo
from src.domain.exceptions import DomainError
from src.infra.protocols import S3Storage


@dataclass
class BaseCommand:
    lesson_repo: LessonRepo
    storage_repo: S3Storage

    async def check_image(self, image_id: str | None):
        if image_id is None:
            return
        if not await self.storage_repo.exists(image_id):
            raise DomainError(f"Image {image_id} does not exist")
        
        
@dataclass
class CreateLessonDto:
    name: str
    course_id: str
    content: dict[str, Any]
    test_id: str | None = None
    
    
@dataclass
class CreateLessonCommand(BaseCommand):
    
    async def __call__(self, dto: CreateLessonDto) -> str:
        identity = self.lesson_repo.new_id()
        lesson = Lesson.create(identity, dto.name, dto.course_id, dto.content, dto.test_id)
        await self.lesson_repo.add(lesson)
        return identity
    

@dataclass
class UpdateLessonDto:
    id: str
    name: str
    course_id: str
    content: dict[str, Any]
    
    
@dataclass
class UpdateLessonCommand(BaseCommand):
    
    async def __call__(self, dto: UpdateLessonDto) -> None:
        lesson = await self.lesson_repo.get(dto.id)
        lesson.name = dto.name
        lesson.content = dto.content
        lesson.test_id = dto.test_id
        await self.lesson_repo.update(dto.id, lesson)
        
        
@dataclass
class DeleteLessonCommand:
    lesson_repo: LessonRepo
    
    async def __call__(self, lesson_id: str) -> str:
        await self.lesson_repo.delete(lesson_id)
        return lesson_id