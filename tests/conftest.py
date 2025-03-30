from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from src.application.article import ArticleCommandsProvider


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
