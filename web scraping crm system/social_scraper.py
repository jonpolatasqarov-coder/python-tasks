from bs4 import BeautifulSoup

from scraper import Scraper
from retry import retry, NotFoundError
from logger import log


class SocialScraper(Scraper):

    @retry
    def scrape(self):
        log(f"START: SocialScraper - {self.url}")

        try:
            response = self.get_response()

            if response.status_code == 404:
                log(f"ERROR: 404 - {self.url}")
                raise NotFoundError("Page not found")

            response.raise_for_status()

            soup = BeautifulSoup(response.text, "lxml")

            people = soup.find_all("article", class_="cm-person")

            self.data = []

            for person in people:
                person_id = person.get("data-person-id")
                region = person.get("data-region")
                industry = person.get("data-industry")
                open_to = person.get("data-open-to-value")

                name_tag = person.find("h3", class_="cm-name")
                headline_tag = person.find(
                    "p",
                    class_="cm-headline"
                )

                meta_tag = person.find(
                    "div",
                    class_="cm-meta"
                )

                name = None
                profile_link = None

                if name_tag:
                    link = name_tag.find("a")

                    if link:
                        name = link.get_text(strip=True)
                        profile_link = link.get("href")
                    else:
                        name = name_tag.get_text(strip=True)

                headline = None

                if headline_tag:
                    headline = headline_tag.get_text(strip=True)

                location = None
                connections = None

                if meta_tag:
                    meta_text = meta_tag.get_text(" ", strip=True)

                    parts = [
                        part.strip()
                        for part in meta_text.split("·")
                    ]

                    if len(parts) >= 1:
                        location = parts[0]

                    for part in parts:
                        if "connections" in part.lower():
                            connections = part
                            break

                self.data.append({
                    "id": person_id,
                    "name": name,
                    "headline": headline,
                    "location": location,
                    "region": region,
                    "industry": industry,
                    "open_to": open_to,
                    "connections": connections,
                    "profile_url": profile_link
                })

            log(
                f"END: SocialScraper - {self.url} "
                f"- {len(self.data)} people"
            )

            print(self.data)

        except NotFoundError:
            raise

        except Exception as error:
            log(f"ERROR: {error}")
            print(f"Error: {error}")