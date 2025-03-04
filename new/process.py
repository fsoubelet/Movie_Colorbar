"""
Extract
-------

Module with high level functions to handle processing
a video into a colorbar, or all videos into a provided
folder into colorbars.
"""

from pathlib import Path
from shutil import rmtree

from loguru import logger
from PIL import Image

from new.bar import create_colorbar_from_images
from new.constants import VALID_VIDEO_EXTENSIONS
from new.extract import extract_frames_from_video

# ----- Video Processing ----- #


def process_video(
    video: Path, method: str, fps: int, outputpath: Path, cleanup: bool = True
) -> None:
    """
    Handles the creation of a colorbar from a video, with the
    given method. Will extract frames from the video via ffmpeg,
    compute colors from the frames, make a colorbar image and
    save it to disk.

    Note
    ----
    The extracted frames are saved in a temporary directory
    named `images_{video.stem}`, placed in the same directory
    as the output colorbar image.

    Parameters
    ----------
    video : pathlib.Path
        Path to the video file.
    method : str
        Method to use to compute the colors from
        extracted images.
    fps : int
        Number of frames to extract per second of video.
    outputpath : pathlib.Path
        Path where to save the colorbar image.
    cleanup : bool, optional
        Flag to remove the extracted frames directory
        after creating the colorbar (default `True`).
    """
    if not _is_handled_video(video):
        logger.warning(f"File '{video.name}' is not a supported format, skipping")
        return

    logger.info(f"Creating colorbar from '{video.name}'")
    images_dir = outputpath.parent / f"images_{video.stem}"
    images: list[Path] = extract_frames_from_video(video, images_dir, fps)

    colorbar: Image = create_colorbar_from_images(images, method)
    colorbar.save(outputpath)
    logger.success(f"Saved created colorbar at '{outputpath.absolute()}'")

    if cleanup is True:
        logger.info(f"Cleaning up: removing temporary '{images_dir.name}' directory")
        rmtree(images_dir)


# ----- Helpers ----- #


def _is_handled_video(video: Path) -> bool:
    """
    Check that the file extension is a handled video format.

    Parameters
    ----------
    video : pathlib.Path
        Path to the video file.

    Returns
    -------
    bool
        True if the video is a valid format, False otherwise.
    """
    return video.suffix.lower() in VALID_VIDEO_EXTENSIONS
