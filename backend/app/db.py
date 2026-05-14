"""
JIAPI - Database Connection
Async PostgreSQL with SQLAlchemy (Serverless Optimized)
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.core.config import settings

# Async engine for FastAPI (SERVERLESS OPTIMIZED)
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=2,            # Very small for serverless
    max_overflow=0,         # No overflow
    pool_pre_ping=True,
    pool_recycle=300,       # Short recycle for serverless
)

AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

# Sync engine for migrations/background tasks
sync_engine = create_engine(
    settings.DATABASE_URL_SYNC,
    echo=settings.DEBUG,
    pool_size=2,
    max_overflow=0,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)


async def get_db() -> AsyncSession:
    """Dependency for FastAPI routes"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

def get_sync_db():
    """Sync session for background tasks"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
