from decorators import vip_discount
from datetime import datetime

class Booking:
    def __init__(self, customer, room, check_in, check_out):
        self.customer = customer
        self.room = room
        self.check_in = check_in
        self.check_out = check_out
        self.is_cancelled = False
        self.is_completed = False

        self.total_price = self.calculate_total()
        self.refund_amount = 0.0

    def calculate_days(self):
        return (self.check_out - self.check_in).days

    @vip_discount
    def calculate_total(self):
        return self.room.price * self.calculate_days()
    
    def cancel(self):
        self.is_cancelled = True
        print("Booking cancelled successfully.")

    def calculate_refund(self):
        today = datetime.now().date()

        total_days = self.calculate_days()

        if total_days <= 0:
            return 0

        used_days = (today - self.check_in.date()).days
        used_days = max(0, min(used_days, total_days))

        remaining_days = total_days - used_days

        daily_price = self.calculate_total() / total_days
        refund = daily_price * remaining_days * 0.8

        return round(refund, 2)