"""
JIAPI - Case Law Models
Appellate Division, High Court, TAT decisions
"""
from sqlalchemy import Column, String, Text, Date, DateTime, Boolean, ForeignKey, Integer, Enum, JSON, Index
from sqlalchemy.orm import relationship
from app.models.base import BaseModel, Base
import enum


class CourtLevel(str, enum.Enum):
    APPELLATE_DIVISION = "appellate_division"
    HIGH_COURT = "high_court"
    TAT = "tat"
    SUPREME_COURT_OTHER = "supreme_court_other"


class CaseStatus(str, enum.Enum):
    GOOD_LAW = "good_law"
    OVERRULED = "overruled"
    DISTINGUISHED = "distinguished"
    FOLLOWED = "followed"
    PENDING = "pending"
    REVIEW_PENDING = "review_pending"


class CaseLaw(BaseModel):
    __tablename__ = "case_laws"

    # Identification
    case_number = Column(String(100), nullable=False, index=True)
    case_title = Column(String(500), nullable=False)
    case_title_bn = Column(String(500), nullable=True)

    # Court
    court_level = Column(Enum(CourtLevel), nullable=False, index=True)
    court_name = Column(String(200), nullable=True)
    bench = Column(String(100), nullable=True)

    # Parties
    appellant = Column(String(500), nullable=True)
    respondent = Column(String(500), nullable=True)

    # Dates
    judgment_date = Column(Date, nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    filing_date = Column(Date, nullable=True)

    # Content
    headnotes = Column(Text, nullable=True)
    headnotes_bn = Column(Text, nullable=True)
    facts = Column(Text, nullable=True)
    issues = Column(Text, nullable=True)
    holding = Column(Text, nullable=True)
    reasoning = Column(Text, nullable=True)
    decision = Column(Text, nullable=True)
    ratio_decidendi = Column(Text, nullable=True)
    obiter_dicta = Column(Text, nullable=True)
    full_text = Column(Text, nullable=True)

    # Documents
    judgment_pdf_url = Column(String(500), nullable=True)
    judgment_text_url = Column(String(500), nullable=True)

    # Status
    status = Column(Enum(CaseStatus), default=CaseStatus.GOOD_LAW)

    # Overruling
    overruling_case_id = Column(String(36), ForeignKey("case_laws.id"), nullable=True)
    overruled_date = Column(Date, nullable=True)

    # Tax specifics
    tax_year = Column(String(20), nullable=True)
    assessment_year = Column(String(20), nullable=True)
    income_amount = Column(String(100), nullable=True)
    tax_involved = Column(String(100), nullable=True)

    # Search
    search_vector = Column(Text, nullable=True)
    keywords = Column(JSON, default=list)

    # Relationships
    overruling_case = relationship("CaseLaw", remote_side=[BaseModel.id], backref="overruled_cases")
    provisions_referenced = relationship("CaseProvisionLink", back_populates="case_law", cascade="all, delete-orphan")
    cited_cases = relationship("CaseCitation", foreign_keys="CaseCitation.citing_case_id", back_populates="citing_case")
    cited_by = relationship("CaseCitation", foreign_keys="CaseCitation.cited_case_id", back_populates="cited_case")

    __table_args__ = (
        Index("idx_case_law_court_year", "court_level", "year"),
        Index("idx_case_law_judgment_date", "judgment_date"),
        Index("idx_case_law_status", "status"),
    )


class CaseProvisionLink(BaseModel):
    __tablename__ = "case_provision_links"

    case_law_id = Column(String(36), ForeignKey("case_laws.id"), nullable=False)
    legislation_id = Column(String(36), ForeignKey("legislations.id"), nullable=False)
    content_block_id = Column(String(36), ForeignKey("content_blocks.id"), nullable=True)

    # How the provision was used
    usage_type = Column(String(50), nullable=False)  # interpreted, applied, distinguished, overruled
    context_quote = Column(Text, nullable=True)

    # Relationships
    case_law = relationship("CaseLaw", back_populates="provisions_referenced")
    legislation = relationship("Legislation")
    content_block = relationship("ContentBlock")

    __table_args__ = (
        Index("idx_case_provision_case", "case_law_id"),
        Index("idx_case_provision_legislation", "legislation_id"),
    )


class CaseCitation(BaseModel):
    __tablename__ = "case_citations"

    citing_case_id = Column(String(36), ForeignKey("case_laws.id"), nullable=False)
    cited_case_id = Column(String(36), ForeignKey("case_laws.id"), nullable=False)

    citation_type = Column(String(50), nullable=False)  # followed, distinguished, overruled, referred
    context = Column(Text, nullable=True)
    paragraph_number = Column(String(50), nullable=True)

    # Relationships
    citing_case = relationship("CaseLaw", foreign_keys=[citing_case_id], back_populates="cited_cases")
    cited_case = relationship("CaseLaw", foreign_keys=[cited_case_id], back_populates="cited_by")

    __table_args__ = (
        Index("idx_citation_citing", "citing_case_id"),
        Index("idx_citation_cited", "cited_case_id"),
    )


class DTAA(BaseModel):
    __tablename__ = "dtaas"

    country_code = Column(String(2), nullable=False, unique=True)
    country_name = Column(String(100), nullable=False)
    country_name_bn = Column(String(100), nullable=True)

    # Treaty details
    treaty_date = Column(Date, nullable=True)
    effective_date = Column(Date, nullable=True)
    status = Column(String(50), default="active")

    # Content
    full_text = Column(Text, nullable=True)
    articles = Column(JSON, default=list)

    # Key provisions
    permanent_establishment_article = Column(String(50), nullable=True)
    withholding_rates = Column(JSON, default=dict)  # {"dividend": "10%", "interest": "10%", "royalty": "10%"}

    # Search
    search_vector = Column(Text, nullable=True)

    __table_args__ = (
        Index("idx_dtaa_country", "country_code"),
        Index("idx_dtaa_status", "status"),
    )
