import os
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()  # Load .env before settings

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    groq_api_key: str = Field(..., env="GROQ_API_KEY")
    openweather_api_key: str = Field(None, env="OPENWEATHER_API_KEY")
    google_maps_api_key: str = Field(None, env="GOOGLE_MAPS_API_KEY")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

def validate_environment() -> None:
    """Ensure required environment variables are set"""
    required = ["GROQ_API_KEY"]
    for var in required:
        if not os.getenv(var):
            raise EnvironmentError(f"Missing required environment variable: {var}")
