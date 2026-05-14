"""
JIAPI - Case Law Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import date, datetime


class CaseLawBase(BaseModel):
    court_level: str
    case_number: str
    case_year: int
    appellant: Optional[str] = None
    respondent: Optional[str] = None
    subject_matter: Optional[str] = None
    tax_type: Optional[str] = None
    assessment_year: Optional[str] = None
    judgment_date: date
    date_of_hearing: Optional[date] = None
    headnotes: Optional[str] = None
    full_text: Optional[str] = None
    full_text_bn: Optional[str] = None
    legal_principles: Optional[List[str]] = None
    key_holdings: Optional[Dict[str, Any]] = None
    bdlaw_citation: Optional[str] = None
    bangladesh_law_chronicle_citation: Optional[str] = None
    official_pdf_url: Optional[str] = None
    bench_strength: Optional[int] = None
    judges: Optional[List[str]] = None


class CaseLawCreate(CaseLawBase):
    pass


class CaseLawUpdate(BaseModel):
    status: Optional[str] = None
    overruling_case_id: Optional[str] = None
    headnotes: Optional[str] = None
    full_text: Optional[str] = None
    key_holdings: Optional[Dict[str, Any]] = None
    legal_principles: Optional[List[str]] = None


class CaseLawResponse(CaseLawBase):
    id: str
    status: str
    overruling_case_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class CaseLawDetailResponse(CaseLawResponse):
    provision_links: List["CaseLawProvisionLinkResponse"] = []
    overruling_case: Optional["CaseLawResponse"] = None
    overruled_cases: List["CaseLawResponse"] = []
    citation_references: List["CitationNetworkResponse"] = []
    cited_by: List["CitationNetworkResponse"] = []


# ==================== PROVISION LINK ====================

class CaseLawProvisionLinkBase(BaseModel):
    case_law_id: str
    content_block_id: str
    reference_type: str
    context: Optional[str] = None


class CaseLawProvisionLinkCreate(CaseLawProvisionLinkBase):
    pass


class CaseLawProvisionLinkResponse(CaseLawProvisionLinkBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== CITATION NETWORK ====================

class CitationNetworkBase(BaseModel):
    citing_case_id: str
    cited_case_id: str
    citation_type: str
    context: Optional[str] = None
    paragraph_reference: Optional[str] = None


class CitationNetworkCreate(CitationNetworkBase):
    pass


class CitationNetworkResponse(CitationNetworkBase):
    id: str
    created_at: datetime
    citing_case: Optional[CaseLawResponse] = None
    cited_case: Optional[CaseLawResponse] = None

    class Config:
        from_attributes = True


# ==================== CITATION CHECKER ====================

class CitationCheckRequest(BaseModel):
    citation: str = Field(..., description="Case citation to verify")


class CitationCheckResponse(BaseModel):
    citation: str
    found: bool
    case_id: Optional[str] = None
    case_title: Optional[str] = None
    judgment_date: Optional[date] = None
    status: Optional[str] = None
    is_good_law: bool
    overruling_case: Optional[str] = None
    message: str


# ==================== SEARCH ====================

class CaseLawSearchFilters(BaseModel):
    court_level: Optional[List[str]] = None
    case_year_from: Optional[int] = None
    case_year_to: Optional[int] = None
    tax_type: Optional[str] = None
    status: Optional[List[str]] = None
    subject_matter: Optional[str] = None
    provisions: Optional[List[str]] = None
    judge_name: Optional[str] = None


class CaseLawSearchResult(BaseModel):
    id: str
    court_level: str
    case_number: str
    case_year: int
    appellant: Optional[str]
    respondent: Optional[str]
    subject_matter: Optional[str]
    judgment_date: date
    headnotes: Optional[str]
    status: str
    relevance_score: float
    highlights: Optional[Dict[str, List[str]]] = None
