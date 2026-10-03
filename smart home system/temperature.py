import matplotlib.pyplot as plt


def plot_temperature(temperatures):
    measurements = range(1, len(temperatures) + 1)

    plt.figure("Temperature History")

    plt.plot(
        measurements,
        temperatures,
        marker="o"
    )

    plt.title("Temperature History")
    plt.xlabel("Measurement")
    plt.ylabel("Temperature (°C)")
    plt.grid()

    plt.show()