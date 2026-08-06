from PIL import Image
import numpy as np
import cv2


def get_image_details(image, uploaded_file):
    """
    Returns image information.
    """

    width, height = image.size

    return {
        "width": width,
        "height": height,
        "mode": image.mode,
        "format": image.format,
        "size_kb": round(uploaded_file.size / 1024, 2),
    }


def image_to_numpy(image):
    """
    Converts PIL image to NumPy array.
    """
    return np.array(image)


def resize_image(image, width=224, height=224):
    """
    Resize image for AI model.
    """
    return image.resize((width, height))


def grayscale_image(image):
    """
    Convert image to grayscale.
    """
    image_np = np.array(image)

    gray = cv2.cvtColor(
        image_np,
        cv2.COLOR_RGB2GRAY
    )

    return gray


def edge_detection(image):
    """
    Detect edges using Canny algorithm.
    """

    image_np = np.array(image)

    gray = cv2.cvtColor(
        image_np,
        cv2.COLOR_RGB2GRAY
    )

    edges = cv2.Canny(
        gray,
        100,
        200
    )

    return edges


def blur_image(image):
    """
    Apply Gaussian Blur.
    """

    image_np = np.array(image)

    blur = cv2.GaussianBlur(
        image_np,
        (9, 9),
        0
    )

    return blur


def calculate_brightness(image):
    """
    Returns average brightness.
    """

    gray = grayscale_image(image)

    return round(
        np.mean(gray),
        2
    )


def calculate_contrast(image):
    """
    Returns image contrast.
    """

    gray = grayscale_image(image)

    return round(
        np.std(gray),
        2
    )


def average_rgb(image):
    """
    Returns average RGB values.
    """

    image_np = np.array(image)

    r = round(np.mean(image_np[:, :, 0]), 2)
    g = round(np.mean(image_np[:, :, 1]), 2)
    b = round(np.mean(image_np[:, :, 2]), 2)

    return {
        "R": r,
        "G": g,
        "B": b,
    }