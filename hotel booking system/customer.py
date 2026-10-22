
import json
import os


class Customer:
    def __init__(
        self, name, phone, is_vip=False,
        total_nights=0, customer_id=None
    ):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone
        self.is_vip = is_vip
        self.total_nights = total_nights

    def add_nights(self, nights):
        self.total_nights += nights

        if self.total_nights >= 10:
            self.is_vip = True

    @staticmethod
    def load_customers():
        if not os.path.exists("customers.json"):
            return []

        with open("customers.json", "r", encoding="utf-8") as file:
            return json.load(file)

    def save_customer(self):
        customers = Customer.load_customers()

        for customer in customers:
            if customer["phone"] == self.phone:
                customer["name"] = self.name
                customer["is_vip"] = self.is_vip
                customer["total_nights"] = self.total_nights

                with open(
                    "customers.json", "w", encoding="utf-8"
                ) as file:
                    json.dump(
                        customers, file,
                        ensure_ascii=False, indent=4
                    )

                return

        customer_id = max(
            (customer.get("customer_id", 0) for customer in customers),
            default=0
        ) + 1

        customers.append({
            "customer_id": customer_id,
            "name": self.name,
            "phone": self.phone,
            "is_vip": self.is_vip,
            "total_nights": self.total_nights
        })

        with open("customers.json", "w", encoding="utf-8") as file:
            json.dump(
                customers, file,
                ensure_ascii=False, indent=4
            )

    @staticmethod
    def find_by_phone(phone):
        customers = Customer.load_customers()

        for data in customers:
            if data["phone"] == phone:
                return Customer(
                    data["name"],
                    data["phone"],
                    data.get("is_vip", False),
                    data.get("total_nights", 0),
                    data.get("customer_id")
                )

        return None

    @staticmethod
    def find_by_id(customer_id):
        customers = Customer.load_customers()

        for data in customers:
            if data.get("customer_id") == customer_id:
                return Customer(
                    data["name"],
                    data["phone"],
                    data.get("is_vip", False),
                    data.get("total_nights", 0),
                    data.get("customer_id")
                )

        return None
