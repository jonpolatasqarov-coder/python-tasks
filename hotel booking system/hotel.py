import logging
from datetime import timedelta
from collections import defaultdict
from booking import Booking


logging.basicConfig(
    filename="hotel.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)


class Hotel:
    def __init__(self, name):
        self.name = name
        self.rooms = []
        self.bookings = []

    def is_room_available(self, room, check_in, check_out):
        for booking in self.bookings:
            if booking.is_cancelled:
                continue
            if booking.room == room:
                if check_in < booking.check_out and check_out > booking.check_in:
                    return False

        return True

    def book_room(self, customer, room, check_in, check_out):
        if check_in >= check_out:
            print("Invalid booking dates.")
            return
         
        if not self.is_room_available(room, check_in, check_out):
            print("Room is not available.")
            return

        booking = Booking(customer, room, check_in, check_out)
        self.bookings.append(booking)

        current_day = check_in
        while current_day < check_out:
            room.booked_days.append(current_day.date())
            current_day += timedelta(days=1)

        logging.info(
            f"Booking created: {customer.name} - Room {room.room_number} - "
            f"{check_in.date()} to {check_out.date()}"
        )

        print("Room booked successfully.")

        return booking


    def cancel_booking(self, booking):
        if booking not in self.bookings:
            print("Booking not found.")
            return

        if booking.is_cancelled:
            print("Booking is already cancelled.")
            return

        booking.cancel()
        current_day = booking.check_in

        while current_day < booking.check_out:
            day = current_day.date()

            if day in booking.room.booked_days:
                booking.room.booked_days.remove(day)

            current_day += timedelta(days=1)

        logging.info(
            f"Booking cancelled: {booking.customer.name} - "
            f"Room {booking.room.room_number}"
        )

        refund = booking.calculate_refund()

        print(f"Refund amount: ${refund}")

    def revenue_report(self):
        daily_revenue = defaultdict(float)
        monthly_revenue = defaultdict(float)

        for booking in self.bookings:
            total = booking.calculate_total()

            if booking.is_cancelled:
                total = total * 0.2

            days = booking.calculate_days()

            if days == 0:
                continue

            daily_amount = total / days

            current_day = booking.check_in

            while current_day < booking.check_out:
                day = current_day.date()
                month = current_day.strftime("%Y-%m")

                daily_revenue[day] += daily_amount
                monthly_revenue[month] += daily_amount

                current_day += timedelta(days=1)

        print("\nDAILY REVENUE")
        print("-" * 32)
        print(f"{'Date':<15} Revenue")
        print("-" * 32)

        total_daily = 0

        for day in sorted(daily_revenue):
            revenue = daily_revenue[day]
            print(f"{str(day):<15} ${revenue:.2f}")
            total_daily += revenue

        print("-" * 32)
        print(f"Total Daily Revenue: ${total_daily:.2f}")

        print("\nMONTHLY REVENUE")
        print("-" * 32)
        print(f"{'Month':<15} Revenue")
        print("-" * 32)

        total_monthly = 0

        for month in sorted(monthly_revenue):
            revenue = monthly_revenue[month]
            print(f"{month:<15} ${revenue:.2f}")
            total_monthly += revenue

        print("-" * 32)
        print(f"Total Revenue: ${total_monthly:.2f}")

    def filter_by_price(self, max_price):
        result = []

        for room in self.rooms:
            if room.price <= max_price:
                result.append(room)

        return result

    def filter_by_amenity(self, amenity):
        result = []

        for room in self.rooms:
            for room_amenity in room.amenities:
                if amenity.lower() == room_amenity.lower():
                    result.append(room)
                    break

        return result

    def filter_by_location(self, location):
        result = []

        location = " ".join(location.lower().split())

        for room in self.rooms:
            room_location = " ".join(room.location.lower().split())

            if room_location == location:
                result.append(room)

        return result

    def view_logs(self):
        try:
            with open("hotel.log", "r", encoding="utf-8") as file:
                print(file.read())
        except FileNotFoundError:
            print("Log file not found.")