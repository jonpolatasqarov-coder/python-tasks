
class EnergyCalculator:
    def calculate_device(self, device):
        working_hours = device.get_working_hours()
        energy = device.power * working_hours

        total_seconds = int(working_hours * 3600)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        working_time = (
            f"{hours} hours "
            f"{minutes} minutes "
            f"{seconds} seconds"
        )

        print(
            f"{device.name}: "
            f"{energy:.2f} Wh "
            f"({working_time})"
        )

        return energy

    def calculate_all(self, devices):
        total_energy = 0.0

        print("\n--- Energy Consumption ---")

        for device in devices:
            total_energy += self.calculate_device(device)

        print("-" * 40)
        print(
            f"Total Energy Consumption: "
            f"{total_energy:.2f} Wh"
        )

        return total_energy
