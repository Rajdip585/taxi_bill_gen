import openrouteservice
from openrouteservice import convert
from dotenv import load_dotenv
import requests
import os

# Load API key from .env
load_dotenv()
ORS_API_KEY = os.getenv("ORS_API_KEY")

class MapsAPIHandler:
    def __init__(self):
        if not ORS_API_KEY:
            raise ValueError("ORS_API_KEY not found. Please check your .env file.")
        self.client = openrouteservice.Client(key=ORS_API_KEY)

    def get_coordinates(self, address):
        geocode = self.client.pelias_search(text=address)
        coords = geocode['features'][0]['geometry']['coordinates']
        return coords  # [longitude, latitude]

    def get_distance_km(self, origin_address, destination_address):
        start_coords = self.get_coordinates(origin_address)
        end_coords = self.get_coordinates(destination_address)

        route = self.client.directions(
            coordinates=[start_coords, end_coords],
            profile='driving-car',
            format='geojson'
        )

        distance_meters = route['features'][0]['properties']['segments'][0]['distance']
        return round(distance_meters / 1000, 2)  # distance in km
    
    def download_route_map(self, pickup, destination, save_path="ui/route_map.png"):
        try:
            start = self.get_coordinates(pickup)
            end = self.get_coordinates(destination)

            coords_param = f"{start[0]},{start[1]}|{end[0]},{end[1]}"
            url = f"https://api.openrouteservice.org/maps/staticmap?api_key={ORS_API_KEY}&coordinates={coords_param}&layer=standard"

            response = requests.get(url)
            if response.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(response.content)
                print("[MAP] Static route map saved successfully.")
                return True
            else:
                print("[MAP] Failed to download map:", response.text)
                return False
        except Exception as e:
            print("[MAP ERROR]", e)
            return False
