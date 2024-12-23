import logging
from typing import List

# Set up a logger for this module.
logger = logging.getLogger('text_processing')
logger.info("Text processing module initialized")


def chunk_text(text: str, chunk_size: int = 5000, overlap: int = 200) -> List[str]:
    """Splits text into overlapping chunks.

    Args:
        text: The text to be chunked.
        chunk_size: The desired size of each chunk (in characters).
        overlap: The number of overlapping characters between consecutive chunks.

    Returns:
        A list of text chunks.
    """
    logger.debug(f"Chunking text into chunks of size {
                 chunk_size} with overlap {overlap}")
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    logger.info(f"Text chunked into {len(chunks)} chunks")
    return chunks
