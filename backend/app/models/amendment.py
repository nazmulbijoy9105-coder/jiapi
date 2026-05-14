"""
JIAPI - Amendment Tracking Model
"""
from sqlalchemy import Column, String, Text, Date, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
import enum
from .base import BaseModel


class ChangeType(str, enum.Enum):
    INSERT = "insert"
    DELETE = "delete"
    SUBSTITUTE = "substitute"
    RENUMBER = "renumber"
    REPEAL = "repeal"


class Amendment(BaseModel):
    __tablename__ = "amendments"

    # Source (what made the change)
    source_legislation_id = Column(String(36), ForeignKey("legislations.id"), nullable=False)
    source_section_id = Column(String(36), ForeignKey("sections.id"), nullable=True)

    # Target (what was changed)
    target_legislation_id = Column(String(36), ForeignKey("legislations.id"), nullable=False)
    target_section_id = Column(String(36), ForeignKey("sections.id"), nullable=True)

    # Change details
    change_type = Column(Enum(ChangeType), nullable=False)
    old_text = Column(Text, nullable=True)
    new_text = Column(Text, nullable=True)
    old_number = Column(String(50), nullable=True)
    new_number = Column(String(50), nullable=True)

    # Effective dates
    effective_date = Column(Date, nullable=False)
    notification_date = Column(Date, nullable=True)
    published_in_gazette = Column(String(200), nullable=True)

    # Context
    amendment_summary = Column(Text, nullable=True)
    amendment_summary_bn = Column(Text, nullable=True)
    reasoning = Column(Text, nullable=True)

    # Status
    is_applied = Column(String(20), default="pending")  # pending, applied, reverted
    applied_at = Column(Date, nullable=True)
    applied_by = Column(String(100), nullable=True)

    # Metadata
    tags = Column(JSON, default=list)

    # Relationships
    source_legislation = relationship("Legislation", foreign_keys=[source_legislation_id], back_populates="amendments")
    target_legislation = relationship("Legislation", foreign_keys=[target_legislation_id])
    section = relationship("Section", foreign_keys=[target_section_id], back_populates="amendments")

    def __repr__(self):
        return f"<Amendment {self.change_type} on {self.target_section_id}>"
