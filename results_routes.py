"""
Results Routes - FastAPI endpoints for assessment results
Integrates with Day 2 scenario assessment

Endpoints:
- GET /api/v1/results/{session_id} - Get complete results
- GET /api/v1/results/{session_id}/profile - Personality profile only
- GET /api/v1/results/{session_id}/gaps - Gap analysis only
- GET /api/v1/results/{session_id}/radar - Radar chart data
- POST /api/v1/results/{session_id}/track - Track engagement
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import logging

from results_generator import ResultsGenerator, generate_assessment_results

# Setup logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/v1/results", tags=["Results"])

# Initialize generator
results_generator = ResultsGenerator()

# In-memory storage for results (replace with DB in production)
_results_cache: Dict[str, Dict[str, Any]] = {}
_engagement_tracking: Dict[str, Dict[str, Any]] = {}


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class DimensionScoreInput(BaseModel):
    """Input format for dimension scores"""
    theta: float = Field(..., description="IRT theta value")
    percentile: int = Field(..., ge=0, le=100, description="Percentile ranking")


class BusinessContextInput(BaseModel):
    """Input format for business context"""
    business_type: str = Field(..., description="Type of business")
    target_customer: Optional[str] = None
    business_idea: Optional[str] = None
    stage: Optional[str] = None


class GenerateResultsRequest(BaseModel):
    """Request to generate results"""
    user_id: str
    session_id: str
    dimension_scores: Dict[str, DimensionScoreInput]
    business_context: BusinessContextInput
    completed_modules: List[int] = Field(default_factory=list)


class TrackEngagementRequest(BaseModel):
    """Request to track engagement"""
    event_type: str = Field(..., description="Type of engagement event")
    event_data: Optional[Dict[str, Any]] = None
    timestamp: Optional[str] = None


class ResultsResponse(BaseModel):
    """Complete results response"""
    success: bool
    session_id: str
    results: Dict[str, Any]
    generated_at: str


class ProfileResponse(BaseModel):
    """Personality profile response"""
    success: bool
    session_id: str
    profile: Dict[str, Any]


class GapsResponse(BaseModel):
    """Gap analysis response"""
    success: bool
    session_id: str
    gaps: Dict[str, Any]


class RadarResponse(BaseModel):
    """Radar chart data response"""
    success: bool
    session_id: str
    chart_data: List[Dict[str, Any]]


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _get_cached_results(session_id: str) -> Optional[Dict[str, Any]]:
    """Get results from cache"""
    return _results_cache.get(session_id)


def _cache_results(session_id: str, results: Dict[str, Any]) -> None:
    """Cache results"""
    _results_cache[session_id] = results


def _convert_dimension_scores(
    scores: Dict[str, DimensionScoreInput]
) -> Dict[str, Dict[str, float]]:
    """Convert Pydantic models to dict format"""
    return {
        dim: {"theta": score.theta, "percentile": score.percentile}
        for dim, score in scores.items()
    }


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/generate", response_model=ResultsResponse)
async def generate_results(request: GenerateResultsRequest):
    """
    Generate complete assessment results.
    
    Called after assessment completion to create
    personality profile, gap analysis, and CTAs.
    """
    try:
        logger.info(f"Generating results for session: {request.session_id}")
        
        # Convert input formats
        dimension_scores = _convert_dimension_scores(request.dimension_scores)
        business_context = request.business_context.dict()
        
        # Generate results
        results = results_generator.generate_results_dict(
            user_id=request.user_id,
            session_id=request.session_id,
            dimension_scores=dimension_scores,
            business_context=business_context,
            completed_modules=request.completed_modules
        )
        
        # Cache results
        _cache_results(request.session_id, results)
        
        logger.info(
            f"Results generated: archetype={results['personality_profile']['archetype']['id']}, "
            f"readiness={results['gap_analysis']['readiness']['current']}%"
        )
        
        return ResultsResponse(
            success=True,
            session_id=request.session_id,
            results=results,
            generated_at=datetime.now(timezone.utc).isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error generating results: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}", response_model=ResultsResponse)
async def get_results(session_id: str):
    """
    Get complete assessment results for a session.
    
    Returns cached results or 404 if not found.
    """
    results = _get_cached_results(session_id)
    
    if not results:
        raise HTTPException(
            status_code=404,
            detail=f"Results not found for session: {session_id}"
        )
    
    return ResultsResponse(
        success=True,
        session_id=session_id,
        results=results,
        generated_at=results.get("timestamp", datetime.now(timezone.utc).isoformat())
    )


@router.get("/{session_id}/profile", response_model=ProfileResponse)
async def get_profile(session_id: str):
    """
    Get personality profile only.
    
    Useful for quick profile displays.
    """
    results = _get_cached_results(session_id)
    
    if not results:
        raise HTTPException(
            status_code=404,
            detail=f"Results not found for session: {session_id}"
        )
    
    return ProfileResponse(
        success=True,
        session_id=session_id,
        profile=results.get("personality_profile", {})
    )


@router.get("/{session_id}/gaps", response_model=GapsResponse)
async def get_gaps(session_id: str):
    """
    Get gap analysis only.
    
    Returns readiness scores and critical gaps.
    """
    results = _get_cached_results(session_id)
    
    if not results:
        raise HTTPException(
            status_code=404,
            detail=f"Results not found for session: {session_id}"
        )
    
    return GapsResponse(
        success=True,
        session_id=session_id,
        gaps=results.get("gap_analysis", {})
    )


@router.get("/{session_id}/radar", response_model=RadarResponse)
async def get_radar_data(session_id: str):
    """
    Get radar chart visualization data.
    
    Returns formatted data for recharts or Chart.js.
    """
    results = _get_cached_results(session_id)
    
    if not results:
        raise HTTPException(
            status_code=404,
            detail=f"Results not found for session: {session_id}"
        )
    
    chart_data = results.get("visualization", {}).get("radar_chart_data", [])
    
    return RadarResponse(
        success=True,
        session_id=session_id,
        chart_data=chart_data
    )


@router.post("/{session_id}/track")
async def track_engagement(session_id: str, request: TrackEngagementRequest):
    """
    Track user engagement on results page.
    
    Events:
    - page_view: User viewed results
    - scroll_depth: How far user scrolled
    - cta_click: Clicked Module 1 CTA
    - share_click: Clicked share button
    - time_on_page: Time spent on results
    """
    try:
        # Initialize tracking for session if needed
        if session_id not in _engagement_tracking:
            _engagement_tracking[session_id] = {
                "events": [],
                "first_view": None,
                "cta_clicked": False
            }
        
        tracking = _engagement_tracking[session_id]
        
        # Record event
        event = {
            "type": request.event_type,
            "data": request.event_data,
            "timestamp": request.timestamp or datetime.now(timezone.utc).isoformat()
        }
        tracking["events"].append(event)
        
        # Track specific events
        if request.event_type == "page_view" and not tracking["first_view"]:
            tracking["first_view"] = event["timestamp"]
        
        if request.event_type == "cta_click":
            tracking["cta_clicked"] = True
        
        logger.info(f"Tracked {request.event_type} for session {session_id}")
        
        return {
            "success": True,
            "event_recorded": request.event_type,
            "session_id": session_id
        }
        
    except Exception as e:
        logger.error(f"Error tracking engagement: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}/engagement")
async def get_engagement(session_id: str):
    """
    Get engagement data for a session.
    
    Used for analytics and conversion tracking.
    """
    tracking = _engagement_tracking.get(session_id)
    
    if not tracking:
        return {
            "success": True,
            "session_id": session_id,
            "has_engagement": False,
            "data": None
        }
    
    return {
        "success": True,
        "session_id": session_id,
        "has_engagement": True,
        "data": {
            "event_count": len(tracking["events"]),
            "first_view": tracking["first_view"],
            "cta_clicked": tracking["cta_clicked"],
            "events": tracking["events"][-10:]  # Last 10 events
        }
    }


@router.get("/health")
async def results_health():
    """Health check for results engine"""
    return {
        "status": "healthy",
        "engine": "ResultsGenerator",
        "components": {
            "personality_profiler": "operational",
            "gap_analyzer": "operational",
            "cta_generator": "operational"
        },
        "cache_size": len(_results_cache),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# ============================================================================
# INTEGRATION WITH SCENARIO ENGINE
# ============================================================================

async def generate_results_from_assessment(
    session_id: str,
    user_id: str,
    dimension_estimates: Dict[str, Dict[str, float]],
    business_context: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Integration function called by scenario_cat_engine when assessment completes.
    
    This is called automatically when a user finishes all scenarios.
    
    Args:
        session_id: Assessment session ID
        user_id: User ID
        dimension_estimates: Final theta estimates from CAT engine
        business_context: Business context from Day 1
    
    Returns:
        Complete results dictionary
    """
    # Convert dimension estimates to expected format
    dimension_scores = {}
    for dim, estimate in dimension_estimates.items():
        theta = estimate.get('theta', 0.0)
        # Convert theta to percentile using normal CDF approximation
        percentile = _theta_to_percentile(theta)
        dimension_scores[dim] = {
            "theta": theta,
            "percentile": percentile
        }
    
    # Generate results
    results = results_generator.generate_results_dict(
        user_id=user_id,
        session_id=session_id,
        dimension_scores=dimension_scores,
        business_context=business_context,
        completed_modules=[]
    )
    
    # Cache results
    _cache_results(session_id, results)
    
    return results


def _theta_to_percentile(theta: float) -> int:
    """
    Convert theta to percentile using normal CDF approximation.
    
    Uses Zelen & Severo approximation for standard normal CDF.
    """
    import math
    
    # Clamp theta to reasonable range
    theta = max(-3.0, min(3.0, theta))
    
    # Zelen & Severo approximation
    if theta < 0:
        return 100 - _theta_to_percentile(-theta)
    
    b0 = 0.2316419
    b1 = 0.319381530
    b2 = -0.356563782
    b3 = 1.781477937
    b4 = -1.821255978
    b5 = 1.330274429
    
    t = 1.0 / (1.0 + b0 * theta)
    
    pdf = math.exp(-0.5 * theta * theta) / math.sqrt(2 * math.pi)
    cdf = 1.0 - pdf * (b1*t + b2*t**2 + b3*t**3 + b4*t**4 + b5*t**5)
    
    return int(round(cdf * 100))
