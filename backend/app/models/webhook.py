"""
JIAPI - Webhook Subscription Model
Real-time notifications for law changes
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


class WebhookSubscription(Base):
    __tablename__ = "webhook_subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Endpoint
    endpoint_url = Column(String(500), nullable=False)
    endpoint_secret = Column(String(255), nullable=True)

    # Event types
    event_types = Column(ARRAY(String), nullable=False)
    # e.g., ["legislation.amended", "sro.issued", "case_law.published", "circular.issued"]

    # Filters
    era_filter = Column(ARRAY(String), nullable=True)
    type_filter = Column(ARRAY(String), nullable=True)
    sector_filter = Column(ARRAY(String), nullable=True)
    section_numbers = Column(ARRAY(String), nullable=True)

    # Status
    is_active = Column(Boolean, default=True, nullable=False)

    # Delivery tracking
    last_delivered_at = Column(DateTime, nullable=True)
    last_delivery_status = Column(Integer, nullable=True)
    delivery_failures = Column(Integer, default=0)

    # Retry configuration
    max_retries = Column(Integer, default=3)
    retry_interval_seconds = Column(Integer, default=300)

    # Audit
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="webhooks")

    __table_args__ = (
        Index("idx_webhook_user", "user_id", "is_active"),
        Index("idx_webhook_events", "event_types", "is_active"),
    )
