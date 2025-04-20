# rescura/input_processing/text_processor.py
import re
import logging
from typing import Dict, Optional, List
from langdetect import detect, LangDetectException
from utils.validation import sanitize_input 

logger = logging.getLogger(__name__)

class TextProcessor:
    def __init__(self):
        self.medical_terms = {
            'fracture', 'bleeding', 'burn', 'allergy', 'cardiac',
            'respiratory', 'trauma', 'poison', 'seizure', 'shock'
        }

    def clean_text(self, text: str) -> str:
        """Clean and normalize input text"""
        try:
            # Basic sanitization
            cleaned = sanitize_input(text)
            
            # Remove special characters except medical relevant ones
            cleaned = re.sub(r'[^a-zA-Z0-9\s.,!?\-%\']', '', cleaned)
            
            # Normalize whitespace
            cleaned = re.sub(r'\s+', ' ', cleaned).strip()
            
            return cleaned.lower()  # Case-insensitive processing
            
        except Exception as e:
            logger.error(f"Text cleaning failed: {str(e)}")
            return text  # Return original as fallback

    def detect_language(self, text: str) -> Optional[str]:
        """Detect language of input text"""
        try:
            return detect(text)
        except LangDetectException as e:
            logger.warning(f"Language detection failed: {str(e)}")
            return None

    def translate_to_english(self, text: str) -> str:
        """Placeholder for translation service integration"""
        # In production, integrate with DeepL/Google Translate API
        return text  # Implement actual translation logic here

    def extract_medical_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract medical-related terms from text"""
        try:
            found_terms = []
            symptoms = []
            
            # Simple pattern matching (expand with regex patterns)
            symptom_pattern = r"(pain|swelling|nausea|dizziness|shortness of breath)"
            matches = re.findall(symptom_pattern, text, re.IGNORECASE)
            if matches:
                symptoms.extend(matches)
            
            # Check against medical terms dictionary
            tokens = set(text.lower().split())
            found_terms = list(tokens & self.medical_terms)
            
            return {
                "medical_terms": found_terms,
                "symptoms": symptoms,
                "severity_keywords": self._detect_severity(text)
            }
            
        except Exception as e:
            logger.error(f"Entity extraction failed: {str(e)}")
            return {}

    def _detect_severity(self, text: str) -> List[str]:
        """Identify severity indicators in text"""
        severity_words = {
            'mild', 'moderate', 'severe', 'critical',
            'emergency', 'urgent', 'extreme'
        }
        return [word for word in text.lower().split() if word in severity_words]

    def process(self, raw_text: str) -> Dict[str, any]:
        """Full text processing pipeline"""
        try:
            cleaned = self.clean_text(raw_text)
            
            return {
                "cleaned_text": cleaned,
                "language": self.detect_language(cleaned),
                "entities": self.extract_medical_entities(cleaned),
                "word_count": len(cleaned.split()),
                "contains_emergency_keywords": bool(re.search(
                    r"\b(emergency|911|urgent|help|accident)\b", 
                    cleaned, 
                    re.IGNORECASE
                ))
            }
            
        except Exception as e:
            logger.error(f"Text processing failed: {str(e)}")
            return {}
