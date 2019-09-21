"""
Color bar
---------

Created on 2019.08.28
:author: Felix Soubelet

A little script for fun that will make a video file into a color bar image. The colors are calculated from frames of
the video according the a specified method. Enjoy.
"""
import argparse
import subprocess
import shutil
from pathlib import Path
from halo import Halo
from PIL import Image
from generative_functions import (
    get_avg_rgb,
    get_avg_rgb_squared,
    get_avg_hsv,
    get_avg_hue,
    get_kmeans_color,
    get_most_common,
    get_avg_xyz,
    get_avg_lab,
    get_resized_color,
    get_quantized_color,
)


METHOD_ACTION_MAP: dict = {
    "rgb": get_avg_rgb,
    "hsv": get_avg_hsv,
    "hue": get_avg_hue,
    "kmeans": get_kmeans_color,
    "common": get_most_common,
    "xyz": get_avg_xyz,
    "lab": get_avg_lab,
    "rgbsquared": get_avg_rgb_squared,
    "resize": get_resized_color,
    "quantized": get_quantized_color,
}


def parse_arguments() -> tuple:
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
        help="String. Name that will be given to intermediate directory.",
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
        "--source-path",
        dest="source_path",
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
    return options.title, options.method, options.source_path, options.frames_per_second


@Halo(text="Extracting Images.", spinner="dots")
def extract_frames(movie_input_path: str, fps: int) -> list:
    """
    Runs ffmpeg to decompose the video file into stills.
    :param movie_input_path: Absolute path to the video file.
    :param fps: Number of frames to extract per second.
    :return: list of absolute paths to all frames extracted (and stored in an intermediate folder).
    """
    if not Path("images").is_dir():
        Path("images").mkdir()
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
        average_image_color = METHOD_ACTION_MAP[method](image)
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


def process_video(title: str, method: str, source_path: str, frames_per_second: int = 10) -> None:
    """
    Will populate a folder named `images` with every extracted image from the provided video, and create the color
    bar from those images. Deletes said folder afterwards.
    :param title: name to give the intermediate directory.
    :param method: method to use to get the colors.
    :param source_path: absolute path to the video file.
    :param frames_per_second: number of frames to extract per second of video. You'll want to lower this parameter
    on longer videos.
    :return: nothing.
    """
    images = extract_frames(source_path, frames_per_second)
    bar_colors = get_colors(images, method)
    bar_image = create_image(bar_colors)

    if not Path("bars").is_dir():
        Path("bars").mkdir()
    if not Path(f"bars/{title}").is_dir():
        Path(f"bars/{title}").mkdir()
    bar_image.save(f"bars/{title}/{source_path.split('/')[-1].split('.')[0]}_{method}.png")
    shutil.rmtree("images")


def process_dir(title: str, method: str, source_path: str, frames_per_second: int = 10) -> None:
    """
    Will process every video into the directory.
    :param title: name to give the intermediate directory.
    :param method: method to use to get the colors.
    :param source_path: absolute path to the video file.
    :param frames_per_second: number of frames to extract per second of video. You'll want to lower this parameter
    on longer videos.
    :return: nothing.
    """
    directory = Path(source_path)
    for video_path in sorted(directory.iterdir()):
        process_video(title=title, method=method, source_path=str(video_path), frames_per_second=frames_per_second)


def main() -> None:
    """
    Run the entire process.
    Takes arguments from the commandline, namely a `title` to give to the finished product, a `method` to apply,
    the `filepath` to source video and the number of `frames_per_second` to exctract from said video.
    It will populate (and create if needed) a folder named `images` with every extracted image, and leave that up
    after completing the process. It's yours to clean.
    :return: nothing.
    """
    title, method, source_path, frames_per_second = parse_arguments()
    if Path(source_path).is_file():
        process_video(title=title, method=method, source_path=source_path, frames_per_second=frames_per_second)
    elif Path(source_path).is_dir():
        process_dir(title=title, method=method, source_path=source_path, frames_per_second=frames_per_second)


if __name__ == "__main__":
    main()
