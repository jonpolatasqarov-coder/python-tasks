from device import Device


class Camera(Device):
    def __init__(self, name, power=15):
        super().__init__(name, power)

    def turn_on(self):
        self.is_on = True
        print(f"{self.name} is recording.")

    def turn_off(self):
        self.is_on = False
        print(f"{self.name} stopped recording.")

    def status_report(self):
        status = "ON" if self.is_on else "OFF"
        return f"{self.name}: {status}"