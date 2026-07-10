from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore")

    APP_NAME: str = "qonys-service"
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str

    CORS_ORIGINS: list[str] = ["*"]

    # -- LLM --
    OLLAMA_URL: str = "http://localhost:11434/api/generate"
    MODEL: str = "second_constantine/t-lite-it-2.1:8b"


settings = Settings()
