import logging
from typing import List, Tuple, Dict, Any
from pathlib import Path

from .text_processing import chunk_text

# Set up a logger for this module.
logger = logging.getLogger('context')
logger.info("Context module initialized")


def prepare_context(embeddings_dict: Dict[str, Any], relevant_chunks: List[Tuple[str, int, float]]) -> str:
    """Prepare context from relevant chunks.

    Args:
        embeddings_dict: A dictionary where keys are file paths and values are dictionaries containing 'content' and 'chunk_embeddings' (and optionally 'chunk_content').
        relevant_chunks: A list of tuples, each containing (file_path, chunk_index, similarity_score), as returned by semantic_search.

    Returns:
        A string containing the formatted context.
    """
    CONTEXT_CHUNK_FALLBACK_SIZE = 5000  # Define constant here
    logger.debug("Preparing context from relevant chunks")
    context_parts = []

    for file_path, chunk_idx, similarity in relevant_chunks:
        data = embeddings_dict[file_path]
        content = data['content']
        chunks = data.get('chunk_content', chunk_text(content))

        if chunk_idx is not None and chunk_idx < len(chunks):
            context_chunk = chunks[chunk_idx]
            source = f"{Path(file_path).name} (chunk {chunk_idx + 1})"
        else:
            logger.warning(f"Invalid chunk index {chunk_idx} for {
                           file_path}")
            context_chunk = content[:CONTEXT_CHUNK_FALLBACK_SIZE]
            source = Path(file_path).name

        context_parts.append(f"Source: {source}\nRelevance: {
                             similarity:.2f}\n\n{context_chunk}\n")

    logger.info(f"Prepared context with {len(context_parts)} parts")
    return "\n---\n".join(context_parts)
