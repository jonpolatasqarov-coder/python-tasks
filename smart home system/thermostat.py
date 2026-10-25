
from device import Device


class Thermostat(Device):
    def __init__(self, name, temperature=20, power=100):
        super().__init__(name, power)
        self.temperature = temperature
        self.temperature_history = [temperature]
        self.observers = []

    def add_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.temperature)

    def turn_on(self):
        if not self.is_on:
            self.start_timer()
            print(f"{self.name} turned ON.")

    def turn_off(self):
        if self.is_on:
            self.stop_timer()
            print(f"{self.name} turned OFF.")


    def set_temperature(self, temperature):
        if not self.is_on:
            print(
                "Cannot change temperature. "
                "The thermostat is OFF."
            )
            return

        try:
            temperature = float(temperature)
        except (ValueError, TypeError):
            print("Invalid temperature. Please enter a number.")
            return

        if not 10 <= temperature <= 35:
            print("Temperature must be between 10°C and 35°C.")
            return

        self.temperature = temperature
        self.temperature_history.append(self.temperature)

        print(
            f"{self.name} temperature set to "
            f"{self.temperature}°C."
        )

        self.notify_observers()


    def status_report(self):
        status = "ON" if self.is_on else "OFF"
        working_time = self.format_working_time()

        return (
            f"{self.name}: {status}, "
            f"Temperature: {self.temperature}°C, "
            f"Working time: {working_time}"
        )
