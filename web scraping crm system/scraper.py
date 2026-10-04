from abc import ABC, abstractmethod

import requests


class Scraper(ABC):
    def __init__(self, url):
        self.url = url
        self.data = []

    def get_response(self):
        response = requests.get(self.url)

        return response

    @abstractmethod
    def scrape(self):
        pass