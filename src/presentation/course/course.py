from typing import Annotated, Literal
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Path, Query
from pydantic import BaseModel, Field, Json

from src.application.course.course import CreateCourseCommand, CreateCourseDto, DeleteCourseCommand, UpdateCourseCommand, UpdateCourseDto
from src.infra.database.reader import CourseReader
from src.presentation.base import (
    APIModelConfig,
    ApiInputModelConfig,
    ModelResponse,
    PaginatedListResponse,
    SuccessResponse,
    check_found,
)

router = APIRouter(route_class=DishkaRoute)


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["pub_date", "-pub_date", "views", "-views"] = "pub_date"
    filter: str = ""


@router.get("/")
async def get_courses_list(
    filter_query: Annotated[FilterParams, Query()], reader: FromDishka[CourseReader]
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
async def get_article(reader: FromDishka[CourseReader], id: str = Path()):
    item = check_found(await reader.fetch_by_id(id))
    return {"item": item}


class CreateCourse(BaseModel):
    model_config = ApiInputModelConfig
    name: str
    description: Json
    author_id: str
    price: int
    preview: str | None = None


@router.post("/", response_model=SuccessResponse)
async def post_article(course: CreateCourse, cmd: FromDishka[CreateCourseCommand]):
    identity = await cmd(
        CreateCourseDto(
            course.name, course.description, course.author_id, course.price, course.preview
        )
    )
    return identity



class UpdateArticle(BaseModel):
    model_config = ApiInputModelConfig
    title: str
    description: Json
    category_id: str
    preview: str | None = None


@router.patch("/{id}", response_model=SuccessResponse)
async def update_article(
    article: UpdateArticle, cmd: FromDishka[UpdateCourseCommand], id: UUID = Path(...)
):
    await cmd(UpdateCourseDto(article_id=id, **article))
    return SuccessResponse()


@router.delete("/{id}", response_model=SuccessResponse)
async def delete_article(cmd: FromDishka[DeleteCourseCommand], id: UUID = Path(...)):
    await cmd(id)
    return SuccessResponse()