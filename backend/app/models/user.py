"""
JIAPI - User & Subscription Models
Commercial API access control
"""
from sqlalchemy import Column, String, Text, Date, DateTime, Boolean, ForeignKey, Integer, Enum, JSON, Numeric, Index
from sqlalchemy.orm import relationship
from app.models.base import BaseModel, Base
import enum


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    RESEARCHER = "researcher"
    API_USER = "api_user"
    FREE = "free"


class SubscriptionTier(str, enum.Enum):
    FREE = "free"
    BASIC = "basic"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    LAW_FIRM = "law_firm"


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String(255), nullable=False, unique=True, index=True)
    hashed_password = Column(String(255), nullable=True)
    full_name = Column(String(200), nullable=True)
    full_name_bn = Column(String(200), nullable=True)

    # Organization
    organization = Column(String(200), nullable=True)
    organization_type = Column(String(50), nullable=True)  # law_firm, corporate, nbr, academic, individual
    tin_number = Column(String(50), nullable=True)

    # Role & Status
    role = Column(Enum(UserRole), default=UserRole.FREE)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)

    # Subscription
    subscription_tier = Column(Enum(SubscriptionTier), default=SubscriptionTier.FREE)
    subscription_expires = Column(DateTime, nullable=True)

    # API Usage
    api_key = Column(String(100), nullable=True, unique=True, index=True)
    api_key_created = Column(DateTime, nullable=True)
    api_calls_today = Column(Integer, default=0)
    api_calls_total = Column(Integer, default=0)
    rate_limit = Column(Integer, default=100)  # requests per day

    # Preferences
    preferred_language = Column(String(10), default="en")  # en, bn
    notification_email = Column(Boolean, default=True)
    notification_webhook = Column(String(500), nullable=True)

    # Metadata
    last_login = Column(DateTime, nullable=True)
    login_count = Column(Integer, default=0)

    # Relationships
    bookmarks = relationship("Bookmark", back_populates="user", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="user", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_user_email", "email"),
        Index("idx_user_api_key", "api_key"),
        Index("idx_user_subscription", "subscription_tier"),
    )


class Bookmark(BaseModel):
    __tablename__ = "bookmarks"

    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    item_type = Column(String(50), nullable=False)  # legislation, case_law, content_block
    item_id = Column(String(36), nullable=False)

    # Annotation
    notes = Column(Text, nullable=True)
    tags = Column(JSON, default=list)

    # Relationships
    user = relationship("User", back_populates="bookmarks")

    __table_args__ = (
        Index("idx_bookmark_user", "user_id"),
        Index("idx_bookmark_item", "item_type", "item_id"),
    )


class Alert(BaseModel):
    __tablename__ = "alerts"

    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)

    # What to watch
    alert_type = Column(String(50), nullable=False)  # legislation_change, new_case, new_sro, rate_change
    target_legislation_id = Column(String(36), ForeignKey("legislations.id"), nullable=True)
    target_section = Column(String(100), nullable=True)
    keywords = Column(JSON, default=list)

    # Delivery
    email_enabled = Column(Boolean, default=True)
    webhook_enabled = Column(Boolean, default=False)
    webhook_url = Column(String(500), nullable=True)

    # Status
    is_active = Column(Boolean, default=True)
    last_triggered = Column(DateTime, nullable=True)
    trigger_count = Column(Integer, default=0)

    # Relationships
    user = relationship("User", back_populates="alerts")

    __table_args__ = (
        Index("idx_alert_user", "user_id"),
        Index("idx_alert_type", "alert_type"),
    )
