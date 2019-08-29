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
    gen_most_common,
    gen_avg_xyz,
    gen_avg_lab,
    gen_resized_color,
    gen_quantized_color,
)


def apply_method(method: str, source_image: Image):
    """
    Intermediate function to apply the right method to an image, based on the method name given at the commandline.
    :param method: The method to apply to the image.
    :param source_image: Pillow.Image instance.
    :return: the result of said method applied to the image, as programmed in generative_functions.py
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
        return gen_most_common(source_image)
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
    :return: variables for each argument.
    """
    parser = argparse.ArgumentParser(description="Getting your average colorbar.")
    parser.add_argument(
        "-t",
        "--title",
        dest="title",
        default="output",
        type=str,
        help="String. Filename for output file.",
        required=True,
    )
    parser.add_argument(
        "-m",
        "--method",
        dest="method",
        default="rgbsquared",
        type=str,
        help="""String. Method to use to calculate the average color. Options are:
        rgb, hsv, hue, kmeans, common, lab, xyz, rgbsquared, resize, and quantized.""",
        required=True,
    )
    parser.add_argument(
        "-s",
        "--source-file",
        dest="source_file",
        default=".",
        type=str,
        help="String. Path to source video file to get the images from.",
        required=True,
    )
    parser.add_argument(
        "-fps",
        "--frames-per-second",
        dest="frames_per_second",
        default=5,
        type=int,
        help="Integer. Number of frames to extract per second of video footage.",
        required=False,
    )
    options = parser.parse_args()
    return options.title, options.method, options.source_file, options.frames_per_second


@Halo(text="Extracting Images.", spinner="dots")
def extract_frames(movie_input_path: str, fps: int) -> list:
    """
    Runs ffmpeg to decompose the video file into stills.
    :param movie_input_path: Absolute path to the video file.
    :param fps: Number of frames to extract per second.
    :return: list of absolute paths to all frames extracted (and stored in an intermediate folder).
    """
    if not os.path.isdir("images"):
        os.mkdir("images")
    command = ["ffmpeg", "-i", f"{movie_input_path}", "-vf", f"fps={fps}", "images/%05d.jpg"]

    _ = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    all_images = [str(element) for element in Path("images").iterdir()]
    all_images.sort(key=lambda x: int(x[7:-4]))
    return all_images


@Halo(text="Calculating Colors.", spinner="dots")
def get_colors(images_list: list, method: str) -> list:
    """
    Getting average color of each image through to the provided method.
    :param images_list: List of absolute paths to all frames to process.
    :param method: method to apply to each image to get its average color.
    :return: list of computed average color for all images, one per image.
    """
    bar_colors = []
    for filename in images_list:
        image = Image.open(filename).resize((25, 25))
        average_image_color = apply_method(method, image)
        bar_colors.append(average_image_color)
    return bar_colors


@Halo(text="Rendering Image.", spinner="dots")
def create_image(all_bar_colors: list) -> Image:
    """
    Create the colorbar from the computed average colors.
    :param all_bar_colors: list of computed average color for all images, one per image.
    :return: a Pillow.Image instance, with the colors implemented as a colorbar.
    """
    bar_image = Image.new("RGB", (len(all_bar_colors), max([1, int(len(all_bar_colors) / 2.5)])))
    bar_full_data = [x for x in all_bar_colors] * bar_image.size[1]
    bar_image.putdata(bar_full_data)
    return bar_image


def main() -> None:
    """
    Run the entire process.
    :return: nothing.
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
