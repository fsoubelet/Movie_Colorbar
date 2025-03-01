"""
Image
-----

Small module with different functions to handle parsing
of images and extracting color information from them.
"""

from PIL import Image

from new.colors import *


def get_rgb_colors(image: Image) -> list:
    """
    Get the RGB colors of an image.

    Parameters
    ----------
    image : PIL.Image
        The image to extract the colors from.

    Returns
    -------
    list
        A list of RGB colors.
    """

    # return list(image.getdata())