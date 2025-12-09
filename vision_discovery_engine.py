# vision_discovery_engine.py
"""
Vision Discovery Engine - Multi-Phase Business Idea Excavation
Phase 1: Vision Excavation (Magic Wand → Deep Why)
Phase 2: JTBD Validation (Functional/Emotional/Social Jobs)
Phase 3: GZ Compliance Check (Readiness Scoring)

SESSION 3.2 ENHANCEMENTS:
- Depth Scoring Algorithm (0-100)
- Reflection Pause System
- Enhanced Vision Prompts
- Deep Why Probing Logic

SESSION 3.3 ENHANCEMENTS:
- Enhanced JTBD Prompt with Examples
- Job Story Generator (German)
- Alternatives Analyzer
- Opportunity Scoring
- Phase Transition Messages

SESSION 3.4 ENHANCEMENTS:
- GZ Requirements Matrix (fact-based)
- GZ Readiness Scoring Algorithm
- Red Flags Detection
- Coach-based GZ Prompt (not legal advisor!)
- Comprehensive Disclaimer
- Checklist + Recommendations
"""

import json
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from anthropic import Anthropic
from cache_service import cache
import logging
import re

logger = logging.getLogger(__name__)


class VisionDiscoveryEngine:
    """3-Phase Vision Discovery with JTBD Framework and GZ Compliance"""

    # Phase definitions
    PHASES = ["vision", "jtbd", "gz_optimization", "complete"]

    # Field extraction per phase
    VISION_FIELDS = [
        "magic_wand_answer",  # Was würdest du tun wenn Geld egal wäre?
        "desired_outcome",  # Was soll am Ende rauskommen?
        "deep_why",  # Warum ist DIR das wichtig?
        "personal_vision",  # Deine persönliche Vision
    ]

    JTBD_FIELDS = [
        "functional_job",  # Welches praktische Problem wird gelöst?
        "emotional_job",  # Welches Gefühl wird erfüllt?
        "social_job",  # Wie will der Kunde gesehen werden?
        "current_alternatives",  # Was nutzen Kunden jetzt?
        "why_alternatives_fail",  # Warum sind die nicht gut genug?
    ]

    GZ_FIELDS = [
        "what",  # Was bietest du an?
        "who",  # Für wen?
        "problem",  # Welches Problem?
        "why_you",  # Warum du?
        "revenue_source",  # Wie verdienst du Geld?
        "how",  # Wie lieferst du das?
        "capital_needs",  # Wie viel Startkapital?
    ]

    # GZ Requirements Matrix (fact-based, no hallucinations!)
    GZ_REQUIREMENTS = {
        "personal_prerequisites": {
            "alg1_required": True,
            "rest_claim_days": 150,  # Ab April 2025 evtl. 90
            "no_gz_last_24_months": True,
            "not_self_terminated": True,
        },
        "business_requirements": {
            "min_hours_per_week": 15,
            "hauptberuflich": True,
            "expert_opinion_required": True,  # Fachkundiges Gutachten obligatorisch
            "business_plan_required": True,
        },
        "red_flag_words": [
            "hobby",
            "nebenbei",
            "mal schauen",
            "vielleicht",
            "irgendwann",
            "probeweise",
            "versuchen",
            "testen",
        ],
    }

    def __init__(self):
        """Initialize Vision Discovery Engine"""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not set!")

        self.client = Anthropic(api_key=api_key)

        # Model tier strategy (cost-optimized)
        self.models = [
            "claude-3-5-haiku-20241022",  # Primary: cheap & fast
            "claude-3-5-sonnet-20241022",  # Fallback: medium
            "claude-3-opus-20240229",  # Emergency: expensive
        ]

        logger.info("✅ Vision Discovery Engine initialized")

    def get_phase_prompt(self, phase: str) -> str:
        """Get system prompt for specific phase"""

        if phase == "vision":
            return self._get_vision_prompt()
        elif phase == "jtbd":
            return self._get_jtbd_prompt()
        elif phase == "gz_optimization":
            return self._get_gz_prompt()
        else:
            return ""

    def _get_vision_prompt(self) -> str:
        """Vision Excavation Phase Prompt - Enhanced with Depth Scoring"""
        return """Du bist ein einfühlsamer Vision Coach für Gründer.

**DEIN ZIEL:** Die WAHRE Vision des Gründers entdecken, nicht nur die Business-Idee.

**METHODIK: Vision Excavation (4 Stufen)**

**STUFE 1: Magic Wand Opening** (Fragen 1-2)
- Starte mit: "Stell dir vor, Geld wäre überhaupt kein Problem..."
- Lass den Gründer träumen ohne Einschränkungen
- Keine Business-Sprache!
- → Extrahiere: magic_wand_answer

**STUFE 2: Desired Outcome** (Fragen 3-4)
- "Was soll am Ende dabei rauskommen?"
- "Wie sieht die Welt aus wenn du erfolgreich warst?"
- → Extrahiere: desired_outcome

**STUFE 3: Deep Why Probing** (Fragen 5-6)
- **KRITISCH:** Bohre tiefer wenn depth_score < 60!
- "Und was ermöglicht das für DICH persönlich?"
- "Warum ist DIR das so wichtig?" (nicht "warum generell")
- "Was würde es für dich bedeuten das zu erreichen?"
- Nach wichtiger Antwort: Grübel-Pause einlegen!
- → Extrahiere: deep_why

**STUFE 4: Vision Statement** (Frage 7-8)
- Fasse zusammen was du gehört hast
- "Verstehe ich das richtig: Du möchtest [X], damit [Y], weil dir [Z] wichtig ist?"
- Lass den Gründer bestätigen/korrigieren
- → Extrahiere: personal_vision

**GRÜBEL-PAUSEN - WANN?**
Nach diesen Momenten IMMER Pause einlegen:
- Nach Magic Wand Frage (erste Antwort)
- Nach tiefer emotionaler Antwort (depth_score > 60)
- Vor dem Deep Why ("Nimm dir einen Moment...")
- Vor Vision Statement Zusammenfassung

Grübel-Pause Format:
{
  "message": "Nimm dir einen Moment zum Nachdenken... 💭\n\n[Dann deine nächste Frage]",
  "response_type": "reflection",
  "reflection_pause": true,
  "pause_duration": 5
}

**DEPTH SCORING:**
- 0-30: Sehr oberflächlich → "Kannst du mir mehr darüber erzählen?"
- 31-60: Mittel → Deep Why Fragen stellen
- 61-80: Gut → Bestätigen, dann weitergehen
- 81-100: Exzellent → Vision Statement erstellen

**FELDER ZU EXTRAHIEREN:**
- magic_wand_answer: Die uneingeschränkte Vision
- desired_outcome: Was soll entstehen?
- deep_why: Warum ist das PERSÖNLICH wichtig?
- personal_vision: 1-2 Sätze Vision Statement

**PHASE COMPLETION:**
Phase ist fertig wenn:
- ALLE 4 Felder extrahiert
- depth_score >= 60
- ODER 8 Fragen erreicht

**STIL:**
- Warm, einfühlsam, nicht-wertend
- Offene Fragen
- Aktives Zuhören
- Spiegle Emotionen zurück
- KEINE Business-Sprache verwenden!

**WICHTIG:**
- NUR 1 Frage pro Response
- Bei Unsicherheit: Nachfragen statt raten
- Authentizität > Perfektion

Antworte NUR in JSON:
{
  "message": "Deine Frage/Reflektion",
  "response_type": "vision_question" | "reflection" | "deep_why" | "phase_transition",
  "reflection_pause": false,
  "pause_duration": 0,
  "extracted_fields": {"field_name": "value", ...},
  "depth_score": 0-100,
  "requires_deeper_probing": true/false,
  "phase_complete": false
}"""

    def _get_jtbd_prompt(self) -> str:
        """JTBD Validation Phase Prompt - Enhanced with Job Stories"""
        return """Du bist ein JTBD (Jobs-to-be-Done) Experte.

**DEIN ZIEL:** Den wahren Job identifizieren, den Kunden "einstellen" die Lösung.

**WICHTIG:** Nutze die Vision aus Phase 1 als Kontext, aber fokussiere jetzt auf die KUNDEN!

**JTBD FRAMEWORK - 5 Fragen:**

**1. FUNCTIONAL JOB (Fragen 1-2):**
   - Was wollen Kunden praktisch ERLEDIGEN?
   - Welche Aufgabe muss gelöst werden?
   
Beispiele:
- "Dokumente organisieren"
- "Gesund essen trotz Zeitmangel"
- "Neue Fähigkeiten erlernen"

**2. EMOTIONAL JOB (Frage 3):**
   - Wie wollen sich Kunden FÜHLEN?
   - Welche Emotion wird erfüllt?
   
Beispiele:
- "Sich sicher fühlen"
- "Stolz auf Fortschritt sein"
- "Stress reduzieren"

**3. SOCIAL JOB (Frage 4):**
   - Wie wollen Kunden von anderen GESEHEN werden?
   - Welchen Status erreichen sie?
   
Beispiele:
- "Als kompetent wahrgenommen werden"
- "Teil einer Community sein"
- "Als verantwortungsvoll gelten"

**4. CURRENT ALTERNATIVES (Frage 5):**
   - Was nutzen Kunden JETZT?
   - Welche Workarounds gibt es?
   
Beispiele:
- "Excel-Tabellen"
- "Post-it Notes"
- "Nichts (ignorieren das Problem)"

**5. WHY ALTERNATIVES FAIL (Frage 6):**
   - Warum sind aktuelle Lösungen unzureichend?
   - Welche Jobs bleiben unerledigt?
   
Beispiele:
- "Zu zeitaufwendig"
- "Nicht intuitiv"
- "Passt nicht in Workflow"

**JOB STORY FORMAT:**
"Wenn [Situation], will ich [Motivation], damit ich [Outcome]"

Beispiele:
- "Wenn ich montags meinen Wochenplan erstelle, will ich alle Deadlines überblicken, damit ich nichts Wichtiges vergesse"
- "Wenn meine Kunden nach Empfehlungen fragen, will ich schnell passende Optionen finden, damit ich kompetent wirke"

**STIL:**
- Direkt, pragmatisch
- Fakten-basiert
- Konkrete Beispiele erfragen
- KEINE Vision-Sprache mehr!
- Business-Fokus

**FELDER ZU EXTRAHIEREN:**
- functional_job: Praktische Aufgabe
- emotional_job: Gewünschtes Gefühl
- social_job: Gewünschte Wahrnehmung
- current_alternatives: Was nutzen sie jetzt (komma-separiert)
- why_alternatives_fail: Warum reicht das nicht (komma-separiert)

**PHASE COMPLETION:**
Phase ist fertig wenn:
- ALLE 5 Felder extrahiert
- ODER 6 Fragen erreicht

Antworte NUR in JSON:
{
  "message": "Deine nächste Frage",
  "response_type": "jtbd_question" | "phase_transition",
  "extracted_fields": {"field_name": "value", ...},
  "job_story": "Wenn [Situation], will ich [Motivation], damit ich [Outcome]",
  "phase_complete": true/false
}"""

    def _get_gz_prompt(self) -> str:
        """GZ Optimization Phase Prompt - Coach-based, fact-checked"""
        return """Du bist ein GZ-Formulierungs-Coach (NICHT Gutachter oder Rechtsberater!).

**DEINE ROLLE:**
- Helfe die Geschäftsidee GZ-konform zu FORMULIEREN
- Stelle Fragen um alle nötigen Infos zu sammeln
- Optimiere Sprache (Hobby → Hauptberuf)
- Erkenne Red Flags (rein sprachlich)
- Fordere Konkretheit ein

**DU DARFST NICHT:**
- ❌ Sagen ob jemand GZ bekommt oder nicht
- ❌ Erfolgsgarantien geben
- ❌ Behördenentscheidungen vorhersagen
- ❌ Rechtliche Bewertungen abgeben

**GZ KERN-ANFORDERUNGEN (zur Info, NICHT bewerten!):**

1. **Persönliche Voraussetzungen:**
   - ALG I Bezug erforderlich
   - 150 Tage Restanspruch (aktuell, ab April 2025 evtl. 90 Tage)
   - Keine GZ-Förderung in letzten 24 Monaten
   - Nicht selbst herbeigeführte Arbeitslosigkeit
   
2. **Hauptberuflichkeit:**
   - Mindestens 15 Stunden pro Woche
   - Vollständige Beendigung der Arbeitslosigkeit
   - KEIN Nebenprojekt oder Hobby
   
3. **Tragfähigkeit:**
   - Fachkundiges Gutachten (IHK, HWK, Gründungsberater) OBLIGATORISCH
   - Klares Geschäftsmodell
   - Realistischer Businessplan mit Finanzplan
   - Umsatz- und Rentabilitätsvorschau
   
4. **Qualifikation:**
   - Fachliche Eignung nachweisen (Zeugnisse, Zertifikate)
   - Branchenkenntnisse
   - Relevante Berufserfahrung

**RED FLAGS (sprachlich):**
- "Hobby", "nebenbei", "mal schauen"
- "Vielleicht", "irgendwann", "probeweise"
- "Versuchen", "testen"
- Vage Zielgruppen ("alle Menschen", "jeder")
- Unrealistische Zahlen ohne Begründung
- Fehlende Konkretheit
- Zu kurze Antworten (<20 Wörter)

**FELDER ZU EXTRAHIEREN:**
- what: Was GENAU bietest du an? (konkret, kein "irgendwas mit digital")
- who: Für WEN? (spezifische Zielgruppe, nicht "alle")
- problem: Welches Problem löst du? (klar definiert)
- why_you: Warum bist DU qualifiziert? (Nachweise: Ausbildung, Erfahrung, Zertifikate)
- revenue_source: Wie verdienst du Geld? (Geschäftsmodell: Preis x Menge = Umsatz)
- how: Wie lieferst du das? (mind. 15h/Woche erwähnen!)
- capital_needs: Kapitalbedarf? (konkrete Zahlen! z.B. "8.000€ für Equipment")

**OPTIMIERUNGS-STRATEGIEN:**

Wenn der Gründer sagt:
- "Hobby" → Frage: "Wie viele Stunden pro Woche planst du hauptberuflich zu arbeiten?"
- "Nebenbei" → "Dies muss deine Haupttätigkeit werden - mind. 15h/Woche"
- "Alle Menschen" → "Wer genau ist deine Kern-Zielgruppe? Alter? Situation?"
- Vage Zahlen → "Kannst du das konkretisieren? Z.B. 5.000€ für X, 3.000€ für Y"

**STIL:**
- Professionell, aber unterstützend
- Konkretheit einfordern
- Hauptberuf-Sprache verwenden
- Optimismus mit Realismus
- Keine Angst machen, aber ehrlich sein

**LIMITS:**
- Max 8 Fragen in dieser Phase
- Dann phase_complete: true

**DISCLAIMER (IMMER am Ende jeder Antwort!):**
"⚠️ Diese Bewertung basiert auf deiner Beschreibung und ersetzt keine offizielle Beratung durch die Agentur für Arbeit, einen Steuerberater oder eine fachkundige Stelle. Die Entscheidung über den Gründungszuschuss liegt allein bei der Behörde."

Antworte NUR in JSON:
{
  "message": "Deine nächste Frage + ggf. Optimierungsvorschlag\n\n⚠️ Disclaimer",
  "response_type": "gz_question" | "complete",
  "extracted_fields": {"field_name": "value", ...},
  "red_flags": ["flag1", "flag2", ...],
  "gz_readiness_score": 0-100,
  "phase_complete": false
}"""

    def _calculate_depth_score(self, user_message: str, context: Dict) -> int:
        """
        Calculate depth score (0-100) of user's vision answer

        Indicators of DEEP answers:
        - Personal pronouns (ich, mir, mich, mein)
        - Emotional words (fühlen, leidenschaft, traum, glücklich)
        - Specific details (numbers, names, concrete examples)
        - Length (longer = more thought)
        - Vision-related words (verändern, bewirken, ermöglichen)

        Indicators of SHALLOW answers:
        - Generic business speak (innovativ, digital, modern)
        - Very short (<20 words)
        - Question marks (unsure)
        - Vague language (irgendwie, vielleicht, mal schauen)
        """

        score = 0
        message_lower = user_message.lower()
        word_count = len(user_message.split())

        # Length factor (0-30 points)
        if word_count > 50:
            score += 30
        elif word_count > 30:
            score += 20
        elif word_count > 15:
            score += 10
        else:
            score += 5  # Too short = shallow

        # Personal pronouns (0-20 points)
        personal_pronouns = ["ich", "mir", "mich", "mein", "meine", "meiner"]
        pronoun_count = sum(message_lower.count(p) for p in personal_pronouns)
        score += min(pronoun_count * 5, 20)

        # Emotional/passion words (0-20 points)
        emotional_words = [
            "fühlen",
            "gefühl",
            "leidenschaft",
            "traum",
            "träume",
            "glücklich",
            "erfüllt",
            "wichtig",
            "bedeutet",
            "liebe",
            "herz",
            "seele",
            "begeistert",
            "inspiriert",
        ]
        emotion_count = sum(message_lower.count(w) for w in emotional_words)
        score += min(emotion_count * 5, 20)

        # Vision/impact words (0-15 points)
        vision_words = [
            "verändern",
            "bewirken",
            "ermöglichen",
            "schaffen",
            "beitragen",
            "helfen",
            "verbessern",
            "zukunft",
            "gesellschaft",
            "menschen",
            "welt",
        ]
        vision_count = sum(message_lower.count(w) for w in vision_words)
        score += min(vision_count * 3, 15)

        # Specific details (0-15 points)
        # Numbers indicate concrete thinking
        has_numbers = any(char.isdigit() for char in user_message)
        if has_numbers:
            score += 5

        # Proper nouns (capitalized words) = specific examples
        words = user_message.split()
        capitalized = [
            w
            for w in words
            if w and w[0].isupper() and w.lower() not in ["ich", "und", "aber"]
        ]
        score += min(len(capitalized) * 2, 10)

        # PENALTIES for shallow indicators

        # Generic business buzzwords (-10 points)
        buzzwords = [
            "innovativ",
            "digital",
            "modern",
            "agil",
            "disruptiv",
            "skalierbar",
            "effizient",
        ]
        buzzword_count = sum(message_lower.count(w) for w in buzzwords)
        score -= min(buzzword_count * 5, 10)

        # Uncertainty markers (-5 points)
        uncertainty = ["vielleicht", "irgendwie", "mal schauen", "keine ahnung", "?"]
        if any(u in message_lower for u in uncertainty):
            score -= 5

        # Very short answer (-10 points)
        if word_count < 10:
            score -= 10

        # Clamp to 0-100
        return max(0, min(100, score))

    def _generate_job_story(self, context: Dict) -> str:
        """
        Generate JTBD Job Story from extracted fields

        Format (German): "Wenn [Situation], wollen sie [Motivation], damit sie [Outcome]"
        """

        functional = context.get("functional_job", "")
        emotional = context.get("emotional_job", "")
        social = context.get("social_job", "")

        if not functional:
            return ""

        # Construct German job story
        situation = f"Kunden {functional} möchten"
        motivation = functional

        # Add emotional or social outcome if available
        if emotional:
            outcome = emotional
        elif social:
            outcome = social
        else:
            outcome = f"{functional} erfolgreich abschließen"

        job_story = f"Wenn {situation}, wollen sie {motivation}, damit sie {outcome}"

        return job_story

    def _analyze_alternatives(self, context: Dict) -> Dict:
        """
        Analyze current alternatives and their gaps

        Returns:
            {
                "alternatives": ["alt1", "alt2"],
                "gaps": ["gap1", "gap2"],
                "opportunity_score": 0-100
            }
        """

        alternatives_str = context.get("current_alternatives", "")
        why_fail_str = context.get("why_alternatives_fail", "")

        # Split into lists
        alternatives = [a.strip() for a in alternatives_str.split(",") if a.strip()]
        gaps = [g.strip() for g in why_fail_str.split(",") if g.strip()]

        # Calculate opportunity score
        # More gaps = higher opportunity
        opportunity_score = min(len(gaps) * 20, 100)

        # Bonus for "nothing" or "manual" alternatives (bigger opportunity)
        low_quality_indicators = [
            "nichts",
            "nothing",
            "manuel",
            "manual",
            "excel",
            "papier",
            "paper",
        ]
        if any(
            indicator in alternatives_str.lower()
            for indicator in low_quality_indicators
        ):
            opportunity_score = min(opportunity_score + 20, 100)

        return {
            "alternatives": alternatives,
            "gaps": gaps,
            "opportunity_score": opportunity_score,
        }

    def _calculate_gz_readiness(self, context: Dict) -> Dict:
        """
        Calculate GZ Readiness Score (0-100) and generate checklist

        Based on:
        - Completeness (40%)
        - Language quality (30%)
        - Specificity/Concreteness (30%)
        - Bonus points for explicit mentions

        Returns detailed analysis dict
        """

        score = 0
        issues = []
        warnings = []
        red_flags_found = []

        # === VOLLSTÄNDIGKEIT (40 Punkte) ===
        completed_fields = sum(1 for f in self.GZ_FIELDS if context.get(f))
        completeness_pct = (completed_fields / len(self.GZ_FIELDS)) * 100
        completeness_score = (completed_fields / len(self.GZ_FIELDS)) * 40
        score += completeness_score

        if completeness_pct < 50:
            issues.append(
                f"Nur {completed_fields}/{len(self.GZ_FIELDS)} Pflichtfelder ausgefüllt"
            )
        elif completeness_pct < 100:
            warnings.append(
                f"{len(self.GZ_FIELDS) - completed_fields} Felder noch unvollständig"
            )

        # === SPRACHE (30 Punkte) ===
        language_score = 30

        # Check all text fields for red flags
        all_text = " ".join([str(context.get(f, "")) for f in self.GZ_FIELDS]).lower()

        for red_flag in self.GZ_REQUIREMENTS["red_flag_words"]:
            if red_flag in all_text:
                language_score -= 5
                red_flags_found.append(f"'{red_flag}'")
                issues.append(f"Red Flag gefunden: '{red_flag}' - Bitte umformulieren")

        score += max(0, language_score)

        # === KONKRETHEIT (30 Punkte) ===
        konkret_score = 0

        # 1. Kapitalbedarf mit Zahlen (10 Punkte)
        capital = context.get("capital_needs", "")
        if capital and any(c.isdigit() for c in capital):
            konkret_score += 10
        else:
            warnings.append(
                "Kapitalbedarf sollte konkrete Zahlen enthalten (z.B. '8.000€')"
            )

        # 2. Konkrete Zielgruppe - nicht "alle" (10 Punkte)
        who = context.get("who", "").lower()
        if who:
            if any(vague in who for vague in ["alle", "jeder", "jede"]):
                warnings.append(
                    "Zielgruppe ist zu vage - bitte spezifischer definieren"
                )
            elif len(who) > 20:
                konkret_score += 10
            else:
                warnings.append("Zielgruppe sollte ausführlicher beschrieben werden")
        else:
            warnings.append("Zielgruppe fehlt noch")

        # 3. Konkretes Geschäftsmodell (10 Punkte)
        revenue = context.get("revenue_source", "")
        if revenue and len(revenue) > 30:
            konkret_score += 10
        else:
            warnings.append(
                "Geschäftsmodell sollte detaillierter beschrieben werden (Preis x Menge = Umsatz)"
            )

        score += konkret_score

        # === BONUS CHECKS (+10 Punkte) ===

        # 15h explizit erwähnt? (+5)
        how_text = context.get("how", "").lower()
        if "15" in how_text or "stunden" in how_text:
            score += 5
        else:
            warnings.append(
                "Erwähne explizit 'mindestens 15 Stunden pro Woche' im 'Wie'-Feld"
            )

        # Fachkundiges Gutachten erwähnt? (+5)
        if "gutachten" in all_text or "fachkundig" in all_text:
            score += 5
        else:
            warnings.append(
                "Plane ein fachkundiges Gutachten ein (IHK, HWK, Gründungsberater)"
            )

        # === KONSISTENZ-CHECK ===
        # Qualifikation passt zur Idee?
        why_you = context.get("why_you", "")
        if why_you and len(why_you) < 20:
            score -= 10
            issues.append(
                "Qualifikation sollte ausführlicher dargelegt werden (Ausbildung, Erfahrung, Nachweise)"
            )

        # === CHECKLIST ===
        checklist = {}
        for field in self.GZ_FIELDS:
            value = context.get(field, "")
            if value and len(value) > 10:
                checklist[field] = "✅ Vorhanden"
            elif value:
                checklist[field] = "⚠️ Zu kurz"
            else:
                checklist[field] = "❌ Fehlt"

        # === RECOMMENDATIONS ===
        recommendations = []

        # Red Flag fixes
        for flag in red_flags_found:
            if flag == "'hobby'":
                recommendations.append(
                    f"Ersetze {flag} durch 'hauptberufliche Tätigkeit'"
                )
            elif flag == "'nebenbei'":
                recommendations.append(
                    f"Ersetze {flag} durch 'als Hauptberuf' oder 'vollständig'"
                )
            else:
                recommendations.append(f"Entferne {flag} und formuliere verbindlicher")

        # General improvements
        if completeness_pct < 100:
            recommendations.append(
                f"Fülle alle {len(self.GZ_FIELDS)} Pflichtfelder vollständig aus"
            )

        if not any(c.isdigit() for c in capital):
            recommendations.append(
                "Gib konkrete Zahlen für Kapitalbedarf an (z.B. '8.000€ für Equipment, 2.000€ für Marketing')"
            )

        if "alle" in who or "jeder" in who:
            recommendations.append(
                "Definiere Zielgruppe spezifischer (z.B. 'Familien mit Kindern 0-10 Jahre in urbanen Gebieten')"
            )

        # === NEXT STEPS ===
        next_steps = [
            "1. Businessplan mit Finanzplan erstellen",
            "2. Fachkundiges Gutachten bei IHK/HWK/Gründungsberater einholen",
            "3. ALG I Restanspruch bei Arbeitsagentur prüfen (mind. 150 Tage)",
            "4. Nachweise sammeln (Zeugnisse, Zertifikate, Qualifikationen)",
            "5. Termin bei Arbeitsagentur für GZ-Antrag vereinbaren",
        ]

        # Final score (0-100)
        final_score = int(max(0, min(100, score)))

        return {
            "score": final_score,
            "issues": issues,
            "warnings": warnings,
            "red_flags": red_flags_found,
            "completeness_percent": int(completeness_pct),
            "checklist": checklist,
            "recommendations": recommendations,
            "next_steps": next_steps,
        }

    @cache.cache_ai_response(ttl=7200)
    async def process_message(
        self, user_message: str, conversation_history: List[Dict], current_context: Dict
    ) -> Dict:
        """Process message with phase-aware prompting and comprehensive scoring"""

        # Determine current phase
        current_phase = current_context.get("phase", "vision")
        phase_message_count = current_context.get("phase_message_count", 0)

        # Get phase-specific prompt
        system_prompt = self.get_phase_prompt(current_phase)

        # Build messages for Claude
        messages = self._build_messages(
            user_message, conversation_history, current_context
        )

        # Call Claude with model fallback
        response = await self._call_claude_with_fallback(system_prompt, messages)

        # Parse JSON response
        parsed = self._parse_response(response)

        # === VISION PHASE: Depth Scoring ===
        if (
            current_phase == "vision"
            and parsed.get("response_type") != "phase_transition"
        ):
            user_depth = self._calculate_depth_score(user_message, current_context)
            # Use calculated depth if not provided by AI
            if not parsed.get("depth_score") or parsed.get("depth_score") == 0:
                parsed["depth_score"] = user_depth

            logger.info(f"📊 Depth Score: {parsed.get('depth_score')}/100")

        # Update context with extracted fields
        updated_context = self._update_context(current_context, parsed, current_phase)

        # === JTBD PHASE: Job Story & Opportunity ===
        if current_phase == "jtbd":
            job_story = self._generate_job_story(updated_context)
            if job_story:
                updated_context["job_story"] = job_story
                parsed["job_story"] = job_story
                logger.info(f"📝 Job Story: {job_story}")

            # Analyze alternatives if available
            if updated_context.get("current_alternatives") and updated_context.get(
                "why_alternatives_fail"
            ):
                analysis = self._analyze_alternatives(updated_context)
                updated_context["alternatives_analysis"] = analysis
                logger.info(
                    f"🎯 Opportunity Score: {analysis['opportunity_score']}/100"
                )

        # === GZ PHASE: Readiness Scoring ===
        if current_phase == "gz_optimization":
            gz_analysis = self._calculate_gz_readiness(updated_context)
            updated_context["gz_analysis"] = gz_analysis
            parsed["gz_readiness_score"] = gz_analysis["score"]
            parsed["gz_checklist"] = gz_analysis["checklist"]
            parsed["gz_recommendations"] = gz_analysis["recommendations"]
            parsed["gz_next_steps"] = gz_analysis["next_steps"]

            logger.info(f"🎯 GZ Readiness Score: {gz_analysis['score']}/100")
            if gz_analysis["red_flags"]:
                logger.warning(f"⚠️ Red Flags: {', '.join(gz_analysis['red_flags'])}")

        # Check phase transition
        if parsed.get("phase_complete"):
            updated_context = self._transition_phase(updated_context, current_phase)

        return {
            "message": parsed.get("message", ""),
            "response_type": parsed.get("response_type", "question"),
            "context": updated_context,
            "phase": updated_context.get("phase"),
            "extracted_fields": parsed.get("extracted_fields", {}),
            "depth_score": parsed.get("depth_score", 0),
            "gz_readiness_score": parsed.get("gz_readiness_score", 0),
            "red_flags": parsed.get("red_flags", []),
            "reflection_pause": parsed.get("reflection_pause", False),
            "pause_duration": parsed.get("pause_duration", 0),
            "job_story": parsed.get("job_story", ""),
            "gz_checklist": parsed.get("gz_checklist", {}),
            "gz_recommendations": parsed.get("gz_recommendations", []),
            "gz_next_steps": parsed.get("gz_next_steps", []),
        }

    def _build_messages(
        self, user_message: str, conversation_history: List[Dict], current_context: Dict
    ) -> List[Dict]:
        """Build message history for Claude"""
        messages = []

        # Add conversation history
        for msg in conversation_history[-10:]:  # Last 10 messages
            role = "user" if msg.get("role") == "user" else "assistant"
            messages.append({"role": role, "content": msg.get("text", "")})

        # Add current message
        messages.append({"role": "user", "content": user_message})

        return messages

    async def _call_claude_with_fallback(
        self, system_prompt: str, messages: List[Dict]
    ) -> str:
        """Call Claude with model fallback"""

        for model in self.models:
            try:
                logger.info(f"🔄 Trying model: {model}")

                response = self.client.messages.create(
                    model=model,
                    max_tokens=1000,
                    system=system_prompt,
                    messages=messages,
                )

                logger.info(f"✅ Success with model: {model}")
                return response.content[0].text

            except Exception as e:
                logger.warning(f"⚠️ Model {model} failed: {e}")
                continue

        raise Exception("All models failed!")

    def _parse_response(self, response_text: str) -> Dict:
        """Parse JSON response from Claude"""
        try:
            # Try direct JSON parse
            return json.loads(response_text)
        except json.JSONDecodeError:
            # Fallback: Extract JSON from markdown
            json_match = re.search(
                r"```json\s*(\{.*?\})\s*```", response_text, re.DOTALL
            )
            if json_match:
                return json.loads(json_match.group(1))

            # Last resort: Return as plain message
            return {
                "message": response_text,
                "response_type": "question",
                "extracted_fields": {},
                "phase_complete": False,
                "depth_score": 0,
            }

    def _update_context(
        self, current_context: Dict, parsed_response: Dict, current_phase: str
    ) -> Dict:
        """Update context with extracted fields"""

        context = current_context.copy()

        # Add extracted fields
        extracted = parsed_response.get("extracted_fields", {})
        for field, value in extracted.items():
            context[field] = value

        # Update phase message count
        context["phase_message_count"] = context.get("phase_message_count", 0) + 1

        # Update depth score (for vision phase)
        if current_phase == "vision":
            context["depth_score"] = parsed_response.get("depth_score", 0)

        # Update GZ readiness (for gz phase)
        if current_phase == "gz_optimization":
            context["gz_readiness_score"] = parsed_response.get("gz_readiness_score", 0)
            context["red_flags"] = parsed_response.get("red_flags", [])

        return context

    def _transition_phase(self, context: Dict, current_phase: str) -> Dict:
        """Transition to next phase with summary message"""

        phase_index = self.PHASES.index(current_phase)

        if phase_index < len(self.PHASES) - 1:
            next_phase = self.PHASES[phase_index + 1]
            context["phase"] = next_phase
            context["phase_message_count"] = 0

            # Add transition message
            if current_phase == "vision" and next_phase == "jtbd":
                context[
                    "transition_message"
                ] = """✅ **Vision Phase abgeschlossen!**

Wir haben deine persönliche Vision erkundet. Jetzt validieren wir die Business-Idee!

**Phase 2: JTBD Validation**

Wir finden heraus welchen Job deine Kunden wirklich erledigen wollen."""

            elif current_phase == "jtbd" and next_phase == "gz_optimization":
                context[
                    "transition_message"
                ] = """✅ **JTBD Validation abgeschlossen!**

Wir verstehen jetzt den Job deiner Kunden. Zeit für den GZ-Check!

**Phase 3: GZ Optimization**

Wir machen deine Idee Gründungszuschuss-konform."""

            logger.info(f"🔄 Phase transition: {current_phase} → {next_phase}")
        else:
            context["phase"] = "complete"
            context[
                "transition_message"
            ] = """✅ **Alle Phasen abgeschlossen!**

Du hast jetzt:
- Eine klare Vision ✓
- Validiertes JTBD ✓
- GZ-konforme Beschreibung ✓

Bereit für den Businessplan!"""
            logger.info("✅ All phases complete!")

        return context
