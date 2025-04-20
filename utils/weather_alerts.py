import requests
import os
from location import get_user_location

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY") 

def get_weather_alerts(lat=None, lon=None):
    """
    Fetch current weather/natural disaster alerts for a given latitude and longitude.
    If lat/lon are not provided, use the user's location via IP geolocation.
    Returns a list of alerts, each with 'event', 'description', etc.
    """
    # If lat/lon not provided, get from user location
    if lat is None or lon is None:
        location = get_user_location()
        if "error" in location or not location.get("loc"):
            return [{"event": "Error", "description": "Could not determine location for weather alerts."}]
        lat, lon = map(float, location["loc"].split(","))

    url = (
        f"https://api.openweathermap.org/data/3.0/onecall"
        f"?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    )
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        alerts = data.get("alerts", [])
        return alerts
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