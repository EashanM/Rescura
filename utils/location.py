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

def reverse_geocode(lat, lng):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse"
        params = {
            "lat": lat,
            "lon": lng,
            "format": "json",
            "zoom": 10,
            "addressdetails": 1
        }
        headers = {"User-Agent": "Rescura/1.0"}
        resp = requests.get(url, params=params, headers=headers, timeout=5)
        data = resp.json()
        address = data.get("address", {})
        return {
            "city": address.get("city") or address.get("town") or address.get("village"),
            "region": address.get("state"),
            "country": address.get("country"),
            "country_code": address.get("country_code", "").upper(),
            "lat": lat,
            "lng": lng
        }
    except Exception as e:
        print("Reverse geocoding failed:", e)
        return {"lat": lat, "lng": lng}

if __name__ == "__main__":
    location = get_user_location()
    if "error" in location:
        print(f"Error: {location['error']}")
    else:
        print(f"Location: {location['city']}, {location['region']}, {location['country']}")
        print(f"Coordinates: {location['loc']}")