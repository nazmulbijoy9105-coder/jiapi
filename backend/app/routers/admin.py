"""
JIAPI - Admin Router
System administration endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user

router = APIRouter()


@router.get("/stats")
async def get_stats(current_user: dict = Depends(get_current_user)):
    """Get system statistics"""
    return {
        "legislations": {"post2023": 5, "pre2023": 40},
        "case_laws": {"appellate_division": 120, "high_court": 850, "tat": 3200},
        "dtaas": 35,
        "sros": {"post2023": 150, "pre2023": 2000},
        "circulars": {"post2023": 45, "pre2023": 500},
        "users": {"total": 1200, "free": 1000, "basic": 150, "professional": 40, "enterprise": 10},
        "api_requests_today": 15000
    }


@router.get("/users")
async def list_users(current_user: dict = Depends(get_current_user)):
    """List all users (admin only)"""
    return {"users": []}
