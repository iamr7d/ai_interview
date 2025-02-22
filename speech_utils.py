import streamlit as st
import speech_recognition as sr

# Initialize speech recognizer
recognizer = sr.Recognizer()

def record_audio():
    """Record audio from microphone and convert to text"""
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            st.error("Could not understand audio")
            return None
        except sr.RequestError:
            st.error("Could not request results")
            return None