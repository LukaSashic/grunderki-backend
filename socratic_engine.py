# socratic_engine.py
"""
Socratic Dialogue Engine for Business Idea Discovery
✅ YC-Style Advanced Prompting + German Market Expertise
✅ Completion-Optimized (prevents infinite loops)
✅ Professional Bureaucratic Tone (Sie-Form)
"""

import json
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from anthropic import Anthropic


class SocraticEngine:
    """Manages Socratic dialogue for business idea extraction"""

    # Business context fields
    REQUIRED_FIELDS = ["what", "who", "problem"]
    GOOD_FIELDS = ["what", "who", "problem", "why_you", "revenue_source"]
    EXCELLENT_FIELDS = [
        "what",
        "who",
        "problem",
        "why_you",
        "revenue_source",
        "how",
        "capital_needs",
    ]

    # ✨ NEW: Boredom prevention
    MAX_QUESTIONS = 8  # Force summary after 8 questions

    # ✨ IMPROVED: YC-Style System Prompt with German Expertise
    SYSTEM_PROMPT = """Sie sind ein erfahrener Gründungsberater mit Spezialisierung auf den deutschen Gründungszuschuss.

=== IHRE AUFGABE ===
Führen Sie ein professionelles Beratungsgespräch, um die Geschäftsidee des Gründers zu verstehen und für den Gründungszuschuss zu optimieren.

=== GESPRÄCHSSTRATEGIE ===

**Phase 1: Kernverständnis (Fragen 1-3)**
Ziel: WAS, WER, PROBLEM klären
- Frage 1: "Was möchten Sie anbieten?" (Service/Produkt)
- Frage 2: "Für wen ist das gedacht?" (Zielgruppe) 
- Frage 3: "Welches Problem lösen Sie?" (Kundennutzen)

**Phase 2: GZ-Optimierung (Fragen 4-6)**
Ziel: Bewilligungskriterien abdecken
- Frage 4: "Warum sind Sie die richtige Person dafür?" (Qualifikation)
- Frage 5: "Wie werden Sie damit Geld verdienen?" (Ertragsmechanik)
- Frage 6: "Wie werden Sie das konkret umsetzen?" (Machbarkeit)

**Phase 3: Risiko-Check (Frage 7-8)**
Ziel: Red Flags erkennen
- Prüfen: Ist das Vollzeit-fähig? (GZ erfordert Haupterwerb)
- Prüfen: Ist das profitabel genug? (Min. €1500/Monat Gewinn)

=== AKTUELLE SITUATION ===

**Bereits erfasster Kontext:**
{context_json}

**Bisheriger Gesprächsverlauf:**
{conversation_history}

**Nachrichtenzähler:** {message_count} von max. 8 Fragen

=== ENTSCHEIDUNGSLOGIK (Denken Sie laut) ===

Schritt 1: Analysieren Sie den Kontext
- Was fehlt noch für eine GZ-Bewilligung?
- Welche Felder sind leer: {missing_fields}
- Gibt es Red Flags? (z.B. "Hobby", "Nebenerwerb", "erst mal schauen")

Schritt 2: Priorisieren Sie
- Wenn {message_count} >= 7: IMMER Zusammenfassung, auch wenn unvollständig
- Wenn REQUIRED_FIELDS vollständig: Kann zusammenfassen
- Wenn kritische Lücke: Stelle präzise Frage

Schritt 3: Formulieren Sie
- Ton: Professionell, höflich, Sie-Form
- Länge: Maximal 12 Wörter pro Frage
- Stil: Direkt, ohne Füllwörter

=== RED FLAGS (Automatisch erkennen) ===
Wenn der Nutzer sagt:
- "Hobby" / "Nebenbei" → Warnung: GZ erfordert Haupterwerb
- "Erstmal schauen" → Warnung: Benötigt tragfähiges Konzept
- "Kein Einkommen nötig" → Warnung: Min. €18.000/Jahr Gewinn erforderlich

=== OUTPUT FORMAT (NUR JSON) ===

**Bei weiterer Frage benötigt:**
```json
{{
  "type": "question",
  "question": "Ihre nächste präzise Frage (max 12 Wörter)",
  "current_extraction": {{
    "what": "extrahierter Wert oder null",
    "who": "extrahierter Wert oder null",
    "problem": "extrahierter Wert oder null",
    "why_you": "extrahierter Wert oder null",
    "revenue_source": "extrahierter Wert oder null",
    "how": "extrahierter Wert oder null",
    "capital_needs": "extrahierter Wert oder null"
  }},
  "reasoning": "Warum diese Frage jetzt wichtig ist",
  "confidence": 0-100,
  "ui_hint": "location|market_size|competitors|pricing|none"
}}
```

**Bei Red Flag erkannt:**
```json
{{
  "type": "warning",
  "warning_message": "⚠️ Der Gründungszuschuss erfordert [X]. Möchten Sie Ihre Idee anpassen?",
  "severity": "low|medium|high",
  "current_extraction": {{...}},
  "reasoning": "GZ-Kriterium verletzt"
}}
```

**Bei ausreichend Kontext:**
```json
{{
  "type": "summary",
  "summary": "Präzise 2-3 Satz Zusammenfassung der Geschäftsidee",
  "context": {{...}},
  "confidence": 0-100,
  "gz_score": {{
    "overall": 0-100,
    "strengths": ["Liste von Stärken"],
    "concerns": ["Liste von Bedenken"],
    "missing": ["Fehlende Informationen"]
  }}
}}
```

=== BENCHMARK-DATEN (Zur Orientierung) ===
{benchmark_data}

=== WICHTIG ===
- Output NUR valides JSON, keine Erklärungen drumherum
- Extrahieren Sie bei JEDER Antwort incremental alle verfügbaren Felder
- Nach 7 Fragen: Zwingend zusammenfassen (auch wenn unvollständig)
- Red Flags sofort ansprechen, nicht ignorieren
- Professionell aber zugänglich (keine Silicon-Valley-Kumpel-Sprache)
"""

    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not set!")
        if not api_key.startswith("sk-ant-"):
            raise ValueError("Invalid API key format!")

        self.client = Anthropic(api_key=api_key)

        # ✨ NEW: Load benchmark data (placeholder for now)
        self.benchmark_data = self._load_benchmark_data()

        print(f"✅ Socratic Engine initialized with YC prompting")

    def _load_benchmark_data(self) -> str:
        """Load successful GZ application benchmarks"""
        # TODO: Load from database
        # For now, return static examples
        return """
**Erfolgreiche Consulting-Gründungen (Berlin):**
- Digitalisierungs-Beratung für Restaurants: Ø €800/Tag, 10-15 Kunden im ersten Jahr
- IT-Beratung für KMUs: Ø €1200/Tag, 5-8 Projekte gleichzeitig
- HR-Consulting: Ø €600/Tag, 12-20 Kunden/Jahr

**Typische Anlaufkosten:**
- Consulting/Dienstleistung: €2000-5000 (Website, Marketing, Versicherungen)
- E-Commerce: €10000-20000 (Lager, Inventory, Shop-Setup)
- Lokale Services: €5000-15000 (Werkzeug, Fahrzeug, Lizenzen)
        """.strip()

    async def process_message(
        self, user_message: str, conversation_history: List[Dict], current_context: Dict
    ) -> Dict:
        """Process message with YC prompting and boredom prevention"""

        # Add user message
        conversation_history.append(
            {
                "role": "user",
                "text": user_message,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

        # ✨ NEW: Count user questions (boredom prevention)
        user_message_count = len(
            [m for m in conversation_history if m["role"] == "user"]
        )

        # ✨ NEW: Check if we should force summary
        force_summary = user_message_count >= self.MAX_QUESTIONS

        if force_summary:
            print(
                f"⚠️ Boredom threshold reached ({user_message_count} questions) - forcing summary"
            )

        # Calculate missing fields for prompt
        missing_fields = [f for f in self.GOOD_FIELDS if not current_context.get(f)]

        messages = self._build_messages(conversation_history)

        # Try multiple models with fallback
        models = [
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
            "claude-2.1",
        ]

        response = None
        last_error = None

        for model in models:
            try:
                print(f"🔄 Model: {model}")

                # ✨ IMPROVED: Enhanced system prompt with YC reasoning
                system_prompt = self.SYSTEM_PROMPT.format(
                    context_json=json.dumps(
                        current_context, indent=2, ensure_ascii=False
                    ),
                    conversation_history=json.dumps(
                        conversation_history[-6:], indent=2, ensure_ascii=False
                    ),
                    message_count=user_message_count,
                    missing_fields=(
                        ", ".join(missing_fields)
                        if missing_fields
                        else "Alle Felder erfasst"
                    ),
                    benchmark_data=self.benchmark_data,
                )

                # ✨ NEW: Force summary instruction if needed
                if force_summary:
                    system_prompt += "\n\n🚨 WICHTIG: Sie haben die maximale Fragenzahl erreicht. Erstellen Sie JETZT eine Zusammenfassung, auch wenn Informationen fehlen."

                response = self.client.messages.create(
                    model=model,
                    max_tokens=2000,  # Increased for reasoning
                    temperature=0.7,
                    system=system_prompt,
                    messages=messages,
                )
                print(f"✅ Success: {model}")
                break

            except Exception as e:
                last_error = e
                if "404" in str(e) or "not_found" in str(e):
                    print(f"❌ {model} not available")
                    continue
                else:
                    raise

        if response is None:
            raise Exception(f"All models failed: {last_error}")

        # Process response
        try:
            response_text = response.content[0].text.strip()
            response_text = (
                response_text.replace("```json", "").replace("```", "").strip()
            )

            print(f"📝 Raw response: {response_text[:200]}...")

            result = json.loads(response_text)

            # ✨ NEW: Handle warning type
            if result["type"] == "warning":
                conversation_history.append(
                    {
                        "role": "assistant",
                        "text": result["warning_message"],
                        "timestamp": datetime.utcnow().isoformat(),
                    }
                )

                # Still extract context
                extracted = result.get("current_extraction", {})
                for key, value in extracted.items():
                    if value and value != "null":
                        current_context[key] = value

                return {
                    "type": "warning",
                    "question": result["warning_message"],
                    "context": current_context,
                    "sufficient": False,
                    "confidence": 0,
                    "severity": result.get("severity", "medium"),
                }

            # Handle question type
            if result["type"] == "question":
                # Extract context incrementally
                extracted = result.get("current_extraction", {})
                for key, value in extracted.items():
                    if value and value != "null":
                        current_context[key] = value

                print(f"📊 Context: {current_context}")

                conversation_history.append(
                    {
                        "role": "assistant",
                        "text": result["question"],
                        "timestamp": datetime.utcnow().isoformat(),
                    }
                )

                # Calculate confidence
                filled = sum(1 for f in self.GOOD_FIELDS if current_context.get(f))
                confidence = min(100, int((filled / len(self.GOOD_FIELDS)) * 100))

                return {
                    "type": "question",
                    "question": result["question"],
                    "context": current_context,
                    "sufficient": False,
                    "confidence": confidence,
                    "ui_hint": result.get("ui_hint", "none"),  # ✨ NEW
                }

            # Handle summary type
            else:  # summary
                confirmation = (
                    f"Perfekt verstanden! ✓\n\n{result['summary']}\n\nStimmt das so?"
                )
                conversation_history.append(
                    {
                        "role": "assistant",
                        "text": confirmation,
                        "timestamp": datetime.utcnow().isoformat(),
                    }
                )

                return {
                    "type": "summary",
                    "question": confirmation,
                    "summary": result["summary"],
                    "context": result.get("context", current_context),
                    "sufficient": True,
                    "confidence": result.get("confidence", 100),
                    "gz_score": result.get("gz_score", None),  # ✨ NEW
                }

        except json.JSONDecodeError as e:
            print(f"❌ JSON error: {e}")
            fallback = "Können Sie das bitte näher erläutern?"
            conversation_history.append(
                {
                    "role": "assistant",
                    "text": fallback,
                    "timestamp": datetime.utcnow().isoformat(),
                }
            )
            return {
                "type": "question",
                "question": fallback,
                "context": current_context,
                "sufficient": False,
                "confidence": 0,
            }
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback

            traceback.print_exc()
            raise

    def _build_messages(self, history: List[Dict]) -> List[Dict]:
        """Build message list for Claude API"""
        return [
            {
                "role": "user" if msg["role"] == "user" else "assistant",
                "content": msg["text"],
            }
            for msg in history
        ]

    def check_sufficiency(self, context: Dict) -> Tuple[bool, str]:
        """Check if enough context gathered"""
        filled = [f for f in context.keys() if context.get(f)]

        if all(f in filled for f in self.EXCELLENT_FIELDS):
            return True, "excellent"
        elif all(f in filled for f in self.GOOD_FIELDS):
            return True, "good"
        elif all(f in filled for f in self.REQUIRED_FIELDS):
            return True, "minimum"
        return False, "insufficient"

    def get_opening_message(self) -> str:
        """Opening message with professional tone"""
        return (
            "Guten Tag! 👋\n\n"
            "Ich bin Ihr digitaler Gründungsberater und unterstütze Sie bei der "
            "Optimierung Ihrer Gründungszuschuss-Bewerbung.\n\n"
            "Lassen Sie uns Ihre Geschäftsidee gemeinsam präzisieren. "
            "Das Gespräch dauert etwa 3-5 Minuten.\n\n"
            "Was möchten Sie anbieten?"
        )
