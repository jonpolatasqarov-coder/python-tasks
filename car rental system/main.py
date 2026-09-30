import os

from fleet_manager import FleetManager
 

fleet = FleetManager()

if os.path.exists("vehicles.json"):
    fleet.load_from_json("vehicles.json")
else:
    fleet.load_initial_fleet("fleet.json")

while True:
    print("\n╔══════════════════════════════════════════╗")
    print("║            🚗 CAR RENTAL SYSTEM          ║")
    print("╠══════════════════════════════════════════╣")
    print("║  1. 🚘 Vehicle List                      ║")
    print("║  2. 🔑 Rent Vehicle                      ║")
    print("║  3. 🔄 Return Vehicle                    ║")
    print("║  4. 🔍 Search Vehicle                    ║")
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
        print("\n╔══════════════════════════════════════════╗")
        print("║              🔑 RENT VEHICLE             ║")
        print("╠══════════════════════════════════════════╣")
        print("║          Available Vehicles              ║")
        print("╚══════════════════════════════════════════╝")

        print()

        print(f"{'No.':<5}{'Name':<25}{'Type':<12}{'Price/day':>10}")
        print("-" * 52)

        number = 1

        for vehicle in fleet.vehicles:
            if vehicle.is_available:
                print(
                    f"{number:<5}"
                    f"{vehicle.name:<25}"
                    f"{type(vehicle).__name__:<12}"
                    f"${vehicle.price_per_day:>9.2f}"
                )
                number += 1

        print()

        name = input("Enter vehicle name: ").strip()

        try:
            days = int(input("Enter rental days: ").strip())
        except ValueError:
            print("Please enter a valid number.")
            continue

        fleet.rent_vehicle(name, days)
        fleet.save_to_json("vehicles.json")

    elif choice == "3":
        print("\n╔══════════════════════════════════════════╗")
        print("║             🔄 RETURN VEHICLE            ║")
        print("╠══════════════════════════════════════════╣")
        print("║          🚘 Rented Vehicles              ║")
        print("╚══════════════════════════════════════════╝")

        print()

        rented_vehicles = []

        for vehicle in fleet.vehicles:
            if not vehicle.is_available:
                rented_vehicles.append(vehicle)

        if rented_vehicles:
            print(f"{'No.':<5}{'Name':<25}{'Type':<12}{'Price/day':>10}")
            print("-" * 52)

            for number, vehicle in enumerate(rented_vehicles, start=1):
                print(
                    f"{number:<5}"
                    f"{vehicle.name:<25}"
                    f"{type(vehicle).__name__:<12}"
                    f"${vehicle.price_per_day:>9.2f}"
                )

            print()

            name = input("Enter vehicle name: ").strip()

            fleet.return_vehicle(name)
            fleet.save_to_json("vehicles.json")

        else:
            print("No vehicles are currently rented.")

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

            search_choice = input("\nChoose an option: ").strip()

            if search_choice == "0":
                break

            elif search_choice == "1":
                name = input("Enter vehicle name: ").strip()

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
                vehicle_type = input("Enter vehicle type: ").strip()

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
                try:
                    max_price = float(input("Enter maximum price: ").strip())
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
        print("Invalid option.")