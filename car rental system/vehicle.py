from abc import ABC, abstractmethod

 
class Vehicle(ABC):
    def __init__(self, name, price_per_day):
        self.name = name
        self.price_per_day = price_per_day
        self.is_available = True
        self.rental_count = 0

    @abstractmethod
    def rent(self, days):
        pass

    @abstractmethod
    def return_vehicle(self):
        pass

    @abstractmethod
    def calculate_rent(self, days):
        pass