
import csv
import json

from news_scraper import NewsScraper
from product_scraper import ProductScraper
from social_scraper import SocialScraper
from storage import save_json, load_json, save_csv
from cleaner import DataCleaner
from lead_manager import LeadManager
from logger import log


scrapers = [
    NewsScraper(),
    ProductScraper(),
    SocialScraper(
        "https://scrapifydatalabs.com/playground/careermesh/people.html"
    )
]

lead_manager = LeadManager()


def log_error(context, error):
    try:
        log(
            f"ERROR: {context} - "
            f"{type(error).__name__}: {error}"
        )
    except Exception:
        print("Warning: could not write to log.txt.")


def get_non_empty_input(prompt):
    while True:
        try:
            value = input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            print("\nInput cancelled.")
            return None

        if value:
            return value

        print("Input cannot be empty. Please try again.")


def choose_lead():
    try:
        leads = lead_manager.load_leads()
    except (OSError, ValueError) as error:
        log_error("Loading leads", error)
        print(f"Could not load leads: {error}")
        return None

    if not leads:
        print("No leads available. Run scraping first.")
        return None

    print("\n========== SELECT A LEAD ==========")

    for index, lead in enumerate(leads, start=1):
        print(
            f"{index}. {lead.get('name', 'Unknown')} "
            f"| {lead.get('status', 'new')} "
            f"| ID: {lead.get('id', 'N/A')}"
        )

    print("0. Cancel")

    while True:
        choice = get_non_empty_input(
            "Select lead number: "
        )

        if choice is None or choice == "0":
            print("Operation cancelled.")
            return None

        if not choice.isdigit():
            print("Enter a valid number from the list.")
            continue

        index = int(choice)

        if 1 <= index <= len(leads):
            lead = leads[index - 1]
            lead_id = lead.get("id")

            if not lead_id:
                print("Selected lead has no ID.")
                return None

            return str(lead_id)

        print(
            f"Choose a number between 1 and {len(leads)}, "
            "or 0 to cancel."
        )


def start_scraping():
    successful = []
    failed = []

    for scraper in scrapers:
        scraper.data = []

        try:
            scraper.scrape()

            if not scraper.data:
                raise ValueError("Scraping returned no data.")

            for item in scraper.data:
                if not isinstance(item, dict):
                    continue

                for field in ("title", "name", "headline"):
                    value = item.get(field)

                    if isinstance(value, str) and value.strip():
                        item[field] = DataCleaner.clean_text(value)

            save_json(
                scraper.data,
                f"{scraper.__class__.__name__}.json"
            )
            successful.append(scraper)

        except Exception as error:
            failed.append(scraper.__class__.__name__)
            log_error(scraper.__class__.__name__, error)

            print(
                f"{scraper.__class__.__name__} failed: "
                f"{type(error).__name__}: {error}"
            )

    social_scraper = next(
        (
            scraper for scraper in scrapers
            if isinstance(scraper, SocialScraper)
        ),
        None
    )

    if social_scraper in successful:
        try:
            leads = lead_manager.merge_leads(
                social_scraper.data
            )
            print(f"CRM updated: {len(leads)} leads.")


        except Exception as error:
            log_error("Updating leads", error)
            print(
                f"Could not update leads: {type(error).__name__}: {error}"
            )

    else:
        print("Social scraping failed; leads were not updated.")

    if failed:
        print("Scraping finished with errors:", ", ".join(failed))
    else:
        print("Scraping completed successfully!")


def show_stats():
    files = {
        "News": "NewsScraper.json",
        "Products": "ProductScraper.json",
        "Social profiles": "SocialScraper.json",
        "Leads": "leads.json"
    }

    print("\n========== STATISTICS ==========")

    for label, filename in files.items():
        try:
            data = load_json(filename)

            if not isinstance(data, list):
                print(f"{label}: invalid format")
            else:
                print(f"{label}: {len(data)}")

        except FileNotFoundError:
            print(f"{label}: file not found")
        except json.JSONDecodeError as error:
            print(f"{label}: invalid JSON ({error})")
        except OSError as error:
            log_error(f"Reading {filename}", error)
            print(f"{label}: could not read file")


