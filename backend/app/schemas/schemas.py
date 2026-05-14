"""
JIAPI - Pydantic Schemas
Request/Response models for API
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.models.models import (
    Era, LegislationType, BlockType, ChangeType, CourtLevel,
    CaseStatus, LegislationStatus
)


# ============== BASE SCHEMAS ==============

class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


class PaginatedResponse(BaseSchema):
    total: int
    page: int
    page_size: int
    total_pages: int
    items: List[Any]


# ============== USER SCHEMAS ==============

class UserCreate(BaseSchema):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None
    organization: Optional[str] = None


class UserResponse(BaseSchema):
    id: UUID
    email: EmailStr
    full_name: Optional[str]
    organization: Optional[str]
    role: str
    subscription_tier: str
    created_at: datetime


class TokenResponse(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


# ============== LEGISLATION SCHEMAS ==============

class LegislationCreate(BaseSchema):
    era: Era
    legislation_type: LegislationType
    title_en: str
    title_bn: Optional[str] = None
    short_title: Optional[str] = None
    citation: Optional[str] = None
    authority: str
    status: LegislationStatus = LegislationStatus.ACTIVE
    enactment_date: Optional[datetime] = None
    effective_date: datetime
    repeal_date: Optional[datetime] = None
    gazette_notification_date: Optional[datetime] = None
    source_url: Optional[str] = None
    gazette_reference: Optional[str] = None
    tags: Optional[List[str]] = None
    sector: Optional[str] = None
    keywords: Optional[List[str]] = None


class LegislationUpdate(BaseSchema):
    title_en: Optional[str] = None
    title_bn: Optional[str] = None
    status: Optional[LegislationStatus] = None
    repeal_date: Optional[datetime] = None
    tags: Optional[List[str]] = None
    keywords: Optional[List[str]] = None


class LegislationResponse(BaseSchema):
    id: UUID
    era: Era
    legislation_type: LegislationType
    title_en: str
    title_bn: Optional[str]
    short_title: Optional[str]
    citation: Optional[str]
    authority: str
    status: LegislationStatus
    enactment_date: Optional[datetime]
    effective_date: datetime
    repeal_date: Optional[datetime]
    version_number: int
    source_url: Optional[str]
    tags: Optional[List[str]]
    sector: Optional[str]
    created_at: datetime
    updated_at: datetime


class LegislationDetailResponse(LegislationResponse):
    content_blocks: List["ContentBlockResponse"] = []
    amendments_received: List["AmendmentResponse"] = []


# ============== CONTENT BLOCK SCHEMAS ==============

class ContentBlockCreate(BaseSchema):
    block_type: BlockType
    numbering: str
    sort_order: int = 0
    parent_block_id: Optional[UUID] = None
    heading_en: Optional[str] = None
    heading_bn: Optional[str] = None
    text_original: str
    text_current: str
    effective_from: datetime
    effective_to: Optional[datetime] = None
    tags: Optional[List[str]] = None


class ContentBlockResponse(BaseSchema):
    id: UUID
    legislation_id: UUID
    block_type: BlockType
    numbering: str
    sort_order: int
    parent_block_id: Optional[UUID]
    heading_en: Optional[str]
    heading_bn: Optional[str]
    text_current: str
    effective_from: datetime
    effective_to: Optional[datetime]
    is_active: bool
    child_blocks: List["ContentBlockResponse"] = []


class ContentBlockPointInTimeRequest(BaseSchema):
    as_of: datetime


class ContentBlockDiffRequest(BaseSchema):
    from_date: datetime
    to_date: datetime


class ContentBlockDiffResponse(BaseSchema):
    block_id: UUID
    numbering: str
    old_text: str
    new_text: str
    changes: List["AmendmentResponse"]


# ============== AMENDMENT SCHEMAS ==============

class AmendmentCreate(BaseSchema):
    source_legislation_id: UUID
    target_legislation_id: UUID
    target_block_id: UUID
    change_type: ChangeType
    old_text: Optional[str] = None
    new_text: Optional[str] = None
    old_numbering: Optional[str] = None
    new_numbering: Optional[str] = None
    change_summary: Optional[str] = None
    change_reason: Optional[str] = None
    effective_date: datetime
    notification_date: Optional[datetime] = None
    gazette_date: Optional[datetime] = None


class AmendmentResponse(BaseSchema):
    id: UUID
    source_legislation_id: UUID
    target_legislation_id: UUID
    target_block_id: UUID
    change_type: ChangeType
    old_text: Optional[str]
    new_text: Optional[str]
    old_numbering: Optional[str]
    new_numbering: Optional[str]
    change_summary: Optional[str]
    effective_date: datetime
    is_applied: bool
    applied_at: Optional[datetime]
    created_at: datetime


class AmendmentApplyRequest(BaseSchema):
    amendment_ids: List[UUID]


class AmendmentApplyResponse(BaseSchema):
    applied: int
    failed: int
    details: List[Dict[str, Any]]


# ============== CASE LAW SCHEMAS ==============

class CaseLawCreate(BaseSchema):
    court_level: CourtLevel
    case_number: str
    year: int
    petitioner: str
    respondent: str
    parties_bn: Optional[str] = None
    judgment_date: datetime
    filing_date: Optional[datetime] = None
    headnotes_en: Optional[str] = None
    headnotes_bn: Optional[str] = None
    summary: Optional[str] = None
    full_text: Optional[str] = None
    citation: str
    parallel_citations: Optional[List[str]] = None
    status: CaseStatus = CaseStatus.GOOD_LAW
    era_referenced: str = "both"
    assessment_year: Optional[str] = None
    tax_amount_involved: Optional[float] = None
    issue_category: Optional[str] = None
    source_url: Optional[str] = None
    bdlaw_reference: Optional[str] = None
    provision_ids: Optional[List[UUID]] = None


class CaseLawResponse(BaseSchema):
    id: UUID
    court_level: CourtLevel
    case_number: str
    year: int
    petitioner: str
    respondent: str
    judgment_date: datetime
    headnotes_en: Optional[str]
    citation: str
    status: CaseStatus
    era_referenced: str
    issue_category: Optional[str]
    created_at: datetime


class CaseLawDetailResponse(CaseLawResponse):
    full_text: Optional[str]
    summary: Optional[str]
    provisions_referenced: List[ContentBlockResponse] = []
    parallel_citations: Optional[List[str]]
    assessment_year: Optional[str]
    tax_amount_involved: Optional[float]


class CaseLawSearchRequest(BaseSchema):
    query: str = Field(..., min_length=2)
    court_level: Optional[CourtLevel] = None
    year_from: Optional[int] = None
    year_to: Optional[int] = None
    status: Optional[CaseStatus] = None
    issue_category: Optional[str] = None
    era_referenced: Optional[str] = None


class CitationCheckRequest(BaseSchema):
    citation: str


class CitationCheckResponse(BaseSchema):
    citation: str
    found: bool
    case: Optional[CaseLawResponse] = None
    status: Optional[str] = None
    overruling_case: Optional[str] = None
    is_good_law: bool


# ============== DTAA SCHEMAS ==============

class DTAACreate(BaseSchema):
    country_name_en: str
    country_name_bn: Optional[str] = None
    country_code: str = Field(..., min_length=2, max_length=3)
    treaty_name: str
    signing_date: Optional[datetime] = None
    effective_date: datetime
    status: str = "active"
    articles: Optional[Dict[str, Any]] = None
    full_text: Optional[str] = None
    mli_applicable: bool = False
    oecd_model: Optional[str] = None
    source_url: Optional[str] = None


class DTAAResponse(BaseSchema):
    id: UUID
    country_name_en: str
    country_name_bn: Optional[str]
    country_code: str
    treaty_name: str
    effective_date: datetime
    status: str
    mli_applicable: bool
    created_at: datetime


class DTAADetailResponse(DTAAResponse):
    articles: Optional[Dict[str, Any]]
    full_text: Optional[str]
    protocols: Optional[List[Dict[str, Any]]]
    source_url: Optional[str]


# ============== SEARCH SCHEMAS ==============

class SearchRequest(BaseSchema):
    query: str = Field(..., min_length=2)
    era: Optional[Era] = None
    legislation_type: Optional[LegislationType] = None
    court_level: Optional[CourtLevel] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    tags: Optional[List[str]] = None
    sector: Optional[str] = None


class SearchResultItem(BaseSchema):
    id: UUID
    type: str  # legislation, case_law, dtaa
    title: str
    highlight: Optional[str]
    score: float
    url: str


class SearchResponse(BaseSchema):
    query: str
    total: int
    results: List[SearchResultItem]
    facets: Optional[Dict[str, Any]] = None


# ============== WEBHOOK SCHEMAS ==============

class WebhookCreate(BaseSchema):
    url: str
    events: List[str]
    secret: Optional[str] = None


class WebhookResponse(BaseSchema):
    id: UUID
    url: str
    events: List[str]
    is_active: bool
    created_at: datetime


# ============== AMENDMENT FEED SCHEMAS ==============

class AmendmentFeedItem(BaseSchema):
    id: UUID
    legislation_title: str
    legislation_type: LegislationType
    change_type: ChangeType
    change_summary: Optional[str]
    effective_date: datetime
    created_at: datetime


class AmendmentFeedResponse(BaseSchema):
    items: List[AmendmentFeedItem]
    last_updated: datetime


# ============== CROSS-REFERENCE SCHEMAS ==============

class CrossReferenceResponse(BaseSchema):
    legislation_id: UUID
    legislation_title: str
    section_number: str
    section_heading: Optional[str]
    related_legislation_id: UUID
    related_legislation_title: str
    related_section_number: str
    reference_type: str
    context: Optional[str]
