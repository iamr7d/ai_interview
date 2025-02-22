import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# Configuration class to manage environment variables and settings
class Config:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.validate_config()
    
    def validate_config(self):
        """Validate required configuration variables"""
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set. Please add your API key to the .env file.")
        if not isinstance(self.groq_api_key, str) or len(self.groq_api_key.strip()) == 0:
            raise ValueError("Invalid GROQ_API_KEY format. Please check your API key.")
        self.groq_api_key = self.groq_api_key.strip()

# Initialize configuration
def init_config():
    """Initialize and validate configuration"""
    try:
        return Config()
    except Exception as e:
        st.error(f"Configuration Error: {str(e)}")
        st.stop()

# Global configuration instance
config = init_config()