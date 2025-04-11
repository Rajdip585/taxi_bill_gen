from modules.maps_api_handler import MapsAPIHandler
from modules import db_handler

class BillingHandler:
    def __init__(self, rate_per_km=10):
        self.maps = MapsAPIHandler()
        self.rate_per_km = rate_per_km

    def calculate_bill(self, distance_km):
        return round(distance_km * self.rate_per_km, 2)

    def generate_and_store_bill(self, name, pickup, destination):
        try:
            distance = self.maps.get_distance_km(pickup, destination)
            amount = self.calculate_bill(distance)

            db_handler.log_bill(name, pickup, destination, distance, amount)

            print(f"[BILLING] User: {name} | Distance: {distance} km | Amount: ₹{amount}")
            return {
                "username": name,
                "pickup": pickup,
                "destination": destination,
                "distance": distance,
                "amount": amount
            }
        except Exception as e:
            print(f"[ERROR] Billing failed: {e}")
            return None
