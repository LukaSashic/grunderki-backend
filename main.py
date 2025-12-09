"""
GründerAI Backend - FastAPI Application with IRT-CAT Engine
"""

from socratic_api import router as socratic_router
from vision_discovery_api import router as vision_router
from businessplan_api import router as businessplan_router
from fastapi import FastAPI, HTTPException, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import logging
import os
from dotenv import load_dotenv

# Load environment variables FIRST!
load_dotenv()
from datetime import datetime
import uuid

from database import engine, Base, get_db
from sqlalchemy.orm import Session
from models import (
    User,
    AssessmentSession,
    UserIntake,
    ItemResponse,
    PersonalityScore,
    IRTItemBank,
)

# Import IRT Engine
from irt_engine import IRTCATEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="GründerAI Backend API",
    description="IRT-CAT Personality Assessment for German Entrepreneurs",
    version="1.0.0",
)
app.include_router(socratic_router)
app.include_router(vision_router)
app.include_router(businessplan_router)

# CORS Configuration
allowed_origins_str = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:5173,https://gruenderki.netlify.app",
)
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize IRT-CAT Engine
irt_engine = IRTCATEngine()


# Startup Event - Create Tables
@app.on_event("startup")
async def startup_event():
    """Create tables on startup if they don't exist"""
    logger.info("=" * 50)
    logger.info("GründerAI Backend Starting...")

    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables checked/created successfully")
    except Exception as e:
        logger.error(f"❌ Database table creation error: {e}")

    logger.info(f"Configuring CORS for origins: {allowed_origins}")
    logger.info(f"IRT-CAT Engine initialized with {len(irt_engine.item_bank)} items")
    logger.info(f"Assessing {len(irt_engine.dimensions)} personality dimensions")
    logger.info("=" * 50)


# Pydantic Models
class IntakeRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., pattern=r"^[^@]+@[^@]+\.[^@]+$")
    business_idea: str = Field(..., min_length=10, max_length=1000)
    business_type: str
    experience_level: str
    timeline: str
    gz_interest: str
    growth_vision: str


class AssessmentStartRequest(BaseModel):
    session_id: str


class SubmitResponseRequest(BaseModel):
    session_id: str
    item_id: str
    response_value: int = Field(..., ge=1, le=5)
    response_time_ms: Optional[int] = None


# Health Check
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "gruenderai-backend",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/api/cache-stats")
async def cache_stats():
    """Get cache statistics"""
    from cache_service import cache

    stats = cache.get_stats()
    return {"cache": stats, "redis_connected": cache.client is not None}


@app.get("/api/admin/create-tables")
async def create_tables_endpoint():
    """
    Admin endpoint to create database tables
    WARNING: Remove this in production!
    """
    try:
        from database import Base, engine

        Base.metadata.create_all(bind=engine)

        return {
            "success": True,
            "message": "Tables created successfully",
            "tables": [
                "users",
                "user_intakes",
                "assessment_sessions",
                "item_responses",
                "personality_scores",
                "irt_item_bank",
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "service": "GründerAI Backend API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/api/health",
            "intake": "POST /api/v1/intake",
            "start_assessment": "POST /api/v1/assessment/start",
            "submit_response": "POST /api/v1/assessment/response",
            "get_results": "GET /api/v1/assessment/results/{session_id}",
        },
    }


# NEW: Save User Intake
@app.post("/api/v1/intake")
async def save_user_intake(intake: IntakeRequest, db: Session = Depends(get_db)):
    """
    Save user intake data from progressive profiling
    Creates user, session, and intake records
    """
    try:
        # 1. Create or get user by email
        user = db.query(User).filter(User.email == intake.email).first()
        if not user:
            user = User(email=intake.email)
            db.add(user)
            db.flush()  # Get user.id
            logger.info(f"Created new user: {intake.email}")
        else:
            logger.info(f"Existing user found: {intake.email}")

        # 2. Create assessment session
        session = AssessmentSession(
            user_id=user.id,
            business_idea=intake.business_idea,
            status="intake_complete",
        )
        db.add(session)
        db.flush()  # Get session.id

        # 3. Create intake record
        intake_record = UserIntake(
            session_id=session.id,
            name=intake.name,
            email=intake.email,
            business_idea=intake.business_idea,
            business_type=intake.business_type,
            experience_level=intake.experience_level,
            timeline=intake.timeline,
            gz_interest=intake.gz_interest,
            growth_vision=intake.growth_vision,
        )
        db.add(intake_record)

        # 4. Commit all changes
        db.commit()

        logger.info(f"✅ Intake saved: {session.id} for {intake.email}")

        return {
            "success": True,
            "session_id": session.id,
            "message": "Intake data gespeichert",
            "user": {"name": intake.name, "email": intake.email},
        }

    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error saving intake: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Fehler beim Speichern: {str(e)}")


