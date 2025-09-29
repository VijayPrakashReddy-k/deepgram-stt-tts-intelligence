import base64
import os
import streamlit as st
from dotenv import load_dotenv
from narrative_renderer import render_narrative
from deepgram_processor import process_input
import re

# Load environment variables
load_dotenv()

def clean_text_for_tts(text):
    """Clean text by removing markdown formatting for better TTS."""
    # Remove markdown bold formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    # Remove markdown headers
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    # Remove markdown bullet points
    text = re.sub(r'^[-*]\s*', '', text, flags=re.MULTILINE)
    # Remove extra whitespace and newlines
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters that TTS might read
    text = re.sub(r'[#$%&*+=\[\]\\^_`|~]', '', text)
    return text.strip()

def clean_analysis_for_tts(text):
    """Clean analysis text specifically for TTS with better formatting."""
    # Remove markdown bold formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    # Remove markdown headers but keep structure
    text = re.sub(r'^###\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^##\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^#\s*', '', text, flags=re.MULTILINE)
    # Replace bullet points with "and" for better flow
    text = re.sub(r'^[-*]\s*', 'and ', text, flags=re.MULTILINE)
    # Remove extra whitespace and newlines
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters that TTS might read
    text = re.sub(r'[#$%&*+=\[\]\\^_`|~]', '', text)
    # Clean up multiple "and" words
    text = re.sub(r'\band\s+and\s+', 'and ', text)
    return text.strip()

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'transcript' not in st.session_state:
    st.session_state.transcript = None
if 'narrative' not in st.session_state:
    st.session_state.narrative = None

# Page configuration
st.set_page_config(
    page_title="Deepgram AI Speech Intelligence Platform",
    page_icon="🎤",
    layout="wide"
)

