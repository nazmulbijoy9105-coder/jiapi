"""
JIAPI - International Tax Models
DTAAs, BEPS, Transfer Pricing
"""
from sqlalchemy import Column, String, Text, Date, Boolean, ForeignKey, Integer, Enum, JSON, Index
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel, Base


class TreatyType(str, enum.Enum):
    DTAA = "dtaa"
    TIEA = "tiea"
    MLI = "mli"
    OTHER = "other"


class DTAA(BaseModel):
    __tablename__ = "dtaas"

    # Country
    country_code = Column(String(3), nullable=False, index=True)  # ISO 3166-1 alpha-3
    country_name_en = Column(String(200), nullable=False)
    country_name_bn = Column(String(200), nullable=True)

    # Treaty details
    treaty_type = Column(Enum(TreatyType), default=TreatyType.DTAA)
    treaty_name = Column(String(300), nullable=False)
    signing_date = Column(Date, nullable=True)
    effective_date = Column(Date, nullable=False, index=True)

    # Status
    is_active = Column(Boolean, default=True)
    termination_date = Column(Date, nullable=True)

    # Content
    preamble = Column(Text, nullable=True)
    full_text = Column(Text, nullable=True)
    pdf_url = Column(String(500), nullable=True)

    # Key articles (structured)
    articles = Column(JSON, default=list)  # [{"article": 1, "title": "Personal Scope", "text": "..."}]

    # Specific provisions
    permanent_establishment_period = Column(Integer, nullable=True)  # days
    withholding_rates = Column(JSON, default=dict)  # {"dividend": 10, "interest": 10, "royalty": 10}

    # Protocols & updates
    protocols = Column(JSON, default=list)
    beps_actions_implemented = Column(JSON, default=list)

    # Source
    source_url = Column(String(500), nullable=True)

    __table_args__ = (
        Index("idx_dtaa_country", "country_code", "effective_date"),
        Index("idx_dtaa_active", "is_active", "effective_date"),
    )


class BEPSReference(BaseModel):
    __tablename__ = "beps_references"

    action_number = Column(Integer, nullable=False, index=True)  # 1-15
    action_title = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)

    # Bangladesh implementation status
    implementation_status = Column(String(50), default="not_implemented")  # implemented, partial, not_implemented
    implementation_date = Column(Date, nullable=True)

    # Relevant Bangladesh provisions
    related_legislation_ids = Column(JSON, default=list)
    related_section_ids = Column(JSON, default=list)

    # OECD content
    oecd_guidance_url = Column(String(500), nullable=True)
    oecd_summary = Column(Text, nullable=True)

    # Commentary
    local_commentary = Column(Text, nullable=True)
    practical_implications = Column(Text, nullable=True)


class TransferPricingRegulation(BaseModel):
    __tablename__ = "tp_regulations"

    # Reference to ITA 2023 Chapter
    legislation_id = Column(String(36), ForeignKey("legislations.id"), nullable=False)
    section_id = Column(String(36), ForeignKey("sections.id"), nullable=True)

    # Regulation details
    regulation_number = Column(String(50), nullable=False)
    title = Column(String(500), nullable=False)

    # Content
    full_text = Column(Text, nullable=True)
    key_requirements = Column(JSON, default=list)

    # Applicability
    threshold_amount = Column(String(100), nullable=True)  # e.g., "3 crore BDT"
    applicable_entities = Column(JSON, default=list)  # ["company", "permanent_establishment"]

    # Documentation
    documentation_requirements = Column(JSON, default=list)
    penalty_provisions = Column(Text, nullable=True)

    # Source
    nbr_circular_reference = Column(String(200), nullable=True)
    effective_date = Column(Date, nullable=False)
