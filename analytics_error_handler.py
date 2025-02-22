import streamlit as st
from typing import Optional, Callable
from functools import wraps

class AnalyticsErrorHandler:
    def __init__(self):
        self.tracking_enabled = True
        self.error_count = 0
        self.max_retries = 3
    
    def handle_tracking_error(self, error: Exception) -> None:
        """Handle tracking-related errors"""
        if 'ERR_BLOCKED_BY_CLIENT' in str(error):
            self.tracking_enabled = False
            st.debug("Analytics tracking has been disabled due to client blocking")
        else:
            self.error_count += 1
            if self.error_count >= self.max_retries:
                self.tracking_enabled = False
                st.debug(f"Analytics disabled after {self.max_retries} failed attempts")
    
    def with_error_handling(self, func: Callable) -> Callable:
        """Decorator for handling analytics errors"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not self.tracking_enabled:
                return None
            
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.handle_tracking_error(e)
                return None
        return wrapper

# Global error handler instance
error_handler = AnalyticsErrorHandler()

def safe_track(func: Callable) -> Callable:
    """Decorator for safely tracking analytics"""
    return error_handler.with_error_handling(func)