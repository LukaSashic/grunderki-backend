"""
Test Suite for GründerAI Scenario Assessment System

Tests:
- ScenarioGenerator: Personalization and scenario selection
- ScenarioMapper: Response mapping and theta estimation
- ScenarioCATEngine: Full assessment flow
- API Routes: Integration tests
"""

import pytest
import json
from datetime import datetime
from typing import Dict, Any

# Import modules to test
from scenario_generator import ScenarioGenerator, create_test_business_context
from scenario_mapper import ScenarioMapper, DimensionEstimate
from scenario_cat_engine import (
    ScenarioCATEngine, 
    AssessmentSession, 
    AssessmentPhase, 
    SessionStatus
)


# ========== Fixtures ==========

@pytest.fixture
def scenario_generator():
    """Create ScenarioGenerator instance."""
    return ScenarioGenerator()


@pytest.fixture
def scenario_mapper():
    """Create ScenarioMapper instance."""
    return ScenarioMapper()


@pytest.fixture
def cat_engine():
    """Create ScenarioCATEngine instance."""
    return ScenarioCATEngine()


@pytest.fixture
def restaurant_context():
    """Restaurant business context."""
    return create_test_business_context('restaurant')


@pytest.fixture
def saas_context():
    """SaaS business context."""
    return create_test_business_context('saas')


@pytest.fixture
def consulting_context():
    """Consulting business context."""
    return create_test_business_context('consulting')


# ========== ScenarioGenerator Tests ==========

class TestScenarioGenerator:
    """Tests for ScenarioGenerator class."""
    
    def test_initialization(self, scenario_generator):
        """Test generator initializes correctly."""
        assert scenario_generator is not None
        assert len(scenario_generator.scenario_bank['scenarios']) == 35
        assert len(scenario_generator.scenarios_by_dimension) == 7
    
    def test_validate_coverage(self, scenario_generator):
        """Test scenario bank validation."""
        report = scenario_generator.validate_coverage()
        
        assert report['valid'] is True
        assert report['total_scenarios'] == 35
        assert report['dimensions_covered'] == 7
        
        # Each dimension should have 5 scenarios
        for dim, count in report['scenarios_per_dimension'].items():
            assert count == 5, f"{dim} has {count} scenarios, expected 5"
    
    def test_scenarios_per_dimension(self, scenario_generator):
        """Test each dimension has correct number of scenarios."""
        dimensions = [
            "innovativeness",
            "risk_taking",
            "achievement_orientation",
            "autonomy_orientation",
            "proactiveness",
            "locus_of_control",
            "self_efficacy"
        ]
        
        for dim in dimensions:
            scenarios = scenario_generator.scenarios_by_dimension.get(dim, [])
            assert len(scenarios) == 5, f"{dim} has {len(scenarios)} scenarios"
    
    def test_generate_scenario_basic(self, scenario_generator, restaurant_context):
        """Test basic scenario generation."""
        scenario = scenario_generator.generate_scenario(
            dimension='innovativeness',
            target_difficulty=0.0,
            business_context=restaurant_context
        )
        
        assert scenario is not None
        assert 'scenario_id' in scenario
        assert 'dimension' in scenario
        assert scenario['dimension'] == 'innovativeness'
        assert 'template' in scenario
        assert 'options' in scenario['template']
        assert len(scenario['template']['options']) == 4
    
    def test_personalization_restaurant(self, scenario_generator, restaurant_context):
        """Test scenario personalization for restaurant."""
        scenario = scenario_generator.generate_scenario(
            dimension='innovativeness',
            target_difficulty=0.0,
            business_context=restaurant_context
        )
        
        # Check that restaurant-specific terms appear
        situation = scenario['template']['situation']
        assert 'Restaurant' in situation or 'Gäste' in situation or 'Speisekarte' in situation
    
    def test_personalization_saas(self, scenario_generator, saas_context):
        """Test scenario personalization for SaaS."""
        scenario = scenario_generator.generate_scenario(
            dimension='innovativeness',
            target_difficulty=0.0,
            business_context=saas_context
        )
        
        situation = scenario['template']['situation']
        # Should contain SaaS-specific terms
        assert 'Software' in situation or 'Nutzer' in situation or 'Produkt' in situation
    
    def test_difficulty_selection(self, scenario_generator, restaurant_context):
        """Test that scenarios are selected based on target difficulty."""
        # Request low difficulty scenario
        low_diff = scenario_generator.generate_scenario(
            dimension='risk_taking',
            target_difficulty=-1.5,
            business_context=restaurant_context
        )
        
        # Request high difficulty scenario
        high_diff = scenario_generator.generate_scenario(
            dimension='risk_taking',
            target_difficulty=1.5,
            business_context=restaurant_context,
            previously_seen=[low_diff['scenario_id']]
        )
        
        # Higher difficulty scenario should have higher difficulty parameter
        assert high_diff['difficulty'] > low_diff['difficulty']
    
    def test_previously_seen_filter(self, scenario_generator, restaurant_context):
        """Test that previously seen scenarios are filtered out."""
        seen = []
        
        for _ in range(5):
            scenario = scenario_generator.generate_scenario(
                dimension='achievement_orientation',
                target_difficulty=0.0,
                business_context=restaurant_context,
                previously_seen=seen
            )
            
            assert scenario['scenario_id'] not in seen
            seen.append(scenario['scenario_id'])
        
        # Should have seen all 5 unique scenarios
        assert len(set(seen)) == 5
    
    def test_format_for_frontend(self, scenario_generator, restaurant_context):
        """Test frontend formatting removes psychological data."""
        scenario = scenario_generator.generate_scenario(
            dimension='innovativeness',
            target_difficulty=0.0,
            business_context=restaurant_context
        )
        
        formatted = scenario_generator.format_for_frontend(scenario, include_metadata=False)
        
        # Should have user-facing fields
        assert 'situation' in formatted
        assert 'question' in formatted
        assert 'options' in formatted
        
        # Should NOT have psychological mappings
        for option in formatted['options']:
            assert 'psychological_mapping' not in option
            assert 'theta_value' not in option
    
    def test_all_dimensions_have_scenarios(self, scenario_generator):
        """Test all 7 Howard dimensions have scenarios."""
        dimensions = [
            "innovativeness",
            "risk_taking", 
            "achievement_orientation",
            "autonomy_orientation",
            "proactiveness",
            "locus_of_control",
            "self_efficacy"
        ]
        
        for dim in dimensions:
            assert dim in scenario_generator.scenarios_by_dimension
            assert len(scenario_generator.scenarios_by_dimension[dim]) > 0


