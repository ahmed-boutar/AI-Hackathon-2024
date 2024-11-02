# app/core/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Music Transcription API"
    BACKEND_CORS_ORIGINS: list = ["*"]  # In production, replace with actual origins
    UPLOAD_DIR: str = "temp_uploads"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()