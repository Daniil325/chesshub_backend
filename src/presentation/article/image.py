from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Path, Query, UploadFile
from pydantic import BaseModel

from src.application.article.image import CreateImageCommand, CreateImageDto
from src.infra.s3.minio import ImageDescr, MinioImageRepo
from src.presentation.base import APIModelConfig

router = APIRouter(route_class=DishkaRoute)


class ImagesList(BaseModel):
    model_config = APIModelConfig
    items: list[ImageDescr] = []
    next: str | None = None


@router.get("/", response_model=ImagesList)
async def list_images(
    storage: FromDishka[MinioImageRepo],
    prefix: str | None = Query(None),
    next: str | None = Query(None),
):
    items = [it async for it in storage.list(prefix, start_after=next)]
    return ImagesList(items=items, next=items and items[-1].name or None)


@router.get("/{image_id}", response_model=ImageDescr)
async def get_image(storage: FromDishka[MinioImageRepo], image_id: str = Path(...)):
    return await storage.get(image_id)


@router.post("/", response_model=ImageDescr)
async def upload_image(
    image: UploadFile,
    storage: FromDishka[MinioImageRepo],
    cmd: FromDishka[CreateImageCommand],
):
    image_id = await cmd(
        CreateImageDto(
            filename=image.filename,
            content_type=image.content_type,
            file=image.file,
            size=image.size,
        )
    )
    return await storage.get(image_id)
