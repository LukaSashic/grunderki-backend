"""
Scenario Generator - Personalizes business scenarios for invisible personality assessment
Based on Howard's 7-dimension entrepreneurial personality framework
"""

from typing import Dict, List, Optional, Any
import json
from pathlib import Path
import random
import re
from datetime import datetime


class ScenarioGenerator:
    """
    Generates personalized business scenarios for personality assessment.
    
    Core Innovation: "Invisible Personality Integration"
    - Users think they're making business decisions
    - System measures Howard's 7 personality dimensions
    - Scenarios feel relevant to user's specific business type
    """
    
    def __init__(self, scenario_bank_path: Optional[str] = None):
        """
        Initialize with scenario bank.
        
        Args:
            scenario_bank_path: Path to scenario_bank.json. If None, uses default.
        """
        if scenario_bank_path is None:
            scenario_bank_path = Path(__file__).parent / "scenario_bank.json"
        
        with open(scenario_bank_path, 'r', encoding='utf-8') as f:
            self.scenario_bank = json.load(f)
        
        # Build indices for fast lookup
        self.scenarios_by_dimension = self._index_by_dimension()
        self.personalization_keys = self.scenario_bank.get('personalization_keys', {})
        
        # Track generated scenarios per session
        self._session_scenarios: Dict[str, List[str]] = {}
    
    def _index_by_dimension(self) -> Dict[str, List[Dict]]:
        """Create index of scenarios by dimension for fast lookup."""
        index = {}
        for scenario in self.scenario_bank['scenarios']:
            dimension = scenario['dimension']
            if dimension not in index:
                index[dimension] = []
            index[dimension].append(scenario)
        
        # Sort by difficulty for better adaptive selection
        for dimension in index:
            index[dimension].sort(key=lambda s: s['difficulty'])
        
        return index
    
    def generate_scenario(
        self,
        dimension: str,
        target_difficulty: float,
        business_context: Dict[str, Any],
        previously_seen: Optional[List[str]] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a personalized scenario for assessment.
        
        Args:
            dimension: Howard dimension to measure (e.g., 'innovativeness')
            target_difficulty: IRT difficulty level (-2 to +2)
            business_context: User's business information from Day 1
            previously_seen: List of scenario IDs already shown
            session_id: Optional session ID for tracking
            
        Returns:
            Personalized scenario ready for presentation
        """
        if previously_seen is None:
            previously_seen = []
        
        # Get candidates for this dimension
        candidates = self.scenarios_by_dimension.get(dimension, [])
        
        if not candidates:
            raise ValueError(f"No scenarios available for dimension: {dimension}")
        
        # Filter out previously seen scenarios
        available = [s for s in candidates if s['scenario_id'] not in previously_seen]
        
        if not available:
            # All scenarios seen - allow repeats (shouldn't happen with 5 per dimension)
            available = candidates
        
        # Select scenario closest to target difficulty
        selected = min(
            available,
            key=lambda s: abs(s['difficulty'] - target_difficulty)
        )
        
        # Personalize the scenario
        personalized = self._personalize_scenario(selected, business_context)
        
        # Track for session if provided
        if session_id:
            if session_id not in self._session_scenarios:
                self._session_scenarios[session_id] = []
            self._session_scenarios[session_id].append(selected['scenario_id'])
        
        return personalized
    
    def _personalize_scenario(
        self,
        scenario: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Replace template variables with business-specific content.
        
        Template variables like {{business_label}} are replaced with
        context-appropriate values (e.g., "Restaurant" for restaurant business).
        
        Args:
            scenario: Raw scenario from scenario bank
            context: Business context from Day 1 assessment
            
        Returns:
            Personalized scenario with all variables replaced
        """
        # Deep copy to avoid modifying original
        personalized = {
            'scenario_id': scenario['scenario_id'],
            'dimension': scenario['dimension'],
            'difficulty': scenario['difficulty'],
            'discrimination': scenario['discrimination'],
            'template': {
                'situation': scenario['template']['situation'],
                'question': scenario['template']['question'],
                'options': []
            }
        }
        
        # Get business type (default to 'other' if not specified)
        business_type = context.get('business_type', 'other')
        
        # Get personalization values for this business type
        business_values = self.personalization_keys.get('business_type', {}).get(
            business_type, 
            self.personalization_keys.get('business_type', {}).get('other', {})
        )
        
        # Add context-specific values
        replacement_values = {
            **business_values,
            'business_type': business_type,
        }
        
        # If we have more specific context, use it
        if context.get('description'):
            # Could use description to make even more specific - future enhancement
            pass
        
        # Replace variables in situation
        personalized['template']['situation'] = self._replace_variables(
            personalized['template']['situation'],
            replacement_values
        )
        
        # Replace variables in question
        personalized['template']['question'] = self._replace_variables(
            personalized['template']['question'],
            replacement_values
        )
        
        # Replace variables in each option
        for option in scenario['template']['options']:
            personalized_option = {
                'id': option['id'],
                'text': self._replace_variables(option['text'], replacement_values),
                'theta_value': option['theta_value'],
                'psychological_mapping': option['psychological_mapping']
            }
            personalized['template']['options'].append(personalized_option)
        
        return personalized
    
    def _replace_variables(self, text: str, values: Dict[str, str]) -> str:
        """
        Replace {{variable}} placeholders with actual values.
        
        Args:
            text: Text with {{variable}} placeholders
            values: Dictionary of variable -> value mappings
            
        Returns:
            Text with all variables replaced
        """
        def replacer(match):
            var_name = match.group(1)
            return values.get(var_name, match.group(0))  # Keep original if not found
        
        return re.sub(r'\{\{(\w+)\}\}', replacer, text)
    
    def get_scenarios_for_dimension(
        self,
        dimension: str,
        business_context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Get all available scenarios for a dimension, personalized.
        
        Useful for testing or previewing scenarios.
        
        Args:
            dimension: Howard dimension
            business_context: Business context for personalization
            
        Returns:
            List of personalized scenarios
        """
        scenarios = self.scenarios_by_dimension.get(dimension, [])
        return [
            self._personalize_scenario(s, business_context) 
            for s in scenarios
        ]
    
    def validate_coverage(self) -> Dict[str, Any]:
        """
        Validate that scenario bank has adequate coverage.
        
        Returns:
            Validation report with coverage metrics
        """
        required_dimensions = [
            "innovativeness",
            "risk_taking",
            "achievement_orientation",
            "autonomy_orientation",
            "proactiveness",
            "locus_of_control",
            "self_efficacy"
        ]
        
        report = {
            "total_scenarios": len(self.scenario_bank['scenarios']),
            "dimensions_covered": len(self.scenarios_by_dimension),
            "scenarios_per_dimension": {},
            "difficulty_ranges": {},
            "discrimination_stats": {},
            "warnings": [],
            "valid": True
        }
        
        for dim in required_dimensions:
            scenarios = self.scenarios_by_dimension.get(dim, [])
            count = len(scenarios)
            
            report['scenarios_per_dimension'][dim] = count
            
            if count < 5:
                report['warnings'].append(
                    f"Dimension '{dim}' has only {count} scenarios (minimum 5 recommended)"
                )
                report['valid'] = False
            
            if scenarios:
                difficulties = [s['difficulty'] for s in scenarios]
                discriminations = [s['discrimination'] for s in scenarios]
                
                report['difficulty_ranges'][dim] = {
                    "min": round(min(difficulties), 2),
                    "max": round(max(difficulties), 2),
                    "mean": round(sum(difficulties) / len(difficulties), 2),
                    "range": round(max(difficulties) - min(difficulties), 2)
                }
                
                report['discrimination_stats'][dim] = {
                    "min": round(min(discriminations), 2),
                    "max": round(max(discriminations), 2),
                    "mean": round(sum(discriminations) / len(discriminations), 2)
                }
                
                # Check difficulty spread
                if report['difficulty_ranges'][dim]['range'] < 1.5:
                    report['warnings'].append(
                        f"Dimension '{dim}' has limited difficulty range ({report['difficulty_ranges'][dim]['range']})"
                    )
        
        return report
    
    def get_session_history(self, session_id: str) -> List[str]:
        """Get list of scenario IDs shown in a session."""
        return self._session_scenarios.get(session_id, [])
    
    def clear_session(self, session_id: str):
        """Clear session tracking data."""
        if session_id in self._session_scenarios:
            del self._session_scenarios[session_id]
    
    def format_for_frontend(
        self,
        scenario: Dict[str, Any],
        include_metadata: bool = False
    ) -> Dict[str, Any]:
        """
        Format scenario for frontend display.
        
        Removes psychological mappings and IRT parameters that
        shouldn't be visible to users.
        
        Args:
            scenario: Personalized scenario
            include_metadata: If True, include scenario_id for tracking
            
        Returns:
            Frontend-safe scenario object
        """
        formatted = {
            'situation': scenario['template']['situation'],
            'question': scenario['template']['question'],
            'options': [
                {
                    'id': opt['id'],
                    'text': opt['text']
                }
                for opt in scenario['template']['options']
            ]
        }
        
        if include_metadata:
            formatted['scenario_id'] = scenario['scenario_id']
            formatted['dimension'] = scenario['dimension']
        
        return formatted


# Utility functions for testing
def create_test_business_context(business_type: str = 'restaurant') -> Dict[str, Any]:
    """Create a test business context for development/testing."""
    contexts = {
        'restaurant': {
            'business_type': 'restaurant',
            'sub_type': 'casual_dining',
            'target_customer': 'families',
            'problem': 'quality_family_dining',
            'stage': 'planning',
            'description': 'Italienisches Restaurant für Familien'
        },
        'saas': {
            'business_type': 'saas',
            'sub_type': 'b2b_productivity',
            'target_customer': 'small_businesses',
            'problem': 'tools_too_complex',
            'stage': 'mvp',
            'description': 'Projektmanagement-Tool für kleine Teams'
        },
        'consulting': {
            'business_type': 'consulting',
            'sub_type': 'business_strategy',
            'target_customer': 'startups',
            'problem': 'strategy_unclear',
            'stage': 'revenue',
            'description': 'Strategieberatung für Startups'
        },
        'ecommerce': {
            'business_type': 'ecommerce',
            'sub_type': 'fashion',
            'target_customer': 'young_adults',
            'problem': 'sustainable_fashion',
            'stage': 'idea',
            'description': 'Nachhaltiger Online-Modeshop'
        }
    }
    return contexts.get(business_type, contexts['restaurant'])


if __name__ == "__main__":
    # Test the scenario generator
    generator = ScenarioGenerator()
    
    # Validate coverage
    print("=== Scenario Bank Validation ===")
    report = generator.validate_coverage()
    print(f"Total scenarios: {report['total_scenarios']}")
    print(f"Dimensions covered: {report['dimensions_covered']}")
    print(f"Valid: {report['valid']}")
    
    if report['warnings']:
        print("\nWarnings:")
        for w in report['warnings']:
            print(f"  - {w}")
    
    print("\nScenarios per dimension:")
    for dim, count in report['scenarios_per_dimension'].items():
        print(f"  {dim}: {count}")
    
    # Test personalization
    print("\n=== Personalization Test ===")
    
    for biz_type in ['restaurant', 'saas', 'consulting']:
        context = create_test_business_context(biz_type)
        scenario = generator.generate_scenario(
            dimension='innovativeness',
            target_difficulty=0.0,
            business_context=context
        )
        
        print(f"\n{biz_type.upper()} Scenario:")
        formatted = generator.format_for_frontend(scenario, include_metadata=True)
        print(f"  Situation: {formatted['situation'][:100]}...")
        print(f"  Question: {formatted['question']}")
