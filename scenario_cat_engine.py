"""
Scenario CAT Engine - Computerized Adaptive Testing with Business Scenarios
Core Innovation: "Invisible Personality Integration"

This engine orchestrates the complete personality assessment using business scenarios
that feel like natural planning decisions while measuring Howard's 7 dimensions.
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timezone
import uuid
import json
from pathlib import Path
from enum import Enum
from dataclasses import dataclass, field, asdict

from scenario_generator import ScenarioGenerator
from scenario_mapper import ScenarioMapper, DimensionEstimate


class AssessmentPhase(str, Enum):
    """Assessment phases in the user journey."""
    BUSINESS_CONTEXT = "business_context"
    PERSONALITY_SCENARIOS = "personality_scenarios"
    COMPLETED = "completed"


class SessionStatus(str, Enum):
    """Session status values."""
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


@dataclass
class AssessmentSession:
    """Complete assessment session state."""
    session_id: str
    user_id: Optional[str] = None
    
    # Phase tracking
    current_phase: AssessmentPhase = AssessmentPhase.BUSINESS_CONTEXT
    status: SessionStatus = SessionStatus.ACTIVE
    
    # Business context from Day 1
    business_context: Dict[str, Any] = field(default_factory=dict)
    business_context_complete: bool = False
    
    # Personality assessment state
    dimension_estimates: Dict[str, DimensionEstimate] = field(default_factory=dict)
    scenarios_seen: List[str] = field(default_factory=list)
    current_scenario_id: Optional[str] = None
    current_dimension: Optional[str] = None
    total_scenarios: int = 0
    
    # Timing
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    business_context_completed_at: Optional[str] = None
    scenarios_completed_at: Optional[str] = None
    
    # Results
    final_results: Optional[Dict] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for storage."""
        return {
            'session_id': self.session_id,
            'user_id': self.user_id,
            'current_phase': self.current_phase.value,
            'status': self.status.value,
            'business_context': self.business_context,
            'business_context_complete': self.business_context_complete,
            'dimension_estimates': {
                dim: est.to_dict() for dim, est in self.dimension_estimates.items()
            },
            'scenarios_seen': self.scenarios_seen,
            'current_scenario_id': self.current_scenario_id,
            'current_dimension': self.current_dimension,
            'total_scenarios': self.total_scenarios,
            'started_at': self.started_at,
            'business_context_completed_at': self.business_context_completed_at,
            'scenarios_completed_at': self.scenarios_completed_at,
            'final_results': self.final_results
        }


