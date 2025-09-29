# 🎤 Deepgram AI Speech Intelligence Platform

A comprehensive Streamlit application that leverages Deepgram's powerful AI capabilities for speech-to-text, intelligent analysis, and text-to-speech conversion.

## ✨ Features

### 🎯 **Multi-Input Support**
- **URL Input**: Process audio files directly from URLs (default: spacewalk.wav)
- **Text Input**: Analyze text directly for sentiment, topics, and intent
- **File Upload**: Support for WAV, MP3, M4A, FLAC, OGG, WEBM formats

### 🧠 **AI-Powered Analysis**
- **Sentiment Analysis**: Detect emotional tone with confidence scores
- **Topic Detection**: Identify key topics and themes discussed
- **Intent Recognition**: Understand the underlying purpose or goal
- **Confidence Scoring**: All analyses include reliability metrics

### 🎙️ **Text-to-Speech (TTS)**
- **6 Voice Personas**: Choose from Thalia, Zeus, Asteria, Odysseus, Arcas, Andromeda
- **Smart Caching**: Instant playback for repeated requests
- **Clean Audio**: Automatic removal of markdown formatting
- **Multiple Languages**: Support for English variants (en, en-US, en-GB)

### ⚙️ **Advanced Configuration**
- **Model Selection**: Choose from Nova-3, Nova-2, Enhanced, or Base models
- **Language Support**: Multiple English language variants
- **Voice Customization**: Select from 6 different Aura-2 voice personas
- **Real-time Processing**: Fast analysis with progress indicators

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Deepgram API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/deepgram-speech-intelligence.git
   cd deepgram-speech-intelligence
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   echo "DEEPGRAM_API_KEY=your_api_key_here" > .env
   ```

4. **Run the application**
   ```bash
   streamlit run streamlit_demo.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## 📋 Usage

### 1. **Select Input Method**
   - **URL Input**: Paste audio file URL (default spacewalk.wav included)
   - **Text Input**: Type or paste text directly
   - **File Upload**: Upload audio files from your device

### 2. **Configure Settings** (Sidebar)
   - Choose Deepgram model (Nova-3 recommended)
   - Select language variant
   - Pick voice persona for TTS

### 3. **Analyze Content**
   - Click "🚀 Analyze" button
   - View real-time processing progress
   - Get comprehensive results

### 4. **Listen to Results**
   - Click "🎵 Generate Speech" for transcript
   - Click "🎵 Generate Speech" for analysis
   - Enjoy natural-sounding audio output

## 🏗️ Project Structure

```
deepgram-speech-intelligence/
├── streamlit_demo.py          # Main Streamlit application
├── deepgram_processor.py      # Deepgram API integration
├── tts_processor.py           # Text-to-speech functionality
├── narrative_renderer.py      # Analysis formatting
├── requirements.txt           # Python dependencies
├── background.png            # Application background
├── .env                      # Environment variables (not in git)
└── README.md                 # This file
```

## 🔧 Configuration

### Environment Variables
```bash
DEEPGRAM_API_KEY=your_deepgram_api_key_here
```

### Supported Audio Formats
- WAV, MP3, M4A, FLAC, OGG, WEBM

### Voice Personas
| Persona | Description |
|---------|-------------|
| **Thalia** | Warm and friendly |
| **Zeus** | Authoritative and strong |
| **Asteria** | Clear and professional |
| **Odysseus** | Conversational and engaging |
| **Arcas** | Calm and soothing |
| **Andromeda** | Modern and dynamic |

## 🎨 Features in Detail

### **Speech-to-Text**
- High-accuracy transcription using Deepgram's latest models
- Support for multiple audio formats and sources
- Real-time processing with progress indicators

### **Intelligent Analysis**
- **Sentiment Analysis**: Positive, negative, or neutral with confidence scores
- **Topic Detection**: Identifies key subjects and themes
- **Intent Recognition**: Understands the speaker's purpose or goal
- **Structured Output**: Clean, readable analysis results

### **Text-to-Speech**
- **Multiple Voices**: 6 different Aura-2 voice personas
- **Smart Processing**: Automatic text cleaning for natural speech
- **Caching System**: Instant playback for repeated requests
- **High Quality**: Professional-grade audio output

### **User Interface**
- **Responsive Design**: Works on desktop and mobile
- **Professional Styling**: Clean, modern interface
- **Real-time Feedback**: Progress indicators and status messages
- **Intuitive Controls**: Easy-to-use input methods

## 🔒 Security

- API keys stored in environment variables
- `.env` file excluded from version control
- No sensitive data in codebase

## 📊 Performance

- **Fast Processing**: Optimized for speed with caching
- **Memory Efficient**: Smart session state management
- **Scalable**: Handles various input sizes and formats
- **Reliable**: Error handling and graceful fallbacks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Deepgram](https://deepgram.com/) for powerful AI speech processing
- [Streamlit](https://streamlit.io/) for the amazing web framework
- [Aura-2](https://deepgram.com/aura) for high-quality voice synthesis

## 📞 Support

For questions, issues, or contributions, please:
- Open an issue on GitHub
- Check the documentation
- Review the code comments

---

**Built with ❤️ using Deepgram AI and Streamlit**
