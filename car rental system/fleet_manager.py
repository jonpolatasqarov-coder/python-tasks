import json

from car import Car
from truck import Truck
from bike import Bike
 

class FleetManager:
    def __init__(self):
        self.vehicles = []

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def search_by_name(self, name):
        name = " ".join(name.lower().split())

        for vehicle in self.vehicles:
            vehicle_name = " ".join(vehicle.name.lower().split())

            if vehicle.name.lower() == name.lower():
                return vehicle

        return None

    def search_by_type(self, vehicle_type):
        results = []

        for vehicle in self.vehicles:
            if type(vehicle).__name__.lower() == vehicle_type.lower():
                results.append(vehicle)

        return results

    def search_by_price(self, max_price):
        results = []

        for vehicle in self.vehicles:
            if vehicle.price_per_day <= max_price:
                results.append(vehicle)

        return results

    def rent_vehicle(self, name, days):
        vehicle = self.search_by_name(name)

        if vehicle is None:
            print("Vehicle not found.")    
            return

        if days <= 0:
            print("Invalid number of rental days.")
            return

        if vehicle.rent(days):
            total = vehicle.calculate_rent(days)

            print(f"Total rent: ${total:.2f}")

            self.log_event(
                f"{vehicle.name} rented for {days} day(s). "
                f"Total: ${total:.2f}"
            )

    def return_vehicle(self, name):
        vehicle = self.search_by_name(name)

        if vehicle is None:
            print("Vehicle not found.")
            return

        if vehicle.return_vehicle():
            self.log_event(f"{vehicle.name} has been returned.")

    def log_event(self, message):
        with open("rental.log", "a") as file:
            file.write(message + "\n")

    def save_to_json(self, filename):
        data = []

        for vehicle in self.vehicles:
            vehicle_data = {
                "type": type(vehicle).__name__,
                "name": vehicle.name,
                "price_per_day": vehicle.price_per_day,
                "is_available": vehicle.is_available,
                "rental_count": vehicle.rental_count

            }   

            data.append(vehicle_data)

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    def load_from_json(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)

        self.vehicles = []

        for vehicle_data in data:
            if vehicle_data["type"] == "Car":
                vehicle = Car(
                    vehicle_data["name"],
                    vehicle_data["price_per_day"]
                )

            elif vehicle_data["type"] == "Truck":
                vehicle = Truck(
                    vehicle_data["name"],
                    vehicle_data["price_per_day"]
                )

            elif vehicle_data["type"] == "Bike":
                vehicle = Bike(
                    vehicle_data["name"],
                    vehicle_data["price_per_day"]
                )

            else:
                continue

            vehicle.is_available = vehicle_data["is_available"]
            vehicle.rental_count = vehicle_data["rental_count"]

            self.vehicles.append(vehicle)

    def load_initial_fleet(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)

        self.vehicles = []

        for vehicle_data in data:
            if vehicle_data["type"] == "Car":
                vehicle = Car(
                    vehicle_data["name"],
                    vehicle_data["price_per_day"]
                )

            elif vehicle_data["type"] == "Truck":
                vehicle = Truck(
                    vehicle_data["name"],
                    vehicle_data["price_per_day"]
                )

            elif vehicle_data["type"] == "Bike":
                vehicle = Bike(
                    vehicle_data["name"],
                    vehicle_data["price_per_day"]
                )

            else:
                continue

            self.vehicles.append(vehicle)


