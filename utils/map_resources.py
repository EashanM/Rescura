import requests
import folium
import os
from dotenv import load_dotenv
load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")  # Set this in your .env

SEARCH_TYPES = [
    "hospital", "school", "police", "doctor", "pharmacy", "clinic", "university", "fire_station", "health"
]

def search_places(lat, lon, radius=5000, types=SEARCH_TYPES):
    """Search for relevant places near the given lat/lon using Google Places API."""
    results = []
    for place_type in types:
        url = (
            f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            f"?location={lat},{lon}&radius={radius}&type={place_type}&key={GOOGLE_MAPS_API_KEY}"
        )
        resp = requests.get(url)
        if resp.status_code == 200:
            data = resp.json()
            for place in data.get("results", []):
                results.append({
                    "name": place.get("name"),
                    "lat": place["geometry"]["location"]["lat"],
                    "lon": place["geometry"]["location"]["lng"],
                    "type": place_type,
                    "address": place.get("vicinity", "")
                })
            print(f"Found {len(data.get('results', []))} {place_type}(s) near ({lat}, {lon})")
    return results

def create_resource_map(lat, lon, places):
    """Create a folium map with markers for each place."""
    fmap = folium.Map(location=[lat, lon], zoom_start=14)
    for place in places:
        folium.Marker(
            [place["lat"], place["lon"]],
            popup=f"{place['name']} ({place['type']})\n{place['address']}",
            icon=folium.Icon(color="red" if place["type"] == "hospital" else "green")
        ).add_to(fmap)
    folium.Marker(
        [lat, lon],
        popup="You are here",
        icon=folium.Icon(color="blue")
    ).add_to(fmap)
    return fmap

if __name__ == "__main__":
    # Example usage: Palo Alto, CA
    lat, lon = 37.4419, -122.1430
    places = search_places(lat, lon)
    fmap = create_resource_map(lat, lon, places)
    fmap.save("resources_map.html")
    print("Map saved as resources_map.html")