# Start Assessment
@app.post("/api/v1/assessment/start")
async def start_assessment(
    request: AssessmentStartRequest, db: Session = Depends(get_db)
):
    """
    Start IRT-CAT assessment for a session
    """
    try:
        # Get session
        session = (
            db.query(AssessmentSession)
            .filter(AssessmentSession.id == request.session_id)
            .first()
        )

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Update session status
        session.status = "assessment_active"
        db.commit()

        # Start IRT-CAT session
        result = irt_engine.start_session(
            session_id=request.session_id,
            business_idea=session.business_idea,
        )

        logger.info(f"Assessment started: {request.session_id}")

        return {
            **result,
            "instructions": "Beantworten Sie die Fragen basierend auf Ihren echten Präferenzen.",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting assessment: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Submit Response
@app.post("/api/v1/assessment/response")
async def submit_response(
    request: SubmitResponseRequest, db: Session = Depends(get_db)
):
    """
    Submit response to an assessment item
    """
    try:
        # Get session
        session = (
            db.query(AssessmentSession)
            .filter(AssessmentSession.id == request.session_id)
            .first()
        )

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Submit to IRT engine
        result = irt_engine.submit_response(
            session_id=request.session_id,
            item_id=request.item_id,
            response_value=request.response_value,
        )

        # Save response to database
        item_response = ItemResponse(
            session_id=request.session_id,
            item_id=request.item_id,
            dimension=result.get("dimension", "unknown"),
            response_value=request.response_value,
            response_time_ms=request.response_time_ms,
        )
        db.add(item_response)
        db.commit()

        logger.info(
            f"Response submitted: {request.session_id} - Item {request.item_id}"
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting response: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Get Results
@app.get("/api/v1/assessment/results/{session_id}")
async def get_results(session_id: str, db: Session = Depends(get_db)):
    """
    Get final assessment results
    """
    try:
        # Get session
        session = (
            db.query(AssessmentSession)
            .filter(AssessmentSession.id == session_id)
            .first()
        )

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Get results from IRT engine
        results = irt_engine.get_session_results(session_id)

        # Save personality scores to database
        if results["is_complete"]:
            # Check if scores already saved
            existing_scores = (
                db.query(PersonalityScore)
                .filter(PersonalityScore.session_id == session_id)
                .first()
            )

            if not existing_scores:
                scores = results["personality_profile"]["dimensions"]

                personality_score = PersonalityScore(
                    session_id=session_id,
                    innovativeness=scores.get("innovativeness", {}).get(
                        "score_percentile"
                    ),
                    risk_taking=scores.get("risk_taking", {}).get("score_percentile"),
                    achievement_orientation=scores.get(
                        "achievement_orientation", {}
                    ).get("score_percentile"),
                    autonomy_orientation=scores.get("autonomy_orientation", {}).get(
                        "score_percentile"
                    ),
                    proactiveness=scores.get("proactiveness", {}).get(
                        "score_percentile"
                    ),
                    locus_of_control=scores.get("locus_of_control", {}).get(
                        "score_percentile"
                    ),
                    self_efficacy=scores.get("self_efficacy", {}).get(
                        "score_percentile"
                    ),
                )
                db.add(personality_score)

            # Update session status
            session.status = "completed"
            session.completed_at = datetime.now()
            db.commit()

        logger.info(f"Results retrieved: {session_id}")

        return results

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting results: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": str(exc),
            "status_code": 500,
        },
    )


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
