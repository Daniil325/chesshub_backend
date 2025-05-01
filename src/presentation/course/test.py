from typing import Annotated, Literal

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Path, Query
from pydantic import BaseModel, Field, Json

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
async def get_article(reader: FromDishka[TestReader], id: str = Path()):
    item = check_found(await reader.fetch_by_id(id))
    return {"item": item}