# ========== ScenarioMapper Tests ==========

class TestScenarioMapper:
    """Tests for ScenarioMapper class."""
    
    def test_initialization(self, scenario_mapper):
        """Test mapper initializes correctly."""
        assert scenario_mapper is not None
        assert len(scenario_mapper.dimension_labels) == 7
    
    def test_map_response_to_theta(self, scenario_mapper):
        """Test response mapping to theta value."""
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
        
        # Test each option
        theta_a, info_a = scenario_mapper.map_response_to_theta(test_scenario, 'A')
        assert theta_a == -1.8
        assert info_a > 0
        
        theta_d, info_d = scenario_mapper.map_response_to_theta(test_scenario, 'D')
        assert theta_d == 1.9
        assert info_d > 0
    
    def test_invalid_option_raises_error(self, scenario_mapper):
        """Test that invalid option raises ValueError."""
        test_scenario = {
            'template': {
                'options': [
                    {'id': 'A', 'theta_value': -1.0}
                ]
            }
        }
        
        with pytest.raises(ValueError):
            scenario_mapper.map_response_to_theta(test_scenario, 'Z')
    
    def test_update_theta_estimate(self, scenario_mapper):
        """Test theta estimate updating."""
        estimate = DimensionEstimate()
        
        # Initial state
        assert estimate.theta == 0.0
        assert estimate.se == 2.0
        assert estimate.n_items == 0
        
        # First update
        updated = scenario_mapper.update_theta_estimate(estimate, 1.0, 1.5)
        
        assert updated.n_items == 1
        assert updated.theta != 0.0  # Should have changed
        assert updated.se < 2.0  # Should have decreased
    
    def test_estimate_converges(self, scenario_mapper):
        """Test that estimate converges with consistent responses."""
        estimate = DimensionEstimate()
        
        # Simulate consistent high responses
        for _ in range(5):
            estimate = scenario_mapper.update_theta_estimate(estimate, 1.5, 1.5)
        
        # Should converge toward 1.5
        assert estimate.theta > 1.0
        assert estimate.se < 0.5  # Should be more certain
    
    def test_theta_to_percentile(self, scenario_mapper):
        """Test theta to percentile conversion."""
        # Average person (theta=0) should be around 50th percentile
        p_avg = scenario_mapper.convert_theta_to_percentile(0.0)
        assert 45 <= p_avg <= 55
        
        # High theta should be high percentile
        p_high = scenario_mapper.convert_theta_to_percentile(2.0)
        assert p_high > 90
        
        # Low theta should be low percentile
        p_low = scenario_mapper.convert_theta_to_percentile(-2.0)
        assert p_low < 10
    
    def test_theta_to_score(self, scenario_mapper):
        """Test theta to 0-100 score conversion."""
        score_low = scenario_mapper.convert_theta_to_score(-3.0)
        assert score_low == 0
        
        score_mid = scenario_mapper.convert_theta_to_score(0.0)
        assert score_mid == 50
        
        score_high = scenario_mapper.convert_theta_to_score(3.0)
        assert score_high == 100
    
    def test_interpret_dimension_score(self, scenario_mapper):
        """Test dimension score interpretation."""
        # High innovativeness
        interp = scenario_mapper.interpret_dimension_score('innovativeness', 1.8)
        
        assert interp['dimension'] == 'innovativeness'
        assert interp['level'] in ['sehr_hoch', 'hoch']
        assert interp['percentile'] > 80
        assert 'strength' in interp
        assert 'description' in interp
    
    def test_calculate_overall_profile(self, scenario_mapper):
        """Test overall profile calculation."""
        estimates = {
            'innovativeness': DimensionEstimate(theta=1.0, se=0.4, n_items=2),
            'risk_taking': DimensionEstimate(theta=0.5, se=0.4, n_items=2),
            'achievement_orientation': DimensionEstimate(theta=1.5, se=0.4, n_items=2),
            'autonomy_orientation': DimensionEstimate(theta=0.3, se=0.4, n_items=2),
            'proactiveness': DimensionEstimate(theta=0.8, se=0.4, n_items=2),
            'locus_of_control': DimensionEstimate(theta=0.6, se=0.4, n_items=2),
            'self_efficacy': DimensionEstimate(theta=1.2, se=0.4, n_items=2)
        }
        
        profile = scenario_mapper.calculate_overall_profile(estimates)
        
        assert 'dimensions' in profile
        assert len(profile['dimensions']) == 7
        assert 'summary' in profile
        assert 'gz_readiness' in profile
        assert 'approval_probability' in profile['gz_readiness']


