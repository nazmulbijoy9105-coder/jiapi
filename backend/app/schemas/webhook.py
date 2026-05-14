"""
JIAPI - Webhook Schemas
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, HttpUrl
from uuid import UUID


class WebhookSubscriptionBase(BaseModel):
    endpoint_url: HttpUrl
    event_types: List[str]
    era_filter: Optional[List[str]] = None
    type_filter: Optional[List[str]] = None
    sector_filter: Optional[List[str]] = None
    section_numbers: Optional[List[str]] = None
    max_retries: int = 3
    retry_interval_seconds: int = 300


class WebhookSubscriptionCreate(WebhookSubscriptionBase):
    pass


class WebhookSubscriptionUpdate(BaseModel):
    endpoint_url: Optional[HttpUrl] = None
    event_types: Optional[List[str]] = None
    era_filter: Optional[List[str]] = None
    type_filter: Optional[List[str]] = None
    sector_filter: Optional[List[str]] = None
    section_numbers: Optional[List[str]] = None
    is_active: Optional[bool] = None


class WebhookSubscriptionResponse(WebhookSubscriptionBase):
    id: UUID
    user_id: UUID
    is_active: bool
    last_delivered_at: Optional[datetime] = None
    last_delivery_status: Optional[int] = None
    delivery_failures: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class WebhookEvent(BaseModel):
    event_id: str
    event_type: str
    timestamp: datetime
    payload: dict

    class Config:
        from_attributes = True


class WebhookDeliveryLog(BaseModel):
    event_id: str
    subscription_id: UUID
    status_code: Optional[int] = None
    response_body: Optional[str] = None
    delivery_attempt: int
    delivered_at: Optional[datetime] = None
    error_message: Optional[str] = None
