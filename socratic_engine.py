# socratic_engine.py
"""
Socratic Dialogue Engine for Business Idea Discovery
✅ FIXED: Multiple model fallback + Latest Anthropic SDK
"""

import json
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from anthropic import Anthropic


class SocraticEngine:
    """Manages Socratic dialogue for business idea extraction"""

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

    SYSTEM_PROMPT = """Du bist ein erfahrener Gründungsberater, der im Socratic Dialogue eine Geschäftsidee versteht.

DEINE MISSION:
Extrahiere durch natürliche Konversation ausreichend Kontext:
1. WAS wird angeboten (Service/Produkt)
2. WER sind die Kunden (Zielgruppe)
3. WELCHES PROBLEM wird gelöst
4. WARUM du/der Gründer (Einzigartiger Vorteil)
5. WIE wird es geliefert (optional)
6. ERTRAGSMECHANIK - wer zahlt wie viel (für Gründungszuschuss wichtig)
7. KAPITALBEDARF - grobe Schätzung (optional)

GESPRÄCHSREGELN:
- Stelle EINE fokussierte Frage zur Zeit
- Halte Fragen KURZ (max 15 Wörter auf Deutsch)
- Ton: Professionell aber zugänglich
- Baue auf vorherigen Antworten auf
- Validiere Verständnis regelmäßig
- Natürliches Deutsch
- Stoppe wenn du ausreichend Kontext hast

AKTUELLER KONTEXT STATUS:
{context_json}

GESPRÄCHSVERLAUF:
{conversation_history}

OUTPUT FORMAT (NUR JSON, kein anderer Text):

Wenn mehr Info benötigt:
{{
  "type": "question",
  "question": "Deine nächste Frage hier",
  "current_extraction": {{
    "what": "Extrahiertes Service/Produkt (oder null)",
    "who": "Extrahierte Zielgruppe (oder null)",
    "problem": "Extrahiertes Problem (oder null)",
    "why_you": "Einzigartiger Vorteil (oder null)",
    "revenue_source": "Wer zahlt wieviel (oder null)",
    "how": "Liefermethode (oder null)",
    "capital_needs": "Kapitalbedarf (oder null)"
  }},
  "reasoning": "Warum du diese Frage stellst",
  "confidence": 0-100
}}

Wenn ausreichend Kontext:
{{
  "type": "summary",
  "summary": "Klare Zusammenfassung in 2-3 Sätzen",
  "context": {{...}},
  "confidence": 0-100
}}"""

    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not set!")
        if not api_key.startswith("sk-ant-"):
            raise ValueError("Invalid API key format!")

        self.client = Anthropic(api_key=api_key)
        print(f"✅ Anthropic client initialized")

    async def process_message(
        self, user_message: str, conversation_history: List[Dict], current_context: Dict
    ) -> Dict:
        """Process message with model fallback"""

        conversation_history.append(
            {
                "role": "user",
                "text": user_message,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

        messages = self._build_messages(conversation_history)

        # ✅ Try multiple models with fallback
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
                print(f"🔄 Trying: {model}")
                response = self.client.messages.create(
                    model=model,
                    max_tokens=1500,
                    temperature=0.7,
                    system=self.SYSTEM_PROMPT.format(
                        context_json=json.dumps(
                            current_context, indent=2, ensure_ascii=False
                        ),
                        conversation_history=json.dumps(
                            conversation_history[-6:], indent=2, ensure_ascii=False
                        ),
                    ),
                    messages=messages,
                )
                print(f"✅ Success with: {model}")
                break

            except Exception as e:
                last_error = e
                if "404" in str(e) or "not_found" in str(e):
                    print(f"❌ {model} not found, trying next...")
                    continue
                else:
                    raise

        if response is None:
            raise Exception(f"All models failed! Last error: {last_error}")

        # Process response
        try:
            response_text = (
                response.content[0]
                .text.strip()
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )
            result = json.loads(response_text)

            if result["type"] == "question":
                extracted = result.get("current_extraction", {})
                for key, value in extracted.items():
                    if value and value != "null":
                        current_context[key] = value

                conversation_history.append(
                    {
                        "role": "assistant",
                        "text": result["question"],
                        "timestamp": datetime.utcnow().isoformat(),
                    }
                )

                filled = sum(1 for f in self.GOOD_FIELDS if current_context.get(f))
                confidence = min(100, int((filled / len(self.GOOD_FIELDS)) * 100))

                return {
                    "type": "question",
                    "question": result["question"],
                    "context": current_context,
                    "sufficient": False,
                    "confidence": confidence,
                }

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
                }

        except json.JSONDecodeError as e:
            print(f"❌ JSON error: {e}")
            fallback = "Kannst du mir mehr darüber erzählen?"
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
        return [
            {
                "role": "user" if msg["role"] == "user" else "assistant",
                "content": msg["text"],
            }
            for msg in history
        ]

    def check_sufficiency(self, context: Dict) -> Tuple[bool, str]:
        filled = [f for f in context.keys() if context.get(f)]
        if all(f in filled for f in self.EXCELLENT_FIELDS):
            return True, "excellent"
        elif all(f in filled for f in self.GOOD_FIELDS):
            return True, "good"
        elif all(f in filled for f in self.REQUIRED_FIELDS):
            return True, "minimum"
        return False, "insufficient"

    def get_opening_message(self) -> str:
        return "Hallo! 👋\n\nLass uns gemeinsam deine Geschäftsidee verstehen. Ich stelle dir ein paar kurze Fragen – das dauert nur 2-3 Minuten.\n\nWas möchtest du anbieten?"
