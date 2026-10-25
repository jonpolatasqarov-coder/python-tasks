
from device import Device


class Light(Device):
    def __init__(self, name, power=10):
        super().__init__(name, power)

    def turn_on(self):
        if not self.is_on:
            self.start_timer()
            print(f"{self.name} turned ON.")

    def turn_off(self):
        if self.is_on:
            self.stop_timer()
            print(f"{self.name} turned OFF.")

    def status_report(self):
        status = "ON" if self.is_on else "OFF"
        working_time = self.format_working_time()

        return (
            f"{self.name}: {status}, "
            f"Working time: {working_time}"
        )
