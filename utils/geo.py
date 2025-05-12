# rescura/utils/geo.py
import os
import googlemaps
import time
from haversine import haversine
from dotenv import load_dotenv

load_dotenv()

def geocode_location(location: str) -> dict:
    """Convert address/coordinates to latitude/longitude"""
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        raise ValueError("Google Maps API key missing in .env")
        
    gmaps = googlemaps.Client(key=api_key)
    try:
        result = gmaps.geocode(location)[0]
        return result["geometry"]["location"]
    except Exception as e:
        raise ValueError(f"Geocoding failed: {str(e)}")

def find_nearby_hospitals(location: str, radius: int = 5000) -> list:
    """Find hospitals near a location (address or coordinates)"""
    coords = geocode_location(location)
    gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))
    
    hospitals = []
    try:
        places_result = gmaps.places_nearby(
            location=(coords["lat"], coords["lng"]),
            radius=radius,
            type="hospital"
        )
        while True:
            for place in places_result.get("results", []):
                # Get detailed info including phone numbers
                details = gmaps.place(place["place_id"], fields=["formatted_phone_number"])
                
                hospitals.append({
                    "name": place["name"],
                    "address": place["vicinity"],
                    "phone": details.get("result", {}).get("formatted_phone_number", "N/A"),
                    "distance_km": haversine(
                        (coords["lat"], coords["lng"]),
                        (place["geometry"]["location"]["lat"], place["geometry"]["location"]["lng"])
                    )
                })
            
            if "next_page_token" not in places_result:
                break
            time.sleep(2)
            places_result = gmaps.places_nearby(page_token=places_result["next_page_token"])
    
    except Exception as e:
        print(f"Hospital search error: {str(e)}")
        return []
    
    return sorted(hospitals, key=lambda x: x["distance_km"])[:5]  # Return top 5 nearest
