import requests

# A simple mapping for common countries. Expand as needed.
EMERGENCY_NUMBERS = {
    "US": "911",
    "CA": "911",
    "GB": "999",
    "AU": "000",
    "IN": "112",
    "FR": "112",
    "DE": "112",
    "ES": "112",
    "IT": "112",
    "CN": "120",
    "JP": "119",
    "SG": "995",
    "ZA": "10111",
    "BR": "190",
    "RU": "112",
    # Add more as needed
}

def get_emergency_number(country_code: str) -> str:
    """Return the emergency services number for a given country code (ISO Alpha-2)."""
    return EMERGENCY_NUMBERS.get(country_code.upper(), "112")  # 112 is the international GSM emergency number

if __name__ == "__main__":
    # Example usage
    for code in ["US", "GB", "IN", "FR", "ZZ"]:
        print(f"Country: {code}, Emergency Number: {get_emergency_number(code)}")
        