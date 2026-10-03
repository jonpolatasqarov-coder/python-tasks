from device import Device


class Fan(Device):
    def __init__(self, name, power=75):
        super().__init__(name, power)

    def turn_on(self):
        self.is_on = True
        print(f"{self.name} is turned on automatically.")

    def turn_off(self):
        self.is_on = False
        print(f"{self.name} is turned off.")

    def status_report(self):
        status = "ON" if self.is_on else "OFF"
        return f"{self.name}: {status}"