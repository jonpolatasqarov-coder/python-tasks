class TemperatureObserver:
    def __init__(self, fan):
        self.fan = fan

    def update(self, temperature):
        if temperature > 30:
            self.fan.turn_on()