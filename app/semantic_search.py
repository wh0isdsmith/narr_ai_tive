import logging
from typing import List, Tuple, Dict, Any
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai
from sentence_transformers import SentenceTransformer

# Set up a logger for this module.
logger = logging.getLogger('semantic_search')
logger.info("Semantic search module initialized")

# Initialize the sentence transformer model
model = SentenceTransformer('all-mpnet-base-v2')

def semantic_search(
    genai_model: genai.GenerativeModel,
    query: str,
    embeddings_dict: Dict[str, Any],
    top_n: int = 3
) -> List[Tuple[str, int, float]]:
    """Perform semantic search on embeddings.

    Args:
        model: The generative model to use for generating embeddings.
        query: The query string.
        embeddings_dict: A dictionary where keys are file paths and values are dictionaries containing 'content' and 'chunk_embeddings'.
        top_n: The number of most relevant chunks to return.

    Returns:
        A list of tuples, each containing (file_path, chunk_index, similarity_score).
    """
    logger.debug(f"Performing semantic search for query: '{query}'")

    try:
        # Generate query embedding using sentence transformers
        query_embedding = model.encode([query])[0]
    except Exception as e:
        logger.error(f"Error generating embedding for query '{query}': {e}")
        return []

    if query_embedding is None:
        logger.error("Could not generate embedding for query")
        return []

    similarities = []
    for file_path, data in embeddings_dict.items():
        # Always use chunk_embeddings
        for i, chunk_embedding in enumerate(data['chunk_embeddings']):
            similarity = cosine_similarity(
                [query_embedding], [chunk_embedding])[0][0]
            similarities.append((file_path, i, similarity))

    similarities.sort(key=lambda x: x[2], reverse=True)
    logger.info(f"Found {len(similarities)} similar chunks, returning top {top_n}")
    return similarities[:top_n]
