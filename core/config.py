from os import getenv
from pydantic_settings import BaseSettings
from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(
    __file__
).parent.parent  # абсолютный адрес базовой директории для файла бд

DB_PATH = BASE_DIR / "db.sqlite3"

class DbSettings(BaseModel):
    url: str = f"sqlite+aiosqlite:///{DB_PATH}"  # адрес бд
    echo: bool = True


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db: DbSettings = DbSettings()
    

settings = Settings()

