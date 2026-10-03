import json


class SmartHomeController:
    def __init__(self):
        self.devices = []

    def add_device(self, device):
        self.devices.append(device)

    def turn_on_all(self):
        for device in self.devices:
            device.turn_on()

    def turn_off_all(self):
        for device in self.devices:
            device.turn_off()

    def show_status(self):
        for device in self.devices:
            print(device.status_report())

    def save_devices(self, filename="devices.json"):
        data = []

        for device in self.devices:
            device_data = {
                "name": device.name,
                "type": device.__class__.__name__,
                "is_on": device.is_on
            }

            if hasattr(device, "temperature"):
                device_data["temperature"] = device.temperature
                device_data["temperature_history"] = (
                    device.temperature_history
                )

            data.append(device_data)

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print("Device states saved.")

    def load_devices(self, filename="devices.json"):
        from light import Light
        from thermostat import Thermostat
        from camera import Camera
        from alarm import Alarm
        from fan import Fan

        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)

        except FileNotFoundError:
            print("No saved device data found.")
            return False

        self.devices = []

        for device_data in data:
            device_type = device_data["type"]

            if device_type == "Light":
                device = Light(device_data["name"])

            elif device_type == "Thermostat":
                device = Thermostat(
                    device_data["name"],
                    device_data.get("temperature", 20)
                )

                device.temperature_history = device_data.get(
                    "temperature_history",
                    [device.temperature]
                )

            elif device_type == "Camera":
                device = Camera(device_data["name"])

            elif device_type == "Alarm":
                device = Alarm(device_data["name"])

            elif device_type == "Fan":
                device = Fan(device_data["name"])

            else:
                continue

            device.is_on = device_data["is_on"]

            self.devices.append(device)

        print("Device states loaded.")
        return True