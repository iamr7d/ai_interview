import streamlit as st

def initialize_session_state():
    """Initialize all session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "interview_stage" not in st.session_state:
        st.session_state.interview_stage = "initial"
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    
    if "interview_questions" not in st.session_state:
        st.session_state.interview_questions = None
    
    if "candidate_info" not in st.session_state:
        st.session_state.candidate_info = {
            "name": "",
            "position": "",
            "requirements": ""
        }
    
    if "analytics" not in st.session_state:
        st.session_state.analytics = {
            "emotion": [],
            "technical_score": 0,
            "behavioral_score": 0,
            "communication_score": 0,
            "confidence_score": 0,
            "experience_alignment": 0
        }

def update_candidate_info(name, position, requirements):
    """Update candidate information in session state"""
    st.session_state.candidate_info = {
        "name": name,
        "position": position,
        "requirements": requirements
    }

def update_interview_progress(questions=None):
    """Update interview progress and questions"""
    if questions:
        st.session_state.interview_questions = questions
    st.session_state.interview_stage = "interview"
    st.session_state.current_question = 1

def add_message(role, content):
    """Add a new message to the chat history"""
    st.session_state.messages.append({"role": role, "content": content})

def increment_question():
    """Increment the current question counter"""
    st.session_state.current_question += 1
    if st.session_state.current_question > 10:
        st.session_state.interview_stage = "complete"
        return True
    return False

def reset_session():
    """Reset all session state variables"""
    st.session_state.messages = []
    st.session_state.interview_stage = "initial"
    st.session_state.current_question = 0
    st.session_state.interview_questions = None
    st.session_state.candidate_info = {"name": "", "position": "", "requirements": ""}
    st.session_state.analytics = {
        "emotion": [],
        "technical_score": 0,
        "behavioral_score": 0,
        "communication_score": 0,
        "confidence_score": 0,
        "experience_alignment": 0
    }