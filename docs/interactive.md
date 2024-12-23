# `interactive.py` Documentation

This module provides functionality for interactive story generation using a Text User Interface (TUI). It leverages the `rich` library for a visually appealing terminal interface and integrates with the story generation utilities provided in the `utils` module.

## Functions

### `interactive_loop(story_gen: StoryGenerator, plot_gen: PlotGenerator, embeddings_dict: dict, session_history: list, current_settings: dict)`

This function provides the main loop for interactive story generation. It allows the user to generate a plot outline, create chapters based on user queries or plot points, and refine the generated story iteratively.

#### Parameters

- `story_gen` (StoryGenerator): An instance of the `StoryGenerator` class.
- `plot_gen` (PlotGenerator): An instance of the `PlotGenerator` class.
- `embeddings_dict` (dict): A dictionary containing embeddings for semantic search.
- `session_history` (list): A list to store the history of the interactive session.
- `current_settings` (dict): A dictionary to store the current settings for story generation.

#### Usage

```python
interactive_loop(story_gen, plot_gen, embeddings_dict, session_history, current_settings)
```

#### Steps

1. **Generate Plot Outline**: Optionally generates a plot outline based on a user-provided prompt.
2. **Display World Details**: Displays the world details in a panel.
3. **Main Loop**: Enters the main loop for interactive story generation.
   - **User Query**: Prompts the user for a story query or command (e.g., 'exit', 'new chapter').
   - **Use Previous Settings**: Optionally uses previous settings or prompts the user for new settings.
   - **Generate Story**: Generates a story chapter based on the user query and settings.
   - **Refine Story**: Allows the user to refine the generated story iteratively.
   - **Save/Load/Export**: Provides options to save the session, load a session, or export the generated story.

#### Example

```python
from interactive import interactive_loop
from utils import StoryGenerator, load_config, load_api_key
from plot import PlotGenerator

config = load_config()
api_key = load_api_key(config)
story_gen = StoryGenerator(config)
plot_gen = PlotGenerator(story_gen.model)
embeddings_dict = {}  # Load your embeddings dictionary here
session_history = []
current_settings = {}

interactive_loop(story_gen, plot_gen, embeddings_dict, session_history, current_settings)
```

## Dependencies

- `logging`: For logging messages and errors.
- `json`: For handling JSON data.
- `pathlib`: For handling file paths.
- `rich.console.Console`: For creating a rich console interface.
- `rich.prompt.Prompt`: For prompting user inputs.
- `rich.panel.Panel`: For displaying panels in the console.
- `utils`: For utility functions such as `load_config`, `load_api_key`, and `StoryGenerator`.
- `plot`: For the `PlotGenerator` class.

## Example Usage

To use the `interactive_loop` function, simply import it and call it in your script:

```python
from interactive import interactive_loop
from utils import StoryGenerator, load_config, load_api_key
from plot import PlotGenerator

config = load_config()
api_key = load_api_key(config)
story_gen = StoryGenerator(config)
plot_gen = PlotGenerator(story_gen.model)
embeddings_dict = {}  # Load your embeddings dictionary here
session_history = []
current_settings = {}

interactive_loop(story_gen, plot_gen, embeddings_dict, session_history, current_settings)
```

This will launch the interactive TUI and guide you through the process of generating and refining a story.

## Configuration

The function relies on a configuration file (`config.yaml`) for various settings, including the default story style, temperature, max tokens, and more. Ensure that this file is properly set up before running the function.

## Error Handling

The function includes error handling to catch and display any exceptions that occur during the story generation process. Errors are logged using the `logging` module and displayed in the console using `rich`.

## Conclusion

The `interactive.py` module provides a user-friendly interface for interactive story generation. By leveraging the `rich` library, it offers a visually appealing and interactive experience. The function is highly configurable and integrates seamlessly with the story generation utilities provided in the `utils` module.
