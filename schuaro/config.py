from pydantic import BaseSettings


class Settings(BaseSettings):
    secret: str
    mongo_host: str
    mongo_port: int
    db_name: str
    authcode_clientid: str
    authcode_clientsecret: str

    class Config:
        env_file = ".env"

settings = Settings()

