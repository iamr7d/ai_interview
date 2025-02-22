import streamlit as st
import speech_recognition as sr

# Initialize speech recognizer
recognizer = sr.Recognizer()

def record_audio():
    """Record audio from microphone and convert to text"""
    try:
        with sr.Microphone() as source:
            st.write("Listening...")
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=30)
            try:
                text = recognizer.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                st.error("Could not understand audio. Please speak clearly and try again.")
                return None
            except sr.RequestError as e:
                st.error(f"Could not request results from speech recognition service: {str(e)}")
                return None
    except Exception as e:
        st.error(f"Error accessing microphone: {str(e)}. Please check your microphone settings.")
        return None