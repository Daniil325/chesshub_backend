from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class DBSession:
    def __init__(self, url, debug: bool = False, readonly: bool = False):
        engine = create_async_engine(
            str(url), echo=debug, pool_pre_ping=True, pool_recycle=3600
        )
        # Not use transaction for read-only connections
        self.engine = (
            engine.execution_options(isolation_level="AUTOCOMMIT")
            if readonly
            else engine
        )
        self.sessionmaker = async_sessionmaker(self.engine, expire_on_commit=False)

    async def get_session(self) -> AsyncSession:
        return self._async_session
    
    async def __aenter__(self):
        self._async_session = self.sessionmaker()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None and not self.engine.execution_options.get("isolation_level"):
            await self._async_session.commit()
        else:
            await self._async_session.rollback()
        await self._async_session.close()
        self._async_session = None

    @staticmethod
    def async_pg_url(
        pg_user: str, pg_password: str, pg_host: str, pg_port: str, pg_db: str
    ) -> str:
        return (
            f"postgresql+asyncpg://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"
        )

    async def close(self):
        await self.engine.dispose()
