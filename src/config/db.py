from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    SYNC_DRIVER: str = "postgresql+psycopg"
    ASYNC_DRIVER: str = "postgresql+asyncpg"
    USER: SecretStr = SecretStr("")
    PASSWORD: SecretStr = SecretStr("")
    HOST: SecretStr = SecretStr("")
    PORT: str = "5432"
    NAME: SecretStr = SecretStr("")

    model_config = SettingsConfigDict(
        env_prefix="POSTGRES_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def SYNC_URL(self) -> SecretStr:
        return SecretStr(
            f"{self.SYNC_DRIVER}://{self.USER.get_secret_value()}:{self.PASSWORD.get_secret_value()}@{self.HOST.get_secret_value()}:{self.PORT}/{self.NAME.get_secret_value()}"
        )

    @property
    def ASYNC_URL(self) -> SecretStr:
        return SecretStr(
            f"{self.ASYNC_DRIVER}://{self.USER.get_secret_value()}:{self.PASSWORD.get_secret_value()}@{self.HOST.get_secret_value()}:{self.PORT}/{self.NAME.get_secret_value()}"
        )


db_settings = PostgresSettings()
