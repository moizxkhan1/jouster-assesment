"""
Application configuration settings
"""

from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    """Application settings"""
    
    # Server settings
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-2024-08-06"
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:admin@localhost:5432/jouster_db"
    
    # Application settings
    MAX_TEXT_LENGTH: int = 10000
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
