import requests

def get_user_location():
    """Get user's approximate location (city, region, country, lat/lon) via IP geolocation."""
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        loc = data.get("loc", "")  # "lat,lon"
        city = data.get("city", "")
        region = data.get("region", "")
        country = data.get("country", "")
        return {
            "city": city,
            "region": region,
            "country": country,
            "loc": loc
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    location = get_user_location()
    if "error" in location:
        print(f"Error: {location['error']}")
    else:
        print(f"Location: {location['city']}, {location['region']}, {location['country']}")
        print(f"Coordinates: {location['loc']}")