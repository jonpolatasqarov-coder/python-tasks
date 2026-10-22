import json
import logging
from datetime import datetime, timedelta
from collections import defaultdict
from booking import Booking
from customer import Customer
import os 

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

            if booking.room.room_number == room.room_number:
                if (
                    check_in < booking.check_out
                    and check_out > booking.check_in
                ):
                    return False

        return True


    def book_room(self, customer, room, check_in, check_out):
        if check_in >= check_out:
            print("Invalid booking dates.")
            return None

        if not self.is_room_available(room, check_in, check_out):
            print(
                f"Booking is not available from "
                f"{check_in.date()} to {check_out.date()}."
            )
            return None

        booking = Booking(customer, room, check_in, check_out)
        self.bookings.append(booking)

        current_day = check_in

        while current_day < check_out:
            day = current_day.date()

            if day not in room.booked_days:
                room.booked_days.append(day)

            current_day += timedelta(days=1)

        self.save_bookings()

        logging.info(
            f"Booking created: {customer.name} - "
            f"Room {room.room_number} - "
            f"{check_in.date()} to {check_out.date()}"
        )

        print("Room booked successfully.")
        return booking

    def save_rooms(self):
        rooms_data = []

        for room in self.rooms:
            rooms_data.append({
                "room_number": room.room_number,
                "room_type": room.room_type,
                "price": room.price,
                "amenities": room.amenities,
                "location": room.location,
                "is_available": room.is_available
            })

        with open("rooms.json", "w", encoding="utf-8") as file:
            json.dump(rooms_data, file, indent=4, ensure_ascii=False)


    def load_rooms(self):
        self.rooms.clear()

        try:
            with open("rooms.json", "r", encoding="utf-8") as file:
                rooms_data = json.load(file)
        except FileNotFoundError:
            print("Rooms file not found.")
            return

        from room import StandardRoom, DeluxeRoom, SuiteRoom

        for data in rooms_data:
            room_number = data["room_number"]
            room_type = data["room_type"]
            price = data["price"]
            amenities = data["amenities"]

            # Location JSON'da qanday saqlangan bo'lsa, shunday olinadi.
            location = data["location"]

            # Eski JSON'da location integer bo'lsa, matnga aylantiramiz.
            if isinstance(location, int):
                suffix = (
                    "st" if location % 10 == 1 and location % 100 != 11
                    else "nd" if location % 10 == 2 and location % 100 != 12
                    else "rd" if location % 10 == 3 and location % 100 != 13
                    else "th"
                )
                location = f"{location}{suffix} Floor"

            if room_type in [
                "Standard Single",
                "Standard Double",
                "Twin Room",
                "Family Room"
            ]:
                room = StandardRoom(
                    room_number, room_type, price, amenities, location
                )

            elif room_type == "Deluxe Double":
                room = DeluxeRoom(
                    room_number, room_type, price, amenities, location
                )

            elif room_type in [
                "Junior Suite",
                "Executive Suite",
                "Presidential Suite"
            ]:
                room = SuiteRoom(
                    room_number, room_type, price, amenities, location
                )

            else:
                continue

            # Booking mavjudligi is_available flag bilan emas,
            # bookings ro'yxatidagi sanalar orqali aniqlanadi.
            room.is_available = True
            room.booked_days = []

            self.rooms.append(room)

    def save_bookings(self):
        bookings_data = []
        customers = Customer.load_customers()

        for booking in self.bookings:
            customer_id = None

            for customer_data in customers:
                if customer_data["phone"] == booking.customer.phone:
                    customer_id = customer_data.get("customer_id")
                    break

            if customer_id is None:
                continue

            bookings_data.append({
                "customer_id": customer_id,
                "room_number": booking.room.room_number,
                "check_in": booking.check_in.isoformat(),
                "check_out": booking.check_out.isoformat(),
                "total_price": getattr(booking, "total_price", booking.calculate_total()),
                "refund_amount": getattr(booking, "refund_amount", 0),
                "is_cancelled": booking.is_cancelled,
                "is_completed": booking.is_completed
            })
        print("Saving bookings to:", os.path.abspath("bookings.json"))
        with open("bookings.json", "w", encoding="utf-8") as file:
            json.dump(
                bookings_data,
                file,
                indent=4,
                ensure_ascii=False
            )


    def load_bookings(self):
        # Method qayta chaqirilsa, takroriy bookinglar bo'lmasin.
        self.bookings.clear()

        for room in self.rooms:
            room.booked_days.clear()

        try:
            with open("bookings.json", "r", encoding="utf-8") as file:
                bookings_data = json.load(file)
        except FileNotFoundError:
            return

        for data in bookings_data:
            customer = Customer.find_by_id(data["customer_id"])

            room = None
            for item in self.rooms:
                if item.room_number == data["room_number"]:
                    room = item
                    break

            if customer is None or room is None:
                continue

            booking = Booking(
                customer,
                room,
                datetime.fromisoformat(data["check_in"]),
                datetime.fromisoformat(data["check_out"])
            )

            booking.is_cancelled = data.get("is_cancelled", False)
            booking.is_completed = data.get("is_completed", False)


            # Load saved financial data
            booking.total_price = data.get(
                "total_price", booking.calculate_total()
            )
            booking.refund_amount = data.get("refund_amount", 0.0)

            self.bookings.append(booking)

            # Bekor qilingan booking xonani band qilmaydi.
            if not booking.is_cancelled:
                current_day = booking.check_in

                while current_day < booking.check_out:
                    day = current_day.date()

                    if day not in room.booked_days:
                        room.booked_days.append(day)

                    current_day += timedelta(days=1)

    def cancel_booking(self, booking):
        if booking not in self.bookings:
            print("Booking not found.")
            return

        if booking.is_cancelled:
            print("Booking is already cancelled.")
            return

        if booking.is_completed:
            print("Completed booking cannot be cancelled.")
            return

        today = datetime.now().date()

        if booking.check_out.date() <= today:
            print("Ended booking cannot be cancelled.")
            return

        total_days = booking.calculate_days()

        if total_days <= 0:
            print("Invalid booking duration.")
            return

        used_days = max(
            0,
            min((today - booking.check_in.date()).days, total_days)
        )
        remaining_days = total_days - used_days

        if used_days > 0:
            customer = Customer.find_by_id(booking.customer.customer_id)

            if customer is not None:
                customer.add_nights(used_days)
                customer.save_customer()
                booking.customer = customer

        daily_price = booking.calculate_total() / total_days
        refund = round(daily_price * remaining_days * 0.8, 2)

        booking.refund_amount = refund
        booking.is_cancelled = True

        current_day = booking.check_in
        while current_day < booking.check_out:
            day = current_day.date()

            if day in booking.room.booked_days:
                booking.room.booked_days.remove(day)

            current_day += timedelta(days=1)

        self.save_bookings()

        logging.info(
            f"Booking cancelled: {booking.customer.name} - "
            f"Room {booking.room.room_number}"
        )

        print(f"Used nights: {used_days}")
        print(f"Unused nights: {remaining_days}")
        print(f"Refund amount: ${refund:.2f}")


    def complete_booking(self, booking):
        if booking not in self.bookings:
            print("Booking not found.")
            return

        if booking.is_cancelled:
            print("Cancelled booking cannot be completed.")
            return

        if booking.is_completed:
            print("Booking is already completed.")
            return

        if booking.check_out.date() > datetime.now().date():
            print("Booking has not ended yet.")
            return

        # JSON'dagi eng yangi mijoz ma'lumotini olamiz.
        customer = Customer.find_by_phone(booking.customer.phone)

        if customer is None:
            print("Customer not found.")
            return

        nights = booking.calculate_days()

        customer.add_nights(nights)
        customer.save_customer()

        # Booking ichidagi customer ham yangilangan bo'lsin.
        booking.customer = customer
        booking.is_completed = True

        self.save_bookings()

        logging.info(
            f"Booking completed: {customer.name} - "
            f"{nights} nights - VIP: {customer.is_vip}"
        )

        print(f"Booking completed. Nights stayed: {nights}")
        print(f"Total nights: {customer.total_nights}")

        if customer.is_vip:
            print("Congratulations! Customer has VIP status.")

    
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
        input("\nPress Enter to return to Main Menu...")

    def filter_by_price(self, max_price):
        result = []

        for room in self.rooms:
            if room.price <= max_price:
                result.append(room)

        return result


    def filter_by_amenity(self, amenity):
        result = []
        amenity = amenity.strip().lower()

        for room in self.rooms:
            for room_amenity in room.amenities:
                if amenity in room_amenity.lower():
                    result.append(room)
                    break

        return result

    def filter_by_location(self, location):
        result = []

        location = " ".join(location.lower().split())

        for room in self.rooms:
            room_location = " ".join(room.location.lower().split())

            if location in room_location:
                result.append(room)

        return result

    def view_logs(self):
        try:
            with open("hotel.log", "r", encoding="utf-8") as file:
                print(file.read())
        except FileNotFoundError:
            print("Log file not found.")