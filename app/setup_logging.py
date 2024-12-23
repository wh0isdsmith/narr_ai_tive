import logging
from pathlib import Path

def setup_logging(log_level: str = "INFO", log_file: str = "app.log"):
    """Set up logging configuration."""
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_path, mode='a', encoding='utf-8')
        ]
    )