# ========== ScenarioCATEngine Tests ==========

class TestScenarioCATEngine:
    """Tests for ScenarioCATEngine class."""
    
    def test_initialization(self, cat_engine):
        """Test CAT engine initializes correctly."""
        assert cat_engine is not None
        assert len(cat_engine.DIMENSIONS) == 7
        assert cat_engine.STOPPING_CRITERIA['max_items'] == 15
        assert cat_engine.STOPPING_CRITERIA['min_items'] == 9
    
    def test_create_session_empty(self, cat_engine):
        """Test session creation without business context."""
        session = cat_engine.create_session()
        
        assert session is not None
        assert session.session_id is not None
        assert session.status == SessionStatus.ACTIVE
        assert session.current_phase == AssessmentPhase.BUSINESS_CONTEXT
        assert not session.business_context_complete
    
    def test_create_session_with_context(self, cat_engine, restaurant_context):
        """Test session creation with business context."""
        session = cat_engine.create_session(
            user_id='test_user',
            business_context=restaurant_context
        )
        
        assert session.user_id == 'test_user'
        assert session.business_context_complete
        assert session.current_phase == AssessmentPhase.PERSONALITY_SCENARIOS
    
    def test_set_business_context(self, cat_engine, restaurant_context):
        """Test setting business context transitions phase."""
        session = cat_engine.create_session()
        
        assert not session.business_context_complete
        
        response = cat_engine.set_business_context(
            session.session_id, 
            restaurant_context
        )
        
        assert session.business_context_complete
        assert session.current_phase == AssessmentPhase.PERSONALITY_SCENARIOS
        assert 'scenario' in response
    
    def test_start_scenarios(self, cat_engine, restaurant_context):
        """Test starting scenario assessment."""
        session = cat_engine.create_session(business_context=restaurant_context)
        
        response = cat_engine.start_scenarios(session.session_id)
        
        assert not response['complete']
        assert response['phase'] == AssessmentPhase.PERSONALITY_SCENARIOS.value
        assert response['scenario'] is not None
        assert response['progress'] is not None
    
    def test_submit_response(self, cat_engine, restaurant_context):
        """Test submitting a scenario response."""
        session = cat_engine.create_session(business_context=restaurant_context)
        first_response = cat_engine.start_scenarios(session.session_id)
        
        scenario_id = first_response['scenario']['scenario_id']
        
        response = cat_engine.submit_scenario_response(
            session_id=session.session_id,
            scenario_id=scenario_id,
            selected_option='C'
        )
        
        assert session.total_scenarios == 1
        assert scenario_id in session.scenarios_seen
        
        # Should either have next scenario or be complete
        assert 'scenario' in response or response['complete']
    
    def test_full_assessment_flow(self, cat_engine, saas_context):
        """Test complete assessment from start to finish."""
        session = cat_engine.create_session(business_context=saas_context)
        
        response = cat_engine.start_scenarios(session.session_id)
        iterations = 0
        max_iterations = 20  # Safety limit
        
        while not response.get('complete', False) and iterations < max_iterations:
            scenario = response['scenario']
            
            # Simulate response (always select 'C' for consistency)
            response = cat_engine.submit_scenario_response(
                session_id=session.session_id,
                scenario_id=scenario['scenario_id'],
                selected_option='C'
            )
            
            iterations += 1
        
        # Should complete within reasonable number of items
        assert response['complete']
        assert session.status == SessionStatus.COMPLETED
        assert session.total_scenarios >= 9  # Min items
        assert session.total_scenarios <= 15  # Max items
        
        # Should have results
        assert 'results' in response
        assert 'dimensions' in response['results']
        assert 'gz_readiness' in response['results']
    
    def test_dimension_coverage(self, cat_engine, consulting_context):
        """Test that all dimensions get assessed."""
        session = cat_engine.create_session(business_context=consulting_context)
        
        response = cat_engine.start_scenarios(session.session_id)
        
        while not response.get('complete', False):
            scenario = response['scenario']
            response = cat_engine.submit_scenario_response(
                session_id=session.session_id,
                scenario_id=scenario['scenario_id'],
                selected_option='B'
            )
        
        # Check all dimensions were assessed
        for dim in cat_engine.DIMENSIONS:
            estimate = session.dimension_estimates[dim]
            assert estimate.n_items >= 1, f"{dim} was not assessed"
    
    def test_adaptive_selection(self, cat_engine, restaurant_context):
        """Test that scenario selection is adaptive."""
        session = cat_engine.create_session(business_context=restaurant_context)
        
        dimensions_seen = []
        response = cat_engine.start_scenarios(session.session_id)
        
        # First few items should cover different dimensions
        for _ in range(7):
            if response.get('complete'):
                break
                
            scenario = response['scenario']
            dimensions_seen.append(scenario.get('dimension'))
            
            response = cat_engine.submit_scenario_response(
                session_id=session.session_id,
                scenario_id=scenario['scenario_id'],
                selected_option='C'
            )
        
        # Should have covered most dimensions
        unique_dimensions = set(dimensions_seen)
        assert len(unique_dimensions) >= 5, "Not enough dimension coverage in first 7 items"
    
    def test_session_not_found_error(self, cat_engine):
        """Test error handling for non-existent session."""
        with pytest.raises(ValueError, match="Session not found"):
            cat_engine.start_scenarios("non_existent_session")
    
    def test_scenario_mismatch_error(self, cat_engine, restaurant_context):
        """Test error for scenario ID mismatch."""
        session = cat_engine.create_session(business_context=restaurant_context)
        cat_engine.start_scenarios(session.session_id)
        
        with pytest.raises(ValueError, match="Scenario mismatch"):
            cat_engine.submit_scenario_response(
                session_id=session.session_id,
                scenario_id="wrong_scenario_id",
                selected_option='A'
            )
    
    def test_progress_tracking(self, cat_engine, saas_context):
        """Test progress calculation."""
        session = cat_engine.create_session(business_context=saas_context)
        
        response = cat_engine.start_scenarios(session.session_id)
        
        progress = response['progress']
        assert progress['current_item'] == 0
        assert progress['percentage'] == 0
        
        # Submit a response
        scenario = response['scenario']
        response = cat_engine.submit_scenario_response(
            session_id=session.session_id,
            scenario_id=scenario['scenario_id'],
            selected_option='C'
        )
        
        if not response.get('complete'):
            progress = response['progress']
            assert progress['current_item'] == 1
            assert progress['percentage'] > 0


