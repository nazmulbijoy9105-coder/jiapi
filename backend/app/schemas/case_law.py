"""
JIAPI - Pydantic Schemas for Case Law
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from enum import Enum


class CourtLevel(str, Enum):
    APPELLATE_DIVISION = "appellate_division"
    HIGH_COURT = "high_court"
    TAT = "tat"
    SUPREME_COURT_OTHER = "supreme_court_other"


class CaseStatus(str, Enum):
    GOOD_LAW = "good_law"
    OVERRULED = "overruled"
    DISTINGUISHED = "distinguished"
    FOLLOWED = "followed"
    PENDING = "pending"
    REVIEW_PENDING = "review_pending"


class CaseProvisionLinkBase(BaseModel):
    legislation_id: str
    content_block_id: Optional[str] = None
    usage_type: str
    context_quote: Optional[str] = None


class CaseProvisionLinkResponse(CaseProvisionLinkBase):
    id: str
    case_law_id: str
    legislation_title: Optional[str] = None
    section_number: Optional[str] = None

    class Config:
        from_attributes = True


class CaseCitationBase(BaseModel):
    cited_case_id: str
    citation_type: str
    context: Optional[str] = None
    paragraph_number: Optional[str] = None


class CaseCitationResponse(CaseCitationBase):
    id: str
    citing_case_id: str
    cited_case_title: Optional[str] = None

    class Config:
        from_attributes = True


class CaseLawBase(BaseModel):
    case_number: str
    case_title: str
    case_title_bn: Optional[str] = None
    court_level: CourtLevel
    court_name: Optional[str] = None
    bench: Optional[str] = None
    appellant: Optional[str] = None
    respondent: Optional[str] = None
    judgment_date: date
    year: int
    filing_date: Optional[date] = None
    headnotes: Optional[str] = None
    headnotes_bn: Optional[str] = None
    facts: Optional[str] = None
    issues: Optional[str] = None
    holding: Optional[str] = None
    reasoning: Optional[str] = None
    decision: Optional[str] = None
    tax_year: Optional[str] = None
    assessment_year: Optional[str] = None
    keywords: List[str] = []


class CaseLawCreate(CaseLawBase):
    full_text: Optional[str] = None
    provisions_referenced: List[CaseProvisionLinkBase] = []


class CaseLawUpdate(BaseModel):
    case_title: Optional[str] = None
    status: Optional[CaseStatus] = None
    headnotes: Optional[str] = None
    keywords: Optional[List[str]] = None


class CaseLawResponse(CaseLawBase):
    id: str
    status: CaseStatus
    overruling_case_id: Optional[str] = None
    overruled_date: Optional[date] = None
    judgment_pdf_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    provisions_referenced: List[CaseProvisionLinkResponse] = []
    cited_cases_count: int = 0
    cited_by_count: int = 0

    class Config:
        from_attributes = True


class CaseLawListResponse(BaseModel):
    items: List[CaseLawResponse]
    total: int
    page: int
    page_size: int
    pages: int


class CitationCheckRequest(BaseModel):
    citation: str = Field(..., min_length=5, description="Case citation to verify")


class CitationCheckResponse(BaseModel):
    citation: str
    found: bool
    case_id: Optional[str] = None
    case_title: Optional[str] = None
    status: Optional[str] = None
    is_good_law: bool
    overruling_case: Optional[str] = None
    message: str


class DTAABase(BaseModel):
    country_code: str = Field(..., min_length=2, max_length=2)
    country_name: str
    country_name_bn: Optional[str] = None
    treaty_date: Optional[date] = None
    effective_date: Optional[date] = None
    status: str = "active"
    withholding_rates: Dict[str, str] = {}


class DTAAResponse(DTAABase):
    id: str
    articles: List[Dict[str, Any]] = []
    created_at: datetime

    class Config:
        from_attributes = True


class CaseLawSearchRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=500)
    court_level: Optional[CourtLevel] = None
    year: Optional[int] = None
    judgment_date_from: Optional[date] = None
    judgment_date_to: Optional[date] = None
    provisions_referenced: Optional[List[str]] = None
    status: Optional[CaseStatus] = None
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    highlight: bool = True
