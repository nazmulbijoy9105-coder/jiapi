"""
JIAPI - Complete Database Models
Bangladesh Tax Law Database - All Entity Types
"""
from sqlalchemy import (
    Column, String, Text, DateTime, Date, Boolean, Integer, 
    ForeignKey, Enum, JSON, Float, Index, Table
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from .base import BaseModel, Base
import uuid
from datetime import datetime
from enum import Enum as PyEnum


# Enums
class Era(PyEnum):
    PRE_2023 = "pre2023"
    POST_2023 = "post2023"
    BOTH = "both"

class LegislationType(PyEnum):
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

class CourtLevel(PyEnum):
    APPELLATE_DIVISION = "appellate_division"
    HIGH_COURT = "high_court"
    TAT = "tat"
    DISTRICT_COURT = "district_court"

class CaseStatus(PyEnum):
    GOOD_LAW = "good_law"
    OVERRULED = "overruled"
    DISTINGUISHED = "distinguished"
    FOLLOWED = "followed"
    PENDING = "pending"

class AmendmentType(PyEnum):
    INSERT = "insert"
    DELETE = "delete"
    SUBSTITUTE = "substitute"
    RENUMBER = "renumber"
    REPEAL = "repeal"

class ContentBlockType(PyEnum):
    CHAPTER = "chapter"
    PART = "part"
    SECTION = "section"
    SUBSECTION = "subsection"
    CLAUSE = "clause"
    SUBCLAUSE = "subclause"
    PARAGRAPH = "paragraph"
    SCHEDULE = "schedule"
    TABLE = "table"
    FORM = "form"
    DEFINITION = "definition"


# Association Tables
legislation_case_association = Table(
    'legislation_case_association',
    Base.metadata,
    Column('legislation_id', String(36), ForeignKey('legislations.id')),
    Column('case_law_id', String(36), ForeignKey('case_laws.id'))
)

provision_case_association = Table(
    'provision_case_association',
    Base.metadata,
    Column('content_block_id', String(36), ForeignKey('content_blocks.id')),
    Column('case_law_id', String(36), ForeignKey('case_laws.id'))
)


class Legislation(BaseModel):
    """Primary Legislation - Acts, Rules, Finance Acts, etc."""
    __tablename__ = 'legislations'

    era = Column(Enum(Era), nullable=False, index=True)
    legislation_type = Column(Enum(LegislationType), nullable=False, index=True)

    # Identification
    title_en = Column(String(500), nullable=False)
    title_bn = Column(String(500), nullable=True)
    short_title = Column(String(200), nullable=True)
    act_number = Column(String(50), nullable=True)
    year = Column(Integer, nullable=False, index=True)

    # Authority & Status
    authority = Column(String(100), nullable=False)  # NBR, Parliament, Ministry
    gazette_number = Column(String(100), nullable=True)
    gazette_date = Column(Date, nullable=True)

    # Effective Dates
    effective_date = Column(Date, nullable=False)
    repeal_date = Column(Date, nullable=True)

    # Versioning
    version_number = Column(Integer, default=1)
    parent_id = Column(String(36), ForeignKey('legislations.id'), nullable=True)
    superseded_by_id = Column(String(36), ForeignKey('legislations.id'), nullable=True)

    # Status
    status = Column(String(20), default="active")  # active, amended, repealed, superseded
    is_repealed = Column(Boolean, default=False)

    # Content
    preamble = Column(Text, nullable=True)
    full_text = Column(Text, nullable=True)
    document_url = Column(String(500), nullable=True)
    document_format = Column(String(10), nullable=True)  # pdf, html, docx

    # Metadata
    total_sections = Column(Integer, default=0)
    total_schedules = Column(Integer, default=0)
    keywords = Column(ARRAY(String), nullable=True)
    tags = Column(JSON, nullable=True)

    # Relationships
    parent = relationship("Legislation", remote_side=[BaseModel.id], foreign_keys=[parent_id])
    content_blocks = relationship("ContentBlock", back_populates="legislation", cascade="all, delete-orphan")
    amendments = relationship("Amendment", back_populates="source_legislation")
    case_laws = relationship("CaseLaw", secondary=legislation_case_association, back_populates="legislations")

    __table_args__ = (
        Index('idx_legislation_era_type', 'era', 'legislation_type'),
        Index('idx_legislation_year', 'year'),
        Index('idx_legislation_status', 'status'),
    )


class ContentBlock(BaseModel):
    """Individual sections, subsections, clauses, etc."""
    __tablename__ = 'content_blocks'

    legislation_id = Column(String(36), ForeignKey('legislations.id'), nullable=False)
    parent_block_id = Column(String(36), ForeignKey('content_blocks.id'), nullable=True)

    # Hierarchy
    block_type = Column(Enum(ContentBlockType), nullable=False)
    numbering = Column(String(50), nullable=False)  # e.g., "30", "30(1)", "30(1)(a)"
    heading_en = Column(String(500), nullable=True)
    heading_bn = Column(String(500), nullable=True)

    # Content
    text_original = Column(Text, nullable=False)
    text_current = Column(Text, nullable=False)
    text_bengali = Column(Text, nullable=True)

    # Effective dates
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date, nullable=True)

    # Status
    is_active = Column(Boolean, default=True)
    is_repealed = Column(Boolean, default=False)

    # Ordering
    display_order = Column(Integer, default=0)
    level = Column(Integer, default=0)  # nesting level

    # Metadata
    keywords = Column(ARRAY(String), nullable=True)
    cross_references = Column(JSON, nullable=True)  # [{"section": "45", "act": "ITA 2023"}]

    # Relationships
    legislation = relationship("Legislation", back_populates="content_blocks")
    parent_block = relationship("ContentBlock", remote_side=[BaseModel.id])
    amendments = relationship("Amendment", back_populates="target_block")
    case_laws = relationship("CaseLaw", secondary=provision_case_association, back_populates="provisions_referenced")

    __table_args__ = (
        Index('idx_content_block_legislation', 'legislation_id'),
        Index('idx_content_block_numbering', 'numbering'),
        Index('idx_content_block_type', 'block_type'),
        Index('idx_content_block_effective', 'effective_from', 'effective_to'),
    )


