from pydantic import BaseSettings

from sqlalchemy.orm import declarative_base


class Settings(BaseSettings): 

    DB_URL: str = 'postgresql+asyncpg://postgres:postgres@postgres_economizei:5432/economizei'
    Base = declarative_base()

    JWT_SECRET: str = '6edac97349eb5c3638bd4fb2b69b81f4908e94564d5b5ce8da2d7692b7c5f81c'
    ALGORITHM: str = 'HS256'

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24*7

    class Config:
        case_sensitive = True

settings: Settings = Settings()