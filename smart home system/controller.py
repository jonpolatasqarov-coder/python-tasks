
import json
import time
from pathlib import Path


class SmartHomeController:
    def __init__(self):
        self.devices = []
        self.data_file = Path(__file__).resolve().parent / "devices.json"

    def add_device(self, device):
        if not hasattr(device, "working_hours"):
            device.working_hours = 0.0

        if not hasattr(device, "_turned_on_at"):
            device._turned_on_at = None

        self.devices.append(device)

    def turn_on_all(self):
        for device in self.devices:
            if not device.is_on:
                device.turn_on()

        self.save_devices()

    def turn_off_all(self):
        for device in self.devices:
            if device.is_on:
                device.turn_off()

        self.save_devices()

    def show_status(self):
        for device in self.devices:
            print(device.status_report())


    def save_devices(self, filename=None):
        if filename is None:
            filename = self.data_file

        data = []

        for device in self.devices:
            device_data = {
                "name": device.name,
                "type": device.__class__.__name__,
                "is_on": device.is_on,
                "working_hours": device.working_hours,
                "turned_on_at": device._turned_on_at
            }

            if hasattr(device, "temperature"):
                device_data["temperature"] = device.temperature
                device_data["temperature_history"] = (
                    device.temperature_history
                )

            data.append(device_data)

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)


    def load_devices(self, filename=None):
        import json
        import time
        from pathlib import Path

        from light import Light
        from thermostat import Thermostat
        from camera import Camera
        from alarm import Alarm
        from fan import Fan

        if filename is None:
            filename = self.data_file
        else:
            filename = Path(filename).resolve()

        device_classes = {
            "Light": Light,
            "Thermostat": Thermostat,
            "Camera": Camera,
            "Alarm": Alarm,
            "Fan": Fan
        }

        def create_default_devices():
            return [
                Light("Living Room Light"),
                Thermostat("Living Room Thermostat", 25),
                Camera("Security Camera"),
                Alarm("Main Alarm"),
                Fan("Cooling Fan")
            ]

        # Read the JSON file
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)

        except FileNotFoundError:
            print("Devices file not found. Creating default devices.")
            self.devices = create_default_devices()
            self.save_devices(filename)
            return True

        except (json.JSONDecodeError, UnicodeDecodeError):
            print("Warning: Invalid JSON file. Restoring default devices.")
            self.devices = create_default_devices()
            self.save_devices(filename)
            return True

        # Accept either a list or a dictionary containing "devices"
        if isinstance(data, dict):
            data = data.get("devices")

        if not isinstance(data, list):
            print("Warning: Invalid device data. Restoring defaults.")
            self.devices = create_default_devices()
            self.save_devices(filename)
            return True

        self.devices = []
        loaded_types = set()

        for item in data:
            if not isinstance(item, dict):
                print("Warning: Skipping invalid device entry.")
                continue

            device_type = item.get("type")
            name = item.get("name", "Unknown Device")

            device_class = device_classes.get(device_type)

            if device_class is None:
                print(f"Warning: Unknown device type '{device_type}'.")
                continue

            if device_type in loaded_types:
                print(f"Warning: Duplicate device type '{device_type}'.")
                continue

            # Create the device
            if device_type == "Thermostat":
                try:
                    temperature = float(item.get("temperature", 20))
                except (ValueError, TypeError):
                    temperature = 20.0

                if not 10 <= temperature <= 35:
                    temperature = 20.0

                device = Thermostat(name, temperature)
                history = item.get("temperature_history", [temperature])

                if isinstance(history, list):
                    valid_history = []

                    for value in history:
                        try:
                            value = float(value)
                            if 10 <= value <= 35:
                                valid_history.append(value)
                        except (ValueError, TypeError):
                            continue

                    device.temperature_history = (
                        valid_history if valid_history else [temperature]
                    )
                else:
                    device.temperature_history = [temperature]

            else:
                device = device_class(name)

            # Restore accumulated working hours
            try:
                saved_hours = float(item.get("working_hours", 0.0))
                if not 0 <= saved_hours < 100000:
                    saved_hours = 0.0
            except (ValueError, TypeError):
                saved_hours = 0.0

            device.working_hours = saved_hours
            device.is_on = False
            device._turned_on_at = None

            # Restore the timer for devices that were ON
            if item.get("is_on", False) is True:
                try:
                    saved_start = float(item.get("turned_on_at"))

                    if not 0 < saved_start <= time.time():
                        saved_start = time.time()

                except (ValueError, TypeError):
                    saved_start = time.time()

                device.start_timer(started_at=saved_start)

            self.devices.append(device)
            loaded_types.add(device_type)

        # Add any missing device types
        default_devices = create_default_devices()

        for device in default_devices:
            device_type = device.__class__.__name__

            if device_type not in loaded_types:
                print(f"Missing {device_type}. Adding default device.")
                self.devices.append(device)
                loaded_types.add(device_type)

        # Save the repaired device list
        self.save_devices(filename)

        print("Device states and working hours loaded.")
        return True

