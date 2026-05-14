"""
JIAPI - SQLAlchemy Models
Bangladesh Tax Law Database
"""
import uuid
from datetime import datetime, timezone
from typing import List, Optional
from enum import Enum as PyEnum

from sqlalchemy import (
    Column, String, Text, DateTime, Boolean, Integer, ForeignKey,
    Enum, JSON, Index, UniqueConstraint, Table
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base


# ============== ENUMS ==============

class Era(str, PyEnum):
    POST_2023 = "post2023"
    PRE_2023 = "pre2023"


class LegislationType(str, PyEnum):
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


class BlockType(str, PyEnum):
    SECTION = "section"
    SUBSECTION = "subsection"
    CLAUSE = "clause"
    SUBCLAUSE = "subclause"
    SCHEDULE = "schedule"
    TABLE = "table"
    DEFINITION = "definition"
    CHAPTER = "chapter"
    PART = "part"


class ChangeType(str, PyEnum):
    INSERT = "insert"
    DELETE = "delete"
    SUBSTITUTE = "substitute"
    RENUMBER = "renumber"
    REPEAL = "repeal"


class CourtLevel(str, PyEnum):
    APPELLATE_DIVISION = "appellate_division"
    HIGH_COURT = "high_court"
    TAT = "tat"


class CaseStatus(str, PyEnum):
    GOOD_LAW = "good_law"
    OVERRULED = "overruled"
    DISTINGUISHED = "distinguished"
    FOLLOWED = "followed"
    PENDING = "pending"


class LegislationStatus(str, PyEnum):
    ACTIVE = "active"
    AMENDED = "amended"
    REPEALED = "repealed"
    SUPERSEDED = "superseded"
    DRAFT = "draft"


# ============== ASSOCIATION TABLES ==============

case_law_legislation = Table(
    "case_law_legislation",
    Base.metadata,
    Column("case_law_id", UUID(as_uuid=True), ForeignKey("case_laws.id", ondelete="CASCADE"), primary_key=True),
    Column("content_block_id", UUID(as_uuid=True), ForeignKey("content_blocks.id", ondelete="CASCADE"), primary_key=True),
)


# ============== USER MODEL ==============

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(255))
    organization: Mapped[Optional[str]] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(50), default="user")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    api_key: Mapped[Optional[str]] = mapped_column(String(255), unique=True, index=True)
    subscription_tier: Mapped[str] = mapped_column(String(50), default="free")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    webhooks: Mapped[List["Webhook"]] = relationship("Webhook", back_populates="user", cascade="all, delete-orphan")


# ============== LEGISLATION MODEL ==============

class Legislation(Base):
    __tablename__ = "legislations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    era: Mapped[Era] = mapped_column(Enum(Era), nullable=False, index=True)
    legislation_type: Mapped[LegislationType] = mapped_column(Enum(LegislationType), nullable=False, index=True)

    title_en: Mapped[str] = mapped_column(Text, nullable=False)
    title_bn: Mapped[Optional[str]] = mapped_column(Text)
    short_title: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    citation: Mapped[Optional[str]] = mapped_column(String(255), index=True)

    authority: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[LegislationStatus] = mapped_column(Enum(LegislationStatus), default=LegislationStatus.ACTIVE)

    enactment_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    effective_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    repeal_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    gazette_notification_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    version_number: Mapped[int] = mapped_column(Integer, default=1)
    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("legislations.id"), nullable=True)
    supersedes_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("legislations.id"), nullable=True)

    source_url: Mapped[Optional[str]] = mapped_column(String(500))
    gazette_reference: Mapped[Optional[str]] = mapped_column(String(255))
    document_path: Mapped[Optional[str]] = mapped_column(String(500))

    tags: Mapped[Optional[list]] = mapped_column(ARRAY(String), default=list)
    sector: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    keywords: Mapped[Optional[list]] = mapped_column(ARRAY(String), default=list)
    full_text_search: Mapped[Optional[str]] = mapped_column(Text)

    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    parent: Mapped[Optional["Legislation"]] = relationship("Legislation", remote_side="Legislation.id", foreign_keys=[parent_id])
    content_blocks: Mapped[List["ContentBlock"]] = relationship(
        "ContentBlock", back_populates="legislation", cascade="all, delete-orphan", order_by="ContentBlock.sort_order"
    )
    amendments_made: Mapped[List["Amendment"]] = relationship(
        "Amendment", foreign_keys="Amendment.source_legislation_id", back_populates="source_legislation"
    )
    amendments_received: Mapped[List["Amendment"]] = relationship(
        "Amendment", foreign_keys="Amendment.target_legislation_id", back_populates="target_legislation"
    )

    __table_args__ = (
        Index("idx_leg_era_type", "era", "legislation_type"),
        Index("idx_leg_effective", "effective_date"),
        Index("idx_leg_search", "full_text_search"),
    )


