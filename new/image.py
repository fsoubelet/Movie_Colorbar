"""
Image
-----

Small module with different functions to handle parsing
of images and extracting color information from them.
"""

from PIL import Image
from loguru import logger
from new.colors import *


def get_rgb_colors_and_counts(image: Image) -> list[tuple[int, tuple[int, int, int]]]:
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

