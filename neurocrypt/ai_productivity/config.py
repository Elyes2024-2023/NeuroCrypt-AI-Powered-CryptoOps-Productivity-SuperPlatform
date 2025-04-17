from pydantic import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "NeuroCrypt AI Productivity"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./neurocrypt.db")
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # Redis (for caching)
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # CORS
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    # AI Model Settings
    DEFAULT_AI_MODEL: str = "gpt-4"
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    MAX_TOKENS: int = 2000
    TEMPERATURE: float = 0.7
    
    # Feature Flags
    ENABLE_AI_SUGGESTIONS: bool = True
    ENABLE_JOURNAL_ANALYSIS: bool = True
    ENABLE_GOAL_TRACKING: bool = True
    
    # Cache Settings
    CACHE_TTL: int = 3600  # 1 hour
    
    class Config:
        case_sensitive = True

settings = Settings() 