class Amendment(BaseModel):
    """Tracks every change to legislation"""
    __tablename__ = 'amendments'

    # Source (what made the change)
    source_legislation_id = Column(String(36), ForeignKey('legislations.id'), nullable=False)
    source_section = Column(String(50), nullable=True)

    # Target (what was changed)
    target_block_id = Column(String(36), ForeignKey('content_blocks.id'), nullable=False)
    target_legislation_id = Column(String(36), ForeignKey('legislations.id'), nullable=False)

    # Change details
    change_type = Column(Enum(AmendmentType), nullable=False)
    old_text = Column(Text, nullable=True)
    new_text = Column(Text, nullable=False)
    old_numbering = Column(String(50), nullable=True)
    new_numbering = Column(String(50), nullable=True)

    # Dates
    effective_date = Column(Date, nullable=False)
    notification_date = Column(Date, nullable=True)
    gazette_date = Column(Date, nullable=True)

    # Description
    description = Column(Text, nullable=True)
    change_summary = Column(String(500), nullable=True)

    # Status
    is_applied = Column(Boolean, default=False)
    applied_at = Column(DateTime, nullable=True)
    applied_by = Column(String(100), nullable=True)

    # Relationships
    source_legislation = relationship("Legislation", foreign_keys=[source_legislation_id], back_populates="amendments")
    target_block = relationship("ContentBlock", back_populates="amendments")
    target_legislation = relationship("Legislation", foreign_keys=[target_legislation_id])

    __table_args__ = (
        Index('idx_amendment_source', 'source_legislation_id'),
        Index('idx_amendment_target', 'target_block_id'),
        Index('idx_amendment_effective', 'effective_date'),
        Index('idx_amendment_applied', 'is_applied'),
    )


