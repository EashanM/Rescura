from typing import Any, Dict
import re

def safe_get(data: Dict, *keys: str, default: Any = None) -> Any:
    """Safely retrieve nested dictionary values"""
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current

def calculate_tokens(text: str) -> int:
    """Approximate token count for a string"""
    return len(text) // 4  # Rough approximation

def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS format"""
    return f"{int(seconds // 3600):02}:{int((seconds % 3600) // 60):02}:{int(seconds % 60):02}"
