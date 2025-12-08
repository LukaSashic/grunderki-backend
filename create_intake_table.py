"""
Create intake tables for progressive profiling
"""

from database import engine, Base
from models import (
    User,
    AssessmentSession,
    UserIntake,
    ItemResponse,
    PersonalityScore,
    IRTItemBank,
)


def create_tables():
    """Create all tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")


if __name__ == "__main__":
    create_tables()
