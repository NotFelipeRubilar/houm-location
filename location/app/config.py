from pydantic import BaseSettings


class Settings(BaseSettings):
    rabbit_host: str
    rabbit_port: str
    rabbit_queue: str
    rabbit_username: str
    rabbit_password: str


settings = Settings()
