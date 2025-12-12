"""
Gap Analyzer - Identifies missing requirements for Gründungszuschuss approval
Based on official BA criteria and common rejection reasons

This module:
- Identifies critical gaps in GZ application readiness
- Prioritizes gaps by impact on approval
- Generates personality-adapted recommendations
- Maps gaps to specific modules
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass
class Gap:
    """Represents a single gap in GZ readiness"""
    gap_id: str
    name_de: str
    category: str
    category_de: str
    severity: str  # critical, high, medium, low
    impact: int  # 0-100 impact on approval
    covered_in_module: int
    recommendation_de: str
    priority: int  # Calculated priority for display


@dataclass
class GapAnalysisResult:
    """Complete gap analysis result"""
    current_readiness: int
    readiness_with_module1: int
    readiness_complete: int
    readiness_level: str
    readiness_level_de: str
    readiness_description_de: str
    critical_gaps: List[Gap]
    total_gaps: int
    personality_recommendations: List[str]
    next_milestone: Dict[str, Any]


class GapAnalyzer:
    """
    Analyzes gaps between current state and GZ approval requirements.
    
    Uses:
    - Official GZ criteria
    - Common rejection reasons from BA statistics
    - User's business context
    - Personality profile for recommendations
    """
    
    def __init__(self, criteria_path: Optional[str] = None):
        """
        Initialize with GZ criteria definitions.
        
        Args:
            criteria_path: Path to gz_criteria.json
        """
        if criteria_path is None:
            criteria_path = Path(__file__).parent / "gz_criteria.json"
        
        with open(criteria_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.readiness_components = self.config['readiness_components']
        self.gap_categories = self.config['gap_categories']
        self.readiness_levels = self.config['readiness_levels']
        self.module_progression = self.config['module_progression']
    
    def _get_readiness_level(self, score: int) -> Dict[str, Any]:
        """Get readiness level info based on score"""
        for level_id, level_info in self.readiness_levels.items():
            if score >= level_info['min_score']:
                return {
                    "id": level_id,
                    "label_de": level_info['label_de'],
                    "description_de": level_info['description_de'],
                    "color": level_info['color']
                }
        
        # Default to lowest level
        starting = self.readiness_levels['starting']
        return {
            "id": "starting",
            "label_de": starting['label_de'],
            "description_de": starting['description_de'],
            "color": starting['color']
        }
    
    def _identify_gaps(
        self,
        business_context: Dict[str, Any],
        completed_modules: List[int]
    ) -> List[Gap]:
        """Identify all gaps based on context and completed modules"""
        gaps = []
        priority_counter = 1
        
        for category_id, category_info in self.gap_categories.items():
            for gap_def in category_info['gaps']:
                # Check if this gap is still relevant
                module_num = gap_def['covered_in_module']
                if module_num in completed_modules:
                    continue  # Gap already addressed
                
                # Create Gap object
                gap = Gap(
                    gap_id=gap_def['id'],
                    name_de=gap_def['name_de'],
                    category=category_id,
                    category_de=category_info['name_de'],
                    severity=gap_def['severity'],
                    impact=gap_def['impact'],
                    covered_in_module=module_num,
                    recommendation_de=gap_def['recommendation_de'],
                    priority=priority_counter
                )
                gaps.append(gap)
                priority_counter += 1
        
        return gaps
    
    def _sort_gaps_by_priority(
        self,
        gaps: List[Gap],
        personality_profile: Optional[Dict[str, Any]] = None
    ) -> List[Gap]:
        """
        Sort gaps by priority considering:
        1. Severity (critical > high > medium > low)
        2. Impact score
        3. Personality fit (if available)
        """
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        
        def sort_key(gap: Gap) -> tuple:
            severity_rank = severity_order.get(gap.severity, 4)
            impact_rank = -gap.impact  # Negative for descending
            return (severity_rank, impact_rank, gap.priority)
        
        sorted_gaps = sorted(gaps, key=sort_key)
        
        # Update priorities after sorting
        for idx, gap in enumerate(sorted_gaps, 1):
            gap.priority = idx
        
        return sorted_gaps
    
    def _generate_personality_recommendations(
        self,
        personality_profile: Optional[Dict[str, Any]],
        gaps: List[Gap]
    ) -> List[str]:
        """Generate recommendations adapted to user's personality"""
        recommendations = []
        
        if not personality_profile:
            return [
                "Fokussieren Sie sich auf die kritischen Lücken",
                "Arbeiten Sie Modul für Modul systematisch ab",
                "Dokumentieren Sie alles sorgfältig"
            ]
        
        # Get archetype
        archetype_id = personality_profile.get('archetype', {}).get('id', 'balanced_entrepreneur')
        
        # Archetype-specific recommendations
        archetype_recommendations = {
            "bold_innovator": [
                "Nutzen Sie Ihre Kreativität für eine überzeugende Executive Summary",
                "Zeigen Sie innovative Aspekte, aber vergessen Sie die Marktvalidierung nicht",
                "Dokumentieren Sie, wie Ihre Innovation praktisch umsetzbar ist"
            ],
            "calculated_executor": [
                "Ihre Stärke in detaillierter Planung ist ideal für den Finanzplan",
                "Erstellen Sie einen präzisen Zeitplan für jeden Meilenstein",
                "Nutzen Sie Ihre Prozess-Expertise für den Organisationsplan"
            ],
            "ambitious_achiever": [
                "Setzen Sie sich ambitionierte, aber erreichbare Zwischenziele",
                "Zeigen Sie Ihre Erfolgsbilanz als Qualifikationsnachweis",
                "Formulieren Sie messbare Wachstumsziele für den Finanzplan"
            ],
            "independent_pioneer": [
                "Betonen Sie Ihre Expertise als Alleinstellungsmerkmal",
                "Zeigen Sie, wie Ihre Unabhängigkeit Kunden Mehrwert bietet",
                "Dokumentieren Sie ein Netzwerk für wichtige Unterstützung"
            ],
            "proactive_driver": [
                "Ihre proaktive Art hilft bei der Marktvalidierung",
                "Zeigen Sie erste Kundenkontakte oder Interessenten",
                "Erstellen Sie einen dynamischen Go-to-Market-Plan"
            ],
            "resilient_controller": [
                "Ihre Widerstandsfähigkeit ist ein wichtiger Erfolgsfaktor",
                "Dokumentieren Sie, wie Sie mit Rückschlägen umgehen",
                "Entwickeln Sie detaillierte Notfallpläne"
            ],
            "confident_builder": [
                "Nutzen Sie Ihr Selbstvertrauen für überzeugende Präsentationen",
                "Zeigen Sie konkrete vergangene Erfolge",
                "Dokumentieren Sie relevante Qualifikationen"
            ],
            "balanced_entrepreneur": [
                "Ihre Ausgewogenheit ermöglicht systematisches Vorgehen",
                "Arbeiten Sie alle Module der Reihe nach ab",
                "Nutzen Sie Ihre Anpassungsfähigkeit für verschiedene Bereiche"
            ]
        }
        
        recommendations = archetype_recommendations.get(
            archetype_id,
            archetype_recommendations['balanced_entrepreneur']
        )
        
        # Add dimension-specific recommendations
        dimensions = personality_profile.get('dimensions', {})
        
        # Check for low risk-taking
        risk_dim = dimensions.get('risk_taking', {})
        if risk_dim.get('percentile', 50) < 40:
            recommendations.append(
                "Bei Ihrer vorsichtigen Risikoeinstellung: Betonen Sie bewährte "
                "Geschäftsmodelle und validierte Marktchancen"
            )
        
        # Check for low self-efficacy
        efficacy_dim = dimensions.get('self_efficacy', {})
        if efficacy_dim.get('percentile', 50) < 40:
            recommendations.append(
                "Sammeln Sie Referenzen und Testimonials, die Ihre Fähigkeiten belegen"
            )
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def _get_next_milestone(
        self,
        current_readiness: int,
        completed_modules: List[int]
    ) -> Dict[str, Any]:
        """Determine the next achievable milestone"""
        # Find next uncompleted module
        for module_num in range(1, 8):
            if module_num not in completed_modules:
                module_key = f"module_{module_num}"
                if module_key in self.module_progression:
                    module_info = self.module_progression[module_key]
                    return {
                        "module": module_num,
                        "name_de": module_info['name_de'],
                        "readiness_boost": module_info['readiness_boost'],
                        "new_readiness": current_readiness + module_info['readiness_boost'],
                        "time_minutes": module_info['time_minutes'],
                        "deliverable_de": module_info['deliverable_de']
                    }
        
        # All modules complete
        return {
            "module": 0,
            "name_de": "Abgeschlossen",
            "readiness_boost": 0,
            "new_readiness": current_readiness,
            "time_minutes": 0,
            "deliverable_de": "Vollständiger Businessplan"
        }
    
    def calculate_readiness(
        self,
        completed_modules: List[int] = None
    ) -> Dict[str, Any]:
        """
        Calculate current GZ readiness score.
        
        Readiness starts at 35% after assessment completion.
        Each module adds to the total.
        """
        if completed_modules is None:
            completed_modules = []
        
        # Base readiness from assessment
        readiness = 35
        
        # Add module completions
        for module_num in completed_modules:
            module_key = f"module_{module_num}"
            if module_key in self.module_progression:
                readiness += self.module_progression[module_key]['readiness_boost']
        
        # Cap at 95 (100 requires fachkundige Stelle approval)
        readiness = min(readiness, 95)
        
        return {
            "current": readiness,
            "with_module1": min(readiness + 20, 95) if 1 not in completed_modules else readiness,
            "complete": 95
        }
    
    def analyze_gaps(
        self,
        business_context: Dict[str, Any],
        personality_profile: Optional[Dict[str, Any]] = None,
        completed_modules: List[int] = None
    ) -> GapAnalysisResult:
        """
        Perform complete gap analysis.
        
        Args:
            business_context: User's business information
            personality_profile: Optional personality profile for personalization
            completed_modules: List of completed module numbers
        
        Returns:
            Complete GapAnalysisResult
        """
        if completed_modules is None:
            completed_modules = []
        
        # Calculate readiness
        readiness = self.calculate_readiness(completed_modules)
        readiness_level_info = self._get_readiness_level(readiness['current'])
        
        # Identify gaps
        all_gaps = self._identify_gaps(business_context, completed_modules)
        
        # Sort by priority
        sorted_gaps = self._sort_gaps_by_priority(all_gaps, personality_profile)
        
        # Take only critical/high gaps for display (max 7)
        critical_gaps = [
            g for g in sorted_gaps
            if g.severity in ['critical', 'high']
        ][:7]
        
        # Generate recommendations
        recommendations = self._generate_personality_recommendations(
            personality_profile,
            critical_gaps
        )
        
        # Get next milestone
        next_milestone = self._get_next_milestone(
            readiness['current'],
            completed_modules
        )
        
        return GapAnalysisResult(
            current_readiness=readiness['current'],
            readiness_with_module1=readiness['with_module1'],
            readiness_complete=readiness['complete'],
            readiness_level=readiness_level_info['id'],
            readiness_level_de=readiness_level_info['label_de'],
            readiness_description_de=readiness_level_info['description_de'],
            critical_gaps=critical_gaps,
            total_gaps=len(all_gaps),
            personality_recommendations=recommendations,
            next_milestone=next_milestone
        )
    
    def gap_to_dict(self, gap: Gap) -> Dict[str, Any]:
        """Convert Gap to dictionary"""
        return {
            "gap_id": gap.gap_id,
            "name_de": gap.name_de,
            "category": gap.category,
            "category_de": gap.category_de,
            "severity": gap.severity,
            "impact": gap.impact,
            "covered_in_module": gap.covered_in_module,
            "recommendation_de": gap.recommendation_de,
            "priority": gap.priority
        }
    
    def result_to_dict(self, result: GapAnalysisResult) -> Dict[str, Any]:
        """Convert GapAnalysisResult to dictionary"""
        return {
            "readiness": {
                "current": result.current_readiness,
                "with_module1": result.readiness_with_module1,
                "complete": result.readiness_complete,
                "level": result.readiness_level,
                "level_de": result.readiness_level_de,
                "description_de": result.readiness_description_de
            },
            "gaps": {
                "critical": [self.gap_to_dict(g) for g in result.critical_gaps],
                "total_count": result.total_gaps
            },
            "personality_recommendations": result.personality_recommendations,
            "next_milestone": result.next_milestone
        }
