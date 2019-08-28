import argparse
import os
import subprocess
from pathlib import Path
from halo import Halo
from PIL import Image
from generative_functions import (
    gen_avg_rgb,
    gen_avg_rgb_squared,
    gen_avg_hsv,
    gen_avg_hue,
    kmeans,
    gen_common,
    gen_avg_xyz,
    gen_avg_lab,
    gen_resized_color,
    gen_quantized_color,
)


def apply_method(method: str, source_image: Image):
    """
    Docstring.
    :param method:
    :param source_image:
    :return:
    """
    if method.lower == "rgb":
        return gen_avg_rgb(source_image)
    elif method.lower() == "hsv":
        return gen_avg_hsv(source_image)
    elif method.lower() == "hue":
        return gen_avg_hue(source_image)
    elif method.lower() == "kmeans":
        return kmeans(source_image)
    elif method.lower() == "common":
        return gen_common(source_image)
    elif method.lower() == "xyz":
        return gen_avg_xyz(source_image)
    elif method.lower() == "lab":
        return gen_avg_lab(source_image)
    elif method.lower() == "rgbsquared":
        return gen_avg_rgb_squared(source_image)
    elif method.lower() == "resize":
        return gen_resized_color(source_image)
    elif method.lower() == "quantized":
        return gen_quantized_color(source_image)
    else:
        return gen_avg_rgb(source_image)


def _parse_args():
    """
    Simple argument parser to make life easier in the command-line.
    :return:
    """
    parser = argparse.ArgumentParser(description="Getting your average colorbar.")
    parser.add_argument(
        "-t", "--title", dest="title", default="output", type=str, help="Filename for output.", required=True
    )
    parser.add_argument(
        "-m",
        "--method",
        dest="method",
        default="rgbsquared",
        type=str,
        help="""Method to use to calculate the average color.
        Options are: rgb, hsv, hue, kmeans, common, lab, xyz, rgbsquared, resize, quantize.""",
        required=True,
    )
    parser.add_argument(
        "-s",
        "--source-file",
        dest="source_file",
        default=".",
        type=str,
        help="Path to source video file to get the images from.",
        required=True,
    )
    parser.add_argument(
        "-f",
        "--fps",
        dest="frames_per_second",
        default=5,
        type=int,
        help="Number of frames to extract per second of video footage.",
        required=False,
    )
    options = parser.parse_args()
    return options.title, options.method, options.source_file, options.frames_per_second


@Halo(text="Extracting Images", spinner="dots")
def extract_frames(movie_input_path: str, fps: int) -> list:
    """
    Runs ffmpeg to decompose the video file into stills.
    :param movie_input_path:
    :param fps:
    :return:
    """
    if not os.path.isdir("images"):
        os.mkdir("images")
    command = ["ffmpeg", "-i", f"{movie_input_path}", "-vf", f"fps={fps}", "images/%05d.jpg"]

    _ = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    all_images = [str(element) for element in Path("images").iterdir()]
    all_images.sort(key=lambda x: int(x[7:-4]))
    return all_images


@Halo(text="Calculating Colors", spinner="dots")
def get_colors(images_list: list, method: str) -> list:
    """
    Docstring.
    :param images_list:
    :param method:
    :return:
    """
    bar_colors = []
    for filename in images_list:
        image = Image.open(filename).resize((25, 25))
        average_image_color = apply_method(method, image)
        bar_colors.append(average_image_color)
    return bar_colors


@Halo(text="Rendering Image", spinner="dots")
def create_image(all_bar_colors: list):
    """
    Docstring.
    :param all_bar_colors:
    :return:
    """
    bar_image = Image.new("RGB", (len(all_bar_colors), max([1, int(len(all_bar_colors) / 2.5)])))
    bar_full_data = [x for x in all_bar_colors] * bar_image.size[1]
    bar_image.putdata(bar_full_data)
    return bar_image


def main():
    """
    Docstring.
    :return: 
    """
    title, method, source_movie, frames_per_second = _parse_args()
    images = extract_frames(source_movie, frames_per_second)
    bar_colors = get_colors(images, method)
    bar_image = create_image(bar_colors)

    if not os.path.isdir("bars"):
        os.mkdir("bars")
    bar_image.save(f"bars/{title}_{method}.png")
    bar_image.show()


if __name__ == "__main__":
    main()
