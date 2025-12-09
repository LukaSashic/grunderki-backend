# vision_discovery_api.py
"""
API Routes for Vision Discovery Engine
Endpoints: /start, /message
"""
import os
from dotenv import load_dotenv

load_dotenv()
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
import uuid
import logging

from vision_discovery_engine import VisionDiscoveryEngine

logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter(prefix="/api/v1/vision", tags=["vision-discovery"])

# Initialize engine
try:
    vision_engine = VisionDiscoveryEngine()
    logger.info("✅ Vision Discovery Engine initialized for API")
except Exception as e:
    logger.error(f"❌ Failed to initialize Vision Discovery Engine: {e}")
    vision_engine = None


# Pydantic models
class StartSessionRequest(BaseModel):
    """Request to start new vision discovery session"""

    user_name: Optional[str] = None
    user_email: Optional[str] = None


class StartSessionResponse(BaseModel):
    """Response with session ID and opening message"""

    success: bool
    session_id: str
    opening_message: str
    phase: str
    conversation_history: List[Dict]
    context: Dict


class MessageRequest(BaseModel):
    """Request to send message in session"""

    session_id: str
    user_message: str
    conversation_history: List[Dict]
    context: Dict


class MessageResponse(BaseModel):
    """Response with AI message and updated context"""

    success: bool
    message: str
    response_type: str
    phase: str
    conversation_history: List[Dict]
    context: Dict
    extracted_fields: Dict
    depth_score: Optional[int] = 0
    gz_readiness_score: Optional[int] = 0
    red_flags: Optional[List[str]] = []


# In-memory session storage (replace with Redis/DB in production)
sessions = {}


@router.post("/start", response_model=StartSessionResponse)
async def start_vision_session(request: StartSessionRequest):
    """
    Start a new vision discovery session

    Returns opening message for Phase 1: Vision Excavation
    """

    if not vision_engine:
        raise HTTPException(
            status_code=503, detail="Vision Discovery Engine not available"
        )

    try:
        # Generate session ID
        session_id = str(uuid.uuid4())

        # Initialize context
        context = {
            "session_id": session_id,
            "phase": "vision",
            "phase_message_count": 0,
            "user_name": request.user_name,
            "user_email": request.user_email,
            "started_at": datetime.now().isoformat(),
            "depth_score": 0,
            "gz_readiness_score": 0,
        }

        # Opening message for Vision Excavation Phase
        opening_message = """Hallo! 👋

Ich bin dein Vision Coach und begleite dich auf einer spannenden Reise zu deiner wahren Geschäftsidee.

**Wir gehen in 3 Schritten vor:**

1️⃣ **Vision Excavation** - Wir entdecken deine WAHRE Vision (nicht nur die Business-Idee!)

2️⃣ **JTBD Validation** - Wir finden heraus, welchen Job deine Kunden wirklich erledigen wollen

3️⃣ **GZ Optimization** - Wir machen deine Idee Gründungszuschuss-konform

**Lass uns starten mit etwas Wichtigem:**

Stell dir vor, Geld wäre überhaupt kein Problem mehr. Du hättest alle finanziellen Ressourcen der Welt zur Verfügung.

**Was würdest du dann tun? Was würdest du in die Welt bringen?**

Nimm dir einen Moment zum Nachdenken... 💭"""

        # Initialize conversation history
        conversation_history = [
            {
                "role": "assistant",
                "text": opening_message,
                "timestamp": datetime.now().isoformat(),
                "response_type": "vision_question",
            }
        ]

        # Store session
        sessions[session_id] = {
            "context": context,
            "conversation_history": conversation_history,
            "created_at": datetime.now().isoformat(),
        }

        logger.info(f"✅ Vision session started: {session_id}")

        return StartSessionResponse(
            success=True,
            session_id=session_id,
            opening_message=opening_message,
            phase="vision",
            conversation_history=conversation_history,
            context=context,
        )

    except Exception as e:
        logger.error(f"❌ Error starting vision session: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to start session: {str(e)}"
        )


@router.post("/message", response_model=MessageResponse)
async def send_message(request: MessageRequest):
    """
    Send message in vision discovery session

    Processes user message and returns AI response with phase-aware logic
    """

    if not vision_engine:
        raise HTTPException(
            status_code=503, detail="Vision Discovery Engine not available"
        )

    try:
        # Get session (or use provided context)
        session_data = sessions.get(request.session_id)

        if not session_data:
            # Use provided context if session not found
            logger.warning(
                f"Session {request.session_id} not in memory, using provided context"
            )
            context = request.context
            conversation_history = request.conversation_history
        else:
            context = session_data["context"]
            conversation_history = session_data["conversation_history"]

        # Add user message to history
        user_message_entry = {
            "role": "user",
            "text": request.user_message,
            "timestamp": datetime.now().isoformat(),
        }
        conversation_history.append(user_message_entry)

        # Process with Vision Discovery Engine
        logger.info(f"🔄 Processing message in phase: {context.get('phase')}")

        response = await vision_engine.process_message(
            user_message=request.user_message,
            conversation_history=conversation_history,
            current_context=context,
        )

        # Parse message if it's JSON string (from AI)
        ai_message = response["message"]
        try:
            # Try to parse if message is JSON
            import json

            parsed_msg = json.loads(ai_message)
            ai_message = parsed_msg.get("message", ai_message)
            # Update response with parsed values
            response["response_type"] = parsed_msg.get(
                "response_type", response.get("response_type")
            )
            response["depth_score"] = parsed_msg.get(
                "depth_score", response.get("depth_score", 0)
            )
            response["extracted_fields"] = parsed_msg.get(
                "extracted_fields", response.get("extracted_fields", {})
            )
        except (json.JSONDecodeError, TypeError):
            # Not JSON, use as-is
            pass

        # Add AI response to history
        ai_message_entry = {
            "role": "assistant",
            "text": response["message"],
            "timestamp": datetime.now().isoformat(),
            "response_type": response["response_type"],
            "extracted_fields": response.get("extracted_fields", {}),
        }
        conversation_history.append(ai_message_entry)

        # Update context
        updated_context = response["context"]

        # Update session storage
        if request.session_id in sessions:
            sessions[request.session_id]["context"] = updated_context
            sessions[request.session_id]["conversation_history"] = conversation_history

        logger.info(
            f"✅ Message processed. Phase: {updated_context.get('phase')}, Fields extracted: {len(response.get('extracted_fields', {}))}"
        )

        return MessageResponse(
            success=True,
            message=response["message"],
            response_type=response["response_type"],
            phase=updated_context.get("phase", "vision"),
            conversation_history=conversation_history,
            context=updated_context,
            extracted_fields=response.get("extracted_fields", {}),
            depth_score=response.get("depth_score", 0),
            gz_readiness_score=response.get("gz_readiness_score", 0),
            red_flags=response.get("red_flags", []),
        )

    except Exception as e:
        logger.error(f"❌ Error processing message: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to process message: {str(e)}"
        )


@router.get("/session/{session_id}")
async def get_session(session_id: str):
    """Get session data"""

    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    return {"success": True, "session": sessions[session_id]}


@router.get("/health")
async def health_check():
    """Health check for vision discovery API"""
    return {
        "status": "healthy",
        "service": "vision-discovery-api",
        "engine_available": vision_engine is not None,
    }
