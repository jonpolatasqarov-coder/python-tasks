class Property:
    def __init__(self, property_id, district, area, rooms, price, status):
        self.property_id = property_id
        self.district = district
        self.area = area
        self.rooms = rooms
        self.price = price
        self.status = status

    def calculate_price_per_m2(self):
        if self.area <= 0:
            raise ValueError("Property area must be greater than zero.")

        return self.price / self.area