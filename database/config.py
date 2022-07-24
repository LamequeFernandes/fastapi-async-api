from pydantic import BaseSettings

from sqlalchemy.orm import declarative_base


class Settings(BaseSettings): 

    DB_URL: str = 'postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_teste'
    Base = declarative_base()

    class Config:
        case_sensitive = True

settings = Settings()