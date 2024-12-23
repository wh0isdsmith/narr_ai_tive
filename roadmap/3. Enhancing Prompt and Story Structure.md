# III. Enhancing Prompt and Story Structure

## **III. Enhancing Prompt and Story Structure**

* **A. Plot Point Integration:**

    * **1. Plot Point Selection with Descriptions:**
        * **Concept:** Display plot points with brief descriptions to help users choose.
        * **Implementation:**
            ```python
            from rich.prompt import Prompt
            from rich.table import Table
            from rich.console import Console

            console = Console()

            def prompt_for_plot_point(plot_outline: str):
                """Prompts the user to select a plot point, showing descriptions."""
                plot_points = plot_outline.split("\n")
                plot_points = [
                    pp.strip() for pp in plot_points if pp.strip()
                ]  # Clean up points

                if not plot_points:
                    return None

                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("Number", style="dim", width=6)
                table.add_column("Plot Point", min_width=20)

                for i, point in enumerate(plot_points):
                    # Assuming a simple format like "1. [Plot Point Description]"
                    # You might need to adjust parsing if your format is different.
                    table.add_row(str(i + 1), point)

                console.print(table)

                selected_point_index = Prompt.ask(
                    "[bold blue]Choose a plot point to focus on (or None)",
                    choices=[str(i + 1) for i in range(len(plot_points))] + ["None"],
                    default="None",
                )

                if selected_point_index == "None":
                    return None

                selected_point = plot_points[int(selected_point_index) - 1]
                return selected_point

            # Example usage in interactive_loop():
            plot_outline = plot_gen.generate_plot_outline(plot_prompt) # Assuming you have plot_gen
            # ...
            selected_plot_point = prompt_for_plot_point(plot_outline)
            ```
        * **Benefits:** Clearer choices, users can make more informed decisions.

    * **2. Plot Point Adherence Level:**
        * **Concept:** Allow users to specify how strictly the chapter should follow the selected plot point.
        * **Implementation:**
            ```python
            from rich.prompt import Prompt

            def prompt_for_adherence_level():
                """Prompts the user to select the plot point adherence level."""
                adherence_level = Prompt.ask(
                    "[bold blue]How closely should this chapter follow the plot point?",
                    choices=["Strictly", "Loosely", "Inspiration only"],
                    default="Loosely",
                )
                return adherence_level

            # Example usage:
            if selected_plot_point:
                adherence_level = prompt_for_adherence_level()
            ```
        * **Benefits:** More control over plot usage, allows for deviations or creative interpretations.

    * **3. Marking Plot Points as Completed/Modified:**
        * **Concept:** Add a mechanism to track the status of plot points.
        * **Implementation:**
            * **Data Structure:** You'll need a way to store the status of each plot point. You could:
                * Modify the `plot_outline` string directly (e.g., prefix completed points with "[DONE]").
                * Create a separate list or dictionary to track the status of each point.
            * **Marking Options:** In `interactive_loop()`, after generating a chapter based on a plot point, ask:
                ```python
                mark_as = Prompt.ask(
                    "[bold blue]Mark this plot point as:",
                    choices=["Completed", "Modified", "Skip", "None"],
                    default="None",
                )
                ```
            * **Updating Status:** Implement logic to update the `plot_outline` or your chosen data structure based on the user's selection.
            * **Displaying Status:** When displaying plot points (in `prompt_for_plot_point()`), show their status (e.g., "Completed," "Modified").
        * **Considerations:**
            * Decide on a clear format for storing and displaying the status.
            * Consider how to handle modified plot points (e.g., allow users to view the original and modified versions).

    * **4. Prepended Plot Point:**
        * **Concept:** Add the selected plot point at the beginning of the prompt.
        * **Implementation:**
            * In `generate_chapter()` (or wherever you call `create_prompt()`)
                ```python
                if selected_plot_point:
                    if adherence_level == "Strictly":
                        prompt = f"This chapter should strictly follow the plot point: {
                            selected_plot_point}\n\n" + prompt
                    elif adherence_level == "Loosely":
                        prompt = f"This chapter should loosely follow the plot point: {
                            selected_plot_point}\n\n" + prompt
                    else:  # Inspiration only
                        prompt = f"This chapter should be inspired by the plot point: {
                            selected_plot_point}\n\n" + prompt
                ```

* **B. Customizable Chapter Tone and Mood:**

    * **1. Tone/Mood Selection:**
        * **Concept:** Allow users to choose the overall tone or mood of the chapter.
        * **Implementation:**
            ```python
            from rich.prompt import Prompt

            def prompt_for_tone():
                """Prompts the user to select the chapter's tone."""
                tone_options = [
                    "Suspenseful",
                    "Action-packed",
                    "Romantic",
                    "Mysterious",
                    "Humorous",
                    "Dark",
                    "Hopeful",
                    "Dramatic",
                    "Neutral",
                    "Custom...",
                ]
                tone = Prompt.ask(
                    "[bold blue]What is the overall tone of this chapter?",
                    choices=tone_options,
                    default="Neutral",
                )
                if tone == "Custom...":
                    tone = Prompt.ask("[bold blue]Enter the desired tone")
                return tone

            # Example usage:
            tone = prompt_for_tone()
            ```

    * **2. Tone/Mood Intensity (Optional):**
        * **Concept:** Allow users to specify the intensity of the chosen tone/mood.
        * **Implementation:**
            * Add a follow-up prompt for intensity, similar to the emotion intensity prompt.

    * **3. Incorporating Tone into Prompt:**
        * **Concept:** Use the selected tone to guide the language model.
        * **Implementation:**
            * In `create_prompt()`:
                ```python
                if tone:
                    prompt.append(f"Write this chapter with a {tone} tone.")
                ```
            * You can also add more specific instructions based on the tone (e.g., "Use vivid imagery and descriptive language to create a suspenseful atmosphere.").

