from typing import Annotated, Any, Literal
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Path, Query
from pydantic import BaseModel, Field

from src.application.course.lesson import (
    CreateLessonCommand,
    CreateLessonDto,
    DeleteLessonCommand,
    UpdateLessonCommand,
    UpdateLessonDto,
)
from src.infra.database.reader import LessonReader
from src.presentation.base import SuccessResponse, check_found

router = APIRouter(route_class=DishkaRoute)


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["name"] = "name"
    filter: str = ""


@router.get("/")
async def get_lessons_list(
    filter_query: Annotated[FilterParams, Query()], reader: FromDishka[LessonReader]
):
    result = await reader.fetch_list(
        filter_query.offset,
        filter_query.limit,
        filter_query.filter,
        filter_query.order_by,
    )
    return {
        "items": result,
        "page": filter_query.offset + 1,
        "per_page": filter_query.limit,
    }


@router.get("/{id}")
async def get_lesson(reader: FromDishka[LessonReader], id: str = Path()):
    item = check_found(await reader.fetch_by_id(id))
    return {"item": item}


class CreateLesson(BaseModel):
    course_id: str
    name: str
    content: dict[str, Any]
    test_id: str | None = None


@router.post("/", response_model=SuccessResponse)
async def post_lesson(lesson: CreateLesson, cmd: FromDishka[CreateLessonCommand]):
    identity = await cmd(CreateLessonDto(lesson.name, lesson.course_id, lesson.content, lesson.test_id))
    return identity


class UpdateLesson(CreateLesson):
    id: str


@router.patch("/{id}", response_model=SuccessResponse)
async def update_lesson(
    lesson: UpdateLesson, cmd: FromDishka[UpdateLessonCommand], id: UUID = Path(...)
):
    await cmd(UpdateLessonDto(lesson_id=id, **lesson))
    return SuccessResponse()


@router.delete("/{id}", response_model=SuccessResponse)
async def delete_lesson(cmd: FromDishka[DeleteLessonCommand], id: UUID = Path(...)):
    await cmd(id)
    return SuccessResponse()
