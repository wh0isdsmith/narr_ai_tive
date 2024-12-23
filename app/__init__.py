import logging
import sys
from rich.logging import RichHandler


def setup_logging(log_level: str = "INFO"):
    """Configures the logging module."""
    logging.basicConfig(
        level=log_level,
        format="%(name)s - %(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(
            rich_tracebacks=True,
            tracebacks_show_locals=True,
            show_time=True,
            show_level=True,
            show_path=True
        )]
    )
    logger = logging.getLogger()
    logger.info("Logging initialized")
