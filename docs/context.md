# `context.py` Documentation

This module provides functionality for preparing context from relevant chunks of text. It is used to gather and format context information that will be used in the story generation process.

## Functions

### `prepare_context(embeddings_dict: Dict[str, Any], relevant_chunks: List[Tuple[str, int, float]]) -> str`

Prepares context from relevant chunks of text based on their similarity scores.

#### Parameters

- `embeddings_dict` (Dict[str, Any]): A dictionary where keys are file paths and values are dictionaries containing 'content' and 'chunk_embeddings' (and optionally 'chunk_content').
- `relevant_chunks` (List[Tuple[str, int, float]]): A list of tuples, each containing (file_path, chunk_index, similarity_score), as returned by semantic search.

#### Returns

- `str`: A string containing the formatted context.

#### Usage

```python
context = prepare_context(embeddings_dict, relevant_chunks)
```

#### Steps

1. **Initialize Context Parts**: Initializes an empty list to store parts of the context.
2. **Iterate Over Relevant Chunks**: Iterates over the relevant chunks to extract and format the context.
3. **Extract Content**: Extracts the content and chunks from the embeddings dictionary.
4. **Validate Chunk Index**: Validates the chunk index and extracts the corresponding chunk.
5. **Format Context**: Formats the context with source information and relevance score.
6. **Join Context Parts**: Joins the context parts into a single string.

#### Example

```python
from context import prepare_context

embeddings_dict = {
    "file1.txt": {
        "content": "This is the content of file1.",
        "chunk_embeddings": [
            "This is the first chunk.",
            "This is the second chunk."
        ]
    },
    "file2.txt": {
        "content": "This is the content of file2.",
        "chunk_embeddings": [
            "This is another chunk.",
            "This is yet another chunk."
        ]
    }
}

relevant_chunks = [
    ("file1.txt", 0, 0.95),
    ("file2.txt", 1, 0.90)
]

context = prepare_context(embeddings_dict, relevant_chunks)
print(context)
```

## Dependencies

- `logging`: For logging messages and errors.
- `typing`: For type hints.
- `pathlib`: For handling file paths.
- `text_processing`: For text processing utilities.

## Example Usage

To use the `prepare_context` function, simply import it and call it in your script:

```python
from context import prepare_context

embeddings_dict = {
    "file1.txt": {
        "content": "This is the content of file1.",
        "chunk_embeddings": [
            "This is the first chunk.",
            "This is the second chunk."
        ]
    },
    "file2.txt": {
        "content": "This is the content of file2.",
        "chunk_embeddings": [
            "This is another chunk.",
            "This is yet another chunk."
        ]
    }
}

relevant_chunks = [
    ("file1.txt", 0, 0.95),
    ("file2.txt", 1, 0.90)
]

context = prepare_context(embeddings_dict, relevant_chunks)
print(context)
```

This will prepare and print the context based on the relevant chunks provided.

## Error Handling

The function includes error handling to catch and log any exceptions that occur during the context preparation process. Errors are logged using the `logging` module.

## Conclusion

The `context.py` module provides a robust and efficient approach to preparing context from relevant chunks of text. By leveraging the embeddings dictionary and similarity scores, it ensures that the generated context is relevant and useful for the story generation process.
