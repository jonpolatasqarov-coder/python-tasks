from light import Light
from thermostat import Thermostat
from camera import Camera
from alarm import Alarm
from fan import Fan
from observer import TemperatureObserver
from controller import SmartHomeController
from energy import EnergyCalculator
from temperature import plot_temperature


controller = SmartHomeController()

loaded = controller.load_devices()

if not loaded:
    light = Light("Living Room Light")
    thermostat = Thermostat("Living Room Thermostat", 25)
    camera = Camera("Security Camera")
    alarm = Alarm("Main Alarm")
    fan = Fan("Cooling Fan")

    controller.add_device(light)
    controller.add_device(thermostat)
    controller.add_device(camera)
    controller.add_device(alarm)
    controller.add_device(fan)

else:
    light = next(
        device for device in controller.devices
        if isinstance(device, Light)
    )

    thermostat = next(
        device for device in controller.devices
        if isinstance(device, Thermostat)
    )

    camera = next(
        device for device in controller.devices
        if isinstance(device, Camera)
    )

    alarm = next(
        device for device in controller.devices
        if isinstance(device, Alarm)
    )

    fan = next(
        device for device in controller.devices
        if isinstance(device, Fan)
    )


temperature_observer = TemperatureObserver(fan)
thermostat.add_observer(temperature_observer)

energy_calculator = EnergyCalculator()


while True:
    print("\n===== SMART HOME =====")
    print("1. Status")
    print("2. Control")
    print("3. Report")
    print("4. Temperature Graph")
    print("0. Exit")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        print("\n--- Device Status ---")
        controller.show_status()

    elif choice == "2":
        print("\n--- Control ---")
        print("1. Turn on all devices")
        print("2. Turn off all devices")
        print("3. Change temperature")
        print("0. Back")

        control_choice = input("Choose an option: ").strip()

        if control_choice == "1":
            controller.turn_on_all()

        elif control_choice == "2":
            controller.turn_off_all()

        elif control_choice == "3":
            try:
                temperature = float(
                    input("Enter temperature: ")
                )

                thermostat.set_temperature(temperature)

            except ValueError:
                print("Invalid temperature.")

        elif control_choice == "0":
            continue

        else:
            print("Invalid option.")

    elif choice == "3":
        print("\n--- Report ---")
        controller.show_status()

        try:
            hours = float(
                input("\nEnter working hours: ")
            )

            if hours < 0:
                print("Hours cannot be negative.")
                continue

            print("\n--- Energy Consumption ---")

            energy_calculator.calculate_all(
                controller.devices,
                hours
            )

        except ValueError:
            print("Invalid number of hours.")

    elif choice == "4":
        plot_temperature(
            thermostat.temperature_history
        )

    elif choice == "0":
        controller.save_devices()
        print("Data saved. Goodbye!")
        break

    else:
        print("Invalid option.")