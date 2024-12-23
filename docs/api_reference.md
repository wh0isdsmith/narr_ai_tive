# API Reference

## Prerequisites

### Obtaining Google Gemini API Key

1. Visit the [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google Account
3. Click "Create API Key" if you don't have one
4. Copy your API key and store it securely

### Setting Up API Key

1. Create `secrets.yaml` in your project root:
```yaml
google_api_key: "your-api-key-here"
```

2. Add to environment variables (alternative):
```bash
export GOOGLE_API_KEY="your-api-key-here"
```

**Important**: Never commit your API key to version control!

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

### Example with API Key Setup

```python
from narr_ai_tive import StoryGenerator, load_config
import os

# Method 1: Using secrets.yaml (recommended)
config = load_config()

# Method 2: Using environment variable
os.environ['GOOGLE_API_KEY'] = 'your-api-key-here'

# Initialize generator
generator = StoryGenerator(config)

# Generate content
story = generator.generate_chapter(
    query="Ancient secrets revealed",
    style="mystery",
    character="Professor Blake"
)
```

## API Usage Limits

- Free tier: 60 requests per minute
- See [Google AI pricing](https://ai.google.dev/pricing) for current quotas
- Rate limiting is handled automatically by the library

## Error Handling

```python
from narr_ai_tive.exceptions import APIKeyError, RateLimitError

try:
    story = generator.generate_chapter(...)
except APIKeyError:
    print("Invalid or missing API key")
except RateLimitError:
    print("Rate limit exceeded, please wait")
```

Refer to the source code for more details on additional methods and parameters.
