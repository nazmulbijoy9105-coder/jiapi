"""
JIAPI - Circular & General Order Schemas
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class CircularBase(BaseModel):
    circular_number: str
    circular_date: datetime
    circular_type: str
    title_en: str
    title_bn: Optional[str] = None
    issuing_wing: Optional[str] = None
    issuing_officer: Optional[str] = None
    subject: Optional[str] = None
    full_text: Optional[str] = None
    summary: Optional[str] = None
    applicable_from: Optional[datetime] = None
    applicable_to: Optional[datetime] = None
    tax_year: Optional[str] = None
    assessment_year: Optional[str] = None
    sector_tags: Optional[List[str]] = None
    taxpayer_category: Optional[List[str]] = None
    status: str = "active"
    source_url: Optional[str] = None
    related_legislation_ids: Optional[List[UUID]] = None


class CircularCreate(CircularBase):
    pass


class CircularUpdate(BaseModel):
    status: Optional[str] = None
    summary: Optional[str] = None
    applicable_to: Optional[datetime] = None


class CircularResponse(CircularBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class GeneralOrderBase(BaseModel):
    go_number: str
    go_date: datetime
    title_en: str
    title_bn: Optional[str] = None
    issuing_authority: Optional[str] = None
    subject: Optional[str] = None
    full_text: Optional[str] = None
    applicable_from: Optional[datetime] = None
    tax_year: Optional[str] = None
    status: str = "active"
    source_url: Optional[str] = None


class GeneralOrderResponse(GeneralOrderBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CircularFilter(BaseModel):
    circular_type: Optional[str] = None
    status: Optional[str] = None
    tax_year: Optional[str] = None
    sector_tags: Optional[List[str]] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    search_query: Optional[str] = None
