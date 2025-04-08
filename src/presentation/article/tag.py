from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter
from pydantic import BaseModel

from src.application.article.tag import CreateTagCommand, CreateTagDto
from src.presentation.base import ApiInputModelConfig

router = APIRouter(route_class=DishkaRoute)


class CreateTag(BaseModel):
    model_config = ApiInputModelConfig
    name: str


@router.post("/")
async def post_tag(tag: CreateTag, cmd: FromDishka[CreateTagCommand]):
    identity = await cmd(CreateTagDto(name=tag.name))
    return identity
