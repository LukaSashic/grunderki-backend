# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GründerKI Backend is a Python FastAPI application that powers an AI-driven Businessplan Generator with German Gründungszuschuss (GZ) compliance checking. The system helps entrepreneurs create legally compliant business plans for applying to the German startup subsidy program.

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
# or
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Run tests
pytest
pytest test_businessplan.py -v
pytest test_scenarios.py -v
pytest test_ai_scenario_v2.py -v

# Run a specific test
pytest test_businessplan.py::test_function_name -v
```

## Architecture

### Core Components

**FastAPI Application** (`main.py`):
- Central entry point that imports and includes routers from separate modules
- Routers are loaded with try/except to allow partial functionality if a module fails
- CORS configured for frontend integration (localhost:3000/5173, Vercel deployments)

**Routers**:
- `business_context_routes.py` - Day 1: Business context capture
- `scenario_routes.py` - Day 2: Personality scenario assessment
- `results_routes.py` - Day 3: Results visualization
- `ai_routes.py` - Claude chat integration
- `ai_scenario_routes.py` - AI-powered scenario assessment
- `businessplan_api.py` - Businessplan generation endpoints

**AI Integration** (`ai_scenario_generator_v2.py`):
- Uses Anthropic Claude API with prompt caching for cost optimization
- Implements Howard's 7 entrepreneurial personality dimensions
- Generates personalized business scenarios based on business type
- Uses IRT (Item Response Theory) for adaptive assessment

**Legal Citations System** (`legal_citations.py`):
- Contains German legal references (SGB III § 93, § 94, etc.)
- Validates GZ requirements (minimum 15h/week, part-time rules)
- Provides citations for DOCX document generation

**Database** (`database.py`, `models.py`):
- SQLAlchemy with PostgreSQL (Railway deployment)
- Models: User, UserIntake, AssessmentSession, ItemResponse, PersonalityScore, IRTItemBank

### Key Business Logic

**Personality Dimensions** (Howard's 7):
1. Innovativeness (Innovationsfreude)
2. Risk-taking (Risikobereitschaft)
3. Achievement orientation (Leistungsorientierung)
4. Autonomy orientation (Autonomieorientierung)
5. Proactiveness (Proaktivität)
6. Locus of control (Kontrollüberzeugung)
7. Self-efficacy (Selbstwirksamkeit)

**Business Types**: restaurant, consulting, ecommerce, saas, services, creative, health

**GZ Compliance Rules**:
- Hauptberuflich requires minimum 15 hours/week
- Part-time work allowed if <15h/week and <50% of total income
- Financial viability must be demonstrated via Finanzplan

## Environment Variables

- `ANTHROPIC_API_KEY` - Required for AI scenario generation
- `DATABASE_URL` - PostgreSQL connection string (Railway auto-sets this)

## API Structure

All endpoints use `/api/v1/` prefix. Key endpoint groups:
- `/api/v1/assessment/business-context/*` - Business context capture
- `/api/v1/assessment/*` - Personality assessment flow
- `/api/v1/results/*` - Results and gap analysis
- `/api/v1/ai/*` - AI chat integration
- `/api/businessplan/enhanced` - Generate GZ-compliant businessplan

## Testing

Tests use `pytest-asyncio` for async endpoint testing. Test files:
- `test_businessplan.py` - Businessplan generation
- `test_business_context.py` - Business context validation
- `test_scenarios.py` - Scenario generation
- `test_ai_scenario_v2.py` - AI scenario generator v2
- `test_results.py` - Results generation
