from property import Property


class Apartment(Property):
    def __init__(self, property_id, district, area, rooms, price, status):
        super().__init__(
            property_id, district, area, rooms, price, status
        )

    def calculate_price_per_m2(self):
        return super().calculate_price_per_m2()