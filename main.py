"""
GründerAI Backend - FastAPI Application with IRT-CAT Engine
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import logging
import os
from datetime import datetime
import uuid
from database import engine, Base
from models import (
    User,
    AssessmentSession,
    UserIntake,
    ItemResponse,
    PersonalityScore,
    IRTItemBank,
)


@app.on_event("startup")
async def startup_event():
    """Create tables on startup if they don't exist"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables ready")
    except Exception as e:
        logger.error(f"❌ Database error: {e}")


# Import IRT Engine
from irt_engine import IRTCATEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="GründerAI API",
    description="AI-powered Gründungszuschuss application optimizer with IRT-CAT",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS Configuration
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:5173,https://gruenderai.vercel.app",
).split(",")

logger.info(f"Configuring CORS for origins: {ALLOWED_ORIGINS}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Initialize IRT-CAT Engine (in-memory for now)
irt_engine = IRTCATEngine()

# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str


class AssessmentStartRequest(BaseModel):
    business_idea: str = Field(..., min_length=10, max_length=1000)
    industry: Optional[str] = None
    preferred_language: str = Field(default="de", pattern="^(de|en)$")


class AssessmentStartResponse(BaseModel):
    session_id: str
    first_question: Dict
    estimated_duration: int
    instructions: str


class QuestionResponse(BaseModel):
    session_id: str
    question_id: str
    response_value: int = Field(..., ge=1, le=5)
    response_time_ms: Optional[int] = None


class NextQuestionResponse(BaseModel):
    question: Optional[Dict]
    progress: Dict
    insights: List[str]
    is_complete: bool


# ============================================================================
# HEALTH CHECK & ROOT ENDPOINTS
# ============================================================================


@app.get("/", response_model=Dict)
async def root():
    """Root endpoint - API welcome"""
    return {
        "message": "GründerAI API with IRT-CAT Engine",
        "version": "1.0.0",
        "docs": "/api/docs",
        "health": "/api/health",
    }


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for monitoring"""
    return HealthResponse(
        status="healthy", timestamp=datetime.utcnow().isoformat(), version="1.0.0"
    )


# ============================================================================
# ASSESSMENT ENDPOINTS WITH REAL IRT ENGINE
# ============================================================================


@app.post("/api/v1/assessment/start", response_model=AssessmentStartResponse)
async def start_assessment(request: AssessmentStartRequest):
    """
    Start new personality assessment session with IRT-CAT Engine
    """
    try:
        logger.info(
            f"Starting IRT assessment for business idea: {request.business_idea[:50]}..."
        )

        # Generate session ID
        session_id = f"session_{uuid.uuid4().hex[:16]}"

        # Start IRT-CAT session
        result = irt_engine.start_session(
            session_id=session_id, business_idea=request.business_idea
        )

        return AssessmentStartResponse(
            session_id=result["session_id"],
            first_question=result["first_question"],
            estimated_duration=result["estimated_duration"],
            instructions="Beantworten Sie die Fragen aus Ihrer spontanen Perspektive. Es gibt keine richtigen oder falschen Antworten.",
        )

    except Exception as e:
        logger.error(f"Error starting assessment: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/assessment/respond", response_model=NextQuestionResponse)
async def submit_response(response: QuestionResponse):
    """
    Submit response to current question and get next question via IRT-CAT
    """
    try:
        logger.info(f"Processing response for session {response.session_id}")

        # Process through IRT engine
        result = irt_engine.process_response(
            session_id=response.session_id,
            item_id=response.question_id,
            response_value=response.response_value,
        )

        return NextQuestionResponse(
            question=result["question"],
            progress=result["progress"],
            insights=result["insights"],
            is_complete=result["is_complete"],
        )

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing response: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/assessment/{session_id}/results")
async def get_results(session_id: str):
    """
    Get final assessment results with personality profile and GZ prediction
    """
    try:
        logger.info(f"Fetching results for session {session_id}")

        # Get results from IRT engine
        results = irt_engine.get_results(session_id)

        return results

    except ValueError as e:
        logger.error(f"Session not found: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching results: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ERROR HANDLERS
# ============================================================================


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


# ============================================================================
# STARTUP/SHUTDOWN EVENTS
# ============================================================================


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("=" * 50)
    logger.info("GründerAI Backend Starting...")
    logger.info(f"IRT-CAT Engine initialized with {len(irt_engine.item_bank)} items")
    logger.info(f"Assessing {len(irt_engine.dimensions)} personality dimensions")
    logger.info(f"Allowed CORS origins: {ALLOWED_ORIGINS}")
    logger.info("=" * 50)


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("GründerAI Backend Shutting Down...")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,
        log_level="info",
    )
