import streamlit as st
from gtts import gTTS
from playsound import playsound
import os

def text_to_speech(text):
    """Convert text to speech and play it"""
    try:
        tts = gTTS(text=text, lang='en')
        audio_file = "response.mp3"
        tts.save(audio_file)
        playsound(audio_file)
        os.remove(audio_file)  # Clean up the audio file
    except Exception as e:
        st.error(f"Error in text-to-speech: {str(e)}")