"""
AI Scenario Assessment API Routes
FastAPI endpoints for Claude-powered personality assessment

This replaces the static scenario_routes with dynamic AI-generated scenarios.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum

from ai_scenario_generator import (
    get_ai_cat_engine,
    AIScenarioCAT,
    DIMENSIONS,
    BUSINESS_CONTEXTS
)

router = APIRouter(prefix="/api/v1/ai-assessment", tags=["AI Assessment"])


# ========== Pydantic Models ==========

class BusinessType(str, Enum):
    """Supported business types - must match frontend"""
    restaurant = "restaurant"
    saas = "saas"
    consulting = "consulting"
    ecommerce = "ecommerce"
    services = "services"
    creative = "creative"
    health = "health"


class StartRequest(BaseModel):
    """Request to start AI assessment"""
    user_id: Optional[str] = None
    business_context: Dict[str, Any] = Field(
        ...,
        description="Business context including business_type, target_customer, stage, description"
    )


class ResponseRequest(BaseModel):
    """Submit response to scenario"""
    option_id: str = Field(..., pattern="^[A-D]$", description="Selected option A, B, C, or D")


class ScenarioOption(BaseModel):
    """A scenario option"""
    id: str
    text: str


class ScenarioData(BaseModel):
    """Scenario data for frontend"""
    scenario_id: str
    situation: str
    question: str
    options: List[ScenarioOption]
    dimension: Optional[str] = None


class ProgressData(BaseModel):
    """Assessment progress"""
    current_item: int
    estimated_total: int
    percentage: int
    dimensions_assessed: int


class AssessmentResponse(BaseModel):
    """Standard response format"""
    session_id: str
    complete: bool
    scenario: Optional[ScenarioData] = None
    progress: Optional[ProgressData] = None
    results: Optional[Dict[str, Any]] = None
    message: Optional[str] = None


# ========== Dependency ==========

def get_engine() -> AIScenarioCAT:
    """Get AI CAT engine instance"""
    return get_ai_cat_engine()


# ========== Endpoints ==========

@router.post("/start", response_model=AssessmentResponse)
async def start_assessment(
    request: StartRequest,
    engine: AIScenarioCAT = Depends(get_engine)
):
    """
    Start a new AI-powered assessment session.
    
    Creates session and returns first personalized scenario.
    Scenarios are generated in real-time by Claude based on business context.
    """
    import uuid
    session_id = str(uuid.uuid4())[:8]
    
    try:
        # Validate business context
        business_type = request.business_context.get('business_type', 'services')
        if business_type not in BUSINESS_CONTEXTS:
            business_type = 'services'
            request.business_context['business_type'] = business_type
        
        # Create session
        engine.create_session(session_id, request.business_context)
        
        # Get first scenario
        next_data = engine.get_next_scenario(session_id)
        
        if not next_data:
            raise HTTPException(status_code=500, detail="Failed to generate first scenario")
        
        scenario_data = next_data['scenario']
        progress_data = next_data['progress']
        
        return AssessmentResponse(
            session_id=session_id,
            complete=False,
            scenario=ScenarioData(
                scenario_id=scenario_data['scenario_id'],
                situation=scenario_data['situation'],
                question=scenario_data['question'],
                options=[ScenarioOption(**opt) for opt in scenario_data['options']],
                dimension=scenario_data.get('dimension')
            ),
            progress=ProgressData(
                current_item=progress_data['current_item'],
                estimated_total=progress_data['estimated_total'],
                percentage=progress_data['percentage'],
                dimensions_assessed=progress_data['dimensions_assessed']
            ),
            message="AI-Powered Assessment gestartet"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start assessment: {str(e)}")


@router.post("/{session_id}/respond", response_model=AssessmentResponse)
async def submit_response(
    session_id: str,
    request: ResponseRequest,
    engine: AIScenarioCAT = Depends(get_engine)
):
    """
    Submit response and get next scenario or results.
    
    Each response triggers adaptive scenario selection.
    Claude generates the next scenario based on current ability estimate.
    """
    try:
        result = engine.submit_response(session_id, request.option_id)
        
        if result.get('complete'):
            return AssessmentResponse(
                session_id=session_id,
                complete=True,
                results=result['results'],
                message="Assessment abgeschlossen!"
            )
        
        scenario_data = result['scenario']
        progress_data = result['progress']
        
        return AssessmentResponse(
            session_id=session_id,
            complete=False,
            scenario=ScenarioData(
                scenario_id=scenario_data['scenario_id'],
                situation=scenario_data['situation'],
                question=scenario_data['question'],
                options=[ScenarioOption(**opt) for opt in scenario_data['options']],
                dimension=scenario_data.get('dimension')
            ),
            progress=ProgressData(
                current_item=progress_data['current_item'],
                estimated_total=progress_data['estimated_total'],
                percentage=progress_data['percentage'],
                dimensions_assessed=progress_data['dimensions_assessed']
            )
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process response: {str(e)}")


@router.get("/{session_id}/results")
async def get_results(
    session_id: str,
    engine: AIScenarioCAT = Depends(get_engine)
):
    """Get assessment results for a session"""
    try:
        results = engine.get_results(session_id)
        return {
            "session_id": session_id,
            "complete": True,
            "results": results
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/business-types")
async def get_business_types():
    """Get available business types with German labels"""
    return {
        "business_types": [
            {
                "id": key,
                "label_de": info["label_de"],
                "industry_de": info["industry_de"]
            }
            for key, info in BUSINESS_CONTEXTS.items()
        ]
    }


@router.get("/dimensions")
async def get_dimensions():
    """Get Howard's 7 dimensions with German names"""
    return {
        "dimensions": [
            {
                "id": key,
                "name_de": info["name_de"],
                "description": info["description"]
            }
            for key, info in DIMENSIONS.items()
        ]
    }
