"""Package with all the implementation for execute a Secret Santa game."""

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration for the secret santa game."""

    # mailgun settings
    mailgun_api_url: str
    mailgun_api_key: SecretStr

    # attempts limit
    limit: int = 30

    model_config = SettingsConfigDict(
        env_prefix="santa_", env_file=".env", env_file_encoding="utf-8"
    )


settings = Settings()  # type: ignore
