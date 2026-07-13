from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )
    RBD_EMAIL : str
    RBD_PASSWORD : str
    LOGIN_URL : str = "https://rbd.kz/backend/app/rest/auth/login"
    LIST_URL : str = "https://rbd.kz/backend/app/rest/supply/search/list"
    GET_URL : str = "https://rbd.kz/backend/app/rest/supply/get"

    # --- DB ---
    DATABASE_URL : str

    # --- BASE_DIR ---
    FILES_DIR : Path = BASE_DIR / 'files'

    # --- LLM ---
    OLLAMA_URL : str = "http://localhost:11434/api/generate"
    MODEL : str = "second_constantine/t-lite-it-2.1:8b"

settings = Settings()