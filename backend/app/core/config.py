"""
JIAPI - Core Configuration (Production/Vercel Ready)
Bangladesh Tax Law Database API
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List, Optional


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "JIAPI - Justice & Income API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # API
    API_V1_STR: str = "/api/v1"
    API_POST2023_STR: str = "/api/v1/post2023"
    API_PRE2023_STR: str = "/api/v1/pre2023"
    API_CASELAW_STR: str = "/api/v1/caselaw"

    # Security
    SECRET_KEY: str = "jiapi-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS - Vercel production domains
    BACKEND_CORS_ORIGINS: List[str] = [
        "https://jiapi.vercel.app",
        "https://*.vercel.app",
        "https://jiapi-*.vercel.app",
    ]

    # Database - Use environment variable or fallback to SQLite for Vercel serverless
    DATABASE_URL: str = "sqlite+aiosqlite:///./jiapi.db"
    DATABASE_URL_SYNC: str = "sqlite:///./jiapi.db"

    # Redis - Optional (can use Upstash on Vercel)
    REDIS_URL: Optional[str] = None
    REDIS_CACHE_TTL: int = 3600

    # Elasticsearch - Optional
    ELASTICSEARCH_URL: Optional[str] = None
    ELASTICSEARCH_INDEX_PREFIX: str = "jiapi"

    # File Storage
    UPLOAD_DIR: str = "/tmp/uploads"
    MAX_UPLOAD_SIZE: int = 52428800

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_BURST: int = 10

    # Search
    SEARCH_HIGHLIGHT_FRAGMENT_SIZE: int = 150
    SEARCH_MAX_RESULTS: int = 1000

    # Amendment Engine
    AMENDMENT_AUTO_APPLY: bool = True
    AMENDMENT_NOTIFICATION_WEBHOOK: Optional[str] = None

    # External Sources
    NBR_GAZETTE_URL: str = "https://nbr.gov.bd"
    BDLAWS_URL: str = "http://bdlaws.minlaw.gov.bd"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
