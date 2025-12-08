"""
IRT-CAT Engine for Entrepreneurial Personality Assessment
Based on Howard's 7-dimension framework
Using Mock Item Bank (real IRT parameters will be added later)
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import random
import logging

logger = logging.getLogger(__name__)


class IRTCATEngine:
    """
    Computerized Adaptive Testing engine using Graded Response Model
    Currently using mock data - will be connected to database later
    """

    def __init__(self):
        # Howard's 7 dimensions
        self.dimensions = [
            "innovativeness",
            "risk_taking",
            "achievement_orientation",
            "autonomy_orientation",
            "proactiveness",
            "locus_of_control",
            "self_efficacy",
        ]

        # Mock item bank - will be replaced with database
        self.item_bank = self._create_mock_item_bank()

        # Active sessions (in-memory - will be Redis later)
        self.sessions: Dict[str, Dict] = {}

        # CAT parameters
        self.stopping_criteria = {
            "max_items": 18,
            "min_items": 12,
            "target_se": 0.20,
            "max_time_minutes": 15,
        }

    def _create_mock_item_bank(self) -> List[Dict]:
        """Create mock item bank with business-context questions"""
        items = []

        # Achievement Orientation Items
        items.extend(
            [
                {
                    "item_id": "ach_01",
                    "dimension": "achievement_orientation",
                    "text_de": "Stellen Sie sich vor, Sie müssen Ihr erstes Kundengespräch vorbereiten. Wie gehen Sie vor?",
                    "response_scale": {
                        1: "Ich warte ab und schaue spontan, was im Gespräch passiert",
                        2: "Ich denke kurz über mögliche Fragen nach",
                        3: "Ich bereite die wichtigsten Punkte vor",
                        4: "Ich erstelle eine detaillierte Präsentation und Gesprächsleitfaden",
                        5: "Ich recherchiere intensiv den Kunden, erstelle maßgeschneiderte Lösungsvorschläge und simuliere das Gespräch",
                    },
                    "discrimination": 1.5,
                    "difficulty": 0.0,
                },
                {
                    "item_id": "ach_02",
                    "dimension": "achievement_orientation",
                    "text_de": "Sie haben sich ein Umsatzziel für das erste Jahr gesetzt. Nach 6 Monaten liegen Sie 20% dahinter. Was tun Sie?",
                    "response_scale": {
                        1: "Ich passe mein Ziel nach unten an - war wohl zu ambitioniert",
                        2: "Ich mache weiter wie bisher und hoffe auf Besserung",
                        3: "Ich analysiere die Gründe und passe meine Strategie an",
                        4: "Ich entwickle einen konkreten Aktionsplan und arbeite intensiver",
                        5: "Ich überarbeite komplett meine Strategie, hole mir externe Hilfe und setze einen aggressiven Aufholplan um",
                    },
                    "discrimination": 1.8,
                    "difficulty": 0.5,
                },
            ]
        )

        # Risk Taking Items
        items.extend(
            [
                {
                    "item_id": "risk_01",
                    "dimension": "risk_taking",
                    "text_de": "Ein potenzieller Großkunde bietet Ihnen einen lukrativen Auftrag, der aber 60% Ihrer Kapazität binden würde. Wie entscheiden Sie?",
                    "response_scale": {
                        1: "Zu riskant - ich lehne ab",
                        2: "Ich bin sehr zurückhaltend und prüfe lange",
                        3: "Ich wäge sorgfältig Chancen und Risiken ab",
                        4: "Ich nehme an, wenn die Konditionen stimmen",
                        5: "Ich sage sofort zu - große Chancen muss man nutzen",
                    },
                    "discrimination": 1.6,
                    "difficulty": -0.3,
                },
                {
                    "item_id": "risk_02",
                    "dimension": "risk_taking",
                    "text_de": "Sie haben die Möglichkeit, in einen neuen Markt zu expandieren. Das würde Ihre gesamten Rücklagen erfordern. Was tun Sie?",
                    "response_scale": {
                        1: "Keine Chance - zu gefährlich",
                        2: "Nur wenn ich zusätzliche Sicherheiten habe",
                        3: "Wenn die Analyse positiv ist, ja",
                        4: "Ich würde es wagen mit gutem Geschäftsplan",
                        5: "All-in - wer nicht wagt, der nicht gewinnt",
                    },
                    "discrimination": 1.7,
                    "difficulty": 0.8,
                },
            ]
        )

        # Innovativeness Items
        items.extend(
            [
                {
                    "item_id": "inn_01",
                    "dimension": "innovativeness",
                    "text_de": "Ihr Hauptkonkurrent bietet seit Jahren ein bewährtes Produkt an. Wie positionieren Sie sich?",
                    "response_scale": {
                        1: "Ich kopiere das bewährte Modell - warum neu erfinden?",
                        2: "Ich mache das Gleiche, aber etwas günstiger",
                        3: "Ich verbessere das bestehende Konzept moderat",
                        4: "Ich entwickle eine deutlich innovative Variante",
                        5: "Ich schaffe eine völlig neue Produktkategorie",
                    },
                    "discrimination": 1.4,
                    "difficulty": 0.2,
                }
            ]
        )

        # Autonomy Items
        items.extend(
            [
                {
                    "item_id": "aut_01",
                    "dimension": "autonomy_orientation",
                    "text_de": "Ein erfahrener Investor bietet Ihnen Kapital an, möchte aber bei allen wichtigen Entscheidungen mitbestimmen. Wie reagieren Sie?",
                    "response_scale": {
                        1: "Perfekt - ich brauche die Expertise",
                        2: "Okay, solange die Konditionen gut sind",
                        3: "Nur bei wirklich wichtigen Entscheidungen",
                        4: "Ungern - ich möchte selbst entscheiden",
                        5: "Niemals - lieber weniger Geld, aber volle Kontrolle",
                    },
                    "discrimination": 1.5,
                    "difficulty": 0.3,
                }
            ]
        )

        # Proactiveness Items
        items.extend(
            [
                {
                    "item_id": "pro_01",
                    "dimension": "proactiveness",
                    "text_de": "Sie hören von einer neuen Förderung für Ihr Geschäftsfeld. Die Deadline ist in 2 Wochen. Was tun Sie?",
                    "response_scale": {
                        1: "Zu kurzfristig - ich lasse es",
                        2: "Ich schaue es mir mal an",
                        3: "Ich prüfe es und entscheide dann",
                        4: "Ich fange sofort mit dem Antrag an",
                        5: "Ich arbeite Tag und Nacht, um die Deadline zu schaffen",
                    },
                    "discrimination": 1.6,
                    "difficulty": -0.2,
                }
            ]
        )

        # Locus of Control Items
        items.extend(
            [
                {
                    "item_id": "loc_01",
                    "dimension": "locus_of_control",
                    "text_de": "Ihr Startup läuft besser als erwartet. Woran liegt das hauptsächlich?",
                    "response_scale": {
                        1: "Glück und gutes Timing",
                        2: "Günstige Marktbedingungen",
                        3: "Eine Kombination aus Faktoren",
                        4: "Meine guten Entscheidungen",
                        5: "Meine harte Arbeit und Strategie",
                    },
                    "discrimination": 1.3,
                    "difficulty": 0.1,
                }
            ]
        )

        # Self-Efficacy Items
        items.extend(
            [
                {
                    "item_id": "eff_01",
                    "dimension": "self_efficacy",
                    "text_de": "Eine komplexe technische Herausforderung bedroht Ihr Projekt. Wie sicher sind Sie, das lösen zu können?",
                    "response_scale": {
                        1: "Überfordert - ich brauche dringend Hilfe",
                        2: "Unsicher - hoffe, dass jemand helfen kann",
                        3: "Mit Unterstützung sollte es klappen",
                        4: "Ich werde einen Weg finden",
                        5: "Absolut sicher - ich löse das definitiv",
                    },
                    "discrimination": 1.7,
                    "difficulty": 0.4,
                }
            ]
        )

        return items

    def start_session(
        self, session_id: str, business_idea: str, user_id: Optional[str] = None
    ) -> Dict:
        """Initialize new assessment session"""

        session = {
            "session_id": session_id,
            "user_id": user_id,
            "business_idea": business_idea,
            "started_at": datetime.utcnow(),
            "status": "active",
            # Theta estimates for each dimension (start at 0 = neutral)
            "theta_estimates": {dim: 0.0 for dim in self.dimensions},
            "se_estimates": {dim: 1.0 for dim in self.dimensions},
            # Items administered
            "items_administered": [],
            "responses": [],
            # Current state
            "current_dimension_index": 0,
            "items_per_dimension": 2,  # Simplified: 2 items per dimension = 14 total
        }

        self.sessions[session_id] = session

        # Get first item
        first_item = self._get_next_item(session_id)

        return {
            "session_id": session_id,
            "first_question": self._format_item_for_frontend(first_item),
            "estimated_duration": 12,
            "progress": self._calculate_progress(session_id),
        }

    def process_response(
        self, session_id: str, item_id: str, response_value: int
    ) -> Dict:
        """Process user response and return next item or completion"""

        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")

        session = self.sessions[session_id]

        # Find the item
        item = next((i for i in self.item_bank if i["item_id"] == item_id), None)
        if not item:
            raise ValueError(f"Item {item_id} not found")

        # Store response
        session["responses"].append(
            {
                "item_id": item_id,
                "response_value": response_value,
                "timestamp": datetime.utcnow(),
            }
        )

        # Update theta estimate (simplified IRT)
        dimension = item["dimension"]
        old_theta = session["theta_estimates"][dimension]

        # Simple update: move theta based on response
        # Real IRT would use Maximum Likelihood Estimation
        if response_value >= 4:
            session["theta_estimates"][dimension] = old_theta + 0.3
        elif response_value <= 2:
            session["theta_estimates"][dimension] = old_theta - 0.3
        else:
            session["theta_estimates"][dimension] = old_theta + 0.1

        # Reduce standard error (we're more certain now)
        session["se_estimates"][dimension] *= 0.8

        # Check if we need more items
        session["items_administered"].append(item_id)

        # Check stopping criteria
        if self._should_stop(session):
            session["status"] = "completed"
            session["completed_at"] = datetime.utcnow()

            return {
                "is_complete": True,
                "progress": self._calculate_progress(session_id),
                "insights": self._generate_insights(session_id),
                "question": None,
            }

        # Get next item
        next_item = self._get_next_item(session_id)

        return {
            "is_complete": False,
            "question": self._format_item_for_frontend(next_item),
            "progress": self._calculate_progress(session_id),
            "insights": self._generate_insights(session_id),
        }

    def _get_next_item(self, session_id: str) -> Dict:
        """Select next item using CAT logic"""
        session = self.sessions[session_id]

        # Get current dimension to assess
        dim_index = session["current_dimension_index"]
        current_dimension = self.dimensions[dim_index]

        # Filter items for this dimension that haven't been administered
        available_items = [
            item
            for item in self.item_bank
            if item["dimension"] == current_dimension
            and item["item_id"] not in session["items_administered"]
        ]

        if not available_items:
            # Move to next dimension
            session["current_dimension_index"] += 1
            if session["current_dimension_index"] < len(self.dimensions):
                return self._get_next_item(session_id)
            else:
                # No more items - session complete
                session["status"] = "completed"
                return None

        # Select item (simplified - real CAT would select based on information)
        selected_item = random.choice(available_items)

        return selected_item

    def _should_stop(self, session: Dict) -> bool:
        """Check if assessment should stop"""
        # Simple rule: 2 items per dimension * 7 dimensions = 14 items
        items_done = len(session["items_administered"])
        target_items = session["items_per_dimension"] * len(self.dimensions)

        return items_done >= target_items

    def _calculate_progress(self, session_id: str) -> Dict:
        """Calculate assessment progress"""
        session = self.sessions[session_id]
        items_done = len(session["items_administered"])
        target_items = session["items_per_dimension"] * len(self.dimensions)

        return {
            "items_completed": items_done,
            "estimated_remaining": max(0, target_items - items_done),
            "percentage": int((items_done / target_items) * 100),
        }

    def _generate_insights(self, session_id: str) -> List[str]:
        """Generate personality insights based on current responses"""
        session = self.sessions[session_id]
        insights = []

        # Analyze theta estimates
        for dimension, theta in session["theta_estimates"].items():
            if theta > 0.5:
                insights.append(self._get_positive_insight(dimension))
            elif theta < -0.5:
                insights.append(self._get_development_insight(dimension))

        return insights[:3]  # Return top 3 insights

    def _get_positive_insight(self, dimension: str) -> str:
        """Get positive insight for high score"""
        insights = {
            "achievement_orientation": "Ihre Antworten zeigen eine starke Leistungsorientierung",
            "risk_taking": "Sie zeigen eine gesunde Risikobereitschaft",
            "innovativeness": "Sie denken innovativ und kreativ",
            "autonomy_orientation": "Sie schätzen Unabhängigkeit und Selbstbestimmung",
            "proactiveness": "Sie handeln proaktiv und ergreifen Initiative",
            "locus_of_control": "Sie sehen sich als Gestalter Ihres Erfolgs",
            "self_efficacy": "Sie haben starkes Vertrauen in Ihre Fähigkeiten",
        }
        return insights.get(dimension, "")

    def _get_development_insight(self, dimension: str) -> str:
        """Get development insight for low score"""
        insights = {
            "achievement_orientation": "Überlegen Sie, wie Sie sich höhere Ziele setzen können",
            "risk_taking": "Kalkulierte Risiken können Wachstum ermöglichen",
            "innovativeness": "Innovation kann Wettbewerbsvorteile schaffen",
            "autonomy_orientation": "Mehr Eigenständigkeit könnte hilfreich sein",
            "proactiveness": "Proaktives Handeln führt oft zu mehr Erfolg",
            "locus_of_control": "Sie haben mehr Kontrolle als Sie denken",
            "self_efficacy": "Vertrauen in eigene Fähigkeiten ist wichtig",
        }
        return insights.get(dimension, "")

    def _format_item_for_frontend(self, item: Dict) -> Dict:
        """Format item for frontend display"""
        if not item:
            return None

        return {
            "id": item["item_id"],
            "text_de": item["text_de"],
            "dimension": item["dimension"],
            "response_scale": item["response_scale"],
        }

    def get_results(self, session_id: str) -> Dict:
        """Get final assessment results"""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")

        session = self.sessions[session_id]

        # Calculate final scores (normalized to 0-100)
        personality_profile = {}
        for dimension in self.dimensions:
            theta = session["theta_estimates"][dimension]
            # Convert theta (-3 to +3) to score (0 to 100)
            score = int(((theta + 3) / 6) * 100)
            score = max(0, min(100, score))  # Clamp to 0-100

            personality_profile[dimension] = {
                "score": score,
                "interpretation": self._interpret_score(score),
            }

        return {
            "session_id": session_id,
            "personality_profile": personality_profile,
            "business_compatibility": self._calculate_compatibility(
                personality_profile
            ),
            "gz_prediction": self._calculate_gz_prediction(personality_profile),
        }

    def _interpret_score(self, score: int) -> str:
        """Interpret score level"""
        if score >= 80:
            return "Sehr hoch"
        elif score >= 65:
            return "Hoch"
        elif score >= 50:
            return "Moderat-Hoch"
        elif score >= 35:
            return "Moderat"
        else:
            return "Entwicklungspotenzial"

    def _calculate_compatibility(self, profile: Dict) -> Dict:
        """Calculate business model compatibility"""
        # Simplified - real version would use more sophisticated matching
        return {
            "recommended_models": [
                {
                    "name": "B2B Consulting",
                    "compatibility": 0.89,
                    "gz_approval_probability": 0.87,
                },
                {
                    "name": "Professional Services",
                    "compatibility": 0.84,
                    "gz_approval_probability": 0.82,
                },
            ]
        }

    def _calculate_gz_prediction(self, profile: Dict) -> Dict:
        """Calculate Gründungszuschuss approval prediction"""
        # Calculate average score
        scores = [dim["score"] for dim in profile.values()]
        avg_score = sum(scores) / len(scores)

        # Simple mapping to approval probability
        approval_prob = (avg_score / 100) * 0.95  # Max 95% probability

        return {
            "overall_score": int(avg_score),
            "approval_probability": round(approval_prob, 2),
            "key_strengths": self._get_key_strengths(profile),
            "areas_to_address": self._get_areas_to_address(profile),
        }

    def _get_key_strengths(self, profile: Dict) -> List[str]:
        """Identify key strengths"""
        strengths = []
        for dimension, data in profile.items():
            if data["score"] >= 70:
                strengths.append(
                    f"Hohe {dimension.replace('_', ' ')}: {data['score']}/100"
                )
        return strengths[:3]

    def _get_areas_to_address(self, profile: Dict) -> List[str]:
        """Identify areas for development"""
        areas = []
        for dimension, data in profile.items():
            if data["score"] < 50:
                areas.append(
                    f"{dimension.replace('_', ' ').title()} im Businessplan betonen"
                )
        return areas[:2]
