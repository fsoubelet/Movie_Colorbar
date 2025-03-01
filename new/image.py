"""
Image
-----

Small module with different functions to handle parsing
of images and extracting color information from them.
"""

from PIL import Image
from loguru import logger
from new.colors import *


def get_rgb_colors(image: Image) -> list[tuple[int, int, int]]:
    """
    Get the RGB colors of an image.

    Parameters
    ----------
    image : PIL.Image
        The image to extract the colors from.

    Returns
    -------
    list
        A list of RGB colors as tuples.
    """
    logger.trace("Extracting RGB pixels from Image")
    img_rgb = image.convert("RGB")
    return list(img_rgb.getdata())
