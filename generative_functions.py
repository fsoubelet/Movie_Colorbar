import colorsys
import math
import random
from PIL import Image


def get_rgb_colors(source_image: Image):
    """
    Docstring.
    :param source_image:
    :return:
    """
    image_rgb = source_image.convert("RGB")
    return image_rgb.getcolors(image_rgb.size[0] * image_rgb.size[1])


def gen_avg_rgb(source_image: Image) -> tuple:
    """
    Docstring.
    :param source_image:
    :return:
    """
    colors = get_rgb_colors(source_image)
    return tuple([sum([y[1][x] * y[0] for y in colors]) / sum([z[0] for z in colors]) for x in range(3)])


def gen_avg_rgb_squared(source_image: Image) -> tuple:
    """
    Docstring.
    :param source_image:
    :return:
    """
    colors = get_rgb_colors(source_image)
    average = [sum([(y[1][x] ** 2) * y[0] for y in colors]) / float(sum([z[0] for z in colors])) for x in range(3)]
    return tuple([int(math.sqrt(x)) for x in average])


def gen_avg_hsv(source_image: Image) -> tuple:
    """
    Docstring.
    :param source_image:
    :return:
    """
    colors = get_rgb_colors(source_image)
    colors_hsv = [(w, colorsys.rgb_to_hls(*[y / 255.0 for y in x])) for w, x in colors]
    average = [sum([y[1][x] * y[0] for y in colors_hsv]) / sum([z[0] for z in colors_hsv]) for x in range(3)]

    average_rgb = colorsys.hsv_to_rgb(*average)
    return tuple([int(x * 255) for x in average_rgb])


def gen_avg_hue(source_image: Image) -> tuple:
    """
    Docstring.
    :param source_image:
    :return:
    """
    average_hsv = gen_avg_hsv(source_image)
    average_hsv = colorsys.rgb_to_hsv(*[x / 255.0 for x in average_hsv])

    # highest value and saturation
    average_hsv = [average_hsv[0], 1.0, 1.0]
    average_rgb = colorsys.hsv_to_rgb(*average_hsv)
    return tuple([int(x * 255) for x in average_rgb])


def calculate_distance_between_two_3d_points(point_1, point_2) -> float:
    """
    Docstring.
    :param point_1:
    :param point_2:
    :return:
    """
    return math.sqrt(sum([(point_1[x] - point_2[x]) ** 2 for x in range(len(point_1))]))


def kmeans(source_image: Image) -> list:
    """
    Docstring.
    :param source_image:
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
    return centers[sorted(range(num_centers), key=lambda x: sum([y[0] for y in color_groups[x]]))[-1]]


def gen_common(source_image: Image):
    """
    Docstring.
    :param source_image:
    :return:
    """
    colors = source_image.getcolors(source_image.size[0] * source_image.size[1])
    return sorted(colors)[-1][1]


# xyz conversions refer to D65/2 standard illuminant
def rgb_to_xyz(source_color) -> tuple:
    """
    Docstring.
    :param source_color:
    :return:
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
    Docstring.
    :param source_xyz:
    :return:
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
    Docstring.
    :param source_xyz:
    :return:
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
    Docstring.
    :param source_lab:
    :return:
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


def gen_avg_xyz(source_image: Image) -> tuple:
    """
    Docstring.
    :param source_image:
    :return:
    """
    colors = get_rgb_colors(source_image)
    colors_xyz = [(w, rgb_to_xyz(x)) for (w, x) in colors]

    average = tuple([sum([y[1][x] * y[0] for y in colors_xyz]) / sum([z[0] for z in colors_xyz]) for x in range(3)])
    return xyz_to_rgb(average)


def gen_avg_lab(source_image: Image) -> tuple:
    """
    Docstring.
    :param source_image:
    :return:
    """
    colors = get_rgb_colors(source_image)
    colors_lab = [(w, xyz_to_lab(rgb_to_xyz(x))) for (w, x) in colors]
    average = tuple([sum([y[1][x] * y[0] for y in colors_lab]) / sum([z[0] for z in colors_lab]) for x in range(3)])
    return xyz_to_rgb(lab_to_xyz(average))


def gen_resized_color(source_image: Image):
    """
    Use Pillow's image resizer to reduce the image to 1px by 1px, and return that color.
    :param source_image:
    :return:
    """
    return source_image.convert("RGB").resize((1, 1)).getcolors(1)[0][1]


def gen_quantized_color(source_image: Image):
    """
    Use Pillow's color quantization to reduce the image to one color, then return that color.
    :param source_image:
    :return:
    """
    return source_image.quantize(1).convert("RGB").getcolors()[0][1]
