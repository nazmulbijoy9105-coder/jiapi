"""
JIAPI - Legislation Models
All tax laws, acts, rules, SROs, circulars
"""
from sqlalchemy import Column, String, Text, Date, DateTime, Boolean, ForeignKey, Integer, Enum, JSON, Index
from sqlalchemy.orm import relationship
from app.models.base import BaseModel, Base
import enum


class EraEnum(str, enum.Enum):
    PRE_2023 = "pre2023"
    POST_2023 = "post2023"


class LegislationType(str, enum.Enum):
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


class StatusEnum(str, enum.Enum):
    ACTIVE = "active"
    AMENDED = "amended"
    REPEALED = "repealed"
    SUPERSEDED = "superseded"
    DRAFT = "draft"


class Legislation(BaseModel):
    __tablename__ = "legislations"

    era = Column(Enum(EraEnum), nullable=False, index=True)
    legislation_type = Column(Enum(LegislationType), nullable=False, index=True)

    # Identification
    title_en = Column(String(500), nullable=False)
    title_bn = Column(String(500), nullable=True)
    short_title = Column(String(100), nullable=True)
    act_number = Column(String(50), nullable=True)
    year = Column(Integer, nullable=True)

    # Source & Authority
    authority = Column(String(100), nullable=True)  # NBR, Parliament, Ministry
    gazette_reference = Column(String(200), nullable=True)
    sro_number = Column(String(50), nullable=True)

    # Dates
    enactment_date = Column(Date, nullable=True)
    effective_date = Column(Date, nullable=False)
    repeal_date = Column(Date, nullable=True)

    # Status
    status = Column(Enum(StatusEnum), default=StatusEnum.ACTIVE)
    version_number = Column(Integer, default=1)
    parent_id = Column(String(36), ForeignKey("legislations.id"), nullable=True)

    # Content
    preamble = Column(Text, nullable=True)
    full_text = Column(Text, nullable=True)
    document_url = Column(String(500), nullable=True)
    document_hash = Column(String(64), nullable=True)

    # Metadata
    tags = Column(JSON, default=list)
    keywords = Column(JSON, default=list)
    sector = Column(String(100), nullable=True)  # banking, telecom, manufacturing, etc.

    # Search
    search_vector = Column(Text, nullable=True)

    # Relationships
    parent = relationship("Legislation", remote_side=[BaseModel.id], backref="versions")
    content_blocks = relationship("ContentBlock", back_populates="legislation", cascade="all, delete-orphan")
    amendments = relationship("Amendment", foreign_keys="Amendment.target_legislation_id", back_populates="target_legislation")

    __table_args__ = (
        Index("idx_legislation_era_type", "era", "legislation_type"),
        Index("idx_legislation_effective", "effective_date"),
        Index("idx_legislation_status", "status"),
    )


class ContentBlock(BaseModel):
    __tablename__ = "content_blocks"

    legislation_id = Column(String(36), ForeignKey("legislations.id"), nullable=False)

    # Hierarchy
    block_type = Column(String(50), nullable=False)  # section, subsection, clause, schedule, table, part, chapter
    numbering = Column(String(100), nullable=False)  # "30", "30(1)", "30(1)(a)", "First Schedule"
    heading = Column(String(500), nullable=True)

    # Content
    text_original = Column(Text, nullable=False)
    text_current = Column(Text, nullable=False)

    # Position
    order_index = Column(Integer, nullable=False)
    parent_block_id = Column(String(36), ForeignKey("content_blocks.id"), nullable=True)

    # Temporal
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date, nullable=True)

    # Search
    search_vector = Column(Text, nullable=True)

    # Relationships
    legislation = relationship("Legislation", back_populates="content_blocks")
    parent_block = relationship("ContentBlock", remote_side=[BaseModel.id], backref="children")
    amendment_history = relationship("Amendment", foreign_keys="Amendment.target_block_id", back_populates="target_block")

    __table_args__ = (
        Index("idx_content_block_legislation", "legislation_id"),
        Index("idx_content_block_numbering", "numbering"),
        Index("idx_content_block_type", "block_type"),
    )


class Amendment(BaseModel):
    __tablename__ = "amendments"

    # Source
    source_legislation_id = Column(String(36), ForeignKey("legislations.id"), nullable=False)
    source_section_ref = Column(String(100), nullable=True)  # "Section 12 of Finance Act 2024"

    # Target
    target_legislation_id = Column(String(36), ForeignKey("legislations.id"), nullable=False)
    target_block_id = Column(String(36), ForeignKey("content_blocks.id"), nullable=True)

    # Change details
    change_type = Column(String(50), nullable=False)  # insert, delete, substitute, renumber, repeal
    old_text = Column(Text, nullable=True)
    new_text = Column(Text, nullable=True)

    # Dates
    effective_date = Column(Date, nullable=False)
    notification_date = Column(Date, nullable=True)
    gazette_date = Column(Date, nullable=True)

    # Status
    is_applied = Column(Boolean, default=False)
    applied_at = Column(DateTime, nullable=True)
    applied_by = Column(String(100), nullable=True)

    # Metadata
    description = Column(Text, nullable=True)
    impact_assessment = Column(Text, nullable=True)

    # Relationships
    source_legislation = relationship("Legislation", foreign_keys=[source_legislation_id])
    target_legislation = relationship("Legislation", foreign_keys=[target_legislation_id], back_populates="amendments")
    target_block = relationship("ContentBlock", foreign_keys=[target_block_id], back_populates="amendment_history")

    __table_args__ = (
        Index("idx_amendment_source", "source_legislation_id"),
        Index("idx_amendment_target", "target_legislation_id"),
        Index("idx_amendment_effective", "effective_date"),
    )
