# 🚀 QUICK START: GründerAI Workshop mit Claude Code

## Was du hast:

Ein komplettes Starter-Paket für den GründerAI Workshop:

```
gruenderai-workshop/
├── CLAUDE.md                    ← Claude Code liest das automatisch!
├── README.md                    ← Projekt-Dokumentation
├── docs/
│   ├── WORKSHOP_DESIGN_STRATEGY.md   (1350+ Zeilen - Alle Module)
│   ├── WORKSHOP_MODULES_3-6_SPECS.md (1500+ Zeilen - Detailspecs)
│   └── YC_PROMPT_REVERSE_ENGINEERING.md
├── backend/
│   ├── app/
│   │   ├── main.py              ← FastAPI Starter
│   │   ├── services/
│   │   │   └── ai_service.py    ← Claude API Integration
│   │   └── prompts/
│   │       └── system_prompt.py ← Der Master Prompt
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── package.json
    └── src/types/workshop.types.ts
```

---

## 🔧 SCHRITT 1: Projekt Setup

### 1.1 Entpacke das ZIP

```bash
# Entpacke in deinen Projekte-Ordner
unzip gruenderai-workshop.zip -d ~/Projects/
cd ~/Projects/gruenderai-workshop
```

### 1.2 Öffne in VS Code

```bash
code .
```

---

## 🤖 SCHRITT 2: Claude Code Extension

### 2.1 Installiere Claude Code (falls nicht vorhanden)

1. Öffne VS Code
2. Gehe zu Extensions (Ctrl+Shift+X)
3. Suche "Claude" von Anthropic
4. Installieren

### 2.2 Authentifiziere

1. Klicke auf das Claude Icon in der Sidebar
2. Folge den Anweisungen zur Anmeldung

---

## 🎯 SCHRITT 3: Erste Befehle an Claude Code

### Claude Code liest automatisch die CLAUDE.md!

Öffne den Claude Code Chat (Ctrl+Shift+P → "Claude: Open Chat") und starte mit:

### Befehl 1: Backend Setup

```
@claude I'm building the GründerAI Workshop. 
Read CLAUDE.md and docs/WORKSHOP_DESIGN_STRATEGY.md first.

Then set up the complete FastAPI backend:
1. Create the workshop router with all endpoints
2. Create the assessment router  
3. Set up proper session management
4. Connect the AI service to the routes

Start with the workshop router.
```

### Befehl 2: Module 1 Implementation

```
@claude Now implement Module 1 (Geschäftsidee & Gründerprofil).

Read the detailed specs in docs/WORKSHOP_DESIGN_STRATEGY.md (search for "MODUL 1").

Create:
1. The 6 questions as defined
2. The conditional logic (Frage 2b nur wenn D/E)
3. The output generation for chapters 2.1 and 3.1-3.5
4. The validation checklist
```

### Befehl 3: Frontend Workshop Flow

```
@claude Create the React frontend for the workshop flow.

Read CLAUDE.md for the structure.

Create:
1. WorkshopContainer.tsx - Main wrapper with state
2. ModuleProgress.tsx - Shows module progress
3. QuestionCard.tsx - Renders one question
4. MultipleChoice.tsx - For A/B/C/D/E questions
5. TextInput.tsx - For text questions with char limit

Use Tailwind CSS for styling.
```

---

## 📋 EMPFOHLENE REIHENFOLGE

### Tag 1: Backend Foundation
```
1. Workshop Router
2. Assessment Router  
3. Session Management
4. AI Service Routes
```

### Tag 2-3: Module Implementation
```
1. Module 1 (Geschäftsidee)
2. Module 2 (Zielgruppe)
3. Module 3 (Markt)
4. Module 4 (Marketing)
5. Module 5 (Finanzen)
6. Module 6 (Strategie)
```

### Tag 4: Output Generation
```
1. DOCX Generation
2. Excel Generation
3. PDF Export
4. Executive Summary
```

### Tag 5: Frontend
```
1. Workshop Components
2. Question Components
3. Progress Tracking
4. PayPal Integration
```

### Tag 6: Polish
```
1. End-to-End Testing
2. Error Handling
3. Mobile Responsive
```

---

## ⚙️ BACKEND STARTEN

```bash
cd backend

# Virtuelle Umgebung erstellen
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependencies installieren
pip install -r requirements.txt

# .env erstellen
cp .env.example .env
# Bearbeite .env und füge deinen ANTHROPIC_API_KEY ein

# Server starten
uvicorn app.main:app --reload
```

**API läuft auf:** http://localhost:8000
**Docs:** http://localhost:8000/docs

---

## ⚙️ FRONTEND STARTEN

```bash
cd frontend

# Dependencies installieren
npm install

# Dev Server starten
npm run dev
```

**Frontend läuft auf:** http://localhost:5173

---

## 🔑 WICHTIGE ENV VARS

Erstelle `backend/.env`:

```env
ANTHROPIC_API_KEY=sk-ant-api03-dein-key-hier

# Für später (PayPal)
PAYPAL_CLIENT_ID=dein-paypal-client-id
PAYPAL_CLIENT_SECRET=dein-paypal-secret
PAYPAL_MODE=sandbox
```

---

## 💡 TIPPS FÜR CLAUDE CODE

### Kontext geben
```
@claude Read docs/WORKSHOP_DESIGN_STRATEGY.md section "MODUL 3" 
and implement the market analysis questions.
```

### Spezifisch sein
```
@claude In backend/app/services/ai_service.py, add a method 
generate_financial_plan() that creates the Excel output for Module 5.
```

### Bei Fehlern
```
@claude I'm getting this error: [error message]
The relevant code is in backend/app/routers/workshop.py
How do I fix it?
```

### Iterativ arbeiten
```
# Erst implementieren
@claude Implement the basic workshop router

# Dann testen
@claude Add unit tests for the workshop router

# Dann verbessern
@claude Add error handling to the workshop router
```

---

## ✅ CHECKLISTE

- [ ] ZIP entpackt
- [ ] VS Code geöffnet
- [ ] Claude Code Extension installiert
- [ ] ANTHROPIC_API_KEY in .env
- [ ] Backend startet ohne Fehler
- [ ] Frontend startet ohne Fehler
- [ ] Erster Claude Code Befehl funktioniert

---

## 🆘 HILFE

### Claude Code antwortet nicht?
1. Prüfe ob Extension aktiv ist
2. Prüfe Authentifizierung
3. Starte VS Code neu

### Backend startet nicht?
1. Prüfe Python Version (3.11+)
2. Prüfe virtuelle Umgebung aktiviert
3. Prüfe alle Dependencies installiert

### Import Errors?
```bash
# Prüfe ob alle __init__.py existieren
ls backend/app/*/__init__.py
```

---

**Viel Erfolg! 🚀**
