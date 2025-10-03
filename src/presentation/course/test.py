from typing import Annotated, Literal
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Path, Query
from pydantic import BaseModel, Field

from src.application.course.test import (
    CreateTestCommand,
    DeleteTestCommand,
    TestDto,
    UpdateTestCommand,
    UpdateTestDto,
)
from src.infra.database.reader import TestReader
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
    order_by: Literal["name"] = "name"
    filter: str = ""


@router.get("/")
async def get_tests_list(
    filter_query: Annotated[FilterParams, Query()], reader: FromDishka[TestReader]
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
async def get_test(reader: FromDishka[TestReader], id: str = Path()):
    item = check_found(await reader.fetch_by_id(id))
    return {"item": item}


class CreateTest(BaseModel):
    name: str
    min_score: int = 0


@router.post("/", response_model=SuccessResponse)
async def post_test(test: CreateTest, cmd: FromDishka[CreateTestCommand]):
    identity = await cmd(TestDto(test.name, test.min_score, 0))
    return identity


class UpdateTest(CreateTest):
    id: str


@router.patch("/{id}", response_model=SuccessResponse)
async def update_test(
    test: UpdateTest, cmd: FromDishka[UpdateTestCommand], id: UUID = Path(...)
):
    await cmd(UpdateTestDto(test_id=id, **test))
    return SuccessResponse()


@router.delete("/{id}", response_model=SuccessResponse)
async def delete_test(cmd: FromDishka[DeleteTestCommand], id: UUID = Path(...)):
    await cmd(id)
    return SuccessResponse()
