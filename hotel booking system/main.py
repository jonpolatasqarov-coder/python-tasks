from datetime import datetime
from hotel import Hotel
from room import StandardRoom, DeluxeRoom, SuiteRoom
from customer import Customer


hotel = Hotel("Grand Hotel")

room1 = StandardRoom(101, "1st Floor")
room2 = StandardRoom(102, "1st Floor")
room3 = StandardRoom(103, "1st Floor")
room4 = StandardRoom(104, "1st Floor")
room5 = StandardRoom(105, "1st Floor")

room6 = DeluxeRoom(201, "2nd Floor")
room7 = DeluxeRoom(202, "2nd Floor")
room8 = DeluxeRoom(203, "2nd Floor")
room9 = DeluxeRoom(204, "2nd Floor")
room10 = DeluxeRoom(205, "2nd Floor")

room11 = SuiteRoom(301, "3rd Floor")
room12 = SuiteRoom(302, "3rd Floor")
room13 = SuiteRoom(303, "3rd Floor")

hotel.rooms = [
    room1, room2, room3, room4, room5,
    room6, room7, room8, room9, room10,
    room11, room12, room13
]

while True:
    print()
    print("╔══════════════════════════════════════╗")
    print("║             GRAND HOTEL              ║")
    print("╠══════════════════════════════════════╣")
    print("║  1. Show Rooms                       ║")
    print("║  2. Book Room                        ║")
    print("║  3. Cancel Booking                   ║")
    print("║  4. Search Rooms                     ║")
    print("║  5. Show Booked Days                 ║")
    print("║  6. Revenue Report                   ║")
    print("║  7. View Logs                        ║")
    print("║  0. Exit                             ║")
    print("╚══════════════════════════════════════╝")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        print("\n--- ROOMS ---")

        for room in hotel.rooms:
            print(
                f"Room {room.room_number} | "
                f"{room.get_room_type()} | "
                f"${room.price}/day | "
                f"{room.location}"
            )

    elif choice == "2":
        print("\n--- BOOK ROOM ---")

        print("\nAvailable Rooms:")

        for room in hotel.rooms:
            print(
                f"Room {room.room_number} | "
                f"{room.get_room_type()} | "
                f"${room.price}/day | "
                f"{room.location}"
            )

        room_number = input("Enter room number: ").strip()

        selected_room = None

        for room in hotel.rooms:
            if str(room.room_number) == room_number:
                selected_room = room
                break

        if selected_room is None:
            print("Room not found.")
            continue

        name = input("Customer Name: ").strip()

        if not name.replace(" ", "").isalpha():
            print("Invalid customer name.")
            continue

        phone = input("Phone: ").strip()

        if not phone.replace(" ", "").isdigit():
            print("Invalid phone number.")
            continue

        vip = input("VIP Customer? (yes/no): ").strip().lower()

        if vip == "yes":
            is_vip = True
        elif vip == "no":
            is_vip = False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
            continue

        customer = Customer(name, phone, is_vip)

        check_in_text = input("Check-in date (YYYY-MM-DD): ").strip()

        try:
            check_in = datetime.strptime(check_in_text, "%Y-%m-%d")

            if len(check_in_text.split("-")[0]) != 4:
                print("Invalid year. Please enter a 4-digit year.")
                continue

        except ValueError:
            print("Invalid check-in date. Please use YYYY-MM-DD format.")
            continue

        check_out_text = input("Check-out date (YYYY-MM-DD): ").strip()

        try:
            check_out = datetime.strptime(check_out_text, "%Y-%m-%d")

            if len(check_out_text.split("-")[0]) != 4:
                print("Invalid year. Please enter a 4-digit year.")
                continue

        except ValueError:
            print("Invalid check-out date. Please use YYYY-MM-DD format.")
            continue

        hotel.book_room(
            customer,
            selected_room,
            check_in,
            check_out
        )

    elif choice == "3":
        print("\n--- CANCEL BOOKING ---")

        active_bookings = []

        for booking in hotel.bookings:
            if not booking.is_cancelled:
                active_bookings.append(booking)

        if not active_bookings:
            print("There are no active bookings.")
            continue

        print("\nACTIVE BOOKINGS")
        print("-" * 75)

        for i, booking in enumerate(active_bookings, start=1):
            days = booking.calculate_days()

            print(
                f"{i}. Room {booking.room.room_number} | "
                f"{booking.customer.name} | "
                f"{booking.check_in.date()} to {booking.check_out.date()} "
                f"({days} days)"
            )

        print("-" * 75)

        booking_number = input("Choose booking number to cancel: ").strip()

        if not booking_number.isdigit():
            print("Invalid booking number.")
            continue

        booking_number = int(booking_number)

        if booking_number < 1 or booking_number > len(active_bookings):
            print("Invalid booking number.")
            continue

        selected_booking = active_bookings[booking_number - 1]

        hotel.cancel_booking(selected_booking)

    elif choice == "4":
        print("\n--- SEARCH ROOMS ---")

        print("1. Search by Price")
        print("2. Search by Amenity")
        print("3. Search by Location")

        search_choice = input("Choose search type: ").strip()

        if search_choice == "1":
            price = input("Enter maximum price: ").strip()

            try:
                price = float(price)
            except ValueError:
                print("Invalid price.")
                continue

            rooms = hotel.filter_by_price(price)

        elif search_choice == "2":
            amenity = input("Enter amenity: ").strip()

            rooms = hotel.filter_by_amenity(amenity)

        elif search_choice == "3":
            location = input("Enter location: ").strip()

            rooms = hotel.filter_by_location(location)

        else:
            print("Invalid search option.")
            continue

        if not rooms:
            print("No rooms found.")
            continue

        print("\nSEARCH RESULTS")
        print("-" * 60)

        for room in rooms:
            print(
                f"Room {room.room_number} | "
                f"{room.get_room_type()} | "
                f"${room.price}/day | "
                f"{room.location}"
            )

        print("-" * 60)


    elif choice == "5":
        print("\n--- SHOW BOOKED DAYS ---")

        room_number = input("Enter room number: ").strip()

        if not room_number.isdigit():
            print("Invalid room number.")
            continue

        room_number = int(room_number)

        selected_room = None

        for room in hotel.rooms:
            if room.room_number == room_number:
                selected_room = room
                break

        if selected_room is None:
            print("Room not found.")
            continue

        found_booking = False

        for booking in hotel.bookings:
            if booking.room == selected_room and not booking.is_cancelled:
                days = booking.calculate_days()

                print(
                    f"Room {selected_room.room_number} is booked "
                    f"from {booking.check_in.date()} "
                    f"to {booking.check_out.date()} "
                    f"({days} days)"
                )

                found_booking = True

        if not found_booking:
            print("Room is not booked.")

    elif choice == "6":
        print("\n--- REVENUE REPORT ---")

        hotel.revenue_report()

    elif choice == "7":
        print("\n--- HOTEL LOGS ---")

        hotel.view_logs()

    elif choice == "0":
        print("Goodbye!")
        break

    else:
        print("Invalid option. Please choose a number from the menu.")