class CaseLaw(BaseModel):
    """Judgments from all courts"""
    __tablename__ = 'case_laws'

    # Identification
    case_number = Column(String(100), nullable=False, index=True)
    case_title = Column(String(500), nullable=False)
    case_title_bn = Column(String(500), nullable=True)

    # Court
    court_level = Column(Enum(CourtLevel), nullable=False, index=True)
    bench = Column(String(100), nullable=True)  # Bench #1, Dhaka
    tribunal_bench = Column(String(100), nullable=True)

    # Dates
    judgment_date = Column(Date, nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    filing_date = Column(Date, nullable=True)

    # Parties
    appellant = Column(String(500), nullable=True)
    respondent = Column(String(500), nullable=True)
    assessee_name = Column(String(300), nullable=True)
    dct_name = Column(String(300), nullable=True)

    # Content
    headnotes = Column(Text, nullable=True)
    headnotes_bn = Column(Text, nullable=True)
    full_text = Column(Text, nullable=True)
    judgment_summary = Column(Text, nullable=True)

    # Status
    status = Column(Enum(CaseStatus), default=CaseStatus.GOOD_LAW)
    overruling_case_id = Column(String(36), ForeignKey('case_laws.id'), nullable=True)

    # Tax specifics
    assessment_year = Column(String(20), nullable=True)
    income_year = Column(String(20), nullable=True)
    tax_amount_involved = Column(Float, nullable=True)

    # Cross-references
    era_referenced = Column(Enum(Era), nullable=True)
    sections_referenced = Column(ARRAY(String), nullable=True)
    provisions_referenced_text = Column(JSON, nullable=True)

    # Documents
    judgment_pdf_url = Column(String(500), nullable=True)
    document_path = Column(String(500), nullable=True)

    # Metadata
    keywords = Column(ARRAY(String), nullable=True)
    tags = Column(JSON, nullable=True)
    citation = Column(String(200), nullable=True)
    parallel_citations = Column(ARRAY(String), nullable=True)

    # Relationships
    legislations = relationship("Legislation", secondary=legislation_case_association, back_populates="case_laws")
    provisions_referenced = relationship("ContentBlock", secondary=provision_case_association, back_populates="case_laws")
    overruling_case = relationship("CaseLaw", remote_side=[BaseModel.id])

    __table_args__ = (
        Index('idx_case_law_court', 'court_level'),
        Index('idx_case_law_year', 'year'),
        Index('idx_case_law_status', 'status'),
        Index('idx_case_law_era', 'era_referenced'),
    )


class SRO(BaseModel):
    """Statutory Regulatory Orders"""
    __tablename__ = 'sros'

    era = Column(Enum(Era), nullable=False)
    sro_number = Column(String(50), nullable=False, index=True)
    sro_date = Column(Date, nullable=False)

    title_en = Column(String(500), nullable=False)
    title_bn = Column(String(500), nullable=True)

    # Authority
    issuing_authority = Column(String(100), nullable=False)  # NBR, Ministry
    wing = Column(String(100), nullable=True)  # Income Tax Wing, VAT Wing

    # Content
    description = Column(Text, nullable=True)
    full_text = Column(Text, nullable=True)

    # Scope
    applicable_sections = Column(ARRAY(String), nullable=True)
    tax_rates = Column(JSON, nullable=True)  # [{"rate": 10, "category": "contractor"}]
    exemptions = Column(JSON, nullable=True)
    sectors = Column(ARRAY(String), nullable=True)

    # Status
    effective_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)

    # Document
    document_url = Column(String(500), nullable=True)
    gazette_reference = Column(String(200), nullable=True)

    # Relationships to legislation
    related_legislation_id = Column(String(36), ForeignKey('legislations.id'), nullable=True)

    __table_args__ = (
        Index('idx_sro_era', 'era'),
        Index('idx_sro_date', 'sro_date'),
        Index('idx_sro_active', 'is_active'),
    )


