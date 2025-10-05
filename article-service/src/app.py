from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .settings import load_settings
from src.infra.database import DBSessionFactory, DBFactory
from src.infra.database.mapping import mapper_registry
from src.application import ServiceFactory
from src.api import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


def base_create_app():
    app = FastAPI(lifespan=lifespan)
    app.include_router(router)
    # setup_exception_handlers(app)
    return app


def create_app() -> FastAPI:
    app = base_create_app()
    settings = load_settings()
    (mapper_registry)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    container = make_async_container(
        DBSessionFactory(settings.pg_dsn),
        DBFactory(),
        ServiceFactory(),
    )

    setup_dishka(container, app)
    return app
