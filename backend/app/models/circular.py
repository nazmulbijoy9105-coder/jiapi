"""
JIAPI - Circular & General Order Models
NBR Instruments: SROs, GOs, Circular Letters (প্রজ্ঞাপন)
"""
import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, DateTime, Boolean, Integer,
    ForeignKey, Enum, JSON, Index
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from app.core.database import Base


class Circular(Base):
    __tablename__ = "circulars"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Identification
    circular_number = Column(String(100), nullable=False, index=True)
    circular_date = Column(DateTime, nullable=False, index=True)

    # Type
    circular_type = Column(
        Enum("proggapon", "office_order", "notification", 
             "instruction", "guideline", name="circular_type"),
        nullable=False
    )

    # Titles
    title_en = Column(String(500), nullable=False)
    title_bn = Column(String(500), nullable=True)

    # Issuing authority
    issuing_wing = Column(String(200), nullable=True)
    issuing_officer = Column(String(200), nullable=True)

    # Content
    subject = Column(Text, nullable=True)
    full_text = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)

    # Applicability
    applicable_from = Column(DateTime, nullable=True)
    applicable_to = Column(DateTime, nullable=True)
    tax_year = Column(String(50), nullable=True)
    assessment_year = Column(String(50), nullable=True)

    # Sector/Scope
    sector_tags = Column(ARRAY(String), nullable=True)
    taxpayer_category = Column(ARRAY(String), nullable=True)

    # Status
    status = Column(
        Enum("active", "withdrawn", "superseded", "partially_withdrawn", name="circular_status"),
        default="active",
        nullable=False
    )

    # Links
    source_url = Column(String(500), nullable=True)
    source_file = Column(String(500), nullable=True)

    # Related legislation
    related_legislation_ids = Column(ARRAY(UUID(as_uuid=True)), nullable=True)

    # Search
    search_vector = Column(Text, nullable=True)

    # Audit
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_circular_type_date", "circular_type", "circular_date"),
        Index("idx_circular_status", "status", "tax_year"),
    )


class GeneralOrder(Base):
    __tablename__ = "general_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Identification
    go_number = Column(String(100), nullable=False, index=True)
    go_date = Column(DateTime, nullable=False, index=True)

    # Titles
    title_en = Column(String(500), nullable=False)
    title_bn = Column(String(500), nullable=True)

    # Issuing authority
    issuing_authority = Column(String(200), nullable=True)

    # Content
    subject = Column(Text, nullable=True)
    full_text = Column(Text, nullable=True)

    # Applicability
    applicable_from = Column(DateTime, nullable=True)
    tax_year = Column(String(50), nullable=True)

    # Status
    status = Column(
        Enum("active", "withdrawn", "superseded", name="go_status"),
        default="active",
        nullable=False
    )

    # Links
    source_url = Column(String(500), nullable=True)
    source_file = Column(String(500), nullable=True)

    # Search
    search_vector = Column(Text, nullable=True)

    # Audit
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_go_date", "go_date", "status"),
    )
