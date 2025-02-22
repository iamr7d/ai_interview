import streamlit as st
from typing import Optional, Any, Dict
from functools import wraps

class InterviewError(Exception):
    """Base exception class for interview application"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

class ConfigurationError(InterviewError):
    """Raised when there's a configuration-related error"""
    pass

class LLMError(InterviewError):
    """Raised when there's an error with the LLM service"""
    pass

class AudioError(InterviewError):
    """Raised when there's an error with audio processing"""
    pass

def handle_error(error_type: str = "general"):
    """Decorator for handling errors in a consistent way"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except InterviewError as e:
                st.error(f"{error_type.title()} Error: {e.message}")
                if e.details:
                    st.error(f"Details: {e.details}")
            except Exception as e:
                st.error(f"Unexpected {error_type} error: {str(e)}")
            return None
        return wrapper
    return decorator

def log_error(error: Exception, context: Optional[Dict[str, Any]] = None):
    """Log error with context for debugging"""
    error_data = {
        "type": type(error).__name__,
        "message": str(error),
        "context": context or {}
    }
    # In a production environment, you would want to log this to a proper logging system
    st.error(f"Error occurred: {error_data}")
    return error_data