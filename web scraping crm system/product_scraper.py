
import requests

from scraper import Scraper
from retry import retry
from logger import log
from cleaner import DataCleaner


class ProductScraper(Scraper):

    def __init__(self, url="https://openlibrary.org/search.json"):
        super().__init__(url)


    @retry
    def scrape(self):
        log(f"START: ProductScraper - {self.url}")

        params = {
            "q": "subject:fiction",
            "fields": "key,title,author_name,first_publish_year",
            "limit": 20,
            "page": 1,
            "sort": "rating"
        }

        scraped_data = []
        seen_keys = set()
        max_pages = 3

        for page in range(1, max_pages + 1):
            params["page"] = page

            response = requests.get(
                self.url,
                params=params,
                headers={
                    "User-Agent": "WebScrapingCRM/1.0 (educational project)"
                },
                timeout=20
            )
            response.raise_for_status()

            try:
                result = response.json()
            except requests.exceptions.JSONDecodeError as error:
                raise ValueError(
                    f"API JSON qaytarmadi. "
                    f"HTTP status: {response.status_code}. "
                    f"Content-Type: {response.headers.get('Content-Type')}. "
                    f"Javob: {response.text[:300]!r}"
                ) from error

            books = result.get("docs", [])

            if not books:
                break

            for book in books:
                title = book.get("title", "")
                authors = book.get("author_name", [])
                book_key = book.get("key", "")

                if not title:
                    continue

                # Takroriy kitoblarni o'tkazib yuboramiz.
                unique_key = book_key or title

                if unique_key in seen_keys:
                    continue

                seen_keys.add(unique_key)

                title = DataCleaner.clean_text(title)

                author = ", ".join(authors)
                author = (
                    DataCleaner.clean_text(author)
                    if author else ""
                )

                book_url = (
                    f"https://openlibrary.org{book_key}"
                    if book_key.startswith("/")
                    else ""
                )

                scraped_data.append({
                    "title": title,
                    "author": author,
                    "published_year": book.get(
                        "first_publish_year"
                    ),
                    "url": book_url
                })

        if not scraped_data:
            raise ValueError(
                "No books found. Existing data will be preserved."
            )

        self.data = scraped_data

        log(
            f"END: ProductScraper - {self.url} "
            f"- {len(self.data)} books"
        )

        print(f"Books scraped: {len(self.data)}")
