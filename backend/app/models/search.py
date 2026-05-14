"""
JIAPI - Search Index & Analytics Models
"""
from sqlalchemy import (
    Column, String, Text, DateTime, Boolean, 
    ForeignKey, Integer, JSON, Index, Float
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY

from .base import BaseModel


class SearchIndex(BaseModel):
    """Elasticsearch sync tracking"""
    __tablename__ = "search_indices"

    entity_type = Column(String(50), nullable=False)  # legislation, caselaw, sro, etc.
    entity_id = Column(String(36), nullable=False)

    # Index status
    indexed_at = Column(DateTime, nullable=True)
    index_version = Column(Integer, default=1)

    # Content hash for change detection
    content_hash = Column(String(64), nullable=True)

    # Search metadata
    search_tags = Column(ARRAY(String), nullable=True)
    search_boost = Column(Float, default=1.0)

    is_indexed = Column(Boolean, default=False)
    last_index_error = Column(Text, nullable=True)

    __table_args__ = (
        Index("idx_search_entity", "entity_type", "entity_id"),
        Index("idx_search_indexed", "is_indexed"),
    )


class SearchLog(BaseModel):
    """Search query analytics"""
    __tablename__ = "search_logs"

    # Query info
    query_text = Column(Text, nullable=False)
    query_filters = Column(JSON, nullable=True)

    # User context
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    api_key_id = Column(String(36), ForeignKey("api_keys.id"), nullable=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(Text, nullable=True)

    # Results
    results_count = Column(Integer, default=0)
    results_clicked = Column(Integer, default=0)
    first_result_id = Column(String(36), nullable=True)

    # Performance
    response_time_ms = Column(Integer, nullable=True)

    # Timestamp
    searched_at = Column(DateTime, nullable=False)

    __table_args__ = (
        Index("idx_searchlog_query", "query_text"),
        Index("idx_searchlog_user", "user_id"),
        Index("idx_searchlog_time", "searched_at"),
    )
