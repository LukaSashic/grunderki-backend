"""
AI-Powered Scenario Generator using Claude API
Generates truly personalized business scenarios for invisible personality assessment

This replaces the static scenario_bank.json approach with dynamic AI generation
that creates unique, business-context-aware scenarios for each user.
"""

import os
import json
from typing import Dict, Any, List, Optional
from anthropic import Anthropic
from dataclasses import dataclass
import hashlib

# Initialize Anthropic client
client = Anthropic()

# Howard's 7 Entrepreneurial Personality Dimensions
DIMENSIONS = {
    "innovativeness": {
        "name_de": "Innovationsfreude",
        "description": "Tendency to generate and embrace novel ideas and solutions",
        "low_behavior": "Prefers proven, established methods",
        "high_behavior": "Seeks new approaches, disrupts conventions"
    },
    "risk_taking": {
        "name_de": "Risikobereitschaft", 
        "description": "Comfort with uncertainty and willingness to take chances",
        "low_behavior": "Careful, prefers security and predictability",
        "high_behavior": "Bold, embraces uncertainty for potential gains"
    },
    "achievement_orientation": {
        "name_de": "Leistungsorientierung",
        "description": "Drive for excellence and high standards",
        "low_behavior": "Satisfied with good enough, work-life balance focused",
        "high_behavior": "Pushes for excellence, goal-driven"
    },
    "autonomy_orientation": {
        "name_de": "Autonomieorientierung",
        "description": "Preference for independence and self-direction",
        "low_behavior": "Values guidance, team input, consensus",
        "high_behavior": "Prefers independence, own decisions"
    },
    "proactiveness": {
        "name_de": "Proaktivität",
        "description": "Initiative and forward-thinking action",
        "low_behavior": "Reactive, responds to situations",
        "high_behavior": "Anticipates, initiates, shapes environment"
    },
    "locus_of_control": {
        "name_de": "Kontrollüberzeugung",
        "description": "Belief in personal control over outcomes",
        "low_behavior": "Attributes outcomes to external factors",
        "high_behavior": "Takes full ownership of results"
    },
    "self_efficacy": {
        "name_de": "Selbstwirksamkeit",
        "description": "Confidence in ability to succeed",
        "low_behavior": "Doubts ability, seeks validation",
        "high_behavior": "Strong belief in own capabilities"
    }
}

