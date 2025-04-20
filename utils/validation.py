from typing import Dict, Any

def validate_triage_response(response: Dict) -> bool:
    """Validate structure of triage agent response"""
    required_keys = {"severity", "rationale", "immediate_actions", "diagnosis"}
    if not all(key in response for key in required_keys):
        return False
    
    if not isinstance(response["severity"], int) or not (1 <= response["severity"] <=5):
        return False
    
    return True

def sanitize_input(text: str) -> str:
    """Basic input sanitization"""
    return text.strip().replace("\n", " ").replace("\t", " ")[:1000]
