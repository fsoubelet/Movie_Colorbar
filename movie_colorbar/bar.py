"""
Extract
-------

Module with functions to handle the creation of
a colorbar from images extracted from a video.
"""

from pathlib import Path

from loguru import logger
from PIL import Image

# Try to import joblib (optional), set a flag on availability
try:
    from joblib import Parallel, delayed

    JOBLIB_AVAILABLE: bool = True
except ImportError:
    JOBLIB_AVAILABLE: bool = False

from movie_colorbar.constants import Methods
from movie_colorbar.image import (
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
    Methods.common: get_most_common_color_as_rgb,
    Methods.hsv: get_average_hsv_as_rgb,
    Methods.hue: get_average_hue_as_rgb,
    Methods.kmeans: get_kmeans_color_as_rgb,
    Methods.lab: get_average_lab_as_rgb,
    Methods.quantized: get_quantized_color_as_rgb,
    Methods.resize: get_resized_1px_rgb,
    Methods.rgb: get_average_rgb,
    Methods.rgb_squared: get_average_rgb_squared,
    Methods.xyz: get_average_xyz_as_rgb,
}

# ----- Functions to Turn Create Colorbars ----- #


def create_colorbar_from_images(images: list[Path], method: str) -> Image:
    """
    Create a colorbar from the computed colors of various
    images, the paths of which are provided (they should
    be files on disk).

    Note
    ----
    Currently, the image files are loaded with PIL and
    all resized to a 25x25 pixels image. This should be
    a parameter in the future.

    Parameters
    ----------
    images : list[pathlib.Path]
        List of paths to the images.
    method : str
        Method to use to compute the color from
        each image.

    Returns
    -------
    PIL.Image
        A PIL.Image of the colorbar.
    """
    logger.debug(f"Extracting colors from images, according to method {method}")

    def process_image(img_path: Path) -> tuple[int, int, int]:
        """Load a single image and compute its color according to method."""
        with Image.open(img_path) as img:
            img_resized = img.resize((25, 25))
            return METHOD_ACTION_MAP[method](img_resized)

    # Process all images - either in parallel if joblib is
    # available, or sequentially otherwise
    if JOBLIB_AVAILABLE:
        logger.debug("Using joblib to parallelize image processing, n_jobs=-2")
        bar_colors = Parallel(n_jobs=-2)(delayed(process_image)(img) for img in images)
    else:
        logger.debug("Joblib unavailable, processing images sequentially")
        bar_colors = [process_image(img) for img in images]

    logger.info("Assembling colorbar from extracted colors")

    width = len(bar_colors)
    height = max([1, int(width / 2.5)])  # ensure height is at least 1
    bar_img = Image.new(mode="RGB", size=(width, height))  # blank image with dimensions

    # Prepare color data (we're in RGB mode) for the colorbar
    bar_data = [rgb for rgb in bar_colors] * height  # repeat colors for all rows
    bar_img.putdata(bar_data)  # fill the image
    return bar_img
