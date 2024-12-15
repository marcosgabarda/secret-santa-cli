"""Package with all the implementation for execute a Secret Santa game."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    """Configuration for the secret santa game."""

    # email notification defaults
    default_notification_from: str = "Amigo Invisible <amigoinvisible@mgabarda.com>"
    default_notification_subject: str = "Sorteo Amigo Invisible"

    # mailgun settings
    mailgun_api_url: str
    mailgun_api_key: SecretStr

    # debug
    debug: bool = False
    debug_to_email: str | None = None

    # attempts limit
    limit: int = 30

    model_config = SettingsConfigDict(
        env_prefix="santa_", env_file=".env", env_file_encoding="utf-8"
    )


settings = Settings()  # type: ignore
