
from analyzer import RealEstateAnalyzer
from strategies import (
    PriceFilter,
    AreaFilter,
    DistrictFilter,
    RoomFilter,
    CombinedFilter
)
from visualizer import RealEstateVisualizer


analyzer = RealEstateAnalyzer("properties.csv")
visualizer = RealEstateVisualizer(analyzer.df)


def get_number(prompt, number_type=float, minimum=0):
    while True:
        raw_value = input(
            f"{prompt} or 0 to return: "
        ).strip()

        if raw_value == "0":
            return None

        try:
            value = number_type(raw_value)

            if value < minimum:
                print(
                    f"  [!] Value must be at least {minimum}."
                )
                continue

            return value

        except ValueError:
            print(
                "  [!] Invalid input. Please enter a valid number."
            )


def show_properties(df):
    if df.empty:
        print("\n  No properties found.")
        return

    print("\n" + "=" * 88)
    print(f"  FOUND {len(df)} PROPERTIES")
    print("=" * 88)

    for _, row in df.iterrows():
        print(
            f"  ID: {row['id']:<3} | "
            f"{str(row['type']):<10} | "
            f"{str(row['district']):<16}"
        )

        price_per_m2 = (
            row["price_per_m2"]
            if "price_per_m2" in row.index
            else row["price"] / row["area"]
        )

        print(
            f"  Area: {row['area']} m² | "
            f"Rooms: {row['rooms']} | "
            f"Price: ${row['price']:,.0f} | "
            f"Price/m²: ${price_per_m2:,.2f} | "
            f"Status: {str(row['status']).title()}"
        )

        print("-" * 88)


def show_results(result):
    if result.empty:
        print("\nNo properties found. Try different criteria.")
        return

    show_properties(result)

    while True:
        export_choice = input(
            "\nExport results to Excel? (y/n): "
        ).strip().lower()

        if export_choice in ("y", "n"):
            break

        print("Invalid input. Please enter 'y' or 'n'.")

    if export_choice == "n":
        print("Export skipped.")
        return

    while True:
        filename = input(
            "Enter Excel filename (0 to cancel): "
        ).strip()

        if filename == "0":
            print("Export cancelled.")
            return

        if not filename:
            print("Filename cannot be empty. Please try again.")
            continue

        if not filename.lower().endswith(".xlsx"):
            filename += ".xlsx"

        try:
            analyzer.export_to_excel(result, filename)
            return
        except (OSError, ValueError, PermissionError) as error:
            print(f"Export failed: {error}")
            print("Please try another filename.")


def get_district():
    while True:
        district = input(
            "Enter district (0 to return): "
        ).strip()

        if district == "0":
            return None

        if not district:
            print("  [!] District cannot be empty.")
            continue

        return district


while True:
    print("\n" + "=" * 42)
    print("       REAL ESTATE ANALYZER")
    print("=" * 42)
    print("  FILTER PROPERTIES")
    print("  1. Filter by price ($)")
    print("  2. Filter by area (m²)")
    print("  3. Filter by district")
    print("  4. Filter by rooms")
    print("  14. Filter by price and district")
    print("-" * 42)
    print("  ANALYTICS")
    print("  5. Average price by district")
    print("  6. Property count by district")
    print("  7. Price vs area chart")
    print("  8. Predict property price")
    print("  9. Average property price")
    print("  10. Highest property price")
    print("  11. Sold property count")
    print("  12. Most expensive district")
    print("  13. Price per m² analysis")
    print("-" * 42)
    print("  0. Exit")
    print("=" * 42)

    choice = input("  Select option [0-14]: ").strip()

    if choice == "1":
        max_price = get_number(
            "Enter maximum price ($)",
            minimum=0.01
        )

        if max_price is None:
            continue

        result = analyzer.apply_filter(
            PriceFilter(max_price)
        )
        show_results(result)

    elif choice == "2":
        min_area = get_number(
            "Enter minimum area (m²)",
            minimum=0.01
        )

        if min_area is None:
            continue

        result = analyzer.apply_filter(
            AreaFilter(min_area)
        )
        show_results(result)

    elif choice == "3":
        district = get_district()

        if district is None:
            continue

        result = analyzer.apply_filter(
            DistrictFilter(district)
        )
        show_results(result)

    elif choice == "4":
        rooms = get_number(
            "Enter number of rooms",
            number_type=int,
            minimum=1
        )

        if rooms is None:
            continue

        result = analyzer.apply_filter(
            RoomFilter(rooms)
        )
        show_results(result)

    elif choice == "5":
        visualizer.average_price_by_district()

    elif choice == "6":
        visualizer.property_count_by_district()

    elif choice == "7":
        visualizer.price_vs_area()

    elif choice == "8":
        area = get_number(
            "Enter area (m²)",
            number_type=float,
            minimum=1
        )
        if area is None:
            continue

        rooms = get_number(
            "Enter number of rooms",
            number_type=int,
            minimum=1
        )
        if rooms is None:
            continue

        district = get_district()
        if district is None:
            continue

        print("\nProperty type:")
        print("1. Apartment")
        print("2. House")

        property_choice = input(
            "Select property type [1-2] or 0 to return: "
        ).strip()

        if property_choice == "0":
            continue
        elif property_choice == "1":
            property_type = "Apartment"
        elif property_choice == "2":
            property_type = "House"
        else:
            print("  [!] Invalid property type.")
            continue

        try:
            predicted_price, mae, r2 = analyzer.price_predictor(
                area,
                rooms,
                district,
                property_type
            )

            print(f"\n  Predicted price: ${predicted_price:,.2f}")
            print(f"  Model MAE: ${mae:,.2f}")
            print(f"  Model R²: {r2:.3f}")

        except (ValueError, TypeError) as error:
            print(
                f"  [!] Could not predict the price: {error}"
            )

    elif choice == "9":
        print(
            f"\n  Average property price: "
            f"${analyzer.average_price():,.2f}"
        )

    elif choice == "10":
        print(
            f"\n  Highest property price: "
            f"${analyzer.highest_price():,.2f}"
        )

    elif choice == "11":
        print(
            f"\n  Sold properties: "
            f"{analyzer.sold_count()}"
        )

    elif choice == "12":
        district = analyzer.most_expensive_district()
        print(
            f"\n  Most expensive district "
            f"(by average property price): {district}"
        )

    elif choice == "13":
        result = analyzer.property_price_analysis()
        show_results(result)

    elif choice == "14":
        max_price = get_number(
            "Enter maximum price ($)",
            number_type=float,
            minimum=0.01
        )
        if max_price is None:
            continue

        district = get_district()
        if district is None:
            continue

        strategy = CombinedFilter(
            PriceFilter(max_price),
            DistrictFilter(district)
        )

        result = analyzer.apply_filter(strategy)
        show_results(result)

    elif choice == "0":
        print("\n  Thank you for using Real Estate Analyzer!")
        break

    else:
        print(
            "  [!] Invalid option. Please choose 0-14."
        )

