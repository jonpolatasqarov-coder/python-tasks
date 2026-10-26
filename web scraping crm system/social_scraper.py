
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from scraper import Scraper
from retry import retry
from logger import log
from cleaner import DataCleaner


class SocialScraper(Scraper):

    def __init__(
        self,
        url="https://scrapifydatalabs.com/playground/careermesh/people.html"
    ):
        super().__init__(url)

    @retry
    def scrape(self):
        log(f"START: SocialScraper - {self.url}")

        response = requests.get(
            self.url,
            headers={
                "User-Agent": "WebScrapingCRM/1.0 (educational project)"
            },
            timeout=20
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        scraped_data = []
        seen_ids = set()

        # Saytdagi barcha profil havolalarini topamiz.
        profile_links = soup.select('a[href*="/person-"]')

        for link in profile_links:
            href = link.get("href", "").strip()

            if not href:
                continue

            # Nisbiy URL'ni to'liq URL'ga aylantiramiz.
            profile_url = urljoin(self.url, href)

            # /playground/careermesh/person-p-ava-chen
            # -> p-ava-chen
            profile_id = profile_url.rstrip("/").split("/")[-1]

            if profile_id.startswith("person-"):
                profile_id = profile_id[len("person-"):]

            if not profile_id or profile_id in seen_ids:
                continue

            seen_ids.add(profile_id)

            # Profil kartasini topamiz.
            card = link.find_parent(
                ["article", "div", "li"]
            )

            if card is None:
                card = link.parent

            # Ism.
            name_element = card.select_one(".cm-name")

            name = (
                name_element.get_text(" ", strip=True)
                if name_element
                else link.get_text(" ", strip=True)
            )

            # Kasbiy sarlavha.
            headline_element = card.select_one(".cm-headline")

            headline = (
                headline_element.get_text(" ", strip=True)
                if headline_element
                else ""
            )

            # Joylashuv, soha va ulanishlar.
            meta_element = card.select_one(".cm-meta")

            meta_text = (
                meta_element.get_text(" ", strip=True)
                if meta_element
                else ""
            )

            meta_parts = [
                part.strip()
                for part in meta_text.split("·")
                if part.strip()
            ]

            location = meta_parts[0] if len(meta_parts) > 0 else ""
            industry = meta_parts[1] if len(meta_parts) > 1 else ""

            connections = next(
                (
                    part
                    for part in meta_parts
                    if "connections" in part.lower()
                ),
                ""
            )

            # "Open to" holatini badge'dan olamiz.
            badge = card.select_one(".cm-badge[data-open-to]")

            open_to = (
                badge.get("data-open-to", "").strip()
                if badge
                else ""
            )

            # Matnlarni tozalaymiz, lekin katta-kichik
            # harflarni o'zgartirmaymiz.
            name = DataCleaner.clean_text(name)
            headline = DataCleaner.clean_text(headline)
            location = DataCleaner.clean_text(location)
            industry = DataCleaner.clean_text(industry)
            connections = DataCleaner.clean_text(connections)
            open_to = DataCleaner.clean_text(open_to)

            if not name:
                continue

            scraped_data.append({
                "id": profile_id,
                "name": name,
                "source": profile_url,
                "headline": headline,
                "location": location,
                "region": location,
                "industry": industry,
                "open_to": open_to,
                "connections": connections
            })

        if not scraped_data:
            raise ValueError(
                "Profil topilmadi. Eski ma'lumotlar saqlab qolindi."
            )

        self.data = scraped_data

        log(
            f"END: SocialScraper - {self.url} "
            f"- {len(self.data)} profiles"
        )

        print(f"Profiles scraped: {len(self.data)}")
