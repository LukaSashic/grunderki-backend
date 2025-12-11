"""
Input Validation and Sanitization for Business Context

Provides security-focused validation including:
- SQL injection prevention
- XSS protection
- Input sanitization
- Rate limiting support

Author: Opus (Implementation Layer)
Date: 2025-12-11
"""

from typing import Dict, Any, List, Optional, Union
import re
from html import escape
import logging

logger = logging.getLogger(__name__)


class BusinessContextValidator:
    """
    Handles validation and sanitization of user inputs.
    
    Security features:
    - SQL injection pattern detection
    - XSS pattern detection  
    - HTML escaping
    - Length enforcement
    - Character whitelist validation
    """
    
    # Allowed characters in text fields (German-friendly)
    TEXT_PATTERN = re.compile(r'^[a-zA-ZäöüÄÖÜß0-9\s\-,\.!?()\'\"]+$')
    
    # More permissive pattern for business descriptions
    DESCRIPTION_PATTERN = re.compile(r'^[a-zA-ZäöüÄÖÜß0-9\s\-,\.!?()\'\"&%€@#+:/]+$')
    
    # SQL injection patterns to block
    SQL_INJECTION_PATTERNS = [
        r'(\bUNION\b.*\bSELECT\b)',
        r'(\bSELECT\b.*\bFROM\b)',
        r'(\bDROP\b.*\bTABLE\b)',
        r'(\bDELETE\b.*\bFROM\b)',
        r'(\bINSERT\b.*\bINTO\b)',
        r'(\bUPDATE\b.*\bSET\b)',
        r'(--)',
        r'(;.*--)',
        r'(/\*.*\*/)',
        r'(\bOR\b\s+[\'\"]?\s*=\s*[\'\"]?)',
        r'(\bAND\b\s+[\'\"]?\s*=\s*[\'\"]?)',
        r'(\'\s*OR\s*\')',
        r'(\'\s*AND\s*\')',
        r'(\bEXEC\b|\bEXECUTE\b)',
        r'(\bxp_)',
    ]
    
    # XSS patterns to block
    XSS_PATTERNS = [
        r'<script',
        r'</script',
        r'javascript:',
        r'onerror\s*=',
        r'onload\s*=',
        r'onclick\s*=',
        r'onmouseover\s*=',
        r'onfocus\s*=',
        r'onblur\s*=',
        r'<iframe',
        r'<object',
        r'<embed',
        r'<form',
        r'<input',
        r'document\.',
        r'window\.',
        r'eval\s*\(',
        r'alert\s*\(',
        r'String\.fromCharCode',
        r'&#x',  # Hex entities
        r'&#\d+;',  # Decimal entities
    ]
    
    @classmethod
    def sanitize_text(cls, text: str, max_length: int = 1000) -> str:
        """
        Sanitize text input.
        
        Args:
            text: Raw text input
            max_length: Maximum allowed length
            
        Returns:
            Sanitized text
        """
        if not text:
            return ""
        
        # Strip whitespace
        text = text.strip()
        
        # Limit length
        text = text[:max_length]
        
        # Escape HTML entities
        text = escape(text)
        
        # Remove null bytes
        text = text.replace('\x00', '')
        
        # Normalize whitespace (replace multiple spaces with single)
        text = re.sub(r'\s+', ' ', text)
        
        return text
    
    @classmethod
    def validate_text_safe(cls, text: str) -> Dict[str, Any]:
        """
        Check if text is safe (no injection attempts).
        
        Args:
            text: Text to validate
            
        Returns:
            Dict with 'safe' boolean and optional 'reason'
        """
        if not text:
            return {'safe': True}
        
        text_lower = text.lower()
        
        # Check for SQL injection
        for pattern in cls.SQL_INJECTION_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                logger.warning(f"SQL injection pattern detected: {pattern}")
                return {
                    'safe': False,
                    'reason': 'Potentially unsafe characters detected',
                    'pattern_type': 'sql_injection'
                }
        
        # Check for XSS
        for pattern in cls.XSS_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                logger.warning(f"XSS pattern detected: {pattern}")
                return {
                    'safe': False,
                    'reason': 'Potentially unsafe content detected',
                    'pattern_type': 'xss'
                }
        
        return {'safe': True}
    
    @classmethod
    def validate_selection(
        cls, 
        selected: Union[str, List[str]], 
        valid_options: List[str]
    ) -> bool:
        """
        Validate that selection is in valid options.
        
        Args:
            selected: Selected option(s)
            valid_options: List of valid option IDs
            
        Returns:
            True if valid, False otherwise
        """
        if isinstance(selected, list):
            return all(sel in valid_options for sel in selected)
        else:
            return selected in valid_options
    
    @classmethod
    def validate_session_id(cls, session_id: str) -> bool:
        """
        Validate session ID format (UUID).
        
        Args:
            session_id: Session ID to validate
            
        Returns:
            True if valid UUID format
        """
        uuid_pattern = re.compile(
            r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
            re.IGNORECASE
        )
        return bool(uuid_pattern.match(session_id))
    
    @classmethod
    def validate_question_id(cls, question_id: str) -> bool:
        """
        Validate question ID format.
        
        Args:
            question_id: Question ID to validate
            
        Returns:
            True if valid format
        """
        # Question IDs should be alphanumeric with underscores
        pattern = re.compile(r'^Q[0-9a-zA-Z_]+$')
        return bool(pattern.match(question_id))
    
    @classmethod
    def validate_answer(cls, answer: Dict[str, Any], question_type: str) -> Dict[str, Any]:
        """
        Comprehensive answer validation.
        
        Args:
            answer: Answer data from user
            question_type: Type of question (multiple_choice, text, etc.)
            
        Returns:
            Validation result with status and details
        """
        if not answer:
            return {
                'valid': False,
                'error': 'Answer cannot be empty',
                'code': 'EMPTY_ANSWER'
            }
        
        if question_type in ['multiple_choice', 'multiple_choice_multiple']:
            # Validate selection
            selected = answer.get('selected')
            if not selected:
                return {
                    'valid': False,
                    'error': 'Selection required',
                    'code': 'NO_SELECTION'
                }
            
            # Check for injection in selection value
            if isinstance(selected, str):
                safety_check = cls.validate_text_safe(selected)
                if not safety_check['safe']:
                    return {
                        'valid': False,
                        'error': safety_check['reason'],
                        'code': 'UNSAFE_INPUT'
                    }
            elif isinstance(selected, list):
                for sel in selected:
                    safety_check = cls.validate_text_safe(str(sel))
                    if not safety_check['safe']:
                        return {
                            'valid': False,
                            'error': safety_check['reason'],
                            'code': 'UNSAFE_INPUT'
                        }
            
            # Check other_text if present
            other_text = answer.get('other_text')
            if other_text:
                safety_check = cls.validate_text_safe(other_text)
                if not safety_check['safe']:
                    return {
                        'valid': False,
                        'error': safety_check['reason'],
                        'code': 'UNSAFE_INPUT'
                    }
        
        elif question_type == 'text':
            text = answer.get('text', '')
            
            # Check for injection patterns
            safety_check = cls.validate_text_safe(text)
            if not safety_check['safe']:
                return {
                    'valid': False,
                    'error': safety_check['reason'],
                    'code': 'UNSAFE_INPUT'
                }
        
        return {'valid': True}
    
    @classmethod
    def sanitize_answer(cls, answer: Dict[str, Any], question_type: str) -> Dict[str, Any]:
        """
        Sanitize answer data.
        
        Args:
            answer: Raw answer data
            question_type: Type of question
            
        Returns:
            Sanitized answer data
        """
        sanitized = answer.copy()
        
        if question_type == 'text':
            if 'text' in sanitized:
                sanitized['text'] = cls.sanitize_text(sanitized['text'])
        
        elif question_type in ['multiple_choice', 'multiple_choice_multiple']:
            if 'other_text' in sanitized and sanitized['other_text']:
                sanitized['other_text'] = cls.sanitize_text(sanitized['other_text'])
        
        return sanitized
    
    @classmethod
    def validate_business_context(cls, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate compiled business context before storage.
        
        Args:
            context: Compiled business context
            
        Returns:
            Validation result
        """
        required_fields = ['business_type', 'stage']
        
        for field in required_fields:
            if not context.get(field):
                return {
                    'valid': False,
                    'error': f'Missing required field: {field}',
                    'code': 'INCOMPLETE_CONTEXT'
                }
        
        # Check description if present
        description = context.get('description')
        if description:
            safety_check = cls.validate_text_safe(description)
            if not safety_check['safe']:
                return {
                    'valid': False,
                    'error': 'Description contains unsafe content',
                    'code': 'UNSAFE_CONTENT'
                }
        
        # Check all custom text fields
        custom_fields = ['business_type_custom', 'sub_type_custom', 'problem_custom', 'cuisine_custom']
        for field in custom_fields:
            if context.get(field):
                safety_check = cls.validate_text_safe(context[field])
                if not safety_check['safe']:
                    return {
                        'valid': False,
                        'error': f'{field} contains unsafe content',
                        'code': 'UNSAFE_CONTENT'
                    }
        
        return {'valid': True}


class RateLimiter:
    """
    Simple in-memory rate limiter.
    For production, use Redis-based rate limiting.
    """
    
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: Dict[str, List[float]] = {}
    
    def is_allowed(self, key: str) -> bool:
        """
        Check if request is allowed under rate limit.
        
        Args:
            key: Rate limit key (e.g., user IP or session ID)
            
        Returns:
            True if request is allowed
        """
        import time
        current_time = time.time()
        
        if key not in self._requests:
            self._requests[key] = []
        
        # Clean old requests
        self._requests[key] = [
            t for t in self._requests[key]
            if current_time - t < self.window_seconds
        ]
        
        # Check limit
        if len(self._requests[key]) >= self.max_requests:
            return False
        
        # Record request
        self._requests[key].append(current_time)
        return True
    
    def get_remaining(self, key: str) -> int:
        """
        Get remaining requests for key.
        
        Args:
            key: Rate limit key
            
        Returns:
            Number of remaining requests
        """
        import time
        current_time = time.time()
        
        if key not in self._requests:
            return self.max_requests
        
        # Clean old requests
        valid_requests = [
            t for t in self._requests[key]
            if current_time - t < self.window_seconds
        ]
        
        return max(0, self.max_requests - len(valid_requests))


# Global rate limiter instance
business_context_rate_limiter = RateLimiter(max_requests=30, window_seconds=60)
