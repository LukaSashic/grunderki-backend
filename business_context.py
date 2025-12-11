"""
Business Context Capture System
Handles guided question flow for capturing business information

This is Phase 1 of the GründerAI assessment where users provide
basic business information through 4-5 guided questions.

Author: Opus (Implementation Layer)
Date: 2025-12-11
"""

from typing import Dict, List, Optional, Any
from enum import Enum
import json
from pathlib import Path
from datetime import datetime, timezone
import re
import logging

logger = logging.getLogger(__name__)


class QuestionType(Enum):
    """Supported question types"""
    MULTIPLE_CHOICE = "multiple_choice"
    MULTIPLE_CHOICE_MULTIPLE = "multiple_choice_multiple"
    TEXT = "text"


class BusinessContextHandler:
    """
    Manages the business context capture phase of the assessment.
    
    Responsibilities:
    - Load and serve questions dynamically
    - Validate user responses
    - Track progress through question flow
    - Generate next questions based on previous answers
    - Calculate specificity score
    - Compile final business context
    """
    
    def __init__(self, question_bank_path: Optional[str] = None):
        """
        Initialize with question bank.
        
        Args:
            question_bank_path: Path to question bank JSON file
        """
        if question_bank_path is None:
            question_bank_path = Path(__file__).parent / "question_bank_business.json"
        
        with open(question_bank_path, 'r', encoding='utf-8') as f:
            self.question_bank = json.load(f)
        
        self.questions = self.question_bank['questions']
        self.dynamic_generators = self.question_bank.get('dynamic_option_generators', {})
        self.flow_config = self.question_bank.get('question_flow', {})
        
        logger.info(f"BusinessContextHandler initialized with {len(self.questions)} questions")
    
    def start_session(self) -> Dict[str, Any]:
        """
        Start a new business context session.
        
        Returns:
            First question with metadata
        """
        first_question_id = self.flow_config.get('start', 'Q1a_category')
        question = self._get_question(first_question_id)
        
        return {
            "question": self._format_question_for_api(question),
            "progress": self._calculate_progress([], first_question_id),
            "phase": "business_context"
        }
    
    def process_answer(
        self, 
        question_id: str, 
        answer: Dict[str, Any],
        previous_answers: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Process user's answer and determine next question.
        
        Args:
            question_id: ID of the question being answered
            answer: User's answer data
            previous_answers: List of all previous answers
            
        Returns:
            Result with validation status and next question
        """
        # Validate answer
        question = self._get_question(question_id, previous_answers)
        validation_result = self._validate_answer(question, answer)
        
        if not validation_result['valid']:
            return {
                "accepted": False,
                "error": validation_result['error'],
                "error_code": validation_result['code']
            }
        
        # Record answer
        answer_record = {
            "question_id": question_id,
            "answer": answer,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        # Create new list to avoid mutating input
        updated_answers = previous_answers + [answer_record]
        
        # Determine next question
        next_question_id = self._get_next_question_id(question, answer, updated_answers)
        
        if next_question_id is None:
            # Assessment complete
            business_context = self._compile_business_context(updated_answers)
            specificity = self._calculate_specificity(updated_answers)
            
            return {
                "accepted": True,
                "completed": True,
                "business_context": business_context,
                "specificity_score": specificity,
                "ready_for_personality": specificity >= 0.50,
                "answers": updated_answers
            }
        
        # Get next question
        next_question = self._get_question(next_question_id, updated_answers)
        
        return {
            "accepted": True,
            "completed": False,
            "next_question": self._format_question_for_api(next_question),
            "progress": self._calculate_progress(updated_answers, next_question_id),
            "answers": updated_answers
        }
    
    def _get_question(
        self, 
        question_id: str, 
        previous_answers: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Get question by ID, applying dynamic generation if needed.
        
        Args:
            question_id: Question identifier
            previous_answers: Previous answers for context
            
        Returns:
            Question data
            
        Raises:
            ValueError: If question not found
        """
        if question_id not in self.questions:
            raise ValueError(f"Question {question_id} not found")
        
        question = self.questions[question_id].copy()
        
        # Apply dynamic option generation if specified
        if question.get('dynamic_options') and previous_answers:
            question['options'] = self._generate_dynamic_options(
                question, 
                previous_answers
            )
        
        return question
    
    def _generate_dynamic_options(
        self, 
        question: Dict[str, Any],
        previous_answers: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Generate options dynamically based on business type.
        
        Args:
            question: Question configuration
            previous_answers: Context from previous answers
            
        Returns:
            List of dynamically generated options
        """
        # Find business type from previous answers
        business_type = None
        for answer in previous_answers:
            if answer['question_id'] == 'Q1a_category':
                business_type = answer['answer'].get('selected')
                break
        
        if not business_type or business_type not in self.dynamic_generators:
            return question.get('default_options', [])
        
        # Get appropriate options for this business type
        generator_key = question.get('options_generator', '')
        business_config = self.dynamic_generators[business_type]
        
        if 'customer' in generator_key:
            return business_config.get('customer_options', question.get('default_options', []))
        elif 'problem' in generator_key:
            return business_config.get('problem_options', question.get('default_options', []))
        
        return question.get('default_options', [])
    
    def _validate_answer(
        self, 
        question: Dict[str, Any], 
        answer: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate user's answer against question requirements.
        
        Args:
            question: Question configuration
            answer: User's answer
            
        Returns:
            Validation result with status and error if invalid
        """
        q_type = question['type']
        validation = question.get('validation', {})
        
        # Multiple choice validation
        if q_type in ['multiple_choice', 'multiple_choice_multiple']:
            selected = answer.get('selected')
            
            if not selected:
                return {
                    'valid': False,
                    'error': 'Bitte wähle eine Option',
                    'code': 'NO_SELECTION'
                }
            
            # Get valid options (handle both direct options and dynamic)
            options = question.get('options', question.get('default_options', []))
            valid_options = [opt['id'] for opt in options]
            
            if q_type == 'multiple_choice':
                if selected not in valid_options:
                    return {
                        'valid': False,
                        'error': 'Ungültige Option gewählt',
                        'code': 'INVALID_OPTION'
                    }
            else:  # multiple_choice_multiple
                if not isinstance(selected, list):
                    selected = [selected]
                
                for sel in selected:
                    if sel not in valid_options:
                        return {
                            'valid': False,
                            'error': f'Ungültige Option: {sel}',
                            'code': 'INVALID_OPTION'
                        }
                
                # Check selection count
                min_sel = validation.get('min_selections', 1)
                max_sel = validation.get('max_selections', len(valid_options))
                
                if len(selected) < min_sel:
                    return {
                        'valid': False,
                        'error': f'Bitte wähle mindestens {min_sel} Option(en)',
                        'code': 'TOO_FEW_SELECTIONS'
                    }
                
                if len(selected) > max_sel:
                    return {
                        'valid': False,
                        'error': f'Maximal {max_sel} Optionen erlaubt',
                        'code': 'TOO_MANY_SELECTIONS'
                    }
            
            # Check if "other" requires text
            for opt in options:
                if opt['id'] == selected and opt.get('requires_text'):
                    other_text = answer.get('other_text', '').strip()
                    if not other_text:
                        return {
                            'valid': False,
                            'error': 'Bitte beschreibe deine Auswahl',
                            'code': 'OTHER_TEXT_REQUIRED'
                        }
        
        # Text validation
        elif q_type == 'text':
            text = answer.get('text', '').strip()
            
            if not text:
                return {
                    'valid': False,
                    'error': 'Bitte gib eine Antwort ein',
                    'code': 'TEXT_REQUIRED'
                }
            
            min_length = question.get('min_length', validation.get('min_length', 0))
            max_length = question.get('max_length', validation.get('max_length', 1000))
            
            if len(text) < min_length:
                return {
                    'valid': False,
                    'error': f'Mindestens {min_length} Zeichen erforderlich',
                    'code': 'TEXT_TOO_SHORT'
                }
            
            if len(text) > max_length:
                return {
                    'valid': False,
                    'error': f'Maximal {max_length} Zeichen erlaubt',
                    'code': 'TEXT_TOO_LONG'
                }
            
            # Regex validation if specified
            if 'regex' in validation:
                if not re.match(validation['regex'], text):
                    return {
                        'valid': False,
                        'error': 'Ungültige Zeichen enthalten',
                        'code': 'INVALID_FORMAT'
                    }
        
        return {'valid': True}
    
    def _get_next_question_id(
        self, 
        current_question: Dict[str, Any],
        answer: Dict[str, Any],
        previous_answers: List[Dict[str, Any]]
    ) -> Optional[str]:
        """
        Determine the next question based on current answer.
        
        Args:
            current_question: Current question config
            answer: User's answer
            previous_answers: All previous answers
            
        Returns:
            Next question ID or None if complete
        """
        # Check if this is the final question
        if current_question.get('is_final'):
            return None
        
        # Check if answer determines next question
        selected = answer.get('selected')
        
        if current_question['type'] == 'multiple_choice':
            # Find the selected option
            options = current_question.get('options', current_question.get('default_options', []))
            for option in options:
                if option['id'] == selected:
                    # Check if this option has a specific next question
                    if 'next_question' in option:
                        return option['next_question']
                    
                    # Check if requires followup
                    if option.get('requires_followup'):
                        followup_q = option.get('followup_question')
                        if followup_q:
                            return followup_q
        
        # Default next question from question config
        return current_question.get('next_question')
    
    def _compile_business_context(
        self, 
        answers: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Compile final business context from all answers.
        
        Args:
            answers: List of all answers
            
        Returns:
            Compiled business context dictionary
        """
        context = {
            "business_type": None,
            "sub_type": None,
            "target_customer": None,
            "customer_details": None,
            "problem": None,
            "stage": None,
            "description": None,
            "raw_answers": {}
        }
        
        for answer_record in answers:
            q_id = answer_record['question_id']
            answer = answer_record['answer']
            
            # Map answers to context fields
            if q_id == 'Q1a_category':
                context['business_type'] = answer.get('selected')
                if answer.get('other_text'):
                    context['business_type_custom'] = answer.get('other_text')
            
            elif q_id.startswith('Q1b_subcategory'):
                context['sub_type'] = answer.get('selected')
                if answer.get('other_text'):
                    context['sub_type_custom'] = answer.get('other_text')
            
            elif q_id == 'Q1b2_cuisine':
                context['cuisine'] = answer.get('selected')
                if answer.get('other_text'):
                    context['cuisine_custom'] = answer.get('other_text')
            
            elif q_id == 'Q1c_description':
                context['description'] = answer.get('text')
            
            elif q_id == 'Q2a_target_customer':
                context['target_customer'] = answer.get('selected')
            
            elif q_id == 'Q2b_families_refinement':
                selected = answer.get('selected')
                if isinstance(selected, list):
                    context['customer_details'] = selected
                else:
                    context['customer_details'] = [selected] if selected else []
            
            elif q_id == 'Q3_problem':
                context['problem'] = answer.get('selected')
                if answer.get('other_text'):
                    context['problem_custom'] = answer.get('other_text')
            
            elif q_id == 'Q4_stage':
                context['stage'] = answer.get('selected')
            
            # Store raw answer for reference
            context['raw_answers'][q_id] = answer
        
        return context
    
    def _calculate_specificity(self, answers: List[Dict[str, Any]]) -> float:
        """
        Calculate how specific/detailed the business context is.
        
        Target: 60-70% specificity
        
        Args:
            answers: List of all answers
            
        Returns:
            Specificity score (0.0 to 1.0)
        """
        max_score = 100
        current_score = 0
        
        # Base points for required fields (50 points)
        required_fields = ['Q1a_category', 'Q2a_target_customer', 'Q3_problem', 'Q4_stage']
        for q_id in required_fields:
            if any(a['question_id'] == q_id for a in answers):
                current_score += 12.5  # 50 / 4 fields
        
        # Bonus points for refinements (50 points)
        bonus_questions = {
            'Q1b_subcategory': 15,  # Sub-category specified
            'Q1b2_cuisine': 5,       # Cuisine specified
            'Q1c_description': 20,   # Description provided
            'Q2b_families': 10       # Customer refined
        }
        
        for q_prefix, points in bonus_questions.items():
            # Check if any answer starts with this ID (handles variants)
            if any(a['question_id'].startswith(q_prefix) for a in answers):
                current_score += points
        
        return min(current_score / max_score, 1.0)
    
    def _calculate_progress(
        self, 
        answers: List[Dict[str, Any]], 
        current_question_id: str
    ) -> Dict[str, Any]:
        """
        Calculate progress through the question flow.
        
        Args:
            answers: Answers so far
            current_question_id: Current question
            
        Returns:
            Progress information
        """
        # Estimate total questions (can vary based on path)
        estimated_total = self.flow_config.get('estimated_questions', 5)
        
        # Add bonus questions if we know the path
        for answer in answers:
            if answer['question_id'] == 'Q1a_category':
                # Some categories may have additional subcategory questions
                if answer['answer'].get('selected') in ['restaurant', 'consulting', 'saas']:
                    estimated_total = max(estimated_total, 6)
            
            if answer['question_id'] == 'Q2a_target_customer':
                if answer['answer'].get('selected') == 'families':
                    estimated_total = max(estimated_total, 6)
        
        current = len(answers) + 1  # +1 for current question
        percentage = min(int((current / estimated_total) * 100), 95)  # Never 100 until done
        
        return {
            "current": current,
            "total": estimated_total,
            "percentage": percentage
        }
    
    def _format_question_for_api(self, question: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format question for API response.
        
        Args:
            question: Question data
            
        Returns:
            API-formatted question
        """
        options = question.get('options', question.get('default_options', []))
        
        return {
            "id": question['id'],
            "type": question['type'],
            "text": question['text'],
            "help_text": question.get('help_text'),
            "placeholder": question.get('placeholder'),
            "options": options,
            "required": question.get('required', True),
            "validation": question.get('validation', {}),
            "allow_other": any(
                opt.get('id') == 'other' or opt.get('requires_text')
                for opt in options
            ),
            "min_length": question.get('min_length'),
            "max_length": question.get('max_length')
        }
    
    def get_question_by_id(self, question_id: str, previous_answers: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Public method to get a question by ID.
        
        Args:
            question_id: Question identifier
            previous_answers: Previous answers for context
            
        Returns:
            Formatted question data
        """
        question = self._get_question(question_id, previous_answers)
        return self._format_question_for_api(question)
