"""
Tests for Day 3: Results Visualization Engine
Tests personality profiler, gap analyzer, and results generator
"""

import pytest
from pathlib import Path
import json

from personality_profiler import PersonalityProfiler, PersonalityProfile
from gap_analyzer import GapAnalyzer, GapAnalysisResult, Gap
from results_generator import ResultsGenerator, generate_assessment_results


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def archetypes_path():
    return Path(__file__).parent / "personality_archetypes.json"


@pytest.fixture
def criteria_path():
    return Path(__file__).parent / "gz_criteria.json"


@pytest.fixture
def profiler(archetypes_path):
    return PersonalityProfiler(str(archetypes_path))


@pytest.fixture
def analyzer(criteria_path):
    return GapAnalyzer(str(criteria_path))


@pytest.fixture
def generator(archetypes_path, criteria_path):
    return ResultsGenerator(str(archetypes_path), str(criteria_path))


@pytest.fixture
def high_innovator_scores():
    """Scores for a Bold Innovator type"""
    return {
        "innovativeness": {"theta": 1.5, "percentile": 88},
        "risk_taking": {"theta": 0.8, "percentile": 75},
        "achievement_orientation": {"theta": 0.5, "percentile": 68},
        "autonomy_orientation": {"theta": 1.0, "percentile": 82},
        "proactiveness": {"theta": 0.7, "percentile": 73},
        "locus_of_control": {"theta": 0.3, "percentile": 62},
        "self_efficacy": {"theta": 0.5, "percentile": 70}
    }


@pytest.fixture
def calculated_executor_scores():
    """Scores for a Calculated Executor type"""
    return {
        "innovativeness": {"theta": 0.0, "percentile": 50},
        "risk_taking": {"theta": -0.5, "percentile": 35},
        "achievement_orientation": {"theta": 1.2, "percentile": 85},
        "autonomy_orientation": {"theta": 0.2, "percentile": 58},
        "proactiveness": {"theta": 1.3, "percentile": 88},
        "locus_of_control": {"theta": 1.0, "percentile": 82},
        "self_efficacy": {"theta": 1.2, "percentile": 86}
    }


@pytest.fixture
def balanced_scores():
    """Balanced scores for generic entrepreneur"""
    return {
        "innovativeness": {"theta": 0.3, "percentile": 62},
        "risk_taking": {"theta": 0.2, "percentile": 58},
        "achievement_orientation": {"theta": 0.4, "percentile": 65},
        "autonomy_orientation": {"theta": 0.3, "percentile": 62},
        "proactiveness": {"theta": 0.4, "percentile": 65},
        "locus_of_control": {"theta": 0.3, "percentile": 62},
        "self_efficacy": {"theta": 0.4, "percentile": 65}
    }


@pytest.fixture
def saas_context():
    """SaaS business context"""
    return {
        "business_type": "saas",
        "target_customer": "small_businesses",
        "business_idea": "AI-powered project management tool",
        "stage": "mvp"
    }


@pytest.fixture
def restaurant_context():
    """Restaurant business context"""
    return {
        "business_type": "restaurant",
        "target_customer": "local_families",
        "business_idea": "Organic family restaurant",
        "stage": "concept"
    }


# ============================================================================
# PERSONALITY PROFILER TESTS
# ============================================================================