class ScenarioCATEngine:
    """
    Computerized Adaptive Testing engine using business scenarios.
    
    Key Features:
    - Seamless integration with Day 1 business context
    - Adaptive scenario selection based on IRT
    - Real-time theta estimation per dimension
    - Micro-insights after dimension completion
    - Final profile with GZ readiness assessment
    """
    
    # Howard's 7 dimensions
    DIMENSIONS = [
        "innovativeness",
        "risk_taking",
        "achievement_orientation",
        "autonomy_orientation",
        "proactiveness",
        "locus_of_control",
        "self_efficacy"
    ]
    
    # CAT stopping criteria
    STOPPING_CRITERIA = {
        'max_items': 15,           # Maximum scenarios total
        'min_items': 9,            # Minimum scenarios total
        'min_per_dimension': 1,    # Minimum items per dimension
        'target_per_dimension': 2, # Target items per dimension
        'target_se': 0.5,          # Target SE for stopping
        'max_time_minutes': 20     # Maximum time allowed
    }
    
    def __init__(self, scenario_bank_path: Optional[str] = None):
        """
        Initialize CAT engine.
        
        Args:
            scenario_bank_path: Path to scenario bank JSON
        """
        self.scenario_generator = ScenarioGenerator(scenario_bank_path)
        self.scenario_mapper = ScenarioMapper()
        
        # Session storage (in-memory for now - will be replaced with DB)
        self._sessions: Dict[str, AssessmentSession] = {}
    
    # ========== Session Management ==========
    
    def create_session(
        self,
        user_id: Optional[str] = None,
        business_context: Optional[Dict] = None
    ) -> AssessmentSession:
        """
        Create a new assessment session.
        
        Args:
            user_id: Optional user identifier
            business_context: Optional pre-populated business context
            
        Returns:
            New assessment session
        """
        session_id = str(uuid.uuid4())
        
        # Initialize dimension estimates
        dimension_estimates = {
            dim: DimensionEstimate() for dim in self.DIMENSIONS
        }
        
        session = AssessmentSession(
            session_id=session_id,
            user_id=user_id,
            dimension_estimates=dimension_estimates
        )
        
        # If business context provided, skip to scenarios
        if business_context and self._validate_business_context(business_context):
            session.business_context = business_context
            session.business_context_complete = True
            session.current_phase = AssessmentPhase.PERSONALITY_SCENARIOS
            session.business_context_completed_at = datetime.now(timezone.utc).isoformat()
        
        self._sessions[session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[AssessmentSession]:
        """Get session by ID."""
        return self._sessions.get(session_id)
    
    def _validate_business_context(self, context: Dict) -> bool:
        """Validate that business context has required fields."""
        required = ['business_type']
        return all(key in context for key in required)
    
    # ========== Business Context Integration ==========
    
    def set_business_context(
        self,
        session_id: str,
        business_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Set business context from Day 1 and transition to scenarios.
        
        Args:
            session_id: Session identifier
            business_context: Complete business context from Day 1
            
        Returns:
            Response with first scenario
        """
        session = self.get_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        if session.status != SessionStatus.ACTIVE:
            raise ValueError(f"Session is not active: {session.status}")
        
        # Store business context
        session.business_context = business_context
        session.business_context_complete = True
        session.business_context_completed_at = datetime.now(timezone.utc).isoformat()
        
        # Transition to personality scenarios
        session.current_phase = AssessmentPhase.PERSONALITY_SCENARIOS
        
        # Generate first scenario
        return self._generate_next_scenario_response(session)
    
    # ========== Scenario Assessment ==========
    
    def start_scenarios(self, session_id: str) -> Dict[str, Any]:
        """
        Start the scenario assessment phase.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Response with first scenario
        """
        session = self.get_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        if not session.business_context_complete:
            raise ValueError("Business context must be completed first")
        
        if session.status != SessionStatus.ACTIVE:
            raise ValueError(f"Session is not active: {session.status}")
        
        session.current_phase = AssessmentPhase.PERSONALITY_SCENARIOS
        
        return self._generate_next_scenario_response(session)
    
    def submit_scenario_response(
        self,
        session_id: str,
        scenario_id: str,
        selected_option: str
    ) -> Dict[str, Any]:
        """
        Process user's response to a scenario.
        
        Args:
            session_id: Session identifier
            scenario_id: ID of the scenario being answered
            selected_option: Option ID selected (A/B/C/D)
            
        Returns:
            Next scenario or completion response
        """
        session = self.get_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        if session.status != SessionStatus.ACTIVE:
            raise ValueError(f"Session is not active: {session.status}")
        
        if session.current_scenario_id != scenario_id:
            raise ValueError(f"Scenario mismatch: expected {session.current_scenario_id}")
        
        # Get the scenario
        scenario = self._get_scenario_by_id(scenario_id)
        dimension = scenario['dimension']
        
        # Map response to theta
        theta_value, information = self.scenario_mapper.map_response_to_theta(
            scenario,
            selected_option
        )
        
        # Update dimension estimate
        current_estimate = session.dimension_estimates[dimension]
        updated_estimate = self.scenario_mapper.update_theta_estimate(
            current_estimate,
            theta_value,
            information
        )
        session.dimension_estimates[dimension] = updated_estimate
        
        # Track scenario as seen
        session.scenarios_seen.append(scenario_id)
        session.total_scenarios += 1
        
        # Check if this dimension is complete
        dimension_complete = self._is_dimension_complete(session, dimension)
        
        # Check if assessment should stop
        if self._should_stop(session):
            return self._generate_completion_response(session)
        
        # Generate response with optional micro-insight
        response = self._generate_next_scenario_response(session)
        
        if dimension_complete:
            # Add micro-insight for completed dimension
            response['micro_insight'] = self._generate_micro_insight(
                session, dimension
            )
        
        return response
    
    def _generate_next_scenario_response(
        self,
        session: AssessmentSession
    ) -> Dict[str, Any]:
        """Generate response with the next scenario."""
        # Select next dimension to assess
        dimension = self._select_next_dimension(session)
        
        if dimension is None:
            return self._generate_completion_response(session)
        
        # Calculate target difficulty based on current estimate
        current_estimate = session.dimension_estimates[dimension]
        target_difficulty = current_estimate.theta
        
        # Generate personalized scenario
        scenario = self.scenario_generator.generate_scenario(
            dimension=dimension,
            target_difficulty=target_difficulty,
            business_context=session.business_context,
            previously_seen=session.scenarios_seen,
            session_id=session.session_id
        )
        
        # Update session state
        session.current_scenario_id = scenario['scenario_id']
        session.current_dimension = dimension
        
        # Format for frontend (hide psychological mappings)
        formatted_scenario = self.scenario_generator.format_for_frontend(
            scenario,
            include_metadata=True
        )
        
        return {
            'complete': False,
            'phase': AssessmentPhase.PERSONALITY_SCENARIOS.value,
            'scenario': formatted_scenario,
            'progress': self._calculate_progress(session)
        }
    
    def _select_next_dimension(
        self,
        session: AssessmentSession
    ) -> Optional[str]:
        """
        Select the next dimension to assess using adaptive logic.
        
        Priority:
        1. Dimensions with fewer than minimum items
        2. Dimensions with highest uncertainty (SE)
        3. Dimensions below target items
        """
        # First, ensure all dimensions have minimum items
        for dim in self.DIMENSIONS:
            estimate = session.dimension_estimates[dim]
            if estimate.n_items < self.STOPPING_CRITERIA['min_per_dimension']:
                return dim
        
        # Then, prioritize dimensions with highest uncertainty
        # Filter to dimensions below target
        candidates = [
            (dim, session.dimension_estimates[dim])
            for dim in self.DIMENSIONS
            if session.dimension_estimates[dim].n_items < self.STOPPING_CRITERIA['target_per_dimension']
        ]
        
        if candidates:
            # Sort by SE (highest first) to reduce uncertainty
            candidates.sort(key=lambda x: x[1].se, reverse=True)
            return candidates[0][0]
        
        # All dimensions at target - stop or continue based on overall SE
        return None
    
    def _is_dimension_complete(
        self,
        session: AssessmentSession,
        dimension: str
    ) -> bool:
        """Check if a dimension has enough items."""
        estimate = session.dimension_estimates[dimension]
        return (
            estimate.n_items >= self.STOPPING_CRITERIA['min_per_dimension'] and
            estimate.se < self.STOPPING_CRITERIA['target_se']
        )
    
    def _should_stop(self, session: AssessmentSession) -> bool:
        """Check if assessment should stop."""
        # Stop if maximum items reached
        if session.total_scenarios >= self.STOPPING_CRITERIA['max_items']:
            return True
        
        # Don't stop before minimum
        if session.total_scenarios < self.STOPPING_CRITERIA['min_items']:
            return False
        
        # Check if all dimensions have minimum coverage
        all_dimensions_covered = all(
            session.dimension_estimates[dim].n_items >= self.STOPPING_CRITERIA['min_per_dimension']
            for dim in self.DIMENSIONS
        )
        
        if not all_dimensions_covered:
            return False
        
        # Check if all dimensions have acceptable SE
        all_precise = all(
            session.dimension_estimates[dim].se < self.STOPPING_CRITERIA['target_se']
            for dim in self.DIMENSIONS
        )
        
        return all_precise
    
    def _calculate_progress(self, session: AssessmentSession) -> Dict[str, Any]:
        """Calculate assessment progress."""
        completed_items = session.total_scenarios
        
        # Estimate total based on current progress
        if completed_items == 0:
            estimated_total = 12  # Default estimate
        else:
            # Calculate based on dimensions completed
            dimensions_at_target = sum(
                1 for dim in self.DIMENSIONS
                if session.dimension_estimates[dim].n_items >= self.STOPPING_CRITERIA['target_per_dimension']
            )
            remaining_items = (7 - dimensions_at_target) * 2
            estimated_total = completed_items + remaining_items
            estimated_total = max(self.STOPPING_CRITERIA['min_items'], 
                                min(self.STOPPING_CRITERIA['max_items'], estimated_total))
        
        percentage = int((completed_items / estimated_total) * 100)
        
        return {
            'current_item': completed_items,
            'estimated_total': estimated_total,
            'percentage': min(99, percentage),  # Never show 100% until complete
            'dimensions_assessed': sum(
                1 for dim in self.DIMENSIONS
                if session.dimension_estimates[dim].n_items > 0
            ),
            'total_dimensions': 7
        }
    
    def _generate_micro_insight(
        self,
        session: AssessmentSession,
        dimension: str
    ) -> Dict[str, str]:
        """
        Generate brief insight after completing a dimension.
        
        Keeps user engaged without revealing full assessment intent.
        """
        estimate = session.dimension_estimates[dimension]
        interpretation = self.scenario_mapper.interpret_dimension_score(
            dimension,
            estimate.theta,
            session.business_context
        )
        
        return {
            'title': 'Zwischenerkenntnis',
            'icon': self._get_dimension_icon(dimension),
            'message': f"{interpretation['strength']} - {interpretation['description'][:100]}..."
        }
    
    def _get_dimension_icon(self, dimension: str) -> str:
        """Get emoji icon for dimension."""
        icons = {
            'innovativeness': '💡',
            'risk_taking': '🎯',
            'achievement_orientation': '🏆',
            'autonomy_orientation': '🦅',
            'proactiveness': '🚀',
            'locus_of_control': '🎮',
            'self_efficacy': '💪'
        }
        return icons.get(dimension, '📊')
    
    def _generate_completion_response(
        self,
        session: AssessmentSession
    ) -> Dict[str, Any]:
        """Generate final results when assessment is complete."""
        # Mark session as complete
        session.status = SessionStatus.COMPLETED
        session.current_phase = AssessmentPhase.COMPLETED
        session.scenarios_completed_at = datetime.now(timezone.utc).isoformat()
        
        # Calculate final profile
        profile = self.scenario_mapper.calculate_overall_profile(
            session.dimension_estimates
        )
        
        # Store results
        session.final_results = profile
        
        return {
            'complete': True,
            'phase': AssessmentPhase.COMPLETED.value,
            'results': profile,
            'summary': {
                'total_scenarios': session.total_scenarios,
                'session_duration': self._calculate_duration(session),
                'business_type': session.business_context.get('business_type', 'unknown')
            }
        }
    
    def _calculate_duration(self, session: AssessmentSession) -> str:
        """Calculate session duration."""
        try:
            start = datetime.fromisoformat(session.started_at.replace('Z', '+00:00'))
            end = datetime.now(timezone.utc)
            duration = end - start
            minutes = int(duration.total_seconds() / 60)
            return f"{minutes} Minuten"
        except:
            return "Unbekannt"
    
    def _get_scenario_by_id(self, scenario_id: str) -> Dict[str, Any]:
        """Retrieve scenario from bank by ID."""
        for scenario in self.scenario_generator.scenario_bank['scenarios']:
            if scenario['scenario_id'] == scenario_id:
                # Need to personalize with current session's business context
                return scenario
        raise ValueError(f"Scenario not found: {scenario_id}")
    
    # ========== Results & Analytics ==========
    
    def get_results(self, session_id: str) -> Dict[str, Any]:
        """
        Get final assessment results.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Complete results with profile and recommendations
        """
        session = self.get_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        if session.status != SessionStatus.COMPLETED:
            raise ValueError("Assessment not yet completed")
        
        return session.final_results
    
    def get_session_state(self, session_id: str) -> Dict[str, Any]:
        """Get current session state for debugging/admin."""
        session = self.get_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        return session.to_dict()


# ========== Database Integration Helpers ==========

def session_to_db_record(session: AssessmentSession) -> Dict[str, Any]:
    """Convert session to database record format."""
    return {
        'session_id': session.session_id,
        'user_id': session.user_id,
        'current_phase': session.current_phase.value,
        'status': session.status.value,
        'business_context': json.dumps(session.business_context),
        'dimension_estimates': json.dumps({
            dim: est.to_dict() for dim, est in session.dimension_estimates.items()
        }),
        'scenarios_seen': json.dumps(session.scenarios_seen),
        'total_scenarios': session.total_scenarios,
        'started_at': session.started_at,
        'business_context_completed_at': session.business_context_completed_at,
        'scenarios_completed_at': session.scenarios_completed_at,
        'final_results': json.dumps(session.final_results) if session.final_results else None
    }


def db_record_to_session(record: Dict[str, Any]) -> AssessmentSession:
    """Convert database record to session object."""
    # Parse JSON fields
    business_context = json.loads(record.get('business_context', '{}'))
    dimension_estimates_raw = json.loads(record.get('dimension_estimates', '{}'))
    scenarios_seen = json.loads(record.get('scenarios_seen', '[]'))
    final_results = json.loads(record['final_results']) if record.get('final_results') else None
    
    # Reconstruct dimension estimates
    dimension_estimates = {}
    for dim, data in dimension_estimates_raw.items():
        dimension_estimates[dim] = DimensionEstimate(
            theta=data.get('theta', 0.0),
            se=data.get('se', 2.0),
            n_items=data.get('n_items', 0),
            responses=data.get('responses', [])
        )
    
    return AssessmentSession(
        session_id=record['session_id'],
        user_id=record.get('user_id'),
        current_phase=AssessmentPhase(record.get('current_phase', 'business_context')),
        status=SessionStatus(record.get('status', 'active')),
        business_context=business_context,
        business_context_complete=bool(business_context.get('business_type')),
        dimension_estimates=dimension_estimates,
        scenarios_seen=scenarios_seen,
        total_scenarios=record.get('total_scenarios', 0),
        started_at=record.get('started_at', datetime.now(timezone.utc).isoformat()),
        business_context_completed_at=record.get('business_context_completed_at'),
        scenarios_completed_at=record.get('scenarios_completed_at'),
        final_results=final_results
    )


if __name__ == "__main__":
    # Test the CAT engine
    from scenario_generator import create_test_business_context
    
    print("=== Scenario CAT Engine Test ===\n")
    
    engine = ScenarioCATEngine()
    
    # Create session with business context
    business_context = create_test_business_context('saas')
    session = engine.create_session(
        user_id='test_user',
        business_context=business_context
    )
    
    print(f"Session created: {session.session_id}")
    print(f"Phase: {session.current_phase.value}")
    print(f"Business type: {session.business_context.get('business_type')}")
    
    # Simulate assessment
    print("\n--- Starting Scenarios ---\n")
    
    response = engine.start_scenarios(session.session_id)
    
    while not response.get('complete', False):
        scenario = response['scenario']
        progress = response['progress']
        
        print(f"Item {progress['current_item'] + 1}/{progress['estimated_total']}")
        print(f"Dimension: {scenario.get('dimension', 'unknown')}")
        print(f"Situation: {scenario['situation'][:80]}...")
        print(f"Question: {scenario['question']}")
        
        # Simulate random response (in real use, this comes from user)
        import random
        options = ['A', 'B', 'C', 'D']
        selected = random.choice(options)
        print(f"Selected: {selected}")
        
        # Submit response
        response = engine.submit_scenario_response(
            session.session_id,
            scenario['scenario_id'],
            selected
        )
        
        if response.get('micro_insight'):
            print(f"Insight: {response['micro_insight']['message']}")
        
        print()
    
    # Show results
    print("=== Assessment Complete ===\n")
    
    results = response['results']
    print(f"GZ Approval Probability: {results['gz_readiness']['approval_probability']}%")
    print(f"\nStrengths: {', '.join(results['gz_readiness']['strengths'])}")
    print(f"Development: {', '.join(results['gz_readiness']['development_areas'])}")
    
    print("\nDimension Scores:")
    for dim, data in results['dimensions'].items():
        print(f"  {data['dimension_label']}: {data['level_de']} ({data['percentile']}%ile)")
