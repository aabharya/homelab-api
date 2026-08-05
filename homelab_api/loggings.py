import logging

from rich.console import Console
from rich.logging import RichHandler

console = Console()


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    handler = RichHandler(
        console=console,
        rich_tracebacks=True,
        markup=True,
        show_path=False,
        show_time=True,
        show_level=True,
    )

    handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(handler)

    return logger
