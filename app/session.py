import logging
from typing import Dict, Any
from pathlib import Path
import json
from datetime import datetime

# Set up a logger for this module.
logger = logging.getLogger('session')
logger.info("Session module initialized")


def save_session(session_data: Dict[str, Any], filename: str = None):
    """Saves the current session data to a JSON file.

    Args:
        session_data: A dictionary containing the session data.
        filename: The name of the file to save the session to. If None, a timestamped filename is generated.
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"story_session_{timestamp}.json"

    filepath = Path(__file__).parent / filename
    try:
        with open(filepath, 'w') as f:
            json.dump(session_data, f, indent=4)
        logger.info(f"Session saved to {filename}")
    except Exception as e:
        logger.error(f"Error saving session to {filename}: {e}")


def load_session(filename: str) -> Dict[str, Any]:
    """Loads session data from a JSON file.

    Args:
        filename: The name of the file to load the session from.

    Returns:
        A dictionary containing the session data, or an empty dictionary if the file is not found or there is an error.
    """
    filepath = Path(__file__).parent / filename
    if not filepath.exists():
        logger.error(f"Session file not found: {filename}")
        return {}

    try:
        with open(filepath, 'r') as f:
            session_data = json.load(f)
        logger.info(f"Session loaded from {filename}")
        return session_data
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from session file '{
                     filename}': {e}")
        return {}
    except Exception as e:
        logger.error(f"Error loading session from {filename}: {e}")
        return {}