# ============== CONTENT BLOCK MODEL ==============

class ContentBlock(Base):
    __tablename__ = "content_blocks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    legislation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("legislations.id", ondelete="CASCADE"), nullable=False)

    block_type: Mapped[BlockType] = mapped_column(Enum(BlockType), nullable=False, index=True)
    numbering: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    parent_block_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("content_blocks.id"), nullable=True)

    heading_en: Mapped[Optional[str]] = mapped_column(Text)
    heading_bn: Mapped[Optional[str]] = mapped_column(Text)
    text_original: Mapped[str] = mapped_column(Text, nullable=False)
    text_current: Mapped[str] = mapped_column(Text, nullable=False)

    effective_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    effective_to: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    tags: Mapped[Optional[list]] = mapped_column(ARRAY(String), default=list)
    search_vector: Mapped[Optional[str]] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    legislation: Mapped["Legislation"] = relationship("Legislation", back_populates="content_blocks")
    parent_block: Mapped[Optional["ContentBlock"]] = relationship("ContentBlock", remote_side="ContentBlock.id", back_populates="child_blocks")
    child_blocks: Mapped[List["ContentBlock"]] = relationship("ContentBlock", back_populates="parent_block")
    amendment_history: Mapped[List["Amendment"]] = relationship("Amendment", back_populates="target_block", cascade="all, delete-orphan")
    case_laws: Mapped[List["CaseLaw"]] = relationship("CaseLaw", secondary=case_law_legislation, back_populates="provisions_referenced")

    __table_args__ = (
        UniqueConstraint("legislation_id", "numbering", "effective_from", name="uq_block_leg_num_date"),
        Index("idx_block_leg_type", "legislation_id", "block_type"),
        Index("idx_block_numbering", "numbering"),
        Index("idx_block_effective", "effective_from", "effective_to"),
    )


# ============== AMENDMENT MODEL ==============

class Amendment(Base):
    __tablename__ = "amendments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    source_legislation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("legislations.id"), nullable=False)
    target_legislation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("legislations.id"), nullable=False)
    target_block_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("content_blocks.id"), nullable=False)

    change_type: Mapped[ChangeType] = mapped_column(Enum(ChangeType), nullable=False)
    old_text: Mapped[Optional[str]] = mapped_column(Text)
    new_text: Mapped[Optional[str]] = mapped_column(Text)
    old_numbering: Mapped[Optional[str]] = mapped_column(String(100))
    new_numbering: Mapped[Optional[str]] = mapped_column(String(100))

    change_summary: Mapped[Optional[str]] = mapped_column(Text)
    change_reason: Mapped[Optional[str]] = mapped_column(Text)

    effective_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    notification_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    gazette_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    is_applied: Mapped[bool] = mapped_column(Boolean, default=False)
    applied_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    applied_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    source_legislation: Mapped["Legislation"] = relationship("Legislation", foreign_keys=[source_legislation_id], back_populates="amendments_made")
    target_legislation: Mapped["Legislation"] = relationship("Legislation", foreign_keys=[target_legislation_id], back_populates="amendments_received")
    target_block: Mapped["ContentBlock"] = relationship("ContentBlock", back_populates="amendment_history")

    __table_args__ = (
        Index("idx_amend_source", "source_legislation_id"),
        Index("idx_amend_target", "target_legislation_id"),
        Index("idx_amend_effective", "effective_date"),
        Index("idx_amend_applied", "is_applied"),
    )


