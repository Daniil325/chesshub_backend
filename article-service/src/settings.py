import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Extra

import yaml

BASE_DIR = Path(__file__).parent.parent



class Settings(BaseSettings):
    dev_mode: bool = False
    pg_dsn: str = "postgresql+asyncpg://user:password@localhost:5252/chesshub_article_db"

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