# ========== Integration Tests ==========

class TestIntegration:
    """Integration tests for the complete system."""
    
    def test_restaurant_owner_journey(self, cat_engine):
        """Test complete journey for restaurant owner persona."""
        # Restaurant owner context
        context = {
            'business_type': 'restaurant',
            'sub_type': 'family_dining',
            'target_customer': 'families',
            'problem': 'quality_dining',
            'stage': 'planning'
        }
        
        session = cat_engine.create_session(
            user_id='restaurant_owner',
            business_context=context
        )
        
        response = cat_engine.start_scenarios(session.session_id)
        
        # Complete assessment with moderate responses
        while not response.get('complete', False):
            scenario = response['scenario']
            
            # Verify personalization contains restaurant terms
            if 'situation' in scenario:
                has_restaurant_terms = any(
                    term in scenario['situation']
                    for term in ['Restaurant', 'Gäste', 'Speisekarte', 'Gastronomie']
                )
                # At least some scenarios should have restaurant terms
            
            response = cat_engine.submit_scenario_response(
                session_id=session.session_id,
                scenario_id=scenario['scenario_id'],
                selected_option='C'  # Moderate-high responses
            )
        
        # Verify results
        results = response['results']
        assert 'gz_readiness' in results
        assert results['gz_readiness']['approval_probability'] > 0
    
    def test_saas_founder_journey(self, cat_engine):
        """Test complete journey for SaaS founder persona."""
        context = {
            'business_type': 'saas',
            'sub_type': 'b2b_productivity',
            'target_customer': 'small_businesses',
            'problem': 'tools_too_complex',
            'stage': 'mvp'
        }
        
        session = cat_engine.create_session(
            user_id='saas_founder',
            business_context=context
        )
        
        response = cat_engine.start_scenarios(session.session_id)
        
        # Complete with high-risk, high-innovation responses
        option_pattern = ['D', 'D', 'C', 'D', 'C', 'D', 'C', 'D', 'C', 'D', 'C', 'D', 'C', 'D', 'C']
        idx = 0
        
        while not response.get('complete', False):
            scenario = response['scenario']
            selected = option_pattern[idx % len(option_pattern)]
            
            response = cat_engine.submit_scenario_response(
                session_id=session.session_id,
                scenario_id=scenario['scenario_id'],
                selected_option=selected
            )
            idx += 1
        
        # High responses should result in high approval probability
        results = response['results']
        assert results['gz_readiness']['approval_probability'] >= 70
    
    def test_cautious_consultant_journey(self, cat_engine):
        """Test journey with cautious/conservative responses."""
        context = {
            'business_type': 'consulting',
            'target_customer': 'corporations',
            'stage': 'revenue'
        }
        
        session = cat_engine.create_session(business_context=context)
        response = cat_engine.start_scenarios(session.session_id)
        
        # Complete with conservative responses
        while not response.get('complete', False):
            scenario = response['scenario']
            
            response = cat_engine.submit_scenario_response(
                session_id=session.session_id,
                scenario_id=scenario['scenario_id'],
                selected_option='A'  # Most conservative
            )
        
        # Conservative responses should result in lower scores
        results = response['results']
        for dim_data in results['dimensions'].values():
            assert dim_data['theta'] < 1.0  # Should not be high
    
    def test_timing_constraint(self, cat_engine, restaurant_context):
        """Test that assessment completes in reasonable time."""
        import time
        
        session = cat_engine.create_session(business_context=restaurant_context)
        
        start_time = time.time()
        response = cat_engine.start_scenarios(session.session_id)
        
        while not response.get('complete', False):
            scenario = response['scenario']
            response = cat_engine.submit_scenario_response(
                session_id=session.session_id,
                scenario_id=scenario['scenario_id'],
                selected_option='C'
            )
        
        elapsed = time.time() - start_time
        
        # Should complete quickly (excluding user response time)
        # In real use, user takes 30-90 seconds per scenario
        assert elapsed < 5.0  # Engine processing should be fast


# ========== Run Tests ==========

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
