from abc import ABC, abstractmethod


class Device(ABC):
    def __init__(self, name, power):
        self.name = name
        self.power = power
        self.is_on = False

    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

    @abstractmethod
    def status_report(self):
        pass