from bs4 import BeautifulSoup

from scraper import Scraper
from retry import retry, NotFoundError
from logger import log


class NewsScraper(Scraper):
    @retry
    def scrape(self):
        log(f"START: NewsScraper - {self.url}")

        try:
            response = self.get_response()

            if response.status_code == 404:
                log(f"ERROR: 404 - {self.url}")
                raise NotFoundError("Page not found")

            soup = BeautifulSoup(response.text, "lxml")

            quotes = soup.find_all("div", class_="quote")

            for quote in quotes:
                text = quote.find("span", class_="text")
                author = quote.find("small", class_="author")

                if text and author:
                    self.data.append({
                        "title": text.get_text(strip=True),
                        "author": author.get_text(strip=True),
                        "url": self.url
                    })

            log(f"END: NewsScraper - {self.url}")

            print(self.data)

        except NotFoundError:
            raise

        except Exception as error:
            log(f"ERROR: {error}")
            print(f"Error: {error}")