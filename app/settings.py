from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    TG_BOT_KEY: str
    DEBUG: bool = False
    PUBLIC_ADDR: str
    BIND_PORT: int
    BIND_HOST: str
    POSTGRES_URL: str
    ADMIN_CHAT_ID: int

    class Config:
        env_file = ".env.local"


settings = Settings()
