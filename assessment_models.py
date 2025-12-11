"""
Database Models for GründerAI Assessment System
PostgreSQL models for persistent session storage

Includes:
- AssessmentSession: Main session tracking
- DimensionScore: Individual dimension results
- ScenarioResponse: Individual scenario responses
"""

from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Text, JSON,
    ForeignKey, Enum as SQLEnum, Index, UniqueConstraint
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime, timezone
import uuid
import enum

Base = declarative_base()


class AssessmentPhaseEnum(enum.Enum):
    """Assessment phases."""
    BUSINESS_CONTEXT = "business_context"
    PERSONALITY_SCENARIOS = "personality_scenarios"
    COMPLETED = "completed"


class SessionStatusEnum(enum.Enum):
    """Session status values."""
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class AssessmentSessionModel(Base):
    """
    Main assessment session model.
    
    Tracks the complete user journey from business context through
    personality scenarios to final results.
    """
    __tablename__ = 'assessment_sessions'
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(36), unique=True, nullable=False, index=True,
                       default=lambda: str(uuid.uuid4()))
    
    # User identification (optional for anonymous users)
    user_id = Column(String(255), nullable=True, index=True)
    
    # Phase and status tracking
    current_phase = Column(
        SQLEnum(AssessmentPhaseEnum),
        default=AssessmentPhaseEnum.BUSINESS_CONTEXT,
        nullable=False
    )
    status = Column(
        SQLEnum(SessionStatusEnum),
        default=SessionStatusEnum.ACTIVE,
        nullable=False,
        index=True
    )
    
    # Business context from Day 1 (stored as JSON)
    business_context = Column(JSONB, default={})
    business_context_complete = Column(Boolean, default=False)
    
    # Scenario tracking
    scenarios_seen = Column(JSONB, default=[])
    current_scenario_id = Column(String(50), nullable=True)
    current_dimension = Column(String(50), nullable=True)
    total_scenarios = Column(Integer, default=0)
    
    # Dimension estimates (stored as JSON for flexibility)
    dimension_estimates = Column(JSONB, default={})
    
    # Final results
    final_results = Column(JSONB, nullable=True)
    gz_approval_probability = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), 
                       default=lambda: datetime.now(timezone.utc),
                       onupdate=lambda: datetime.now(timezone.utc))
    business_context_completed_at = Column(DateTime(timezone=True), nullable=True)
    scenarios_completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    dimension_scores = relationship(
        "DimensionScoreModel",
        back_populates="session",
        cascade="all, delete-orphan"
    )
    scenario_responses = relationship(
        "ScenarioResponseModel",
        back_populates="session",
        cascade="all, delete-orphan"
    )
    
    # Indexes
    __table_args__ = (
        Index('ix_session_user_status', 'user_id', 'status'),
        Index('ix_session_created', 'created_at'),
    )
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'user_id': self.user_id,
            'current_phase': self.current_phase.value if self.current_phase else None,
            'status': self.status.value if self.status else None,
            'business_context': self.business_context,
            'business_context_complete': self.business_context_complete,
            'scenarios_seen': self.scenarios_seen,
            'current_scenario_id': self.current_scenario_id,
            'total_scenarios': self.total_scenarios,
            'dimension_estimates': self.dimension_estimates,
            'final_results': self.final_results,
            'gz_approval_probability': self.gz_approval_probability,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'business_context_completed_at': self.business_context_completed_at.isoformat() if self.business_context_completed_at else None,
            'scenarios_completed_at': self.scenarios_completed_at.isoformat() if self.scenarios_completed_at else None
        }


class DimensionScoreModel(Base):
    """
    Individual dimension scores for completed assessments.
    
    Provides normalized, queryable dimension data separate from
    the main session JSON blob.
    """
    __tablename__ = 'dimension_scores'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(36), ForeignKey('assessment_sessions.session_id'), 
                       nullable=False, index=True)
    
    # Dimension identification
    dimension = Column(String(50), nullable=False)
    
    # IRT scores
    theta = Column(Float, nullable=False)
    se = Column(Float, nullable=False)  # Standard error
    
    # User-friendly scores
    percentile = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)  # 0-100 scale
    level = Column(String(20), nullable=False)  # sehr_hoch, hoch, moderat, niedrig, sehr_niedrig
    
    # Assessment quality
    n_items = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    session = relationship("AssessmentSessionModel", back_populates="dimension_scores")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('session_id', 'dimension', name='uq_session_dimension'),
        Index('ix_dimension_scores_dimension', 'dimension'),
    )
    
    def to_dict(self):
        return {
            'dimension': self.dimension,
            'theta': self.theta,
            'se': self.se,
            'percentile': self.percentile,
            'score': self.score,
            'level': self.level,
            'n_items': self.n_items
        }


