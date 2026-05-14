"""
NBR Instruments Models - SROs, General Orders, Circulars
"""
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, 
    ForeignKey, Enum, ARRAY, Index
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.models.legislation import Base


class SROType(str, enum.Enum):
    RATE_CHANGE = "rate_change"
    EXEMPTION = "exemption"
    SECTOR_SPECIFIC = "sector_specific"
    PROCEDURAL = "procedural"
    ADMINISTRATIVE = "administrative"
    AMENDMENT = "amendment"
    CLARIFICATION = "clarification"
    WITHDRAWAL = "withdrawal"


class StatutoryRegulatoryOrder(Base):
    """SROs issued by NBR"""
    __tablename__ = "sros"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # SRO Identification
    sro_number = Column(String(100), nullable=False, index=True)
    sro_number_bn = Column(String(100), nullable=True)
    gazette_number = Column(String(100), nullable=True)

    # Type
    sro_type = Column(Enum(SROType), nullable=False, index=True)

    # Title
    title = Column(String(500), nullable=False)
    title_bn = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)

    # Authority
    issuing_authority = Column(String(200), nullable=False, default="NBR")
    wing = Column(String(100), nullable=True)  # Income Tax Wing, VAT Wing, etc.

    # Dates
    issue_date = Column(DateTime, nullable=False, index=True)
    effective_date = Column(DateTime, nullable=False)
    expiry_date = Column(DateTime, nullable=True)
    publication_date = Column(DateTime, nullable=True)

    # Scope
    applicable_assessment_years = Column(ARRAY(String), default=[])
    applicable_sectors = Column(ARRAY(String), default=[])
    applicable_taxpayer_categories = Column(ARRAY(String), default=[])

    # Content
    content = Column(Text, nullable=False)
    content_bn = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)

    # Documents
    document_url = Column(String(500), nullable=True)
    document_path = Column(String(500), nullable=True)
    gazette_url = Column(String(500), nullable=True)

    # Status
    status = Column(String(50), default="active", index=True)
    is_withdrawn = Column(Boolean, default=False)
    withdrawn_by_sro_id = Column(UUID(as_uuid=True), ForeignKey("sros.id"), nullable=True)

    # Legislation Links
    amends_legislation_id = Column(UUID(as_uuid=True), ForeignKey("legislations.id"), nullable=True)
    amends_section = Column(String(100), nullable=True)

    # Search
    search_vector = Column(Text, nullable=True)

    # Audit
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index('idx_sro_date_type', 'issue_date', 'sro_type'),
        Index('idx_sro_search', 'search_vector', postgresql_using='gin'),
    )


class GeneralOrder(Base):
    """General Orders issued by NBR"""
    __tablename__ = "general_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    go_number = Column(String(100), nullable=False, unique=True, index=True)
    go_number_bn = Column(String(100), nullable=True)

    title = Column(String(500), nullable=False)
    title_bn = Column(String(500), nullable=True)

    issuing_authority = Column(String(200), nullable=False, default="NBR")
    wing = Column(String(100), nullable=True)

    issue_date = Column(DateTime, nullable=False, index=True)
    effective_date = Column(DateTime, nullable=False)

    content = Column(Text, nullable=False)
    content_bn = Column(Text, nullable=True)

    applicable_scope = Column(ARRAY(String), default=[])

    document_url = Column(String(500), nullable=True)
    document_path = Column(String(500), nullable=True)

    status = Column(String(50), default="active")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class CircularLetter(Base):
    """Circular letters (প্রজ্ঞাপন) from NBR Income Tax Wing"""
    __tablename__ = "circular_letters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    circular_number = Column(String(100), nullable=False, index=True)
    circular_number_bn = Column(String(100), nullable=True)

    title = Column(String(500), nullable=False)
    title_bn = Column(String(500), nullable=True)

    issuing_authority = Column(String(200), nullable=False, default="NBR")
    wing = Column(String(100), nullable=False, default="Income Tax Wing")

    issue_date = Column(DateTime, nullable=False, index=True)
    effective_date = Column(DateTime, nullable=False)

    # Subject matter
    subject = Column(String(500), nullable=True)
    subject_bn = Column(String(500), nullable=True)

    content = Column(Text, nullable=False)
    content_bn = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)

    # References
    references_legislation = Column(ARRAY(String), default=[])
    references_sro = Column(ARRAY(String), default=[])
    references_case_law = Column(ARRAY(String), default=[])

    applicable_assessment_years = Column(ARRAY(String), default=[])
    applicable_sectors = Column(ARRAY(String), default=[])

    document_url = Column(String(500), nullable=True)
    document_path = Column(String(500), nullable=True)

    status = Column(String(50), default="active")

    search_vector = Column(Text, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index('idx_circular_search', 'search_vector', postgresql_using='gin'),
    )
