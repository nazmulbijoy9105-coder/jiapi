"""
JIAPI - Pydantic Schemas for Legislation
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from enum import Enum


class EraEnum(str, Enum):
    PRE_2023 = "pre2023"
    POST_2023 = "post2023"


class LegislationType(str, Enum):
    ACT = "act"
    RULE = "rule"
    FINANCE_ACT = "finance_act"
    SRO = "sro"
    GO = "go"
    CIRCULAR = "circular"
    DTAA = "dtaa"
    TP_REGULATION = "tp_regulation"
    BEPS = "beps"
    COMPLIANCE_MANUAL = "compliance_manual"
    VAT_ACT = "vat_act"
    CUSTOMS_ACT = "customs_act"


class StatusEnum(str, Enum):
    ACTIVE = "active"
    AMENDED = "amended"
    REPEALED = "repealed"
    SUPERSEDED = "superseded"
    DRAFT = "draft"


class ContentBlockBase(BaseModel):
    block_type: str
    numbering: str
    heading: Optional[str] = None
    text_current: str
    text_original: Optional[str] = None
    order_index: int
    effective_from: date
    effective_to: Optional[date] = None


class ContentBlockResponse(ContentBlockBase):
    id: str
    legislation_id: str
    amendment_count: int = 0

    class Config:
        from_attributes = True


class AmendmentBase(BaseModel):
    change_type: str
    old_text: Optional[str] = None
    new_text: Optional[str] = None
    effective_date: date
    notification_date: Optional[date] = None
    description: Optional[str] = None


class AmendmentResponse(AmendmentBase):
    id: str
    source_legislation_id: str
    source_section_ref: Optional[str]
    target_legislation_id: str
    target_block_id: Optional[str]
    is_applied: bool
    applied_at: Optional[datetime]

    class Config:
        from_attributes = True


class LegislationBase(BaseModel):
    era: EraEnum
    legislation_type: LegislationType
    title_en: str
    title_bn: Optional[str] = None
    short_title: Optional[str] = None
    act_number: Optional[str] = None
    year: Optional[int] = None
    authority: Optional[str] = None
    gazette_reference: Optional[str] = None
    sro_number: Optional[str] = None
    enactment_date: Optional[date] = None
    effective_date: date
    repeal_date: Optional[date] = None
    status: StatusEnum = StatusEnum.ACTIVE
    preamble: Optional[str] = None
    tags: List[str] = []
    keywords: List[str] = []
    sector: Optional[str] = None


class LegislationCreate(LegislationBase):
    full_text: Optional[str] = None
    content_blocks: List[ContentBlockBase] = []


class LegislationUpdate(BaseModel):
    title_en: Optional[str] = None
    title_bn: Optional[str] = None
    status: Optional[StatusEnum] = None
    tags: Optional[List[str]] = None
    keywords: Optional[List[str]] = None


class LegislationResponse(LegislationBase):
    id: str
    version_number: int
    parent_id: Optional[str] = None
    document_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    content_blocks: List[ContentBlockResponse] = []
    amendment_count: int = 0

    class Config:
        from_attributes = True


class LegislationListResponse(BaseModel):
    items: List[LegislationResponse]
    total: int
    page: int
    page_size: int
    pages: int


class SectionPointInTimeRequest(BaseModel):
    legislation_id: str
    section_number: str
    as_of_date: date


class SectionPointInTimeResponse(BaseModel):
    legislation_id: str
    section_number: str
    as_of_date: date
    text: str
    amendments_applied: List[AmendmentResponse] = []
    is_current: bool


class DiffRequest(BaseModel):
    legislation_id: str
    section_number: str
    from_date: date
    to_date: date


class DiffResponse(BaseModel):
    legislation_id: str
    section_number: str
    from_date: date
    to_date: date
    old_text: str
    new_text: str
    changes: List[Dict[str, Any]] = []
    amendments: List[AmendmentResponse] = []


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=500)
    era: Optional[EraEnum] = None
    legislation_type: Optional[LegislationType] = None
    year: Optional[int] = None
    section_number: Optional[str] = None
    court_level: Optional[str] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    highlight: bool = True


class SearchResultItem(BaseModel):
    id: str
    type: str  # legislation, case_law, content_block
    title: str
    snippet: str
    highlights: List[str] = []
    score: float
    url: Optional[str] = None


class SearchResponse(BaseModel):
    query: str
    results: List[SearchResultItem]
    total: int
    page: int
    page_size: int
    took_ms: int


class AmendmentFeedItem(BaseModel):
    id: str
    source_title: str
    target_title: str
    change_type: str
    effective_date: date
    description: Optional[str]
    created_at: datetime


class AmendmentFeedResponse(BaseModel):
    items: List[AmendmentFeedItem]
    total: int
    last_updated: datetime
