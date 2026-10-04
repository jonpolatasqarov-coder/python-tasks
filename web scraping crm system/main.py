from news_scraper import NewsScraper
from product_scraper import ProductScraper
from social_scraper import SocialScraper
from storage import save_json, load_json, save_csv
from cleaner import DataCleaner
from lead_generator import LeadGenerator


scrapers = [
    NewsScraper("https://quotes.toscrape.com/"),
    ProductScraper("https://books.toscrape.com/"),
    SocialScraper(
        "https://scrapifydatalabs.com/playground/careermesh/people.html"
    )
]


def start_scraping():
    all_leads = []
    success_count = 0

    for scraper in scrapers:
        scraper.data.clear()

        try:
            scraper.scrape()

        except Exception as error:
            print(f"Scraping failed: {error}")
            continue

        for item in scraper.data:

            if "title" in item:
                item["title"] = DataCleaner.clean_text(
                    item["title"]
                )

            if "name" in item:
                item["name"] = DataCleaner.clean_text(
                    item["name"]
                )

            if "headline" in item and item["headline"]:
                item["headline"] = DataCleaner.clean_text(
                    item["headline"]
                )

        save_json(
            scraper.data,
            f"{scraper.__class__.__name__}.json"
        )

        if isinstance(scraper, (NewsScraper, ProductScraper)):
            leads = LeadGenerator.generate(scraper.data)
            all_leads.extend(leads)

        success_count += 1

    save_json(all_leads, "leads.json")

    if success_count == len(scrapers):
        print("Scraping completed successfully!")
    else:
        print("Scraping completed with some errors.")


def show_stats():
    print("\n--- Stats ---")

    try:
        news = load_json("NewsScraper.json")
        products = load_json("ProductScraper.json")
        social = load_json("SocialScraper.json")
        leads = load_json("leads.json")

        print(f"News: {len(news)}")
        print(f"Products: {len(products)}")
        print(f"Social: {len(social)}")
        print(f"Leads: {len(leads)}")

    except FileNotFoundError:
        print("No scraped data found. Start scraping first.")


def export_data():
    try:
        news = load_json("NewsScraper.json")
        products = load_json("ProductScraper.json")
        social = load_json("SocialScraper.json")
        leads = load_json("leads.json")

        save_csv(news, "news.csv")
        save_csv(products, "products.csv")
        save_csv(social, "social.csv")
        save_csv(leads, "leads.csv")

        print("Data exported successfully!")

    except FileNotFoundError:
        print("No scraped data found. Start scraping first.")


while True:
    print("\n--- Web Scraping CRM ---")
    print("1. Start scraping")
    print("2. Show stats")
    print("3. Export data")
    print("4. Exit")

    choice = input("Choose: ")

    if choice == "1":
        start_scraping()

    elif choice == "2":
        show_stats()

    elif choice == "3":
        export_data()

    elif choice == "4":
        print("Goodbye!")
        break

    else:
        print("Invalid choice")