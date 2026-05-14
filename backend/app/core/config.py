from pydantic_settings import BaseSettings
from pydantic import ConfigDict
import os

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="ignore")
    
    APP_NAME: str = "JIAPI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    
    DATABASE_URL: str = "sqlite+aiosqlite:///./jiapi.db"
    DATABASE_URL_SYNC: str = "sqlite:///./jiapi.db"
    
    API_V1_STR: str = "/api/v1"
    API_POST2023_STR: str = "/api/v1/post2023"
    API_PRE2023_STR: str = "/api/v1/pre2023"
    API_CASELAW_STR: str = "/api/v1/caselaw"
    
    BACKEND_CORS_ORIGINS: list = ["*"]

settings = Settings()
