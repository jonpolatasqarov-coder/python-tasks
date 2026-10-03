class EnergyCalculator:
    def calculate(self, device, hours):
        if not device.is_on:
            return 0

        return device.power * hours

    def calculate_all(self, devices, hours):
        total = 0

        for device in devices:
            energy = self.calculate(device, hours)

            print(
                f"{device.name}: "
                f"{energy:.2f} Wh"
            )

            total += energy

        print(
            f"Total energy consumption: "
            f"{total:.2f} Wh"
        )

        return total