# Business Type Contexts for Deep Personalization
BUSINESS_CONTEXTS = {
    "restaurant": {
        "label_de": "Restaurant",
        "industry_de": "Gastronomie",
        "typical_challenges": ["Standortwahl", "Personalfindung", "Lieferanten", "Stammkunden aufbauen"],
        "typical_decisions": ["Speisekarte", "Öffnungszeiten", "Preisgestaltung", "Events"],
        "stakeholders": ["Gäste", "Lieferanten", "Mitarbeiter", "Nachbarn"],
        "success_metrics": ["Tagesumsatz", "Auslastung", "Bewertungen", "Stammkundenanteil"]
    },
    "saas": {
        "label_de": "Software-Unternehmen",
        "industry_de": "Tech/SaaS",
        "typical_challenges": ["Feature-Entwicklung", "Kundenbindung", "Skalierung", "Konkurrenz"],
        "typical_decisions": ["Roadmap", "Pricing", "Vertriebskanal", "Support-Level"],
        "stakeholders": ["Nutzer", "Entwickler", "Investoren", "Partner"],
        "success_metrics": ["MRR", "Churn Rate", "NPS", "Aktivierungsrate"]
    },
    "consulting": {
        "label_de": "Beratung",
        "industry_de": "Beratungsbranche", 
        "typical_challenges": ["Akquise", "Positionierung", "Preisgestaltung", "Skalierung"],
        "typical_decisions": ["Spezialisierung", "Tagessätze", "Kundenauswahl", "Team aufbauen"],
        "stakeholders": ["Kunden", "Auftraggeber", "Partner", "Mitbewerber"],
        "success_metrics": ["Auslastung", "Tagessatz", "Empfehlungsrate", "Folgeaufträge"]
    },
    "ecommerce": {
        "label_de": "Online-Shop",
        "industry_de": "E-Commerce",
        "typical_challenges": ["Traffic", "Conversion", "Logistik", "Retouren"],
        "typical_decisions": ["Sortiment", "Plattform", "Marketing", "Fulfillment"],
        "stakeholders": ["Käufer", "Lieferanten", "Logistikpartner", "Marktplätze"],
        "success_metrics": ["Conversion Rate", "AOV", "Retourenquote", "CAC"]
    },
    "services": {
        "label_de": "Dienstleistung",
        "industry_de": "Dienstleistungssektor",
        "typical_challenges": ["Kundengewinnung", "Termintreue", "Qualität", "Konkurrenz"],
        "typical_decisions": ["Preise", "Einzugsgebiet", "Spezialisierung", "Tools"],
        "stakeholders": ["Kunden", "Auftraggeber", "Lieferanten", "Mitbewerber"],
        "success_metrics": ["Aufträge/Monat", "Kundenzufriedenheit", "Weiterempfehlungen"]
    },
    "creative": {
        "label_de": "Kreativagentur",
        "industry_de": "Kreativwirtschaft",
        "typical_challenges": ["Akquise", "Kreativität vs. Budget", "Kundenwünsche", "Projektmanagement"],
        "typical_decisions": ["Stil/Nische", "Preise", "Kundenauswahl", "Teamaufbau"],
        "stakeholders": ["Auftraggeber", "Kreativpartner", "Lieferanten"],
        "success_metrics": ["Projektmarge", "Folgeaufträge", "Portfolio-Qualität"]
    },
    "health": {
        "label_de": "Gesundheitsunternehmen",
        "industry_de": "Gesundheitssektor",
        "typical_challenges": ["Zulassungen", "Vertrauen aufbauen", "Abrechnung", "Konkurrenz"],
        "typical_decisions": ["Spezialisierung", "Standort", "Kassenzulassung", "Behandlungsspektrum"],
        "stakeholders": ["Patienten", "Krankenkassen", "Zuweiser", "Kollegen"],
        "success_metrics": ["Patientenzahl", "Terminauslastung", "Patientenzufriedenheit"]
    }
}

@dataclass
class GeneratedScenario:
    """A generated scenario with IRT parameters"""
    scenario_id: str
    dimension: str
    difficulty: float
    discrimination: float
    situation: str
    question: str
    options: List[Dict[str, Any]]
    business_type: str