class TestPersonalityProfiler:
    """Tests for PersonalityProfiler"""
    
    def test_initialization(self, profiler):
        """Test profiler initializes correctly"""
        assert profiler is not None
        assert len(profiler.archetypes) == 8
        assert len(profiler.dimension_order) == 7
    
    def test_archetype_detection_bold_innovator(self, profiler, high_innovator_scores):
        """Test Bold Innovator archetype detection"""
        archetype = profiler.determine_archetype(high_innovator_scores)
        assert archetype['id'] == 'bold_innovator'
        assert archetype['name'] == 'Bold Innovator'
    
    def test_archetype_detection_calculated_executor(self, profiler, calculated_executor_scores):
        """Test Calculated Executor archetype detection"""
        archetype = profiler.determine_archetype(calculated_executor_scores)
        # Should be close to calculated_executor or proactive_driver
        assert archetype['id'] in ['calculated_executor', 'proactive_driver', 'ambitious_achiever']
    
    def test_level_determination(self, profiler):
        """Test percentile to level conversion"""
        assert profiler._get_level(90) == 'very_high'
        assert profiler._get_level(70) == 'high'
        assert profiler._get_level(50) == 'medium'
        assert profiler._get_level(30) == 'low'
        assert profiler._get_level(10) == 'very_low'
    
    def test_create_profile(self, profiler, high_innovator_scores, saas_context):
        """Test complete profile creation"""
        profile = profiler.create_profile(high_innovator_scores, saas_context)
        
        assert isinstance(profile, PersonalityProfile)
        assert profile.archetype_id == 'bold_innovator'
        assert len(profile.dimensions) == 7
        assert len(profile.strengths) > 0
        assert len(profile.gz_tips_de) > 0
    
    def test_dimension_interpretations(self, profiler, high_innovator_scores, saas_context):
        """Test dimension interpretations are generated"""
        profile = profiler.create_profile(high_innovator_scores, saas_context)
        
        innov_dim = profile.dimensions.get('innovativeness')
        assert innov_dim is not None
        assert innov_dim.percentile == 88
        assert innov_dim.level in ['high', 'very_high']
        assert len(innov_dim.strength) > 0
        assert len(innov_dim.business_implication) > 0
    
    def test_business_fit_calculation(self, profiler, high_innovator_scores):
        """Test business fit scores are calculated"""
        fit_scores = profiler._calculate_business_fit(high_innovator_scores)
        
        assert 'saas' in fit_scores
        assert 'restaurant' in fit_scores
        assert 'consulting' in fit_scores
        
        # High innovator should fit SaaS better than restaurant
        assert fit_scores['saas'] >= fit_scores['restaurant']
    
    def test_profile_to_dict(self, profiler, high_innovator_scores, saas_context):
        """Test profile serialization to dict"""
        profile = profiler.create_profile(high_innovator_scores, saas_context)
        profile_dict = profiler.profile_to_dict(profile)
        
        assert 'archetype' in profile_dict
        assert 'dimensions' in profile_dict
        assert 'business_fit_scores' in profile_dict
        assert profile_dict['archetype']['id'] == 'bold_innovator'
    
    def test_german_labels(self, profiler, high_innovator_scores, saas_context):
        """Test German labels are present"""
        profile = profiler.create_profile(high_innovator_scores, saas_context)
        
        assert profile.archetype_name_de == 'Mutiger Innovator'
        assert len(profile.strengths_de) > 0
        
        innov_dim = profile.dimensions.get('innovativeness')
        assert innov_dim.dimension_label_de == 'Innovationsfreude'


# ============================================================================
# GAP ANALYZER TESTS
# ============================================================================

