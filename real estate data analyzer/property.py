class Property:
    def __init__(self, property_id, district, area, rooms, price, status):
        self.property_id = property_id
        self.district = district
        self.area = area
        self.rooms = rooms
        self.price = price
        self.status = status

    def calculate_price_per_m2(self):
        return self.price / self.area