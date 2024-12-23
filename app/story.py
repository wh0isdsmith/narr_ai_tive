import logging
from typing import List, Tuple, Dict, Any, Optional
from pathlib import Path

import google.generativeai as genai

# Import from within the app package
from .utils import load_config, StoryGenerator

# Get logger
logger = logging.getLogger('story')
logger.info("Story generator module initialized")
