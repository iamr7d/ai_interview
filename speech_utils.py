import streamlit as st
import speech_recognition as sr
import time

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

def continuous_listening():
    """Continuously listen for user input with automatic silence detection"""
    try:
        with sr.Microphone() as source:
            st.write("Listening... (Speak your answer)")
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # Set dynamic energy threshold for better silence detection
            recognizer.dynamic_energy_threshold = True
            recognizer.energy_threshold = 4000
            
            # Parameters for silence detection
            min_silence_duration = 2.0  # seconds of silence to stop
            phrase_timeout = 30  # maximum time for a single phrase
            
            audio_data = []
            silence_start = None
            recording_start = time.time()
            
            while True:
                try:
                    # Listen for a phrase
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=phrase_timeout)
                    audio_data.append(audio)
                    
                    # Check for silence
                    if recognizer.energy_threshold > recognizer.get_energy(audio):
                        if silence_start is None:
                            silence_start = time.time()
                        elif time.time() - silence_start >= min_silence_duration:
                            break
                    else:
                        silence_start = None
                    
                    # Check for maximum duration
                    if time.time() - recording_start >= phrase_timeout:
                        break
                        
                except sr.WaitTimeoutError:
                    break
            
            # Combine all audio segments and convert to text
            if audio_data:
                try:
                    combined_audio = audio_data[0]  # Use the first segment as base
                    for segment in audio_data[1:]:
                        combined_audio.extend(segment)
                    
                    text = recognizer.recognize_google(combined_audio)
                    return text
                except sr.UnknownValueError:
                    st.error("Could not understand audio. Please speak clearly and try again.")
                    return None
                except sr.RequestError as e:
                    st.error(f"Could not request results from speech recognition service: {str(e)}")
                    return None
            return None
            
    except Exception as e:
        st.error(f"Error in continuous listening: {str(e)}. Please check your microphone settings.")
        return None