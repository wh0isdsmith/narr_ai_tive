# `semantic_search.py` Documentation

This module provides functionality for performing semantic search on text embeddings. It leverages the `sentence-transformers` library to generate embeddings and the `scikit-learn` library to compute cosine similarity.

## Functions

### `semantic_search(genai_model: genai.GenerativeModel, query: str, embeddings_dict: Dict[str, Any], top_n: int = 3) -> List[Tuple[str, int, float]]`

This function performs semantic search on embeddings to find the most relevant chunks of text based on a query.

#### Parameters

- `genai_model` (genai.GenerativeModel): The generative model to use for generating embeddings.
- `query` (str): The query string.
- `embeddings_dict` (Dict[str, Any]): A dictionary where keys are file paths and values are dictionaries containing 'content' and 'chunk_embeddings'.
- `top_n` (int, optional): The number of most relevant chunks to return. Default is 3.

#### Returns

- `List[Tuple[str, int, float]]`: A list of tuples, each containing (file_path, chunk_index, similarity_score).

#### Usage

```python
results = semantic_search(
    genai_model=model,
    query="A dark forest at midnight",
    embeddings_dict=embeddings_dict,
    top_n=3
)
```

#### Steps

1. **Generate Query Embedding**: Generates an embedding for the query using the `sentence-transformers` model.
2. **Compute Similarities**: Computes cosine similarity between the query embedding and each chunk embedding in the `embeddings_dict`.
3. **Sort and Return**: Sorts the chunks by similarity score in descending order and returns the top `top_n` results.

#### Example

```python
from semantic_search import semantic_search
from sentence_transformers import SentenceTransformer

# Initialize the sentence transformer model
model = SentenceTransformer('all-mpnet-base-v2')

# Example embeddings dictionary
embeddings_dict = {
    "file1.txt": {
        "content": "This is the content of file1.",
        "chunk_embeddings": [
            model.encode("This is the first chunk."),
            model.encode("This is the second chunk.")
        ]
    },
    "file2.txt": {
        "content": "This is the content of file2.",
        "chunk_embeddings": [
            model.encode("This is another chunk."),
            model.encode("This is yet another chunk.")
        ]
    }
}

# Perform semantic search
results = semantic_search(
    genai_model=model,
    query="A dark forest at midnight",
    embeddings_dict=embeddings_dict,
    top_n=3
)

# Print results
for file_path, chunk_index, similarity_score in results:
    print(f"File: {file_path}, Chunk: {chunk_index}, Similarity: {similarity_score:.4f}")
```

## Dependencies

- `logging`: For logging messages and errors.
- `typing`: For type hints.
- `numpy`: For numerical operations.
- `scikit-learn`: For computing cosine similarity.
- `google.generativeai`: For the generative model.
- `sentence-transformers`: For generating text embeddings.

## Example Usage

To use the `semantic_search` function, simply import it and call it in your script:

```python
from semantic_search import semantic_search
from sentence_transformers import SentenceTransformer

# Initialize the sentence transformer model
model = SentenceTransformer('all-mpnet-base-v2')

# Example embeddings dictionary
embeddings_dict = {
    "file1.txt": {
        "content": "This is the content of file1.",
        "chunk_embeddings": [
            model.encode("This is the first chunk."),
            model.encode("This is the second chunk.")
        ]
    },
    "file2.txt": {
        "content": "This is the content of file2.",
        "chunk_embeddings": [
            model.encode("This is another chunk."),
            model.encode("This is yet another chunk.")
        ]
    }
}

# Perform semantic search
results = semantic_search(
    genai_model=model,
    query="A dark forest at midnight",
    embeddings_dict=embeddings_dict,
    top_n=3
)

# Print results
for file_path, chunk_index, similarity_score in results:
    print(f"File: {file_path}, Chunk: {chunk_index}, Similarity: {similarity_score:.4f}")
```

This will perform a semantic search on the provided embeddings and return the most relevant chunks based on the query.

## Error Handling

The function includes error handling to catch and log any exceptions that occur during the semantic search process. Errors are logged using the `logging` module.

## Conclusion

The `semantic_search.py` module provides a robust and efficient approach to performing semantic search on text embeddings. By leveraging the `sentence-transformers` library and `scikit-learn`, it ensures accurate and relevant results for a given query.
