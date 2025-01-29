from passlib.context import CryptContext
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config: SettingsConfigDict = {
        "env_file": ".env",
        "env_ignore_empty": True,
        "extra": "ignore",
    }

    ALGORITHM: str = "HS256"

    CURRENT_API_URL: str = "/api/v1"

    PASSWORD_CONTEXT: CryptContext = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto",
    )

    SECRET_KEY: str

    # 60 minutes * 24 hours * 8 days = 8 days
    VALID_TOKEN_IN_MINUTES: int = 60 * 24 * 8


appConfig: Settings = Settings()
