class Room:
    def __init__(self, room_number, price, amenities, location):
        self.room_number = room_number
        self.price = price
        self.amenities = amenities
        self.location = location
        self.booked_days = []

    def get_room_type(self):
        return "Room"

class StandardRoom(Room):
    def __init__(self, room_number, location):
        super().__init__(
            room_number,
            50,
            ["Wi-Fi", "TV"],
            location
        )

    def get_room_type(self):
        return "Standard"

class DeluxeRoom(Room):
    def __init__(self, room_number, location):
        super().__init__(
            room_number,
            80,
            ["Wi-Fi", "TV", "Mini Bar"],
            location
        )

    def get_room_type(self):
        return "Deluxe"

class SuiteRoom(Room):
    def __init__(self, room_number, location):
        super().__init__(
            room_number,
            120,
            ["Wi-Fi", "TV", "Mini Bar", "Jacuzzi"],
            location
        )

    def get_room_type(self):
        return "Suite"

    