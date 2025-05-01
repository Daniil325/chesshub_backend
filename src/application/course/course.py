from dataclasses import asdict, dataclass
from typing import Any

from src.domain.course.entities import Course
from src.domain.course.protocols import CourseRepo
from src.domain.exceptions import DomainError
from src.infra.protocols import S3Storage


@dataclass
class BaseCourseCommand:
    course_repo: CourseRepo
    storage_repo: S3Storage

    async def check_image(self, image_id: str | None):
        if image_id is None:
            return
        if not await self.storage_repo.exists(image_id):
            raise DomainError(f"Image {image_id} does not exist")


@dataclass
class CreateCourseDto:
    name: str
    description: dict[str, Any]
    author_id: str
    price: int
    preview: str | None = None


@dataclass
class CreateCourseCommand(BaseCourseCommand):
    async def __call__(self, dto: CreateCourseDto) -> str:
        identity = self.course_repo.new_id()
        await self.check_image(dto.preview)
        course = Course.create(
            identity, dto.name, dto.description, dto.author_id, dto.preview, dto.price
        )
        await self.course_repo.add(course)
        return identity


@dataclass
class UpdateCourseDto:
    id: str
    name: str
    description: dict[str, Any]
    price: int
    preview: str | None = None


@dataclass
class UpdateCourseCommand(BaseCourseCommand):
    async def __call__(self, dto: UpdateCourseDto) -> None:
        course = await self.course_repo.get(dto.id)
        await self.check_image(dto.preview)
        course.name = dto.name
        course.description = dto.description
        course.price = dto.price
        course.preview = dto.preview
        await self.course_repo.update(dto.id, asdict(course))
        
        
@dataclass
class DeleteCourseCommand:
    course_repo: CourseRepo
    
    async def __call__(self, course_id: str) -> str:
        await self.course_repo.delete(course_id)
        return course_id
