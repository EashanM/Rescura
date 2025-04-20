from input_processing.text_processor import TextProcessor

def test_clean_text():
    tp = TextProcessor()
    assert tp.clean_text("Hello!! 123") == "hello 123"

def test_detect_language():
    tp = TextProcessor()
    assert tp.detect_language("Hello, how are you?") == "en"

def test_extract_medical_entities():
    tp = TextProcessor()
    result = tp.extract_medical_entities("I have severe pain and swelling from a fracture.")
    assert "medical_terms" in result
    assert "symptoms" in result

def test_process_pipeline():
    tp = TextProcessor()
    result = tp.process("Emergency! I can't breathe.")
    assert "cleaned_text" in result
    assert result["contains_emergency_keywords"] is True
