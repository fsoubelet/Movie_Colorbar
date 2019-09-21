"""
Generative functions
--------------------

Created on 2019.08.28
:author: Felix Soubelet

Small module with different functions to handle color calculations on parsed images.
"""
import colorsys
import math
import random
from PIL import Image


def get_rgb_colors(source_image: Image) -> list:
    """
    Get all the rgb colors of an image.
    :param source_image: Pillow.Image instance.
    :return: Returns the list of RGB colors present in the image.
    """
    image_rgb = source_image.convert("RGB")
    return image_rgb.getcolors(image_rgb.size[0] * image_rgb.size[1])


def get_avg_rgb(source_image: Image) -> tuple:
    """
    Get the average of each R, G and B of the colors in an image.
    :param source_image: Pillow.Image instance.
    :return: a tuple of R, G and B calculated averages.
    """
    colors = get_rgb_colors(source_image)
    rgb_colors = tuple([sum([y[1][x] * y[0] for y in colors]) / sum([z[0] for z in colors]) for x in range(3)])
    return tuple([int(e) for e in rgb_colors])


def get_avg_rgb_squared(source_image: Image) -> tuple:
    """
    Get the squared average of each R, G and B of the colors in an image.
    :param source_image: Pillow.Image instance.
    :return: a tuple of R, G and B calculated squared averages.
    """
    colors = get_rgb_colors(source_image)
    average = [sum([(y[1][x] ** 2) * y[0] for y in colors]) / float(sum([z[0] for z in colors])) for x in range(3)]
    return tuple([int(math.sqrt(x)) for x in average])


def get_avg_hsv(source_image: Image) -> tuple:
    """
    Get the average of each H, S and V of the colors in an image, as RGB.
    :param source_image: Pillow.Image instance.
    :return: a tuple with average H, S and V of the image, as converted to RGB.
    """
    colors = get_rgb_colors(source_image)
    colors_hsv = [(w, colorsys.rgb_to_hls(*[y / 255.0 for y in x])) for w, x in colors]
    average = [sum([y[1][x] * y[0] for y in colors_hsv]) / sum([z[0] for z in colors_hsv]) for x in range(3)]

    average_rgb = colorsys.hsv_to_rgb(*average)
    return tuple([int(x * 255) for x in average_rgb])


def get_avg_hue(source_image: Image) -> tuple:
    """
    Get the average hue of the colors in an image, as RGB.
    :param source_image: Pillow.Image instance.
    :return: a tuple with average hue fo the image, as converted to RGB.
    """
    average_hsv = get_avg_hsv(source_image)
    average_hsv = colorsys.rgb_to_hsv(*[x / 255.0 for x in average_hsv])

    # Highest value and saturation
    average_hsv = [average_hsv[0], 1.0, 1.0]
    average_rgb = colorsys.hsv_to_rgb(*average_hsv)
    return tuple([int(x * 255) for x in average_rgb])


def calculate_distance_between_two_3d_points(point_1, point_2) -> float:
    """
    Quite explicit.
    :param point_1: Point 1 coordinates.
    :param point_2: Point 2 coordinates.
    :return: Distance between those two points.
    """
    return math.sqrt(sum([(point_1[x] - point_2[x]) ** 2 for x in range(len(point_1))]))


def get_kmeans_color(source_image: Image) -> tuple:
    """
    Oh boy. I didn't write this...
    :param source_image: Pillow.Image instance.
    :return:
    """
    image_rgb = source_image.convert("RGB")
    colors = image_rgb.getcolors(image_rgb.size[0] * image_rgb.size[1])
    num_centers = 5
    centers = []

    # Check if number of colors is less than number of centers
    if len(colors) < num_centers:
        centers = [x for _, x in colors]
        num_centers = len(colors)

    # Choosing random starting centers
    while len(centers) != num_centers:
        random_color = random.choice(colors)[1]
        if random_color not in centers:
            centers.append(random_color)

    for _ in range(20):
        previous_centers = centers[:]
        color_groups = [[] for _ in range(num_centers)]
        for ele in colors:
            # Calculate the center with the smallest distance to the color
            min_dist_index = sorted(
                range(num_centers), key=lambda x: calculate_distance_between_two_3d_points(centers[x], ele[1]))[0]
            # Appending the color to the group
            color_groups[min_dist_index].append(ele)
        # Calculate new centers
        centers = [tuple([sum([y[1][x] * y[0] for y in group]) / sum([z[0] for z in group]) for x in range(3)])
                   for group in color_groups]
        # Calculate center difference
        diff = sum(
            [calculate_distance_between_two_3d_points(centers[x], previous_centers[x]) for x in range(num_centers)])
        # Breakoff point
        if diff < 4:
            break

    # Getting group with largest number of colors
    group = centers[sorted(range(num_centers), key=lambda x: sum([y[0] for y in color_groups[x]]))[-1]]
    return tuple([int(e) for e in group])


def get_most_common(source_image: Image) -> list:
    """
    Get the most common color in this image, as RGB.
    :param source_image: Pillow.Image instance.
    :return: a tuple with the R, G and B values of the most common color in the image.
    """
    colors = source_image.getcolors(source_image.size[0] * source_image.size[1])
    return sorted(colors)[-1][1]


