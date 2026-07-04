import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    API_KEY: str = os.getenv("API_KEY", "")
    CORS_ORIGINS: list[str] = [
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "").split(",")
        if origin.strip()
    ]
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")


settings = Settings()
