import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    NAME: str = "gRPC User Service"
    ENV: str = "prod"
    DEBUG: bool = False

    BASE_PATH: str = str(Path(os.path.abspath(__file__)).parents[2])

    HOST: str = "[::]"
    PORT: int = 50051

    model_config = SettingsConfigDict(
        env_prefix="APP_", env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    @property
    def server_address(self) -> str:
        return f"{self.HOST}:{self.PORT}"


app_settings = Settings()