def generate_scenario_prompt(
    dimension: str,
    target_difficulty: float,
    business_context: Dict[str, Any],
    previously_seen_themes: List[str] = None
) -> str:
    """Generate the prompt for Claude to create a personalized scenario"""
    
    business_type = business_context.get('business_type', 'services')
    biz_info = BUSINESS_CONTEXTS.get(business_type, BUSINESS_CONTEXTS['services'])
    dim_info = DIMENSIONS.get(dimension, DIMENSIONS['innovativeness'])
    
    # Map difficulty to scenario complexity
    if target_difficulty < -0.5:
        difficulty_hint = "ein einfaches Alltagsszenario"
    elif target_difficulty < 0.5:
        difficulty_hint = "eine mittelschwere strategische Entscheidung"
    else:
        difficulty_hint = "eine komplexe, herausfordernde Situation"
    
    # Get target customer info
    target_customer = business_context.get('target_customer', 'Kunden')
    stage = business_context.get('stage', 'Planung')
    description = business_context.get('description', '')
    
    # Avoid repeating themes
    avoid_themes = ""
    if previously_seen_themes:
        avoid_themes = f"\n\nVERMEIDE diese bereits verwendeten Themen: {', '.join(previously_seen_themes)}"
    
    return f"""Du bist ein Experte für psychometrische Persönlichkeitstests und Unternehmensgründung.

AUFGABE: Erstelle ein realistisches Geschäftsszenario für eine {biz_info['label_de']} ({biz_info['industry_de']}), das die Persönlichkeitsdimension "{dim_info['name_de']}" misst.

BUSINESS-KONTEXT:
- Geschäftstyp: {biz_info['label_de']}
- Branche: {biz_info['industry_de']}
- Zielkunden: {target_customer}
- Phase: {stage}
- Beschreibung: {description or 'Neugründung'}
- Typische Herausforderungen: {', '.join(biz_info['typical_challenges'])}
- Typische Entscheidungen: {', '.join(biz_info['typical_decisions'])}

DIMENSION "{dim_info['name_de']}":
- Beschreibung: {dim_info['description']}
- Niedrige Ausprägung: {dim_info['low_behavior']}
- Hohe Ausprägung: {dim_info['high_behavior']}

SCHWIERIGKEIT: {difficulty_hint} (IRT Difficulty: {target_difficulty:.1f})
{avoid_themes}

ANFORDERUNGEN:
1. Das Szenario muss sich wie eine echte Geschäftsentscheidung anfühlen, NICHT wie ein Persönlichkeitstest
2. Die Situation muss spezifisch für {biz_info['label_de']} sein (erwähne konkrete branchentypische Details)
3. ALLE 4 Antwortoptionen müssen vernünftig und professionell klingen
4. KEINE Option darf offensichtlich "richtig" oder "falsch" sein
5. Die Optionen müssen von niedrig bis hoch auf der Dimension kontinuierlich sein
6. Verwende Du-Form und informelle, aber professionelle Sprache
7. Das Szenario sollte 2-3 Sätze lang sein

ANTWORTE NUR MIT DIESEM JSON-FORMAT (keine andere Erklärung):
{{
  "situation": "Die konkrete Geschäftssituation in 2-3 Sätzen...",
  "question": "Eine kurze Frage wie 'Wie reagierst du?' oder 'Was machst du?'",
  "theme": "Ein Wort das das Thema beschreibt (z.B. 'Preisgestaltung', 'Mitarbeiter', 'Expansion')",
  "options": [
    {{
      "id": "A",
      "text": "Antwort für niedrige {dim_info['name_de']} - vorsichtig, konservativ",
      "theta_value": -1.5
    }},
    {{
      "id": "B", 
      "text": "Antwort für leicht unterdurchschnittliche {dim_info['name_de']}",
      "theta_value": -0.5
    }},
    {{
      "id": "C",
      "text": "Antwort für leicht überdurchschnittliche {dim_info['name_de']}",
      "theta_value": 0.5
    }},
    {{
      "id": "D",
      "text": "Antwort für hohe {dim_info['name_de']} - mutig, proaktiv",
      "theta_value": 1.5
    }}
  ]
}}"""


def generate_scenario(
    dimension: str,
    target_difficulty: float,
    business_context: Dict[str, Any],
    previously_seen_themes: List[str] = None,
    session_id: str = None
) -> GeneratedScenario:
    """
    Generate a personalized scenario using Claude API.
    
    Args:
        dimension: Howard dimension to measure
        target_difficulty: IRT difficulty parameter (-2 to +2)
        business_context: User's business information
        previously_seen_themes: Themes to avoid for variety
        session_id: For tracking/caching
    
    Returns:
        GeneratedScenario with all data needed for IRT calculation
    """
    
    prompt = generate_scenario_prompt(
        dimension=dimension,
        target_difficulty=target_difficulty,
        business_context=business_context,
        previously_seen_themes=previously_seen_themes
    )
    
    # Call Claude API
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # Parse response
    response_text = message.content[0].text
    
    # Extract JSON from response (handle potential markdown formatting)
    if "```json" in response_text:
        response_text = response_text.split("```json")[1].split("```")[0]
    elif "```" in response_text:
        response_text = response_text.split("```")[1].split("```")[0]
    
    scenario_data = json.loads(response_text.strip())
    
    # Generate unique scenario ID
    context_hash = hashlib.md5(
        f"{dimension}_{business_context.get('business_type')}_{target_difficulty}_{session_id}".encode()
    ).hexdigest()[:8]
    scenario_id = f"AI_{dimension.upper()[:4]}_{context_hash}"
    
    return GeneratedScenario(
        scenario_id=scenario_id,
        dimension=dimension,
        difficulty=target_difficulty,
        discrimination=1.6,  # Standard discrimination for AI-generated items
        situation=scenario_data['situation'],
        question=scenario_data['question'],
        options=scenario_data['options'],
        business_type=business_context.get('business_type', 'services')
    )


