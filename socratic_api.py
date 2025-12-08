# socratic_api.py
"""
API endpoints for Socratic dialogue and real-time research
Add these to your main.py
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Optional
import uuid
from datetime import datetime

from database import get_db
from socratic_engine import SocraticEngine
from research_engine import ResearchEngine

# Create router
router = APIRouter(prefix="/api/v1/socratic", tags=["socratic"])

# Initialize engines
socratic_engine = SocraticEngine()


# Pydantic models
class SocraticStartRequest(BaseModel):
    user_id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None


class SocraticMessageRequest(BaseModel):
    session_id: str
    message: str


class SocraticConfirmRequest(BaseModel):
    session_id: str
    confirmed: bool
    adjustments: Optional[str] = None


# Endpoints
@router.post("/start")
async def start_socratic_session(
    request: SocraticStartRequest,
    db: Session = Depends(get_db)
):
    """
    Start a new Socratic dialogue session
    Returns session ID and opening message
    """
    
    try:
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # Get opening message
        opening_message = socratic_engine.get_opening_message()
        
        # Store in database (you'll need to create SocraticConversation model)
        # For now, return the data
        
        conversation_history = [{
            "role": "assistant",
            "text": opening_message,
            "timestamp": datetime.utcnow().isoformat()
        }]
        
        return {
            "success": True,
            "session_id": session_id,
            "opening_message": opening_message,
            "conversation_history": conversation_history,
            "context": {
                "confidence": 0,
                "message_count": 0
            }
        }
        
    except Exception as e:
        print(f"Error starting Socratic session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/message")
async def process_socratic_message(
    request: SocraticMessageRequest,
    db: Session = Depends(get_db)
):
    """
    Process a user message in Socratic dialogue
    Returns next question or summary
    
    Also triggers real-time research in background
    """
    
    try:
        # In production, load conversation from database
        # For now, this is a simplified version
        
        # TODO: Load from database
        # session = db.query(SocraticConversation).filter_by(
        #     session_id=request.session_id
        # ).first()
        
        # For MVP, we'll need to pass conversation history from frontend
        # This is a simplified approach
        
        conversation_history = []  # Load from DB or session storage
        current_context = {}  # Load from DB or session storage
        
        # Process message with Socratic engine
        result = await socratic_engine.process_message(
            user_message=request.message,
            conversation_history=conversation_history,
            current_context=current_context
        )
        
        # Trigger research in background (non-blocking)
        research_task = None
        if not result.get("sufficient"):
            # Only research if we're still gathering info
            # TODO: Implement research engine integration
            pass
        
        return {
            "success": True,
            "session_id": request.session_id,
            **result
        }
        
    except Exception as e:
        print(f"Error processing message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/confirm")
async def confirm_business_idea(
    request: SocraticConfirmRequest,
    db: Session = Depends(get_db)
):
    """
    User confirms or adjusts the business idea summary
    """
    
    try:
        if request.confirmed:
            # Mark session as complete
            # Save final context to database
            # Proceed to next stage
            
            return {
                "success": True,
                "message": "Business idea confirmed!",
                "next_step": "context_questions"
            }
        else:
            # User wants adjustments
            # Continue conversation with adjustment request
            
            adjustment_question = f"Was möchtest du anpassen? {request.adjustments or ''}"
            
            return {
                "success": True,
                "question": adjustment_question,
                "sufficient": False
            }
            
    except Exception as e:
        print(f"Error confirming: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/research/{session_id}")
async def get_research_insights(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Get real-time research insights for a session
    Used by Live Insights Sidebar
    """
    
    try:
        # TODO: Load research results from cache/database
        # For now, return empty
        
        return {
            "success": True,
            "insights": [],
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        print(f"Error fetching research: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Add this router to your main.py:
# from socratic_api import router as socratic_router
# app.include_router(socratic_router)
