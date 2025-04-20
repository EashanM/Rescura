from transformers import pipeline
from typing import Optional
from config.logger import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

class ImageAnalyzer:
    def __init__(self):
        self.model = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
        
    def describe(self, image_path: str) -> Optional[str]:
        try:
            return self.model(image_path)[0]["generated_text"]
        except Exception as e:
            logger.error(f"Image analysis failed: {str(e)}")
            return None
