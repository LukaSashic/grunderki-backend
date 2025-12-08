# socratic_engine.py
"""
Socratic Dialogue Engine for Business Idea Discovery
Uses Claude to conduct intelligent conversations and extract business context
"""

import json
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from anthropic import Anthropic


class SocraticEngine:
    """
    Manages Socratic dialogue for business idea extraction
    """

    # Required business context fields
    REQUIRED_FIELDS = ["what", "who", "problem"]
    GOOD_FIELDS = ["what", "who", "problem", "why_you"]
    EXCELLENT_FIELDS = ["what", "who", "problem", "why_you", "how"]

    SYSTEM_PROMPT = """You are an expert business consultant conducting a Socratic dialogue to understand a founder's business idea.

YOUR MISSION:
Extract sufficient context through natural conversation to understand:
1. WHAT they offer (service/product)
2. WHO their customers are (target segment)
3. WHAT PROBLEM they solve
4. WHY they're qualified (unique advantage) 
5. HOW they deliver (optional)

CONVERSATION RULES:
- Ask ONE focused question at a time
- Keep questions SHORT (max 15 words in German)
- Use casual, encouraging tone
- Build on previous answers
- Validate understanding periodically
- Use German language naturally
- Stop when you have sufficient context

CURRENT CONTEXT STATUS:
{context_json}

CONVERSATION HISTORY:
{conversation_history}

TASK:
Based on the conversation, determine if you need more information or if you have enough to summarize.

OUTPUT FORMAT (JSON only, no other text):

If more info needed:
{{
  "type": "question",
  "question": "Deine nächste Frage hier",
  "reasoning": "Warum du diese Frage stellst",
  "confidence": 0-100
}}

If sufficient context gathered:
{{
  "type": "summary",
  "summary": "Klare Zusammenfassung der Business Idee in 2-3 Sätzen",
  "context": {{
    "what": "extracted service/product",
    "who": "extracted target customer",
    "problem": "extracted problem being solved",
    "why_you": "extracted unique advantage (if mentioned)",
    "how": "extracted delivery method (if mentioned)"
  }},
  "confidence": 0-100
}}

REMEMBER: 
- Output ONLY valid JSON
- No markdown formatting
- No backticks
- No explanatory text outside JSON"""

    def __init__(self):
        # Initialize Anthropic client
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        self.client = Anthropic(api_key=api_key)

    async def process_message(
        self, user_message: str, conversation_history: List[Dict], current_context: Dict
    ) -> Dict:
        """
        Process user message and generate next question or summary

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
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
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

            # Extract response text
            response_text = response.content[0].text.strip()

            # Clean up response (remove markdown formatting if present)
            response_text = (
                response_text.replace("```json", "").replace("```", "").strip()
            )

            # Parse JSON response
            result = json.loads(response_text)

            if result["type"] == "question":
                # Add assistant question to history
                conversation_history.append(
                    {
                        "role": "assistant",
                        "text": result["question"],
                        "timestamp": datetime.utcnow().isoformat(),
                    }
                )

                # Update context based on conversation
                updated_context = self._extract_context_from_history(
                    conversation_history, current_context
                )

                return {
                    "type": "question",
                    "question": result["question"],
                    "context": updated_context,
                    "sufficient": False,
                    "confidence": result.get("confidence", 0),
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

                return {
                    "type": "summary",
                    "question": confirmation,
                    "summary": result["summary"],
                    "context": result["context"],
                    "sufficient": True,
                    "confidence": result.get("confidence", 100),
                }

        except json.JSONDecodeError as e:
            # Fallback if Claude doesn't return valid JSON
            print(f"JSON decode error: {e}")
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
            print(f"Error in Socratic engine: {e}")
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

    def _extract_context_from_history(
        self, conversation_history: List[Dict], current_context: Dict
    ) -> Dict:
        """
        Extract business context from conversation history
        This is a simple heuristic - Claude does the heavy lifting
        """

        # Calculate confidence based on filled fields
        filled_fields = sum(
            [1 for field in self.GOOD_FIELDS if current_context.get(field)]
        )

        confidence = min(100, (filled_fields / len(self.GOOD_FIELDS)) * 100)

        return {
            **current_context,
            "confidence": confidence,
            "message_count": len(
                [m for m in conversation_history if m["role"] == "user"]
            ),
        }

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