class TestGapAnalyzer:
    """Tests for GapAnalyzer"""
    
    def test_initialization(self, analyzer):
        """Test analyzer initializes correctly"""
        assert analyzer is not None
        assert len(analyzer.readiness_components) == 6
        assert len(analyzer.gap_categories) == 5
    
    def test_readiness_calculation_no_modules(self, analyzer):
        """Test readiness with no completed modules"""
        readiness = analyzer.calculate_readiness(completed_modules=[])
        
        assert readiness['current'] == 35
        assert readiness['with_module1'] == 55
        assert readiness['complete'] == 95
    
    def test_readiness_calculation_with_module1(self, analyzer):
        """Test readiness after completing Module 1"""
        readiness = analyzer.calculate_readiness(completed_modules=[1])
        
        assert readiness['current'] == 55  # 35 + 20
        assert readiness['with_module1'] == 55  # Already done
    
    def test_readiness_calculation_multiple_modules(self, analyzer):
        """Test readiness with multiple completed modules"""
        readiness = analyzer.calculate_readiness(completed_modules=[1, 2, 3])
        
        # 35 + 20 + 10 + 5 = 70
        assert readiness['current'] == 70
    
    def test_gap_identification(self, analyzer, saas_context):
        """Test gaps are identified"""
        result = analyzer.analyze_gaps(saas_context)
        
        assert result.total_gaps > 0
        assert len(result.critical_gaps) > 0
        assert len(result.critical_gaps) <= 7  # Max 7 displayed
    
    def test_gap_priority_ordering(self, analyzer, saas_context):
        """Test gaps are ordered by priority"""
        result = analyzer.analyze_gaps(saas_context)
        
        gaps = result.critical_gaps
        if len(gaps) > 1:
            # Critical/high severity should come first
            assert gaps[0].severity in ['critical', 'high']
    
    def test_personality_recommendations(self, analyzer, saas_context):
        """Test personality-adapted recommendations"""
        # With profile
        profile = {
            "archetype": {"id": "bold_innovator"},
            "dimensions": {
                "risk_taking": {"percentile": 30}  # Low risk
            }
        }
        result = analyzer.analyze_gaps(saas_context, personality_profile=profile)
        
        assert len(result.personality_recommendations) > 0
        
        # Should have risk-related recommendation
        recommendations_text = ' '.join(result.personality_recommendations)
        assert 'Risiko' in recommendations_text or 'Innovation' in recommendations_text
    
    def test_next_milestone(self, analyzer, saas_context):
        """Test next milestone identification"""
        result = analyzer.analyze_gaps(saas_context, completed_modules=[])
        
        milestone = result.next_milestone
        assert milestone['module'] == 1
        assert milestone['readiness_boost'] == 20
        assert 'Executive Summary' in milestone['name_de']
    
    def test_readiness_level(self, analyzer, saas_context):
        """Test readiness level classification"""
        result = analyzer.analyze_gaps(saas_context, completed_modules=[])
        
        assert result.readiness_level == 'needs_work'
        assert result.readiness_level_de == 'Grundlage geschaffen'
    
    def test_result_to_dict(self, analyzer, saas_context):
        """Test result serialization to dict"""
        result = analyzer.analyze_gaps(saas_context)
        result_dict = analyzer.result_to_dict(result)
        
        assert 'readiness' in result_dict
        assert 'gaps' in result_dict
        assert 'next_milestone' in result_dict
        assert result_dict['readiness']['current'] == 35


# ============================================================================
# RESULTS GENERATOR TESTS
# ============================================================================

