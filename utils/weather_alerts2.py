import requests
import os
from location import get_user_location

WEATHERBIT_API_KEY = os.getenv("WEATHERBIT_API_KEY")  # Set this in your .env

def get_weather_alerts(lat=None, lon=None):
    """
    Fetch current severe weather/natural disaster alerts for a given latitude and longitude using Weatherbit API.
    If lat/lon are not provided, use the user's location via IP geolocation.
    Returns a list of alerts, each with 'title', 'description', 'severity', etc.
    """
    if WEATHERBIT_API_KEY is None:
        return [{"event": "Error", "description": "Weatherbit API key not set."}]
    
    # If lat/lon not provided, get from user location
    if lat is None or lon is None:
        location = get_user_location()
        if "error" in location or not location.get("loc"):
            return [{"event": "Error", "description": "Could not determine location for weather alerts."}]
        lat, lon = map(float, location["loc"].split(","))

    url = (
        f"https://api.weatherbit.io/v2.0/alerts"
        f"?lat={lat}&lon={lon}&key={WEATHERBIT_API_KEY}"
    )
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        alerts = data.get("alerts", [])
        # Normalize output for consistency
        results = []
        for alert in alerts:
            results.append({
                "event": alert.get("title", "Alert"),
                "description": alert.get("description", ""),
                "severity": alert.get("severity", ""),
                "effective_utc": alert.get("effective_utc", ""),
                "expires_utc": alert.get("expires_utc", ""),
                "uri": alert.get("uri", "")
            })
        return results
    except Exception as e:
        return [{"event": "Error", "description": str(e)}]

if __name__ == "__main__":
    alerts = get_weather_alerts()  # Uses user's location by default
    if alerts:
        print("\n🌩️ Weather/Natural Disaster Alerts:")
        for alert in alerts:
            print(f"- {alert.get('event', 'Alert')}: {alert.get('description', '')}")
    else:
        print("No current weather or disaster alerts.")