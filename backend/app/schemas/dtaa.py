"""
JIAPI - DTAA Schemas
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class DTAABase(BaseModel):
    country_name: str
    country_code_iso2: Optional[str] = None
    country_code_iso3: Optional[str] = None
    treaty_name: str
    treaty_number: Optional[str] = None
    signed_date: Optional[datetime] = None
    effective_date: datetime
    ratification_date: Optional[datetime] = None
    status: str = "active"
    withholding_rates: Optional[Dict[str, Any]] = None
    permanent_establishment_rules: Optional[Dict[str, Any]] = None
    article_summary: Optional[Dict[str, Any]] = None
    lob_provisions: Optional[str] = None
    protocols: Optional[List[Dict[str, Any]]] = None
    full_text: Optional[str] = None
    beps_aligned: bool = False
    beps_actions_covered: Optional[List[str]] = None
    mli_covered: bool = False
    mli_reservations: Optional[str] = None
    source_url: Optional[str] = None


class DTAACreate(DTAABase):
    pass


class DTAAUpdate(BaseModel):
    status: Optional[str] = None
    withholding_rates: Optional[Dict[str, Any]] = None
    protocols: Optional[List[Dict[str, Any]]] = None
    beps_aligned: Optional[bool] = None


class DTAAResponse(DTAABase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DTAAFilter(BaseModel):
    country_name: Optional[str] = None
    status: Optional[str] = None
    beps_aligned: Optional[bool] = None
    mli_covered: Optional[bool] = None
    search_query: Optional[str] = None
