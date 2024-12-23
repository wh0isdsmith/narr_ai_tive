# API Reference

## StoryGenerator Class

### Methods

#### `generate_chapter(query: str, style: str, character: str) -> str`

Generates a chapter based on the given query, style, and character.

- **Parameters:**
  - `query` (str): The initial prompt or query for the story.
  - `style` (str): The storytelling style (e.g., "mystery", "sci-fi").
  - `character` (str): The main character's name.

- **Returns:**
  - `str`: The generated chapter.

### Example

```python
from narr_ai_tive import StoryGenerator, load_config

# Initialize generator
config = load_config()
generator = StoryGenerator(config)

# Generate content
story = generator.generate_chapter(
    query="Ancient secrets revealed",
    style="mystery",
    character="Professor Blake"
)
print(story)
```

Refer to the source code for more details on additional methods and parameters.
