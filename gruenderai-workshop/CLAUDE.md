# CLAUDE.md - GründerAI Workshop Implementation

## PROJECT OVERVIEW

Building an AI-powered workshop that creates GZ-compliant business plans.
The workshop consists of 6 modules that guide users through business plan creation
using bounded questions (not endless Socratic loops).

## ARCHITECTURE

### Three Layers:
1. **System Prompt Layer** - Master AI instructions
2. **Module Prompt Layer** - Per-module AI logic  
3. **User Context Layer** - State management

### Tech Stack:
- Frontend: React + TypeScript + Tailwind CSS
- Backend: FastAPI (Python)
- AI: Claude API (Anthropic)
- Payments: PayPal
- Documents: python-docx, openpyxl, weasyprint

## BUSINESS MODEL

- **FREE**: Initial Assessment (5 questions → GZ-Readiness Score)
- **PAID (€149)**: Full 6-Module Workshop → Complete Business Plan

## KEY DESIGN PRINCIPLES

### Anti-Loop Rules (CRITICAL!)
1. Maximum 5-7 questions per module
2. 70% Multiple Choice, 30% limited text input
3. Maximum 1 follow-up question, then AI generates best-effort
4. Clear output per module (business plan chapter)
5. Always forward momentum - no loops back
6. AI generates even with imperfect answers

### Module Structure Pattern
Each module follows:
```
INPUT PHASE (60%):    5-7 bounded questions
TEACHING PHASE (20%): Framework explanation  
OUTPUT PHASE (15%):   Business plan chapter generation
VALIDATION (5%):      GZ checklist + score
```

## THE 6 MODULES

| # | Module | Time | Questions | Output |
|---|--------|------|-----------|--------|
| 1 | Geschäftsidee & Gründerprofil | 25 min | 6 | Ch. 2.1, 3.1-3.5 |
| 2 | Zielgruppe & Personas | 25 min | 6 | Ch. 2.2, 2.3 |
| 3 | Markt & Wettbewerb | 25 min | 6 | Ch. 3.6, 4.1, 4.2 |
| 4 | Marketing & Vertrieb | 25 min | 6 | Ch. 5.1-5.3 |
| 5 | Finanzplanung | 35 min | 7 | Ch. 6.1-6.4 + Excel |
| 6 | Strategie & Abschluss | 25 min | 6 | Ch. 7, 8, 9 + Summary |

## IMPLEMENTATION PRIORITIES

### Phase 1: Core Infrastructure
1. Set up FastAPI backend with Claude API integration
2. Create system prompt handler
3. Implement session/state management
4. Build basic React workshop flow

### Phase 2: Module Implementation  
1. Module 1: Geschäftsidee & Gründerprofil
2. Module 2: Zielgruppe & Personas
3. Module 3: Markt & Wettbewerb
4. Module 4: Marketing & Vertrieb
5. Module 5: Finanzplanung
6. Module 6: Strategie & Abschluss

### Phase 3: Output Generation
1. Business plan document (DOCX)
2. Financial plan (XLSX with formulas)
3. PDF export
4. Executive Summary auto-generation

### Phase 4: Payment Integration
1. PayPal integration
2. Paywall after free assessment
3. Access management

## FILE REFERENCES

Strategy documents in /docs/:
- WORKSHOP_DESIGN_STRATEGY.md - Complete workshop architecture (1350+ lines)
- WORKSHOP_MODULES_3-6_SPECS.md - Detailed module specifications (1500+ lines)
- YC_PROMPT_REVERSE_ENGINEERING.md - Prompt design rationale

## COMMANDS

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend  
cd frontend
npm install
npm run dev
```

## API ENDPOINTS

```
POST /api/assessment/start     - Start free assessment
POST /api/assessment/submit    - Submit assessment answers
GET  /api/assessment/result    - Get GZ-Readiness score

POST /api/workshop/start       - Start paid workshop (after payment)
POST /api/workshop/module/{n}  - Submit module answers
GET  /api/workshop/output/{n}  - Get module output
POST /api/workshop/complete    - Generate final documents

POST /api/payment/create       - Create PayPal order
POST /api/payment/capture      - Capture PayPal payment
```

## ENVIRONMENT VARIABLES

```
ANTHROPIC_API_KEY=your_key_here
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_CLIENT_SECRET=your_paypal_secret
PAYPAL_MODE=sandbox  # or 'live'
DATABASE_URL=postgresql://...
```

## IMPORTANT NOTES

1. All prompts are in German (target market: Germany)
2. Business plan must comply with BA GZ 04 form requirements
3. Questions 8, 9, 15 of BA GZ 04 are CRITICAL (most rejections happen there)
4. The "fachkundige Stelle" (expert institution) reviews the plan
5. Price: €149 for complete workshop (cheaper than consultants €500-2000)

## BA GZ 04 QUESTION MAPPING

The Gründungszuschuss application form (BA GZ 04) has specific questions our business plan must answer:

- **Frage 7**: Beschreibung des Gründungsvorhabens → Module 1
- **Frage 8**: Fachliche Kenntnisse → Module 1 (CRITICAL - 65% rejections!)
- **Frage 9**: Kaufmännische Kenntnisse → Module 1
- **Frage 10**: Zielgruppe & Kundennutzen → Module 2
- **Frage 11**: Markt & Wettbewerb → Module 3
- **Frage 12**: Marketing & Vertrieb → Module 4
- **Frage 13**: Umsatz/Gewinn-Erwartung → Module 5
- **Frage 14**: Kapitalbedarf → Module 5
- **Frage 15**: Lebensunterhalt → Module 5 (CRITICAL!)

## DEVELOPMENT WORKFLOW

1. Read relevant docs before implementing
2. Implement one module at a time
3. Test with sample data
4. Generate outputs and validate
5. Move to next module

## GETTING STARTED

To begin implementation, start with:

```
@claude Read docs/WORKSHOP_DESIGN_STRATEGY.md and set up the basic 
FastAPI backend structure with Claude API integration.
```
