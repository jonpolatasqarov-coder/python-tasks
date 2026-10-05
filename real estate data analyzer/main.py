from analyzer import RealEstateAnalyzer
from strategies import (
    PriceFilter,
    AreaFilter,
    DistrictFilter,
    RoomFilter
)
from visualizer import RealEstateVisualizer


analyzer = RealEstateAnalyzer("properties.csv")
visualizer = RealEstateVisualizer(analyzer.df)


while True:
    print("\n===== REAL ESTATE ANALYZER =====")
    print("1. Filter by price")
    print("2. Filter by area")
    print("3. Filter by district")
    print("4. Filter by rooms")
    print("5. Average price by district")
    print("6. Property count by district")
    print("7. Price vs area")
    print("8. Predict property price")
    print("0. Exit")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        max_price = float(input("Enter maximum price: "))

        result = analyzer.apply_filter(
            PriceFilter(max_price)
        )

        print("\nFiltered properties:")
        print(result)

        filename = input("Enter Excel filename: ")
        analyzer.export_to_excel(result, filename)

        print(f"Exported to {filename}")

    elif choice == "2":
        min_area = float(input("Enter minimum area: "))

        result = analyzer.apply_filter(
            AreaFilter(min_area)
        )

        print("\nFiltered properties:")
        print(result)

        filename = input("Enter Excel filename: ")
        analyzer.export_to_excel(result, filename)

        print(f"Exported to {filename}")

    elif choice == "3":
        district = input("Enter district: ")

        result = analyzer.apply_filter(
            DistrictFilter(district)
        )

        print("\nFiltered properties:")
        print(result)

        filename = input("Enter Excel filename: ")
        analyzer.export_to_excel(result, filename)

        print(f"Exported to {filename}")

    elif choice == "4":
        rooms = int(input("Enter number of rooms: "))

        result = analyzer.apply_filter(
            RoomFilter(rooms)
        )

        print("\nFiltered properties:")
        print(result)

        filename = input("Enter Excel filename: ")
        analyzer.export_to_excel(result, filename)

        print(f"Exported to {filename}")

    elif choice == "5":
        visualizer.average_price_by_district()

    elif choice == "6":
        visualizer.property_count_by_district()

    elif choice == "7":
        visualizer.price_vs_area()

    elif choice == "8":
        area = float(input("Enter area: "))
        rooms = int(input("Enter number of rooms: "))

        predicted_price = analyzer.price_predictor(
            area,
            rooms
        )

        print(f"Predicted price: ${predicted_price:,.2f}")

    elif choice == "0":
        print("Goodbye!")
        break

    else:
        print("Invalid option!")