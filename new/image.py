"""
Image
-----

Small module with different functions to handle parsing
of images and extracting color information from them.
"""

from loguru import logger
from PIL import Image

from new.colors import convert_hsv_to_rgb, convert_rgb_to_hsv


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


def get_average_rgb(image: Image) -> tuple[int, int, int]:
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
    logger.trace("Computing average RGB components of the image")
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


def get_average_rgb_squared(image: Image) -> tuple[int, int, int]:
    """
    Get the squared averaged R, G and B values of the colors in an image.
    The values are weighted by the number of pixels of each color.

    Parameters
    ----------
    image : PIL.Image
        The image to extract the colors from.

    Returns
    -------
    tuple[float, float, float]
        A tuple with the squared averaged R, G and B values of the image.
    """
    counts_and_colors = get_rgb_counts_and_colors(image)
    logger.trace("Computing square-averaged RGB components of the image")
    total_pixels = 0
    total_r2 = 0
    total_g2 = 0
    total_b2 = 0

    for count, (r, g, b) in counts_and_colors:
        total_pixels += count
        total_r2 += count * r**2
        total_g2 += count * g**2
        total_b2 += count * b**2

    avg_r2 = total_r2 / total_pixels
    avg_g2 = total_g2 / total_pixels
    avg_b2 = total_b2 / total_pixels

    return int(avg_r2**0.5), int(avg_g2**0.5), int(avg_b2**0.5)


def get_average_hsv(image: Image) -> tuple[int, int, int]:
    """
    Get the average H, S and V values of the colors in an image,
    as an RGB color to be displayed.

    Parameters
    ----------
    image : PIL.Image
        The image to extract the colors from.

    Returns
    -------
    tuple[float, float, float]
        A tuple with the R, G, B values corresponding to the
        average HSV color of the image.
    """
    counts_and_colors = get_rgb_counts_and_colors(image)
    logger.trace("Computing average HSV components of the image")
    total_pixels = 0
    total_h = 0
    total_s = 0
    total_v = 0

    for count, (r, g, b) in counts_and_colors:
        # Get HSV values from RGB - colorsys wants RGB in [0, 1] range
        h, s, v = convert_rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        total_pixels += count
        total_h += count * h
        total_s += count * s
        total_v += count * v

    avg_h = total_h / total_pixels
    avg_s = total_s / total_pixels
    avg_v = total_v / total_pixels

    # Get the corresponding RGB values for the average HSV color and
    # scale them back to [0, 255] range (colorsys works in [0, 1])
    avg_r, avg_g, avg_b = convert_hsv_to_rgb(avg_h, avg_s, avg_v)
    return int(avg_r * 255), int(avg_g * 255), int(avg_b * 255)
