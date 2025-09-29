import os
import requests
import base64
import streamlit as st
import time
import hashlib
from functools import lru_cache

class TTSProcessor:
    def __init__(self, api_key: str):
        """Initialize TTS processor with Deepgram API key."""
        self.api_key = api_key
        self.base_url = "https://api.deepgram.com/v1/speak"
        self.session = requests.Session()  # Reuse connections
        self.session.headers.update({
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "audio/mpeg"
        })
        self.cache = {}  # Simple in-memory cache
    
    @lru_cache(maxsize=1)
    def get_available_voices(self):
        """Get list of available Aura-2 voice personas (cached)."""
        return {
            "thalia": "Warm and friendly",
            "zeus": "Authoritative and strong", 
            "asteria": "Clear and professional",
            "odysseus": "Conversational and engaging",
            "arcas": "Calm and soothing",
            "andromeda": "Modern and dynamic"
        }
    
    def generate_speech(self, text: str, voice: str = "thalia", language: str = "en") -> bytes:
        """
        Generate speech from text using Deepgram TTS (optimized for speed).
        
        Args:
            text: Text to convert to speech
            voice: Voice persona (thalia, zeus, asteria, odysseus, arcas, andromeda)
            language: Language code (en, en-US, en-GB)
        
        Returns:
            Audio bytes in MP3 format
        """
        try:
            # Truncate text if too long for faster processing
            max_length = 1000  # Adjust based on your needs
            if len(text) > max_length:
                text = text[:max_length] + "..."
            
            model = f"aura-2-{voice}-{language}"
            url = f"{self.base_url}?model={model}"
            
            payload = {"text": text}
            
            # Use session for connection reuse and faster requests
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            return response.content
            
        except Exception as e:
            raise Exception(f"TTS generation failed: {str(e)}")
    
    def create_audio_player(self, audio_bytes: bytes) -> str:
        """
        Create HTML audio player for Streamlit (optimized).
        
        Args:
            audio_bytes: Audio data in bytes
            
        Returns:
            HTML string for audio player
        """
        try:
            # Use faster base64 encoding
            b64 = base64.b64encode(audio_bytes).decode("ascii")
            return f'<audio controls preload="auto" src="data:audio/mpeg;base64,{b64}"></audio>'
        except Exception as e:
            raise Exception(f"Audio player creation failed: {str(e)}")
    
    def speak_text(self, text: str, voice: str = "thalia", language: str = "en") -> str:
        """
        Complete pipeline: generate speech and return HTML player (optimized).
        
        Args:
            text: Text to convert to speech
            voice: Voice persona
            language: Language code
            
        Returns:
            HTML string for audio player
        """
        try:
            start_time = time.time()
            audio_bytes = self.generate_speech(text, voice, language)
            html_player = self.create_audio_player(audio_bytes)
            
            # Optional: Log performance (remove in production)
            elapsed = time.time() - start_time
            print(f"TTS generation took {elapsed:.2f} seconds")
            
            return html_player
        except Exception as e:
            raise Exception(f"Speech generation failed: {str(e)}")
    
    def speak_text_fast(self, text: str, voice: str = "thalia", language: str = "en") -> str:
        """
        Ultra-fast TTS pipeline with smart caching and minimal processing.
        
        Args:
            text: Text to convert to speech (truncated to 500 chars for speed)
            voice: Voice persona
            language: Language code
            
        Returns:
            HTML string for audio player
        """
        try:
            # Create cache key
            cache_key = hashlib.md5(f"{text[:100]}_{voice}_{language}".encode()).hexdigest()
            
            # Check cache first
            if cache_key in self.cache:
                print(f"Cache hit for TTS: {cache_key[:8]}...")
                return self.cache[cache_key]
            
            # Truncate text more aggressively for speed
            max_length = 500
            if len(text) > max_length:
                text = text[:max_length] + "..."
            
            start_time = time.time()
            audio_bytes = self.generate_speech(text, voice, language)
            html_player = self.create_audio_player(audio_bytes)
            
            # Cache the result
            self.cache[cache_key] = html_player
            
            elapsed = time.time() - start_time
            print(f"Fast TTS generation took {elapsed:.2f} seconds")
            
            return html_player
        except Exception as e:
            raise Exception(f"Fast speech generation failed: {str(e)}")
    
    def speak_text_instant(self, text: str, voice: str = "thalia", language: str = "en") -> str:
        """
        Instant TTS with maximum speed optimizations.
        
        Args:
            text: Text to convert to speech (truncated to 200 chars for instant response)
            voice: Voice persona
            language: Language code
            
        Returns:
            HTML string for audio player
        """
        try:
            # Create cache key
            cache_key = hashlib.md5(f"{text[:50]}_{voice}_{language}".encode()).hexdigest()
            
            # Check cache first
            if cache_key in self.cache:
                print(f"Instant cache hit for TTS: {cache_key[:8]}...")
                return self.cache[cache_key]
            
            # Truncate text aggressively for instant response
            max_length = 200
            if len(text) > max_length:
                text = text[:max_length] + "..."
            
            start_time = time.time()
            audio_bytes = self.generate_speech(text, voice, language)
            html_player = self.create_audio_player(audio_bytes)
            
            # Cache the result
            self.cache[cache_key] = html_player
            
            elapsed = time.time() - start_time
            print(f"Instant TTS generation took {elapsed:.2f} seconds")
            
            return html_player
        except Exception as e:
            raise Exception(f"Instant speech generation failed: {str(e)}")


def create_tts_player(text: str, api_key: str, voice: str, language: str = "en"):
    """
    Create TTS audio player for selected voice persona in Streamlit.
    
    Args:
        text: Text to convert to speech
        api_key: Deepgram API key
        voice: Selected voice persona
        language: Language code
    """
    if not text.strip():
        st.warning("No text available for speech synthesis.")
        return
    
    processor = TTSProcessor(api_key)
    voices = processor.get_available_voices()
    
    if voice not in voices:
        st.error(f"Invalid voice persona: {voice}")
        return
    
    try:
        with st.spinner(f"Generating speech with {voice}..."):
            audio_html = processor.speak_text(text, voice, language)
            st.markdown(audio_html, unsafe_allow_html=True)
            st.success(f"Generated speech with {voice} voice!")
    except Exception as e:
        st.error(f"Failed to generate speech with {voice}: {str(e)}")


def create_tts_buttons(text: str, api_key: str, language: str = "en"):
    """
    Create TTS buttons for all voice personas in Streamlit.
    
    Args:
        text: Text to convert to speech
        api_key: Deepgram API key
        language: Language code
    """
    if not text.strip():
        st.warning("No text available for speech synthesis.")
        return
    
    processor = TTSProcessor(api_key)
    voices = processor.get_available_voices()
    
    st.markdown("### 🎙️ Listen to Results")
    
    # Create columns for voice buttons
    cols = st.columns(3)
    
    for i, (voice, description) in enumerate(voices.items()):
        col_idx = i % 3
        
        with cols[col_idx]:
            if st.button(f"🎵 {voice.title()}", help=description, use_container_width=True):
                try:
                    with st.spinner(f"Generating speech with {voice}..."):
                        audio_html = processor.speak_text(text, voice, language)
                        st.markdown(audio_html, unsafe_allow_html=True)
                        st.success(f"Generated speech with {voice} voice!")
                except Exception as e:
                    st.error(f"Failed to generate speech with {voice}: {str(e)}")
