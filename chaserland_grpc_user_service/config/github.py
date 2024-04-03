from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class GithubSettings(BaseSettings):
    OAUTH_CLIENT_ID: str = ""
    OAUTH_CLIENT_SECRET: SecretStr = SecretStr("")

    model_config = SettingsConfigDict(
        env_prefix="GITHUB_", env_file=".env", env_file_encoding="utf-8"
    )


github_settings = GithubSettings()
