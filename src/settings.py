import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import BaseModel, Extra, PostgresDsn

import yaml
from src.infra.s3.minio import S3StorageSettings

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    
    access_token_expire_minutes: int = 3


class Settings(BaseSettings):
    dev_mode: bool = False
    pg_dsn: PostgresDsn = "postgresql+asyncpg://user:password@localhost:5252/chesshub_db"
    storage: S3StorageSettings | None = None
    auth_jwt: AuthJWT = AuthJWT()

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"
        extra = Extra.ignore


def load_settings() -> Settings:
    filename = os.environ.get("APP_CONFIG_FILE", "config.yml")
    if os.path.isfile(filename):
        with open(filename) as fd:
            config = yaml.load(fd, Loader=yaml.SafeLoader)
    else:
        config = {}
    return Settings.model_validate(config)
