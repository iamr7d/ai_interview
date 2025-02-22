import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_interview_questions(candidate_info):
    """Generate structured interview questions based on candidate info"""
    prompt = f"""Generate a structured set of 10 interview questions for a {candidate_info['position']} position.
    The candidate's name is {candidate_info['name']}.
    Job Requirements: {candidate_info['requirements']}
    
    Format the questions into these categories:
    1. Introduction (2 questions)
    2. Technical Skills (3 questions)
    3. Behavioral (3 questions)
    4. Role-specific (2 questions)
    
    Return the questions as a formatted list with categories."""
    
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": prompt}],
            model="mixtral-8x7b-32768",
            temperature=0.7,
            max_tokens=1024
        )
        questions = completion.choices[0].message.content
        return questions
    except Exception as e:
        st.error(f"Error generating questions: {str(e)}")
        return None

def get_llm_response(prompt, conversation_history=None):
    """Get response from Groq LLM with conversation history"""
    try:
        # Initialize messages with system message
        messages = [{
            "role": "system",
            "content": """You are an AI interviewer conducting a professional job interview. Follow this structured approach:
            1. If this is the first interaction (no conversation history):
               - Generate and ask the first question from the structured question list
            2. For subsequent interactions:
               - Analyze the candidate's response
               - Provide brief, constructive feedback if needed
               - Ask relevant follow-up questions based on their answer
               - When satisfied with the response, move to the next question in the sequence
            3. Maintain professional interview etiquette and tone
            4. Keep responses concise but informative
            5. Track progress through questions and adapt based on candidate's responses
            
            Remember to:
            - Stay focused on the current question topic
            - Ask for clarification when needed
            - Provide smooth transitions between questions
            - End each response with a clear question for the candidate"""
        }]
        
        # Add conversation history if available
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add current user message
        messages.append({"role": "user", "content": prompt})
        
        completion = client.chat.completions.create(
            messages=messages,
            model="mixtral-8x7b-32768",
            temperature=0.7,
            max_tokens=1024
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error getting LLM response: {str(e)}")
        return None