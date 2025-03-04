"""
Running from the command line.
"""

import sys

from pathlib import Path

import typer

from loguru import logger

from new.process import process_directory, process_video

app = typer.Typer()


# ----- Logger helper ----- #


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
