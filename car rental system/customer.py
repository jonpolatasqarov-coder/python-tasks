class Customer:
    def __init__(self, customer_id, name, phone):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone
        self.rental_count = 0
        self.vehicle_rental_counts = {}
        self.used_discounts = {}