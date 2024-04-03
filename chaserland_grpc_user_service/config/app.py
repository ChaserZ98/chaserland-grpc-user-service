import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    NAME: str = "gRPC User Service"
    ENV: str = "prod"
    DEBUG: bool = False

    BASE_PATH: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    HOST: str = "[::]"
    PORT: int = 50051

    model_config = SettingsConfigDict(
        env_prefix="APP_", env_file=".env", env_file_encoding="utf-8"
    )

    @property
    def server_address(self) -> str:
        return f"{self.HOST}:{self.PORT}"


app_settings = Settings()
