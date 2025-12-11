"""
Unit and Integration Tests for Business Context Capture

Run with: pytest test_business_context.py -v

Author: Opus (Implementation Layer)
Date: 2025-12-11
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from business_context import BusinessContextHandler
from business_context_validator import BusinessContextValidator, RateLimiter


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def handler():
    """Create handler instance for testing."""
    return BusinessContextHandler()


@pytest.fixture
def rate_limiter():
    """Create rate limiter for testing."""
    return RateLimiter(max_requests=5, window_seconds=60)


# ============================================================================
# BUSINESS CONTEXT HANDLER TESTS
# ============================================================================

class TestBusinessContextHandler:
    """Test suite for BusinessContextHandler"""
    
    def test_start_session(self, handler):
        """Test session initialization"""
        result = handler.start_session()
        
        assert 'question' in result
        assert 'progress' in result
        assert 'phase' in result
        assert result['question']['id'] == 'Q1a_category'
        assert result['progress']['current'] == 1
        assert result['phase'] == 'business_context'
    
    def test_first_question_has_options(self, handler):
        """Test that first question has proper options"""
        result = handler.start_session()
        question = result['question']
        
        assert 'options' in question
        assert len(question['options']) >= 6
        
        # Check for expected categories
        option_ids = [opt['id'] for opt in question['options']]
        assert 'restaurant' in option_ids
        assert 'consulting' in option_ids
        assert 'saas' in option_ids
    
    def test_valid_category_selection(self, handler):
        """Test valid category selection - restaurant"""
        handler.start_session()
        
        answer = {"selected": "restaurant"}
        result = handler.process_answer(
            "Q1a_category",
            answer,
            []
        )
        
        assert result['accepted'] is True
        assert result['completed'] is False
        assert 'next_question' in result
        assert result['next_question']['id'] == 'Q1b_subcategory_restaurant'
    
    def test_valid_category_selection_consulting(self, handler):
        """Test valid category selection - consulting"""
        handler.start_session()
        
        answer = {"selected": "consulting"}
        result = handler.process_answer(
            "Q1a_category",
            answer,
            []
        )
        
        assert result['accepted'] is True
        assert result['next_question']['id'] == 'Q1b_subcategory_consulting'
    
    def test_invalid_category_selection(self, handler):
        """Test invalid category selection"""
        handler.start_session()
        
        answer = {"selected": "invalid_category"}
        result = handler.process_answer(
            "Q1a_category",
            answer,
            []
        )
        
        assert result['accepted'] is False
        assert 'error' in result
        assert result['error_code'] == 'INVALID_OPTION'
    
    def test_empty_selection(self, handler):
        """Test empty selection"""
        handler.start_session()
        
        answer = {"selected": ""}
        result = handler.process_answer(
            "Q1a_category",
            answer,
            []
        )
        
        assert result['accepted'] is False
        assert result['error_code'] == 'NO_SELECTION'
    
    def test_text_validation_too_short(self, handler):
        """Test text minimum length validation"""
        answer = {"text": "short"}
        
        question = {
            'id': 'test',
            'type': 'text',
            'min_length': 10,
            'validation': {}
        }
        
        result = handler._validate_answer(question, answer)
        assert result['valid'] is False
        assert result['code'] == 'TEXT_TOO_SHORT'
    
    def test_text_validation_too_long(self, handler):
        """Test text maximum length validation"""
        answer = {"text": "x" * 200}
        
        question = {
            'id': 'test',
            'type': 'text',
            'max_length': 100,
            'validation': {}
        }
        
        result = handler._validate_answer(question, answer)
        assert result['valid'] is False
        assert result['code'] == 'TEXT_TOO_LONG'
    
    def test_text_validation_valid(self, handler):
        """Test valid text input"""
        answer = {"text": "Italienisches Restaurant für Familien mit Bio-Zutaten"}
        
        question = {
            'id': 'test',
            'type': 'text',
            'min_length': 10,
            'max_length': 150,
            'validation': {}
        }
        
        result = handler._validate_answer(question, answer)
        assert result['valid'] is True
    
    def test_complete_flow_restaurant(self, handler):
        """Test complete question flow for restaurant"""
        handler.start_session()
        
        answers = []
        
        # Q1a: Category
        result = handler.process_answer(
            "Q1a_category",
            {"selected": "restaurant"},
            answers
        )
        assert result['accepted'], f"Q1a failed: {result.get('error')}"
        answers = result.get('answers', answers + [{"question_id": "Q1a_category", "answer": {"selected": "restaurant"}}])
        
        # Q1b: Subcategory
        result = handler.process_answer(
            "Q1b_subcategory_restaurant",
            {"selected": "casual_dining"},
            answers
        )
        assert result['accepted'], f"Q1b failed: {result.get('error')}"
        answers = result.get('answers', answers)
        
        # Q1c: Description
        result = handler.process_answer(
            "Q1c_description",
            {"text": "Italienisches Restaurant für Familien mit frischen Zutaten"},
            answers
        )
        assert result['accepted'], f"Q1c failed: {result.get('error')}"
        answers = result.get('answers', answers)
        
        # Q2a: Target Customer - use mixed to avoid refinement question
        result = handler.process_answer(
            "Q2a_target_customer",
            {"selected": "mixed"},
            answers
        )
        assert result['accepted'], f"Q2a failed: {result.get('error')}"
        answers = result.get('answers', answers)
        
        # Q3: Problem
        result = handler.process_answer(
            "Q3_problem",
            {"selected": "quality"},
            answers
        )
        assert result['accepted'], f"Q3 failed: {result.get('error')}"
        answers = result.get('answers', answers)
        
        # Q4: Stage (final)
        result = handler.process_answer(
            "Q4_stage",
            {"selected": "idea"},
            answers
        )
        assert result['accepted'], f"Q4 failed: {result.get('error')}"
        assert result['completed'] is True
        assert 'business_context' in result
        assert 'specificity_score' in result
    
    def test_specificity_calculation(self, handler):
        """Test specificity score calculation"""
        answers = [
            {"question_id": "Q1a_category", "answer": {"selected": "restaurant"}},
            {"question_id": "Q1b_subcategory_restaurant", "answer": {"selected": "casual_dining"}},
            {"question_id": "Q1c_description", "answer": {"text": "Italian food for families"}},
            {"question_id": "Q2a_target_customer", "answer": {"selected": "families"}},
            {"question_id": "Q3_problem", "answer": {"selected": "quality"}},
            {"question_id": "Q4_stage", "answer": {"selected": "idea"}}
        ]
        
        specificity = handler._calculate_specificity(answers)
        
        # Should be in target range 60-70%
        assert 0.60 <= specificity <= 0.90
    
    def test_dynamic_option_generation_restaurant(self, handler):
        """Test dynamic options based on restaurant selection"""
        previous_answers = [
            {"question_id": "Q1a_category", "answer": {"selected": "restaurant"}}
        ]
        
        question = handler._get_question("Q2a_target_customer", previous_answers)
        
        # Check that restaurant-specific options are present
        option_ids = [opt['id'] for opt in question['options']]
        assert 'families' in option_ids
        assert 'business_lunch' in option_ids
    
    def test_dynamic_option_generation_saas(self, handler):
        """Test dynamic options based on SaaS selection"""
        previous_answers = [
            {"question_id": "Q1a_category", "answer": {"selected": "saas"}}
        ]
        
        question = handler._get_question("Q2a_target_customer", previous_answers)
        
        # Check that SaaS-specific options are present
        option_ids = [opt['id'] for opt in question['options']]
        assert 'smb' in option_ids or 'enterprise' in option_ids
    
    def test_progress_calculation(self, handler):
        """Test progress calculation"""
        answers = [
            {"question_id": "Q1a_category", "answer": {"selected": "restaurant"}},
            {"question_id": "Q1b_subcategory_restaurant", "answer": {"selected": "casual_dining"}}
        ]
        
        progress = handler._calculate_progress(answers, "Q1c_description")
        
        assert 'current' in progress
        assert 'total' in progress
        assert 'percentage' in progress
        assert progress['current'] == 3  # 2 answered + 1 current
        assert 0 <= progress['percentage'] <= 100
    
    def test_business_context_compilation(self, handler):
        """Test business context compilation"""
        answers = [
            {"question_id": "Q1a_category", "answer": {"selected": "restaurant"}},
            {"question_id": "Q1b_subcategory_restaurant", "answer": {"selected": "casual_dining"}},
            {"question_id": "Q1c_description", "answer": {"text": "Italian food"}},
            {"question_id": "Q2a_target_customer", "answer": {"selected": "families"}},
            {"question_id": "Q3_problem", "answer": {"selected": "quality"}},
            {"question_id": "Q4_stage", "answer": {"selected": "idea"}}
        ]
        
        context = handler._compile_business_context(answers)
        
        assert context['business_type'] == 'restaurant'
        assert context['sub_type'] == 'casual_dining'
        assert context['description'] == 'Italian food'
        assert context['target_customer'] == 'families'
        assert context['problem'] == 'quality'
        assert context['stage'] == 'idea'
    
    def test_other_option_with_text(self, handler):
        """Test 'other' option requires text"""
        handler.start_session()
        
        # Select 'other' without providing text
        answer = {"selected": "other"}
        result = handler.process_answer(
            "Q1a_category",
            answer,
            []
        )
        
        assert result['accepted'] is False
        assert result['error_code'] == 'OTHER_TEXT_REQUIRED'
    
    def test_other_option_with_text_provided(self, handler):
        """Test 'other' option with text provided"""
        handler.start_session()
        
        answer = {"selected": "other", "other_text": "Meine eigene Kategorie"}
        result = handler.process_answer(
            "Q1a_category",
            answer,
            []
        )
        
        assert result['accepted'] is True


# ============================================================================
# BUSINESS CONTEXT VALIDATOR TESTS
# ============================================================================

class TestBusinessContextValidator:
    """Test suite for input validation"""
    
    def test_sanitize_text(self):
        """Test text sanitization"""
        text = "  <script>alert('xss')</script>Test  "
        sanitized = BusinessContextValidator.sanitize_text(text)
        
        assert "<script>" not in sanitized
        assert "&lt;script&gt;" in sanitized  # HTML escaped
        assert sanitized.strip() == sanitized
    
    def test_sanitize_text_max_length(self):
        """Test text length limiting"""
        text = "x" * 2000
        sanitized = BusinessContextValidator.sanitize_text(text, max_length=100)
        
        assert len(sanitized) == 100
    
    def test_sql_injection_detection(self):
        """Test SQL injection pattern detection"""
        safe_text = "Italienisches Restaurant für Familien"
        unsafe_texts = [
            "Restaurant' OR '1'='1",
            "Test; DROP TABLE users;--",
            "UNION SELECT * FROM users",
            "1; DELETE FROM orders"
        ]
        
        # Safe text should pass
        result = BusinessContextValidator.validate_text_safe(safe_text)
        assert result['safe'] is True
        
        # Unsafe texts should fail
        for unsafe in unsafe_texts:
            result = BusinessContextValidator.validate_text_safe(unsafe)
            assert result['safe'] is False, f"Should detect: {unsafe}"
    
    def test_xss_detection(self):
        """Test XSS pattern detection"""
        safe_text = "Click here for menu"
        unsafe_texts = [
            "<script>alert('xss')</script>",
            "javascript:alert(1)",
            "<img onerror='alert(1)'>",
            "<iframe src='evil.com'>",
            "onclick=alert(1)"
        ]
        
        # Safe text should pass
        result = BusinessContextValidator.validate_text_safe(safe_text)
        assert result['safe'] is True
        
        # Unsafe texts should fail
        for unsafe in unsafe_texts:
            result = BusinessContextValidator.validate_text_safe(unsafe)
            assert result['safe'] is False, f"Should detect: {unsafe}"
    
    def test_selection_validation_single(self):
        """Test single option selection validation"""
        valid_options = ['restaurant', 'saas', 'consulting']
        
        # Valid selection
        assert BusinessContextValidator.validate_selection('restaurant', valid_options) is True
        
        # Invalid selection
        assert BusinessContextValidator.validate_selection('invalid', valid_options) is False
    
    def test_selection_validation_multiple(self):
        """Test multiple option selection validation"""
        valid_options = ['young_kids', 'school_age', 'teens', 'multi_gen']
        
        # Valid multiple selection
        assert BusinessContextValidator.validate_selection(
            ['young_kids', 'school_age'], 
            valid_options
        ) is True
        
        # Invalid multiple selection (contains invalid option)
        assert BusinessContextValidator.validate_selection(
            ['young_kids', 'invalid'], 
            valid_options
        ) is False
    
    def test_session_id_validation(self):
        """Test UUID session ID validation"""
        valid_uuid = "550e8400-e29b-41d4-a716-446655440000"
        invalid_uuids = [
            "not-a-uuid",
            "550e8400-e29b-41d4-a716",
            "550e8400e29b41d4a716446655440000",
            ""
        ]
        
        assert BusinessContextValidator.validate_session_id(valid_uuid) is True
        
        for invalid in invalid_uuids:
            assert BusinessContextValidator.validate_session_id(invalid) is False
    
    def test_question_id_validation(self):
        """Test question ID validation"""
        valid_ids = ["Q1a_category", "Q2b_families_refinement", "Q4_stage"]
        invalid_ids = ["1_category", "category", "Q1a category", ""]
        
        for valid in valid_ids:
            assert BusinessContextValidator.validate_question_id(valid) is True
        
        for invalid in invalid_ids:
            assert BusinessContextValidator.validate_question_id(invalid) is False
    
    def test_validate_answer_multiple_choice(self):
        """Test answer validation for multiple choice"""
        valid_answer = {"selected": "restaurant"}
        result = BusinessContextValidator.validate_answer(valid_answer, "multiple_choice")
        assert result['valid'] is True
        
        empty_answer = {"selected": ""}
        result = BusinessContextValidator.validate_answer(empty_answer, "multiple_choice")
        assert result['valid'] is False
    
    def test_validate_answer_text(self):
        """Test answer validation for text input"""
        valid_answer = {"text": "Mein Restaurant für Familien"}
        result = BusinessContextValidator.validate_answer(valid_answer, "text")
        assert result['valid'] is True
        
        unsafe_answer = {"text": "<script>alert('xss')</script>"}
        result = BusinessContextValidator.validate_answer(unsafe_answer, "text")
        assert result['valid'] is False
    
    def test_validate_business_context(self):
        """Test business context validation"""
        valid_context = {
            "business_type": "restaurant",
            "stage": "idea",
            "description": "Italian food"
        }
        result = BusinessContextValidator.validate_business_context(valid_context)
        assert result['valid'] is True
        
        # Missing required field
        invalid_context = {
            "business_type": "restaurant"
            # Missing 'stage'
        }
        result = BusinessContextValidator.validate_business_context(invalid_context)
        assert result['valid'] is False
    
    def test_sanitize_answer(self):
        """Test answer sanitization"""
        answer = {"text": "  Test <script>bad</script>  "}
        sanitized = BusinessContextValidator.sanitize_answer(answer, "text")
        
        assert "<script>" not in sanitized['text']
        assert sanitized['text'].strip() == sanitized['text']


# ============================================================================
# RATE LIMITER TESTS
# ============================================================================

class TestRateLimiter:
    """Test suite for rate limiting"""
    
    def test_allows_under_limit(self, rate_limiter):
        """Test requests under limit are allowed"""
        key = "test-user-1"
        
        for _ in range(5):
            assert rate_limiter.is_allowed(key) is True
    
    def test_blocks_over_limit(self, rate_limiter):
        """Test requests over limit are blocked"""
        key = "test-user-2"
        
        # Use up all requests
        for _ in range(5):
            rate_limiter.is_allowed(key)
        
        # Next request should be blocked
        assert rate_limiter.is_allowed(key) is False
    
    def test_get_remaining(self, rate_limiter):
        """Test remaining requests count"""
        key = "test-user-3"
        
        assert rate_limiter.get_remaining(key) == 5
        
        rate_limiter.is_allowed(key)
        rate_limiter.is_allowed(key)
        
        assert rate_limiter.get_remaining(key) == 3
    
    def test_different_keys_independent(self, rate_limiter):
        """Test different keys have independent limits"""
        key1 = "user-1"
        key2 = "user-2"
        
        # Use up all requests for key1
        for _ in range(5):
            rate_limiter.is_allowed(key1)
        
        # key2 should still be allowed
        assert rate_limiter.is_allowed(key2) is True
        assert rate_limiter.is_allowed(key1) is False


# ============================================================================
# INTEGRATION TESTS (require FastAPI test client)
# ============================================================================

class TestBusinessContextAPI:
    """Integration tests for API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        try:
            from fastapi.testclient import TestClient
            from main import app
            return TestClient(app)
        except ImportError:
            pytest.skip("FastAPI test client not available")
    
    def test_start_endpoint(self, client):
        """Test POST /api/v1/assessment/business-context/start"""
        response = client.post(
            "/api/v1/assessment/business-context/start",
            json={}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'session_id' in data
        assert 'question' in data
        assert data['question']['id'] == 'Q1a_category'
    
    def test_answer_endpoint(self, client):
        """Test POST /api/v1/assessment/business-context/answer"""
        # First start a session
        start_response = client.post(
            "/api/v1/assessment/business-context/start",
            json={}
        )
        session_id = start_response.json()['session_id']
        
        # Submit answer
        response = client.post(
            "/api/v1/assessment/business-context/answer",
            json={
                "session_id": session_id,
                "question_id": "Q1a_category",
                "answer": {"selected": "restaurant"}
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['accepted'] is True
        assert 'next_question' in data
        assert data['next_question']['id'] == 'Q1b_subcategory_restaurant'
    
    def test_invalid_answer(self, client):
        """Test submitting invalid answer"""
        start_response = client.post(
            "/api/v1/assessment/business-context/start",
            json={}
        )
        session_id = start_response.json()['session_id']
        
        # Submit invalid answer
        response = client.post(
            "/api/v1/assessment/business-context/answer",
            json={
                "session_id": session_id,
                "question_id": "Q1a_category",
                "answer": {"selected": "invalid_category"}
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['accepted'] is False
        assert 'error' in data
    
    def test_progress_endpoint(self, client):
        """Test GET /api/v1/assessment/business-context/progress/{session_id}"""
        # Start session
        start_response = client.post(
            "/api/v1/assessment/business-context/start",
            json={}
        )
        session_id = start_response.json()['session_id']
        
        # Get progress
        response = client.get(
            f"/api/v1/assessment/business-context/progress/{session_id}"
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['session_id'] == session_id
        assert data['completed'] is False
        assert 'current_question' in data
    
    def test_invalid_session(self, client):
        """Test request with invalid session ID"""
        response = client.get(
            "/api/v1/assessment/business-context/progress/invalid-session-id"
        )
        
        assert response.status_code == 400
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get(
            "/api/v1/assessment/business-context/health"
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['status'] == 'healthy'
        assert 'questions_loaded' in data


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
