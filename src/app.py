from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.application.user import UserProvider
from src.infra.auth import JwtProvider
from src.application.course import CourseCommandsProvider
from src.application.article import ArticleCommandsProvider
from src.infra.database import DBSessionProvider, ReadersProvider, SqlProvider
from src.infra.s3 import S3Provider
from src.presentation.article import router as article_router
from src.presentation.course import router as course_router
from src.presentation.user import router as user_router
from src.presentation.article.ingetrations import router as ingetrations_router
from src.settings import load_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


def base_create_app():
    app = FastAPI(lifespan=lifespan)
    app.include_router(article_router)
    app.include_router(course_router)
    app.include_router(user_router)
    app.include_router(ingetrations_router)
    # setup_exception_handlers(app)
    return app


def create_app() -> FastAPI:
    app = base_create_app()
    settings = load_settings()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    container = make_async_container(
        DBSessionProvider(settings.pg_dsn),
        SqlProvider(),
        S3Provider(settings),
        ArticleCommandsProvider(),
        CourseCommandsProvider(),
        ReadersProvider(),
        JwtProvider(settings),
        UserProvider()
    )
    
    setup_dishka(container, app)
    return app
