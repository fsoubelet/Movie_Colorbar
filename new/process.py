"""
Extract
-------

Module with high level functions to handle processing
a video into a colorbar, or all videos into a provided
folder into colorbars.
"""

from pathlib import Path

from new.constants import VALID_VIDEO_EXTENSIONS

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