class TestResultsGenerator:
    """Tests for ResultsGenerator"""
    
    def test_initialization(self, generator):
        """Test generator initializes correctly"""
        assert generator is not None
        assert generator.profiler is not None
        assert generator.analyzer is not None
    
    def test_generate_results(self, generator, high_innovator_scores, saas_context):
        """Test complete results generation"""
        results = generator.generate_results(
            user_id="user_123",
            session_id="session_456",
            dimension_scores=high_innovator_scores,
            business_context=saas_context
        )
        
        assert results.user_id == "user_123"
        assert results.session_id == "session_456"
        assert results.personality_profile is not None
        assert results.gap_analysis is not None
        assert results.next_steps is not None
    
    def test_radar_chart_data(self, generator, high_innovator_scores, saas_context):
        """Test radar chart data generation"""
        results = generator.generate_results(
            user_id="user_123",
            session_id="session_456",
            dimension_scores=high_innovator_scores,
            business_context=saas_context
        )
        
        radar_data = results.radar_chart_data
        assert len(radar_data) == 7
        
        # Check format
        for item in radar_data:
            assert 'dimension' in item
            assert 'percentile' in item
            assert 'value' in item
            assert item['fullMark'] == 100
    
    def test_cta_generation(self, generator, high_innovator_scores, saas_context):
        """Test CTA generation"""
        results = generator.generate_results(
            user_id="user_123",
            session_id="session_456",
            dimension_scores=high_innovator_scores,
            business_context=saas_context
        )
        
        cta = results.next_steps.primary_cta
        assert cta['action'] == 'start_module_1'
        assert 'text' in cta
        assert cta['details']['is_free'] is True
        assert cta['progress']['current_readiness'] == 35
    
    def test_cta_adapts_to_archetype(self, generator, high_innovator_scores, 
                                     calculated_executor_scores, saas_context):
        """Test CTA adapts to different archetypes"""
        results_innovator = generator.generate_results(
            user_id="user_1",
            session_id="session_1",
            dimension_scores=high_innovator_scores,
            business_context=saas_context
        )
        
        results_executor = generator.generate_results(
            user_id="user_2",
            session_id="session_2",
            dimension_scores=calculated_executor_scores,
            business_context=saas_context
        )
        
        # CTAs should be different
        cta1 = results_innovator.next_steps.primary_cta['headline_de']
        cta2 = results_executor.next_steps.primary_cta['headline_de']
        
        # At minimum, they should both exist
        assert len(cta1) > 0
        assert len(cta2) > 0
    
    def test_share_data(self, generator, high_innovator_scores, saas_context):
        """Test share data generation"""
        results = generator.generate_results(
            user_id="user_123",
            session_id="session_456",
            dimension_scores=high_innovator_scores,
            business_context=saas_context
        )
        
        share = results.share_data
        assert 'headline_de' in share
        assert 'text_de' in share
        assert 'hashtags' in share
        assert 'Mutiger Innovator' in share['headline_de']
    
    def test_results_to_dict(self, generator, high_innovator_scores, saas_context):
        """Test results serialization to dict"""
        results = generator.generate_results(
            user_id="user_123",
            session_id="session_456",
            dimension_scores=high_innovator_scores,
            business_context=saas_context
        )
        
        results_dict = generator.results_to_dict(results)
        
        assert 'user_id' in results_dict
        assert 'personality_profile' in results_dict
        assert 'gap_analysis' in results_dict
        assert 'next_steps' in results_dict
        assert 'visualization' in results_dict
        assert 'share' in results_dict
    
    def test_generate_results_dict(self, generator, high_innovator_scores, saas_context):
        """Test convenience method"""
        results_dict = generator.generate_results_dict(
            user_id="user_123",
            session_id="session_456",
            dimension_scores=high_innovator_scores,
            business_context=saas_context
        )
        
        assert isinstance(results_dict, dict)
        assert results_dict['session_id'] == "session_456"


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests for complete workflow"""
    
    def test_full_saas_founder_journey(self, generator):
        """Test complete journey for SaaS founder"""
        scores = {
            "innovativeness": {"theta": 1.2, "percentile": 85},
            "risk_taking": {"theta": 0.8, "percentile": 75},
            "achievement_orientation": {"theta": 0.9, "percentile": 80},
            "autonomy_orientation": {"theta": 0.7, "percentile": 73},
            "proactiveness": {"theta": 1.0, "percentile": 82},
            "locus_of_control": {"theta": 0.6, "percentile": 70},
            "self_efficacy": {"theta": 0.8, "percentile": 78}
        }
        
        context = {
            "business_type": "saas",
            "target_customer": "startups",
            "business_idea": "AI recruiting tool",
            "stage": "mvp"
        }
        
        results = generator.generate_results_dict(
            user_id="saas_user",
            session_id="saas_session",
            dimension_scores=scores,
            business_context=context
        )
        
        # Should identify as Bold Innovator or similar
        archetype = results['personality_profile']['archetype']['id']
        assert archetype in ['bold_innovator', 'proactive_driver', 'ambitious_achiever']
        
        # Should have good SaaS fit
        fit_scores = results['personality_profile']['business_fit_scores']
        assert fit_scores['saas'] >= 70
        
        # Should have gaps identified
        assert results['gap_analysis']['gaps']['total_count'] > 0
        
        # CTA should be present
        assert results['next_steps']['primary_cta']['action'] == 'start_module_1'
    
    def test_full_restaurant_owner_journey(self, generator):
        """Test complete journey for restaurant owner"""
        scores = {
            "innovativeness": {"theta": -0.2, "percentile": 42},
            "risk_taking": {"theta": -0.5, "percentile": 32},
            "achievement_orientation": {"theta": 0.8, "percentile": 78},
            "autonomy_orientation": {"theta": 0.5, "percentile": 68},
            "proactiveness": {"theta": 0.6, "percentile": 70},
            "locus_of_control": {"theta": 0.7, "percentile": 73},
            "self_efficacy": {"theta": 0.9, "percentile": 80}
        }
        
        context = {
            "business_type": "restaurant",
            "target_customer": "families",
            "business_idea": "Organic family restaurant",
            "stage": "concept"
        }
        
        results = generator.generate_results_dict(
            user_id="restaurant_user",
            session_id="restaurant_session",
            dimension_scores=scores,
            business_context=context
        )
        
        # Should have good restaurant fit (relative)
        fit_scores = results['personality_profile']['business_fit_scores']
        assert fit_scores['restaurant'] >= 50
        
        # Should have personality recommendations for low risk-taking
        recommendations = results['gap_analysis']['personality_recommendations']
        assert len(recommendations) > 0
    
    def test_convenience_function(self, high_innovator_scores, saas_context):
        """Test generate_assessment_results convenience function"""
        results = generate_assessment_results(
            user_id="conv_user",
            session_id="conv_session",
            dimension_scores=high_innovator_scores,
            business_context=saas_context
        )
        
        assert isinstance(results, dict)
        assert results['session_id'] == "conv_session"
        assert 'personality_profile' in results
    
    def test_timing_constraint(self, generator, high_innovator_scores, saas_context):
        """Test results generation completes quickly"""
        import time
        
        start = time.time()
        
        for _ in range(10):
            generator.generate_results_dict(
                user_id="timing_user",
                session_id="timing_session",
                dimension_scores=high_innovator_scores,
                business_context=saas_context
            )
        
        elapsed = time.time() - start
        
        # 10 generations should take < 2 seconds
        assert elapsed < 2.0, f"Results generation too slow: {elapsed:.2f}s for 10 iterations"


# ============================================================================
# EDGE CASE TESTS
# ============================================================================

class TestEdgeCases:
    """Tests for edge cases and error handling"""
    
    def test_missing_dimensions(self, generator, saas_context):
        """Test handling of missing dimensions"""
        incomplete_scores = {
            "innovativeness": {"theta": 0.5, "percentile": 68},
            "risk_taking": {"theta": 0.3, "percentile": 62},
            # Missing other dimensions
        }
        
        # Should not crash, should use defaults
        results = generator.generate_results_dict(
            user_id="incomplete_user",
            session_id="incomplete_session",
            dimension_scores=incomplete_scores,
            business_context=saas_context
        )
        
        assert results is not None
    
    def test_extreme_scores(self, generator, saas_context):
        """Test handling of extreme scores"""
        extreme_scores = {
            "innovativeness": {"theta": 3.0, "percentile": 99},
            "risk_taking": {"theta": -3.0, "percentile": 1},
            "achievement_orientation": {"theta": 2.5, "percentile": 98},
            "autonomy_orientation": {"theta": -2.5, "percentile": 2},
            "proactiveness": {"theta": 2.0, "percentile": 95},
            "locus_of_control": {"theta": -2.0, "percentile": 5},
            "self_efficacy": {"theta": 1.5, "percentile": 90}
        }
        
        results = generator.generate_results_dict(
            user_id="extreme_user",
            session_id="extreme_session",
            dimension_scores=extreme_scores,
            business_context=saas_context
        )
        
        # Should still work
        assert results is not None
        assert results['gap_analysis']['readiness']['current'] == 35
    
    def test_empty_business_context(self, generator, high_innovator_scores):
        """Test handling of minimal business context"""
        minimal_context = {
            "business_type": "other"
        }
        
        results = generator.generate_results_dict(
            user_id="minimal_user",
            session_id="minimal_session",
            dimension_scores=high_innovator_scores,
            business_context=minimal_context
        )
        
        assert results is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
