# Narr_ai_tive/app/tui.py
import logging
from typing import Optional
from pathlib import Path

from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table
from rich.progress import track
from rich.live import Live
from rich.layout import Layout
import google.generativeai as genai

from .utils import (
    generate_story,
    load_config,
    load_api_key,
    resolve_data_path,
    _load_embeddings,
    StoryGenerator,
    load_character_profiles,  # Import load_character_profiles
    load_world_details,  # Import load_world_details
)
from .plot import PlotGenerator
from .interactive import interactive_loop
import json
from .setup_logging import setup_logging

logger = logging.getLogger("tui")
console = Console()


def get_embeddings_dict():
    """Helper function to get embeddings_dict with error handling."""
    embeddings_file = resolve_data_path("data/embeddings.json")
    try:
        embeddings_dict = _load_embeddings(embeddings_file)
    except FileNotFoundError:
        console.print(
            f"[bold yellow]Warning: Embeddings file not found at {
                embeddings_file}. Functionality relying on embeddings will be limited.[/bold yellow]"
        )
        embeddings_dict = {}
    except Exception as e:
        console.print(f"[bold red]Error loading embeddings: {e}[/bold red]")
        embeddings_dict = {}
    return embeddings_dict


def generate_chapter_tui():
    """TUI for generating a single chapter."""
    console.clear()
    console.print(Panel("Generate a Single Chapter", style="bold blue"))

    config = load_config()
    api_key = load_api_key(config)

    query = Prompt.ask("[bold blue]Enter your story query")
    style = Prompt.ask("[bold blue]Enter the story style",
                       default=config['generation'].get('style', "dark fantasy"))
    character = Prompt.ask("[bold blue]Enter the focus character (optional)")
    situation = Prompt.ask("[bold blue]Enter the story situation (optional)")
    output_file = Prompt.ask("[bold blue]Enter the output file (optional)")

    if Confirm.ask("Configure advanced options?"):
        top_n = int(Prompt.ask("[bold blue]Enter the number of relevant chunks (top_n)", default="3"))
        temperature = float(Prompt.ask("[bold blue]Enter the temperature", default=str(config['generation']['temperature'])))
        max_tokens = int(Prompt.ask("[bold blue]Enter the max tokens", default=str(config['generation']['max_tokens'])))
        max_iterations = int(Prompt.ask("[bold blue]Enter the max iterations", default=str(config['evaluation']['max_iterations'])))
        min_quality = float(Prompt.ask("[bold blue]Enter the min quality", default=str(config['evaluation']['min_quality_score'])))
        force = Confirm.ask("Force regeneration (ignore cache)?")
    else:
        top_n = 3
        temperature = config['generation']['temperature']
        max_tokens = config['generation']['max_tokens']
        max_iterations = config['evaluation']['max_iterations']
        min_quality = config['evaluation']['min_quality_score']
        force = False

    log_level = "INFO"

    try:
        with Live(console=console, refresh_per_second=4) as live:
            def update_progress(step, total, description):
                table = Table(title=description)
                table.add_column("Step", justify="right", style="cyan", no_wrap=True)
                table.add_column("Progress", style="magenta")
                table.add_row(f"{step}/{total}", f"[progress.percentage]{(step + 1) / total * 100:>3.0f}%")
                live.update(table)

            update_progress(1, 4, "Loading Configuration and API Key")
            config = load_config()
            api_key = load_api_key(config)

            update_progress(2, 4, "Initializing Model")
            generation_config = {
                "temperature": temperature,
                "top_p": config['generation']['top_p'],
                "max_output_tokens": max_tokens
            }
            model = genai.GenerativeModel(
                model_name=config['generation']['model'],
                generation_config=generation_config
            )

            update_progress(3, 4, "Loading Embeddings and Data")
            embeddings_dict = _load_embeddings(Path("data/embeddings.json"))
            character_profiles = load_character_profiles(config['paths']['character_profiles'])
            world_details = load_world_details(config['paths']['world_details'])

            update_progress(4, 4, "Generating Story")
            generate_story(
                query,
                Path("data/embeddings.json"),
                Path(output_file) if output_file else None,
                "config.yaml",
                style,
                character,
                situation,
                top_n,
                temperature,
                max_tokens,
                max_iterations,
                min_quality,
                api_key,
                log_level,
                force,
            )

        console.print(Panel(f"Story generation complete. Check the output file: {output_file}", style="bold green"))
    except Exception as e:
        console.print(f"[bold red]Error during story generation: {e}[/bold red]")


def interactive_story_tui():
    """TUI for interactive story generation."""
    console.clear()
    console.print(Panel("Interactive Story Generation", style="bold blue"))

    config = load_config()
    api_key = load_api_key(config)
    embeddings_dict = get_embeddings_dict()
    character_profiles_path = resolve_data_path(config["paths"]["character_profiles"])
    world_details_path = resolve_data_path(config["paths"]["world_details"])

    character_profiles = load_character_profiles(character_profiles_path)
    world_details = load_world_details(world_details_path)

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name=config["generation"]["model"],
            generation_config={
                "temperature": config["generation"]["temperature"],
                "top_p": config["generation"]["top_p"],
                "max_output_tokens": config["generation"]["max_tokens"],
            }
        )
    except Exception as e:
        logger.exception("Error initializing model")
        console.print(f"[bold red]Error initializing model: {e}[/bold red]")
        return

    try:
        story_gen = StoryGenerator(model, character_profiles, world_details)
        plot_gen = PlotGenerator(story_gen.model)
    except Exception as e:
        logger.exception("Error initializing story components")
        console.print(f"[bold red]Error initializing story components: {e}[/bold red]")
        return

    session_history = []
    current_settings = {}

    interactive_loop(story_gen, plot_gen, embeddings_dict, session_history, current_settings)


def main_menu():
    """Main menu for the TUI."""
    setup_logging("INFO")  # Set up logging with INFO level
    while True:
        console.clear()
        console.print(
            Panel("Narrative AI Story Generator", style="bold green"))
        console.print("1. Generate a single chapter")
        console.print("2. Generate an interactive story")
        console.print("3. Exit")

        choice = Prompt.ask("Choose an option", choices=[
                            "1", "2", "3"], default="3")

        if choice == "1":
            generate_chapter_tui()
        elif choice == "2":
            interactive_story_tui()
        elif choice == "3":
            console.print("Exiting...")
            break
