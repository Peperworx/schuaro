from pydantic import BaseSettings


class Settings(BaseSettings):
    secret: str
    mongo_host: str
    mongo_port: int
    db_name: str

    class Config:
        env_file = ".env"

settings = Settings()

