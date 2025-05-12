from utils.location import get_user_location
from utils.map_resources import search_places, create_resource_map

def main():
    ask_location = input("May Rescura access your location to generate a map of nearby emergency resources? (yes/no): ").strip().lower()
    if ask_location != "yes":
        print("Location access denied. Map generation failed.")
        return

    print("Detecting your location...")
    location = get_user_location()
    if "error" in location or not location.get("loc"):
        print("Could not determine your location. Map cannot be generated.")
        return

    lat, lon = map(float, location["loc"].split(","))
    print(f"Your detected location: {location.get('city', '')}, {location.get('region', '')}, {location.get('country', '')}")
    print("Searching for nearby hospitals, schools, clinics, and other resources...")

    places = search_places(lat, lon)
    if not places:
        print("No relevant places found nearby.")
    else:
        print(f"Found {len(places)} places. Generating map...")

    fmap = create_resource_map(lat, lon, places)
    fmap.save("resources_map.html")
    print("Map saved as resources_map.html. Open this file in your browser to view.")

if __name__ == "__main__":
    main()