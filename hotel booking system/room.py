
class Room:
    def __init__(self, room_number, room_type, price, amenities, location):
        self.room_number = room_number
        self.room_type = room_type
        self.price = price
        self.amenities = amenities
        self.location = location
        self.booked_days = []
        self.is_available = True

    def get_room_type(self):
        return self.room_type


class StandardRoom(Room):
    def __init__(self, room_number, room_type, price, amenities, location):
        super().__init__(
            room_number, room_type, price, amenities, location
        )


class DeluxeRoom(Room):
    def __init__(self, room_number, room_type, price, amenities, location):
        super().__init__(
            room_number, room_type, price, amenities, location
        )


class SuiteRoom(Room):
    def __init__(self, room_number, room_type, price, amenities, location):
        super().__init__(
            room_number, room_type, price, amenities, location
        )

    