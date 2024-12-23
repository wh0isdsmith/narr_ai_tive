# Narr_ai_tive/app/interactive.py
import logging
import json
from pathlib import Path

from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
import google.generativeai as genai

from .utils import (
    load_config,
    load_api_key,
    resolve_data_path,
    StoryGenerator
)
from .plot import PlotGenerator

# Set up a logger for this module.
logger = logging.getLogger("interactive")
console = Console()


def interactive_loop(
    story_gen: StoryGenerator,
    plot_gen: PlotGenerator,
    embeddings_dict: dict,
    session_history: list,
    current_settings: dict,
):
    """Main loop for the interactive story generation."""
    plot_outline = ""
    chapter_counter = 0

    use_outline = Prompt.ask(
        "Generate a plot outline? (yes/no)", choices=["yes", "no"], default="no"
    )
    if use_outline.lower() == "yes":
        plot_prompt = Prompt.ask("Enter a prompt for the plot outline")
        console.print("[bold green]Generating plot outline...[/bold green]")
        try:
            plot_outline = plot_gen.generate_plot_outline(plot_prompt)
            if plot_outline:
                console.print(
                    Panel(
                        plot_outline,
                        title="Generated Plot Outline",
                        border_style="cyan",
                    )
                )
            else:
                console.print("[red]Failed to generate plot outline[/red]")
        except Exception as e:
            console.print(
                f"[bold red]Error generating plot outline: {e}[/bold red]"
            )

    # Worldbuilding details
    console.print(
        Panel(
            json.dumps(story_gen.world_details, indent=2),
            title="World Details",
            border_style="blue",
        )
    )

    while True:
        query = Prompt.ask(
            "Enter your story query (or type 'exit' to quit, 'new chapter' for next chapter based on outline)"
        )
        session_history.append({"type": "query", "content": query})

        if query.lower() == "exit":
            break

        if query.lower() == "new chapter":
            if not plot_outline:
                console.print(
                    "[red]No plot outline available. Please generate or load an outline first.[/red]"
                )
                continue

            plot_parts = plot_outline.split("\n")  # Basic plot advancement
            if chapter_counter < len(plot_parts):
                current_plot_point = plot_parts[chapter_counter]
                console.print(
                    f"[bold green]Generating chapter based on: {
                        current_plot_point}[/bold green]"
                )
                query = current_plot_point
                chapter_counter += 1
            else:
                console.print("[red]End of plot outline reached.[/red]")
                continue

        use_previous = Prompt.ask(
            "Use previous settings? (yes/no)",
            choices=["yes", "no"],
            default="yes",
        )
        if use_previous.lower() != "yes":
            style = Prompt.ask(
                "Enter the story style", default="dark fantasy"
            )
            current_settings["style"] = style

            use_style_prompt = Prompt.ask(
                "Provide a style prompt for the story? (yes/no)",
                choices=["yes", "no"],
                default="no",
            )
            if use_style_prompt.lower() == "yes":
                style_prompt = Prompt.ask("Enter the style prompt")
                current_settings["style_prompt"] = style_prompt
            else:
                current_settings.pop("style_prompt", None)

            character = Prompt.ask(
                "Enter the focus character (optional)", default=""
            )
            current_settings["character"] = character

            situation = Prompt.ask(
                "Enter the story situation (optional)", default=""
            )
            current_settings["situation"] = situation

            location_options = list(
                story_gen.world_details["locations"].keys()
            ) + ["None"]
            location = Prompt.ask(
                "Choose a location (optional)",
                choices=location_options,
                default="None",
            )
            if location != "None":
                situation = f"{situation} (in {location})"
            current_settings["situation"] = situation

            theme_options = list(story_gen.world_details["themes"].keys()) + [
                "None"
            ]
            theme = Prompt.ask(
                "Choose a theme to emphasize (optional)",
                choices=theme_options,
                default="None",
            )
            if theme != "None":
                situation = f"{situation} (focusing on the theme of {theme})"
            current_settings["situation"] = situation

            motif_options = list(story_gen.world_details["motifs"].keys()) + [
                "None"
            ]
            motif = Prompt.ask(
                "Choose a motif to use (optional)",
                choices=motif_options,
                default="None",
            )
            if motif != "None":
                situation = f"{situation} (using the motif of {motif})"
            current_settings["situation"] = situation
        else:
            style = current_settings.get("style", "dark fantasy")
            style_prompt = current_settings.get("style_prompt")
            character = current_settings.get("character", "")
            situation = current_settings.get("situation", "")

        previous_attempt = None
        refine = True
        generated_text = None

        while refine:
            console.print("[bold green]Generating story...[/bold green]")
            try:
                result = story_gen.generate_chapter(
                    queries=[query],
                    embeddings_dict=embeddings_dict,
                    style=style,
                    character=character,
                    situation=situation,
                    style_prompt=style_prompt,
                    plot_outline=plot_outline,
                )

                if result:
                    generated_text = result["text"]
                    console.print(
                        Panel(
                            generated_text,
                            title="Generated Story",
                            border_style="cyan",
                        )
                    )
                    session_history.append(
                        {"type": "generation", "content": generated_text}
                    )
                    refine_choice = Prompt.ask(
                        "Do you want to refine the story? (yes/no)",
                        choices=["yes", "no"],
                        default="no",
                    )
                    refine = refine_choice.lower() == "yes"
                    if refine:
                        previous_attempt = generated_text
                else:
                    console.print("[red]Failed to generate story[/red]")
                    refine = False
            except Exception as e:
                console.print(
                    f"[bold red]Error during story generation: {e}[/bold red]"
                )
                # Log the full traceback
                logger.exception("Error during story generation")
                refine = False

        action = Prompt.ask(
            "Do you want to [save] the session, [load] a session, [export] the story, or [exit]?",
            choices=["save", "load", "export", "exit"],
        )
        if action == "save":
            session_data = {
                "settings": current_settings,
                "plot_outline": plot_outline,
                "chapter_counter": chapter_counter,
                "history": session_history,
            }
            try:
                story_gen.save_session(session_data)
            except Exception as e:
                console.print(
                    f"[bold red]Error saving session: {e}[/bold red]"
                )
                logger.exception("Error saving session")
        elif action == "load":
            load_filename = Prompt.ask("Enter the filename to load")
            try:
                session_data = story_gen.load_session(load_filename)
                if session_data:
                    current_settings = session_data.get("settings", {})
                    plot_outline = session_data.get("plot_outline", "")
                    chapter_counter = session_data.get("chapter_counter", 0)
                    session_history.extend(session_data.get("history", []))
                    console.print(f"Session loaded from {load_filename}")
                else:
                    console.print(
                        "[yellow]No session data found in the loaded file.[/yellow]"
                    )
            except FileNotFoundError:
                console.print(
                    f"[bold red]Error: Session file not found: {
                        load_filename}[/bold red]"
                )
            except json.JSONDecodeError as e:
                console.print(
                    f"[bold red]Error parsing session file: {e}[/bold red]"
                )
            except Exception as e:
                console.print(
                    f"[bold red]Error loading session: {e}[/bold red]"
                )
                logger.exception("Error loading session")
        elif action == "export":
            if generated_text:
                export_format = Prompt.ask(
                    "Enter the export format", choices=["txt", "md", "html"]
                )
                try:
                    story_gen.export_story(
                        generated_text, format=export_format
                    )
                except Exception as e:
                    console.print(
                        f"[bold red]Error exporting story: {e}[/bold red]"
                    )
                    logger.exception("Error exporting story")
            else:
                console.print("[yellow]No story generated to export.[/yellow]")
