from fleet_manager import FleetManager
from customer import Customer
from car import Car
from bike import Bike
from truck import Truck

fleet = FleetManager()
fleet.load_from_json("vehicles.json")
fleet.load_customers()
fleet.load_rentals()

while True:
    print("\n╔══════════════════════════════════════════╗")
    print("║            🚗 CAR RENTAL SYSTEM          ║")
    print("╠══════════════════════════════════════════╣")
    print("║  1. 🚘 Vehicle List                      ║")
    print("║  2. 🔑 Rent Vehicle                      ║")
    print("║  3. 🔄 Return Vehicle                    ║")
    print("║  4. 🔍 Search Vehicle                    ║")
    print("║  5. 👤 Register Customer                 ║")
    print("║  0. 🚪 Exit                              ║")
    print("╚══════════════════════════════════════════╝")
    choice = input("\nChoose an option: ").strip()

    if choice == "0":
        fleet.save_to_json("vehicles.json")
        print("Goodbye!")
        break

    elif choice == "1":
        while True:

            print("\n╔══════════════════════════════════════════╗")
            print("║              🚘 VEHICLE LIST             ║")
            print("╠══════════════════════════════════════════╣")
            print("║  1. 🚗 Cars                              ║")
            print("║  2. 🚚 Trucks                            ║")
            print("║  3. 🏍️ Bikes                              ║")
            print("║  0. ↩ Back                               ║")
            print("╚══════════════════════════════════════════╝")

            vehicle_choice = input("\nChoose an option: ").strip()

            if vehicle_choice == "0":
                break

            elif vehicle_choice == "1":
                
                print("\n╔════════════════════════════════════════════════════╗")
                print("║                    🚗 CARS                         ║")
                print("╠════════════════════════════════════════════════════╣")
                print("║ Name                     Price/day     Available   ║")
                print("╠════════════════════════════════════════════════════╣")

                for vehicle in fleet.vehicles:
                    if type(vehicle).__name__ == "Car":
                        status = "✓ Yes" if vehicle.is_available else "✗ No"

                        print(
                            f"║ {vehicle.name:<25}"
                            f"${vehicle.price_per_day:<13.2f}"
                            f"{status:<12}║"
                        )

                print("╚════════════════════════════════════════════════════╝")

                input("\nPress Enter to return to main menu...")
                break

            elif vehicle_choice == "2":
                print("\n╔════════════════════════════════════════════════════╗")
                print("║                   🚚 TRUCKS                        ║")
                print("╠════════════════════════════════════════════════════╣")
                print("║ Name                     Price/day     Available   ║")
                print("╠════════════════════════════════════════════════════╣")

                for vehicle in fleet.vehicles:
                    if type(vehicle).__name__ == "Truck":
                        status = "✓ Yes" if vehicle.is_available else "✗ No"

                        print(
                            f"║ {vehicle.name:<25}"
                            f"${vehicle.price_per_day:<13.2f}"
                            f"{status:<12}║"
                        )

                print("╚════════════════════════════════════════════════════╝")

                input("\nPress Enter to return to main menu...")
                break

            elif vehicle_choice == "3":
                print("\n╔════════════════════════════════════════════════════╗")
                print("║                    🏍️ BIKES                         ║")
                print("╠════════════════════════════════════════════════════╣")
                print("║ Name                     Price/day     Available   ║")
                print("╠════════════════════════════════════════════════════╣")

                for vehicle in fleet.vehicles:
                    if type(vehicle).__name__ == "Bike":
                        status = "✓ Yes" if vehicle.is_available else "✗ No"

                        print(
                            f"║ {vehicle.name:<25}"
                            f"${vehicle.price_per_day:<13.2f}"
                            f"{status:<12}║"
                        )

                print("╚════════════════════════════════════════════════════╝")
                input("\nPress Enter to return to main menu...")
                break

            else:
                print("Invalid option.")


    elif choice == "2":
        print("\n" + "╔" + "═" * 42 + "╗")
        print("║              🔑 RENT VEHICLE             ║")
        print("╠" + "═" * 42 + "╣")
        print("║          Select a Customer First         ║")
        print("╚" + "═" * 42 + "╝")

        if not fleet.customers:
            print("No registered customers. Register first.")
            continue

        while True:
            customer_input = input(
                "Enter your Customer ID (0 to go back): "
            ).strip()

            if customer_input == "0":
                break

            if not customer_input.isdigit():
                print("Invalid Customer ID.")
                continue

            customer_id = int(customer_input)

            customer = None

            for existing_customer in fleet.customers:
                if existing_customer.customer_id == customer_id:
                    customer = existing_customer
                    break

            if customer is None:
                print("Customer not found.")
                continue

            break
        else:
            continue

        if customer is None:
            continue

        # Show available vehicles
        print("\nAvailable Vehicles")
        print(
            f"\n{'No.':<5}"
            f"{'Name':<25}"
            f"{'Type':<13}"
            f"{'Price/day':>12}"
        )
        print("-" * 60)

        available_vehicles = [
            vehicle for vehicle in fleet.vehicles
            if vehicle.is_available
        ]

        if not available_vehicles:
            print("No vehicles available.")
            continue

        for index, vehicle in enumerate(available_vehicles, start=1):
            print(
                f"{index:<5}"
                f"{vehicle.name:<25}"
                f"{type(vehicle).__name__:<13}"
                f"${vehicle.price_per_day:>10.2f}"
            )

        # Select vehicle
        while True:
            name = input(
                "\nEnter vehicle name (0 to go back): "
            ).strip()

            if name == "0":
                break

            vehicle = fleet.search_by_name(name)

            if vehicle is None:
                print("Vehicle not found. Try again.")
                continue

            if not vehicle.is_available:
                print(f"{vehicle.name} is not available.")
                continue

            break

        if name == "0":
            continue

        # Select rental duration
        while True:
            days_input = input(
                "Enter rental days (0 to go back): "
            ).strip()

            if days_input == "0":
                break

            if not days_input.isdigit():
                print("Enter a valid number of days.")
                continue

            days = int(days_input)

            if isinstance(vehicle, Car):
                max_days = 30
            elif isinstance(vehicle, Bike):
                max_days = 14
            elif isinstance(vehicle, Truck):
                max_days = 50

            if days < 1 or days > max_days:
                print(
                    f"Rental period must be between "
                    f"1 and {max_days} days."
                )
                continue

            success = fleet.rent_vehicle(
                name, days, customer_id
            )

            if success:
                fleet.save_to_json("vehicles.json")

            break

    elif choice == "3":
        print("\n" + "╔" + "═" * 42 + "╗")
        print("║              🔄 RETURN VEHICLE           ║")
        print("╚" + "═" * 42 + "╝")

        if not fleet.customers:
            print("No registered customers.")
            continue

        customer = None

        while True:
            customer_input = input(
                "Enter your Customer ID (0 to go back): "
            ).strip()

            if customer_input == "0":
                break

            if not customer_input.isdigit():
                print("Invalid Customer ID.")
                continue

            customer_id = int(customer_input)

            for existing_customer in fleet.customers:
                if existing_customer.customer_id == customer_id:
                    customer = existing_customer
                    break

            if customer is None:
                print("Customer not found.")
                continue

            break

        if customer is None:
            continue

        active_rentals = [
            rental for rental in fleet.rentals
            if rental["customer_id"] == customer_id
            and not rental["returned"]
        ]

        if not active_rentals:
            print("You have no active rentals.")
            continue

        print("\nYour Active Rentals:")

        for rental in active_rentals:
            print(
                f"- {rental['vehicle_name']} "
                f"({rental['vehicle_type']}) | "
                f"Due: {rental['return_date']}"
            )

        name = input(
            "\nEnter vehicle name to return (0 to go back): "
        ).strip()

        if name == "0":
            continue

        fleet.return_vehicle(name, customer_id)



    elif choice == "4":
        while True:
            print("\n╔══════════════════════════════════════════╗")
            print("║              🔍 SEARCH VEHICLE           ║")
            print("╠══════════════════════════════════════════╣")
            print("║  1. 👤 Search by Name                    ║")
            print("║  2. 🚘 Search by Type                    ║")
            print("║  3. 💰 Search by Price                   ║")
            print("║  0. ↩️  Back                              ║")
            print("╚══════════════════════════════════════════╝")

            search_choice = input("\nChoose an option (0 to go back): ").strip()

            if search_choice == "0":
                break

            elif search_choice == "1":
                name = input("Enter vehicle name (0 to go back): ").strip()

                if name == "0":
                    continue

                vehicle = fleet.search_by_name(name)

                if vehicle:
                    status = "✓ Yes" if vehicle.is_available else "✗ No"

                    print("\n╔════════════════════════════════════════════════════╗")
                    print("║                  🔍 SEARCH RESULT                  ║")
                    print("╠════════════════════════════════════════════════════╣")
                    print("║ Name                    Type      Price   Available║")
                    print("╠════════════════════════════════════════════════════╣")
                    print(
                        f"║ {vehicle.name:<25}"
                        f"{type(vehicle).__name__:<9}"
                        f"${vehicle.price_per_day:<7.2f}"
                        f"{status:<9}║"
                    )
                    print("╚════════════════════════════════════════════════════╝")
                else:
                    print("\n❌ Vehicle not found.")

            elif search_choice == "2":
                vehicle_type = input("Enter vehicle type (0 to go back): ").strip()

                if vehicle_type == "0":
                    continue

                results = fleet.search_by_type(vehicle_type)

                if results:
                    print("\n╔════════════════════════════════════════════════════╗")
                    print("║                  🔍 SEARCH RESULT                  ║")
                    print("╠════════════════════════════════════════════════════╣")
                    print("║ Name                    Type     Price   Available ║")
                    print("╠════════════════════════════════════════════════════╣")

                    for vehicle in results:
                        status = "✓ Yes" if vehicle.is_available else "✗ No"
                        print(
                            f"║ {vehicle.name:<25}"
                            f"{type(vehicle).__name__:<9}"
                            f"${vehicle.price_per_day:<7.2f}"
                            f"{status:<9}║"
                        )

                    print("╚════════════════════════════════════════════════════╝")
                else:
                    print("\n❌ No vehicles found.")

            elif search_choice == "3":
                price_input = input("Enter maximum price (0 to go back): ").strip()

                if price_input == "0":
                    continue

                try:
                    max_price = float(price_input)

                    if max_price < 0:
                        print("Price cannot be negative.")
                        continue

                except ValueError:
                    print("Please enter a valid price.")
                    continue

                results = fleet.search_by_price(max_price)

                if results:
                    print("\n╔════════════════════════════════════════════════════╗")
                    print("║                  🔍 SEARCH RESULT                  ║")
                    print("╠════════════════════════════════════════════════════╣")
                    print("║ Name                    Type     Price   Available ║")
                    print("╠════════════════════════════════════════════════════╣")

                    for vehicle in results:
                        status = "✓ Yes" if vehicle.is_available else "✗ No"
                        print(
                            f"║ {vehicle.name:<25}"
                            f"{type(vehicle).__name__:<9}"
                            f"${vehicle.price_per_day:<7.2f}"
                            f"{status:<9}║"
                        )

                    print("╚════════════════════════════════════════════════════╝")
                else:
                    print("\n❌ No vehicles found.")

            else:
                print("Invalid option. Please choose 0, 1, 2, or 3.")


    elif choice == "5":
        while True:
            name = input(
                "Enter first and last name (0 to go back): "
            ).strip()

            if name == "0":
                break

            name_parts = name.split()

            if (
                len(name_parts) >= 2
                and all(
                    part.replace("'", "").replace("‘", "").replace("’", "").isalpha()
                    for part in name_parts
                )
            ):
                name = " ".join(name_parts).title()
                break

            print(
                "Invalid name. Enter first and last name using letters only."
            )

        if name == "0":
            continue

        while True:
            phone = input(
                "Enter phone number (e.g. +998 99-123-45-67, 0 to go back): "
            ).strip()

            if phone == "0":
                break

            digits = phone.replace("+998", "").replace(" ", "").replace("-", "")

            if len(digits) != 9 or not digits.isdigit():
                print("Invalid phone number. Enter exactly 9 digits.")
                continue

            phone = f"+998 {digits[:2]}-{digits[2:5]}-{digits[5:7]}-{digits[7:]}"

            customer_id = len(fleet.customers) + 1
            customer = Customer(customer_id, name, phone)

            if fleet.add_customer(customer):
                fleet.save_customers()
                print("Customer registered successfully!")
                print(f"Customer ID: {customer_id}")
                print(f"Phone: {phone}")
                break

            print("Please enter a different phone number.")

        if phone == "0":
            continue



    else:
        print("Invalid option.")