import streamlit as st
from job_data import job_positions, skills_by_position

# Set up page configuration as the first Streamlit command
st.set_page_config(
    page_title="AI Interview Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'About': 'AI Interview Assistant - Your virtual interviewing companion'
    }
)

# Import other dependencies after page config
import json
from speech_utils import record_audio
from llm_utils import get_llm_response, generate_interview_questions
from tts_utils import text_to_speech
from ui_components import (
    apply_custom_css, add_security_headers,
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
if 'initialized' not in st.session_state:
    try:
        initialize_session_state()
        st.session_state.initialized = True
    except Exception as e:
        st.error(f"Failed to initialize session state: {str(e)}")
        st.stop()
apply_custom_css()
add_security_headers()

# Header with progress bar
st.title("🤖 AI Interview Assistant")

# Display chat history in a container
with st.container():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Candidate information form and interview interface
if not st.session_state.interview_questions:
    try:
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Name 👤", key="name_input", autocomplete="name", help="Enter your full name")
        with col2:
            position = st.selectbox("Position Applied For 💼", options=job_positions, key="position_input", help="Select the job position you're applying for")
        
        if position:
            selected_skills = st.multiselect(
                "Select Required Skills 🎯",
                options=skills_by_position[position],
                default=skills_by_position[position][:3],
                help="Select the required skills for the position"
            )
            requirements = ", ".join(selected_skills)
        else:
            requirements = ""
        
        if st.button("Begin Interview 🎯", help="Click to start the interview process"):
            if not name or not position or not selected_skills:
                st.error("Please fill in all required fields before starting the interview.")
            else:
                try:
                    with st.spinner("Preparing your interview questions..."):
                        update_candidate_info(name, position, requirements)
                        candidate_info_str = json.dumps(st.session_state.candidate_info)
                        questions = generate_interview_questions(candidate_info_str)
                        
                        if questions:
                            update_interview_progress(questions)
                            st.rerun()
                        else:
                            st.error("Failed to generate interview questions. Please try again.")
                except Exception as e:
                    st.error(f"An error occurred while starting the interview: {str(e)}")
    except Exception as e:
        st.error(f"Error in form rendering: {str(e)}")

# Interview progress display
if st.session_state.interview_questions:
    progress = min((st.session_state.current_question / 10) * 100, 100)
    st.progress(progress / 100)
    st.markdown(f"Question {min(st.session_state.current_question, 10)}/10")
    
    # Display current question and its sub-questions
    current_questions = st.session_state.interview_questions.get('questions', [])
    if 0 <= st.session_state.current_question < len(current_questions):
        current_q = current_questions[st.session_state.current_question]
        
        # Display category
        st.subheader(f"Category: {current_q['category']}")
        
        # Display main question
        st.write("**Main Question:**")
        st.info(current_q['main_question'])
        
        # Display sub-questions
        st.write("**Follow-up Questions:**")
        for i, sub_q in enumerate(current_q['sub_questions'], 1):
            st.write(f"{i}. {sub_q}")
    
    # Voice input section
    if st.button("🎤 Start Speaking", help="Click to start speaking your answer"):
        user_response = continuous_listening()
        if user_response:
            add_message("user", user_response)
            with st.spinner("Analyzing your response..."):
                try:
                    llm_response = get_llm_response(user_response)
                    if llm_response:
                        add_message("assistant", llm_response)
                        text_to_speech(llm_response)
                        if increment_question():
                            st.success("Interview completed! Thank you for your time.")
                            st.balloons()
                            display_analytics()
                        else:
                            st.rerun()
                except Exception as e:
                    st.error(f"Error processing response: {str(e)}")

    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("🎤 Click to Answer", key="voice_button", help="Click to start voice recording"):
            with st.spinner("Listening..."):
                user_input = record_audio()
            
            if user_input:
                st.session_state.messages.append({"role": "user", "content": user_input})
                with st.chat_message("user"):
                    st.write(user_input)
                
                context = f"Candidate Name: {st.session_state.candidate_info['name']}\n"
                context += f"Position: {st.session_state.candidate_info['position']}\n"
                context += f"Job Requirements: {st.session_state.candidate_info['requirements']}\n"
                context += f"Current Question Number: {st.session_state.current_question}\n"
                context += f"Interview Questions: {st.session_state.interview_questions}\n"
                context += f"User Input: {user_input}"
                
                with st.spinner("Processing your response..."):
                    import random
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
                    
                    text_to_speech(ai_response)
                    st.session_state.current_question += 1
                    
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

if st.session_state.interview_questions:
    display_analytics(st.session_state.analytics)

# Help section and footer
display_help_section()
display_footer()