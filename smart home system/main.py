
import time

from light import Light
from thermostat import Thermostat
from camera import Camera
from alarm import Alarm
from fan import Fan

from observer import TemperatureObserver
from controller import SmartHomeController
from energy import EnergyCalculator
from temperature import plot_temperature


def find_device(controller, device_class):
    """Safely find a device without raising StopIteration."""
    return next(
        (
            device for device in controller.devices
            if isinstance(device, device_class)
        ),
        None
    )

def get_device_status(device):
    if device is None:
        return "Device is unavailable."

    return device.status_report()

def control_device(device):
    if device is None:
        print("Device is unavailable.")
        return

    if device.is_on:
        device.turn_off()
    else:
        device.turn_on()

def main():
    controller = SmartHomeController()
    energy_calculator = EnergyCalculator()

    # Load saved devices. The controller handles missing
    # devices and invalid JSON.
    print(f"Loading data from: {controller.data_file}")

    try:
        controller.load_devices()
    except (OSError, ValueError) as error:
        print(f"Could not load device data: {error}")
        print("Please check the devices.json file.")
        return

    # Find devices safely.
    light = find_device(controller, Light)
    thermostat = find_device(controller, Thermostat)
    camera = find_device(controller, Camera)
    alarm = find_device(controller, Alarm)
    fan = find_device(controller, Fan)

    # Set up the temperature observer.
    temperature_observer = None

    if thermostat is not None and fan is not None:
        temperature_observer = TemperatureObserver(fan)
        thermostat.add_observer(temperature_observer)

        # Synchronize the fan with the thermostat when
        # the thermostat is ON at startup.
        if thermostat.is_on:
            temperature_observer.update(thermostat.temperature)
            controller.save_devices()

    last_save_time = time.time()

    try:
        while True:
            print("\n========== Smart Home System ==========")
            print("1. Device Status")
            print("2. Control Devices")
            print("3. Energy Report")
            print("4. Temperature History")
            print("5. Exit")
            print("=======================================")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                print("\n--- Device Status ---")
                controller.show_status()

            elif choice == "2":
                while True:
                    print("\n--- Control ---")
                    print("1. Turn on all devices")
                    print("2. Turn off all devices")
                    print("3. Change temperature")
                    print("4. Living Room Light")
                    print("5. Living Room Thermostat")
                    print("6. Security Camera")
                    print("7. Main Alarm")
                    print("8. Cooling Fan")
                    print("0. Back")

                    control_choice = input(
                        "Choose an option: "
                    ).strip()

                    if control_choice == "0":
                        break

                    elif control_choice == "1":
                        controller.turn_on_all()

                        # Notify the observer after turning
                        # everything on.
                        if (
                            thermostat is not None
                            and fan is not None
                            and temperature_observer is not None
                        ):
                            temperature_observer.update(
                                thermostat.temperature
                            )

                    elif control_choice == "2":
                        controller.turn_off_all()

                    elif control_choice == "3":
                        if thermostat is None:
                            print("Thermostat is unavailable.")
                        elif not thermostat.is_on:
                            print(
                                "Cannot change temperature. "
                                "The thermostat is OFF."
                            )
                        else:
                            temperature_input = input(
                                "Enter temperature: "
                            ).strip()

                            try:
                                new_temperature = float(
                                    temperature_input
                                )
                                thermostat.set_temperature(
                                    new_temperature
                                )
                            except ValueError:
                                print(
                                    "Invalid temperature. "
                                    "Please enter a number."
                                )

                    elif control_choice == "4":
                        control_device(light)

                    elif control_choice == "5":
                        control_device(thermostat)

                    elif control_choice == "6":
                        control_device(camera)

                    elif control_choice == "7":
                        control_device(alarm)

                    elif control_choice == "8":
                        control_device(fan)

                    else:
                        print(
                            "Invalid option. "
                            "Please choose again."
                        )

                    # Save after each control action.
                    controller.save_devices()

            elif choice == "3":
                print("\n--- Energy Report ---")
                controller.show_status()

                energy_calculator.calculate_all(
                    controller.devices
                )

            elif choice == "4":
                if thermostat is None:
                    print("Thermostat is unavailable.")
                else:
                    plot_temperature(
                        thermostat.temperature_history
                    )

            elif choice == "5":
                controller.save_devices()
                print("Data saved. Goodbye!")
                break

            else:
                print("Invalid option. Please choose again.")

            # Save data after each main-menu action.
            current_time = time.time()

            if current_time - last_save_time >= 10:
                controller.save_devices()
                last_save_time = current_time

    except (KeyboardInterrupt, EOFError):
        print("\nProgram interrupted.")

    finally:
        controller.save_devices()
        print("Device data saved.")


if __name__ == "__main__":
    main()
