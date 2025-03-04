"""
Constants
---------

Module with constants used in the project.
"""

from enum import Enum

# ----- Methods ----- #


class Methods(str, Enum):
    common: str = "common"
    hsv: str = "hsv"
    hue: str = "hue"
    kmeans: str = "kmeans"
    lab: str = "lab"
    quantized: str = "quantized"
    resize: str = "resize"
    rgb: str = "rgb"
    rgb_squared: str = "rgbsquared"
    xyz: str = "xyz"


# ----- Extensions ----- #

VALID_VIDEO_EXTENSIONS: tuple[str, ...] = (
    ".webm",
    ".mkv",
    ".flv",
    ".vob",
    ".ogg",
    ".ogv",
    ".drc",
    ".gif",
    ".gifv",
    ".mng",
    ".avi",
    ".mov",
    ".qt",
    ".wmv",
    ".yuv",
    ".rm",
    ".rmvb",
    ".asf",
    ".amv",
    ".mp4",
    ".m4p",
    ".m4v",
    ".mpg",
    ".mp2",
    ".mpv",
    ".m4v",
    ".flv",
)


# ----- Logging ----- #


class LogLevels(str, Enum):
    trace: str = "trace"
    debug: str = "debug"
    info: str = "info"
    warning: str = "warning"
    error: str = "error"
    critical: str = "critical"
