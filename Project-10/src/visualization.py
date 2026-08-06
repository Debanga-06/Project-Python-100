import numpy as np
import matplotlib.pyplot as plt


def plot_rgb_histogram(image):
    """
    Generate RGB Histogram.
    """

    image_np = np.array(image)

    fig, ax = plt.subplots(figsize=(6, 4))

    colors = ("red", "green", "blue")

    for i, color in enumerate(colors):

        hist, bins = np.histogram(
            image_np[:, :, i],
            bins=256,
            range=(0, 256)
        )

        ax.plot(
            hist,
            color=color,
            linewidth=2
        )

    ax.set_title("RGB Histogram")
    ax.set_xlabel("Pixel Value")
    ax.set_ylabel("Frequency")

    ax.grid(alpha=0.3)

    return fig


def plot_brightness(brightness):
    """
    Brightness Progress Chart.
    """

    fig, ax = plt.subplots(figsize=(5, 1.2))

    ax.barh(
        ["Brightness"],
        [brightness]
    )

    ax.set_xlim(0, 255)

    return fig


def plot_rgb_bar(avg_rgb):
    """
    Average RGB Bar Chart.
    """

    fig, ax = plt.subplots(figsize=(5, 3))

    ax.bar(
        ["Red", "Green", "Blue"],
        [
            avg_rgb["R"],
            avg_rgb["G"],
            avg_rgb["B"]
        ]
    )

    ax.set_title("Average RGB Values")

    return fig