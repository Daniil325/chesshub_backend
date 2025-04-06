from itertools import chain
from pathlib import Path

import pytest
import imgspy
from miniopy_async import Minio
from miniopy_async.deleteobjects import DeleteObject
from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.infra.s3.minio import S3StorageSettings
from src.application.article import ArticleCommandsProvider


here = Path(__file__).parent


@pytest.fixture(scope="session")
def fixtures_path():
    return Path(here).joinpath("fixtures")


def pytest_addoption(parser):
    parser.addini("minio_keys", "access_key:secret_key for minio instance")
    parser.addini(
        "minio_fixture_dir",
        "directory with files for load minio bucked",
        type="paths",
        default=(),
    )


@pytest.fixture
def minio_settings(request) -> S3StorageSettings:
    keys = request.config.getini("minio_keys").split(":")
    bucket_name = "article-images-test"
    settings = S3StorageSettings(
        endpoint="127.0.0.1:9000",
        bucket_name=bucket_name,
        access_key=keys[0],
        secret_key=keys[1],
        secure=False,
    )
    return settings


@pytest.fixture
async def minio_client(request, minio_settings) -> Minio:
    client = Minio(
        endpoint=minio_settings.endpoint,
        access_key=minio_settings.access_key,
        secret_key=minio_settings.secret_key,
        secure=minio_settings.secure,
    )
    bucket_name = minio_settings.bucket_name
    if await client.bucket_exists(bucket_name):
        delete_object_list = [
            DeleteObject(obj.object_name)
            for obj in await client.list_objects(bucket_name, recursive=True)
        ]
        await client.remove_objects(bucket_name, delete_object_list)
        await client.remove_bucket(bucket_name)
    await client.make_bucket(bucket_name)
    path: Path
    for path in request.config.getini("minio_fixture_dir"):
        if path.is_dir():
            for file in chain(path.glob("*.png"), path.glob("*.jpg")):
                img_info = imgspy.info(file)
                content_type = {"jpg": "jpeg"}.get(img_info["type"], img_info["type"])
                await client.fput_object(
                    bucket_name,
                    file.name,
                    file,
                    content_type=f"image/{content_type}",
                    metadata={
                        "height": img_info["height"],
                        "width": img_info["width"],
                    },
                )
    return client


@pytest.fixture
async def container() -> AsyncContainer:
    return make_async_container(ArticleCommandsProvider())


@pytest.fixture
async def app(container):
    app = FastAPI()
    setup_dishka(container, app)
    return app


@pytest.fixture
async def client(app):
    with TestClient(app) as client:
        yield client
