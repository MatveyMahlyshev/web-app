from os import getenv
from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(
    __file__
).parent.parent  # абсолютный адрес базовой директории для файла бд


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"  # адрес бд
    db_echo: bool = True


settings = Settings()
