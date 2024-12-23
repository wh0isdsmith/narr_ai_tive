# Embeddings Setup Guide

## Prerequisites

Before using Narr_ai_tive, you need to have document embeddings prepared in an `embeddings.json` file. This file contains vector representations of your documents that enable semantic search and context-aware story generation.

## Embeddings File Structure

The `embeddings.json` file should be placed in the `data/` directory and follow this structure:

```json
{
  "documents": [
    {
      "id": "doc1",
      "text": "Original document text",
      "embedding": [0.1, 0.2, ...],  // 1536-dimensional vector
      "metadata": {
        "title": "Document Title",
        "type": "character_profile",
        "tags": ["fantasy", "character"]
      }
    }
  ]
}
```

## Generating Embeddings

1. **Prepare Your Documents**
   - Gather all documents you want to use for story generation
   - Supported formats: `.txt`, `.md`, `.pdf`, `.docx`

2. **Install Required Tools**
   ```bash
   pip install sentence-transformers
   ```

3. **Generate Embeddings**
   ```python
   from sentence_transformers import SentenceTransformer
   import json

   # Initialize the model
   model = SentenceTransformer('all-MiniLM-L6-v2')

   # Generate embeddings
   documents = [
       {"text": "your document text", "title": "Doc Title"}
       # Add more documents...
   ]

   for doc in documents:
       embedding = model.encode(doc["text"])
       doc["embedding"] = embedding.tolist()

   # Save to JSON
   with open('data/embeddings.json', 'w') as f:
       json.dump({"documents": documents}, f)
   ```

## Best Practices

- Keep document chunks between 100-1000 words for optimal performance
- Include relevant metadata for better context handling
- Update embeddings when documents change
- Use consistent document formatting

## Validation

You can validate your embeddings file using our utility:

```bash
narr_ai_tive validate-embeddings data/embeddings.json
```

## Common Issues

1. **Missing Embeddings**
   - Error: `FileNotFoundError: embeddings.json not found`
   - Solution: Ensure the file exists in the `data/` directory

2. **Invalid Format**
   - Error: `InvalidEmbeddingsFormat: Invalid embeddings structure`
   - Solution: Verify JSON structure matches the required format

3. **Incorrect Dimensions**
   - Error: `EmbeddingDimensionError: Expected 1536 dimensions`
   - Solution: Use compatible embedding model (we recommend all-MiniLM-L6-v2)

## Support

For more help with embeddings:
- Check our [FAQ](docs/faq.md)
- Join our [Discord community](#)
- File an issue on GitHub

---

**Note**: The quality of your story generation heavily depends on the quality and relevance of your document embeddings. Take time to prepare them properly.
