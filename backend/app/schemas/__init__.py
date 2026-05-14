"""
JIAPI - Pydantic Schemas for API Request/Response
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from enum import Enum


# Enums
class Era(str, Enum):
    PRE_2023 = "pre2023"
    POST_2023 = "post2023"
    BOTH = "both"

class LegislationType(str, Enum):
    ACT = "act"
    RULES = "rules"
    FINANCE_ACT = "finance_act"
    SRO = "sro"
    GENERAL_ORDER = "general_order"
    CIRCULAR = "circular"
    DTAA = "dtaa"
    TP_REGULATION = "tp_regulation"
    BEPS_REFERENCE = "beps_reference"
    COMPLIANCE_MANUAL = "compliance_manual"
    VAT_ACT = "vat_act"
    CUSTOMS_ACT = "customs_act"

class CourtLevel(str, Enum):
    APPELLATE_DIVISION = "appellate_division"
    HIGH_COURT = "high_court"
    TAT = "tat"

class CaseStatus(str, Enum):
    GOOD_LAW = "good_law"
    OVERRULED = "overruled"
    DISTINGUISHED = "distinguished"
    FOLLOWED = "followed"

class AmendmentType(str, Enum):
    INSERT = "insert"
    DELETE = "delete"
    SUBSTITUTE = "substitute"
    RENUMBER = "renumber"
    REPEAL = "repeal"


# Base Schemas
class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# Legislation Schemas
class LegislationBase(BaseSchema):
    era: Era
    legislation_type: LegislationType
    title_en: str
    title_bn: Optional[str] = None
    short_title: Optional[str] = None
    act_number: Optional[str] = None
    year: int
    authority: str
    effective_date: date
    repeal_date: Optional[date] = None
    status: str = "active"
    preamble: Optional[str] = None
    keywords: Optional[List[str]] = None

class LegislationCreate(LegislationBase):
    pass

class LegislationUpdate(BaseSchema):
    title_en: Optional[str] = None
    title_bn: Optional[str] = None
    status: Optional[str] = None
    repeal_date: Optional[date] = None
    keywords: Optional[List[str]] = None

class LegislationResponse(LegislationBase):
    id: str
    created_at: datetime
    updated_at: datetime
    total_sections: int
    document_url: Optional[str] = None
    tags: Optional[Dict[str, Any]] = None


# Content Block Schemas
class ContentBlockBase(BaseSchema):
    block_type: str
    numbering: str
    heading_en: Optional[str] = None
    heading_bn: Optional[str] = None
    text_current: str
    text_bengali: Optional[str] = None
    effective_from: date
    effective_to: Optional[date] = None
    display_order: int = 0
    level: int = 0
    cross_references: Optional[List[Dict[str, Any]]] = None

class ContentBlockCreate(ContentBlockBase):
    legislation_id: str
    parent_block_id: Optional[str] = None
    text_original: str

class ContentBlockResponse(ContentBlockBase):
    id: str
    legislation_id: str
    text_original: str
    is_active: bool
    is_repealed: bool
    keywords: Optional[List[str]] = None


# Amendment Schemas
class AmendmentBase(BaseSchema):
    change_type: AmendmentType
    old_text: Optional[str] = None
    new_text: str
    old_numbering: Optional[str] = None
    new_numbering: Optional[str] = None
    effective_date: date
    description: Optional[str] = None
    change_summary: Optional[str] = None

class AmendmentCreate(AmendmentBase):
    source_legislation_id: str
    target_block_id: str
    target_legislation_id: str
    source_section: Optional[str] = None
    notification_date: Optional[date] = None
    gazette_date: Optional[date] = None

class AmendmentResponse(AmendmentBase):
    id: str
    source_legislation_id: str
    target_block_id: str
    is_applied: bool
    applied_at: Optional[datetime] = None
    created_at: datetime


# Case Law Schemas
class CaseLawBase(BaseSchema):
    case_number: str
    case_title: str
    case_title_bn: Optional[str] = None
    court_level: CourtLevel
    bench: Optional[str] = None
    judgment_date: date
    year: int
    appellant: Optional[str] = None
    respondent: Optional[str] = None
    assessee_name: Optional[str] = None
    headnotes: Optional[str] = None
    status: CaseStatus = CaseStatus.GOOD_LAW
    assessment_year: Optional[str] = None
    income_year: Optional[str] = None
    tax_amount_involved: Optional[float] = None
    era_referenced: Optional[Era] = None
    sections_referenced: Optional[List[str]] = None
    citation: Optional[str] = None

class CaseLawCreate(CaseLawBase):
    full_text: Optional[str] = None
    judgment_pdf_url: Optional[str] = None
    keywords: Optional[List[str]] = None
    tags: Optional[Dict[str, Any]] = None

class CaseLawResponse(CaseLawBase):
    id: str
    created_at: datetime
    full_text: Optional[str] = None
    provisions_referenced: Optional[List[Dict[str, Any]]] = None


# SRO Schemas
class SROBase(BaseSchema):
    era: Era
    sro_number: str
    sro_date: date
    title_en: str
    title_bn: Optional[str] = None
    issuing_authority: str
    wing: Optional[str] = None
    description: Optional[str] = None
    effective_date: date
    expiry_date: Optional[date] = None
    is_active: bool = True
    applicable_sections: Optional[List[str]] = None
    tax_rates: Optional[List[Dict[str, Any]]] = None
    sectors: Optional[List[str]] = None

class SROCreate(SROBase):
    pass

class SROResponse(SROBase):
    id: str
    created_at: datetime
    document_url: Optional[str] = None


# Circular Schemas
class CircularBase(BaseSchema):
    era: Era
    circular_number: str
    circular_date: date
    title_en: str
    title_bn: Optional[str] = None
    issuing_wing: str
    subject: Optional[str] = None
    description: Optional[str] = None
    effective_date: date
    is_active: bool = True
    applicable_sections: Optional[List[str]] = None

class CircularCreate(CircularBase):
    pass

class CircularResponse(CircularBase):
    id: str
    created_at: datetime
    document_url: Optional[str] = None


# DTAA Schemas
class DTAABase(BaseSchema):
    country_name: str
    country_code: str
    treaty_name: str
    signed_date: Optional[date] = None
    effective_date: date
    status: str = "active"
    withholding_rates: Optional[Dict[str, float]] = None
    relief_method: Optional[str] = None
    is_comprehensive: bool = True

class DTAACreate(DTAABase):
    articles: Optional[List[Dict[str, Any]]] = None
    full_text: Optional[str] = None
    document_url: Optional[str] = None

class DTAAResponse(DTAABase):
    id: str
    created_at: datetime
    articles: Optional[List[Dict[str, Any]]] = None


# Search Schemas
class SearchQuery(BaseSchema):
    q: str = Field(..., min_length=2, max_length=500)
    era: Optional[Era] = None
    legislation_type: Optional[LegislationType] = None
    year_from: Optional[int] = None
    year_to: Optional[int] = None
    court_level: Optional[CourtLevel] = None
    page: int = 1
    page_size: int = 20

class SearchResult(BaseSchema):
    entity_type: str
    entity_id: str
    title: str
    snippet: str
    highlight: Optional[str] = None
    score: float
    metadata: Dict[str, Any]

class SearchResponse(BaseSchema):
    total: int
    page: int
    page_size: int
    results: List[SearchResult]
    facets: Optional[Dict[str, Any]] = None


# Point-in-Time Query
class PointInTimeQuery(BaseSchema):
    legislation_id: str
    section_number: Optional[str] = None
    as_of_date: date

class PointInTimeResponse(BaseSchema):
    legislation: LegislationResponse
    section: Optional[ContentBlockResponse] = None
    text_as_of_date: str
    amendments_applied: List[AmendmentResponse]
    next_amendment: Optional[AmendmentResponse] = None


# Diff Query
class DiffQuery(BaseSchema):
    legislation_id: str
    section_number: str
    from_date: date
    to_date: date

class DiffResponse(BaseSchema):
    legislation_id: str
    section_number: str
    from_date: date
    to_date: date
    old_text: str
    new_text: str
    changes: List[AmendmentResponse]
    diff_html: str


# User Schemas
class UserBase(BaseSchema):
    email: str
    full_name: Optional[str] = None
    organization: Optional[str] = None
    tier: str = "free"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: str
    api_key: Optional[str] = None
    monthly_requests: int
    request_limit: int
    is_verified: bool
    created_at: datetime

class UserLogin(BaseSchema):
    email: str
    password: str

class TokenResponse(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


# Amendment Feed
class AmendmentFeedItem(BaseSchema):
    id: str
    title: str
    description: Optional[str] = None
    affected_sections: Optional[List[str]] = None
    priority: str
    effective_date: date
    created_at: datetime


# Error Response
class ErrorResponse(BaseSchema):
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None
