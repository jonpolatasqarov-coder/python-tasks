
from scraper import Scraper
import feedparser


class NewsScraper(Scraper):
    def __init__(self, url="https://feeds.bbci.co.uk/news/rss.xml"):
        super().__init__(url)

    def scrape(self):
        self.data = []

        response = self.get_response()
        response.raise_for_status()
        
        feed = feedparser.parse(response.content)

        if feed.bozo:
            print(f"RSS parsing warning: {feed.bozo_exception}")

        if not feed.entries:
            raise ValueError(
                f"No news articles found. "
                f"HTTP status: {response.status_code}; "
                f"Content-Type: {response.headers.get('Content-Type')}; "
                f"Response preview: {response.text[:200]!r}"
            )
        
        for entry in feed.entries:
            title = entry.get("title", "").strip()
            link = entry.get("link", "").strip()
            description = entry.get("summary", "").strip()
            published_at = entry.get("published", "")

            if not title or not link:
                continue

            self.data.append({
                "title": title,
                "description": description,
                "url": link,
                "published_at": published_at,
                "source": "BBC News"
            })

        if not self.data:
            raise ValueError("No news articles were found.")

        return self.data
