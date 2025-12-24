# 🚀 GründerAI Workshop

AI-powered workshop for creating Gründungszuschuss-compliant business plans.

## 🎯 What is this?

An AI assistant that guides German entrepreneurs through creating a complete business plan for the Gründungszuschuss (startup grant) application. Instead of hiring expensive consultants (€500-2000), users get a professional business plan in ~2.5 hours for €149.

## 📋 Features

- **Free Assessment**: 5-minute GZ-Readiness check (score 0-100)
- **6-Module Workshop**: Guided business plan creation
- **AI-Generated Outputs**: Professional German business plan chapters
- **Document Export**: PDF, DOCX, and Excel financial plan
- **GZ-Compliant**: Aligned with BA GZ 04 form requirements

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (React)                       │
│  - Workshop Flow                                            │
│  - Question Components                                      │
│  - PayPal Integration                                       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend (FastAPI)                        │
│  - Session Management                                       │
│  - Claude API Integration                                   │
│  - Document Generation                                      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     Claude AI (Anthropic)                   │
│  - System Prompt with GZ expertise                         │
│  - Module-specific prompts                                  │
│  - Output generation                                        │
└─────────────────────────────────────────────────────────────┘
```

## 📦 The 6 Modules

| # | Module | Time | Output |
|---|--------|------|--------|
| 1 | Geschäftsidee & Gründerprofil | 25 min | Business idea + Founder profile |
| 2 | Zielgruppe & Personas | 25 min | Target audience + Customer personas |
| 3 | Markt & Wettbewerb | 25 min | Market + Competition analysis |
| 4 | Marketing & Vertrieb | 25 min | Marketing + Sales strategy |
| 5 | Finanzplanung | 35 min | 36-month financial plan |
| 6 | Strategie & Abschluss | 25 min | SWOT + Milestones + Executive Summary |

**Total: ~2.5 hours → Complete Business Plan**

## 🛠️ Tech Stack

- **Frontend**: React + TypeScript + Tailwind CSS
- **Backend**: FastAPI (Python)
- **AI**: Claude API (Anthropic)
- **Payments**: PayPal
- **Documents**: python-docx, openpyxl, weasyprint

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Anthropic API key

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Open in Browser

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📁 Project Structure

```
gruenderai-workshop/
├── CLAUDE.md                 # Instructions for Claude Code
├── docs/                     # Strategy documents
│   ├── WORKSHOP_DESIGN_STRATEGY.md
│   ├── WORKSHOP_MODULES_3-6_SPECS.md
│   └── YC_PROMPT_REVERSE_ENGINEERING.md
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   ├── services/
│   │   ├── models/
│   │   └── prompts/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── types/
│   │   └── utils/
│   └── package.json
└── templates/                # Document templates
```

## 💡 Using with Claude Code

This project is designed to be implemented with Claude Code (VS Code extension).

1. Open the project in VS Code
2. Claude Code reads `CLAUDE.md` automatically
3. Start with: `@claude Let's implement the workshop backend`

See `CLAUDE.md` for detailed implementation instructions.

## 📄 Documentation

- **WORKSHOP_DESIGN_STRATEGY.md**: Complete architecture and module specs
- **WORKSHOP_MODULES_3-6_SPECS.md**: Detailed questions and output templates
- **YC_PROMPT_REVERSE_ENGINEERING.md**: Why the prompt design works

## 🔑 Environment Variables

```
ANTHROPIC_API_KEY=sk-ant-...
PAYPAL_CLIENT_ID=...
PAYPAL_CLIENT_SECRET=...
PAYPAL_MODE=sandbox
DATABASE_URL=sqlite:///./gruenderai.db
```

## 💰 Business Model

- **Free**: Assessment (5 questions → GZ-Readiness Score)
- **Paid €149**: Full workshop → Complete business plan
- **Comparison**: Traditional consultants charge €500-2000

## 📝 License

Proprietary - All rights reserved

## 👤 Author

PrincipAI UG - Berlin, Germany
