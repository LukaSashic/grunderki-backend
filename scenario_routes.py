"""
Scenario Assessment API Routes
FastAPI endpoints for the personality scenario assessment

Endpoints:
- POST /assessment/start - Start unified assessment
- POST /assessment/business-context - Set business context (Day 1)
- GET /assessment/{session_id}/scenario - Get current scenario
- POST /assessment/{session_id}/respond - Submit scenario response
- GET /assessment/{session_id}/results - Get final results
- GET /assessment/{session_id}/status - Get session status
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

from sqlalchemy.orm import Session

# Import our modules
from scenario_cat_engine import ScenarioCATEngine, AssessmentPhase, SessionStatus
from assessment_models import (
    AssessmentSessionModel, AssessmentPhaseEnum, SessionStatusEnum,
    AssessmentRepository, init_db
)

# Create router
router = APIRouter(prefix="/api/v1/assessment", tags=["Assessment"])


# ========== Pydantic Models ==========

class BusinessType(str, Enum):
    """Supported business types."""
    restaurant = "restaurant"
    saas = "saas"
    consulting = "consulting"
    ecommerce = "ecommerce"
    services = "services"
    creative = "creative"
    health = "health"
    other = "other"


class StartAssessmentRequest(BaseModel):
    """Request to start a new assessment."""
    user_id: Optional[str] = Field(None, description="Optional user identifier")
    business_context: Optional[Dict[str, Any]] = Field(
        None, 
        description="Pre-populated business context to skip Day 1"
    )


class BusinessContextRequest(BaseModel):
    """Business context from Day 1 assessment."""
    business_type: BusinessType = Field(..., description="Type of business")
    sub_type: Optional[str] = Field(None, description="Business sub-category")
    target_customer: Optional[str] = Field(None, description="Target customer segment")
    problem: Optional[str] = Field(None, description="Problem being solved")
    stage: Optional[str] = Field(None, description="Business stage")
    description: Optional[str] = Field(None, description="Business description")
    
    class Config:
        use_enum_values = True


class ScenarioResponseRequest(BaseModel):
    """User's response to a scenario."""
    scenario_id: str = Field(..., description="ID of the scenario being answered")
    selected_option: str = Field(
        ..., 
        description="Selected option (A, B, C, or D)",
        pattern="^[ABCD]$"
    )
    response_time_ms: Optional[int] = Field(
        None, 
        description="Time taken to respond in milliseconds"
    )


class ProgressResponse(BaseModel):
    """Assessment progress information."""
    current_item: int
    estimated_total: int
    percentage: int
    dimensions_assessed: int
    total_dimensions: int = 7


class ScenarioResponse(BaseModel):
    """A scenario to present to the user."""
    scenario_id: str
    dimension: Optional[str] = None
    situation: str
    question: str
    options: List[Dict[str, str]]


class AssessmentResponse(BaseModel):
    """Standard assessment response."""
    session_id: Optional[str] = None  # Added for frontend compatibility
    complete: bool
    phase: str
    scenario: Optional[ScenarioResponse] = None
    progress: Optional[ProgressResponse] = None
    micro_insight: Optional[Dict[str, str]] = None
    results: Optional[Dict[str, Any]] = None
    message: Optional[str] = None


class SessionStatusResponse(BaseModel):
    """Session status information."""
    session_id: str
    status: str
    current_phase: str
    business_context_complete: bool
    total_scenarios: int
    created_at: str
    updated_at: Optional[str] = None


# ========== Dependency Injection ==========

# Global CAT engine instance
_cat_engine: Optional[ScenarioCATEngine] = None


def get_cat_engine() -> ScenarioCATEngine:
    """Get or create CAT engine instance."""
    global _cat_engine
    if _cat_engine is None:
        _cat_engine = ScenarioCATEngine()
    return _cat_engine


# Database session dependency (to be configured in main.py)
def get_db():
    """
    Get database session.
    
    This should be overridden in main.py with actual database connection.
    For now, returns None to use in-memory storage.
    """
    return None


# ========== API Endpoints ==========

