"""
Running the tool from the commandline, if it is installed in your environment.
"""

import sys

from pathlib import Path

import click

from loguru import logger

from movie_colorbar.color_bar import METHOD_ACTION_MAP, process_dir, process_video


@click.command()
@click.option(
    "--inputfile",
    type=click.Path(exists=True, file_okay=True, resolve_path=True, path_type=Path),
    required=True,
    help="Location, relative or absolute, of the source video file to get the images from.",
)
@click.option(
    "--outputfile",
    type=click.Path(file_okay=True, resolve_path=True, path_type=Path),
    default=None,
    help="Path at which to write the output color bar image. Will default to a name constructed from the input file and chosen method.",
    show_default=True,
)
@click.option(
    "--method",
    type=click.Choice(METHOD_ACTION_MAP.keys()),
    default="rgbsquared",
    help="Method used to calculate the average color.",
    show_default=True,
)
@click.option(
    "--fps",
    type=int,
    default=10,
    help="Number of frames to extract per second of video footage.",
    show_default=True,
)
@click.option(
    "--log_level",
    type=click.Choice(["trace", "debug", "info", "warning", "error", "critical"]),
    default="info",
    show_default=True,
    help="Sets the logging level.",
)
def main(inputfile: Path, outputfile: Path, method: str, fps: int, log_level: str):
    """
    Turn a video into a colorbar.
    """
    set_logger_level(log_level)

    if outputfile is None:  # default if not provided
        logger.info("No output file name provided, constructing one from input file and method")
        outputfile = f"{inputfile.stem}_{method}.png"

    if method not in METHOD_ACTION_MAP.keys():
        logger.error(f"Invalid method given: {method} is not valid")
        raise click.Abort()

    if inputfile.is_file():
        process_video(
            title=outputfile,
            method=method,
            source_path=inputfile,
            frames_per_second=fps,
        )
    logger.success("All done!")


def set_logger_level(log_level: str = "info") -> None:
    """
    Sets the logger level to the one provided at the commandline.

    Default loguru handler will have DEBUG level and ID 0.
    We need to first remove this default handler and add ours with the wanted level.

    Args:
        log_level: string, the default logging level to print out.

    Returns:
        Nothing, acts in place.
    """
    logger.remove(0)
    logger.add(sys.stderr, level=log_level.upper())


if __name__ == "__main__":
    main()
