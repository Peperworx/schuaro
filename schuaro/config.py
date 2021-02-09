from pydantic import BaseSettings


class Settings(BaseSettings):
    secret: str
    mongo_connstring: str
    db_name: str
    col_prefix: str
    client_id: str
    client_secret: str
    login_client_id: str

    class Config:
        env_file = ".env"

settings = Settings()

