"""
SQLAlchemy Database Models for GründerAI
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
    JSON,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import uuid


class User(Base):
    """User model - for authentication (future)"""

    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    sessions = relationship("AssessmentSession", back_populates="user")


class AssessmentSession(Base):
    """Assessment Session - tracks one complete assessment"""

    __tablename__ = "assessment_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(
        String, ForeignKey("users.id"), nullable=True
    )  # Nullable for anonymous users

    # Business Context
    business_idea = Column(Text, nullable=False)
    industry = Column(String, nullable=True)

    # Session Metadata
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, default="active")  # active, completed, abandoned

    # IRT-CAT Configuration
    max_items = Column(Integer, default=18)
    min_items = Column(Integer, default=12)
    target_se = Column(Float, default=0.20)
    max_time_minutes = Column(Integer, default=15)

    # Current State (stored as JSON for flexibility)
    current_dimension = Column(String, nullable=True)
    items_administered = Column(JSON, default=list)  # List of item IDs

    # Relationships
    user = relationship("User", back_populates="sessions")
    responses = relationship("ItemResponse", back_populates="session")
    personality_scores = relationship("PersonalityScore", back_populates="session")


class ItemResponse(Base):
    """Individual item response during assessment"""

    __tablename__ = "item_responses"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("assessment_sessions.id"), nullable=False)

    # Item Information
    item_id = Column(String, nullable=False)
    dimension = Column(String, nullable=False)  # Which of 7 dimensions

    # Response Data
    response_value = Column(Integer, nullable=False)  # 1-5 scale
    response_time_ms = Column(Integer, nullable=True)
    responded_at = Column(DateTime(timezone=True), server_default=func.now())

    # IRT Estimates at time of response
    theta_before = Column(Float, nullable=True)
    theta_after = Column(Float, nullable=True)
    se_before = Column(Float, nullable=True)
    se_after = Column(Float, nullable=True)
    information = Column(Float, nullable=True)  # Item information

    # Relationships
    session = relationship("AssessmentSession", back_populates="responses")


class PersonalityScore(Base):
    """Final personality scores for each dimension"""

    __tablename__ = "personality_scores"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("assessment_sessions.id"), nullable=False)

    # Dimension Scores (Howard's 7 dimensions)
    innovativeness = Column(Float, nullable=True)
    risk_taking = Column(Float, nullable=True)
    achievement_orientation = Column(Float, nullable=True)
    autonomy_orientation = Column(Float, nullable=True)
    proactiveness = Column(Float, nullable=True)
    locus_of_control = Column(Float, nullable=True)
    self_efficacy = Column(Float, nullable=True)

    # Standard Errors for each dimension
    innovativeness_se = Column(Float, nullable=True)
    risk_taking_se = Column(Float, nullable=True)
    achievement_orientation_se = Column(Float, nullable=True)
    autonomy_orientation_se = Column(Float, nullable=True)
    proactiveness_se = Column(Float, nullable=True)
    locus_of_control_se = Column(Float, nullable=True)
    self_efficacy_se = Column(Float, nullable=True)

    # Metadata
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    session = relationship("AssessmentSession", back_populates="personality_scores")


class IRTItemBank(Base):
    """Item bank with IRT parameters"""

    __tablename__ = "irt_item_bank"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(String, unique=True, nullable=False, index=True)
    dimension = Column(String, nullable=False, index=True)

    # Item Text
    text_de = Column(Text, nullable=False)
    text_en = Column(Text, nullable=True)

    # IRT Parameters (Graded Response Model)
    discrimination = Column(Float, nullable=False)  # 'a' parameter
    difficulty_b1 = Column(Float, nullable=False)  # Threshold between 1-2
    difficulty_b2 = Column(Float, nullable=False)  # Threshold between 2-3
    difficulty_b3 = Column(Float, nullable=False)  # Threshold between 3-4
    difficulty_b4 = Column(Float, nullable=False)  # Threshold between 4-5

    # Response Scale (stored as JSON)
    response_scale = Column(JSON, nullable=False)  # {1: "text", 2: "text", ...}

    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
