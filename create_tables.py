"""
Script to create all database tables
Run this once to initialize the database
"""

from database import engine, Base
from models import User, AssessmentSession, ItemResponse, PersonalityScore, IRTItemBank
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_tables():
    """Create all tables in the database"""
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ All tables created successfully!")

        # List created tables
        logger.info("Created tables:")
        for table in Base.metadata.sorted_tables:
            logger.info(f"  - {table.name}")

    except Exception as e:
        logger.error(f"❌ Error creating tables: {str(e)}")
        raise


if __name__ == "__main__":
    create_tables()
