from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_PASSWORD: str
    DB_USER: str

settings = Settings()

def __getattr__(name: str):
    return getattr(settings, name)
