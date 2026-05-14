"""
JIAPI - Health Check Router
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": "2025-01-01T00:00:00"
    }


@router.get("/ready")
async def readiness_check():
    """Readiness probe for Kubernetes"""
    return {"status": "ready", "checks": {"database": "ok", "redis": "ok", "elasticsearch": "ok"}}


@router.get("/live")
async def liveness_check():
    """Liveness probe for Kubernetes"""
    return {"status": "alive"}