class ScenarioResponseModel(Base):
    """
    Individual scenario responses for analytics and improvement.
    
    Tracks each response for:
    - Analytics on scenario effectiveness
    - Audit trail of user journey
    - Future ML training data
    """
    __tablename__ = 'scenario_responses'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(36), ForeignKey('assessment_sessions.session_id'),
                       nullable=False, index=True)
    
    # Scenario identification
    scenario_id = Column(String(50), nullable=False)
    dimension = Column(String(50), nullable=False)
    
    # Response data
    selected_option = Column(String(1), nullable=False)  # A, B, C, D
    theta_value = Column(Float, nullable=False)
    information = Column(Float, nullable=False)
    
    # Context at time of response
    theta_before = Column(Float, nullable=True)  # Estimate before this response
    theta_after = Column(Float, nullable=True)   # Estimate after this response
    se_before = Column(Float, nullable=True)
    se_after = Column(Float, nullable=True)
    
    # Scenario details for analysis
    scenario_difficulty = Column(Float, nullable=True)
    scenario_discrimination = Column(Float, nullable=True)
    
    # Order tracking
    response_order = Column(Integer, nullable=False)  # 1-based order in session
    
    # Timing
    responded_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    response_time_ms = Column(Integer, nullable=True)  # Time to respond in milliseconds
    
    # Relationships
    session = relationship("AssessmentSessionModel", back_populates="scenario_responses")
    
    # Indexes
    __table_args__ = (
        Index('ix_responses_scenario', 'scenario_id'),
        Index('ix_responses_dimension', 'dimension'),
        Index('ix_responses_session_order', 'session_id', 'response_order'),
    )
    
    def to_dict(self):
        return {
            'scenario_id': self.scenario_id,
            'dimension': self.dimension,
            'selected_option': self.selected_option,
            'theta_value': self.theta_value,
            'information': self.information,
            'response_order': self.response_order,
            'responded_at': self.responded_at.isoformat() if self.responded_at else None,
            'response_time_ms': self.response_time_ms
        }


# ========== Repository Pattern for Database Operations ==========

class AssessmentRepository:
    """
    Repository for assessment database operations.
    
    Provides clean interface between CAT engine and database.
    """
    
    def __init__(self, db_session):
        """
        Initialize with database session.
        
        Args:
            db_session: SQLAlchemy session object
        """
        self.db = db_session
    
    def create_session(
        self,
        user_id: str = None,
        business_context: dict = None
    ) -> AssessmentSessionModel:
        """Create new assessment session."""
        session = AssessmentSessionModel(
            user_id=user_id,
            business_context=business_context or {},
            dimension_estimates={
                dim: {'theta': 0.0, 'se': 2.0, 'n_items': 0, 'responses': []}
                for dim in [
                    'innovativeness', 'risk_taking', 'achievement_orientation',
                    'autonomy_orientation', 'proactiveness', 'locus_of_control',
                    'self_efficacy'
                ]
            }
        )
        
        if business_context and business_context.get('business_type'):
            session.business_context_complete = True
            session.current_phase = AssessmentPhaseEnum.PERSONALITY_SCENARIOS
            session.business_context_completed_at = datetime.now(timezone.utc)
        
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        
        return session
    
    def get_session(self, session_id: str) -> AssessmentSessionModel:
        """Get session by ID."""
        return self.db.query(AssessmentSessionModel).filter(
            AssessmentSessionModel.session_id == session_id
        ).first()
    
    def update_session(self, session: AssessmentSessionModel) -> AssessmentSessionModel:
        """Update session in database."""
        session.updated_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(session)
        return session
    
    def record_response(
        self,
        session_id: str,
        scenario_id: str,
        dimension: str,
        selected_option: str,
        theta_value: float,
        information: float,
        response_order: int,
        theta_before: float = None,
        theta_after: float = None,
        se_before: float = None,
        se_after: float = None,
        scenario_difficulty: float = None,
        scenario_discrimination: float = None,
        response_time_ms: int = None
    ) -> ScenarioResponseModel:
        """Record a scenario response."""
        response = ScenarioResponseModel(
            session_id=session_id,
            scenario_id=scenario_id,
            dimension=dimension,
            selected_option=selected_option,
            theta_value=theta_value,
            information=information,
            response_order=response_order,
            theta_before=theta_before,
            theta_after=theta_after,
            se_before=se_before,
            se_after=se_after,
            scenario_difficulty=scenario_difficulty,
            scenario_discrimination=scenario_discrimination,
            response_time_ms=response_time_ms
        )
        
        self.db.add(response)
        self.db.commit()
        
        return response
    
    def save_dimension_scores(
        self,
        session_id: str,
        dimension_results: dict
    ):
        """Save final dimension scores."""
        for dimension, data in dimension_results.items():
            score = DimensionScoreModel(
                session_id=session_id,
                dimension=dimension,
                theta=data['theta'],
                se=data['se'],
                percentile=data['percentile'],
                score=data['score'],
                level=data['level'],
                n_items=data['n_items']
            )
            self.db.add(score)
        
        self.db.commit()
    
    def get_user_sessions(
        self,
        user_id: str,
        status: SessionStatusEnum = None,
        limit: int = 10
    ) -> list:
        """Get sessions for a user."""
        query = self.db.query(AssessmentSessionModel).filter(
            AssessmentSessionModel.user_id == user_id
        )
        
        if status:
            query = query.filter(AssessmentSessionModel.status == status)
        
        return query.order_by(
            AssessmentSessionModel.created_at.desc()
        ).limit(limit).all()
    
    def get_session_analytics(self, session_id: str) -> dict:
        """Get detailed analytics for a session."""
        session = self.get_session(session_id)
        if not session:
            return None
        
        responses = self.db.query(ScenarioResponseModel).filter(
            ScenarioResponseModel.session_id == session_id
        ).order_by(ScenarioResponseModel.response_order).all()
        
        return {
            'session': session.to_dict(),
            'responses': [r.to_dict() for r in responses],
            'dimension_scores': [s.to_dict() for s in session.dimension_scores]
        }


