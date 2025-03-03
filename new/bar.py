"""
Bar
---

Module with different functions to handle splitting a
video into many images, and turning these images into
a colorbar.
"""

from pathlib import Path

from loguru import logger
from PIL import Image

from new.constants import VALID_VIDEO_EXTENSIONS
from new.constants import COMMON, HSV, HUE, KMEANS, LAB, QUANTIZED, RESIZE, RGB, RGB_SQUARED, XYZ
from new.image import (
    get_average_hsv_as_rgb,
    get_average_hue_as_rgb,
    get_average_lab_as_rgb,
    get_average_rgb,
    get_average_rgb_squared,
    get_average_xyz_as_rgb,
    get_kmeans_color_as_rgb,
    get_most_common_color_as_rgb,
    get_quantized_color_as_rgb,
    get_resized_1px_rgb,
)

# ----- Mapping methods to called function ----- #

METHOD_ACTION_MAP: dict = {
    COMMON: get_most_common_color_as_rgb,
    HSV: get_average_hsv_as_rgb,
    HUE: get_average_hue_as_rgb,
    KMEANS: get_kmeans_color_as_rgb,
    LAB: get_average_lab_as_rgb,
    QUANTIZED: get_quantized_color_as_rgb,
    RESIZE: get_resized_1px_rgb,
    RGB: get_average_rgb,
    RGB_SQUARED: get_average_rgb_squared,
    XYZ: get_average_xyz_as_rgb,
}
