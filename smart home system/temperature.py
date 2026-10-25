
import matplotlib.pyplot as plt


def plot_temperature(temperatures):
    if not temperatures:
        print("No temperature data available.")
        return

    measurements = range(1, len(temperatures) + 1)

    plt.figure("Temperature History", figsize=(9, 5))

    plt.plot(
        measurements,
        temperatures,
        marker="o",
        linestyle="-",
        label="Temperature"
    )

    plt.title("Temperature History")
    plt.xlabel("Measurement Number")
    plt.ylabel("Temperature (°C)")

    plt.xticks(list(measurements))
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()

    plt.show()
