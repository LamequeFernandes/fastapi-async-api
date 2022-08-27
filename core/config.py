from pydantic import BaseSettings

from sqlalchemy.orm import declarative_base


class Settings(BaseSettings): 

    DB_URL: str = 'postgresql+asyncpg://postgres:postgres@postgres_economizei:5432/economizei'
    Base = declarative_base()

    JWT_SECRET: str = ''
    ALGORITHM: str = 'HS256'

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24*7

    class Config:
        case_sensitive = True

settings: Settings() = Settings()