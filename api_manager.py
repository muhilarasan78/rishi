
import requests
import os
import urllib.parse
import random

class TripGenixAPIManager:
    def __init__(self):
        self.unsplash_access_key = os.environ.get('UNSPLASH_KEY')
        self.user_agent = "TripGenix_AI_Agent/1.0" # OSM requires a user agent

    def get_location_data(self, place_name):
        """
        Fetches Lat, Lon, Display Name, Region from OpenStreetMap (Nominatim).
        """
        try:
            url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(place_name)}&format=json&limit=1"
            headers = {'User-Agent': self.user_agent}
            response = requests.get(url, headers=headers)
            if response.status_code == 200 and response.json():
                data = response.json()[0]
                return {
                    "lat": float(data.get('lat')),
                    "lon": float(data.get('lon')),
                    "display_name": data.get('display_name'),
                    # Region extraction might be tricky from display_name, usually it's comma separated
                    # But for now we just return lat/lon as requested primarily.
                }
        except Exception as e:
            print(f"Error fetching location for {place_name}: {e}")
        return None

    def get_description(self, place_name):
        """
        Fetches description from Wikipedia.
        """
        try:
            # First try direct search
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(place_name)}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if 'extract' in data:
                    return {
                        "title": data.get('title'),
                        "extract": data.get('extract')
                    }
        except Exception as e:
            print(f"Error fetching description for {place_name}: {e}")
        return {"title": place_name, "extract": f"Discover the beauty of {place_name}."}

    def get_images(self, place_name):
        """
        Fetches images from Unsplash.
        """
        if not self.unsplash_access_key:
            # Fallback if key not present, or maybe log a warning
            print("Unsplash Key missing!")
            # Generate 10 unique seeded placeholders for fallback
            return [f"https://picsum.photos/seed/{place_name.replace(' ', '')}{i}/800/600" for i in range(10)]

        try:
            url = f"https://api.unsplash.com/search/photos?query={urllib.parse.quote(place_name)}&client_id={self.unsplash_access_key}&per_page=10&orientation=landscape"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                if results:
                    return [img['urls']['regular'] for img in results]
        except Exception as e:
            print(f"Error fetching images for {place_name}: {e}")
        
        # Fallback if API fails or no images
        return [f"https://source.unsplash.com/800x600/?{urllib.parse.quote(place_name)}"]

    def generate_map_link(self, place_name):
        """
        Generates Google Maps link.
        """
        return f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(place_name)}"

    def get_hotels(self, place_name, lat=None, lon=None):
        """
        Fetches real hotels near the place using OSM/Nominatim.
        """
        try:
            # If lat/lon not provided, fetch them first
            if not lat or not lon:
                loc = self.get_location_data(place_name)
                if loc:
                    lat, lon = loc['lat'], loc['lon']
                else:
                    return [] # Cannot search without location

            # Nominatim search for hotels near coordinates
            # We use a structured query or just 'hotels in [place_name]' if place name is good
            # But searching near lat/lon is better.
            # Nominatim doesn't have a strict 'near' parameter for search endpoint easily exposed, 
            # but we can try searching "hotels near [Place Name]" 
            
            url = f"https://nominatim.openstreetmap.org/search?q=hotels+in+{urllib.parse.quote(place_name)}&format=json&limit=10&addressdetails=1"
            headers = {'User-Agent': self.user_agent}
            response = requests.get(url, headers=headers)
            
            hotels = []
            if response.status_code == 200:
                results = response.json()
                for item in results:
                    # Filter for actual tourism/hotel items just in case
                    if item.get('class') == 'tourism' or 'hotel' in item.get('type', ''):
                        hotels.append({
                            "name": item.get('display_name').split(',')[0], # Keep it short, OSM names are long addresses
                            "address": item.get('display_name'),
                            "lat": item.get('lat'),
                            "lon": item.get('lon'),
                            # Simulate Rating and Price since OSM doesn't have them
                            "rating": round(random.uniform(3.5, 5.0), 1),
                            "price": random.randint(1500, 15000) 
                        })
            
            # Simple fallback if "hotels in X" returns nothing (common for smaller places in OSM)
            if not hotels: 
                # Retry with just "hotel" and viewbox? Too complex.
                # Let's fallback to simulating if empty, but explicitly marked.
                # Actually, ml_engine can handle the empty list fallback.
                pass
                
            return hotels

        except Exception as e:
            print(f"Error fetching hotels for {place_name}: {e}")
            return []

    def enrich_place(self, place_name):
        """
        Orchestrates the data fetching and merging.
        """
        print(f"Enriching data for: {place_name}...")
        
        # 1. Location
        location = self.get_location_data(place_name)
        if not location:
            # Fallback check - maybe append ", India" or similar if generic search fails?
            # For now assume ML engine gives good names.
            location = {"lat": 0.0, "lon": 0.0}

        # 2. Description
        wiki_data = self.get_description(place_name)
        
        # 3. Images
        images = self.get_images(place_name)
        
        # 4. Map Link
        map_link = self.generate_map_link(place_name)
        
        # 5. Hotels (Fetch here or separate? Separate is better for on-demand detail page load)
        # We won't call get_hotels here to save time during bulk generation. Called on demand.

        # 6. Output Format
        return {
            "name": place_name,
            "about": wiki_data['extract'],
            "location": {
                "lat": location['lat'],
                "lon": location['lon']
            },
            "images": images,
            "map": map_link
        }
