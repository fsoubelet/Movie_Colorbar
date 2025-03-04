"""
Running from the command line.
"""

import sys

from pathlib import Path

from loguru import logger
from typer import Argument, Exit, Option, Typer

from new.constants import LogLevels, Methods
from new.process import process_directory, process_video

app = Typer(no_args_is_help=True)


@app.command()
def main(
    input: Path = Argument(
        file_okay=True,
        dir_okay=True,
        exists=True,
        resolve_path=True,
        show_default=False,  # required anyway
        help="Path to the input video file or directory.",
    ),
    output: Path = Argument(
        file_okay=True,
        dir_okay=True,
        exists=False,
        resolve_path=True,
        show_default=False,  # required anyway
        help="Path to the output colorbar image or directory.",
    ),
    method: Methods = Option(
        default=Methods.rgb,
        show_choices=True,
        help="Method used to calculate the color for each frame.",
    ),
    fps: int = Option(
        default=10,
        min=0,
        help="Number of frames to extract per second of video footage.",
    ),
    # cleanup option
    log_level: LogLevels = Option(
        default=LogLevels.info,
        show_choices=True,
        help="The base console logging level.",
    ),
) -> None:
    """Command line tool to create colorbars from videos.

    TODO: info and methodology
    """
    set_logger_level(log_level)


# ----- Logger helper ----- #


def set_logger_level(log_level: str = LogLevels.info) -> None:
    """
    Sets the base logger level to the one provided.

    Default loguru handler will have DEBUG level and ID 0.
    We need to first remove this default handler and add ours
    with the wanted level.

    Parameters
    ----------
    log_level : str
        The base console logging level.
    """
    logger.remove(0)
    logger.add(sys.stderr, level=log_level.upper())


# ----- Entrypoint ----- #

if __name__ == "__main__":
    app()
