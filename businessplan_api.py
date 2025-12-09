# businessplan_api.py
"""
Businessplan API Endpoints

Endpoints:
- POST /api/v1/businessplan/generate - Generate complete businessplan
- GET /api/v1/businessplan/{session_id} - Get generated businessplan
- POST /api/v1/businessplan/download - Download as DOCX/PDF
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import logging
from datetime import datetime

from businessplan_generator import BusinessplanGenerator

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/businessplan", tags=["businessplan"])


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class UserLocation(BaseModel):
    """User location info"""
    city: str
    district: Optional[str] = None
    bundesland: Optional[str] = None
    plz: Optional[str] = None


class UserInfo(BaseModel):
    """User personal info"""
    location: UserLocation
    family_status: str = 'single'  # 'single' | 'familie_2_kinder'
    name: Optional[str] = None


class GenerateBusinessplanRequest(BaseModel):
    """Request to generate businessplan"""
    session_id: str
    user_info: UserInfo
    include_research: bool = False  # Future: Web research integration


class GenerateBusinessplanResponse(BaseModel):
    """Response with generated businessplan"""
    success: bool
    businessplan: Dict
    quality_score: int
    living_validation: Dict
    meta: Dict
    message: str


class GetBusinessplanResponse(BaseModel):
    """Response when fetching existing businessplan"""
    success: bool
    businessplan: Optional[Dict] = None
    generated_at: Optional[str] = None
    message: str


# ============================================================================
# IN-MEMORY STORAGE (for MVP)
# ============================================================================

# Store generated businessplans
businessplans = {}  # session_id -> businessplan_data


# ============================================================================
# API ENDPOINTS
# ============================================================================

@router.post("/generate", response_model=GenerateBusinessplanResponse)
async def generate_businessplan(request: GenerateBusinessplanRequest):
    """
    Generate complete, GZ-compliant businessplan
    
    Requires completed Vision Discovery session with all 3 phases
    """
    
    logger.info(f"📋 Businessplan generation requested for session: {request.session_id}")
    
    try:
        # TODO: Fetch session data from database
        # For now, mock session data (replace with actual DB fetch)
        session_data = _get_mock_session_data()
        
        # Validate session is complete
        if not _validate_session_complete(session_data):
            raise HTTPException(
                status_code=400,
                detail="Session incomplete. All 3 phases (Vision, JTBD, GZ) must be completed."
            )
        
        # Initialize generator
        generator = BusinessplanGenerator()
        
        # Extract phase data
        vision_data = session_data.get('vision', {})
        jtbd_data = session_data.get('jtbd', {})
        gz_data = session_data.get('gz', {})
        
        # Generate businessplan
        logger.info("🚀 Starting generation...")
        businessplan = await generator.generate(
            vision_data=vision_data,
            jtbd_data=jtbd_data,
            gz_data=gz_data,
            user_info=request.user_info.dict()
        )
        
        # Calculate quality score
        quality_score = _calculate_quality_score(businessplan)
        
        # Store in memory
        businessplans[request.session_id] = {
            'businessplan': businessplan,
            'generated_at': datetime.now().isoformat(),
            'user_info': request.user_info.dict(),
            'quality_score': quality_score
        }
        
        logger.info(f"✅ Businessplan generated! Quality: {quality_score}/100")
        
        return GenerateBusinessplanResponse(
            success=True,
            businessplan=businessplan,
            quality_score=quality_score,
            living_validation=businessplan.get('living_validation', {}),
            meta=businessplan.get('meta', {}),
            message=f"Businessplan erfolgreich generiert (Quality Score: {quality_score}/100)"
        )
    
    except Exception as e:
        logger.error(f"❌ Businessplan generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}", response_model=GetBusinessplanResponse)
async def get_businessplan(session_id: str):
    """
    Retrieve generated businessplan
    """
    
    logger.info(f"📄 Fetching businessplan for session: {session_id}")
    
    if session_id not in businessplans:
        return GetBusinessplanResponse(
            success=False,
            businessplan=None,
            message="Businessplan not found. Please generate first."
        )
    
    data = businessplans[session_id]
    
    return GetBusinessplanResponse(
        success=True,
        businessplan=data['businessplan'],
        generated_at=data['generated_at'],
        message="Businessplan retrieved successfully"
    )


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "generator_available": True,
        "stored_plans": len(businessplans)
    }


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _get_mock_session_data() -> Dict:
    """
    Mock session data for testing
    TODO: Replace with actual database fetch
    """
    return {
        'vision': {
            'magic_wand_answer': 'KMUs bei der Digitalisierung unterstützen',
            'deep_why': 'Habe selbst erlebt wie schwer es ist ohne Hilfe',
            'desired_outcome': 'Dass jedes KMU Zugang zu Automatisierung hat',
            'personal_vision': 'Digitalisierung für alle zugänglich machen'
        },
        'jtbd': {
            'functional_job': 'Manuelle Prozesse automatisieren',
            'emotional_job': 'Sich modern und zukunftsfähig fühlen',
            'social_job': 'Als innovatives Unternehmen wahrgenommen werden',
            'current_alternatives': 'Excel, manuelle Prozesse, externe Berater',
            'why_alternatives_fail': 'Zu zeitaufwendig, zu teuer, nicht nachhaltig',
            'job_story': 'Wenn KMUs ihre Prozesse optimieren wollen, wollen sie manuelle Prozesse automatisieren, damit sie sich zukunftsfähig fühlen',
            'opportunity_score': 75
        },
        'gz': {
            'what': 'AI-Automatisierungs-Beratung für deutsche KMUs',
            'who': 'Deutsche KMUs mit 10-50 Mitarbeitern',
            'problem': 'Manuelle Prozesse die Zeit und Geld kosten',
            'why_you': '8 Jahre IT-Beratung, 5 Jahre RPA-Expertise, Zertifikate von Roboyo',
            'revenue_source': 'Beratungsstunden à 120€, monatliche Workshops à 2.500€',
            'how': 'Hauptberuflich 30 Stunden pro Woche, vor Ort und remote',
            'capital_needs': '8.000€ für Equipment und Marketing'
        }
    }


def _validate_session_complete(session_data: Dict) -> bool:
    """Check if all phases are complete"""
    
    required_phases = ['vision', 'jtbd', 'gz']
    
    for phase in required_phases:
        if phase not in session_data:
            return False
        if not session_data[phase]:
            return False
    
    return True


def _calculate_quality_score(businessplan: Dict) -> int:
    """
    Calculate overall quality score (0-100)
    
    Criteria:
    - Completeness (40%)
    - Living validation (30%)
    - Citations (15%)
    - SWOT depth (15%)
    """
    
    score = 0
    
    # 1. Completeness (40 points)
    required_sections = [
        'executive_summary',
        'geschaeftsidee',
        'swot_data',
        'finanzplan',
        'lebenshaltungskosten'
    ]
    
    completed = sum(1 for s in required_sections if s in businessplan)
    score += (completed / len(required_sections)) * 40
    
    # 2. Living validation (30 points)
    living_val = businessplan.get('living_validation', {})
    if living_val.get('lebensfaehig'):
        score += 30
    elif living_val.get('monate_ueberbrueckbar', 0) >= 6:
        score += 15  # Partial points if 6+ months bridgeable
    
    # 3. Citations (15 points)
    quellenverzeichnis = businessplan.get('quellenverzeichnis', '')
    if len(quellenverzeichnis) > 100:
        score += 15
    elif len(quellenverzeichnis) > 50:
        score += 10
    
    # 4. SWOT depth (15 points)
    swot = businessplan.get('swot_data', {})
    swot_items = sum(len(swot.get(k, [])) for k in ['staerken', 'schwaechen', 'chancen', 'risiken'])
    score += min(15, swot_items * 1.5)
    
    return int(min(100, score))


# ============================================================================
# EXPORT
# ============================================================================

__all__ = ['router']
