from datetime import datetime, timedelta
from hotel import Hotel
from customer import Customer


hotel = Hotel("Grand Hotel")
hotel.load_rooms()
hotel.load_bookings()

while True:
    print()
    print("╔══════════════════════════════════════╗")
    print("║             GRAND HOTEL              ║")
    print("╠══════════════════════════════════════╣")
    print("║  1. Show Rooms                       ║")
    print("║  2. Reception                        ║")
    print("║  3. Book Room                        ║")
    print("║  4. Cancel Booking                   ║")
    print("║  5. Search Rooms                     ║")
    print("║  6. Show Booked Days                 ║")
    print("║  7. Revenue Report                   ║")
    print("║  8. View Logs                        ║")
    print("║  9. Complete Booking                 ║")
    print("║  0. Exit                             ║")
    print("╚══════════════════════════════════════╝")

    choice = input("Choose an option: ").strip()


    if choice == "1":
        print("\n" + "=" * 92)
        print(" " * 35 + "GRAND HOTEL")
        print(" " * 37 + "ROOMS")
        print("=" * 92)

        print(
            f"{'No.':<5}"
            f"{'Room':<10}"
            f"{'Room Type':<25}"
            f"{'Price/Night':<16}"
            f"{'Location':<18}"
            f"{'Available':<12}"
        )

        print("-" * 92)

        today = datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        tomorrow = today + timedelta(days=1)

        for i, room in enumerate(hotel.rooms, start=1):
            available_today = hotel.is_room_available(
                room, today, tomorrow
            )

            availability = "Yes" if available_today else "No"

            print(
                f"{i:<5}"
                f"{room.room_number:<10}"
                f"{room.get_room_type():<25}"
                f"${room.price:<15}"
                f"{room.location:<18}"
                f"{availability:<12}"
            )

        print("=" * 92)
        print(f"Total Rooms: {len(hotel.rooms)}")
        print("-" * 92)

        input("\nPress Enter to return to the main menu...")


    elif choice == "2":
        print("\n--- RECEPTION ---")

        while True:
            print("\n1. Register New Customer")
            print("2. Find Customer by ID")
            print("0. Back to Main Menu")

            reception_choice = input(
                "Choose an option: "
            ).strip()

            if reception_choice == "":
                print("Please choose an option: 1, 2, or 0.")
                continue

            # Back to main menu
            if reception_choice == "0":
                break

            # Register a new customer
            elif reception_choice == "1":
                print("\n--- REGISTER NEW CUSTOMER ---")

                # Enter customer name
                while True:
                    name = input(
                        "Customer name (0 to go back): "
                    ).strip().title()

                    if name == "0":
                        break

                    if not name:
                        print("Name cannot be empty.")
                        continue

                    clean_name = name.replace(" ", "").replace("'", "").replace("-", "")

                    if not clean_name.isalpha():
                        print("Invalid name. Use letters, spaces, apostrophes or hyphens.")
                        continue

                    break

                if name == "0":
                    continue

                # Enter phone number
                while True:
                    phone = input(
                        "Phone number (digits only, 0 to go back): "
                    ).strip()

                    if phone == "0":
                        break

                    # Remove spaces
                    phone = phone.replace("+", "").replace(" ", "").replace("-", "")

                    if not phone.isdigit():
                        print("Invalid phone number. Enter a valid phone number.")
                        continue

                    if not 7 <= len(phone) <= 15:
                        print("Phone number must contain 7 to 15 digits.")
                        continue

                    existing_customer = Customer.find_by_phone(phone)

                    if existing_customer is not None:
                        print(
                            "\nThis phone number is already registered."
                        )

                        customers = Customer.load_customers()

                        for data in customers:
                            if data["phone"] == phone:
                                print(
                                    f"Customer ID: "
                                    f"{data['customer_id']}"
                                )
                                print(f"Name: {data['name']}")
                                print(f"Phone: {data['phone']}")
                                break

                        break

                    customer = Customer(name, phone)
                    customer.save_customer()

                    customers = Customer.load_customers()

                    for data in customers:
                        if data["phone"] == phone:
                            print(
                                "\nCustomer registered successfully!"
                            )
                            print(
                                f"Customer ID: {data['customer_id']}"
                            )
                            print(f"Name: {data['name']}")
                            print(f"Phone: {data['phone']}")
                            print("VIP: No")
                            print(
                                "Please remember the customer ID "
                                "for future bookings."
                            )
                            break

                    break

            # Find an existing customer
            elif reception_choice == "2":
                print("\n--- FIND CUSTOMER ---")

                while True:
                    customer_id_text = input(
                        "Enter customer ID (0 to go back): "
                    ).strip()

                    if customer_id_text == "0":
                        break

                    if not customer_id_text:
                        print("Customer ID cannot be empty.")
                        continue

                    if not customer_id_text.isdigit():
                        print("Invalid ID. Enter numbers only.")
                        continue

                    customer_id = int(customer_id_text)
                    customer = Customer.find_by_id(customer_id)

                    if customer is None:
                        print("Customer not found. Please try again.")
                        continue

                    print("\n--- CUSTOMER DETAILS ---")
                    print(f"ID: {customer_id}")
                    print(f"Name: {customer.name}")
                    print(f"Phone: {customer.phone}")
                    print(
                        f"VIP: {'Yes' if customer.is_vip else 'No'}"
                    )
                    print(
                        f"Total nights stayed: "
                        f"{customer.total_nights}"
                    )
                    break

            else:
                print("Invalid option. Please choose 1, 2, or 0.")


    elif choice == "3":
        print("\n--- BOOK ROOM ---")

        # 1. Find customer
        while True:
            customer_id_text = input(
                "Enter customer ID (0 to go back): "
            ).strip()

            if customer_id_text == "0":
                break

            if not customer_id_text.isdigit():
                print("Invalid ID. Enter numbers only.")
                continue

            customer_id = int(customer_id_text)
            customer = Customer.find_by_id(customer_id)

            if customer is None:
                print(
                    "Customer not found. "
                    "Please register at Reception first."
                )
                continue

            break

        if customer_id_text == "0":
            continue

        print(f"\nWelcome, {customer.name}!")

        if customer.is_vip:
            print("VIP discount: 10%")

        # 2. Select room
        while True:

            print("\n" + "=" * 92)
            print(" " * 34 + "AVAILABLE ROOMS")
            print("=" * 92)

            print(
                f"{'No.':<5}"
                f"{'Room':<10}"
                f"{'Room Type':<25}"
                f"{'Price/Night':<16}"
                f"{'Location':<18}"
                f"{'Available':<12}"
            )

            print("-" * 92)

            today = datetime.now().replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0
            )
            tomorrow = today + timedelta(days=1)

            for i, room in enumerate(hotel.rooms, start=1):
                available_today = hotel.is_room_available(
                    room, today, tomorrow
                )

                status = "Yes" if available_today else "No"

                print(
                    f"{i:<5}"
                    f"{room.room_number:<10}"
                    f"{room.get_room_type():<25}"
                    f"${room.price:<15}"
                    f"{room.location:<18}"
                    f"{status:<12}"
                )

            print("=" * 92)

            room_number_text = input(
                "\nEnter room number (0 to go back): "
            ).strip()


            if room_number_text == "0":
                break

            if not room_number_text.isdigit():
                print("Invalid room number. Enter digits only.")
                continue

            room_number = int(room_number_text)

            selected_room = None

            for room in hotel.rooms:
                if room.room_number == room_number:
                    selected_room = room
                    break

            if selected_room is None:
                print("Room not found. Please try again.")
                continue

            today = datetime.now().replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0
            )

            tomorrow = today + timedelta(days=1)

            if not hotel.is_room_available(selected_room, today, tomorrow):
                print(f"Room {selected_room.room_number} is not available today.")
                continue

            # 3. Choose number of nights
            while True:
                nights_text = input(
                    "Number of nights (1-30, 0 to go back): "
                ).strip()

                if nights_text == "0":
                    break

                if not nights_text.isdigit():
                    print("Invalid input. Enter a whole number.")
                    continue

                nights = int(nights_text)

                if not 1 <= nights <= 30:
                    print("You can book from 1 to 30 nights.")
                    continue

                break

            if nights_text == "0":
                break

            # 4. Set check-in and check-out dates
            check_in = datetime.now().replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0
            )

            check_out = check_in + timedelta(days=nights)

            # 5. Check room availability
            if not hotel.is_room_available(
                selected_room, check_in, check_out
            ):
                print(
                    f"\nRoom {selected_room.room_number} is not "
                    f"available from {check_in.date()} "
                    f"to {check_out.date()}."
                )
                print("Please choose another room.")
                continue

            # 6. Calculate total price
            total = selected_room.price * nights

            if customer.is_vip:
                total *= 0.9

            # 7. Show booking summary
            print("\n" + "=" * 40)
            print("          BOOKING SUMMARY")
            print("=" * 40)
            print(f"Customer: {customer.name}")
            print(f"Room: {selected_room.room_number}")
            print(f"Room type: {selected_room.get_room_type()}")
            print(f"Check-in: {check_in.date()}")
            print(f"Check-out: {check_out.date()}")
            print(f"Nights: {nights}")
            print(f"Total price: ${total:,.2f}")
            print("=" * 40)

            # 8. Confirm booking
            while True:
                confirm = input(
                    "Confirm booking? (yes/no): "
                ).strip().lower()

                if confirm in ("yes", "y"):
                    booking = hotel.book_room(
                        customer,
                        selected_room,
                        check_in,
                        check_out
                    )

                    if booking is not None:
                        print("\n" + "=" * 40)
                        print("    BOOKING CONFIRMED SUCCESSFULLY")
                        print("=" * 40)
                        print(f"Customer: {customer.name}")
                        print(f"Room: {selected_room.room_number}")
                        print(f"Check-in: {check_in.date()}")
                        print(f"Check-out: {check_out.date()}")
                        print(f"Total price: ${total:,.2f}")
                        print(
                            f"Have a pleasant stay, "
                            f"dear {customer.name}!"
                        )
                        print("=" * 40)

                    break

                elif confirm in ("no", "n"):
                    print("Booking cancelled. No room was booked.")
                    break

                else:
                    print("Please enter yes or no.")

            break

    elif choice == "4":
        print("\n--- CANCEL BOOKING ---")

        # 1. Identify customer
        while True:
            customer_id_text = input(
                "Enter your Customer ID (0 to go back): "
            ).strip()

            if customer_id_text == "0":
                break

            if not customer_id_text.isdigit():
                print("Invalid ID. Enter numbers only.")
                continue

            customer_id = int(customer_id_text)
            customer = Customer.find_by_id(customer_id)

            if customer is None:
                print("Customer not found. Please try again.")
                continue

            break

        if customer_id_text == "0":
            continue

        print(f"\nWelcome, {customer.name}!")

        # 2. Find this customer's active bookings
        today = datetime.now().date()

        active_bookings = [
            booking for booking in hotel.bookings
            if booking.customer.customer_id == customer_id
            and not booking.is_cancelled
            and not booking.is_completed
            and booking.check_out.date() > today
        ]

        if not active_bookings:
            print("You have no active bookings to cancel.")
            continue

        # 3. Display bookings
        print("\n" + "=" * 75)
        print(" " * 25 + "YOUR ACTIVE BOOKINGS")
        print("=" * 75)

        for i, booking in enumerate(active_bookings, start=1):
            days = booking.calculate_days()

            print(
                f"{i}. Room {booking.room.room_number} | "
                f"{booking.check_in.date()} to "
                f"{booking.check_out.date()} | "
                f"{days} nights"
            )

        print("=" * 75)

        # 4. Select booking
        booking_number = input(
            "Choose booking number to cancel (0 to go back): "
        ).strip()

        if booking_number == "0":
            continue

        if not booking_number.isdigit():
            print("Invalid booking number.")
            continue

        booking_number = int(booking_number)

        if not 1 <= booking_number <= len(active_bookings):
            print("Invalid booking number.")
            continue

        selected_booking = active_bookings[booking_number - 1]

        # 5. Confirm cancellation
        while True:
            confirm = input(
                "Are you sure you want to cancel this booking? (yes/no): "
            ).strip().lower()

            if confirm in ("yes", "y"):
                hotel.cancel_booking(selected_booking)
                break

            elif confirm in ("no", "n"):
                print("Booking cancellation aborted.")
                break

            else:
                print("Please enter yes or no.")

    elif choice == "5":
        while True:
            print("\n" + "=" * 44)
            print(" " * 13 + "SEARCH ROOMS")
            print("=" * 44)

            print("  1. Search by Price")
            print("  2. Search by Amenity")
            print("  3. Search by floor")
            print("  0. Back to Main Menu")
            print("-" * 44)

            search_choice = input("Choose search type: ").strip()

            if search_choice == "0":
                break

            elif search_choice == "1":
                price_text = input("Enter maximum price ($): ").strip()

                try:
                    price = float(price_text)

                    if price < 0:
                        print("Price cannot be negative.")
                        continue

                except ValueError:
                    print("Invalid price. Enter a number.")
                    continue

                rooms = hotel.filter_by_price(price)

            elif search_choice == "2":
                amenity = input("Enter amenity to search: ").strip()

                if not amenity:
                    print("Amenity cannot be empty.")
                    continue

                rooms = hotel.filter_by_amenity(amenity)

            elif search_choice == "3":
                location = input(
                    "Enter floor (e.g. 1st Floor): "
                ).strip()

                if not location:
                    print("Location cannot be empty.")
                    continue

                rooms = hotel.filter_by_location(location)

            else:
                print("Invalid option. Choose 0, 1, 2, or 3.")
                continue

            if not rooms:
                print("\nNo rooms found matching your search.")
                input("Press Enter to search again...")
                continue

            print("\nSEARCH RESULTS")
            print("-" * 60)

            for room in rooms:
                status = "Available" if room.is_available else "Not Available"

                print(
                    f"Room {room.room_number} | "
                    f"{room.get_room_type()} | "
                    f"${room.price}/day | "
                    f"{room.location}| "
                    f"Status: {status}"
                )

                if search_choice == "2":
                    print(f"Amenities: {', '.join(room.amenities)}")

                print("-" * 60)

            print(f"Total rooms found: {len(rooms)}")
            input("\nPress Enter to search again...")

    elif choice == "6":
        while True:
            print("\n" + "=" * 50)
            print(" " * 15 + "SHOW BOOKED DAYS")
            print("=" * 50)

            booked_rooms = {}

            for booking in hotel.bookings:
                if booking.is_cancelled:
                    continue

                current_day = booking.check_in.date()
                check_out = booking.check_out.date()

                while current_day < check_out:
                    room_number = booking.room.room_number

                    if room_number not in booked_rooms:
                        booked_rooms[room_number] = set()

                    booked_rooms[room_number].add(current_day)
                    current_day += timedelta(days=1)

            if not booked_rooms:
                print("No booked days found.")
                break

            print("\nRooms with booking history:")
            print("-" * 50)

            for room_number in sorted(booked_rooms):
                print(f"Room {room_number}")

            print("-" * 50)
            print("0. Back to Main Menu")

            room_input = input(
                "\nEnter room number to view booked days: "
            ).strip()

            if room_input == "0":
                break

            selected_room = next(
                (
                    room for room in hotel.rooms
                    if str(room.room_number) == room_input
                ),
                None
            )

            if selected_room is None:
                print("Room not found.")
                continue

            room_number = selected_room.room_number

            if room_number not in booked_rooms:
                print("This room has no booking history.")
                continue

            booked_days = sorted(booked_rooms[room_number])
            today = datetime.now().date()

            print(f"\nBooked days for Room {room_number}:")
            print("-" * 60)

            for day in booked_days:
                if day < today:
                    status = "PAST"
                else:
                    status = "UPCOMING"

                print(f"{day.strftime('%Y-%m-%d')} | {status}")

            print("-" * 60)
            print(f"Total booked days: {len(booked_days)}")

            input("\nPress Enter to return to the room list...")

    elif choice == "7":
        print("\n--- REVENUE REPORT ---")

        hotel.revenue_report()



    elif choice == "8":
        print("\n" + "=" * 100)
        print(" " * 38 + "HOTEL ACTIVITY LOGS")
        print("=" * 100)

        log_file = "hotel.log"

        try:
            with open(log_file, "r", encoding="utf-8") as file:
                log_lines = file.readlines()

            if not log_lines:
                print("No logs available.")

            else:
                print(
                    f"{'DATE':<12} "
                    f"{'TIME':<10} "
                    f"{'ACTION':<12} "
                    f"{'CUSTOMER':<18} "
                    f"{'ROOM':<8} "
                    f"{'DETAILS'}"
                )
                print("-" * 100)

                count = 0

                for line in log_lines:
                    line = line.strip()

                    if not line:
                        continue

                    try:
                        timestamp, message = line.split(" - ", 1)
                        date, time = timestamp.split(" ", 1)
                        time = time.split(",")[0]

                        if message.startswith("Booking created: "):
                            action = "BOOKED"
                            details = message.replace(
                                "Booking created: ", "", 1
                            )

                        elif message.startswith("Booking cancelled: "):
                            action = "CANCELLED"
                            details = message.replace(
                                "Booking cancelled: ", "", 1
                            )

                        else:
                            action = "OTHER"
                            details = message

                        customer = "-"
                        room = "-"
                        booking_dates = details

                        if " - Room " in details:
                            customer, remaining = details.split(
                                " - Room ", 1
                            )
                            room, separator, dates = remaining.partition(
                                " - "
                            )

                            if separator:
                                booking_dates = dates
                            else:
                                booking_dates = "-"

                        print(
                            f"{date:<12} "
                            f"{time:<10} "
                            f"{action:<12} "
                            f"{customer[:17]:<18} "
                            f"{room:<8} "
                            f"{booking_dates}"
                        )

                        count += 1

                    except ValueError:
                        print(f"Could not read log entry: {line}")

                print("-" * 100)
                print(f"Total log entries: {count}")

        except FileNotFoundError:
            print("Log file not found.")

        input("\nPress Enter to return to Main Menu...")

    elif choice == "9":
        print("\n" + "=" * 50)
        print(" " * 15 + "COMPLETE BOOKING")
        print("=" * 50)

        customer_id_input = input(
            "Enter your customer ID (0 to go back): "
        ).strip()

        if customer_id_input == "0":
            continue

        if not customer_id_input.isdigit():
            print("Invalid customer ID.")
            continue

        customer_id = int(customer_id_input)
        customer = Customer.find_by_id(customer_id)

        if customer is None:
            print("Customer not found.")
            continue

        today = datetime.now().date()

        customer_bookings = [
            booking for booking in hotel.bookings
            if booking.customer.customer_id == customer_id
            and not booking.is_cancelled
            and not booking.is_completed
        ]

        if not customer_bookings:
            print("You have no active bookings.")
            continue

        print(f"\nBookings for {customer.name}:")
        print("-" * 70)

        for index, booking in enumerate(customer_bookings, start=1):
            status = (
                "ENDED"
                if booking.check_out.date() <= today
                else "NOT ENDED"
            )

            print(
                f"{index}. Room {booking.room.room_number} | "
                f"{booking.check_in.date()} to "
                f"{booking.check_out.date()} | "
                f"{status}"
            )

        print("-" * 70)

        booking_input = input(
            "Choose booking number (0 to go back): "
        ).strip()

        if booking_input == "0":
            continue

        if not booking_input.isdigit():
            print("Invalid booking number.")
            continue

        booking_index = int(booking_input)

        if not 1 <= booking_index <= len(customer_bookings):
            print("Booking number not found.")
            continue

        selected_booking = customer_bookings[booking_index - 1]

        if selected_booking.check_out.date() > today:
            print("Booking has not ended yet.")
            continue

        hotel.complete_booking(selected_booking)


    elif choice == "0":
        print("Goodbye!")
        break

    else:
        print("Invalid option. Please choose a number from the menu.")