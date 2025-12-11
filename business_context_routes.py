"""
Business Context API Routes

Provides REST endpoints for the business context capture phase:
- POST /api/v1/assessment/business-context/start
- POST /api/v1/assessment/business-context/answer
- GET  /api/v1/assessment/business-context/progress/{session_id}
- POST /api/v1/assessment/business-context/complete

Author: Opus (Implementation Layer)
Date: 2025-12-11
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
import uuid
import logging

from business_context import BusinessContextHandler
from business_context_validator import (
    BusinessContextValidator, 
    business_context_rate_limiter
)

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/api/v1/assessment/business-context",
    tags=["Business Context"]
)

# Initialize handler (singleton)
_handler: Optional[BusinessContextHandler] = None


def get_handler() -> BusinessContextHandler:
    """Get or create BusinessContextHandler singleton."""
    global _handler
    if _handler is None:
        _handler = BusinessContextHandler()
    return _handler


# In-memory session storage (for development - use Redis/DB in production)
_sessions: Dict[str, Dict[str, Any]] = {}


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class StartBusinessContextRequest(BaseModel):
    """Request model for starting business context capture."""
    user_id: Optional[str] = Field(None, description="Optional user ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user-123"
            }
        }


class StartBusinessContextResponse(BaseModel):
    """Response model for starting business context capture."""
    session_id: str
    question: Dict[str, Any]
    progress: Dict[str, Any]
    phase: str = "business_context"


class SubmitAnswerRequest(BaseModel):
    """Request model for submitting an answer."""
    session_id: str = Field(..., description="Session ID")
    question_id: str = Field(..., description="Question being answered")
    answer: Dict[str, Any] = Field(..., description="User's answer")
    response_time_ms: Optional[int] = Field(None, description="Time to respond in ms")
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "question_id": "Q1a_category",
                "answer": {"selected": "restaurant"},
                "response_time_ms": 4500
            }
        }


class SubmitAnswerResponse(BaseModel):
    """Response model for answer submission."""
    accepted: bool
    completed: bool = False
    next_question: Optional[Dict[str, Any]] = None
    progress: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    business_context: Optional[Dict[str, Any]] = None
    specificity_score: Optional[float] = None


class ProgressResponse(BaseModel):
    """Response model for progress check."""
    session_id: str
    completed: bool
    current_question: int
    total_questions: int
    percentage: int
    captured_data: Dict[str, Any]
    time_elapsed_seconds: int


class CompleteRequest(BaseModel):
    """Request model for completing business context."""
    session_id: str = Field(..., description="Session ID")


class CompleteResponse(BaseModel):
    """Response model for completing business context."""
    completed: bool
    business_context: Dict[str, Any]
    specificity_score: float
    ready_for_personality: bool
    next_step: Dict[str, Any]


# ============================================================================
# RATE LIMITING MIDDLEWARE
# ============================================================================

async def check_rate_limit(request: Request):
    """Check rate limit for request."""
    # Get client IP or use session ID
    client_ip = request.client.host if request.client else "unknown"
    
    if not business_context_rate_limiter.is_allowed(client_ip):
        remaining = business_context_rate_limiter.get_remaining(client_ip)
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Rate limit exceeded",
                "message": "Zu viele Anfragen. Bitte warte einen Moment.",
                "retry_after_seconds": 60,
                "remaining": remaining
            }
        )


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post(
    "/start",
    response_model=StartBusinessContextResponse,
    summary="Start Business Context Capture",
    description="""
    Start a new business context capture session.
    
    This initiates the guided question flow where users provide
    business information through 4-5 questions.
    
    Returns the first question and session metadata.
    """
)
async def start_business_context(
    request: StartBusinessContextRequest = None,
    _: None = Depends(check_rate_limit)
):
    """Start business context capture session."""
    try:
        logger.info("Starting new business context session")
        
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # Get handler and start session
        handler = get_handler()
        result = handler.start_session()
        
        # Store session
        _sessions[session_id] = {
            "user_id": request.user_id if request else None,
            "started_at": datetime.now(timezone.utc),
            "answers": [],
            "current_question": result["question"]["id"],
            "status": "active"
        }
        
        logger.info(f"Session {session_id} started successfully")
        
        return StartBusinessContextResponse(
            session_id=session_id,
            question=result["question"],
            progress=result["progress"],
            phase=result.get("phase", "business_context")
        )
        
    except Exception as e:
        logger.error(f"Error starting business context: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to start session",
                "message": str(e)
            }
        )


@router.post(
    "/answer",
    response_model=SubmitAnswerResponse,
    summary="Submit Answer",
    description="""
    Submit an answer to the current question.
    
    Validates the answer, processes it, and returns either:
    - The next question (if more questions remain)
    - The completed business context (if all questions answered)
    - An error (if validation fails)
    """
)
async def submit_answer(
    request: SubmitAnswerRequest,
    _: None = Depends(check_rate_limit)
):
    """Submit answer to current question."""
    try:
        # Validate session exists
        if request.session_id not in _sessions:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "Session not found",
                    "message": "Session existiert nicht oder ist abgelaufen",
                    "code": "SESSION_NOT_FOUND"
                }
            )
        
        session = _sessions[request.session_id]
        
        # Validate session is active
        if session["status"] != "active":
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Session not active",
                    "message": "Session ist nicht mehr aktiv",
                    "code": "SESSION_INACTIVE"
                }
            )
        
        # Validate question ID
        if not BusinessContextValidator.validate_question_id(request.question_id):
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid question ID",
                    "message": "Ungültige Fragen-ID",
                    "code": "INVALID_QUESTION_ID"
                }
            )
        
        # Validate and sanitize answer
        question_type = "multiple_choice"  # Will be determined from question
        validation = BusinessContextValidator.validate_answer(request.answer, question_type)
        
        if not validation["valid"]:
            return SubmitAnswerResponse(
                accepted=False,
                error=validation.get("error"),
                error_code=validation.get("code")
            )
        
        # Sanitize answer
        sanitized_answer = BusinessContextValidator.sanitize_answer(
            request.answer, 
            question_type
        )
        
        # Process answer
        handler = get_handler()
        result = handler.process_answer(
            question_id=request.question_id,
            answer=sanitized_answer,
            previous_answers=session["answers"]
        )
        
        # Check if answer was accepted
        if not result.get("accepted", False):
            return SubmitAnswerResponse(
                accepted=False,
                error=result.get("error"),
                error_code=result.get("error_code")
            )
        
        # Update session with new answers
        if "answers" in result:
            session["answers"] = result["answers"]
        
        # Check if completed
        if result.get("completed", False):
            session["status"] = "completed"
            session["completed_at"] = datetime.now(timezone.utc)
            session["business_context"] = result.get("business_context", {})
            
            logger.info(f"Session {request.session_id} completed")
            
            return SubmitAnswerResponse(
                accepted=True,
                completed=True,
                business_context=result.get("business_context"),
                specificity_score=result.get("specificity_score")
            )
        
        # More questions to go
        session["current_question"] = result["next_question"]["id"]
        
        return SubmitAnswerResponse(
            accepted=True,
            completed=False,
            next_question=result.get("next_question"),
            progress=result.get("progress")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing answer: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to process answer",
                "message": str(e)
            }
        )


@router.get(
    "/progress/{session_id}",
    response_model=ProgressResponse,
    summary="Get Progress",
    description="""
    Get current progress for a business context session.
    
    Returns:
    - Current question number
    - Total estimated questions
    - Percentage complete
    - Data captured so far
    - Time elapsed
    """
)
async def get_progress(
    session_id: str,
    _: None = Depends(check_rate_limit)
):
    """Get progress for session."""
    try:
        # Validate session ID format
        if not BusinessContextValidator.validate_session_id(session_id):
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid session ID",
                    "message": "Ungültige Session-ID",
                    "code": "INVALID_SESSION_ID"
                }
            )
        
        # Check session exists
        if session_id not in _sessions:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "Session not found",
                    "message": "Session existiert nicht",
                    "code": "SESSION_NOT_FOUND"
                }
            )
        
        session = _sessions[session_id]
        
        # Calculate time elapsed
        time_elapsed = (datetime.now(timezone.utc) - session["started_at"]).total_seconds()
        
        # Calculate captured data from answers
        handler = get_handler()
        captured_data = {}
        if session["answers"]:
            captured_data = handler._compile_business_context(session["answers"])
            # Remove raw_answers for cleaner response
            captured_data.pop("raw_answers", None)
        
        # Calculate progress
        answers_count = len(session["answers"])
        estimated_total = 5  # Base estimate
        
        return ProgressResponse(
            session_id=session_id,
            completed=session["status"] == "completed",
            current_question=answers_count + 1,
            total_questions=estimated_total,
            percentage=min(int((answers_count / estimated_total) * 100), 95),
            captured_data=captured_data,
            time_elapsed_seconds=int(time_elapsed)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting progress: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to get progress",
                "message": str(e)
            }
        )


@router.post(
    "/complete",
    response_model=CompleteResponse,
    summary="Complete Business Context",
    description="""
    Mark business context capture as complete and prepare for next phase.
    
    Returns:
    - Completed business context
    - Specificity score
    - Whether ready for personality assessment
    - Next step information
    """
)
async def complete_business_context(
    request: CompleteRequest,
    _: None = Depends(check_rate_limit)
):
    """Complete business context capture."""
    try:
        # Validate session ID
        if not BusinessContextValidator.validate_session_id(request.session_id):
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid session ID",
                    "message": "Ungültige Session-ID",
                    "code": "INVALID_SESSION_ID"
                }
            )
        
        # Check session exists
        if request.session_id not in _sessions:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "Session not found",
                    "message": "Session existiert nicht",
                    "code": "SESSION_NOT_FOUND"
                }
            )
        
        session = _sessions[request.session_id]
        
        # Check if already completed
        if session["status"] == "completed" and "business_context" in session:
            # Return existing completion
            handler = get_handler()
            specificity = handler._calculate_specificity(session["answers"])
            
            return CompleteResponse(
                completed=True,
                business_context=session["business_context"],
                specificity_score=specificity,
                ready_for_personality=specificity >= 0.50,
                next_step={
                    "phase": "personality_scenarios",
                    "endpoint": "/api/v1/assessment/personality/start"
                }
            )
        
        # Compile business context
        handler = get_handler()
        business_context = handler._compile_business_context(session["answers"])
        specificity = handler._calculate_specificity(session["answers"])
        
        # Validate business context
        validation = BusinessContextValidator.validate_business_context(business_context)
        if not validation["valid"]:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": validation.get("error"),
                    "code": validation.get("code")
                }
            )
        
        # Update session
        session["status"] = "completed"
        session["completed_at"] = datetime.now(timezone.utc)
        session["business_context"] = business_context
        
        # Remove raw_answers from response
        response_context = business_context.copy()
        response_context.pop("raw_answers", None)
        
        logger.info(f"Session {request.session_id} completed with specificity {specificity:.2%}")
        
        return CompleteResponse(
            completed=True,
            business_context=response_context,
            specificity_score=specificity,
            ready_for_personality=specificity >= 0.50,
            next_step={
                "phase": "personality_scenarios",
                "endpoint": "/api/v1/assessment/personality/start"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error completing business context: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to complete",
                "message": str(e)
            }
        )


# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@router.get(
    "/questions/{question_id}",
    summary="Get Question by ID",
    description="Get a specific question by its ID (for debugging/testing)"
)
async def get_question(question_id: str):
    """Get question by ID."""
    try:
        if not BusinessContextValidator.validate_question_id(question_id):
            raise HTTPException(
                status_code=400,
                detail={"error": "Invalid question ID"}
            )
        
        handler = get_handler()
        question = handler.get_question_by_id(question_id)
        
        return {"question": question}
        
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail={"error": str(e)}
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": str(e)}
        )


@router.get(
    "/health",
    summary="Health Check",
    description="Check if business context service is healthy"
)
async def health_check():
    """Health check for business context service."""
    try:
        handler = get_handler()
        question_count = len(handler.questions)
        
        return {
            "status": "healthy",
            "questions_loaded": question_count,
            "active_sessions": len(_sessions),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
