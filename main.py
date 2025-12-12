"""
GründerAI Backend - Complete with Legal Citations System
ENHANCED VERSION - Business Context + Personality Scenarios + Results Visualization
Version: 3.0.0
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import logging
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

# Load environment
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="GründerAI Backend API",
    version="3.0.0",
    description="Backend with Business Context, Personality Scenarios, Results Visualization, Legal Citations for GZ-compliant Businessplans",
)

# ============================================================================
# IMPORT AND INCLUDE ROUTERS
# ============================================================================

# Day 1: Business Context Router
try:
    from business_context_routes import router as business_context_router
    app.include_router(business_context_router)
    logger.info("✅ Business Context routes loaded")
except ImportError as e:
    logger.warning(f"⚠️ Business Context routes not loaded: {e}")

# Day 2: Personality Scenarios Router
try:
    from scenario_routes import router as scenario_router
    app.include_router(scenario_router)
    logger.info("✅ Personality Scenario routes loaded")
except ImportError as e:
    logger.warning(f"⚠️ Personality Scenario routes not loaded: {e}")

# Day 3: Results Visualization Router (NEW!)
try:
    from results_routes import router as results_router
    app.include_router(results_router)
    logger.info("✅ Results Visualization routes loaded")
except ImportError as e:
    logger.warning(f"⚠️ Results Visualization routes not loaded: {e}")

# AI Routes (Claude Chat Integration)
try:
    from ai_routes import router as ai_router
    app.include_router(ai_router)
    logger.info("✅ AI routes loaded")
except ImportError as e:
    logger.warning(f"⚠️ AI routes not loaded: {e}")

# ============================================================================
# CORS - Allow frontend origins
# ============================================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://grunderai.vercel.app",
        "https://gruenderai.vercel.app",
        "*",  # For development - restrict in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# MODELS
# ============================================================================


class EnhancedBusinessplanRequest(BaseModel):
    """Enhanced businessplan request with legal citations"""

    # Basic Info
    name: str
    email: Optional[str] = None
    business_idea: str

    # Business Details
    industry: Optional[str] = "dienstleistung"
    target_market: Optional[str] = None

    # Experience
    experience_level: Optional[str] = "junior"
    years_experience: Optional[int] = 0
    previous_self_employment: Optional[bool] = False

    # Network
    network_strength: Optional[str] = "medium"
    first_customers_pipeline: Optional[int] = 0

    # Financial (REQUIRED for GZ compliance)
    hours_per_week_available: int = 20
    startup_capital: float = 10000
    monthly_living_costs: float = 2000
    partner_income_monthly: Optional[float] = 0

    # Part-time (optional)
    part_time_job_possible: Optional[bool] = False
    part_time_hours_per_week: Optional[int] = 0
    part_time_income_monthly: Optional[float] = 0


# ============================================================================
# ENDPOINTS
# ============================================================================


@app.get("/")
async def root():
    """Root endpoint - Service info"""
    return {
        "service": "GründerAI Backend API",
        "version": "3.0.0",
        "status": "running",
        "features": [
            "Business Context Capture (Day 1)",
            "Personality Scenarios (Day 2)",
            "Results Visualization (Day 3 - NEW!)",
            "AI Chat Integration (Claude)",
            "Legal Citations (18+ official sources)",
            "GZ Compliance Checking",
            "Enhanced Businessplan Generator",
        ],
        "endpoints": {
            "business_context": {
                "start": "POST /api/v1/assessment/business-context/start",
                "answer": "POST /api/v1/assessment/business-context/answer",
                "progress": "GET /api/v1/assessment/business-context/progress/{session_id}",
                "complete": "POST /api/v1/assessment/business-context/complete",
            },
            "personality_scenarios": {
                "start": "POST /api/v1/assessment/start",
                "respond": "POST /api/v1/assessment/{session_id}/respond",
                "scenario": "GET /api/v1/assessment/{session_id}/scenario",
                "results": "GET /api/v1/assessment/{session_id}/results",
                "status": "GET /api/v1/assessment/{session_id}/status",
            },
            "results_visualization": {
                "generate": "POST /api/v1/results/generate",
                "get": "GET /api/v1/results/{session_id}",
                "profile": "GET /api/v1/results/{session_id}/profile",
                "gaps": "GET /api/v1/results/{session_id}/gaps",
                "radar": "GET /api/v1/results/{session_id}/radar",
                "track": "POST /api/v1/results/{session_id}/track",
            },
            "businessplan": "POST /api/businessplan/enhanced",
            "citations": "GET /api/citations",
            "health": "GET /api/health",
            "ai": {
                "chat": "POST /api/v1/ai/chat",
                "intake": "POST /api/v1/intake",
                "health": "GET /api/v1/ai/health",
            },
        },
    }


@app.get("/api/health")
async def health():
    """Health check endpoint"""
    api_key_set = bool(os.getenv("ANTHROPIC_API_KEY"))
    return {
        "status": "ok",
        "version": "3.0.0",
        "api_key_set": api_key_set,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "components": {
            "business_context": "operational",
            "personality_scenarios": "operational",
            "results_visualization": "operational",
            "legal_citations": "operational",
        }
    }


@app.post("/api/businessplan/enhanced")
async def generate_enhanced_businessplan(request: EnhancedBusinessplanRequest):
    """
    Generate GZ-compliant businessplan with legal citations

    Features:
    ✅ Legal citations (SGB III § 93, Fachliche Weisungen BA)
    ✅ Input validation (hours ≥15, part-time rules, capital)
    ✅ Compliance checking with rechtsgrundlage
    ✅ Enhanced prompts with official sources

    Returns:
    - businessplan: Complete businessplan sections
    - compliance_score: 0-100 GZ compliance score
    - legal_citations: List of citations used
    - validations: Validation results with legal basis
    - gz_compliant: Boolean compliance status
    """
    try:
        logger.info("=" * 70)
        logger.info(f"📝 Generating enhanced businessplan for: {request.name}")
        logger.info(f"   Business: {request.business_idea}")
        logger.info(f"   Hours/week: {request.hours_per_week_available}")
        logger.info(f"   Capital: €{request.startup_capital:,.2f}")
        logger.info("=" * 70)

        # Import generator (lazy import to avoid startup issues)
        from businessplan_generator_enhanced import EnhancedBusinessplanGenerator

        # Initialize generator
        generator = EnhancedBusinessplanGenerator()

        # Convert request to dict
        profile = request.dict()

        # Generate using wrapper method
        result = await generator.generate_from_simple_profile(profile)

        # ===================================================================
        # EXTRACT RESULTS FROM CORRECT KEYS - FIXED!
        # ===================================================================

        # Extract compliance data from gz_compliance dict
        gz_compliance_data = result.get("gz_compliance", {})
        compliance_score = gz_compliance_data.get("total_score", 0)
        gz_compliant = compliance_score >= 70

        # Extract legal citations from legal_basis
        legal_basis_dict = gz_compliance_data.get("legal_basis", {})
        legal_citations = [
            {
                "category": cat,
                "format": info.get("rechtsgrundlage", ""),
                "short_text": info.get("anforderung", ""),
                "source": info.get("quelle", ""),
            }
            for cat, info in legal_basis_dict.items()
        ]

        # Build businessplan dict from individual sections
        businessplan = {
            "executive_summary": result.get("executive_summary", ""),
            "geschaeftsidee": result.get("geschaeftsidee", ""),
            "gruenderperson": result.get("gruenderperson", ""),
            "markt_wettbewerb": result.get("markt_wettbewerb", ""),
            "marketing_vertrieb": result.get("marketing_vertrieb", ""),
            "organisation": result.get("organisation", ""),
            "finanzplan": result.get("finanzplan", {}),
            "risikomanagement": result.get("risikomanagement", ""),
            "meilensteine": result.get("meilensteine", ""),
            "swot": result.get("swot_data", {}),
            "meta": result.get("meta", {}),
        }

        # Extract validations
        validations = result.get("living_validation", {})

        logger.info("=" * 70)
        logger.info(f"✅ Businessplan generated successfully!")
        logger.info(f"   Compliance Score: {compliance_score}/100")
        logger.info(f"   Legal Citations: {len(legal_citations)}")
        logger.info(f"   GZ Compliant: {gz_compliant}")
        logger.info("=" * 70)

        # Return result
        return {
            "success": True,
            "businessplan": businessplan,
            "compliance_score": compliance_score,
            "legal_citations": legal_citations,
            "validations": validations,
            "gz_compliant": gz_compliant,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "metadata": {
                "generator_version": "enhanced_with_legal_citations",
                "citations_count": len(legal_citations),
                "validation_passed": gz_compliant,
                "sections_generated": list(businessplan.keys()),
            },
        }

    except ValueError as e:
        # Validation errors
        error_msg = str(e)
        logger.error(f"❌ Validation error: {error_msg}")
        raise HTTPException(
            status_code=422,
            detail={
                "error": "Validation failed",
                "message": error_msg,
                "type": "validation_error",
            },
        )

    except Exception as e:
        # Other errors
        error_msg = str(e)
        logger.error(f"❌ Error generating businessplan: {error_msg}")
        logger.exception("Full traceback:")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Generation failed",
                "message": error_msg,
                "type": "generation_error",
            },
        )


@app.get("/api/citations")
async def list_citations():
    """
    List all available legal citations

    Returns all 18+ official legal citations used for GZ compliance
    """
    try:
        from legal_citations import LEGAL_CITATIONS, get_citation

        citations = []
        for key in LEGAL_CITATIONS.keys():
            citation = get_citation(key)
            if citation:
                citations.append(
                    {
                        "key": key,
                        "format": citation.format(),
                        "short_text": citation.short_text,
                        "category": citation.category,
                        "official_source": citation.official_source,
                    }
                )

        return {
            "total": len(citations),
            "citations": citations,
            "categories": list(set(c["category"] for c in citations)),
        }

    except Exception as e:
        logger.error(f"Error listing citations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/citations/{citation_key}")
async def get_citation_detail(citation_key: str):
    """Get detailed information about a specific legal citation"""
    try:
        from legal_citations import get_citation

        citation = get_citation(citation_key)
        if not citation:
            raise HTTPException(
                status_code=404, detail=f"Citation '{citation_key}' not found"
            )

        return {
            "key": citation_key,
            "format": citation.format(),
            "short_text": citation.short_text,
            "full_text": citation.full_text,
            "category": citation.category,
            "official_source": citation.official_source,
            "applies_to": citation.applies_to,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting citation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# STARTUP
# ============================================================================


@app.on_event("startup")
async def startup_event():
    """Startup event"""
    logger.info("=" * 70)
    logger.info("🚀 GründerAI Backend Starting...")
    logger.info("")
    logger.info("📋 Business Context Capture: Available")
    logger.info("🧠 Personality Scenarios: Available")
    logger.info("📊 Results Visualization: Available (NEW!)")
    logger.info("📝 Enhanced Generator: Available")
    logger.info("🏛️  Legal Citations: 18+ official sources")
    logger.info("✅ Input Validations: Enabled")
    logger.info(
        f"🔑 API Key: {'✓ Set' if os.getenv('ANTHROPIC_API_KEY') else '✗ NOT SET'}"
    )
    logger.info("")
    logger.info("Day 1 Endpoints (Business Context):")
    logger.info("  POST /api/v1/assessment/business-context/start")
    logger.info("  POST /api/v1/assessment/business-context/answer")
    logger.info("  GET  /api/v1/assessment/business-context/progress/{id}")
    logger.info("  POST /api/v1/assessment/business-context/complete")
    logger.info("")
    logger.info("Day 2 Endpoints (Personality Scenarios):")
    logger.info("  POST /api/v1/assessment/start")
    logger.info("  POST /api/v1/assessment/{id}/business-context")
    logger.info("  GET  /api/v1/assessment/{id}/scenario")
    logger.info("  POST /api/v1/assessment/{id}/respond")
    logger.info("  GET  /api/v1/assessment/{id}/results")
    logger.info("")
    logger.info("Frontend Compatibility Endpoints:")
    logger.info("  GET  /api/v1/assessment/{id}/next")
    logger.info("  POST /api/v1/assessment/respond")
    logger.info("")
    logger.info("Day 3 Endpoints (Results Visualization):")
    logger.info("  POST /api/v1/results/generate")
    logger.info("  GET  /api/v1/results/{id}")
    logger.info("  GET  /api/v1/results/{id}/profile")
    logger.info("  GET  /api/v1/results/{id}/gaps")
    logger.info("  GET  /api/v1/results/{id}/radar")
    logger.info("  POST /api/v1/results/{id}/track")
    logger.info("")
    logger.info("Other Endpoints:")
    logger.info("  POST /api/businessplan/enhanced")
    logger.info("  GET  /api/citations")
    logger.info("  GET  /api/health")
    logger.info("")
    logger.info("AI Endpoints:")
    logger.info("  POST /api/v1/ai/chat")
    logger.info("  POST /api/v1/intake")
    logger.info("  GET  /api/v1/ai/health")
    logger.info("=" * 70)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    logger.info("Starting Uvicorn server...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False, log_level="info")