* **C. Style Prompt Refinements:**

    * **1. Style Refinement Prompt:**
        * **Concept:** Allow users to add specific stylistic instructions.
        * **Implementation:**
            ```python
            from rich.prompt import Prompt

            def prompt_for_style_refinements():
                """Prompts the user for specific style refinements."""
                refinements = Prompt.ask(
                    "[bold blue]Are there any specific stylistic elements to emphasize in this chapter (or None)?"
                )
                return refinements

            # Example usage:
            style_refinements = prompt_for_style_refinements()
            ```

    * **2. Incorporating Refinements into Prompt:**
        * **Concept:** Append the refinements to the prompt.
        * **Implementation:**
            * In `create_prompt()`:
                ```python
                if style_refinements and style_refinements != "None":
                    prompt.append(
                        f"Stylistic refinements for this chapter: {
                            style_refinements}"
                    )
                ```

* **D. Multi-Part Chapter Generation:**

    * **1. Multi-Part Option:**
        * **Concept:** Add an option to generate the chapter in parts.
        * **Implementation:**
            ```python
            from rich.prompt import Confirm

            # In generate_chapter_tui() or interactive_loop():
            multi_part = Confirm.ask(
                "[bold blue]Generate this chapter in multiple parts?"
            )
            ```

    * **2. Part-Specific Prompts:**
        * **Concept:** If the user chooses multi-part, prompt for the focus of each part.
        * **Implementation:**
            ```python
            from rich.prompt import Prompt

            def generate_multi_part_chapter( # ... parameters ...
                                            ):
                parts = []
                part_num = 1
                while True:
                    part_focus = Prompt.ask(
                        f"[bold blue]Enter the focus or scene for part {
                            part_num} (or type 'done')"
                    )
                    if part_focus.lower() == "done":
                        break

                    # Generate the part (you'll need to adapt your generation logic)
                    # ... (call generate_chapter() or a modified version for a single part)
                    part = generate_part(
                        # ... your parameters, including part_focus
                    )
                    parts.append(part)
                    part_num += 1

                # Combine the parts
                full_chapter = "\n\n".join(parts)
                return full_chapter

            def generate_part( # ... parameters
                              ):
                # You may need a modified create_prompt() that takes the part_focus
                # and any other relevant information for generating a single part.
                part_prompt = create_part_prompt(# ... your parameters, including part_focus
                                                )
                # Call the model to generate the part
                response = model.generate_content(part_prompt)

                # ... (error handling, etc.)
                return response.text
            ```
            * **Key Idea:** You need a way to create prompts specific to each part and then call your generation logic for each part separately.

    * **3. Combining Parts:**
        * **Concept:** Join the generated parts with appropriate separators.
        * **Implementation:**
            * The `generate_multi_part_chapter()` function above shows a basic way to combine parts using `"\n\n"` as a separator. You might want to add more sophisticated transitions or adjust the separator based on the content.

**III. Example: Putting It Together**

```python
# ... (imports, utility functions)

def generate_chapter_tui():
    # ... (initial setup)

    # --- Plot Point Integration ---
    plot_outline = # ... (load or generate plot outline)
    selected_plot_point = prompt_for_plot_point(plot_outline)
    if selected_plot_point:
        adherence_level = prompt_for_adherence_level()
        # ... (handle plot point marking)

    # --- Tone and Style ---
    tone = prompt_for_tone()
    style_refinements = prompt_for_style_refinements()

    # --- Multi-Part Generation ---
    multi_part = Confirm.ask(
        "[bold blue]Generate this chapter in multiple parts?"
    )
    if multi_part:
        full_chapter = generate_multi_part_chapter(
            # ... pass in relevant parameters, including plot point, tone, style refinements, etc.
        )
        # ... (handle output of full_chapter)
    else:
        # ... (your existing single-part generation logic)
        # ... (call generate_story, passing in plot point, adherence level, tone, style refinements)

# ... (other functions like create_prompt, generate_multi_part_chapter, etc.)
```

**IV. Further Refinements**

* **Plot Outline Visualization:** Consider using a `rich` `Tree` to display the plot outline with status indicators (completed, modified, etc.).
* **Dynamic Tone Adjustments:** Allow users to change the tone/mood *within* a chapter (e.g., start suspenseful, then become hopeful). This would likely require multi-part generation or a more advanced prompt engineering approach.
* **Style Presets:** Create predefined style presets (e.g., "Hemingway-esque," "Flowery Prose") that users can select from, in addition to the refinement prompt.

---
