from pathlib import Path

def resolve_data_path(path: str) -> Path:
    """Resolve the data path."""
    return Path(path).resolve()
