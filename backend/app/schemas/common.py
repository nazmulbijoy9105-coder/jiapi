"""
JIAPI - Common Schemas (Pagination, Search, Diff, Point-in-Time)
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import date, datetime


class PaginatedResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool
    data: List[Any]


class SearchQuery(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    era: Optional[str] = None  # post2023, pre2023, caselaw
    legislation_type: Optional[str] = None
    court_level: Optional[str] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    sector: Optional[str] = None
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    highlight: bool = True


class DiffRequest(BaseModel):
    legislation_id: str
    block_numbering: Optional[str] = None
    from_date: date
    to_date: date


class PointInTimeRequest(BaseModel):
    legislation_id: str
    block_numbering: Optional[str] = None
    as_of_date: date


class DiffResponse(BaseModel):
    legislation_id: str
    legislation_title: str
    block_numbering: Optional[str]
    from_date: date
    to_date: date
    old_text: Optional[str]
    new_text: Optional[str]
    amendments: List[Dict[str, Any]]
    has_changes: bool


class PointInTimeResponse(BaseModel):
    legislation_id: str
    legislation_title: str
    block_numbering: Optional[str]
    as_of_date: date
    text: str
    status: str
    applicable_amendments: List[Dict[str, Any]]
    next_change_date: Optional[date]


class AmendmentFeedItem(BaseModel):
    id: str
    title: str
    legislation_type: str
    change_type: str
    effective_date: date
    description: str
    source: str
    created_at: datetime


class WebhookPayload(BaseModel):
    event: str
    timestamp: datetime
    data: Dict[str, Any]
    signature: Optional[str]


class HealthCheck(BaseModel):
    status: str
    version: str
    database: str
    redis: str
    elasticsearch: str
    timestamp: datetime
