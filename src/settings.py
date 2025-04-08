import os
from pydantic_settings import BaseSettings
from pydantic import Extra, PostgresDsn

from src.infra.s3.minio import S3StorageSettings


class Settings(BaseSettings):
    dev_mode: bool = False
    pg_dsn: PostgresDsn = "postgresql+asyncpg://user:password@localhost:5252/chesshub_db"
    storage: S3StorageSettings | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"
        extra = Extra.ignore


settings = Settings()