class Circular(BaseModel):
    """NBR Circular Letters (প্রজ্ঞাপন)"""
    __tablename__ = 'circulars'

    era = Column(Enum(Era), nullable=False)
    circular_number = Column(String(50), nullable=False, index=True)
    circular_date = Column(Date, nullable=False)

    title_en = Column(String(500), nullable=False)
    title_bn = Column(String(500), nullable=True)

    issuing_wing = Column(String(100), nullable=False)
    issued_by = Column(String(200), nullable=True)

    # Content
    subject = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    full_text = Column(Text, nullable=True)

    # Scope
    applicable_sections = Column(ARRAY(String), nullable=True)
    applicable_assessees = Column(ARRAY(String), nullable=True)

    # Status
    effective_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)
    superseded_by = Column(String(36), ForeignKey('circulars.id'), nullable=True)

    document_url = Column(String(500), nullable=True)

    __table_args__ = (
        Index('idx_circular_era', 'era'),
        Index('idx_circular_date', 'circular_date'),
    )


class DTAA(BaseModel):
    """Double Taxation Avoidance Agreements"""
    __tablename__ = 'dtaas'

    country_name = Column(String(100), nullable=False)
    country_code = Column(String(3), nullable=False, index=True)

    # Treaty details
    treaty_name = Column(String(300), nullable=False)
    signed_date = Column(Date, nullable=True)
    effective_date = Column(Date, nullable=False)
    status = Column(String(20), default="active")  # active, terminated, renegotiated

    # Articles
    articles = Column(JSON, nullable=True)  # [{"article": 1, "title": "Persons Covered", "text": "..."}]

    # Key rates
    withholding_rates = Column(JSON, nullable=True)
    # {"dividend": 10, "interest": 10, "royalty": 10, "technical_services": 7.5}

    permanent_establishment_rules = Column(JSON, nullable=True)
    capital_gains_provisions = Column(JSON, nullable=True)

    # Methods
    relief_method = Column(String(50), nullable=True)  # exemption, credit, tax_sparing

    # Documents
    full_text = Column(Text, nullable=True)
    document_url = Column(String(500), nullable=True)
    protocol_url = Column(String(500), nullable=True)

    # Metadata
    is_comprehensive = Column(Boolean, default=True)
    is_limited = Column(Boolean, default=False)
    limitations = Column(Text, nullable=True)

    keywords = Column(ARRAY(String), nullable=True)
    tags = Column(JSON, nullable=True)

    __table_args__ = (
        Index('idx_dtaa_country', 'country_code'),
        Index('idx_dtaa_status', 'status'),
    )


class BEPSReference(BaseModel):
    """OECD BEPS Framework References"""
    __tablename__ = 'beps_references'

    action_number = Column(String(10), nullable=False)  # Action 1, Action 2, etc.
    action_title = Column(String(300), nullable=False)

    # Content
    description = Column(Text, nullable=True)
    key_principles = Column(Text, nullable=True)

    # Bangladesh relevance
    bd_relevance = Column(Text, nullable=True)
    bd_implementation_status = Column(String(50), nullable=True)  # adopted, pending, not_applicable

    # Cross-references
    related_ita2023_sections = Column(ARRAY(String), nullable=True)
    related_dtaa_provisions = Column(ARRAY(String), nullable=True)

    # Documents
    oecd_document_url = Column(String(500), nullable=True)
    nbr_circular_reference = Column(String(200), nullable=True)

    is_binding = Column(Boolean, default=False)

    __table_args__ = (
        Index('idx_beps_action', 'action_number'),
        Index('idx_beps_bd_status', 'bd_implementation_status'),
    )


class TransferPricingRegulation(BaseModel):
    """Transfer Pricing Regulations under ITA 2023"""
    __tablename__ = 'tp_regulations'

    regulation_number = Column(String(50), nullable=False)
    title = Column(String(500), nullable=False)

    # ITA 2023 Reference
    chapter = Column(String(50), nullable=True)
    sections_covered = Column(ARRAY(String), nullable=True)  # ["233", "234", "235"]

    # Content
    description = Column(Text, nullable=True)
    full_text = Column(Text, nullable=True)

    # Key provisions
    arm_length_methods = Column(JSON, nullable=True)
    documentation_requirements = Column(JSON, nullable=True)
    penalty_provisions = Column(JSON, nullable=True)

    effective_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)

    document_url = Column(String(500), nullable=True)

    __table_args__ = (
        Index('idx_tp_reg_section', 'sections_covered'),
        Index('idx_tp_reg_active', 'is_active'),
    )


