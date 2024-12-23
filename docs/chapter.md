# `chapter.py` Documentation

This module provides functionality for generating a single chapter of a story using a Text User Interface (TUI). It leverages the `rich` library for a visually appealing terminal interface and integrates with the story generation utilities provided in the `utils` module.

## Functions

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
from chapter import generate_chapter_tui

generate_chapter_tui()
```

## Dependencies

- `logging`: For logging messages and errors.
- `typing`: For type hints.
- `pathlib`: For handling file paths.
- `rich.console.Console`: For creating a rich console interface.
- `rich.prompt.Prompt`: For prompting user inputs.
- `rich.prompt.Confirm`: For confirming user inputs.
- `rich.table.Table`: For displaying tables in the console.
- `rich.progress.track`: For tracking progress.
- `rich.panel.Panel`: For displaying panels in the console.
- `rich.live.Live`: For live updates in the console.
- `utils`: For utility functions such as `generate_story`, `load_config`, and `load_api_key`.

## Example Usage

To use the `generate_chapter_tui` function, simply import it and call it in your script:

```python
from chapter import generate_chapter_tui

generate_chapter_tui()
```

This will launch the TUI and guide you through the process of generating a single chapter of a story.

## Configuration

The function relies on a configuration file (`config.yaml`) for various settings, including the default story style, temperature, max tokens, and more. Ensure that this file is properly set up before running the function.

## Error Handling

The function includes error handling to catch and display any exceptions that occur during the story generation process. Errors are logged using the `logging` module and displayed in the console using `rich`.

## Conclusion

The `chapter.py` module provides a user-friendly interface for generating a single chapter of a story. By leveraging the `rich` library, it offers a visually appealing and interactive experience. The function is highly configurable and integrates seamlessly with the story generation utilities provided in the `utils` module.
