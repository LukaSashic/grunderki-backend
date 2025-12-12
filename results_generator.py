"""
Results Generator - Compiles complete assessment results
Main orchestrator for Day 3 Results Page

This module:
- Combines personality profile + gap analysis + next steps
- Creates conversion-optimized results package
- Generates Module 1 CTA
- Prepares data for frontend visualization
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from personality_profiler import PersonalityProfiler, PersonalityProfile
from gap_analyzer import GapAnalyzer, GapAnalysisResult


@dataclass
class NextSteps:
    """Next steps and CTA information"""
    primary_cta: Dict[str, Any]
    secondary_actions: List[Dict[str, Any]]
    time_investment_total: int  # Total minutes for complete workshop
    potential_readiness: int


@dataclass
class CompleteResults:
    """Complete assessment results package"""
    user_id: str
    session_id: str
    timestamp: str
    personality_profile: PersonalityProfile
    gap_analysis: GapAnalysisResult
    next_steps: NextSteps
    radar_chart_data: List[Dict[str, Any]]
    share_data: Dict[str, Any]


class ResultsGenerator:
    """
    Generates complete assessment results for display.
    
    Orchestrates:
    - PersonalityProfiler for archetype classification
    - GapAnalyzer for gap identification
    - CTA generation for conversion
    - Chart data for visualization
    """
    
    def __init__(
        self,
        archetypes_path: Optional[str] = None,
        criteria_path: Optional[str] = None
    ):
        """
        Initialize with config paths.
        
        Args:
            archetypes_path: Path to personality_archetypes.json
            criteria_path: Path to gz_criteria.json
        """
        self.profiler = PersonalityProfiler(archetypes_path)
        self.analyzer = GapAnalyzer(criteria_path)
    
    def _generate_cta(
        self,
        personality_profile: PersonalityProfile,
        gap_analysis: GapAnalysisResult
    ) -> NextSteps:
        """
        Generate conversion-optimized CTA.
        
        Adapts language to personality type for maximum impact.
        """
        archetype_id = personality_profile.archetype_id
        
        # Archetype-specific CTA variants
        cta_variants = {
            "bold_innovator": {
                "text": "Jetzt Executive Summary erstellen",
                "headline_de": "Verwandeln Sie Ihre Innovation in einen überzeugenden Plan",
                "value_prop_de": "Erstellen Sie in 25 Minuten eine Executive Summary, die Ihre einzigartige Vision auf den Punkt bringt"
            },
            "calculated_executor": {
                "text": "Strategisches Fundament aufbauen",
                "headline_de": "Bauen Sie Ihr strategisches Fundament",
                "value_prop_de": "Erstellen Sie eine systematische Executive Summary mit bewährten Frameworks"
            },
            "ambitious_achiever": {
                "text": "Erfolgsjourney starten",
                "headline_de": "Starten Sie Ihre Erfolgsjourney",
                "value_prop_de": "Generieren Sie eine hochwertige Executive Summary, die Ihre Ambitionen widerspiegelt"
            },
            "independent_pioneer": {
                "text": "Eigenen Weg dokumentieren",
                "headline_de": "Dokumentieren Sie Ihren einzigartigen Weg",
                "value_prop_de": "Erstellen Sie eine Executive Summary, die Ihre Expertise und Unabhängigkeit hervorhebt"
            },
            "proactive_driver": {
                "text": "Jetzt durchstarten",
                "headline_de": "Starten Sie durch!",
                "value_prop_de": "Erstellen Sie sofort Ihre Executive Summary und nutzen Sie Ihren Vorsprung"
            },
            "resilient_controller": {
                "text": "Solide Basis schaffen",
                "headline_de": "Schaffen Sie eine solide Basis",
                "value_prop_de": "Erstellen Sie eine durchdachte Executive Summary mit klarem Notfallplan"
            },
            "confident_builder": {
                "text": "Vision umsetzen",
                "headline_de": "Setzen Sie Ihre Vision um",
                "value_prop_de": "Erstellen Sie eine überzeugende Executive Summary, die Ihr Selbstvertrauen widerspiegelt"
            },
            "balanced_entrepreneur": {
                "text": "Modul 1 starten",
                "headline_de": "Starten Sie mit Modul 1",
                "value_prop_de": "Erstellen Sie Ihre Executive Summary in einem strukturierten Prozess"
            }
        }
        
        cta_info = cta_variants.get(archetype_id, cta_variants['balanced_entrepreneur'])
        
        readiness_boost = gap_analysis.next_milestone.get('readiness_boost', 20)
        new_readiness = gap_analysis.current_readiness + readiness_boost
        
        primary_cta = {
            "action": "start_module_1",
            "text": cta_info['text'],
            "headline_de": cta_info['headline_de'],
            "value_proposition_de": cta_info['value_prop_de'],
            "details": {
                "time_minutes": 25,
                "deliverable_de": "Fertige Executive Summary (PDF)",
                "is_free": True,
                "no_credit_card": True
            },
            "progress": {
                "current_readiness": gap_analysis.current_readiness,
                "after_module1": new_readiness,
                "boost": readiness_boost,
                "boost_text": f"+{readiness_boost}% GZ-Bereitschaft"
            },
            "urgency_de": "Nutzen Sie den Schwung - starten Sie jetzt!",
            "social_proof_de": "Über 500 Gründer haben bereits gestartet"
        }
        
        secondary_actions = [
            {
                "action": "download_results_pdf",
                "text_de": "Ergebnisse als PDF",
                "icon": "download"
            },
            {
                "action": "share_linkedin",
                "text_de": "Auf LinkedIn teilen",
                "icon": "share"
            },
            {
                "action": "schedule_consultation",
                "text_de": "Beratungsgespräch buchen",
                "icon": "calendar"
            },
            {
                "action": "learn_more",
                "text_de": "Mehr über das Programm",
                "icon": "info"
            }
        ]
        
        # Calculate total time for complete workshop
        total_time = 25 + 30 + 20 + 25 + 20 + 35 + 20  # All modules
        
        return NextSteps(
            primary_cta=primary_cta,
            secondary_actions=secondary_actions,
            time_investment_total=total_time,
            potential_readiness=95
        )
    
    def _generate_radar_chart_data(
        self,
        personality_profile: PersonalityProfile
    ) -> List[Dict[str, Any]]:
        """
        Generate data for radar chart visualization.
        
        Format optimized for recharts or Chart.js
        """
        dimension_order = [
            "innovativeness",
            "risk_taking", 
            "achievement_orientation",
            "autonomy_orientation",
            "proactiveness",
            "locus_of_control",
            "self_efficacy"
        ]
        
        chart_data = []
        for dim in dimension_order:
            if dim in personality_profile.dimensions:
                interp = personality_profile.dimensions[dim]
                chart_data.append({
                    "dimension": dim,
                    "label_de": interp.dimension_label_de,
                    "percentile": interp.percentile,
                    "level": interp.level,
                    "level_de": interp.level_de,
                    # For radar chart rendering
                    "value": interp.percentile,
                    "fullMark": 100
                })
        
        return chart_data
    
    def _generate_share_data(
        self,
        personality_profile: PersonalityProfile,
        gap_analysis: GapAnalysisResult
    ) -> Dict[str, Any]:
        """Generate data for social sharing"""
        return {
            "headline_de": f"Ich bin ein {personality_profile.archetype_name_de}!",
            "text_de": (
                f"Mein unternehmerisches Profil: {personality_profile.archetype_name_de}. "
                f"GZ-Bereitschaft: {gap_analysis.current_readiness}%. "
                f"Entdecke dein Gründerprofil auf GründerAI!"
            ),
            "hashtags": ["Gründer", "Startup", "Gründungszuschuss", "Entrepreneurship"],
            "url": "https://gruenderai.de/assessment"
        }
    
    def generate_results(
        self,
        user_id: str,
        session_id: str,
        dimension_scores: Dict[str, Dict[str, float]],
        business_context: Dict[str, Any],
        completed_modules: List[int] = None
    ) -> CompleteResults:
        """
        Generate complete assessment results.
        
        Args:
            user_id: User identifier
            session_id: Assessment session identifier
            dimension_scores: Dict with 7 dimensions, each containing
                            'theta' and 'percentile' values
            business_context: User's business information
            completed_modules: List of already completed module numbers
        
        Returns:
            CompleteResults object with all data for display
        """
        if completed_modules is None:
            completed_modules = []
        
        # Generate personality profile
        profile = self.profiler.create_profile(dimension_scores, business_context)
        
        # Convert profile to dict for gap analyzer
        profile_dict = self.profiler.profile_to_dict(profile)
        
        # Analyze gaps
        gap_analysis = self.analyzer.analyze_gaps(
            business_context,
            profile_dict,
            completed_modules
        )
        
        # Generate CTA
        next_steps = self._generate_cta(profile, gap_analysis)
        
        # Generate chart data
        radar_data = self._generate_radar_chart_data(profile)
        
        # Generate share data
        share_data = self._generate_share_data(profile, gap_analysis)
        
        return CompleteResults(
            user_id=user_id,
            session_id=session_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            personality_profile=profile,
            gap_analysis=gap_analysis,
            next_steps=next_steps,
            radar_chart_data=radar_data,
            share_data=share_data
        )
    
    def results_to_dict(self, results: CompleteResults) -> Dict[str, Any]:
        """
        Convert CompleteResults to dictionary for JSON serialization.
        
        This is the format returned by the API.
        """
        return {
            "user_id": results.user_id,
            "session_id": results.session_id,
            "timestamp": results.timestamp,
            "personality_profile": self.profiler.profile_to_dict(results.personality_profile),
            "gap_analysis": self.analyzer.result_to_dict(results.gap_analysis),
            "next_steps": {
                "primary_cta": results.next_steps.primary_cta,
                "secondary_actions": results.next_steps.secondary_actions,
                "time_investment_total_minutes": results.next_steps.time_investment_total,
                "potential_readiness": results.next_steps.potential_readiness
            },
            "visualization": {
                "radar_chart_data": results.radar_chart_data
            },
            "share": results.share_data
        }
    
    def generate_results_dict(
        self,
        user_id: str,
        session_id: str,
        dimension_scores: Dict[str, Dict[str, float]],
        business_context: Dict[str, Any],
        completed_modules: List[int] = None
    ) -> Dict[str, Any]:
        """
        Convenience method to generate results directly as dict.
        
        Combines generate_results() and results_to_dict().
        """
        results = self.generate_results(
            user_id,
            session_id,
            dimension_scores,
            business_context,
            completed_modules
        )
        return self.results_to_dict(results)


# Convenience function for simple usage
def generate_assessment_results(
    user_id: str,
    session_id: str,
    dimension_scores: Dict[str, Dict[str, float]],
    business_context: Dict[str, Any],
    completed_modules: List[int] = None
) -> Dict[str, Any]:
    """
    Generate complete assessment results.
    
    Simple function interface for the ResultsGenerator.
    
    Args:
        user_id: User identifier
        session_id: Assessment session identifier
        dimension_scores: Dimension scores from CAT engine
        business_context: Business context from Day 1
        completed_modules: Already completed modules
    
    Returns:
        Complete results as dictionary
    """
    generator = ResultsGenerator()
    return generator.generate_results_dict(
        user_id,
        session_id,
        dimension_scores,
        business_context,
        completed_modules
    )
