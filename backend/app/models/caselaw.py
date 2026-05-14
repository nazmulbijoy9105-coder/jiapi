"""
JIAPI - Case Law Models
Appellate Division, High Court Division, Tax Appellate Tribunal
"""
from sqlalchemy import Column, String, Text, Date, DateTime, Boolean, ForeignKey, Integer, Enum, JSON, Index
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel, Base


class CourtLevel(str, enum.Enum):
    APPELLATE_DIVISION = "appellate_division"
    HIGH_COURT_DIVISION = "high_court_division"
    TAX_APPELLATE_TRIBUNAL = "tax_appellate_tribunal"
    DISTRICT_COURT = "district_court"


class CaseStatus(str, enum.Enum):
    GOOD_LAW = "good_law"
    OVERRULED = "overruled"
    DISTINGUISHED = "distinguished"
    FOLLOWED = "followed"
    EXPLAINED = "explained"
    DOUBTED = "doubted"
    PENDING_APPEAL = "pending_appeal"


class CaseLaw(BaseModel):
    __tablename__ = "case_laws"

    # Identification
    case_number = Column(String(100), nullable=False, index=True)
    case_year = Column(Integer, nullable=False, index=True)
    court_level = Column(Enum(CourtLevel), nullable=False, index=True)

    # Parties
    petitioner = Column(String(500), nullable=True)
    respondent = Column(String(500), nullable=True)

    # Dates
    judgment_date = Column(Date, nullable=False, index=True)
    filing_date = Column(Date, nullable=True)

    # Content
    headnotes = Column(Text, nullable=True)
    headnotes_bn = Column(Text, nullable=True)
    full_text = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)

    # Citation
    citation_primary = Column(String(200), nullable=True, index=True)
    citation_secondary = Column(String(200), nullable=True)
    citation_parallel = Column(JSON, default=list)

    # Status
    status = Column(Enum(CaseStatus), default=CaseStatus.GOOD_LAW, index=True)
    overruling_case_id = Column(String(36), ForeignKey("case_laws.id"), nullable=True)

    # Tax specifics
    assessment_years = Column(JSON, default=list)
    tax_amount_involved = Column(String(100), nullable=True)

    # Source
    source_url = Column(String(500), nullable=True)
    pdf_url = Column(String(500), nullable=True)
    bdlaw_reference = Column(String(200), nullable=True)

    # Metadata
    judges = Column(JSON, default=list)
    bench_size = Column(Integer, nullable=True)
    keywords = Column(JSON, default=list)
    principles_established = Column(JSON, default=list)

    # Relationships
    provisions_referenced = relationship("CaseLawProvision", back_populates="case_law", cascade="all, delete-orphan")
    overruling_case = relationship("CaseLaw", remote_side="CaseLaw.id")

    __table_args__ = (
        Index("idx_caselaw_court_year", "court_level", "case_year"),
        Index("idx_caselaw_judgment", "judgment_date", "court_level"),
        Index("idx_caselaw_citation", "citation_primary"),
        Index("idx_caselaw_status", "status", "court_level"),
    )


class CaseLawProvision(BaseModel):
    __tablename__ = "case_law_provisions"

    case_law_id = Column(String(36), ForeignKey("case_laws.id"), nullable=False, index=True)
    section_id = Column(String(36), ForeignKey("sections.id"), nullable=False, index=True)

    # How the provision was treated
    treatment = Column(String(50), nullable=False)  # interpreted, applied, distinguished, overruled
    context_text = Column(Text, nullable=True)  # Relevant excerpt from judgment

    # Relationships
    case_law = relationship("CaseLaw", back_populates="provisions_referenced")
    section = relationship("Section", back_populates="case_law_references")

    __table_args__ = (
        Index("idx_clp_case_section", "case_law_id", "section_id"),
    )
