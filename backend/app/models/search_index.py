"""
JIAPI - Search Index Model
For Elasticsearch synchronization tracking
"""
import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, DateTime, Boolean, Integer,
    ForeignKey, Enum, JSON, Index
)
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class SearchIndex(Base):
    __tablename__ = "search_index"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Source reference
    source_type = Column(
        Enum("legislation", "content_block", "case_law", "circular", 
             "general_order", "dtaa", name="source_type"),
        nullable=False,
        index=True
    )
    source_id = Column(UUID(as_uuid=True), nullable=False, index=True)

    # Searchable content
    title = Column(String(500), nullable=True)
    content = Column(Text, nullable=True)
    content_summary = Column(Text, nullable=True)

    # Metadata for faceting
    era = Column(String(20), nullable=True)
    document_type = Column(String(50), nullable=True)
    year = Column(Integer, nullable=True)
    authority = Column(String(100), nullable=True)
    sector_tags = Column(JSON, nullable=True)
    keywords = Column(JSON, nullable=True)

    # Language
    language = Column(String(10), default="en", nullable=False)

    # Elasticsearch status
    indexed_at = Column(DateTime, nullable=True)
    index_version = Column(Integer, default=1)
    needs_reindex = Column(Boolean, default=True)

    # Audit
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_search_source", "source_type", "source_id"),
        Index("idx_search_needs_reindex", "needs_reindex", "source_type"),
        Index("idx_search_type_year", "document_type", "year"),
    )
