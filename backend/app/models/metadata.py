"""
JIAPI Metadata, Search & Supporting Models
"""
import uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, Text, DateTime, 
    ForeignKey, Integer, Table
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .legislation import Base


# Association tables
legislation_tags = Table(
    "legislation_tags",
    Base.metadata,
    Column("legislation_id", UUID(as_uuid=True), ForeignKey("legislations.id")),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id"))
)

legislation_categories = Table(
    "legislation_categories",
    Base.metadata,
    Column("legislation_id", UUID(as_uuid=True), ForeignKey("legislations.id")),
    Column("category_id", UUID(as_uuid=True), ForeignKey("categories.id"))
)


class Source(Base):
    """External data sources (bdlaws, NBR, etc.)"""
    __tablename__ = "sources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    url = Column(String(500), nullable=True)
    source_type = Column(String(50), nullable=False)  # government, court, international
    reliability_score = Column(Integer, default=100)  # 0-100
    last_scraped_at = Column(DateTime(timezone=True), nullable=True)
    scrape_config = Column(Text, nullable=True)  # JSON config for scraper
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Tag(Base):
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    name_bn = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    color = Column(String(7), nullable=True)  # hex color

    legislations = relationship("Legislation", secondary=legislation_tags, backref="tag_objects")


class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    name_bn = Column(String(100), nullable=True)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    description = Column(Text, nullable=True)

    legislations = relationship("Legislation", secondary=legislation_categories, backref="category_objects")
    parent = relationship("Category", remote_side="Category.id", backref="children")


class DocumentAttachment(Base):
    """PDFs, scanned documents, official gazettes"""
    __tablename__ = "document_attachments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Polymorphic reference
    attachable_type = Column(String(50), nullable=False)  # legislation, case_law, amendment
    attachable_id = Column(UUID(as_uuid=True), nullable=False)

    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=True)
    mime_type = Column(String(100), nullable=True)

    # OCR data
    ocr_text = Column(Text, nullable=True)
    ocr_confidence = Column(Float, nullable=True)
    ocr_language = Column(String(10), default="ben")  # ben, eng

    # Metadata
    page_count = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SearchIndex(Base):
    """Elasticsearch sync tracking"""
    __tablename__ = "search_indices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    index_name = Column(String(100), nullable=False)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(UUID(as_uuid=True), nullable=False)

    indexed_at = Column(DateTime(timezone=True), server_default=func.now())
    index_version = Column(Integer, default=1)

    __table_args__ = (
        Index("idx_search_entity", "entity_type", "entity_id"),
    )


class SearchQuery(Base):
    """Search analytics"""
    __tablename__ = "search_queries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_text = Column(Text, nullable=False)
    filters = Column(Text, nullable=True)  # JSON
    results_count = Column(Integer, nullable=True)
    user_id = Column(UUID(as_uuid=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("idx_search_query", "query_text"),
    )
