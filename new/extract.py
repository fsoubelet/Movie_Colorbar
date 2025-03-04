"""
Extract
-------

Module with functions to handle splitting
a video into many images.
"""

import subprocess

from pathlib import Path

from loguru import logger

# ----- Video Extraction ----- #


def extract_frames_from_video(
    video: Path, output_dir: Path, fps: int, file_format: str = "png"
) -> list[Path]:
    """
    Runs ffmpeg to decompose the video into still frames.
    The frames are extracted in the provided `output_dir`.

    Parameters
    ----------
    video : pathlib.Path
        Path to the video file.
    output_dir : pathlib.Path
        Directory where the extracted frames will be saved.
    fps : int
        Number of frames to extract per second of video.
    output_format : str, optional
        Image format for extracted frames (default is 'png').

    Returns
    -------
    list[Path]
        List of paths to the extracted frames.

    Raises
    ------
    FileNotFoundError
        If the video file does not exist.
    ValueError
        If fps is not a positive integer.
    RuntimeError
        If ffmpeg fails to extract frames.
    """
    # Check the video exists and fps is valid
    if not video.exists() and video.is_file():
        raise FileNotFoundError(f"The video file {video} does not exist.")
    if fps <= 0:
        raise ValueError("FPS must be a positive integer.")

    logger.debug("Extracting frames from video")
    output_dir.mkdir(exist_ok=True)

    # Define the output file pattern and ffmpeg command
    pattern = output_dir / f"%05d.{file_format}"
    command = ["ffmpeg", "-i", str(video), "-vf", f"fps={fps}", str(pattern)]

    logger.debug(f"Running ffmpeg with command: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)

    # Check for ffmpeg errors
    if result.returncode != 0:
        logger.error(f"ffmpeg failed: {result.stderr}")
        raise RuntimeError(f"Failed to extract frames: {result.stderr}")

    # Gather the extracted frames (frame number from filename)
    logger.debug("Gathering extracted frames")
    images = sorted(output_dir.iterdir(), key=lambda x: int(x.stem))

    logger.debug(f"Successfully extracted {len(images)} images from {video.name}")
    return images