def rgb_to_xyz(source_color) -> tuple:
    """
    Converts a color from the RGB to the CIE XYZ 1931 colorspace.
    :param source_color: a tuple with R, G and B values of the color.
    :return: a tuple with the X, Y, Z values of the color.
    """
    colors = [x / 255.0 for x in source_color]

    for index in range(3):
        if colors[index] > 0.04045:
            colors[index] = ((colors[index] + 0.055) / 1.055) ** 2.4
        else:
            colors[index] /= 12.92
    colors = [100 * x for x in colors]

    x_val = colors[0] * 0.4124 + colors[1] * 0.3575 + colors[2] * 0.1805
    y_val = colors[0] * 0.2126 + colors[1] * 0.7152 + colors[2] * 0.0722
    z_val = colors[0] * 0.0193 + colors[1] * 0.1192 + colors[2] * 0.9505
    return x_val, y_val, z_val


def xyz_to_rgb(source_xyz) -> tuple:
    """
    Converts a color from the CIE XYZ 1931 to the RGB colorspace.
    :param source_xyz: a tuple with X, Y and Z values of the color.
    :return: a tuple with the R, G and B values of the color.
    """
    xyz = [x / 100 for x in source_xyz]
    r_val = xyz[0] * 3.2406 + xyz[1] * -1.5372 + xyz[2] * -0.4986
    g_val = xyz[0] * -0.9689 + xyz[1] * 1.8758 + xyz[2] * 0.0415
    b_val = xyz[0] * 0.0557 + xyz[1] * -0.2040 + xyz[2] * 1.0570
    color = [r_val, g_val, b_val]

    for index in range(3):
        if color[index] > 0.0031308:
            color[index] = 1.055 * (color[index] ** (1 / 2.4)) - 0.055
        else:
            color[index] *= 12.92
    return tuple([int(x * 255) for x in color])


def xyz_to_lab(source_xyz) -> tuple:
    """
    Converts a color from the CIE XYZ 1931 to the LAB colorspace.
    :param source_xyz: a tuple with X, Y, and Z values of the color.
    :return: a tuple with the Lightness, A channel and B channel values of the color.
    """
    xyz = [source_xyz[0] / 95.047, source_xyz[1] / 100.0, source_xyz[2] / 108.883]

    for index in range(3):
        if xyz[index] > 0.008856:
            xyz[index] = xyz[index] ** (1.0 / 3)
        else:
            xyz[index] = (7.787 * xyz[index]) + (16.0 / 116)

    l_val = (116 * xyz[1]) - 16
    a_val = 500 * (xyz[0] - xyz[1])
    b_val = 200 * (xyz[1] - xyz[2])
    return l_val, a_val, b_val


def lab_to_xyz(source_lab) -> tuple:
    """
    Converts a color from the LAB to the CIE XYZ 1931 colorspace.
    :param source_lab: a tuple with the Lightness, A channel and B channel values of the color.
    :return: a tuple with X, Y, and Z values of the color.
    """
    y_val = (source_lab[0] + 16) / 116.0
    x_val = source_lab[1] / 500 + y_val
    z_val = y_val - source_lab[2] / 200.0
    xyz = [x_val, y_val, z_val]

    for index in range(3):
        if xyz[index] ** 3 > 0.008856:
            xyz[index] = xyz[index] ** 3
        else:
            xyz[index] = (xyz[index] - 16 / 116.0) / 7.787
    return xyz[0] * 95.047, xyz[1] * 100, xyz[2] * 108.883


def get_avg_xyz(source_image: Image) -> tuple:
    """
    Get the average of each X, Y and Z of the colors in an image.
    :param source_image: Pillow.Image instance.
    :return: a tuple with the average X, Y and Z values of the image.
    """
    colors = get_rgb_colors(source_image)
    colors_xyz = [(w, rgb_to_xyz(x)) for (w, x) in colors]

    average = tuple([sum([y[1][x] * y[0] for y in colors_xyz]) / sum([z[0] for z in colors_xyz]) for x in range(3)])
    return xyz_to_rgb(average)


def get_avg_lab(source_image: Image) -> tuple:
    """
    Get the average of each L, A and B values of the colors in an image.
    :param source_image: Pillow.Image instance.
    :return: a tuple with the average L, A and B values of the image.
    """
    colors = get_rgb_colors(source_image)
    colors_lab = [(w, xyz_to_lab(rgb_to_xyz(x))) for (w, x) in colors]
    average = tuple([sum([y[1][x] * y[0] for y in colors_lab]) / sum([z[0] for z in colors_lab]) for x in range(3)])
    return xyz_to_rgb(lab_to_xyz(average))


def get_resized_color(source_image: Image) -> list:
    """
    Use Pillow's image resizer to reduce the image to 1px by 1px, and return the corresponding color.
    :param source_image: Pillow.Image instance.
    :return: a tuple with the R, G and B values of the image as 1 by 1 pixel.
    """
    return source_image.convert("RGB").resize((1, 1)).getcolors(1)[0][1]


def get_quantized_color(source_image: Image) -> list:
    """
    Use Pillow's color quantization to reduce the image to one color, then return that color.
    :param source_image: Pillow.Image instance.
    :return: a tuple with the R, G and B values of the image reduced to one collor by Pillow.
    """
    return source_image.quantize(1).convert("RGB").getcolors()[0][1]
