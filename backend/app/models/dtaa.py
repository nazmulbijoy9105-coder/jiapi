"""
JIAPI - DTAA Models
Double Taxation Avoidance Agreements
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


class DTAA(Base):
    __tablename__ = "dtaas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Country
    country_name = Column(String(200), nullable=False)
    country_code_iso2 = Column(String(2), nullable=True)
    country_code_iso3 = Column(String(3), nullable=True)

    # Treaty identification
    treaty_name = Column(String(500), nullable=False)
    treaty_number = Column(String(100), nullable=True)

    # Dates
    signed_date = Column(DateTime, nullable=True)
    effective_date = Column(DateTime, nullable=False, index=True)
    ratification_date = Column(DateTime, nullable=True)

    # Status
    status = Column(
        Enum("active", "terminated", "renegotiated", "pending", name="dtaa_status"),
        default="active",
        nullable=False
    )

    # Key provisions (structured JSON for quick access)
    withholding_rates = Column(JSON, nullable=True)
    permanent_establishment_rules = Column(JSON, nullable=True)
    article_summary = Column(JSON, nullable=True)

    # Limitation of Benefits
    lob_provisions = Column(Text, nullable=True)

    # Protocols/Amendments
    protocols = Column(JSON, nullable=True)

    # Full text
    full_text = Column(Text, nullable=True)

    # BEPS alignment
    beps_aligned = Column(Boolean, default=False)
    beps_actions_covered = Column(ARRAY(String), nullable=True)

    # MLI (Multilateral Instrument)
    mli_covered = Column(Boolean, default=False)
    mli_reservations = Column(Text, nullable=True)

    # Links
    source_url = Column(String(500), nullable=True)
    source_file = Column(String(500), nullable=True)

    # Search
    search_vector = Column(Text, nullable=True)

    # Audit
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_dtaa_country", "country_name", "status"),
        Index("idx_dtaa_effective", "effective_date", "status"),
    )