# ============== CASE LAW MODEL ==============

class CaseLaw(Base):
    __tablename__ = "case_laws"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    court_level: Mapped[CourtLevel] = mapped_column(Enum(CourtLevel), nullable=False, index=True)
    case_number: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    petitioner: Mapped[str] = mapped_column(Text, nullable=False)
    respondent: Mapped[str] = mapped_column(Text, nullable=False)
    parties_bn: Mapped[Optional[str]] = mapped_column(Text)

    judgment_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    filing_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    headnotes_en: Mapped[Optional[str]] = mapped_column(Text)
    headnotes_bn: Mapped[Optional[str]] = mapped_column(Text)
    summary: Mapped[Optional[str]] = mapped_column(Text)
    full_text: Mapped[Optional[str]] = mapped_column(Text)
    document_path: Mapped[Optional[str]] = mapped_column(String(500))

    citation: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    parallel_citations: Mapped[Optional[list]] = mapped_column(ARRAY(String), default=list)

    status: Mapped[CaseStatus] = mapped_column(Enum(CaseStatus), default=CaseStatus.GOOD_LAW)
    era_referenced: Mapped[str] = mapped_column(String(50), default="both")

    overruling_case_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("case_laws.id"), nullable=True)

    assessment_year: Mapped[Optional[str]] = mapped_column(String(20))
    tax_amount_involved: Mapped[Optional[float]] = mapped_column()
    issue_category: Mapped[Optional[str]] = mapped_column(String(100), index=True)

    search_vector: Mapped[Optional[str]] = mapped_column(Text)

    source_url: Mapped[Optional[str]] = mapped_column(String(500))
    bdlaw_reference: Mapped[Optional[str]] = mapped_column(String(255))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    provisions_referenced: Mapped[List["ContentBlock"]] = relationship("ContentBlock", secondary=case_law_legislation, back_populates="case_laws")
    overruling_case: Mapped[Optional["CaseLaw"]] = relationship("CaseLaw", remote_side="CaseLaw.id", foreign_keys=[overruling_case_id])

    __table_args__ = (
        Index("idx_case_court_year", "court_level", "year"),
        Index("idx_case_judgment", "judgment_date"),
        Index("idx_case_status", "status"),
        Index("idx_case_issue", "issue_category"),
    )


# ============== DTAA MODEL ==============

class DTAA(Base):
    __tablename__ = "dtaas"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    country_name_en: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    country_name_bn: Mapped[Optional[str]] = mapped_column(String(255))
    country_code: Mapped[str] = mapped_column(String(3), nullable=False, unique=True, index=True)

    treaty_name: Mapped[str] = mapped_column(Text, nullable=False)
    signing_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    effective_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="active")

    articles: Mapped[Optional[dict]] = mapped_column(JSON, default=dict)
    full_text: Mapped[Optional[str]] = mapped_column(Text)
    document_path: Mapped[Optional[str]] = mapped_column(String(500))

    protocols: Mapped[Optional[list]] = mapped_column(ARRAY(JSON), default=list)

    mli_applicable: Mapped[bool] = mapped_column(Boolean, default=False)
    oecd_model: Mapped[Optional[str]] = mapped_column(String(50))

    source_url: Mapped[Optional[str]] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_dtaa_country", "country_code"),
        Index("idx_dtaa_effective", "effective_date"),
    )


# ============== WEBHOOK MODEL ==============

class Webhook(Base):
    __tablename__ = "webhooks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))

    url: Mapped[str] = mapped_column(String(500), nullable=False)
    secret: Mapped[str] = mapped_column(String(255), nullable=False)
    events: Mapped[list] = mapped_column(ARRAY(String), default=list)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user: Mapped["User"] = relationship("User", back_populates="webhooks")


# ============== AUDIT LOG ==============

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    table_name: Mapped[str] = mapped_column(String(100), nullable=False)
    record_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    old_values: Mapped[Optional[dict]] = mapped_column(JSON)
    new_values: Mapped[Optional[dict]] = mapped_column(JSON)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    user_agent: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_audit_table_record", "table_name", "record_id"),
        Index("idx_audit_created", "created_at"),
    )
