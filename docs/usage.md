# Usage Guide

## Interactive TUI

To start the interactive terminal user interface:

```bash
python -m app.main
```

## CLI Generation

### Generate a single chapter

```bash
narr_ai_tive generate --query "A mystical journey begins" --style "epic fantasy"
```

### Generate with character focus

```bash
narr_ai_tive generate --input story.txt --character "Elena" --situation "dark forest"
```

## Python API

### Example Usage

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

Refer to the API reference for more details on available methods and parameters.
