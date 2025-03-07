"""
Running from the command line.
"""

import sys

from pathlib import Path

from loguru import logger
from typer import Argument, Exit, Option, Typer

from movie_colorbar.constants import LogLevels, Methods
from movie_colorbar.process import process_directory, process_video

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
    cleanup: bool = Option(
        default=True,
        show_choices=True,
        help="Whether to remove the extracted frames after processing.",
    ),
    log_level: LogLevels = Option(
        default=LogLevels.info,
        show_choices=True,
        help="The base console logging level.",
    ),
) -> None:
    """Command line tool to create colorbars from videos.

    From the input video individual frames are extracted with ffmpeg
    and written to disk in a directory placed next to the final output
    and named after the video. Each frame is reduced to a single color
    according to the chosen method. Finally a colorbar is created from
    these determined colors, and written to disk as an image file at
    the provided output location. By default the extracted frames are
    removed after processing, but they can be kept if desired (see the
    'cleanup' option).

    Should the input be a directory, then every video file contained
    within will be processed, provided it is supported by ffmpeg. In
    this case the output should also be a directory, in which one
    colorbar will be created for each video file.
    """
    set_logger_level(log_level)

    # Handle a single file provided as input
    if input.is_file():
        # Make sure the output is a file as well
        if output.exists() and not output.is_file():
            logger.error("The output path should match the type of the input path")
            raise Exit(code=1)
        # Process the video (skipped if unsupported format)
        process_video(video=input, method=method, fps=fps, outputpath=output, cleanup=cleanup)

    # Handle a directory provided as input
    elif input.is_dir():
        # Make sure the output is a directory as well
        if output.exists() and not output.is_dir():
            logger.error("The output path should match the type of the input path")
            raise Exit(code=1)
        # Process all videos in the directory
        process_directory(
            directory=input, method=method, fps=fps, outputdir=output, cleanup=cleanup
        )

    logger.success("All done!")


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
