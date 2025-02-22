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
        
        For each main question, generate 2-3 relevant sub-questions that dive deeper into the topic.
        Format the questions into these categories:
        1. Introduction (2 main questions)
        2. Technical Skills (3 main questions)
        3. Behavioral (3 main questions)
        4. Role-specific (2 main questions)
        
        IMPORTANT: Your response must be a valid JSON string with exactly this structure:
        {
            "questions": [
                {
                    "category": "Introduction",
                    "main_question": "Tell me about your background and experience.",
                    "sub_questions": [
                        "What aspects of your previous roles are most relevant to this position?",
                        "How has your education prepared you for this role?"
                    ]
                }
            ]
        }
        
        Ensure to:
        1. Use proper JSON formatting with double quotes for all strings
        2. Include exactly 10 questions total across all categories
        3. Each main question must have 2-3 sub-questions
        4. Follow the category distribution specified above"""
        
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
            
        questions = completion.choices[0].message.content.strip()
        if not questions:
            raise Exception("Empty response received from LLM")
            
        # Parse the JSON response with better error handling
        try:
            # First, ensure we're working with valid JSON string
            questions = questions.replace("'", "\"")  # Replace single quotes with double quotes
            questions = questions.strip()
            if not questions.startswith('{'):
                # Try to find the JSON object start
                start_idx = questions.find('{')
                if start_idx != -1:
                    questions = questions[start_idx:]
                else:
                    raise Exception("Invalid JSON format: No object start found")
            
            questions_data = json.loads(questions)
            
            # Validate the response structure
            if not isinstance(questions_data, dict) or 'questions' not in questions_data:
                raise Exception("Invalid response format: Missing 'questions' key")
                
            if not isinstance(questions_data['questions'], list):
                raise Exception("Invalid response format: 'questions' must be an array")
                
            for q in questions_data['questions']:
                if not all(key in q for key in ['category', 'main_question', 'sub_questions']):
                    raise Exception("Invalid question format: Missing required fields")
                    
            return questions_data
            
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse questions response as JSON: {str(e)}")
            
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