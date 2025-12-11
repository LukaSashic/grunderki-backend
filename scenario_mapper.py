"""
Scenario Mapper - Maps scenario responses to IRT theta estimates
Based on Howard's 7-dimension entrepreneurial personality framework
"""

from typing import Dict, List, Tuple, Optional, Any
import math
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class DimensionEstimate:
    """Track theta estimate for a single dimension."""
    theta: float = 0.0  # Current ability estimate
    se: float = 2.0     # Standard error (high = uncertain)
    n_items: int = 0    # Number of items answered
    responses: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            'theta': round(self.theta, 3),
            'se': round(self.se, 3),
            'n_items': self.n_items,
            'confidence': self._calculate_confidence()
        }
    
    def _calculate_confidence(self) -> str:
        """Convert SE to human-readable confidence level."""
        if self.se > 1.0:
            return 'low'
        elif self.se > 0.5:
            return 'moderate'
        elif self.se > 0.3:
            return 'good'
        else:
            return 'high'


class ScenarioMapper:
    """
    Maps user responses to scenarios back to IRT theta values.
    
    Key Responsibilities:
    - Convert option selection (A/B/C/D) to theta estimate
    - Calculate information provided by each response
    - Update running theta estimates using EAP (Expected A Posteriori)
    - Track dimension-specific response patterns
    - Convert theta to percentile for user display
    """
    
    def __init__(self):
        """Initialize mapper with prior distribution parameters."""
        # Prior distribution: N(0, 1) for theta
        self.prior_mean = 0.0
        self.prior_var = 1.0
        
        # Theta bounds for numerical stability
        self.theta_min = -3.0
        self.theta_max = 3.0
        
        # Dimension interpretations for user feedback
        self.dimension_labels = {
            'innovativeness': 'Innovationsfreude',
            'risk_taking': 'Risikobereitschaft',
            'achievement_orientation': 'Leistungsorientierung',
            'autonomy_orientation': 'Autonomiestreben',
            'proactiveness': 'Proaktivität',
            'locus_of_control': 'Kontrollüberzeugung',
            'self_efficacy': 'Selbstwirksamkeit'
        }
    
    def map_response_to_theta(
        self,
        scenario: Dict[str, Any],
        selected_option_id: str
    ) -> Tuple[float, float]:
        """
        Map user's option selection to theta value and information.
        
        Unlike traditional IRT where responses are scored, our scenarios
        have direct theta mappings for each option.
        
        Args:
            scenario: The scenario that was presented
            selected_option_id: The option ID selected (A/B/C/D)
            
        Returns:
            Tuple of (theta_value, information)
        """
        # Find the selected option
        selected_option = None
        for option in scenario['template']['options']:
            if option['id'] == selected_option_id:
                selected_option = option
                break
        
        if selected_option is None:
            raise ValueError(f"Invalid option ID: {selected_option_id}")
        
        # Get theta value directly from option
        theta_value = selected_option['theta_value']
        
        # Calculate information (based on discrimination and how far from extremes)
        discrimination = scenario.get('discrimination', 1.5)
        information = self._calculate_information(
            discrimination=discrimination,
            theta_selected=theta_value,
            scenario_difficulty=scenario.get('difficulty', 0.0)
        )
        
        return theta_value, information
    
    def _calculate_information(
        self,
        discrimination: float,
        theta_selected: float,
        scenario_difficulty: float
    ) -> float:
        """
        Calculate Fisher information for this response.
        
        Information is highest when:
        - Discrimination is high
        - Response is near scenario difficulty (good targeting)
        
        Formula: I = a² * P * (1 - P) where P depends on theta-difficulty match
        """
        # Simplified information calculation
        # Higher discrimination = more informative
        # Better match between response and difficulty = more informative
        
        match_quality = 1.0 - min(1.0, abs(theta_selected - scenario_difficulty) / 3.0)
        
        # Base information from discrimination
        base_info = discrimination ** 2
        
        # Scale by match quality (0.5 to 1.0 multiplier)
        info = base_info * (0.5 + 0.5 * match_quality)
        
        return info
    
    def update_theta_estimate(
        self,
        current_estimate: DimensionEstimate,
        new_theta: float,
        information: float
    ) -> DimensionEstimate:
        """
        Update theta estimate using weighted combination.
        
        Uses a Bayesian-inspired approach:
        - Prior: Current estimate weighted by its precision (1/SE²)
        - Likelihood: New response weighted by its information
        
        Args:
            current_estimate: Current dimension estimate
            new_theta: Theta from new response
            information: Information from new response
            
        Returns:
            Updated dimension estimate
        """
        # Convert SE to precision (inverse variance)
        current_precision = 1.0 / (current_estimate.se ** 2) if current_estimate.n_items > 0 else 0.0
        
        # New response precision is approximately its information
        new_precision = information
        
        # Combined precision
        total_precision = current_precision + new_precision
        
        if total_precision > 0:
            # Weighted average of theta estimates
            if current_estimate.n_items > 0:
                new_theta_estimate = (
                    current_estimate.theta * current_precision + 
                    new_theta * new_precision
                ) / total_precision
            else:
                # First item - use prior
                prior_precision = 1.0 / self.prior_var
                new_theta_estimate = (
                    self.prior_mean * prior_precision + 
                    new_theta * new_precision
                ) / (prior_precision + new_precision)
            
            # New SE is sqrt(1 / total_precision)
            new_se = math.sqrt(1.0 / total_precision)
        else:
            # Edge case - shouldn't happen
            new_theta_estimate = new_theta
            new_se = 2.0
        
        # Clamp theta to bounds
        new_theta_estimate = max(self.theta_min, min(self.theta_max, new_theta_estimate))
        
        # Create updated estimate
        updated = DimensionEstimate(
            theta=new_theta_estimate,
            se=new_se,
            n_items=current_estimate.n_items + 1,
            responses=current_estimate.responses + [{
                'theta': new_theta,
                'info': information,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }]
        )
        
        return updated
    
    def convert_theta_to_percentile(self, theta: float) -> int:
        """
        Convert theta to percentile rank.
        
        Assumes theta ~ N(0, 1) in population.
        
        Args:
            theta: Ability estimate
            
        Returns:
            Percentile (0-100)
        """
        # Use cumulative distribution function
        # For N(0,1), CDF at theta gives proportion below theta
        
        # Approximation of standard normal CDF
        z = theta
        
        # Zelen & Severo approximation
        if z >= 0:
            t = 1.0 / (1.0 + 0.2316419 * z)
            d = 0.3989422804 * math.exp(-z * z / 2.0)
            p = 1.0 - d * t * (
                0.3193815 + t * (
                    -0.3565638 + t * (
                        1.781478 + t * (
                            -1.821256 + t * 1.330274
                        )
                    )
                )
            )
        else:
            t = 1.0 / (1.0 - 0.2316419 * z)
            d = 0.3989422804 * math.exp(-z * z / 2.0)
            p = d * t * (
                0.3193815 + t * (
                    -0.3565638 + t * (
                        1.781478 + t * (
                            -1.821256 + t * 1.330274
                        )
                    )
                )
            )
        
        percentile = int(round(p * 100))
        return max(1, min(99, percentile))  # Clamp to 1-99
    
    def convert_theta_to_score(self, theta: float) -> int:
        """
        Convert theta to 0-100 score for display.
        
        Maps [-3, +3] theta range to [0, 100] score.
        
        Args:
            theta: Ability estimate
            
        Returns:
            Score (0-100)
        """
        # Linear mapping from [-3, 3] to [0, 100]
        score = int(((theta - self.theta_min) / (self.theta_max - self.theta_min)) * 100)
        return max(0, min(100, score))
    
    def interpret_dimension_score(
        self,
        dimension: str,
        theta: float,
        business_context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Generate human-readable interpretation of dimension score.
        
        Args:
            dimension: Howard dimension name
            theta: Theta estimate
            business_context: Optional context for tailored interpretation
            
        Returns:
            Interpretation with strength, description, and implications
        """
        percentile = self.convert_theta_to_percentile(theta)
        score = self.convert_theta_to_score(theta)
        label = self.dimension_labels.get(dimension, dimension)
        
        # Determine level
        if theta >= 1.5:
            level = 'sehr_hoch'
            level_de = 'Sehr Hoch'
        elif theta >= 0.5:
            level = 'hoch'
            level_de = 'Hoch'
        elif theta >= -0.5:
            level = 'moderat'
            level_de = 'Moderat'
        elif theta >= -1.5:
            level = 'niedrig'
            level_de = 'Niedrig'
        else:
            level = 'sehr_niedrig'
            level_de = 'Sehr Niedrig'
        
        # Get dimension-specific interpretation
        interpretation = self._get_interpretation_text(dimension, level, business_context)
        
        return {
            'dimension': dimension,
            'dimension_label': label,
            'theta': round(theta, 2),
            'percentile': percentile,
            'score': score,
            'level': level,
            'level_de': level_de,
            'strength': interpretation['strength'],
            'description': interpretation['description'],
            'business_implication': interpretation['implication'],
            'development_tip': interpretation.get('tip', None)
        }
    
    def _get_interpretation_text(
        self,
        dimension: str,
        level: str,
        context: Optional[Dict] = None
    ) -> Dict[str, str]:
        """Get localized interpretation text for dimension and level."""
        
        interpretations = {
            'innovativeness': {
                'sehr_hoch': {
                    'strength': 'Disruptives Denken',
                    'description': 'Sie suchen aktiv nach völlig neuen Lösungen und hinterfragen etablierte Ansätze.',
                    'implication': 'Stark für Startups in neuen Märkten, kann in traditionellen Branchen anecken.',
                    'tip': None
                },
                'hoch': {
                    'strength': 'Kreative Problemlösung',
                    'description': 'Sie kombinieren gerne Bestehendes neu und entwickeln innovative Varianten.',
                    'implication': 'Gute Balance zwischen Innovation und Praxistauglichkeit.',
                    'tip': None
                },
                'moderat': {
                    'strength': 'Pragmatische Verbesserung',
                    'description': 'Sie optimieren Bestehendes und sind offen für bewährte Innovationen.',
                    'implication': 'Solide Basis, könnte von mehr Experimentierfreude profitieren.',
                    'tip': 'Reservieren Sie Zeit für kreative Experimente ohne sofortigen ROI-Druck.'
                },
                'niedrig': {
                    'strength': 'Bewährte Methoden',
                    'description': 'Sie bevorzugen erprobte Ansätze und vermeiden unnötige Risiken.',
                    'implication': 'Gut für etablierte Geschäftsmodelle, könnte Differenzierung erschweren.',
                    'tip': 'Betonen Sie im Businessplan, wie Sie sich vom Wettbewerb abheben.'
                },
                'sehr_niedrig': {
                    'strength': 'Traditioneller Ansatz',
                    'description': 'Sie setzen auf das Bewährte und kopieren erfolgreiche Modelle.',
                    'implication': 'Differenzierung ist kritisch - Gutachter wollen Alleinstellungsmerkmale sehen.',
                    'tip': 'Arbeiten Sie Ihr USP klar heraus, auch wenn das Geschäftsmodell klassisch ist.'
                }
            },
            'risk_taking': {
                'sehr_hoch': {
                    'strength': 'Unternehmerischer Mut',
                    'description': 'Sie sind bereit, große Risiken für große Chancen einzugehen.',
                    'implication': 'Hohes Wachstumspotenzial, aber zeigen Sie Risikobewusstsein im Businessplan.',
                    'tip': 'Dokumentieren Sie Ihre Risikoanalyse und Absicherungsstrategien.'
                },
                'hoch': {
                    'strength': 'Kalkulierte Risikobereitschaft',
                    'description': 'Sie wägen Chancen und Risiken ab und handeln dann entschlossen.',
                    'implication': 'Ideales Profil für Gründer - mutig, aber nicht leichtsinnig.',
                    'tip': None
                },
                'moderat': {
                    'strength': 'Ausgewogene Entscheidungen',
                    'description': 'Sie sichern sich ab, bevor Sie Risiken eingehen.',
                    'implication': 'Solide Basis, aber zeigen Sie auch Entschlusskraft.',
                    'tip': 'Betonen Sie Ihre Fähigkeit, wichtige Entscheidungen zu treffen.'
                },
                'niedrig': {
                    'strength': 'Sicherheitsorientierung',
                    'description': 'Sie minimieren Risiken und bevorzugen sichere Optionen.',
                    'implication': 'Gut für stabile Branchen, kann bei Investoren als mangelnder Drive wirken.',
                    'tip': 'Zeigen Sie im Businessplan, dass Sie handlungsfähig sind.'
                },
                'sehr_niedrig': {
                    'strength': 'Maximale Absicherung',
                    'description': 'Sie vermeiden Risiken so weit wie möglich.',
                    'implication': 'Gründung ist per se riskant - Gutachter wollen sehen, dass Sie das akzeptieren.',
                    'tip': 'Arbeiten Sie an Ihrer Darstellung unternehmerischer Entschlossenheit.'
                }
            },
            'achievement_orientation': {
                'sehr_hoch': {
                    'strength': 'Exzellenzstreben',
                    'description': 'Sie setzen sich hohe Ziele und ruhen nicht, bis Sie sie übertreffen.',
                    'implication': 'Starker Antrieb, kann zu Überarbeitung führen.',
                    'tip': None
                },
                'hoch': {
                    'strength': 'Leistungsmotivation',
                    'description': 'Sie streben nach Verbesserung und messen sich an hohen Standards.',
                    'implication': 'Ideales Profil für nachhaltiges Wachstum.',
                    'tip': None
                },
                'moderat': {
                    'strength': 'Realistische Ziele',
                    'description': 'Sie setzen erreichbare Ziele und arbeiten stetig darauf hin.',
                    'implication': 'Solide, aber zeigen Sie im Businessplan ambitionierte Ziele.',
                    'tip': 'Formulieren Sie messbare, ambitionierte Meilensteine.'
                },
                'niedrig': {
                    'strength': 'Work-Life-Balance',
                    'description': 'Sie priorisieren Zufriedenheit über maximale Leistung.',
                    'implication': 'Gutachter wollen Ehrgeiz sehen - betonen Sie Ihre Motivation.',
                    'tip': 'Zeigen Sie Ihre langfristige Vision und was Sie antreibt.'
                },
                'sehr_niedrig': {
                    'strength': 'Genügsamkeit',
                    'description': 'Sie sind zufrieden, wenn das Grundlegende funktioniert.',
                    'implication': 'Kritisch für Gründungszuschuss - zeigen Sie unternehmerischen Ehrgeiz.',
                    'tip': 'Arbeiten Sie im Businessplan Ihre Wachstumsziele klar heraus.'
                }
            },
            'autonomy_orientation': {
                'sehr_hoch': {
                    'strength': 'Absolute Unabhängigkeit',
                    'description': 'Sie entscheiden selbst und lehnen externe Einflussnahme ab.',
                    'implication': 'Gut für Solopreneure, kann Partnerschaften erschweren.',
                    'tip': None
                },
                'hoch': {
                    'strength': 'Selbstbestimmung',
                    'description': 'Sie schätzen Unabhängigkeit und treffen eigene Entscheidungen.',
                    'implication': 'Ideales Gründerprofil - selbstständig und zielorientiert.',
                    'tip': None
                },
                'moderat': {
                    'strength': 'Flexible Zusammenarbeit',
                    'description': 'Sie können allein und im Team arbeiten.',
                    'implication': 'Vielseitig einsetzbar, gut für verschiedene Geschäftsmodelle.',
                    'tip': None
                },
                'niedrig': {
                    'strength': 'Teamorientierung',
                    'description': 'Sie arbeiten gerne mit anderen und teilen Entscheidungen.',
                    'implication': 'Zeigen Sie, dass Sie als Gründer führen können.',
                    'tip': 'Betonen Sie Ihre Fähigkeit, Verantwortung zu übernehmen.'
                },
                'sehr_niedrig': {
                    'strength': 'Starke Zusammenarbeit',
                    'description': 'Sie bevorzugen gemeinsame Entscheidungen und Strukturen.',
                    'implication': 'Als Gründer müssen Sie führen - zeigen Sie Ihre Entscheidungsfähigkeit.',
                    'tip': 'Arbeiten Sie Ihre Rolle als alleinverantwortlicher Gründer klar heraus.'
                }
            },
            'proactiveness': {
                'sehr_hoch': {
                    'strength': 'Marktgestaltung',
                    'description': 'Sie schaffen Trends statt ihnen zu folgen.',
                    'implication': 'Starkes First-Mover-Potenzial.',
                    'tip': None
                },
                'hoch': {
                    'strength': 'Initiative',
                    'description': 'Sie ergreifen Chancen bevor andere sie sehen.',
                    'implication': 'Exzellent für schnelllebige Märkte.',
                    'tip': None
                },
                'moderat': {
                    'strength': 'Aktives Handeln',
                    'description': 'Sie reagieren schnell auf Chancen und Herausforderungen.',
                    'implication': 'Solide Basis, könnte von mehr Vorausplanung profitieren.',
                    'tip': 'Zeigen Sie im Businessplan proaktive Marktstrategien.'
                },
                'niedrig': {
                    'strength': 'Reaktive Anpassung',
                    'description': 'Sie warten ab und reagieren auf Entwicklungen.',
                    'implication': 'Gutachter wollen Initiative sehen.',
                    'tip': 'Betonen Sie Ihre Pläne zur aktiven Kundengewinnung.'
                },
                'sehr_niedrig': {
                    'strength': 'Abwartende Haltung',
                    'description': 'Sie lassen die Dinge auf sich zukommen.',
                    'implication': 'Kritisch - zeigen Sie aktive Marktbearbeitung.',
                    'tip': 'Entwickeln Sie einen konkreten Aktionsplan für die ersten 6 Monate.'
                }
            },
            'locus_of_control': {
                'sehr_hoch': {
                    'strength': 'Volle Eigenverantwortung',
                    'description': 'Sie sehen sich als alleiniger Gestalter Ihres Erfolgs.',
                    'implication': 'Starke Handlungsorientierung, aber externe Faktoren nicht ignorieren.',
                    'tip': None
                },
                'hoch': {
                    'strength': 'Interne Kontrolle',
                    'description': 'Sie glauben, dass Ihr Erfolg von Ihren Handlungen abhängt.',
                    'implication': 'Ideale Einstellung für Unternehmer.',
                    'tip': None
                },
                'moderat': {
                    'strength': 'Realistische Einschätzung',
                    'description': 'Sie sehen sowohl eigene als auch externe Einflussfaktoren.',
                    'implication': 'Ausgewogen, aber zeigen Sie Gestaltungswillen.',
                    'tip': 'Betonen Sie, wie Sie Herausforderungen aktiv angehen.'
                },
                'niedrig': {
                    'strength': 'Umweltbewusstsein',
                    'description': 'Sie erkennen viele externe Einflussfaktoren.',
                    'implication': 'Zeigen Sie, dass Sie trotzdem handlungsfähig sind.',
                    'tip': 'Formulieren Sie im Businessplan Ihre Strategien zur Risikobewältigung.'
                },
                'sehr_niedrig': {
                    'strength': 'Externe Attribution',
                    'description': 'Sie sehen Erfolg stark von äußeren Faktoren abhängig.',
                    'implication': 'Kritisch für Gründer - zeigen Sie Eigenverantwortung.',
                    'tip': 'Arbeiten Sie heraus, welche Faktoren SIE kontrollieren und gestalten.'
                }
            },
            'self_efficacy': {
                'sehr_hoch': {
                    'strength': 'Unerschütterliches Selbstvertrauen',
                    'description': 'Sie sind überzeugt, jede Herausforderung meistern zu können.',
                    'implication': 'Starke Resilienz, aber offen für Feedback bleiben.',
                    'tip': None
                },
                'hoch': {
                    'strength': 'Selbstvertrauen',
                    'description': 'Sie vertrauen auf Ihre Fähigkeiten und lernen schnell.',
                    'implication': 'Ideale Voraussetzung für Gründer.',
                    'tip': None
                },
                'moderat': {
                    'strength': 'Realistische Selbsteinschätzung',
                    'description': 'Sie kennen Ihre Stärken und arbeiten an Schwächen.',
                    'implication': 'Solide Basis, mehr Selbstvertrauen kann helfen.',
                    'tip': 'Dokumentieren Sie Ihre relevanten Erfolge und Kompetenzen.'
                },
                'niedrig': {
                    'strength': 'Lernbereitschaft',
                    'description': 'Sie wissen, dass Sie noch viel lernen müssen.',
                    'implication': 'Zeigen Sie im Businessplan Ihre vorhandenen Kompetenzen.',
                    'tip': 'Listen Sie Ihre relevanten Qualifikationen und Erfahrungen auf.'
                },
                'sehr_niedrig': {
                    'strength': 'Bescheidenheit',
                    'description': 'Sie unterschätzen möglicherweise Ihre Fähigkeiten.',
                    'implication': 'Kritisch - Gutachter wollen sehen, dass Sie es schaffen können.',
                    'tip': 'Arbeiten Sie Ihre Stärken und Erfolge klar heraus.'
                }
            }
        }
        
        dim_interp = interpretations.get(dimension, {})
        level_interp = dim_interp.get(level, {
            'strength': 'Keine Interpretation verfügbar',
            'description': '',
            'implication': '',
            'tip': None
        })
        
        return level_interp
    
    def calculate_overall_profile(
        self,
        dimension_estimates: Dict[str, DimensionEstimate]
    ) -> Dict[str, Any]:
        """
        Calculate overall personality profile from dimension estimates.
        
        Args:
            dimension_estimates: Dict of dimension -> DimensionEstimate
            
        Returns:
            Complete profile with scores, interpretations, and recommendations
        """
        profile = {
            'dimensions': {},
            'summary': {},
            'gz_readiness': {}
        }
        
        total_theta = 0
        count = 0
        
        for dimension, estimate in dimension_estimates.items():
            interpretation = self.interpret_dimension_score(dimension, estimate.theta)
            profile['dimensions'][dimension] = {
                **interpretation,
                'se': round(estimate.se, 3),
                'n_items': estimate.n_items
            }
            total_theta += estimate.theta
            count += 1
        
        # Calculate summary statistics
        if count > 0:
            avg_theta = total_theta / count
            profile['summary'] = {
                'average_theta': round(avg_theta, 2),
                'average_percentile': self.convert_theta_to_percentile(avg_theta),
                'average_score': self.convert_theta_to_score(avg_theta)
            }
            
            # GZ readiness assessment
            profile['gz_readiness'] = self._calculate_gz_readiness(dimension_estimates)
        
        return profile
    
    def _calculate_gz_readiness(
        self,
        estimates: Dict[str, DimensionEstimate]
    ) -> Dict[str, Any]:
        """Calculate Gründungszuschuss approval readiness."""
        
        # Key dimensions for GZ approval (weighted)
        weights = {
            'achievement_orientation': 0.20,
            'proactiveness': 0.20,
            'self_efficacy': 0.15,
            'risk_taking': 0.15,
            'innovativeness': 0.10,
            'autonomy_orientation': 0.10,
            'locus_of_control': 0.10
        }
        
        weighted_sum = 0
        total_weight = 0
        
        strengths = []
        development_areas = []
        
        for dimension, estimate in estimates.items():
            weight = weights.get(dimension, 0.1)
            weighted_sum += estimate.theta * weight
            total_weight += weight
            
            if estimate.theta >= 0.5:
                strengths.append(self.dimension_labels.get(dimension, dimension))
            elif estimate.theta <= -0.5:
                development_areas.append(self.dimension_labels.get(dimension, dimension))
        
        weighted_avg = weighted_sum / total_weight if total_weight > 0 else 0
        
        # Convert to approval probability estimate (0-100%)
        # Theta of 1.0 = ~85% probability, 0 = ~65%, -1 = ~45%
        base_prob = 65
        adjustment = weighted_avg * 20  # ±20% adjustment per theta unit
        approval_prob = max(20, min(95, base_prob + adjustment))
        
        return {
            'approval_probability': round(approval_prob),
            'weighted_score': round(weighted_avg, 2),
            'strengths': strengths[:3],
            'development_areas': development_areas[:2],
            'recommendation': self._get_gz_recommendation(approval_prob)
        }
    
    def _get_gz_recommendation(self, prob: float) -> str:
        """Get recommendation text based on approval probability."""
        if prob >= 80:
            return "Ausgezeichnetes Profil für den Gründungszuschuss. Fokussieren Sie sich auf einen starken Businessplan."
        elif prob >= 65:
            return "Gutes Gründerprofil. Der Businessplan sollte Ihre Stärken betonen und Entwicklungsbereiche adressieren."
        elif prob >= 50:
            return "Solides Potenzial. Arbeiten Sie die gekennzeichneten Bereiche im Businessplan gezielt aus."
        else:
            return "Entwicklungspotenzial vorhanden. Nutzen Sie den Businessplan, um Ihre Gründungsfähigkeit zu demonstrieren."


if __name__ == "__main__":
    # Test the mapper
    mapper = ScenarioMapper()
    
    # Test theta to percentile conversion
    print("=== Theta to Percentile Test ===")
    for theta in [-2.0, -1.0, 0.0, 1.0, 2.0]:
        percentile = mapper.convert_theta_to_percentile(theta)
        score = mapper.convert_theta_to_score(theta)
        print(f"Theta {theta:+.1f} -> Percentile {percentile}, Score {score}")
    
    # Test response mapping
    print("\n=== Response Mapping Test ===")
    test_scenario = {
        'scenario_id': 'TEST_001',
        'dimension': 'innovativeness',
        'difficulty': 0.0,
        'discrimination': 1.7,
        'template': {
            'options': [
                {'id': 'A', 'text': 'Option A', 'theta_value': -1.8},
                {'id': 'B', 'text': 'Option B', 'theta_value': -0.5},
                {'id': 'C', 'text': 'Option C', 'theta_value': 0.7},
                {'id': 'D', 'text': 'Option D', 'theta_value': 1.9}
            ]
        }
    }
    
    for opt_id in ['A', 'B', 'C', 'D']:
        theta, info = mapper.map_response_to_theta(test_scenario, opt_id)
        print(f"Option {opt_id}: theta={theta:+.1f}, information={info:.2f}")
    
    # Test estimate updating
    print("\n=== Estimate Update Test ===")
    estimate = DimensionEstimate()
    
    # Simulate 3 responses
    responses = [('C', 0.7), ('D', 1.9), ('C', 1.0)]
    
    for opt, theta_val in responses:
        theta, info = mapper.map_response_to_theta(test_scenario, opt)
        estimate = mapper.update_theta_estimate(estimate, theta, info)
        print(f"After response {opt}: theta={estimate.theta:.2f}, SE={estimate.se:.2f}, n={estimate.n_items}")
    
    # Test interpretation
    print("\n=== Interpretation Test ===")
    interp = mapper.interpret_dimension_score('innovativeness', estimate.theta)
    print(f"Level: {interp['level_de']}")
    print(f"Strength: {interp['strength']}")
    print(f"Percentile: {interp['percentile']}")
