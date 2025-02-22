import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
from functools import lru_cache
import hashlib
import json

# Load environment variables
load_dotenv()

# Import configuration
from config import config

# Initialize Groq client with proper error handling
def initialize_groq_client():
    try:
        # Use the config instance to get the validated API key
        api_key = config.groq_api_key
            
        # Initialize Groq client with validated API key
        client = Groq(api_key=api_key)
        
        # Test the client with a simple completion
        try:
            test_completion = client.chat.completions.create(
                messages=[{
                    "role": "user",
                    "content": "Test connection"
                }],
                model="llama-3.3-70b-versatile"
            )
            if test_completion and test_completion.choices:
                return client
            else:
                st.error("Failed to validate Groq client connection. Please check your API key.")
                return None
        except Exception as e:
            st.error(f"Failed to validate Groq client connection: {str(e)}")
            return None
    except Exception as e:
        st.error(f"Failed to initialize Groq client: {str(e)}")
        return None

client = initialize_groq_client()

# Cache configuration
CACHE_TTL = 3600  # Cache time-to-live in seconds

def generate_cache_key(data):
    """Generate a unique cache key from input data"""
    return hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()

@lru_cache(maxsize=100)
def generate_interview_questions(candidate_info_str):
    """Generate structured interview questions based on candidate info"""
    try:
        # Convert string back to dict
        candidate_info = json.loads(candidate_info_str)
        prompt = f"""Generate a structured set of 10 interview questions for a {candidate_info['position']} position.
        The candidate's name is {candidate_info['name']}.
        Job Requirements: {candidate_info['requirements']}
        
        Format the questions into these categories:
        1. Introduction (2 questions)
        2. Technical Skills (3 questions)
        3. Behavioral (3 questions)
        4. Role-specific (2 questions)
        
        Return the questions as a formatted list with categories."""
        
        if not client:
            raise Exception("LLM client not initialized properly")
            
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1024
        )
        
        if not completion or not completion.choices:
            raise Exception("No response received from LLM")
            
        questions = completion.choices[0].message.content
        if not questions or len(questions.strip()) == 0:
            raise Exception("Empty response received from LLM")
            
        return questions
    except json.JSONDecodeError as e:
        st.error(f"Invalid candidate info format: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Error generating questions: {str(e)}")
        return None

@lru_cache(maxsize=1000)
def get_llm_response_cached(prompt_key):
    """Cached version of LLM response generation"""
    try:
        return client.chat.completions.create(
            messages=[{"role": "user", "content": prompt_key}],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1024
        ).choices[0].message.content
    except Exception as e:
        st.error(f"Error in cached LLM response: {str(e)}")
        return None

def get_llm_response(prompt, conversation_history=None, model="mixtral-8x7b-32768", temperature=0.7, max_tokens=1024):
    """Get response from Groq LLM with conversation history and configurable parameters"""
    if not client:
        st.error("LLM client not initialized")
        return None
        
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
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1024
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error getting LLM response: {str(e)}")
        return None