from decorators import vip_discount


class Booking:
    def __init__(self, customer, room, check_in, check_out):
        self.customer = customer
        self.room = room
        self.check_in = check_in
        self.check_out = check_out
        self.is_cancelled = False

    def calculate_days(self):
        return (self.check_out - self.check_in).days

    @vip_discount
    def calculate_total(self):
        return self.room.price * self.calculate_days()
    
    def cancel(self):
        self.is_cancelled = True
        print("Booking cancelled successfully.")

    def calculate_refund(self):
        total = self.calculate_total()
        return total * 0.8 