# ========== Database Initialization ==========

def init_db(engine):
    """Create all tables."""
    Base.metadata.create_all(engine)


def drop_db(engine):
    """Drop all tables (use with caution!)."""
    Base.metadata.drop_all(engine)


# SQL for manual creation (if needed)
CREATE_TABLES_SQL = """
-- Assessment Sessions Table
CREATE TABLE IF NOT EXISTS assessment_sessions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(36) UNIQUE NOT NULL,
    user_id VARCHAR(255),
    current_phase VARCHAR(30) NOT NULL DEFAULT 'business_context',
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    business_context JSONB DEFAULT '{}',
    business_context_complete BOOLEAN DEFAULT FALSE,
    scenarios_seen JSONB DEFAULT '[]',
    current_scenario_id VARCHAR(50),
    current_dimension VARCHAR(50),
    total_scenarios INTEGER DEFAULT 0,
    dimension_estimates JSONB DEFAULT '{}',
    final_results JSONB,
    gz_approval_probability FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    business_context_completed_at TIMESTAMP WITH TIME ZONE,
    scenarios_completed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS ix_session_id ON assessment_sessions(session_id);
CREATE INDEX IF NOT EXISTS ix_session_user ON assessment_sessions(user_id);
CREATE INDEX IF NOT EXISTS ix_session_status ON assessment_sessions(status);

-- Dimension Scores Table
CREATE TABLE IF NOT EXISTS dimension_scores (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(36) NOT NULL REFERENCES assessment_sessions(session_id),
    dimension VARCHAR(50) NOT NULL,
    theta FLOAT NOT NULL,
    se FLOAT NOT NULL,
    percentile INTEGER NOT NULL,
    score INTEGER NOT NULL,
    level VARCHAR(20) NOT NULL,
    n_items INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(session_id, dimension)
);

CREATE INDEX IF NOT EXISTS ix_dim_session ON dimension_scores(session_id);

-- Scenario Responses Table
CREATE TABLE IF NOT EXISTS scenario_responses (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(36) NOT NULL REFERENCES assessment_sessions(session_id),
    scenario_id VARCHAR(50) NOT NULL,
    dimension VARCHAR(50) NOT NULL,
    selected_option VARCHAR(1) NOT NULL,
    theta_value FLOAT NOT NULL,
    information FLOAT NOT NULL,
    theta_before FLOAT,
    theta_after FLOAT,
    se_before FLOAT,
    se_after FLOAT,
    scenario_difficulty FLOAT,
    scenario_discrimination FLOAT,
    response_order INTEGER NOT NULL,
    responded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    response_time_ms INTEGER
);

CREATE INDEX IF NOT EXISTS ix_resp_session ON scenario_responses(session_id);
CREATE INDEX IF NOT EXISTS ix_resp_scenario ON scenario_responses(scenario_id);
"""


if __name__ == "__main__":
    # Print SQL for manual creation
    print("=== Create Tables SQL ===")
    print(CREATE_TABLES_SQL)
