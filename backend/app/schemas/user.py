"""
JIAPI - User Schemas
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import date, datetime


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    organization: Optional[str] = None
    phone: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    organization: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None


class UserResponse(UserBase):
    id: str
    role: str
    is_verified: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


# ==================== API KEY ====================

class APIKeyBase(BaseModel):
    name: Optional[str] = None
    rate_limit_per_minute: int = 60
    daily_quota: int = 1000
    allowed_endpoints: Optional[List[str]] = None
    allowed_eras: Optional[List[str]] = None
    expires_at: Optional[datetime] = None


class APIKeyCreate(APIKeyBase):
    pass


class APIKeyResponse(APIKeyBase):
    id: str
    key_prefix: str
    daily_usage: int
    last_used_at: Optional[datetime] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class APIKeyFullResponse(APIKeyResponse):
    """Includes the actual key - only shown once on creation"""
    api_key: str


class APIKeyUsage(BaseModel):
    key_id: str
    name: Optional[str]
    daily_usage: int
    daily_quota: int
    remaining: int
    last_used_at: Optional[datetime]


# ==================== SUBSCRIPTION ====================

class SubscriptionBase(BaseModel):
    tier: str
    price_bdt: Optional[float] = None
    billing_cycle: Optional[str] = None
    features: Optional[Dict[str, Any]] = None
    max_requests_per_day: int = 1000
    max_webhooks: int = 0
    started_at: datetime
    expires_at: datetime


class SubscriptionCreate(SubscriptionBase):
    user_id: str


class SubscriptionResponse(SubscriptionBase):
    id: str
    user_id: str
    cancelled_at: Optional[datetime] = None
    payment_status: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class SubscriptionTierInfo(BaseModel):
    tier: str
    name: str
    price_bdt_monthly: float
    price_bdt_annual: float
    features: List[str]
    max_requests_per_day: int
    max_webhooks: int
    includes_history: bool
    includes_diff: bool
    includes_webhooks: bool


# ==================== WEBHOOK ====================

class WebhookBase(BaseModel):
    url: str
    secret: Optional[str] = None
    events: List[str]
    filter_eras: Optional[List[str]] = None
    filter_sections: Optional[List[str]] = None
    filter_categories: Optional[List[str]] = None


class WebhookCreate(WebhookBase):
    pass


class WebhookUpdate(BaseModel):
    url: Optional[str] = None
    secret: Optional[str] = None
    events: Optional[List[str]] = None
    filter_eras: Optional[List[str]] = None
    filter_sections: Optional[List[str]] = None
    filter_categories: Optional[List[str]] = None
    is_active: Optional[bool] = None


class WebhookResponse(WebhookBase):
    id: str
    user_id: str
    is_active: bool
    last_delivered_at: Optional[datetime] = None
    last_error: Optional[str] = None
    delivery_count: int
    failure_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class WebhookDeliveryLog(BaseModel):
    webhook_id: str
    event_type: str
    payload: Dict[str, Any]
    response_status: Optional[int] = None
    response_body: Optional[str] = None
    delivered_at: Optional[datetime] = None
    error_message: Optional[str] = None
    retry_count: int = 0
