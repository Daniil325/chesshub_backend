from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka

from src.infra.s3 import S3Provider
from src.settings import load_settings

from src.infra.database import DBSessionProvider, SqlProvider
from src.application.article import ArticleCommandsProvider
from src.presentation.article import router as article_router
from src.infra.database.models.base import metadata

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


def base_create_app():
    app = FastAPI(lifespan=lifespan)
    app.include_router(article_router)
    # setup_exception_handlers(app)
    return app


def create_app() -> FastAPI:
    app = base_create_app()
    settings = load_settings()
    print(metadata)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    container = make_async_container(
        DBSessionProvider(settings.pg_dsn),
        SqlProvider(),
        S3Provider(settings),
        ArticleCommandsProvider(),
    )
    setup_dishka(container, app)
    return app
