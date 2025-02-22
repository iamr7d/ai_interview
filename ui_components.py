import streamlit as st

def setup_page_config():
    """Set up the initial page configuration"""
    st.set_page_config(
        page_title="AI Interview Assistant",
        page_icon="🤖",
        layout="centered",
        menu_items={
            'About': 'AI Interview Assistant - Your virtual interviewing companion'
        }
    )

def apply_custom_css():
    """Apply custom CSS styles for better UI"""
    st.markdown("""
        <style>
        .stButton>button {
            width: 100%;
            border-radius: 20px;
            height: 3em;
            position: relative;
        }
        .stProgress > div > div > div {
            background-color: #00cc00;
        }
        [role="button"] {
            cursor: pointer;
        }
        </style>
        """, unsafe_allow_html=True)

def add_security_headers():
    """Add security-related HTML headers"""
    st.markdown("""
        <meta charset="utf-8">
        <meta http-equiv="X-Content-Type-Options" content="nosniff">
        <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
        """, unsafe_allow_html=True)

def display_header(current_question=None, interview_stage="initial"):
    """Display the header with progress bar"""
    st.title("🤖 AI Interview Assistant")
    if interview_stage != "initial" and current_question is not None:
        progress = (current_question / 10) * 100
        st.progress(progress / 100)
        st.markdown(f"Question {current_question}/10")

def display_chat_history(messages):
    """Display the chat history in a container"""
    with st.container():
        for message in messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

def display_initial_form():
    """Display the initial form for candidate information"""
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
    
    return name, position, requirements

def display_interview_interface():
    """Display the interview interface with voice input"""
    st.markdown("""
        <div style='text-align: center; margin-bottom: 20px;'>
            <h3>Interview in Progress 🎯</h3>
        </div>
    """, unsafe_allow_html=True)

def display_sidebar_controls():
    """Display the sidebar controls and help section"""
    st.sidebar.markdown("### Interview Controls 🎛️")
    return st.sidebar.button("🔄 Reset Interview", help="Click to start over", key="reset_button")

def display_analytics(analytics):
    """Display analytics in the sidebar"""
    st.sidebar.markdown("### Real-time Analytics 📊")
    
    # Emotion Tracking
    st.sidebar.markdown("#### Current Emotion 😊")
    if analytics["emotion"]:
        current_emotion = analytics["emotion"][-1]
        st.sidebar.info(f"Current Emotion: {current_emotion}")
    
    # Performance Metrics
    st.sidebar.markdown("#### Performance Metrics 📈")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Technical", f"{analytics['technical_score']}%")
        st.metric("Communication", f"{analytics['communication_score']}%")
    with col2:
        st.metric("Behavioral", f"{analytics['behavioral_score']}%")
        st.metric("Confidence", f"{analytics['confidence_score']}%")
    
    # Experience Alignment
    st.sidebar.markdown("#### Job Fit Analysis 🎯")
    st.sidebar.progress(analytics["experience_alignment"] / 100)
    st.sidebar.caption(f"Experience Alignment: {analytics['experience_alignment']}%")
    
    # Emotion History
    if analytics["emotion"]:
        st.sidebar.markdown("#### Emotion Timeline 📋")
        emotion_history = ", ".join(analytics["emotion"])
        st.sidebar.caption(f"Emotion Progress: {emotion_history}")

def display_help_section():
    """Display help and instructions in the sidebar"""
    st.sidebar.markdown("### Help & Instructions ℹ️")
    st.sidebar.markdown("""
        1. Fill in your details
        2. Click 'Begin Interview'
        3. Use the microphone to answer questions
        4. Questions progress automatically
        5. Use 'Skip' to move to next question
        6. Reset interview at any time
    """)

def display_footer():
    """Display the footer with accessibility improvements"""
    st.markdown("""
        <div style='position: fixed; bottom: 0; width: 100%; text-align: center; padding: 10px; background: rgba(255, 255, 255, 0.9);' role="contentinfo">
            <p style='margin: 0;' role="text">Powered by AI Interview Assistant 🤖</p>
        </div>
    """, unsafe_allow_html=True)