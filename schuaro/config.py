from pydantic import BaseSettings


class Settings(BaseSettings):
    secret: str
    mongo_host: str
    mongo_port: int
    db_name: str
    access_token_key: dict = {}
    refresh_token_key: dict = {}

    class Config:
        env_file = ".env"

settings = Settings()

