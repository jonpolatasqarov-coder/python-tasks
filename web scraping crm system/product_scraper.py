from bs4 import BeautifulSoup

from scraper import Scraper
from retry import retry, NotFoundError
from logger import log


class ProductScraper(Scraper):

    @retry
    def scrape(self):
        log(f"START: ProductScraper - {self.url}")

        try:
            response = self.get_response()

            if response.status_code == 404:
                log(f"ERROR: 404 - {self.url}")
                raise NotFoundError("Page not found")

            response.raise_for_status()

            soup = BeautifulSoup(response.content, "lxml")

            products = soup.find_all(
                "article",
                class_="product_pod"
            )

            for product in products:
                title = product.find("h3").find("a")
                price = product.find(
                    "p",
                    class_="price_color"
                )

                if title and price:
                    self.data.append({
                        "title": title.get("title"),
                        "price": price.get_text(strip=True),
                        "url": self.url
                    })

            log(
                f"END: ProductScraper - {self.url} "
                f"- {len(self.data)} products"
            )

            print(self.data)

        except NotFoundError:
            raise

        except Exception as error:
            log(f"ERROR: {error}")
            print(f"Error: {error}")