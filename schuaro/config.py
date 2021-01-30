from pydantic import BaseSettings


class Settings(BaseSettings):
    secret: str
    class Config:
        env_file = ".env"

settings = Settings()

