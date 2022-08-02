from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = 'postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_teste'

    class Config:
        case_sensitive = True


settings: Settings = Settings()
