"""
JIAPI - Amendment Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import date
from enum import Enum


class ChangeType(str, Enum):
    INSERT = "insert"
    DELETE = "delete"
    SUBSTITUTE = "substitute"
    RENUMBER = "renumber"
    REPEAL = "repeal"


class AmendmentBase(BaseModel):
    change_type: ChangeType
    effective_date: date
    old_text: Optional[str] = None
    new_text: Optional[str] = None
    old_number: Optional[str] = None
    new_number: Optional[str] = None
    amendment_summary: Optional[str] = None
    amendment_summary_bn: Optional[str] = None
    reasoning: Optional[str] = None
    tags: List[str] = []


class AmendmentCreate(AmendmentBase):
    source_legislation_id: str
    source_section_id: Optional[str] = None
    target_legislation_id: str
    target_section_id: Optional[str] = None
    notification_date: Optional[date] = None
    published_in_gazette: Optional[str] = None


class AmendmentUpdate(BaseModel):
    is_applied: Optional[str] = None
    applied_at: Optional[date] = None
    amendment_summary: Optional[str] = None


class AmendmentResponse(AmendmentBase):
    id: str
    source_legislation_id: str
    target_legislation_id: str
    target_section_id: Optional[str] = None
    is_applied: str
    applied_at: Optional[date] = None
    applied_by: Optional[str] = None
    notification_date: Optional[date] = None
    created_at: str

    class Config:
        from_attributes = True


class AmendmentFeedItem(BaseModel):
    id: str
    change_type: ChangeType
    target_legislation_title: str
    target_section_number: Optional[str] = None
    effective_date: date
    amendment_summary: Optional[str] = None
    created_at: str


class AmendmentFeedResponse(BaseModel):
    total: int
    items: List[AmendmentFeedItem]
    last_updated: str
