
class TemperatureObserver:
    def __init__(self, fan):
        self.fan = fan

    def update(self, temperature):
        if temperature > 30:
            if not self.fan.is_on:
                self.fan.turn_on()
                print("High temperature detected. Fan turned ON.")

        else:
            if self.fan.is_on:
                self.fan.turn_off()
                print("Temperature is normal. Fan turned OFF.")
