import streamlit as st
from speech_utils import record_audio
from llm_utils import get_llm_response, generate_interview_questions
from tts_utils import text_to_speech
from ui_components import (
    setup_page_config, apply_custom_css, add_security_headers,
    display_header, display_chat_history, display_initial_form,
    display_interview_interface, display_sidebar_controls,
    display_analytics, display_help_section, display_footer
)
from state_management import (
    initialize_session_state, update_candidate_info,
    update_interview_progress, add_message, increment_question,
    reset_session
)

# Initialize the application
setup_page_config()
apply_custom_css()
add_security_headers()
initialize_session_state()

# Header with progress bar
st.title("🤖 AI Interview Assistant")
if st.session_state.interview_stage != "initial":
    progress = (st.session_state.current_question / 10) * 100  # Assuming 10 questions total
    st.progress(progress / 100)
    st.markdown(f"Question {st.session_state.current_question}/10")

# Display chat history in a container
with st.container():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Initial form for candidate information with improved UI and accessibility
if st.session_state.interview_stage == "initial":
    st.markdown("""
        <h2 style='text-align: center;' role="heading" aria-level="2">Welcome to Your AI Interview! 👋</h2>
        <p style='text-align: center;' role="text">Please provide the following information to begin.</p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your Name 👤", key="name_input", autocomplete="name", help="Enter your full name")
    with col2:
        position = st.text_input("Position Applied For 💼", key="position_input", autocomplete="organization-title", help="Enter the job position you're applying for")
    
    requirements = st.text_area("Key Job Requirements 📝", 
        key="requirements_input",
        help="List the main requirements for the position",
        placeholder="Enter key job requirements here")
    
    if st.button("Begin Interview 🎯", help="Click to start the interview process") and name and position and requirements:
        st.session_state.candidate_info = {
            "name": name,
            "position": position,
            "requirements": requirements
        }
        # Generate interview questions
        st.session_state.interview_questions = generate_interview_questions(st.session_state.candidate_info)
        st.session_state.interview_stage = "interview"
        st.session_state.current_question = 1
        st.rerun()

# Interview stage with sequential questions
elif st.session_state.interview_stage == "interview":
    st.markdown("""
        <div style='text-align: center; margin-bottom: 20px;'>
            <h3>Interview in Progress 🎯</h3>
        </div>
    """, unsafe_allow_html=True)

    # Display current question category and progress
    if st.session_state.interview_questions:
        st.info(st.session_state.interview_questions)

    # Voice input section with improved UI and accessibility
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("🎤 Click to Answer", key="voice_button", help="Click to start voice recording"):
            with st.spinner("Listening..."):
                user_input = record_audio()
            
            if user_input:
                # Display user message
                st.session_state.messages.append({"role": "user", "content": user_input})
                with st.chat_message("user"):
                    st.write(user_input)
                
                # Prepare context for AI with current question number and questions
                context = f"Candidate Name: {st.session_state.candidate_info['name']}\n"
                context += f"Position: {st.session_state.candidate_info['position']}\n"
                context += f"Job Requirements: {st.session_state.candidate_info['requirements']}\n"
                context += f"Current Question Number: {st.session_state.current_question}\n"
                context += f"Interview Questions: {st.session_state.interview_questions}\n"
                context += f"User Input: {user_input}"
                
                # Get and display AI response
                with st.spinner("Processing your response..."):
                    # Update analytics based on response
                    import random  # Simulating analytics for demo
                    st.session_state.analytics["emotion"].append(random.choice(["Confident", "Nervous", "Enthusiastic", "Calm"]))
                    st.session_state.analytics["technical_score"] = min(100, st.session_state.analytics["technical_score"] + random.randint(5, 15))
                    st.session_state.analytics["behavioral_score"] = min(100, st.session_state.analytics["behavioral_score"] + random.randint(5, 15))
                    st.session_state.analytics["communication_score"] = min(100, st.session_state.analytics["communication_score"] + random.randint(5, 15))
                    st.session_state.analytics["confidence_score"] = min(100, st.session_state.analytics["confidence_score"] + random.randint(5, 15))
                    st.session_state.analytics["experience_alignment"] = min(100, st.session_state.analytics["experience_alignment"] + random.randint(5, 15))
                    
                    ai_response = get_llm_response(context, st.session_state.messages[:-1])
                
                if ai_response:
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                    with st.chat_message("assistant"):
                        st.write(ai_response)
                    
                    # Convert response to speech
                    text_to_speech(ai_response)
                    
                    # Increment question counter
                    st.session_state.current_question += 1
                    
                    # Check if interview is complete
                    if st.session_state.current_question > 10:
                        st.success("Interview Complete! Thank you for your time.")
                        st.session_state.interview_stage = "complete"
    
    with col2:
        if st.button("⏭️ Skip Question", key="skip_button", help="Click to skip current question"):
            st.session_state.current_question += 1
            st.rerun()

# Sidebar controls and analytics
if display_sidebar_controls():
    reset_session()
    st.rerun()

if st.session_state.interview_stage == "interview":
    display_analytics(st.session_state.analytics)

# Help section and footer
display_help_section()
display_footer()
st.rerun()