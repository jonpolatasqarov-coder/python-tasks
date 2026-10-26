from abc import ABC, abstractmethod

import requests


class Scraper(ABC):
    def __init__(self, url):
        self.url = url
        self.data = []

    def get_response(self):
        response = requests.get(self.url, timeout=10)
        response.raise_for_status()
        return response

    @abstractmethod
    def scrape(self):
        pass
