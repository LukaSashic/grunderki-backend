"""
Personality Profiler - Maps dimension scores to entrepreneurial archetypes
Based on Howard's 7-dimension framework

This module:
- Classifies users into personality archetypes
- Generates dimension-specific interpretations
- Calculates business-type fit scores
- Creates personalized summaries
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json
from pathlib import Path
import math


@dataclass
class DimensionInterpretation:
    """Interpretation for a single dimension"""
    dimension: str
    dimension_label_de: str
    theta: float
    percentile: int
    level: str
    level_de: str
    strength: str
    watch_out: str
    business_implication: str


@dataclass
class PersonalityProfile:
    """Complete personality profile"""
    archetype_id: str
    archetype_name: str
    archetype_name_de: str
    archetype_description: str
    archetype_description_de: str
    archetype_color: str
    dimensions: Dict[str, DimensionInterpretation]
    strengths: List[str]
    strengths_de: List[str]
    watch_outs: List[str]
    watch_outs_de: List[str]
    business_fit_scores: Dict[str, int]
    overall_summary_de: str
    gz_tips_de: List[str]


class PersonalityProfiler:
    """
    Creates personality profiles from dimension scores.
    
    Maps Howard's 7 dimensions to memorable entrepreneur archetypes
    and generates actionable interpretations.
    """
    
    def __init__(self, archetypes_path: Optional[str] = None):
        """
        Initialize with archetype definitions.
        
        Args:
            archetypes_path: Path to personality_archetypes.json
        """
        if archetypes_path is None:
            archetypes_path = Path(__file__).parent / "personality_archetypes.json"
        
        with open(archetypes_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.archetypes = self.config['archetypes']
        self.dimension_order = self.config['dimension_order']
        self.dimension_labels_de = self.config['dimension_labels_de']
        self.level_thresholds = self.config['level_thresholds']
        
        # Dimension interpretations in German
        self.dimension_interpretations = self._load_dimension_interpretations()
    
    def _load_dimension_interpretations(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        """Load dimension-specific interpretations"""
        return {
            "innovativeness": {
                "very_high": {
                    "strength": "Sie sind ein Visionär, der ständig neue Möglichkeiten sieht",
                    "watch_out": "Achten Sie darauf, auch bewährte Lösungen in Betracht zu ziehen",
                    "business_implication": "Betonen Sie Ihr einzigartiges Wertversprechen und Ihre Differenzierung"
                },
                "high": {
                    "strength": "Sie entwickeln kreative Lösungen für komplexe Probleme",
                    "watch_out": "Balance zwischen Innovation und Praktikabilität finden",
                    "business_implication": "Zeigen Sie innovative Aspekte mit solider Marktvalidierung"
                },
                "medium": {
                    "strength": "Sie kombinieren bewährte Ansätze mit frischen Ideen",
                    "watch_out": "Seien Sie offen für unkonventionelle Lösungen",
                    "business_implication": "Demonstrieren Sie, wie Sie Bestehendes verbessern"
                },
                "low": {
                    "strength": "Sie setzen auf bewährte und erprobte Methoden",
                    "watch_out": "Überlegen Sie, wie Sie sich vom Wettbewerb abheben",
                    "business_implication": "Fokussieren Sie auf Qualität und Zuverlässigkeit"
                },
                "very_low": {
                    "strength": "Sie priorisieren Stabilität und Vorhersagbarkeit",
                    "watch_out": "Märkte verändern sich - bleiben Sie anpassungsfähig",
                    "business_implication": "Betonen Sie Ihre Expertise in etablierten Methoden"
                }
            },
            "risk_taking": {
                "very_high": {
                    "strength": "Sie sind bereit, für große Chancen große Risiken einzugehen",
                    "watch_out": "Kalkulierte Risiken sind besser als blinde Sprünge",
                    "business_implication": "Dokumentieren Sie Ihre Risikomanagement-Strategie sorgfältig"
                },
                "high": {
                    "strength": "Sie erkennen und nutzen Chancen, die andere meiden",
                    "watch_out": "Stellen Sie sicher, dass Sie Fallback-Pläne haben",
                    "business_implication": "Zeigen Sie, wie Sie Risiken identifizieren und managen"
                },
                "medium": {
                    "strength": "Sie gehen kalkulierte Risiken ein",
                    "watch_out": "Manchmal erfordern Chancen mutigere Entscheidungen",
                    "business_implication": "Präsentieren Sie eine ausgewogene Risiko-Chancen-Analyse"
                },
                "low": {
                    "strength": "Sie treffen vorsichtige, gut durchdachte Entscheidungen",
                    "watch_out": "Zu viel Vorsicht kann Chancen kosten",
                    "business_implication": "Betonen Sie Ihr bewährtes Geschäftsmodell und validierte Märkte"
                },
                "very_low": {
                    "strength": "Sie priorisieren Sicherheit und Stabilität",
                    "watch_out": "Unternehmertum erfordert ein gewisses Maß an Risiko",
                    "business_implication": "Zeigen Sie einen sehr detaillierten Plan mit Sicherheitsnetzen"
                }
            },
            "achievement_orientation": {
                "very_high": {
                    "strength": "Ihr Antrieb nach Exzellenz ist außergewöhnlich",
                    "watch_out": "Setzen Sie auch erreichbare Zwischenziele",
                    "business_implication": "Zeigen Sie ambitionierte aber realistische Wachstumsziele"
                },
                "high": {
                    "strength": "Sie setzen sich hohe Ziele und arbeiten hart daran",
                    "watch_out": "Balance zwischen Ehrgeiz und Wohlbefinden finden",
                    "business_implication": "Präsentieren Sie messbare Erfolgsindikatoren"
                },
                "medium": {
                    "strength": "Sie streben nach Erfolg mit realistischen Erwartungen",
                    "watch_out": "Fordern Sie sich gelegentlich etwas mehr heraus",
                    "business_implication": "Demonstrieren Sie stetige Fortschritte"
                },
                "low": {
                    "strength": "Sie setzen erreichbare, nachhaltige Ziele",
                    "watch_out": "Die Agentur erwartet sichtbares Wachstumspotenzial",
                    "business_implication": "Betonen Sie nachhaltige Profitabilität"
                },
                "very_low": {
                    "strength": "Sie fokussieren auf Stabilität statt Wachstum",
                    "watch_out": "Gründungszuschuss erfordert Wachstumsnachweis",
                    "business_implication": "Entwickeln Sie konkrete Wachstumsmeilensteine"
                }
            },
            "autonomy_orientation": {
                "very_high": {
                    "strength": "Sie sind ein geborener Unternehmer mit starkem Unabhängigkeitsdrang",
                    "watch_out": "Strategische Partnerschaften können wertvoll sein",
                    "business_implication": "Zeigen Sie, wie Ihre Unabhängigkeit Kunden nützt"
                },
                "high": {
                    "strength": "Sie bevorzugen Selbstständigkeit und eigene Entscheidungen",
                    "watch_out": "Delegation kann Wachstum ermöglichen",
                    "business_implication": "Betonen Sie Ihre Expertise als Alleinstellungsmerkmal"
                },
                "medium": {
                    "strength": "Sie balancieren Unabhängigkeit mit Zusammenarbeit",
                    "watch_out": "Definieren Sie klar, wo Sie allein und wo im Team arbeiten",
                    "business_implication": "Zeigen Sie flexible Arbeitsmodelle"
                },
                "low": {
                    "strength": "Sie arbeiten gut in kooperativen Umgebungen",
                    "watch_out": "Als Gründer müssen Sie oft allein entscheiden",
                    "business_implication": "Beschreiben Sie Ihr Unterstützungsnetzwerk"
                },
                "very_low": {
                    "strength": "Sie schätzen Teamarbeit und gemeinsame Entscheidungen",
                    "watch_out": "Selbstständigkeit erfordert oft Alleinentscheidungen",
                    "business_implication": "Zeigen Sie, wie Sie unabhängig agieren können"
                }
            },
            "proactiveness": {
                "very_high": {
                    "strength": "Sie sind immer einen Schritt voraus und antizipieren Trends",
                    "watch_out": "Manchmal ist Geduld und Timing entscheidend",
                    "business_implication": "Zeigen Sie Ihre Marktforschung und frühe Kundenvalidierung"
                },
                "high": {
                    "strength": "Sie ergreifen Initiative und warten nicht auf Gelegenheiten",
                    "watch_out": "Validieren Sie Ihre Annahmen vor dem Handeln",
                    "business_implication": "Präsentieren Sie erste Kundenanfragen oder Vorbestellungen"
                },
                "medium": {
                    "strength": "Sie handeln zum richtigen Zeitpunkt",
                    "watch_out": "Gelegentlich proaktiver sein kann Vorteile bringen",
                    "business_implication": "Demonstrieren Sie einen klaren Zeitplan für den Start"
                },
                "low": {
                    "strength": "Sie reagieren bedacht und überlegt",
                    "watch_out": "Zu langes Warten kann Chancen kosten",
                    "business_implication": "Zeigen Sie konkrete nächste Schritte mit Terminen"
                },
                "very_low": {
                    "strength": "Sie handeln erst nach gründlicher Analyse",
                    "watch_out": "Unternehmer müssen oft schnell handeln",
                    "business_implication": "Entwickeln Sie einen detaillierten Aktionsplan"
                }
            },
            "locus_of_control": {
                "very_high": {
                    "strength": "Sie glauben fest daran, Ihr Schicksal selbst zu bestimmen",
                    "watch_out": "Manche externen Faktoren sind real und wichtig",
                    "business_implication": "Zeigen Sie, wie Sie auf verschiedene Szenarien vorbereitet sind"
                },
                "high": {
                    "strength": "Sie übernehmen volle Verantwortung für Ihre Ergebnisse",
                    "watch_out": "Akzeptieren Sie auch externe Einflüsse",
                    "business_implication": "Demonstrieren Sie Ihre Anpassungsfähigkeit"
                },
                "medium": {
                    "strength": "Sie balancieren eigene Kontrolle mit externen Faktoren",
                    "watch_out": "Fokussieren Sie auf das, was Sie beeinflussen können",
                    "business_implication": "Zeigen Sie proaktives Risikomanagement"
                },
                "low": {
                    "strength": "Sie sind realistisch bezüglich externer Einflüsse",
                    "watch_out": "Glauben Sie mehr an Ihre eigene Handlungsfähigkeit",
                    "business_implication": "Betonen Sie Ihre Strategien zur Risikosteuerung"
                },
                "very_low": {
                    "strength": "Sie berücksichtigen viele externe Faktoren",
                    "watch_out": "Unternehmer müssen an eigene Wirksamkeit glauben",
                    "business_implication": "Entwickeln Sie Strategien für verschiedene Szenarien"
                }
            },
            "self_efficacy": {
                "very_high": {
                    "strength": "Sie haben außergewöhnliches Selbstvertrauen in Ihre Fähigkeiten",
                    "watch_out": "Bleiben Sie offen für Feedback und Lernmöglichkeiten",
                    "business_implication": "Zeigen Sie konkrete Erfolge aus der Vergangenheit"
                },
                "high": {
                    "strength": "Sie glauben fest an Ihre Fähigkeit, erfolgreich zu sein",
                    "watch_out": "Unterschätzen Sie Herausforderungen nicht",
                    "business_implication": "Präsentieren Sie Ihre relevante Erfahrung und Erfolge"
                },
                "medium": {
                    "strength": "Sie haben ein gesundes Selbstvertrauen",
                    "watch_out": "Trauen Sie sich mehr zu",
                    "business_implication": "Betonen Sie Ihre übertragbaren Fähigkeiten"
                },
                "low": {
                    "strength": "Sie sind bescheiden und selbstreflektiert",
                    "watch_out": "Mehr Selbstvertrauen kann Türen öffnen",
                    "business_implication": "Dokumentieren Sie alle relevanten Qualifikationen"
                },
                "very_low": {
                    "strength": "Sie sind sehr selbstkritisch",
                    "watch_out": "Gründer brauchen Überzeugung von ihren Fähigkeiten",
                    "business_implication": "Sammeln Sie Referenzen und Empfehlungen"
                }
            }
        }
    
    def _get_level(self, percentile: int) -> str:
        """Convert percentile to level string"""
        if percentile >= self.level_thresholds['very_high']:
            return 'very_high'
        elif percentile >= self.level_thresholds['high']:
            return 'high'
        elif percentile >= self.level_thresholds['medium']:
            return 'medium'
        elif percentile >= self.level_thresholds['low']:
            return 'low'
        else:
            return 'very_low'
    
    def _get_level_de(self, level: str) -> str:
        """Get German label for level"""
        level_labels = {
            'very_high': 'Sehr hoch',
            'high': 'Hoch',
            'medium': 'Mittel',
            'low': 'Niedrig',
            'very_low': 'Sehr niedrig'
        }
        return level_labels.get(level, 'Mittel')
    
    def _calculate_distance(self, score_vector: List[float], prototype: List[int]) -> float:
        """Calculate Euclidean distance between score vector and prototype"""
        if len(score_vector) != len(prototype):
            raise ValueError("Score vector and prototype must have same length")
        
        squared_diff_sum = sum(
            (s - p) ** 2 
            for s, p in zip(score_vector, prototype)
        )
        return math.sqrt(squared_diff_sum)
    
    def determine_archetype(
        self, 
        dimension_scores: Dict[str, Dict[str, float]]
    ) -> Dict[str, Any]:
        """
        Determine best-fitting archetype based on dimension scores.
        
        Uses Euclidean distance to archetype prototypes.
        
        Args:
            dimension_scores: Dict with dimension names as keys,
                            each containing 'percentile' value
        
        Returns:
            Best matching archetype definition
        """
        # Build score vector in correct order
        score_vector = []
        for dim in self.dimension_order:
            if dim in dimension_scores:
                score_vector.append(dimension_scores[dim]['percentile'])
            else:
                score_vector.append(50)  # Default to median
        
        # Find closest archetype
        min_distance = float('inf')
        best_archetype = self.archetypes[0]  # Default
        
        for archetype in self.archetypes:
            distance = self._calculate_distance(score_vector, archetype['prototype'])
            if distance < min_distance:
                min_distance = distance
                best_archetype = archetype
        
        return best_archetype
    
    def _interpret_dimension(
        self,
        dimension: str,
        theta: float,
        percentile: int
    ) -> DimensionInterpretation:
        """Generate interpretation for a single dimension"""
        level = self._get_level(percentile)
        level_de = self._get_level_de(level)
        
        interpretation = self.dimension_interpretations.get(dimension, {}).get(level, {
            "strength": "Ausgewogene Ausprägung",
            "watch_out": "Keine besonderen Hinweise",
            "business_implication": "Standard-Empfehlung"
        })
        
        return DimensionInterpretation(
            dimension=dimension,
            dimension_label_de=self.dimension_labels_de.get(dimension, dimension),
            theta=theta,
            percentile=percentile,
            level=level,
            level_de=level_de,
            strength=interpretation['strength'],
            watch_out=interpretation['watch_out'],
            business_implication=interpretation['business_implication']
        )
    
    def _calculate_business_fit(
        self,
        dimension_scores: Dict[str, Dict[str, float]]
    ) -> Dict[str, int]:
        """
        Calculate fit scores for different business types.
        
        Uses research-based weights for each business type.
        """
        # Research-based weights
        weights = {
            "restaurant": {
                "innovativeness": 0.15,
                "risk_taking": 0.10,
                "achievement_orientation": 0.20,
                "autonomy_orientation": 0.10,
                "proactiveness": 0.20,
                "locus_of_control": 0.15,
                "self_efficacy": 0.10
            },
            "saas": {
                "innovativeness": 0.25,
                "risk_taking": 0.20,
                "achievement_orientation": 0.15,
                "autonomy_orientation": 0.05,
                "proactiveness": 0.20,
                "locus_of_control": 0.10,
                "self_efficacy": 0.05
            },
            "consulting": {
                "innovativeness": 0.10,
                "risk_taking": 0.10,
                "achievement_orientation": 0.25,
                "autonomy_orientation": 0.15,
                "proactiveness": 0.15,
                "locus_of_control": 0.15,
                "self_efficacy": 0.10
            },
            "ecommerce": {
                "innovativeness": 0.15,
                "risk_taking": 0.15,
                "achievement_orientation": 0.20,
                "autonomy_orientation": 0.10,
                "proactiveness": 0.25,
                "locus_of_control": 0.10,
                "self_efficacy": 0.05
            },
            "services": {
                "innovativeness": 0.10,
                "risk_taking": 0.10,
                "achievement_orientation": 0.20,
                "autonomy_orientation": 0.15,
                "proactiveness": 0.15,
                "locus_of_control": 0.15,
                "self_efficacy": 0.15
            },
            "creative": {
                "innovativeness": 0.30,
                "risk_taking": 0.15,
                "achievement_orientation": 0.15,
                "autonomy_orientation": 0.20,
                "proactiveness": 0.10,
                "locus_of_control": 0.05,
                "self_efficacy": 0.05
            }
        }
        
        fit_scores = {}
        for business_type, type_weights in weights.items():
            fit_score = sum(
                dimension_scores.get(dim, {}).get('percentile', 50) * weight
                for dim, weight in type_weights.items()
            )
            fit_scores[business_type] = int(fit_score)
        
        return fit_scores
    
    def _generate_summary(
        self,
        archetype: Dict[str, Any],
        dimension_interpretations: Dict[str, DimensionInterpretation],
        business_context: Dict[str, Any]
    ) -> str:
        """Generate personalized German summary"""
        archetype_name = archetype['name_de']
        business_type = business_context.get('business_type', 'Geschäft')
        
        # Find top strengths (percentile >= 65)
        strengths = [
            interp.dimension_label_de
            for interp in dimension_interpretations.values()
            if interp.percentile >= 65
        ]
        
        # Find development areas (percentile < 40)
        development = [
            interp.dimension_label_de
            for interp in dimension_interpretations.values()
            if interp.percentile < 40
        ]
        
        # Build summary
        summary_parts = [f"Als {archetype_name} "]
        
        if strengths:
            if len(strengths) == 1:
                summary_parts.append(f"ist Ihre Stärke die {strengths[0]}. ")
            else:
                summary_parts.append(f"liegen Ihre Stärken in {', '.join(strengths[:2])}. ")
        
        if development:
            if len(development) == 1:
                summary_parts.append(f"Achten Sie besonders auf {development[0]}. ")
            else:
                summary_parts.append(f"Entwicklungspotenzial besteht bei {', '.join(development[:2])}. ")
        
        summary_parts.append(
            f"Für Ihr {business_type} bedeutet das: Nutzen Sie Ihre natürlichen Stärken "
            f"und arbeiten Sie gezielt an den identifizierten Bereichen."
        )
        
        return ''.join(summary_parts)
    
    def create_profile(
        self,
        dimension_scores: Dict[str, Dict[str, float]],
        business_context: Dict[str, Any]
    ) -> PersonalityProfile:
        """
        Create complete personality profile.
        
        Args:
            dimension_scores: Dict with 7 dimensions, each containing
                            'theta' and 'percentile' values
            business_context: User's business information
        
        Returns:
            Complete PersonalityProfile object
        """
        # Determine archetype
        archetype = self.determine_archetype(dimension_scores)
        
        # Generate dimension interpretations
        dim_interpretations = {}
        for dim, scores in dimension_scores.items():
            dim_interpretations[dim] = self._interpret_dimension(
                dim,
                scores.get('theta', 0.0),
                scores.get('percentile', 50)
            )
        
        # Calculate business fit scores
        business_fit = self._calculate_business_fit(dimension_scores)
        
        # Generate summary
        summary = self._generate_summary(archetype, dim_interpretations, business_context)
        
        return PersonalityProfile(
            archetype_id=archetype['id'],
            archetype_name=archetype['name'],
            archetype_name_de=archetype['name_de'],
            archetype_description=archetype['description'],
            archetype_description_de=archetype['description_de'],
            archetype_color=archetype['color'],
            dimensions=dim_interpretations,
            strengths=archetype['strengths'],
            strengths_de=archetype['strengths_de'],
            watch_outs=archetype['watch_outs'],
            watch_outs_de=archetype['watch_outs_de'],
            business_fit_scores=business_fit,
            overall_summary_de=summary,
            gz_tips_de=archetype['gz_tips_de']
        )
    
    def profile_to_dict(self, profile: PersonalityProfile) -> Dict[str, Any]:
        """Convert PersonalityProfile to dictionary for JSON serialization"""
        return {
            "archetype": {
                "id": profile.archetype_id,
                "name": profile.archetype_name,
                "name_de": profile.archetype_name_de,
                "description": profile.archetype_description,
                "description_de": profile.archetype_description_de,
                "color": profile.archetype_color
            },
            "dimensions": {
                dim: {
                    "label_de": interp.dimension_label_de,
                    "theta": interp.theta,
                    "percentile": interp.percentile,
                    "level": interp.level,
                    "level_de": interp.level_de,
                    "interpretation": {
                        "strength": interp.strength,
                        "watch_out": interp.watch_out,
                        "business_implication": interp.business_implication
                    }
                }
                for dim, interp in profile.dimensions.items()
            },
            "strengths": profile.strengths,
            "strengths_de": profile.strengths_de,
            "watch_outs": profile.watch_outs,
            "watch_outs_de": profile.watch_outs_de,
            "business_fit_scores": profile.business_fit_scores,
            "overall_summary_de": profile.overall_summary_de,
            "gz_tips_de": profile.gz_tips_de
        }