@router.post("/start", response_model=AssessmentResponse)
async def start_assessment(
    request: StartAssessmentRequest,
    engine: ScenarioCATEngine = Depends(get_cat_engine)
):
    """
    Start a new assessment session.
    
    Creates a new session and either:
    - Starts with business context phase (if no context provided)
    - Skips to personality scenarios (if business context provided)
    
    Returns first scenario or instructions for business context.
    """
    try:
        # Create session
        session = engine.create_session(
            user_id=request.user_id,
            business_context=request.business_context
        )
        
        # If business context was provided, start scenarios
        if session.business_context_complete:
            response = engine.start_scenarios(session.session_id)
            return AssessmentResponse(
                session_id=session.session_id,
                complete=response.get('complete', False),
                phase=response.get('phase', AssessmentPhase.PERSONALITY_SCENARIOS.value),
                scenario=_format_scenario(response.get('scenario')),
                progress=_format_progress(response.get('progress')),
                message=f"Session {session.session_id} started with business context"
            )
        
        # Otherwise, return instructions for business context
        return AssessmentResponse(
            session_id=session.session_id,
            complete=False,
            phase=AssessmentPhase.BUSINESS_CONTEXT.value,
            message=f"Session {session.session_id} created. Please provide business context.",
            progress=ProgressResponse(
                current_item=0,
                estimated_total=12,
                percentage=0,
                dimensions_assessed=0
            )
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{session_id}/business-context", response_model=AssessmentResponse)
async def set_business_context(
    session_id: str,
    request: BusinessContextRequest,
    engine: ScenarioCATEngine = Depends(get_cat_engine)
):
    """
    Set business context and transition to personality scenarios.
    
    This completes the Day 1 phase and automatically starts Day 2.
    Returns the first personality scenario.
    """
    try:
        # Convert request to dict
        business_context = request.dict(exclude_none=True)
        
        # Set context and get first scenario
        response = engine.set_business_context(session_id, business_context)
        
        return AssessmentResponse(
            session_id=session_id,
            complete=response.get('complete', False),
            phase=response.get('phase', AssessmentPhase.PERSONALITY_SCENARIOS.value),
            scenario=_format_scenario(response.get('scenario')),
            progress=_format_progress(response.get('progress')),
            message="Business context saved. Starting personality assessment."
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}/scenario", response_model=AssessmentResponse)
async def get_current_scenario(
    session_id: str,
    engine: ScenarioCATEngine = Depends(get_cat_engine)
):
    """
    Get the current scenario for a session.
    
    Returns the active scenario if assessment is in progress,
    or results if assessment is complete.
    """
    try:
        session = engine.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        if session.status == SessionStatus.COMPLETED:
            return AssessmentResponse(
                complete=True,
                phase=AssessmentPhase.COMPLETED.value,
                results=session.final_results,
                message="Assessment already completed"
            )
        
        if not session.business_context_complete:
            return AssessmentResponse(
                complete=False,
                phase=AssessmentPhase.BUSINESS_CONTEXT.value,
                message="Please provide business context first"
            )
        
        # Get current scenario from session state
        if session.current_scenario_id:
            # Regenerate the scenario for display
            scenario_data = engine._get_scenario_by_id(session.current_scenario_id)
            personalized = engine.scenario_generator._personalize_scenario(
                scenario_data, 
                session.business_context
            )
            formatted = engine.scenario_generator.format_for_frontend(
                personalized, 
                include_metadata=True
            )
            
            return AssessmentResponse(
                complete=False,
                phase=AssessmentPhase.PERSONALITY_SCENARIOS.value,
                scenario=_format_scenario(formatted),
                progress=_format_progress(engine._calculate_progress(session))
            )
        
        # No current scenario - generate next
        response = engine.start_scenarios(session_id)
        return AssessmentResponse(
            complete=response.get('complete', False),
            phase=response.get('phase'),
            scenario=_format_scenario(response.get('scenario')),
            progress=_format_progress(response.get('progress'))
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{session_id}/respond", response_model=AssessmentResponse)
async def submit_response(
    session_id: str,
    request: ScenarioResponseRequest,
    engine: ScenarioCATEngine = Depends(get_cat_engine)
):
    """
    Submit a response to the current scenario.
    
    Processes the response, updates theta estimates, and returns
    either the next scenario or final results.
    """
    try:
        response = engine.submit_scenario_response(
            session_id=session_id,
            scenario_id=request.scenario_id,
            selected_option=request.selected_option
        )
        
        result = AssessmentResponse(
            session_id=session_id,
            complete=response.get('complete', False),
            phase=response.get('phase'),
            scenario=_format_scenario(response.get('scenario')),
            progress=_format_progress(response.get('progress')),
            micro_insight=response.get('micro_insight'),
            results=response.get('results')
        )
        
        if result.complete:
            result.message = "Assessment complete! View your results."
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}/results")
async def get_results(
    session_id: str,
    engine: ScenarioCATEngine = Depends(get_cat_engine)
):
    """
    Get final assessment results.
    
    Only available after assessment is complete.
    Returns full personality profile with GZ readiness assessment.
    """
    try:
        results = engine.get_results(session_id)
        
        return {
            "session_id": session_id,
            "status": "completed",
            "results": results
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}/status", response_model=SessionStatusResponse)
async def get_session_status(
    session_id: str,
    engine: ScenarioCATEngine = Depends(get_cat_engine)
):
    """
    Get current session status.
    
    Returns phase, progress, and timing information.
    """
    try:
        session = engine.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return SessionStatusResponse(
            session_id=session.session_id,
            status=session.status.value,
            current_phase=session.current_phase.value,
            business_context_complete=session.business_context_complete,
            total_scenarios=session.total_scenarios,
            created_at=session.started_at
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{session_id}")
async def abandon_session(
    session_id: str,
    engine: ScenarioCATEngine = Depends(get_cat_engine)
):
    """
    Mark a session as abandoned.
    
    Used when user exits before completing assessment.
    """
    try:
        session = engine.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session.status = SessionStatus.ABANDONED
        
        return {
            "session_id": session_id,
            "status": "abandoned",
            "message": "Session marked as abandoned"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== Admin/Debug Endpoints ==========

@router.get("/{session_id}/debug")
async def get_debug_info(
    session_id: str,
    engine: ScenarioCATEngine = Depends(get_cat_engine)
):
    """
    Get detailed session state for debugging.
    
    Returns full internal state including theta estimates.
    """
    try:
        state = engine.get_session_state(session_id)
        return state
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/health")
async def health_check(engine: ScenarioCATEngine = Depends(get_cat_engine)):
    """
    Health check endpoint.
    
    Returns status of CAT engine and scenario bank.
    """
    validation = engine.scenario_generator.validate_coverage()
    
    return {
        "status": "healthy",
        "engine": "ScenarioCATEngine",
        "scenario_bank": {
            "total_scenarios": validation['total_scenarios'],
            "dimensions_covered": validation['dimensions_covered'],
            "valid": validation['valid']
        },
        "timestamp": datetime.utcnow().isoformat()
    }


# ========== Helper Functions ==========

def _format_scenario(scenario_data: Optional[Dict]) -> Optional[ScenarioResponse]:
    """Format scenario data for API response."""
    if not scenario_data:
        return None
    
    return ScenarioResponse(
        scenario_id=scenario_data.get('scenario_id', ''),
        dimension=scenario_data.get('dimension'),
        situation=scenario_data.get('situation', ''),
        question=scenario_data.get('question', ''),
        options=scenario_data.get('options', [])
    )


def _format_progress(progress_data: Optional[Dict]) -> Optional[ProgressResponse]:
    """Format progress data for API response."""
    if not progress_data:
        return None
    
    return ProgressResponse(
        current_item=progress_data.get('current_item', 0),
        estimated_total=progress_data.get('estimated_total', 12),
        percentage=progress_data.get('percentage', 0),
        dimensions_assessed=progress_data.get('dimensions_assessed', 0),
        total_dimensions=progress_data.get('total_dimensions', 7)
    )


# ========== Unified Assessment Flow ==========

@router.post("/unified/start", response_model=AssessmentResponse)
async def start_unified_assessment(
    request: StartAssessmentRequest,
    engine: ScenarioCATEngine = Depends(get_cat_engine)
):
    """
    Start a unified assessment that includes both business context and personality scenarios.
    
    This is the recommended entry point for the complete assessment flow.
    """
    return await start_assessment(request, engine)


@router.post("/unified/{session_id}/next", response_model=AssessmentResponse)
async def get_next_item(
    session_id: str,
    business_context: Optional[BusinessContextRequest] = None,
    response: Optional[ScenarioResponseRequest] = None,
    engine: ScenarioCATEngine = Depends(get_cat_engine)
):
    """
    Get the next item in the unified assessment flow.
    
    Handles both:
    - Setting business context (if in Day 1 phase)
    - Submitting scenario responses (if in Day 2 phase)
    
    Automatically transitions between phases.
    """
    try:
        session = engine.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # If business context provided and needed, set it
        if business_context and not session.business_context_complete:
            return await set_business_context(session_id, business_context, engine)
        
        # If response provided and in scenario phase, process it
        if response and session.current_phase == AssessmentPhase.PERSONALITY_SCENARIOS:
            return await submit_response(session_id, response, engine)
        
        # Otherwise, get current scenario
        return await get_current_scenario(session_id, engine)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== Frontend Compatibility Endpoint ==========

@router.get("/{session_id}/next")
async def get_next_question(
    session_id: str,
    engine: ScenarioCATEngine = Depends(get_cat_engine)
):
    """
    Get next question - Frontend compatibility endpoint.
    
    Returns data in format expected by React frontend:
    - 'question' instead of 'scenario'
    - 'is_complete' instead of 'complete'
    """
    try:
        session = engine.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # If not business context complete, return instructions
        if not session.business_context_complete:
            return {
                "session_id": session_id,
                "question": None,
                "progress": {
                    "items_completed": 0,
                    "estimated_remaining": 12,
                    "percentage": 0
                },
                "is_complete": False,
                "phase": "business_context",
                "message": "Please provide business context first"
            }
        
        # If completed, return results
        if session.status == SessionStatus.COMPLETED:
            return {
                "session_id": session_id,
                "question": None,
                "is_complete": True,
                "phase": "completed",
                "results": session.final_results
            }
        
        # Get current/next scenario
        if session.current_scenario_id:
            scenario_data = engine._get_scenario_by_id(session.current_scenario_id)
            personalized = engine.scenario_generator._personalize_scenario(
                scenario_data, 
                session.business_context
            )
            formatted = engine.scenario_generator.format_for_frontend(
                personalized, 
                include_metadata=True
            )
        else:
            # Generate first scenario
            response = engine.start_scenarios(session_id)
            formatted = response.get('scenario')
        
        # Map to frontend format
        question = None
        if formatted:
            question = {
                "id": formatted.get("scenario_id"),
                "text_de": formatted.get("situation", "") + " " + formatted.get("question", ""),
                "dimension": formatted.get("dimension"),
                "options": formatted.get("options", [])
            }
        
        progress = engine._calculate_progress(session)
        
        return {
            "session_id": session_id,
            "question": question,
            "progress": {
                "items_completed": progress.get("current_item", 0),
                "estimated_remaining": progress.get("estimated_total", 12) - progress.get("current_item", 0),
                "percentage": progress.get("percentage", 0)
            },
            "is_complete": False,
            "phase": "assessment"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class FrontendRespondRequest(BaseModel):
    """Frontend-compatible respond request."""
    session_id: str
    question_id: str
    response_value: int  # 1-5 scale from frontend
    response_time_ms: Optional[int] = None


@router.post("/respond")
async def frontend_submit_response(
    request: FrontendRespondRequest,
    engine: ScenarioCATEngine = Depends(get_cat_engine)
):
    """
    Submit response - Frontend compatibility endpoint.
    
    Accepts frontend format and maps to backend format:
    - question_id -> scenario_id
    - response_value (1-5) -> selected_option (A-D)
    """
    try:
        # Map response_value (1-5) to option letter (A-D)
        # 1=strongly disagree -> A, 5=strongly agree -> D
        option_map = {1: "A", 2: "B", 3: "C", 4: "D", 5: "D"}
        selected_option = option_map.get(request.response_value, "B")
        
        # Call the actual respond endpoint
        response = engine.submit_scenario_response(
            session_id=request.session_id,
            scenario_id=request.question_id,
            selected_option=selected_option
        )
        
        # Format response for frontend
        question = None
        scenario = response.get('scenario')
        if scenario:
            question = {
                "id": scenario.get("scenario_id"),
                "text_de": scenario.get("situation", "") + " " + scenario.get("question", ""),
                "dimension": scenario.get("dimension"),
                "options": scenario.get("options", [])
            }
        
        progress_data = response.get('progress', {})
        
        return {
            "session_id": request.session_id,
            "question": question,
            "progress": {
                "items_completed": progress_data.get("current_item", 0),
                "estimated_remaining": progress_data.get("estimated_total", 12) - progress_data.get("current_item", 0),
                "percentage": progress_data.get("percentage", 0)
            },
            "is_complete": response.get('complete', False),
            "insights": [response.get('micro_insight')] if response.get('micro_insight') else [],
            "results": response.get('results')
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
