import os
import json
from deepgram import (
    DeepgramClient,
    UrlSource,
    PrerecordedOptions,
    AnalyzeOptions,
    TextSource,
)

class DeepgramProcessor:
    def __init__(self, api_key: str):
        """Initialize Deepgram client with API key."""
        self.dg = DeepgramClient(api_key)
    
    def transcribe_audio_url(self, audio_url: str, model: str = "nova-3-general") -> str:
        """Transcribe audio from URL and return transcript text."""
        try:
            t_payload = UrlSource(url=audio_url)
            t_opts = PrerecordedOptions(
                model=model,
                smart_format=True
            )
            t_resp = self.dg.listen.rest.v("1").transcribe_url(t_payload, t_opts)
            
            # Extract transcript text
            transcript = t_resp.results.channels[0].alternatives[0].transcript
            if not transcript:
                raise RuntimeError("Empty transcript. Check the audio URL, model, or credentials.")
            
            return transcript
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")
    
    def transcribe_audio_file(self, audio_file, model: str = "nova-3-general") -> str:
        """Transcribe uploaded audio file and return transcript text."""
        try:
            # Read the uploaded file
            audio_data = audio_file.read()
            
            t_payload = {"buffer": audio_data}
            t_opts = PrerecordedOptions(
                model=model,
                smart_format=True
            )
            t_resp = self.dg.listen.rest.v("1").transcribe_file(t_payload, t_opts)
            
            # Extract transcript text
            transcript = t_resp.results.channels[0].alternatives[0].transcript
            if not transcript:
                raise RuntimeError("Empty transcript. Check the audio file, model, or credentials.")
            
            return transcript
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")
    
    def analyze_text(self, text: str, language: str = "en") -> dict:
        """Analyze text for sentiment, topics, and intents."""
        try:
            a_payload = TextSource(buffer=text)
            a_opts = AnalyzeOptions(
                language=language,
                summarize="v2",
                sentiment=True,
                intents=True,
                topics=True
            )
            a_resp = self.dg.read.analyze.v("1").analyze_text(a_payload, a_opts)
            
            return self.normalize_analyze(a_resp)
        except Exception as e:
            raise Exception(f"Analysis failed: {str(e)}")
    
    def to_dict(self, resp_obj):
        """Convert response object to dictionary."""
        if isinstance(resp_obj, dict):
            return resp_obj
        if hasattr(resp_obj, "to_json"):
            return json.loads(resp_obj.to_json())
        # last resort
        return json.loads(json.dumps(resp_obj, default=lambda o: getattr(o, "__dict__", str(o))))
    
    def normalize_analyze(self, resp_obj):
        """Normalize analyze response to match template format."""
        j = self.to_dict(resp_obj)

        avg = (j.get("results", {}).get("sentiments", {}).get("average", {}) or {})
        sentiment = {
            "label": avg.get("sentiment", ""),
            "score": avg.get("sentiment_score", None),
        }

        topics = []
        for seg in (j.get("results", {}).get("topics", {}).get("segments", []) or []):
            for t in (seg.get("topics", []) or []):
                topics.append({
                    "topic": t.get("topic", ""),
                    "score": t.get("confidence_score", None)
                })

        intents = []
        for seg in (j.get("results", {}).get("intents", {}).get("segments", []) or []):
            for it in (seg.get("intents", []) or []):
                intents.append({
                    "intent": it.get("intent", ""),
                    "score": it.get("confidence_score", None)
                })

        return {"sentiment": sentiment, "topics": topics, "intents": intents}
    
    def process_audio_url(self, audio_url: str, model: str = "nova-3-general", language: str = "en") -> dict:
        """Complete pipeline: transcribe audio URL and analyze transcript."""
        try:
            # Step 1: Transcribe audio
            transcript = self.transcribe_audio_url(audio_url, model)
            
            # Step 2: Analyze transcript
            analysis = self.analyze_text(transcript, language)
            
            return {
                "transcript": transcript,
                "analysis": analysis
            }
        except Exception as e:
            raise Exception(f"Processing failed: {str(e)}")
    
    def process_audio_file(self, audio_file, model: str = "nova-3-general", language: str = "en") -> dict:
        """Complete pipeline: transcribe audio file and analyze transcript."""
        try:
            # Step 1: Transcribe audio
            transcript = self.transcribe_audio_file(audio_file, model)
            
            # Step 2: Analyze transcript
            analysis = self.analyze_text(transcript, language)
            
            return {
                "transcript": transcript,
                "analysis": analysis
            }
        except Exception as e:
            raise Exception(f"Processing failed: {str(e)}")
    
    def process_text(self, text: str, language: str = "en") -> dict:
        """Process text directly for analysis."""
        try:
            analysis = self.analyze_text(text, language)
            return {
                "transcript": text,
                "analysis": analysis
            }
        except Exception as e:
            raise Exception(f"Processing failed: {str(e)}")


# Example usage function
def process_input(api_key: str, input_type: str, input_data, model: str = "nova-3-general", language: str = "en") -> dict:
    """
    Process input based on type.
    
    Args:
        api_key: Deepgram API key
        input_type: "url", "file", or "text"
        input_data: URL string, uploaded file, or text string
        model: Deepgram model to use
        language: Language code for analysis
    
    Returns:
        Dictionary with transcript and analysis results
    """
    processor = DeepgramProcessor(api_key)
    
    if input_type == "url":
        return processor.process_audio_url(input_data, model, language)
    elif input_type == "file":
        return processor.process_audio_file(input_data, model, language)
    elif input_type == "text":
        return processor.process_text(input_data, language)
    else:
        raise ValueError("Invalid input_type. Must be 'url', 'file', or 'text'")
