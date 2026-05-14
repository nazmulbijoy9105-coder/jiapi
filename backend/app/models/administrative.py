"""
JIAPI - Administrative Guidance Models
Tax Compliance Manual, Transfer Pricing Regulations
"""
from sqlalchemy import Column, String, Text, DateTime, Date, Boolean, ForeignKey, Integer, JSON
from sqlalchemy.orm import relationship

from .base import BaseModel


class ComplianceManual(BaseModel):
    __tablename__ = "compliance_manuals"

    legislation_id = Column(String(36), ForeignKey("legislations.id"), nullable=False)

    manual_version = Column(String(50), nullable=False)
    effective_date = Column(Date, nullable=False)

    # Content
    chapter_number = Column(Integer, nullable=False)
    chapter_title = Column(String(300), nullable=False)
    section_title = Column(String(300), nullable=True)

    content = Column(Text, nullable=False)
    procedures = Column(JSON, default=list)
    forms_required = Column(JSON, default=list)

    # Applicability
    applicable_to = Column(String(200), nullable=True)  # all_taxpayers, corporate, individual, specific_sector
    compliance_deadline = Column(String(100), nullable=True)
    penalty_for_non_compliance = Column(Text, nullable=True)

    # NBR reference
    nbr_order_reference = Column(String(200), nullable=True)

    def __repr__(self):
        return f"<ComplianceManual v{self.manual_version} Ch.{self.chapter_number}>"


class TPRegulation(BaseModel):
    __tablename__ = "tp_regulations"

    legislation_id = Column(String(36), ForeignKey("legislations.id"), nullable=False)

    regulation_number = Column(String(50), nullable=False)
    chapter_reference = Column(String(100), nullable=False)  # ITA 2023 Chapter reference

    # Content
    title = Column(String(300), nullable=False)
    applicability_threshold = Column(Float, nullable=True)  # e.g., BDT 30 crore for TP documentation

    documentation_requirements = Column(JSON, default=list)
    methods_allowed = Column(JSON, default=list)  # CUP, RPM, CP, TNMM, PSM

    safe_harbor_provisions = Column(Text, nullable=True)
    penalty_provisions = Column(Text, nullable=True)

    # International alignment
    oecd_alignment = Column(String(50), nullable=True)  # full, partial, none
    beps_action_reference = Column(String(50), nullable=True)

    def __repr__(self):
        return f"<TPRegulation {self.regulation_number}>"