def format_for_frontend(scenario: GeneratedScenario, include_metadata: bool = False) -> Dict[str, Any]:
    """Format scenario for frontend display (hides IRT parameters)"""
    
    result = {
        'scenario_id': scenario.scenario_id,
        'situation': scenario.situation,
        'question': scenario.question,
        'options': [
            {'id': opt['id'], 'text': opt['text']}
            for opt in scenario.options
        ]
    }
    
    if include_metadata:
        result['dimension'] = scenario.dimension
    
    return result


def get_theta_for_option(scenario: GeneratedScenario, option_id: str) -> float:
    """Get the theta value for a selected option"""
    for opt in scenario.options:
        if opt['id'] == option_id:
            return opt['theta_value']
    return 0.0  # Default if not found


class AIScenarioCAT:
    """
    AI-Powered CAT Engine using Claude for scenario generation.
    
    This is the main class that manages the assessment flow with
    dynamically generated, fully personalized scenarios.
    """
    
    def __init__(self):
        self.sessions: Dict[str, Dict] = {}
    
    def create_session(
        self,
        session_id: str,
        business_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new assessment session"""
        
        self.sessions[session_id] = {
            'business_context': business_context,
            'responses': [],
            'theta_estimates': {dim: 0.0 for dim in DIMENSIONS},
            'se_estimates': {dim: 1.0 for dim in DIMENSIONS},
            'items_per_dimension': {dim: 0 for dim in DIMENSIONS},
            'seen_themes': [],
            'current_dimension_index': 0,
            'complete': False
        }
        
        return {'session_id': session_id, 'status': 'created'}
    
    def get_next_scenario(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get the next adaptively selected scenario"""
        
        session = self.sessions.get(session_id)
        if not session or session['complete']:
            return None
        
        # Select dimension that needs more items
        dimensions_order = list(DIMENSIONS.keys())
        current_dim = None
        
        for dim in dimensions_order:
            if session['items_per_dimension'][dim] < 2:  # Target 2 items per dimension
                current_dim = dim
                break
        
        if current_dim is None:
            # All dimensions have enough items
            session['complete'] = True
            return None
        
        # Get current theta estimate for adaptive difficulty
        current_theta = session['theta_estimates'][current_dim]
        
        # Generate scenario
        scenario = generate_scenario(
            dimension=current_dim,
            target_difficulty=current_theta,  # Adaptive: target current ability
            business_context=session['business_context'],
            previously_seen_themes=session['seen_themes'],
            session_id=session_id
        )
        
        # Store for later response processing
        session['current_scenario'] = scenario
        
        # Calculate progress
        total_items = sum(session['items_per_dimension'].values())
        total_needed = len(DIMENSIONS) * 2  # 14 items total
        
        return {
            'scenario': format_for_frontend(scenario, include_metadata=True),
            'progress': {
                'current_item': total_items + 1,
                'estimated_total': total_needed,
                'percentage': int((total_items / total_needed) * 100),
                'dimensions_assessed': sum(1 for v in session['items_per_dimension'].values() if v > 0)
            }
        }
    
    def submit_response(
        self,
        session_id: str,
        option_id: str
    ) -> Dict[str, Any]:
        """Process a response and update theta estimates"""
        
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError("Session not found")
        
        scenario = session.get('current_scenario')
        if not scenario:
            raise ValueError("No current scenario")
        
        # Get theta value for selected option
        theta = get_theta_for_option(scenario, option_id)
        
        # Update estimates (simplified Bayesian update)
        dim = scenario.dimension
        prior_theta = session['theta_estimates'][dim]
        prior_se = session['se_estimates'][dim]
        
        # Weight new information by reliability
        weight = 0.6 / (1 + session['items_per_dimension'][dim])
        new_theta = prior_theta * (1 - weight) + theta * weight
        new_se = prior_se * 0.85  # SE decreases with each item
        
        session['theta_estimates'][dim] = new_theta
        session['se_estimates'][dim] = new_se
        session['items_per_dimension'][dim] += 1
        
        # Track theme to avoid repetition
        if hasattr(scenario, 'theme'):
            session['seen_themes'].append(scenario.theme)
        
        # Store response
        session['responses'].append({
            'scenario_id': scenario.scenario_id,
            'dimension': dim,
            'option_id': option_id,
            'theta_value': theta
        })
        
        # Clear current scenario
        session['current_scenario'] = None
        
        # Check if complete
        total_items = sum(session['items_per_dimension'].values())
        if total_items >= len(DIMENSIONS) * 2:
            session['complete'] = True
            return {
                'complete': True,
                'results': self.get_results(session_id)
            }
        
        # Get next scenario
        next_data = self.get_next_scenario(session_id)
        return {
            'complete': False,
            **next_data
        }
    
    def get_results(self, session_id: str) -> Dict[str, Any]:
        """Get final assessment results"""
        
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError("Session not found")
        
        # Convert theta to percentiles
        def theta_to_percentile(theta: float) -> int:
            # Approximate normal distribution mapping
            import math
            z = theta / 1.0  # Assuming SD = 1
            percentile = 50 * (1 + math.erf(z / math.sqrt(2)))
            return max(1, min(99, int(percentile)))
        
        dimensions = {}
        for dim, theta in session['theta_estimates'].items():
            percentile = theta_to_percentile(theta)
            level = 'high' if percentile >= 70 else ('medium' if percentile >= 40 else 'low')
            dimensions[dim] = {
                'theta': round(theta, 2),
                'percentile': percentile,
                'level': level,
                'level_de': DIMENSIONS[dim]['name_de']
            }
        
        # Calculate average
        avg_theta = sum(session['theta_estimates'].values()) / len(DIMENSIONS)
        avg_percentile = theta_to_percentile(avg_theta)
        
        # GZ readiness based on profile
        gz_readiness = self._calculate_gz_readiness(dimensions)
        
        return {
            'dimensions': dimensions,
            'summary': {
                'average_theta': round(avg_theta, 2),
                'average_percentile': avg_percentile
            },
            'gz_readiness': gz_readiness
        }
    
    def _calculate_gz_readiness(self, dimensions: Dict) -> Dict[str, Any]:
        """Calculate Gründungszuschuss readiness based on personality profile"""
        
        # Key dimensions for GZ success
        key_dims = ['achievement_orientation', 'self_efficacy', 'proactiveness', 'locus_of_control']
        
        key_avg = sum(dimensions[d]['percentile'] for d in key_dims) / len(key_dims)
        
        # Strengths are high dimensions
        strengths = [
            dimensions[d]['level_de'] 
            for d, data in dimensions.items() 
            if data['percentile'] >= 65
        ][:3]
        
        # Development areas are lower dimensions
        development = [
            dimensions[d]['level_de']
            for d, data in dimensions.items()
            if data['percentile'] < 50
        ][:2]
        
        return {
            'approval_probability': int(min(95, max(35, key_avg + 10))),
            'strengths': strengths or ['Solide Grundlage'],
            'development_areas': development or ['Weiter aufbauen']
        }


# Singleton instance
_ai_cat_engine = None

def get_ai_cat_engine() -> AIScenarioCAT:
    """Get or create the AI CAT engine singleton"""
    global _ai_cat_engine
    if _ai_cat_engine is None:
        _ai_cat_engine = AIScenarioCAT()
    return _ai_cat_engine


# Test function
if __name__ == "__main__":
    # Test scenario generation
    print("Testing AI Scenario Generator...")
    
    test_context = {
        'business_type': 'restaurant',
        'target_customer': 'Familien mit Kindern',
        'stage': 'Planung',
        'description': 'Italienisches Restaurant im Stadtzentrum'
    }
    
    print("\n=== Restaurant Scenario ===")
    scenario = generate_scenario(
        dimension='innovativeness',
        target_difficulty=0.0,
        business_context=test_context,
        session_id='test123'
    )
    print(f"Situation: {scenario.situation}")
    print(f"Question: {scenario.question}")
    for opt in scenario.options:
        print(f"  {opt['id']}: {opt['text']}")
    
    # Test with SaaS context
    saas_context = {
        'business_type': 'saas',
        'target_customer': 'Kleine Unternehmen',
        'stage': 'MVP',
        'description': 'Projektmanagement-Tool für Teams'
    }
    
    print("\n=== SaaS Scenario ===")
    scenario2 = generate_scenario(
        dimension='innovativeness',
        target_difficulty=0.0,
        business_context=saas_context,
        session_id='test456'
    )
    print(f"Situation: {scenario2.situation}")
    print(f"Question: {scenario2.question}")
    for opt in scenario2.options:
        print(f"  {opt['id']}: {opt['text']}")
