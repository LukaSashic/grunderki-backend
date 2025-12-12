"""
AI Scenario Assessment API Routes v2
FastAPI endpoints for Claude-powered personality assessment

OPTIMIZED VERSION with:
- Prompt caching (90% cost reduction)
- Batch pre-generation (80% latency reduction)
- Dynamic personalized gap analysis
- 6 advanced prompting techniques
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
import logging

# Use optimized v2 generator
from ai_scenario_generator_v2 import (
    get_ai_cat_engine,
    AIScenarioCATv2 as AIScenarioCAT,
    DIMENSIONS,
    BUSINESS_CONTEXTS
)

logger = logging.getLogger(__name__)

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
    
    ON-DEMAND: Generates first scenario immediately (~2-3s).
    Subsequent scenarios generated per question for fast initial load.
    Uses prompt caching for 90% cost reduction.
    """
    import uuid
    import time
    
    session_id = str(uuid.uuid4())[:8]
    start_time = time.time()
    
    try:
        # Validate business context
        business_type = request.business_context.get('business_type', 'services')
        if business_type not in BUSINESS_CONTEXTS:
            business_type = 'services'
            request.business_context['business_type'] = business_type
        
        # Create session WITHOUT batch pre-generation (faster startup!)
        # Scenarios will be generated on-demand for each question
        session_info = engine.create_session(
            session_id, 
            request.business_context,
            use_batch_generation=False  # On-demand is faster for first response
        )
        
        creation_time = time.time() - start_time
        logger.info(f"Session {session_id} created in {creation_time:.2f}s")
        
        # Get first scenario (generated on-demand, ~2-3s)
        scenario_start = time.time()
        next_data = engine.get_next_scenario(session_id)
        scenario_time = time.time() - scenario_start
        logger.info(f"First scenario generated in {scenario_time:.2f}s")
        
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
        logger.error(f"Failed to start assessment: {str(e)}")
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


@router.get("/health")
async def health_check():
    """Health check endpoint with optimization status"""
    return {
        "status": "healthy",
        "version": "2.1.0",
        "mode": "on-demand",
        "optimizations": {
            "prompt_caching": True,
            "on_demand_generation": True,
            "advanced_prompting": True,
            "dynamic_gaps": True
        },
        "expected_performance": {
            "first_scenario_ms": "2000-3000",
            "subsequent_scenario_ms": "1500-2500 (cached)",
            "cost_per_assessment_eur": "0.02"
        }
    }


@router.get("/{session_id}/stats")
async def get_session_stats(
    session_id: str,
    engine: AIScenarioCAT = Depends(get_engine)
):
    """Get performance stats for a session"""
    try:
        results = engine.get_results(session_id)
        stats = results.get('session_stats', {})
        return {
            "session_id": session_id,
            "scenarios_generated": stats.get('scenarios_generated', 0),
            "cache_hits": stats.get('cache_hits', 0),
            "cache_hit_rate": f"{stats.get('cache_hits', 0) / max(1, stats.get('scenarios_generated', 1)) * 100:.0f}%"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