def export_data():
    files = {
        "NewsScraper.json": "news.csv",
        "ProductScraper.json": "products.csv",
        "SocialScraper.json": "social.csv",
        "leads.json": "leads.csv"
    }

    try:
        datasets = {}

        for json_file, csv_file in files.items():
            data = load_json(json_file)

            if not isinstance(data, list):
                raise ValueError(
                    f"{json_file} must contain a list."
                )

            if any(not isinstance(row, dict) for row in data):
                raise ValueError(
                    f"{json_file} contains invalid records."
                )

            datasets[csv_file] = data

        for csv_file, data in datasets.items():
            if not data:
                print(f"Skipped {csv_file}: no data.")
                continue

            save_csv(data, csv_file)
            print(f"Exported: {csv_file}")

        print("Export completed.")

    except FileNotFoundError as error:
        print(f"File not found: {error.filename}")
    except json.JSONDecodeError as error:
        print(f"Invalid JSON: {error}")
    except (OSError, csv.Error, ValueError) as error:
        log_error("CSV export", error)
        print(f"Export failed: {error}")


def update_lead_status():
    lead_id = choose_lead()

    if lead_id is None:
        return

    statuses = [
        "new",
        "contacted",
        "qualified",
        "converted",
        "lost"
    ]

    print("\nSelect new status:")

    for index, status in enumerate(statuses, start=1):
        print(f"{index}. {status}")

    print("0. Cancel")

    while True:
        choice = get_non_empty_input("Choose status: ")

        if choice is None or choice == "0":
            print("Operation cancelled.")
            return

        if not choice.isdigit():
            print("Enter a number from 1 to 5.")
            continue

        index = int(choice)

        if 1 <= index <= len(statuses):
            break

        print("Invalid selection.")

    try:
        lead_manager.update_status(
            lead_id,
            statuses[index - 1]
        )
    except (OSError, ValueError) as error:
        log_error("Updating status", error)
        print(f"Could not update status: {error}")


def add_lead_note():
    lead_id = choose_lead()

    if lead_id is None:
        return

    while True:
        note = get_non_empty_input(
            "Enter note (or 0 to cancel): "
        )

        if note is None or note == "0":
            print("Operation cancelled.")
            return

        try:
            if lead_manager.add_note(lead_id, note):
                return

        except (OSError, ValueError) as error:
            log_error("Adding note", error)
            print(f"Could not save note: {error}")
            return


def show_lead_history():
    lead_id = choose_lead()

    if lead_id is None:
        return

    try:
        lead_manager.show_history(lead_id)
    except (OSError, ValueError) as error:
        log_error("Showing history", error)
        print(f"Could not show history: {error}")


def show_leads():
    try:
        lead_manager.show_leads()
    except (OSError, ValueError) as error:
        log_error("Showing leads", error)
        print(f"Could not load leads: {error}")


def main():
    while True:
        print("\n========== WEB SCRAPING CRM ==========")
        print("1. Start scraping")
        print("2. Show statistics")
        print("3. Export data to CSV")
        print("4. Show leads")
        print("5. Update lead status")
        print("6. Add note to lead")
        print("7. Show lead history")
        print("8. Exit")

        try:
            choice = input("Choose (1-8): ").strip()

            if choice == "1":
                start_scraping()
            elif choice == "2":
                show_stats()
            elif choice == "3":
                export_data()
            elif choice == "4":
                show_leads()
            elif choice == "5":
                update_lead_status()
            elif choice == "6":
                add_lead_note()
            elif choice == "7":
                show_lead_history()
            elif choice == "8":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Enter a number from 1 to 8.")

        except (KeyboardInterrupt, EOFError):
            print("\nInput cancelled. Returning to menu.")

        except Exception as error:
            log_error("Main menu", error)
            print(
                f"Unexpected error: {type(error).__name__}: {error}"
            )


if __name__ == "__main__":
    main()