class ComplianceManual(BaseModel):
    """NBR Tax Compliance Manual"""
    __tablename__ = 'compliance_manuals'

    title = Column(String(500), nullable=False)
    version = Column(String(20), nullable=False)

    # Content
    description = Column(Text, nullable=True)
    full_text = Column(Text, nullable=True)

    # Chapters
    chapters = Column(JSON, nullable=True)

    effective_date = Column(Date, nullable=False)
    is_current = Column(Boolean, default=True)

    document_url = Column(String(500), nullable=True)

    __table_args__ = (
        Index('idx_compliance_current', 'is_current'),
    )


class SearchIndex(BaseModel):
    """Search index for full-text search"""
    __tablename__ = 'search_indices'

    entity_type = Column(String(50), nullable=False)  # legislation, case_law, sro, circular
    entity_id = Column(String(36), nullable=False)

    # Searchable content
    title = Column(String(500), nullable=True)
    content = Column(Text, nullable=True)
    content_bengali = Column(Text, nullable=True)

    # Metadata for filtering
    era = Column(Enum(Era), nullable=True)
    year = Column(Integer, nullable=True)
    category = Column(String(100), nullable=True)
    tags = Column(ARRAY(String), nullable=True)

    # Search ranking
    search_vector = Column(String(50), nullable=True)

    __table_args__ = (
        Index('idx_search_entity', 'entity_type', 'entity_id'),
        Index('idx_search_era', 'era'),
        Index('idx_search_year', 'year'),
    )


class AmendmentFeed(BaseModel):
    """Feed of latest amendments for notification"""
    __tablename__ = 'amendment_feeds'

    amendment_id = Column(String(36), ForeignKey('amendments.id'), nullable=False)

    # Notification
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)

    # Target audience
    affected_sections = Column(ARRAY(String), nullable=True)
    affected_assessees = Column(ARRAY(String), nullable=True)

    # Status
    is_notified = Column(Boolean, default=False)
    notified_at = Column(DateTime, nullable=True)
    webhook_sent = Column(Boolean, default=False)
    webhook_sent_at = Column(DateTime, nullable=True)

    # Priority
    priority = Column(String(20), default="normal")  # low, normal, high, urgent

    __table_args__ = (
        Index('idx_feed_notified', 'is_notified'),
        Index('idx_feed_priority', 'priority'),
    )


class User(BaseModel):
    """API Users"""
    __tablename__ = 'users'

    email = Column(String(255), nullable=False, unique=True, index=True)
    hashed_password = Column(String(255), nullable=True)

    # Profile
    full_name = Column(String(200), nullable=True)
    organization = Column(String(200), nullable=True)
    phone = Column(String(20), nullable=True)

    # Subscription
    tier = Column(String(20), default="free")  # free, basic, professional, enterprise
    api_key = Column(String(100), nullable=True, unique=True, index=True)

    # Usage tracking
    monthly_requests = Column(Integer, default=0)
    request_limit = Column(Integer, default=100)

    # Status
    is_verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)

    # Webhooks
    webhook_url = Column(String(500), nullable=True)
    webhook_events = Column(ARRAY(String), nullable=True)

    __table_args__ = (
        Index('idx_user_tier', 'tier'),
        Index('idx_user_api_key', 'api_key'),
    )


class ApiLog(BaseModel):
    """API Request Logs"""
    __tablename__ = 'api_logs'

    user_id = Column(String(36), ForeignKey('users.id'), nullable=True)
    api_key = Column(String(100), nullable=True)

    # Request
    endpoint = Column(String(200), nullable=False)
    method = Column(String(10), nullable=False)
    query_params = Column(JSON, nullable=True)

    # Response
    status_code = Column(Integer, nullable=True)
    response_time_ms = Column(Integer, nullable=True)

    # Metadata
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)

    __table_args__ = (
        Index('idx_api_log_user', 'user_id'),
        Index('idx_api_log_endpoint', 'endpoint'),
        Index('idx_api_log_date', 'created_at'),
    )
