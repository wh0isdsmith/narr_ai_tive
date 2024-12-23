import json
import logging
from typing import Any, Dict
from pathlib import Path

from .path_utils import resolve_data_path

# Set up a logger for this module.
logger = logging.getLogger('world')
logger.info("World module initialized")


def load_world_details(world_details_path: str) -> Dict[str, Any]:
    """Loads world details from a JSON file.

    Args:
        world_details_path: The path to the JSON file containing the world details.

    Returns:
        A dictionary containing the world details.

    Raises:
        FileNotFoundError: If the world details file is not found.
        json.JSONDecodeError: If there is an error decoding the JSON file.
    """
    logger.debug(f"Loading world details from {world_details_path}")

    filepath = resolve_data_path(world_details_path)
    if not filepath.exists():
        logger.error(f"World details file not found: {filepath}")
        raise FileNotFoundError(f"World details file not found: {filepath}")

    try:
        with open(filepath, 'r') as f:
            world_details = json.load(f)
        logger.info(f"World details successfully loaded from {filepath}")
        return world_details
    except json.JSONDecodeError as e:
        logger.error(
            f"Error decoding JSON from world details file '{filepath}': {e}"
        )
        raise
