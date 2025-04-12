from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter
from pydantic import BaseModel

from src.application.article.tag import (
    CreateTagCommand,
    CreateTagDto,
    UpdateTagDto,
    UpdateTagCommand,
    DeleteTagCommand,
)
from src.presentation.base import ApiInputModelConfig

router = APIRouter(route_class=DishkaRoute)


class CreateTag(BaseModel):
    model_config = ApiInputModelConfig
    name: str


class UpdateTag(BaseModel):
    model_config = ApiInputModelConfig
    tag_id: str
    name: str


@router.post("/")
async def post_tag(tag: CreateTag, cmd: FromDishka[CreateTagCommand]):
    identity = await cmd(CreateTagDto(name=tag.name))
    return identity


@router.patch("/")
async def patch_tag(tag: UpdateTag, cmd: FromDishka[UpdateTagCommand]):
    await cmd(UpdateTagDto(tag_id=tag.tag_id, name=tag.name))


@router.delete("/")
async def delete_tag(tag_id: str, cmd: FromDishka[DeleteTagCommand]):
    await cmd(tag_id)
