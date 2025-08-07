import os
from dataclasses import field
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
dot_env = os.path.join(BASE_DIR, ".env")


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=dot_env,
        env_file_encoding="utf-8",
        extra="ignore",
    )


class DatabaseSettings(EnvSettings):
    DB_NAME: str = "postgres"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = ""
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"

    @property
    def database_url(self):
        """URL database Postgres."""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class AppSettings(EnvSettings):
    DEBUG: bool = False
    CORS_ORIGIN: List[str] = field(default=["*"])
    BACK_URL: str = "127.0.0.1"
    FRONT_URL: str = "127.0.0.1"
    MEDIA_ROOT: str = "media"


class Config(EnvSettings):
    app: AppSettings = AppSettings()
    db: DatabaseSettings = DatabaseSettings()


config = Config()
