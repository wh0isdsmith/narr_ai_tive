# Navigating Narr_ai_tive

This guide provides detailed instructions on how to navigate the Narr_ai_tive application after running it. The application offers a Text User Interface (TUI) for interactive story generation, as well as command-line and Python API options.

## Running the Application

To start the application, run the following command:

```bash
python -m app.main
```

This will launch the main menu of the TUI.

## Main Menu

Upon launching the application, you will be presented with the main menu. The main menu offers several options:

1. **Generate a Single Chapter**
2. **Interactive Mode**
3. **Exit**

### 1. Generate a Single Chapter

Select this option to generate a single chapter of a story. You will be prompted for various inputs, including the story query, style, character, situation, and output file. You can also configure advanced options such as the number of relevant chunks, temperature, max tokens, max iterations, min quality score, and whether to force regeneration.

#### Steps

1. **Enter Story Query**: Provide a query or prompt for the story.
   - Example: "A knight embarks on a quest to find a lost artifact."
2. **Enter Story Style**: Specify the style of the story (e.g., "dark fantasy").
   - Example: "Epic fantasy"
3. **Enter Focus Character**: Optionally, specify the main character of the story.
   - Example: "Sir Roland"
4. **Enter Story Situation**: Optionally, provide the situation or setting of the story.
   - Example: "A dark forest at midnight"
5. **Enter Output File**: Optionally, specify the output file for the generated story.
   - Example: "output/story_chapter.txt"
6. **Configure Advanced Options**: Optionally, configure advanced settings such as the number of relevant chunks, temperature, max tokens, max iterations, min quality score, and whether to force regeneration.
   - Example: 
     - Number of relevant chunks: 5
     - Temperature: 0.7
     - Max tokens: 1000
     - Max iterations: 3
     - Min quality score: 0.8
     - Force regeneration: Yes
7. **Generate Story**: The application will generate the story based on the provided inputs and configuration settings.
8. **Completion**: A panel will display the completion of the story generation and the location of the output file.

### Example

```python
from tui import generate_chapter_tui

generate_chapter_tui()
```

### 2. Interactive Mode

Select this option to enter the interactive story generation mode. This mode allows you to generate a plot outline, create chapters based on user queries or plot points, and refine the generated story iteratively.

#### Steps

1. **Generate Plot Outline**: Optionally, generate a plot outline based on a user-provided prompt.
   - Example: "A young wizard discovers a hidden power within himself."
2. **Display World Details**: The application will display the world details in a panel.
3. **Main Loop**: Enter the main loop for interactive story generation.
   - **Enter Story Query**: Provide a query or command (e.g., 'exit', 'new chapter').
     - Example: "The wizard meets a mysterious mentor."
   - **Use Previous Settings**: Optionally, use previous settings or provide new settings.
     - Example: Use previous settings for style, character, and situation.
   - **Generate Story**: The application will generate a story chapter based on the provided query and settings.
   - **Refine Story**: Optionally, refine the generated story iteratively.
     - Example: "Add more detail to the mentor's description."
   - **Save/Load/Export**: Save the session, load a session, or export the generated story.
     - Example: Save the session to "session1.json", load a session from "session2.json", or export the story to "story.md".

### Example

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

## Command-Line Interface (CLI)

The application also supports command-line automation for generating stories.

### Generate a Single Chapter

```bash
narr_ai_tive generate --query "A mystical journey begins" --style "epic fantasy"
```

### Generate with Character Focus

```bash
narr_ai_tive generate --input story.txt --character "Elena" --situation "dark forest"
```

## Python API

You can use the Python API to integrate the story generation functionality into your own scripts.

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
```

## Configuration

The application relies on a configuration file (`config.yaml`) for various settings, including the default story style, temperature, max tokens, and more. Ensure that this file is properly set up before running the application.

## Error Handling

The application includes error handling to catch and display any exceptions that occur during the story generation process. Errors are logged using the `logging` module and displayed in the console using `rich`.

## Conclusion

This guide provides an overview of how to navigate the Narr_ai_tive application after running it. Whether you are using the TUI, CLI, or Python API, the application offers a user-friendly interface for generating and refining stories. By leveraging advanced language models and rich character and world-building details, Narr_ai_tive ensures that the generated stories are engaging and high-quality.
