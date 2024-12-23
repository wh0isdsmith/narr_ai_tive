# `tui.py` Documentation

This module provides the main Text User Interface (TUI) for the Narr_ai_tive application. It leverages the `rich` library to create a visually appealing and interactive terminal interface for story generation.

## Functions

### `main_menu()`

This function displays the main menu of the TUI and handles user input to navigate through different options.

#### Usage

```python
main_menu()
```

#### Steps

1. **Display Menu**: Displays the main menu with options for generating a chapter, interactive mode, and exiting the application.
2. **Handle User Input**: Prompts the user to select an option and calls the corresponding function based on the selection.
3. **Generate Chapter**: Calls the `generate_chapter_tui` function to generate a single chapter.
4. **Interactive Mode**: Calls the `interactive_loop` function to enter the interactive story generation mode.
5. **Exit**: Exits the application.

#### Example

```python
from tui import main_menu

main_menu()
```

### `generate_chapter_tui()`

This function provides a TUI for generating a single chapter of a story. It prompts the user for various inputs, including the story query, style, character, situation, and output file. It also offers advanced configuration options for more control over the generation process.

#### Usage

```python
generate_chapter_tui()
```

#### Steps

1. **Clear Console**: Clears the console for a fresh start.
2. **Print Panel**: Displays a panel with the title "Generate a Single Chapter".
3. **Load Configuration**: Loads the configuration settings from `config.yaml`.
4. **Load API Key**: Loads the API key from the configuration or secrets file.
5. **Prompt for Inputs**: Prompts the user for the story query, style, character, situation, and output file.
6. **Advanced Options**: Optionally prompts the user for advanced configuration settings, including the number of relevant chunks (`top_n`), temperature, max tokens, max iterations, min quality score, and whether to force regeneration.
7. **Set Log Level**: Sets the log level for the story generation process.
8. **Live Progress**: Uses `rich.live.Live` to display a live progress bar during the story generation process.
9. **Generate Story**: Calls the `generate_story` function with the provided inputs and configuration settings.
10. **Print Completion Panel**: Displays a panel indicating the completion of the story generation and the location of the output file.
11. **Error Handling**: Catches and prints any exceptions that occur during the story generation process.

#### Example

```python
from tui import generate_chapter_tui

generate_chapter_tui()
```

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
from tui import interactive_loop
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

To use the `main_menu` function, simply import it and call it in your script:

```python
from tui import main_menu

main_menu()
```

This will launch the main menu of the TUI and guide you through the process of generating and refining a story.

## Configuration

The functions rely on a configuration file (`config.yaml`) for various settings, including the default story style, temperature, max tokens, and more. Ensure that this file is properly set up before running the functions.

## Error Handling

The functions include error handling to catch and display any exceptions that occur during the story generation process. Errors are logged using the `logging` module and displayed in the console using `rich`.

## Conclusion

The `tui.py` module provides a user-friendly interface for interactive story generation. By leveraging the `rich` library, it offers a visually appealing and interactive experience. The functions are highly configurable and integrate seamlessly with the story generation utilities provided in the `utils` module.
