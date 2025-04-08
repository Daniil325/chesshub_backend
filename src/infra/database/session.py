from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.domain.base import Singleton


class DBSession:

    def __init__(self, url):
        self._async_session: AsyncSession = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=create_async_engine(
                echo=True,
                url=str(url)
            ),
        )()

    async def get_session(self) -> AsyncSession:
        return self._async_session

    @staticmethod
    def async_pg_url(
        pg_user: str, pg_password: str, pg_host: str, pg_port: str, pg_db: str
    ) -> str:
        return (
            f"postgresql+asyncpg://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"
        )
