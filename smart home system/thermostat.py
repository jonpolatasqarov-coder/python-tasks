from device import Device


class Thermostat(Device):
    def __init__(self, name, temperature=20, power=100):
        super().__init__(name, power)
        self.temperature = temperature
        self.temperature_history = [temperature]
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def set_temperature(self, temperature):
        self.temperature = temperature
        self.temperature_history.append(temperature)

        print(
            f"{self.name} temperature changed to "
            f"{self.temperature}°C."
        )

        for observer in self.observers:
            observer.update(self.temperature)

    def turn_on(self):
        self.is_on = True
        print(f"{self.name} is turned on.")

    def turn_off(self):
        self.is_on = False
        print(f"{self.name} is turned off.")

    def status_report(self):
        status = "ON" if self.is_on else "OFF"

        return (
            f"{self.name}: {status}, "
            f"Temperature: {self.temperature}°C"
        )