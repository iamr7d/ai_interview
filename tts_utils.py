import streamlit as st
from gtts import gTTS
from playsound import playsound
import os

def text_to_speech(text):
    """Convert text to speech and play it"""
    audio_file = "response.mp3"
    try:
        if not text or len(text.strip()) == 0:
            raise ValueError("Empty text provided for speech conversion")
            
        tts = gTTS(text=text, lang='en')
        tts.save(audio_file)
        playsound(audio_file)
    except Exception as e:
        st.error(f"Error in text-to-speech: {str(e)}")
    finally:
        # Clean up the audio file in finally block to ensure it's always removed
        try:
            if os.path.exists(audio_file):
                os.remove(audio_file)
        except Exception as e:
            st.warning(f"Failed to clean up audio file: {str(e)}")