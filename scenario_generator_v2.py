"""
Enhanced Scenario Generator - Uses truly personalized business-specific scenarios

Key improvement: Instead of just variable substitution ({{business_label}}),
we now have completely different scenarios for each business type.

Example:
- Restaurant: "Ein Stammgast beschwert sich über die Speisekarte..."
- SaaS: "Nutzer fordern ein Feature, das Konkurrenten haben..."
- Consulting: "Ein Kunde fragt nach einem Workshop-Format..."

All scenarios measure the same Howard dimension but feel native to the user's business.
"""

from typing import Dict, List, Optional, Any
import json
from pathlib import Path
import random
import re


class EnhancedScenarioGenerator:
    """
    Generates truly personalized business scenarios for personality assessment.
    
    Core Innovation: "Deep Context Integration"
    - Each business type has completely different scenario situations
    - Scenarios feel native to the user's specific industry
    - Variable substitution is backup, not primary personalization
    """
    
    # Mapping from frontend IDs to backend business types
    BUSINESS_TYPE_MAPPING = {
        'consulting': 'consulting',
        'tech': 'saas',
        'saas': 'saas',
        'ecommerce': 'ecommerce',
        'service': 'services',
        'services': 'services',
        'creative': 'creative',
        'health': 'health',
        'gastro': 'restaurant',
        'restaurant': 'restaurant',
        'education': 'services',
        'other': 'other',
    }
    
    def __init__(self, scenario_bank_path: Optional[str] = None):
        """Initialize with enhanced scenario bank."""
        if scenario_bank_path is None:
            # Try v2 first, fallback to v1
            v2_path = Path(__file__).parent / "scenario_bank_v2.json"
            v1_path = Path(__file__).parent / "scenario_bank.json"
            scenario_bank_path = v2_path if v2_path.exists() else v1_path
        
        with open(scenario_bank_path, 'r', encoding='utf-8') as f:
            self.scenario_bank = json.load(f)
        
        # Check if we have business-specific scenarios
        self.has_business_specific = 'business_specific_scenarios' in self.scenario_bank
        
        # Build indices
        self.personalization_keys = self.scenario_bank.get('personalization_keys', {})
        
        if self.has_business_specific:
            self.business_scenarios = self.scenario_bank['business_specific_scenarios']
            self.generic_scenarios = self.scenario_bank.get('generic_fallback_scenarios', [])
            self._build_business_indices()
        else:
            # Fallback to old format
            self.scenarios_by_dimension = self._index_by_dimension_legacy()
        
        # Track generated scenarios per session
        self._session_scenarios: Dict[str, List[str]] = {}
    
    def _build_business_indices(self):
        """Build indices for business-specific scenarios."""
        self.scenarios_by_business_and_dimension: Dict[str, Dict[str, List[Dict]]] = {}
        
        for business_type, scenarios in self.business_scenarios.items():
            self.scenarios_by_business_and_dimension[business_type] = {}
            
            for scenario in scenarios:
                dim = scenario['dimension']
                if dim not in self.scenarios_by_business_and_dimension[business_type]:
                    self.scenarios_by_business_and_dimension[business_type][dim] = []
                self.scenarios_by_business_and_dimension[business_type][dim].append(scenario)
        
        # Also index generic fallback scenarios
        self.generic_by_dimension: Dict[str, List[Dict]] = {}
        for scenario in self.generic_scenarios:
            dim = scenario['dimension']
            if dim not in self.generic_by_dimension:
                self.generic_by_dimension[dim] = []
            self.generic_by_dimension[dim].append(scenario)
    
    def _index_by_dimension_legacy(self) -> Dict[str, List[Dict]]:
        """Create index of scenarios by dimension (legacy format)."""
        index = {}
        for scenario in self.scenario_bank.get('scenarios', []):
            dimension = scenario['dimension']
            if dimension not in index:
                index[dimension] = []
            index[dimension].append(scenario)
        
        for dimension in index:
            index[dimension].sort(key=lambda s: s['difficulty'])
        
        return index
    
    def _get_normalized_business_type(self, context: Dict[str, Any]) -> str:
        """Normalize business type from various context formats."""
        # Try different keys
        raw_type = (
            context.get('business_type') or 
            context.get('category') or 
            context.get('type') or 
            'other'
        )
        
        # Map to canonical type
        return self.BUSINESS_TYPE_MAPPING.get(raw_type.lower(), 'other')
    
    def generate_scenario(
        self,
        dimension: str,
        target_difficulty: float,
        business_context: Dict[str, Any],
        previously_seen: Optional[List[str]] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a truly personalized scenario for assessment.
        
        Priority:
        1. Business-specific scenario (if available)
        2. Generic scenario with variable substitution (fallback)
        """
        if previously_seen is None:
            previously_seen = []
        
        business_type = self._get_normalized_business_type(business_context)
        
        if self.has_business_specific:
            scenario = self._get_business_specific_scenario(
                business_type, dimension, target_difficulty, previously_seen
            )
        else:
            scenario = self._get_generic_scenario(
                dimension, target_difficulty, previously_seen
            )
        
        # Apply any variable substitution needed
        personalized = self._personalize_scenario(scenario, business_context)
        
        # Track for session
        if session_id:
            if session_id not in self._session_scenarios:
                self._session_scenarios[session_id] = []
            self._session_scenarios[session_id].append(scenario['scenario_id'])
        
        return personalized
    
    def _get_business_specific_scenario(
        self,
        business_type: str,
        dimension: str,
        target_difficulty: float,
        previously_seen: List[str]
    ) -> Dict[str, Any]:
        """Get scenario from business-specific bank."""
        # Try business-specific first
        if business_type in self.scenarios_by_business_and_dimension:
            dim_scenarios = self.scenarios_by_business_and_dimension[business_type].get(dimension, [])
            available = [s for s in dim_scenarios if s['scenario_id'] not in previously_seen]
            
            if available:
                return min(available, key=lambda s: abs(s['difficulty'] - target_difficulty))
        
        # Fallback to generic
        generic_scenarios = self.generic_by_dimension.get(dimension, [])
        available = [s for s in generic_scenarios if s['scenario_id'] not in previously_seen]
        
        if available:
            return min(available, key=lambda s: abs(s['difficulty'] - target_difficulty))
        
        # Last resort: return any scenario for this dimension
        if business_type in self.scenarios_by_business_and_dimension:
            dim_scenarios = self.scenarios_by_business_and_dimension[business_type].get(dimension, [])
            if dim_scenarios:
                return dim_scenarios[0]
        
        if generic_scenarios:
            return generic_scenarios[0]
        
        raise ValueError(f"No scenarios available for dimension: {dimension}")
    
    def _get_generic_scenario(
        self,
        dimension: str,
        target_difficulty: float,
        previously_seen: List[str]
    ) -> Dict[str, Any]:
        """Get scenario from legacy format."""
        candidates = self.scenarios_by_dimension.get(dimension, [])
        
        if not candidates:
            raise ValueError(f"No scenarios available for dimension: {dimension}")
        
        available = [s for s in candidates if s['scenario_id'] not in previously_seen]
        
        if not available:
            available = candidates
        
        return min(available, key=lambda s: abs(s['difficulty'] - target_difficulty))
    
    def _personalize_scenario(
        self,
        scenario: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply variable substitution for any remaining placeholders."""
        business_type = self._get_normalized_business_type(context)
        
        # Get personalization values
        business_values = self.personalization_keys.get(business_type, 
            self.personalization_keys.get('other', {}))
        
        # Deep copy to avoid modifying original
        personalized = {
            'scenario_id': scenario['scenario_id'],
            'dimension': scenario['dimension'],
            'difficulty': scenario['difficulty'],
            'discrimination': scenario.get('discrimination', 1.5),
            'template': {
                'situation': self._replace_variables(
                    scenario['template']['situation'], business_values
                ),
                'question': self._replace_variables(
                    scenario['template']['question'], business_values
                ),
                'options': []
            }
        }
        
        for option in scenario['template']['options']:
            personalized['template']['options'].append({
                'id': option['id'],
                'text': self._replace_variables(option['text'], business_values),
                'theta_value': option['theta_value'],
                'psychological_mapping': option['psychological_mapping']
            })
        
        return personalized
    
    def _replace_variables(self, text: str, values: Dict[str, str]) -> str:
        """Replace {{variable}} placeholders with actual values."""
        def replacer(match):
            var_name = match.group(1)
            return values.get(var_name, match.group(0))
        
        return re.sub(r'\{\{(\w+)\}\}', replacer, text)
    
    def format_for_frontend(
        self,
        scenario: Dict[str, Any],
        include_metadata: bool = False
    ) -> Dict[str, Any]:
        """Format scenario for frontend display (hide psychological data)."""
        formatted = {
            'situation': scenario['template']['situation'],
            'question': scenario['template']['question'],
            'options': [
                {'id': opt['id'], 'text': opt['text']}
                for opt in scenario['template']['options']
            ]
        }
        
        if include_metadata:
            formatted['scenario_id'] = scenario['scenario_id']
            formatted['dimension'] = scenario['dimension']
        
        return formatted
    
    def get_all_scenarios_for_business(
        self,
        business_type: str
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Get all scenarios for a business type, organized by dimension."""
        normalized_type = self.BUSINESS_TYPE_MAPPING.get(business_type.lower(), 'other')
        
        if not self.has_business_specific:
            return self.scenarios_by_dimension
        
        if normalized_type in self.scenarios_by_business_and_dimension:
            return self.scenarios_by_business_and_dimension[normalized_type]
        
        # Return generic if no business-specific
        return self.generic_by_dimension
    
    def validate_coverage(self) -> Dict[str, Any]:
        """Validate scenario coverage for all business types."""
        required_dimensions = [
            "innovativeness", "risk_taking", "achievement_orientation",
            "autonomy_orientation", "proactiveness", "locus_of_control", "self_efficacy"
        ]
        
        report = {
            "version": self.scenario_bank.get("version", "1.0.0"),
            "has_business_specific": self.has_business_specific,
            "business_types": {},
            "warnings": [],
            "valid": True
        }
        
        if self.has_business_specific:
            for business_type in self.business_scenarios.keys():
                dims = self.scenarios_by_business_and_dimension.get(business_type, {})
                report["business_types"][business_type] = {
                    "dimensions_covered": len(dims),
                    "scenarios_per_dimension": {
                        dim: len(dims.get(dim, [])) for dim in required_dimensions
                    }
                }
                
                # Check coverage
                for dim in required_dimensions:
                    if dim not in dims or len(dims[dim]) < 1:
                        report["warnings"].append(
                            f"{business_type}: Missing dimension '{dim}'"
                        )
                        report["valid"] = False
        
        return report
    
    def get_session_history(self, session_id: str) -> List[str]:
        """Get list of scenario IDs shown in a session."""
        return self._session_scenarios.get(session_id, [])
    
    def clear_session(self, session_id: str):
        """Clear session tracking data."""
        if session_id in self._session_scenarios:
            del self._session_scenarios[session_id]


# Compatibility: Use enhanced generator as default
ScenarioGenerator = EnhancedScenarioGenerator


if __name__ == "__main__":
    # Test the enhanced generator
    generator = EnhancedScenarioGenerator()
    
    print("=== Enhanced Scenario Generator Validation ===\n")
    report = generator.validate_coverage()
    print(f"Version: {report['version']}")
    print(f"Has business-specific scenarios: {report['has_business_specific']}")
    print(f"Valid: {report['valid']}")
    
    if report['warnings']:
        print("\nWarnings:")
        for w in report['warnings']:
            print(f"  - {w}")
    
    print("\n=== Business Type Coverage ===")
    for biz_type, data in report.get('business_types', {}).items():
        print(f"\n{biz_type.upper()}:")
        print(f"  Dimensions: {data['dimensions_covered']}/7")
        for dim, count in data['scenarios_per_dimension'].items():
            status = "✓" if count > 0 else "✗"
            print(f"    {status} {dim}: {count}")
    
    # Test personalization
    print("\n=== Personalization Test ===")
    
    test_cases = [
        {'business_type': 'restaurant', 'name': 'Restaurant'},
        {'business_type': 'consulting', 'name': 'Beratung'},
        {'business_type': 'saas', 'name': 'SaaS'},
        {'business_type': 'ecommerce', 'name': 'E-Commerce'},
    ]
    
    for ctx in test_cases:
        scenario = generator.generate_scenario(
            dimension='innovativeness',
            target_difficulty=0.0,
            business_context=ctx
        )
        formatted = generator.format_for_frontend(scenario, include_metadata=True)
        print(f"\n{ctx['name']}:")
        print(f"  ID: {formatted['scenario_id']}")
        print(f"  Situation: {formatted['situation'][:80]}...")
