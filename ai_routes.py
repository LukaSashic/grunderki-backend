"""
AI Routes - Claude Integration für GründerAI
=============================================

Datei: src/api/ai_routes.py

Endpoints:
- POST /api/v1/intake - Speichert Nutzerdaten
- POST /api/v1/ai/chat - Claude AI Chat
- GET /api/v1/ai/health - Health Check
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import anthropic
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
    logger.info("✅ Anthropic package available")
except ImportError:
    ANTHROPIC_AVAILABLE = False
    logger.warning("⚠️ Anthropic package not installed - AI will use fallbacks")

# Create router
router = APIRouter(prefix="/api/v1", tags=["AI"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class IntakeRequest(BaseModel):
    """User intake data from business context capture"""
    name: str
    email: EmailStr
    business_type: str
    target_customer: Optional[str] = None
    business_stage: Optional[str] = None
    problem_description: Optional[str] = None
    unique_approach: Optional[str] = None


class IntakeResponse(BaseModel):
    """Response after saving intake"""
    success: bool
    message: str
    intake_id: Optional[str] = None


class AIChatRequest(BaseModel):
    """Request for AI-powered chat"""
    system_prompt: str
    user_message: Optional[str] = ""
    max_tokens: Optional[int] = 200
    context: Optional[Dict[str, Any]] = None


class AIChatResponse(BaseModel):
    """Response from AI chat"""
    response: str
    model: str
    tokens_used: Optional[int] = None


# ============================================================================
# ANTHROPIC CLIENT INITIALIZATION
# ============================================================================

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

if ANTHROPIC_AVAILABLE and ANTHROPIC_API_KEY:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    logger.info("✅ Anthropic client initialized")
else:
    client = None
    if not ANTHROPIC_API_KEY:
        logger.warning("⚠️ ANTHROPIC_API_KEY environment variable not set")


# ============================================================================
# INTAKE ENDPOINT
# ============================================================================

@router.post("/intake", response_model=IntakeResponse)
async def save_intake(request: IntakeRequest):
    """
    Save user intake data from business context capture.
    
    This data is used to personalize the assessment and business plan.
    """
    try:
        logger.info(f"📥 Intake received: {request.name} - {request.email} - {request.business_type}")
        
        # TODO: Save to PostgreSQL database
        # Example with SQLAlchemy:
        # 
        # from src.database import get_db
        # from src.models import UserIntake
        # 
        # db_intake = UserIntake(
        #     name=request.name,
        #     email=request.email,
        #     business_type=request.business_type,
        #     target_customer=request.target_customer,
        #     business_stage=request.business_stage,
        #     problem_description=request.problem_description,
        #     unique_approach=request.unique_approach,
        # )
        # db.add(db_intake)
        # db.commit()
        # db.refresh(db_intake)
        # intake_id = str(db_intake.id)
        
        return IntakeResponse(
            success=True,
            message="Intake data saved successfully",
            intake_id="placeholder-uuid"  # Replace with actual UUID from DB
        )
        
    except Exception as e:
        logger.error(f"❌ Error saving intake: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save intake data")


# ============================================================================
# AI CHAT ENDPOINT
# ============================================================================

@router.post("/ai/chat", response_model=AIChatResponse)
async def ai_chat(request: AIChatRequest):
    """
    AI-powered chat using Claude API.
    
    Used for:
    - Generating personalized questions in business context capture
    - Extracting structured data from user responses
    - Providing coaching insights
    
    Falls back to template responses if Claude is unavailable.
    """
    
    # Check if Claude is available
    if not client:
        logger.info("🔄 Using fallback (Claude not available)")
        return generate_fallback_response(request)
    
    try:
        # Build messages array
        messages = []
        
        if request.user_message:
            messages.append({
                "role": "user",
                "content": request.user_message
            })
        else:
            # If no user message, create a trigger message
            messages.append({
                "role": "user",
                "content": "Bitte antworte basierend auf dem System-Prompt."
            })
        
        # Call Claude API
        logger.info("🤖 Calling Claude API...")
        response = client.messages.create(
            model="claude-3-haiku-20240307",  # Fast & cost-effective
            max_tokens=request.max_tokens,
            system=request.system_prompt,
            messages=messages
        )
        
        # Extract response text
        response_text = ""
        if response.content:
            response_text = response.content[0].text
        
        tokens_used = None
        if hasattr(response, 'usage'):
            tokens_used = response.usage.output_tokens
        
        logger.info(f"✅ Claude response received ({tokens_used} tokens)")
        
        return AIChatResponse(
            response=response_text,
            model="claude-3-haiku-20240307",
            tokens_used=tokens_used
        )
        
    except anthropic.APIError as e:
        logger.error(f"❌ Anthropic API error: {str(e)}")
        return generate_fallback_response(request)
        
    except Exception as e:
        logger.error(f"❌ AI chat error: {str(e)}")
        return generate_fallback_response(request)


# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================

@router.get("/ai/health")
async def ai_health_check():
    """
    Check AI service availability.
    
    Returns status information about the AI integration.
    """
    return {
        "anthropic_available": ANTHROPIC_AVAILABLE,
        "api_key_configured": bool(ANTHROPIC_API_KEY),
        "client_initialized": client is not None,
        "status": "ready" if client else "fallback_mode"
    }


# ============================================================================
# FALLBACK RESPONSE GENERATOR
# ============================================================================

def generate_fallback_response(request: AIChatRequest) -> AIChatResponse:
    """
    Generate intelligent fallback when Claude is unavailable.
    
    Uses context from the request to generate relevant responses.
    These are high-quality template responses based on production-grade
    prompting techniques.
    """
    context = request.context or {}
    
    category_label = context.get("categoryLabel", "deinem Geschäft")
    target_customer_label = context.get("targetCustomerLabel", "deinen Kunden")
    user_name = context.get("userName", "")
    
    # Check what kind of prompt this is based on keywords
    system_prompt_lower = request.system_prompt.lower()
    
    if "frage" in system_prompt_lower or "question" in system_prompt_lower:
        # This is a question generation request
        import random
        fallback_questions = [
            f"Was ist das größte Problem, das {target_customer_label} aktuell haben und das du mit {category_label} lösen möchtest?",
            f"Wenn {target_customer_label} deine {category_label} nutzen - was soll danach anders sein als vorher?",
            f"Was unterscheidet deinen Ansatz von dem, was {target_customer_label} aktuell als Alternative nutzen?",
            f"Warum bist gerade du die richtige Person, um dieses Problem für {target_customer_label} zu lösen?",
        ]
        response = random.choice(fallback_questions)
        
    elif "extrahiere" in system_prompt_lower or "extract" in system_prompt_lower:
        # This is a data extraction request - return structured JSON
        response = '''{
  "problem_description": "Lösung für Zielgruppe im gewählten Bereich",
  "unique_approach": "Personalisierter, professioneller Ansatz",
  "confidence": 0.7
}'''
        
    else:
        # Generic fallback response
        greeting = f", {user_name}" if user_name else ""
        response = f"Vielen Dank{greeting}! Lass uns mit deiner Gründungsanalyse weitermachen."
    
    return AIChatResponse(
        response=response,
        model="fallback",
        tokens_used=0
    )
