from pathlib import Path

from environs import Env

env = Env()
env.read_env()

class Settings:
    def __init__(self):
        self.username = env.str("RBD_EMAIL")
        self.password = env.str("RBD_PASSWORD")
        self.LOGIN_URL = "https://rbd.kz/backend/app/rest/auth/login"
        self.LIST_URL = "https://rbd.kz/backend/app/rest/supply/search/list"
        self.GET_URL = "https://rbd.kz/backend/app/rest/supply/get"

        # --- DB ---
        self.DATABASE_URL = env.str("DATABASE_URL")

        # --- BASE_DIR ---
        self.BASE_DIR = Path(__file__).parent
        self.FILES_DIR = self.BASE_DIR / 'files'

        # --- LLM ---
        self.OLLAMA_URL = "http://localhost:11434/api/generate"
        self.MODEL = "second_constantine/t-lite-it-2.1:8b"

settings = Settings()