def get_base64_of_file(png_path: str) -> str:
    with open(png_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_page_bg(png_path: str) -> None:
    try:
        bin_str = get_base64_of_file(png_path)
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{bin_str}");
                background-size: cover;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
    except Exception:
        pass  # background is optional

# Set background image
set_page_bg("background.png")


# Title and description - centered
st.markdown("""
<div style="text-align: center;">
    <h1>🎤 Deepgram AI Speech Intelligence Platform</h1>
    <p>Upload audio files, enter text, or provide URLs to analyze with Deepgram's AI capabilities</p>
</div>
""", unsafe_allow_html=True)

# Add spacing
st.markdown("<br><br>", unsafe_allow_html=True)


# Sidebar for settings and instructions
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Model selection
    model = st.selectbox(
        "Deepgram Model",
        ["nova-3-general", "nova-2", "nova", "enhanced", "base"],
        help="Choose the Deepgram model to use for transcription"
    )
    
    # Language selection
    language = st.selectbox(
        "Language",
        ["en", "en-US", "en-GB"],
        help="Select the language for analysis"
    )
    
    # Voice persona selection
    voice_persona = st.selectbox(
        "Voice Persona",
        ["thalia", "zeus", "asteria", "odysseus", "arcas", "andromeda"],
        help="Select voice persona for text-to-speech"
    )
    
    st.markdown("---")
    
    st.header("🎙️ Voice Personas")
    st.markdown("""
    **Aura-2** is a family with multiple voice personas:
    - **thalia** - Warm and friendly
    - **zeus** - Authoritative and strong
    - **asteria** - Clear and professional
    - **odysseus** - Conversational and engaging
    - **arcas** - Calm and soothing
    - **andromeda** - Modern and dynamic
    """)
    
    st.markdown("---")
    
    st.header("📝 Instructions")
    st.markdown("""
    1. Choose input method:
       - Upload audio file
       - Enter text directly
       - Provide URL to audio
    2. Click 'Analyze' to process
    """)

# Main content area
# Create single row with two columns
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Choose Input Method")
    # Input method selection
    input_method = st.radio(
        "Select:",
        ["URL Input", "Text Input", "Audio File Upload"],
        horizontal=False,
        label_visibility="collapsed"
    )

with col2:
    # URL input
    if input_method == "URL Input":
        st.subheader("🔗 Audio URL")
        url_input = st.text_input(
            "Enter audio URL:",
            value="https://dpgr.am/spacewalk.wav",
            placeholder="https://example.com/audio.mp3",
            help="Provide a direct URL to an audio file"
        )

    # Text input
    elif input_method == "Text Input":
        st.subheader("📝 Enter Text")
        text_input = st.text_area(
            "Enter text to analyze:",
            height=200,
            placeholder="Type or paste your text here...",
            help="Enter the text you want to analyze for sentiment, topics, and intents"
        )

    # Audio file upload
    elif input_method == "Audio File Upload":
        st.subheader("🎵 Upload Audio File")
        uploaded_file = st.file_uploader(
            "Choose an audio file",
            type=['wav', 'mp3', 'm4a', 'flac', 'ogg', 'webm'],
            help="Supported formats: WAV, MP3, M4A, FLAC, OGG, WEBM"
        )

# Analyze button
st.markdown("<br>", unsafe_allow_html=True)
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

with col_btn2:
    analyze_button = st.button(
        "🚀 Analyze",
        type="primary",
        use_container_width=True
    )

# Analyze button functionality
if analyze_button:
    # Check if any input is provided
    has_input = False
    input_data = None
    input_type = None
    
    if input_method == "Audio File Upload" and uploaded_file is not None:
        has_input = True
        input_data = uploaded_file
        input_type = "file"
    elif input_method == "Text Input" and text_input.strip():
        has_input = True
        input_data = text_input
        input_type = "text"
    elif input_method == "URL Input" and url_input.strip():
        has_input = True
        input_data = url_input
        input_type = "url"
    
    if not has_input:
        st.warning("Please provide input (audio file, text, or URL) before analyzing")
    else:
        with st.spinner("Processing with Deepgram... This may take a few moments"):
            try:
                # Load Deepgram API key from environment
                api_key = os.getenv("DEEPGRAM_API_KEY")
                if not api_key:
                    st.error("DEEPGRAM_API_KEY not found in environment variables. Please check your .env file.")
                    st.stop()
                
                # Process the input with selected model and language
                result = process_input(api_key, input_type, input_data, model, language)
                
                # Store results in session state
                st.session_state.analysis_results = result
                st.session_state.transcript = result["transcript"]
                st.session_state.narrative = render_narrative(result["analysis"])
                
                st.success("Analysis completed!")
                    
            except Exception as e:
                st.error(f"Error during processing: {str(e)}")

# Display results if they exist in session state
if st.session_state.analysis_results is not None:
    st.markdown("---")
    st.markdown("<h2 style='text-align: center;'>📝 Transcript</h2>", unsafe_allow_html=True)
    st.write(st.session_state.transcript)
    
    st.markdown("---")
    st.markdown("<h2 style='text-align: center;'>🧠 Text Intelligence</h2>", unsafe_allow_html=True)
    st.write(st.session_state.narrative)
    
    # TTS section
    st.markdown("---")
    st.markdown("<h2 style='text-align: center;'>🎙️ Text-to-Speech (TTS)</h2>", unsafe_allow_html=True)
    
    # TTS for transcript
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Listen to Transcript:**")
        transcript_clicked = st.button("🎵 Generate Speech", key="transcript_tts")
        
        if transcript_clicked:
            try:
                from tts_processor import TTSProcessor
                api_key = os.getenv("DEEPGRAM_API_KEY")
                processor = TTSProcessor(api_key)
                with st.spinner(f"Generating speech with {voice_persona}..."):
                    # Clean the transcript text for better TTS
                    clean_transcript = clean_text_for_tts(st.session_state.transcript)
                    # Use speak_text_fast for longer transcript text (500 chars vs 200)
                    audio_html = processor.speak_text_fast(clean_transcript, voice_persona, language)
                    st.markdown(audio_html, unsafe_allow_html=True)
                    st.success(f"Generated speech with {voice_persona} voice!")
            except Exception as e:
                st.error(f"Failed to generate speech: {str(e)}")
    
    with col2:
        st.markdown("**Listen to Analysis:**")
        analysis_clicked = st.button("🎵 Generate Speech", key="analysis_tts")
        
        if analysis_clicked:
            try:
                from tts_processor import TTSProcessor
                api_key = os.getenv("DEEPGRAM_API_KEY")
                processor = TTSProcessor(api_key)
                with st.spinner(f"Generating speech with {voice_persona}..."):
                    # Clean the narrative text for better TTS
                    clean_narrative = clean_analysis_for_tts(st.session_state.narrative)
                    # Use speak_text_fast for longer analysis text (500 chars vs 200)
                    audio_html = processor.speak_text_fast(clean_narrative, voice_persona, language)
                    st.markdown(audio_html, unsafe_allow_html=True)
                    st.success(f"Generated speech with {voice_persona} voice!")
            except Exception as e:
                st.error(f"Failed to generate speech: {str(e)}")
    
    # Raw analysis data (collapsible)
    st.markdown("---")
    with st.expander("🔍 Raw Analysis Data"):
        st.json(st.session_state.analysis_results["analysis"])

