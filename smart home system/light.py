from device import Device


class Light(Device):
    def __init__(self, name, power=60):
        super().__init__(name, power)

    def turn_on(self):
        self.is_on = True
        print(f"{self.name} is turned on.")

    def turn_off(self):
        self.is_on = False
        print(f"{self.name} is turned off.")

    def status_report(self):
        status = "ON" if self.is_on else "OFF"
        return f"{self.name}: {status}"