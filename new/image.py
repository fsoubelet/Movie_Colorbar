"""
Image
-----

Small module with different functions to handle parsing
of images and extracting color information from them.
"""

from loguru import logger
from PIL import Image

from new.colors import *


def get_rgb_counts_and_colors(image: Image) -> list[tuple[int, tuple[int, int, int]]]:
    """
    Get the RGB colors of an image.

    Parameters
    ----------
    image : PIL.Image
        The image to extract the colors from.

    Returns
    -------
    list[tuple[int, tuple[int, int, int]]]
        A list of the count for each color, and the RGB values
        for the given color. An entry in this list might read:
        (3378, (41, 33, 29))  # 3378 pixels with RGB values (41, 33, 29)
    """
    logger.trace("Extracting RGB pixels from Image")
    img_rgb = image.convert("RGB")
    return img_rgb.getcolors(img_rgb.size[0] * img_rgb.size[1])


def get_average_rgb(image: Image) -> tuple[float, float, float]:
    """
    Get the average R, G and B values of the colors in an image.
    The values are weighted by the number of pixels of each color.

    Parameters
    ----------
    image : PIL.Image
        The image to extract the colors from.

    Returns
    -------
    tuple[float, float, float]
        A tuple with the average R, G and B values of the image.
    """
    counts_and_colors = get_rgb_counts_and_colors(image)

    total_pixels = 0
    total_r = 0
    total_g = 0
    total_b = 0

    for count, (r, g, b) in counts_and_colors:
        total_pixels += count
        total_r += count * r
        total_g += count * g
        total_b += count * b

    avg_r = total_r / total_pixels
    avg_g = total_g / total_pixels
    avg_b = total_b / total_pixels

    return int(avg_r), int(avg_g), int(avg_b)
