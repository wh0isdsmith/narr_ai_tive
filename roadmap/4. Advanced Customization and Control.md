# IV. Advanced Customization and Control

## **IV. Advanced Customization and Control**

* **A. Direct Prompt Editing:**

    * **1. "Show Prompt" Option:**
        * **Concept:** Provide a way to trigger the prompt display and editing mode.
        * **Implementation:**
            * **Hidden Command:** You could use a specific keyword (e.g., "/editprompt," "/showprompt") in a regular prompt (like the story query prompt) to activate this mode.
            * **Advanced Setting:** Add a toggle in an "Advanced Settings" menu (if you have one) that enables "Prompt Editing Mode."
            * **Button/Link in UI:** If you ever develop a graphical interface, a simple button would work.

    * **2. Displaying the Prompt:**
        * **Concept:** Show the generated prompt clearly within the TUI.
        * **Implementation:**
            * Use `rich.panel.Panel` to neatly display the prompt:
                ```python
                from rich.console import Console
                from rich.panel import Panel

                console = Console()

                def show_prompt(prompt: str):
                    """Displays the generated prompt in a panel."""
                    console.print(
                        Panel(prompt, title="Generated Prompt", border_style="yellow")
                    )

                # Example usage (after calling create_prompt()):
                prompt = create_prompt(...)
                if prompt_edit_mode:  # Check if the mode is activated
                    show_prompt(prompt)
                ```

    * **3. Editing the Prompt:**
        * **Concept:** Provide an in-TUI text editing interface.
        * **Implementation:**
            * **`prompt_toolkit`:** This library is excellent for creating interactive command-line applications and provides good text editing capabilities.
                ```python
                from prompt_toolkit import prompt
                from prompt_toolkit.history import InMemoryHistory

                def edit_prompt(prompt: str):
                    """Allows the user to edit the prompt using prompt_toolkit."""
                    edited_prompt = prompt(
                        "Edit the prompt (press ESC then Enter to submit):",
                        default=prompt,  # Show the original prompt as default
                        multiline=True,
                        history=InMemoryHistory(),
                    )
                    return edited_prompt

                # Example usage:
                if prompt_edit_mode:
                    show_prompt(prompt)
                    prompt = edit_prompt(prompt)  # Update the prompt with edits
                ```
            * **Simpler (but less user-friendly) approach:**
                * Use a regular `Prompt.ask()` to get the edited prompt as a single (potentially very long) string. This is not ideal for multi-line editing but might suffice for simple changes.

    * **4. Using the Edited Prompt:**
        * **Concept:** Pass the edited prompt to the model for generation.
        * **Implementation:**
            * Ensure that the `prompt` variable (or whatever you call it) holds the edited prompt after the editing step.
            * The rest of your generation logic should then use this `prompt` normally.

    * **5. Cautionary Notes and Input Validation:**
        * **Warnings:** Display a clear warning that direct prompt editing is an advanced feature and can lead to unexpected results.
        * **Validation:** Consider adding basic validation after editing:
            * Check for excessively long prompts (that might exceed the model's token limit).
            * Potentially check for obviously invalid formatting (though this is difficult to do comprehensively).

* **B. Parameter Tuning Per Chapter:**

    * **1. "Adjust Chapter Generation Settings" Option:**
        * **Concept:** Provide a menu or prompt to access parameter settings.
        * **Implementation:**
            * In `generate_chapter_tui()` or `interactive_loop()`:
                ```python
                from rich.prompt import Confirm

                if Confirm.ask("[bold blue]Adjust chapter generation settings?"):
                    # ... call a function to handle parameter adjustments
                    adjust_chapter_parameters(current_settings)
                ```

    * **2. Parameter Prompts:**
        * **Concept:** Use prompts to allow modifying parameters.
        * **Implementation:**
            ```python
            from rich.prompt import FloatPrompt, IntPrompt

            def adjust_chapter_parameters(current_settings: dict):
                """Prompts the user to adjust chapter-specific generation parameters."""
                temperature = FloatPrompt.ask(
                    "[bold blue]Enter temperature (0.0-1.0)",
                    default=current_settings.get("temperature", 0.7),
                )
                max_tokens = IntPrompt.ask(
                    "[bold blue]Enter max tokens",
                    default=current_settings.get("max_tokens", 500),
                )
                # ... add prompts for other parameters you want to expose

                current_settings["temperature"] = temperature
                current_settings["max_tokens"] = max_tokens
                # ... update current_settings with other modified parameters
            ```

    * **3. Storing Chapter-Specific Settings:**
        * **Concept:** Store the modified parameters so they can be used for the current chapter.
        * **Implementation:**
            * **`interactive_loop()`:** You're already using `current_settings`, which is a good place to store these.
            * **`generate_chapter_tui()`:** You might need to introduce a similar dictionary to hold chapter-specific settings.
            * **Example:** In `interactive_loop()`:
                ```python
                # ... inside the loop
                if action == "adjust_settings":  # Or however you trigger this
                    adjust_chapter_parameters(current_settings)
                # ... later, when calling generate_chapter() or generate_story()
                result = story_gen.generate_chapter(
                    # ... other parameters
                    temperature=current_settings.get("temperature", 0.7),
                    max_tokens=current_settings.get("max_tokens", 500),
                    # ... pass other parameters from current_settings
                )
                ```

    * **4. Passing Parameters to `generate_story()` and `generate_chapter()`:**
        * **Concept:** Make sure the modified parameters are used by the model.
        * **Implementation:**
            * Modify `generate_story()` to accept the parameters and pass them to `StoryGenerator.generate_chapter()`.
            * Modify `StoryGenerator.generate_chapter()` to use the passed parameters when calling `model.generate_content()`. You'll likely need to adjust the `generation_config` you're creating.

* **C. Embedding/Context Selection:**

    * **1. Displaying Top Chunks:**
        * **Concept:** After the semantic search, show the most relevant chunks to the user.
        * **Implementation:**
            ```python
            from rich.console import Console
            from rich.table import Table

            console = Console()

            def show_top_chunks(
                relevant_chunks: List[Tuple[str, int, float]],
                embeddings_dict: Dict[str, Any],
                top_n: int = 10,
            ):
                """Displays the top N relevant chunks with their similarity scores."""
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("Index", style="dim", width=6)
                table.add_column("File", min_width=15)
                table.add_column("Chunk", min_width=20)
                table.add_column("Similarity", min_width=10)

                for i, (file_path, chunk_idx, similarity) in enumerate(
                    relevant_chunks[:top_n]
                ):
                    chunk_content = embeddings_dict[file_path]["content"]
                    # You might need to extract a relevant snippet from chunk_content
                    # if the chunks are very long.
                    table.add_row(
                        str(i + 1), file_path, chunk_content[:100] + "...", f"{similarity:.4f}"  # Show first 100 characters of the chunk as an example
                    )

                console.print(table)

            # Example usage (in generate_chapter() after semantic_search):
            relevant_chunks = semantic_search(...)
            show_top_chunks(relevant_chunks, embeddings_dict)
            ```

    * **2. Chunk Selection:**
        * **Concept:** Allow users to select which chunks to include in the context.
        * **Implementation:**
            ```python
            from rich.prompt import Prompt

            def select_chunks(relevant_chunks: List[Tuple[str, int, float]]):
                """Allows the user to select which chunks to include in the context."""
                selected_indices = Prompt.ask(
                    "[bold blue]Select chunks to include (comma-separated, or None)",
                    default="None",
                )

                if selected_indices == "None":
                    return []

                selected_indices = [
                    int(idx.strip()) - 1 for idx in selected_indices.split(",")
                ]  # Adjust to 0-based indexing

                selected_chunks = [
                    chunk for i, chunk in enumerate(relevant_chunks) if i in selected_indices
                ]
                return selected_chunks

            # Example usage:
            selected_chunks = select_chunks(relevant_chunks)
            # ... later, use selected_chunks instead of relevant_chunks directly
            context = prepare_context(embeddings_dict, selected_chunks)
            ```

    * **3. Context Preparation:**
        * **Concept:** Use the selected chunks to create the context.
        * **Implementation:**
            * You'll likely need to modify your `prepare_context()` function to accept a list of `selected_chunks` (which might be different from the initial `relevant_chunks` returned by `semantic_search()`).

**IV. Example: Putting It Together (Partial)**

```python
# ... imports, utility functions

def generate_chapter_tui():
    # ... initial setup

    # --- Advanced Settings ---
    if Confirm.ask("[bold blue]Configure advanced settings?"):
        # ... (handle prompt editing mode, parameter adjustments)

    # ... other prompts (query, style, character, etc.)

    # --- Generate Story ---
    if multi_part:
       # ... handle multi part generation
    else:
        # ... (your existing single-part generation logic)

        # Load embeddings and perform semantic search
        embeddings_dict = _load_embeddings(Path("data/embeddings.json"))
        relevant_chunks = story_gen.semantic_search(
            query, embeddings_dict, top_n=top_n
        )
        selected_chunks = relevant_chunks

        # --- Embedding/Context Selection ---
        if advanced_context_selection_mode:  # A flag you set based on advanced settings
            show_top_chunks(relevant_chunks, embeddings_dict)
            selected_chunks = select_chunks(relevant_chunks)

        # Prepare context using selected_chunks
        context = story_gen.prepare_context(embeddings_dict, selected_chunks)

        # Create prompt (potentially using edited_prompt if in that mode)
        prompt = story_gen._create_prompt(
            # ... your parameters
            # ... pass in chapter-specific settings
        )

        if prompt_edit_mode:
            show_prompt(prompt)
            prompt = edit_prompt(prompt)  # Update the prompt with edits

        # Generate chapter using the prompt and parameters
        result = story_gen.generate_chapter(
            # ... other parameters
            # ... pass in chapter-specific settings (temperature, max_tokens, etc.)
        )

# ... other functions (create_prompt, generate_chapter, adjust_chapter_parameters, etc.)
```

**V. Further Refinements**

* **Context Snippet Extraction:** If your chunks are very long, you might want to extract relevant snippets from the selected chunks instead of showing the entire chunk.
* **Chunk Summarization:** Consider using a text summarization technique to provide more concise summaries of the chunks in `show_top_chunks()`.
* **Parameter Presets:** Allow users to save and load sets of parameters (e.g., "High Creativity," "Low Randomness").

---
