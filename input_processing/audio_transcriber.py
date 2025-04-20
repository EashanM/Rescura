import whisper
from typing import Optional
from config.logger import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

class AudioTranscriber:
    def __init__(self, model_size="base"):
        self.model = whisper.load_model(model_size)
        
    def transcribe(self, audio_path: str) -> Optional[str]:
        try:
            result = self.model.transcribe(audio_path)
            return result["text"]
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            return None
