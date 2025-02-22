import streamlit as st
from typing import Dict, List, Any
from datetime import datetime
from analytics_error_handler import safe_track

class InterviewAnalytics:
    def __init__(self):
        self.initialize_metrics()
    
    def initialize_metrics(self):
        """Initialize or reset analytics metrics"""
        self.metrics = {
            "emotion": [],
            "technical_score": 0,
            "behavioral_score": 0,
            "communication_score": 0,
            "confidence_score": 0,
            "experience_alignment": 0,
            "interview_duration": 0,
            "questions_answered": 0,
            "start_time": datetime.now()
        }
    
    @safe_track
    def update_scores(self, 
                     technical: float = 0, 
                     behavioral: float = 0,
                     communication: float = 0,
                     confidence: float = 0,
                     alignment: float = 0):
        """Update interview scores with validation"""
        try:
            self.metrics["technical_score"] = min(100, max(0, self.metrics["technical_score"] + technical))
            self.metrics["behavioral_score"] = min(100, max(0, self.metrics["behavioral_score"] + behavioral))
            self.metrics["communication_score"] = min(100, max(0, self.metrics["communication_score"] + communication))
            self.metrics["confidence_score"] = min(100, max(0, self.metrics["confidence_score"] + confidence))
            self.metrics["experience_alignment"] = min(100, max(0, self.metrics["experience_alignment"] + alignment))
        except Exception as e:
            st.error(f"Error updating scores: {str(e)}")
    
    @safe_track
    def add_emotion(self, emotion: str):
        """Add emotion detection result"""
        if emotion and isinstance(emotion, str):
            self.metrics["emotion"].append(emotion)
    
    @safe_track
    def increment_questions(self):
        """Increment questions answered counter"""
        self.metrics["questions_answered"] += 1
        self.update_duration()
    
    @safe_track
    def update_duration(self):
        """Update interview duration"""
        current_time = datetime.now()
        duration = (current_time - self.metrics["start_time"]).total_seconds()
        self.metrics["interview_duration"] = round(duration)
    
    @safe_track
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        self.update_duration()
        return self.metrics

# Global analytics instance
analytics = InterviewAnalytics()