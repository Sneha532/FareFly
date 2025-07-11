from pydantic_settings import BaseSettings
from typing import Optional, List
import secrets
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database settings
    DATABASE_URL: str
    
    # Amadeus API settings
    AMADEUS_CLIENT_ID: str
    AMADEUS_CLIENT_SECRET: str
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Additional API keys
    GEMINI_API_KEY: Optional[str] = None
    UNSPLASH_ACCESS_KEY: str = ""
    UNSPLASH_SECRET_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()