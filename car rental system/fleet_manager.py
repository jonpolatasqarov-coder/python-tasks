import json
from car import Car
from truck import Truck
from bike import Bike
from customer import Customer
from datetime import datetime, timedelta

class FleetManager:
    def __init__(self):
        self.vehicles = []
        self.customers = []
        self.rentals = []

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def search_by_name(self, name):
        name = " ".join(name.lower().split())

        for vehicle in self.vehicles:
            vehicle_name = " ".join(vehicle.name.lower().split())

            if vehicle_name == name:
                return vehicle

        return None
    
    def add_customer(self, customer):
        for existing_customer in self.customers:
            if existing_customer.customer_id == customer.customer_id:
                print("Customer ID already exists.")
                return False

            if existing_customer.phone == customer.phone:
                print("This phone number is already registered.")
                return False

        self.customers.append(customer)
        return True

    def save_customers(self, filename="customers.json"):
        data = []

        for customer in self.customers:
            data.append({
                "customer_id": customer.customer_id,
                "name": customer.name,
                "phone": customer.phone,
                "rental_count": customer.rental_count,
                "vehicle_rental_counts": customer.vehicle_rental_counts,
                "used_discounts": customer.used_discounts
            })

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)


    def save_rentals(self, filename="rentals.json"):
        with open(filename, "w") as file:
            json.dump(self.rentals, file, indent=4)


    def load_rentals(self, filename="rentals.json"):
        try:
            with open(filename, "r") as file:
                self.rentals = json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):
            self.rentals = []

    def load_customers(self, filename="customers.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):
            self.customers = []
            return

        self.customers = []

        for customer_data in data:
            customer = Customer(
                customer_data["customer_id"],
                customer_data["name"],
                customer_data["phone"]
            )

            customer.rental_count = customer_data.get("rental_count", 0)

            customer.vehicle_rental_counts = customer_data.get(
                "vehicle_rental_counts", {}
            )

            customer.used_discounts = customer_data.get(
                "used_discounts", {}
            )

            self.customers.append(customer)

    
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
    
    def show_customers(self):
        if not self.customers:
            print("No registered customers.")
            return False

        print(f"{'ID':<6}{'Name':<25}{'Phone'}")
        print("-" * 50)

        for customer in self.customers:
            print(
                f"{customer.customer_id:<6}"
                f"{customer.name:<25}"
                f"{customer.phone}"
            )

        return True

    def rent_vehicle(self, name, days, customer_id):
        vehicle = self.search_by_name(name)

        if vehicle is None:
            print("Vehicle not found.")
            return False

        if not vehicle.is_available:
            print(f"{vehicle.name} is not available.")
            return False

        customer = None

        for existing_customer in self.customers:
            if existing_customer.customer_id == customer_id:
                customer = existing_customer
                break

        if customer is None:
            print("Customer not found.")
            return False

        if isinstance(vehicle, Car):
            max_days = 30
        elif isinstance(vehicle, Bike):
            max_days = 14
        elif isinstance(vehicle, Truck):
            max_days = 50

        if days < 1 or days > max_days:
            print(f"Rental period must be between 1 and {max_days} days.")
            return False

        vehicle_count = customer.vehicle_rental_counts.get(
            vehicle.name, 0
        )

        discount_used = customer.used_discounts.get(
            vehicle.name, False
        )

        discount_eligible = vehicle_count >= 3 and not discount_used

        total = vehicle.calculate_rent(
            days,
            vehicle_count if discount_eligible else 0
        )

        print(f"Total rent: ${total:.2f}")

        while True:
            payment = input("Confirm payment? (yes/no): ").strip().lower()

            if payment == "yes":
                break
            elif payment == "no":
                print("Payment cancelled. Rental aborted.")
                return False
            else:
                print("Please enter 'yes' or 'no'.")

        if vehicle.rent(days):
            customer.rental_count += 1

            customer.vehicle_rental_counts[vehicle.name] = (
                customer.vehicle_rental_counts.get(vehicle.name, 0) + 1
            )

            if discount_eligible:
                customer.used_discounts[vehicle.name] = True

            self.save_customers()

            start_date = datetime.now()
            return_date = start_date + timedelta(days=days)

            rental = {
                "customer_id": customer.customer_id,
                "customer_name": customer.name,
                "customer_phone": customer.phone,
                "vehicle_name": vehicle.name,
                "vehicle_type": type(vehicle).__name__,
                "rental_days": days,
                "total_price": total,
                "start_date": start_date.strftime("%Y-%m-%d %H:%M:%S"),
                "return_date": return_date.strftime("%Y-%m-%d %H:%M:%S"),
                "returned": False
            }

            self.rentals.append(rental)
            self.save_rentals()

            self.log_event(
                f"Customer ID: {customer.customer_id} | "
                f"Name: {customer.name} | "
                f"Phone: {customer.phone} | "
                f"Vehicle: {vehicle.name} ({type(vehicle).__name__}) | "
                f"Rental days: {days} | "
                f"Start date: {rental['start_date']} | "
                f"Return date: {rental['return_date']} | "
                f"Total: ${total:.2f}"
            )

            print(f"Vehicle rented successfully by {customer.name}.")
            print(f"Expected return date: {rental['return_date']}")
            return True

        return False

    def return_vehicle(self, name, customer_id):
        vehicle = self.search_by_name(name)

        if vehicle is None:
            print("Vehicle not found.")
            return False

        rental = None

        for item in reversed(self.rentals):
            if (
                item["vehicle_name"].lower() == vehicle.name.lower()
                and item["customer_id"] == customer_id
                and not item["returned"]
            ):
                rental = item
                break

        if rental is None:
            print("No active rental found for this customer and vehicle.")
            return False

        if vehicle.is_available:
            print(f"{vehicle.name} is already available.")
            return False

        if vehicle.return_vehicle():
            actual_return_date = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            rental["returned"] = True
            rental["actual_return_date"] = actual_return_date

            self.save_rentals()
            self.save_to_json("vehicles.json")

            self.log_event(
                f"Vehicle: {vehicle.name} | "
                f"Customer ID: {customer_id} | "
                f"Customer: {rental['customer_name']} | "
                f"Actual return date: {actual_return_date}"
            )

            print(f"{vehicle.name} returned successfully.")
            print(f"Customer: {rental['customer_name']}")
            print(f"Returned on: {actual_return_date}")
            return True

        return False




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