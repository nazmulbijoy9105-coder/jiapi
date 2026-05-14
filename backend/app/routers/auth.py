"""
JIAPI - Authentication Router
User registration, login, API keys
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from datetime import timedelta
from app.schemas import UserCreate, UserResponse, UserLogin, TokenResponse
from app.core.security import (
    verify_password, get_password_hash, 
    create_access_token, create_refresh_token, get_current_user
)

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    """
    Register new user account.

    Free tier includes 100 requests/day.
    """
    return {
        "id": "user-001",
        "email": user.email,
        "full_name": user.full_name,
        "organization": user.organization,
        "tier": "free",
        "api_key": "jiapi_free_abc123xyz",
        "monthly_requests": 0,
        "request_limit": 100,
        "is_verified": False,
        "created_at": "2024-01-01T00:00:00"
    }


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """Login and get JWT tokens"""
    access_token = create_access_token({"sub": credentials.email, "tier": "free"})
    refresh_token = create_refresh_token({"sub": credentials.email})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 86400
    }


@router.post("/refresh")
async def refresh_token(refresh_token: str):
    """Refresh access token"""
    return {"access_token": "new_token", "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current user profile"""
    return {
        "id": "user-001",
        "email": current_user.get("sub", "user@example.com"),
        "tier": current_user.get("tier", "free"),
        "monthly_requests": 0,
        "request_limit": 100,
        "is_verified": True,
        "created_at": "2024-01-01T00:00:00"
    }
