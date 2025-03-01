"""
Image
-----

Small module with different functions to handle parsing
of images and extracting color information from them.
"""

import random

from loguru import logger
from PIL import Image

from new.colors import cs_hsv_to_rgb, cs_rgb_to_hsv
from new.jit import maybe_jit


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


def get_average_hsv_as_rgb(image: Image) -> tuple[int, int, int]:
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
        h, s, v = cs_rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        total_pixels += count
        total_h += count * h
        total_s += count * s
        total_v += count * v

    avg_h = total_h / total_pixels
    avg_s = total_s / total_pixels
    avg_v = total_v / total_pixels

    # Get the corresponding RGB values for the average HSV color and
    # scale them back to [0, 255] range (colorsys works in [0, 1])
    avg_r, avg_g, avg_b = cs_hsv_to_rgb(avg_h, avg_s, avg_v)
    return int(avg_r * 255), int(avg_g * 255), int(avg_b * 255)


def get_average_hue(image: Image) -> tuple[int, int, int]:
    """
    Get the average hue of the colors in an image,
    as an RGB color to be displayed.

    Parameters
    ----------
    image : PIL.Image
        The image to extract the colors from.

    Returns
    -------
    tuple[int, int, int]
        A tuple with the R, G, B values corresponding to the
        average hue color of the image.
    """
    logger.trace("Computing average hue of the image")

    # Get RGB representation of average HSV color
    avg_hsv_as_rgb = get_average_hsv_as_rgb(image)

    # Convert the average RGB to the [0, 1] scale required by
    # the HSV conversion function from colorsys (JIT-compiled)
    scaled_avg = tuple(val / 255.0 for val in avg_hsv_as_rgb)
    avg_hsv = cs_rgb_to_hsv(*scaled_avg)

    # Use the hue from avg_hsv with full saturation and brightness
    # and convert to get the RGB representation
    hue_color_hsv = (avg_hsv[0], 1.0, 1.0)
    hue_color_rgb = cs_hsv_to_rgb(*hue_color_hsv)

    # Scale the RGB values back to [0, 255] before returning
    return tuple(int(val * 255) for val in hue_color_rgb)


def get_kmeans_color(image: Image) -> tuple[int, int, int]:
    """
    Compute the dominant (average) color of an image using a simplified
    k-means algorithm. Returns the RGB color of the dominant average.

    The function extracts the weighted RGB colors from the image and applies
    k-means clustering  (with a default of 5 clusters) to group similar colors.
    It then returns the center of the cluster with the largest total pixel count
    as the dominant color.

    Parameters
    ----------
    image : PIL.Image
        The image to extract the colors from.

    Returns
    -------
    tuple[int, int, int]
        A tuple with the R, G, B values corresponding to
        the kmean-average color of the image.
    """
    counts_and_colors = get_rgb_counts_and_colors(image)
    logger.trace("Starting k-means algorithm, defaulting to 5 clusters")

    # Number of clusters (centers) to use.
    nclusters = 5
    centers: list[tuple[int, int, int]] = []  # holds RGB colors

    # If there are fewer unique colors than k, use all available
    # colors, and naturally the centers are the unique colors
    logger.trace("Checking number of colors vs number of clusters")
    ncolors = len(counts_and_colors)
    if ncolors < nclusters:
        nclusters = ncolors
        centers = [rgb_color for _, rgb_color in counts_and_colors]
        logger.trace("Set number of clusters to number of unique colors")
    else:
        # Randomly select nclusters distinct starting centers.
        logger.trace("Selecting random starting centers")
        while len(centers) < nclusters:
            rgb_candidate = random.choice(counts_and_colors)[1]
            if rgb_candidate not in centers:
                centers.append(rgb_candidate)

    # Iterate to update centers (up to 20 iterations)
    logger.trace("Iterating on means")
    for iteration in range(20):
        previous_centers = centers.copy()
        color_groups = [[] for _ in range(nclusters)]

        # Assign each color to the closest center.
        for count, color in counts_and_colors:
            logger.trace("Determining closest center for current color")
            distances = [euclidean_distance_3d(center, color) for center in centers]
            closest_index = distances.index(min(distances))
            color_groups[closest_index].append((count, color))

        # Update centers as weighted averages of the groups
        logger.trace("Calculating new centers from groups' weighted averages")
        new_centers: list[tuple[int, int, int]] = []
        for i in range(nclusters):
            group = color_groups[i]
            if group:
                total_count = sum(count for count, _ in group)
                avg_color = tuple(
                    sum(count * color[channel] for count, color in group) / total_count
                    for channel in range(3)
                )
                new_centers.append(avg_color)
            else:
                # If a cluster is empty, retain the previous center
                new_centers.append(centers[i])

        # We update the centers with the newly determined ones
        centers = new_centers

        # We compute the total movement of centers
        logger.trace("Calculating total shift of centers")
        total_shift = sum(
            euclidean_distance_3d(centers[i], previous_centers[i]) for i in range(nclusters)
        )

        logger.trace(f"Iteration {iteration + 1}: Total center shift = {total_shift}")
        if total_shift < 4:
            logger.trace("Converged")
            break

    # Select the cluster with the largest total pixel count
    logger.trace("Selecting the dominant color as center with the largest pixel count")
    cluster_counts = [sum(count for count, _ in group) for group in color_groups]
    dominant_index = cluster_counts.index(max(cluster_counts))
    dominant_color = centers[dominant_index]

    return tuple(int(channel) for channel in dominant_color)


def get_quantized_color_as_rgb(image: Image) -> tuple[int, int, int]:
    """
    Reduce the image to a single dominant color using Pillow's
    quantization method. Pillow's built-in color quantization
    compresses the image to a  palette containing only one color.
    We then retrieve the equivalent RGB value of that color, which
    represents the most prominent color in the image.

    Parameters
    ----------
    image : PIL.Image
        The image to extract the color from.

    Returns
    -------
    tuple[int, int, int]
        A tuple containing the RGB values (R, G, B) of the quantized
        dominant color.
    """
    logger.trace("Quantizing the image to a single dominant color")
    quantized_image_rgb = image.quantize(colors=1).convert("RGB")

    # Get the dominant color and return it directly
    # (.getcolors() returns a list of (count, color))
    return quantized_image_rgb.getcolors()[0][1]


# ----- Some useful JIT-compiled (maybe) functions ----- #


@maybe_jit
def euclidean_distance_3d(
    point1: tuple[float, float, float], point2: tuple[float, float, float]
) -> float:
    """
    Calculate the Euclidean distance between two 3D points.

    Parameters
    ----------
    point1 : tuple[float, float, float]
        The first 3D point's coordinates.
    point2 : tuple[float, float, float]
        The second 3D point's coordinates.

    Returns
    -------
    float
        The Euclidean distance between the two points.
    """
    dx = point1[0] - point2[0]
    dy = point1[1] - point2[1]
    dz = point1[2] - point2[2]
    return (dx**2 + dy**2 + dz**2) ** 0.5
