# socratic_engine.py
"""
Socratic Dialogue Engine for Business Idea Discovery
Uses Claude to conduct intelligent conversations and extract business context
UPDATED: Incremental extraction for real-time research, GZ-specific fields
"""

import json
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from anthropic import Anthropic


class SocraticEngine:
    """
    Manages Socratic dialogue for business idea extraction
    ✨ NEW: Extracts context INCREMENTALLY for real-time research sidebar
    """

    # Required business context fields
    REQUIRED_FIELDS = ["what", "who", "problem"]

    # ✨ UPDATED: Added GZ-specific fields
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

    # ✨ UPDATED: Professional but accessible tone, incremental extraction
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
- Ton: Professionell aber zugänglich (nicht zu casual, nicht zu formell)
- Baue auf vorherigen Antworten auf
- Validiere Verständnis regelmäßig
- Natürliches Deutsch
- Stoppe wenn du ausreichend Kontext hast

AKTUELLER KONTEXT STATUS:
{context_json}

GESPRÄCHSVERLAUF:
{conversation_history}

AUFGABE:
Basierend auf der Konversation, entscheide ob du mehr Informationen brauchst oder genug hast für eine Zusammenfassung.

OUTPUT FORMAT (NUR JSON, kein anderer Text):

Wenn mehr Info benötigt:
{{
  "type": "question",
  "question": "Deine nächste Frage hier",
  "current_extraction": {{
    "what": "Extrahiertes Service/Produkt (oder null wenn noch nicht erwähnt)",
    "who": "Extrahierte Zielgruppe (oder null)",
    "problem": "Extrahiertes Problem (oder null)",
    "why_you": "Einzigartiger Vorteil (oder null)",
    "revenue_source": "Wer zahlt wieviel (oder null)",
    "how": "Liefermethode (oder null)",
    "capital_needs": "Kapitalbedarf Schätzung (oder null)"
  }},
  "reasoning": "Warum du diese Frage stellst",
  "confidence": 0-100
}}

Wenn ausreichend Kontext gesammelt:
{{
  "type": "summary",
  "summary": "Klare Zusammenfassung der Business Idee in 2-3 Sätzen",
  "context": {{
    "what": "extrahiertes Service/Produkt",
    "who": "extrahierte Zielgruppe",
    "problem": "extrahiertes Problem",
    "why_you": "einzigartiger Vorteil",
    "revenue_source": "Ertragsmechanik",
    "how": "Liefermethode (optional)",
    "capital_needs": "Kapitalbedarf (optional)"
  }},
  "confidence": 0-100
}}

WICHTIG:
- Output NUR valides JSON
- Kein Markdown
- Keine Backticks
- Kein Text außerhalb JSON
- EXTRAHIERE Kontext INCREMENTELL in jedem Turn (current_extraction)"""

    def __init__(self):
        # ✅ FIXED: Proper API key initialization with validation
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set!")

        # Validate API key format
        if not api_key.startswith("sk-ant-"):
            raise ValueError(
                "Invalid ANTHROPIC_API_KEY format - should start with 'sk-ant-'"
            )

        self.client = Anthropic(api_key=api_key)
        print(f"✅ Anthropic client initialized (key: {api_key[:15]}...)")

    async def process_message(
        self, user_message: str, conversation_history: List[Dict], current_context: Dict
    ) -> Dict:
        """
        Process user message and generate next question or summary
        ✨ NEW: Extracts context INCREMENTALLY for real-time research

        Args:
            user_message: Latest message from user
            conversation_history: Full conversation so far
            current_context: Currently extracted business context

        Returns:
            Dict with question/summary and updated context
        """

        # Add user message to history
        conversation_history.append(
            {
                "role": "user",
                "text": user_message,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

        # Build messages for Claude
        messages = self._build_messages(conversation_history)

        # Call Claude
        try:
            print(f"🔄 Calling Claude API...")

            response = self.client.messages.create(
                # ✅ FIXED: Correct model name
                model="claude-3-opus-20240229",  # Current stable version
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

            print(f"✅ Claude API response received")

            # Extract response text
            response_text = response.content[0].text.strip()

            # Clean up response (remove markdown formatting if present)
            response_text = (
                response_text.replace("```json", "").replace("```", "").strip()
            )

            print(f"📝 Claude raw response: {response_text[:200]}...")

            # Parse JSON response
            result = json.loads(response_text)

            if result["type"] == "question":
                # ✨ CRITICAL FIX: Extract context INCREMENTALLY
                # This enables real-time research sidebar!
                extracted_data = result.get("current_extraction", {})

                # Update current_context with newly extracted fields
                for key, value in extracted_data.items():
                    if value and value != "null":  # Only update if value exists
                        current_context[key] = value

                print(f"📊 Updated context: {current_context}")

                # Add assistant question to history
                conversation_history.append(
                    {
                        "role": "assistant",
                        "text": result["question"],
                        "timestamp": datetime.utcnow().isoformat(),
                    }
                )

                # Calculate confidence based on filled fields
                filled_count = sum(
                    1 for field in self.GOOD_FIELDS if current_context.get(field)
                )
                confidence = min(100, int((filled_count / len(self.GOOD_FIELDS)) * 100))

                return {
                    "type": "question",
                    "question": result["question"],
                    "context": current_context,  # ✅ Now contains incremental data!
                    "sufficient": False,
                    "confidence": confidence,
                }

            else:  # summary
                # Add confirmation question to history
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

                # Use extracted context from summary
                final_context = result.get("context", current_context)

                return {
                    "type": "summary",
                    "question": confirmation,
                    "summary": result["summary"],
                    "context": final_context,
                    "sufficient": True,
                    "confidence": result.get("confidence", 100),
                }

        except json.JSONDecodeError as e:
            # Fallback if Claude doesn't return valid JSON
            print(f"❌ JSON decode error: {e}")
            print(f"Response text: {response_text}")

            # Return a safe fallback question
            fallback_question = "Kannst du mir mehr darüber erzählen?"
            conversation_history.append(
                {
                    "role": "assistant",
                    "text": fallback_question,
                    "timestamp": datetime.utcnow().isoformat(),
                }
            )

            return {
                "type": "question",
                "question": fallback_question,
                "context": current_context,
                "sufficient": False,
                "confidence": 0,
            }

        except Exception as e:
            print(f"❌ Error in Socratic engine: {e}")
            import traceback

            traceback.print_exc()
            raise

    def _build_messages(self, conversation_history: List[Dict]) -> List[Dict]:
        """Build message list for Claude API from conversation history"""
        messages = []

        for msg in conversation_history:
            messages.append(
                {
                    "role": "user" if msg["role"] == "user" else "assistant",
                    "content": msg["text"],
                }
            )

        return messages

    def check_sufficiency(self, context: Dict) -> Tuple[bool, str]:
        """
        Check if we have enough context to proceed

        Returns:
            Tuple of (is_sufficient, quality_level)
        """

        filled = [field for field in context.keys() if context.get(field)]

        if all(field in filled for field in self.EXCELLENT_FIELDS):
            return True, "excellent"
        elif all(field in filled for field in self.GOOD_FIELDS):
            return True, "good"
        elif all(field in filled for field in self.REQUIRED_FIELDS):
            return True, "minimum"
        else:
            return False, "insufficient"

    def get_opening_message(self) -> str:
        """Get the opening message to start conversation"""
        return (
            "Hallo! 👋\n\n"
            "Lass uns gemeinsam deine Geschäftsidee verstehen. "
            "Ich stelle dir ein paar kurze Fragen – das dauert nur 2-3 Minuten.\n\n"
            "Was möchtest du anbieten?"
        )
