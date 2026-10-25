
from abc import ABC, abstractmethod
import time


class Device(ABC):
    def __init__(self, name, power):
        self.name = name
        self.power = power
        self.is_on = False
        self.working_hours = 0.0
        self._turned_on_at = None

    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

    @abstractmethod
    def status_report(self):
        pass

    def start_timer(self, started_at=None):
        if not self.is_on:
            self.is_on = True

            if started_at is not None:
                self._turned_on_at = float(started_at)
            else:
                self._turned_on_at = time.time()

    def stop_timer(self):
        if self.is_on and self._turned_on_at is not None:
            elapsed_seconds = max(
                0, time.time() - self._turned_on_at
            )

            self.working_hours += elapsed_seconds / 3600
            self._turned_on_at = None
            self.is_on = False

    def get_working_hours(self):
        hours = self.working_hours

        if self.is_on and self._turned_on_at is not None:
            elapsed_seconds = max(
                0, time.time() - self._turned_on_at
            )
            hours += elapsed_seconds / 3600

        return hours

    def format_working_time(self):
        total_seconds = int(self.get_working_hours() * 3600)

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        return (
            f"{hours} hours "
            f"{minutes} minutes "
            f"{seconds} seconds"
        )
