import json
import logging
from typing import Any, Dict
from pathlib import Path

from .path_utils import resolve_data_path

# Set up a logger for this module.
logger = logging.getLogger('character')
logger.info("Character module initialized")


def load_character_profiles(character_profiles_path: str) -> Dict[str, Any]:
    """Loads character profiles from a JSON file.

    Args:
        character_profiles_path: The path to the JSON file containing the character profiles.

    Returns:
        A dictionary containing the character profiles.

    Raises:
        FileNotFoundError: If the character profiles file is not found.
        json.JSONDecodeError: If there is an error decoding the JSON file.
    """
    logger.debug(f"Loading character profiles from {character_profiles_path}")

    filepath = resolve_data_path(character_profiles_path)
    if not filepath.exists():
        logger.error(f"Character profiles file not found: {filepath}")
        raise FileNotFoundError(
            f"Character profiles file not found: {filepath}")

    try:
        with open(filepath, 'r') as f:
            profiles = json.load(f)
        logger.info(f"Character profiles successfully loaded from {filepath}")
        return profiles
    except json.JSONDecodeError as e:
        logger.error(
            f"Error decoding JSON from character profiles file '{
                filepath}': {e}"
        )
        raise
