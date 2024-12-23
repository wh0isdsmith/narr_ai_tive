import logging
from typing import Optional
from pathlib import Path

from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.progress import track
from rich.panel import Panel
from rich.live import Live

from .utils import (
    generate_story,
    load_config,
    load_api_key
)

logger = logging.getLogger("chapter")
console = Console()


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

    # Advanced options (optional)
    if Confirm.ask("Configure advanced options?"):
        top_n = int(Prompt.ask(
            "[bold blue]Enter the number of relevant chunks (top_n)", default="3"))
        temperature = float(
            Prompt.ask("[bold blue]Enter the temperature",
                       default=str(config['generation']['temperature']))
        )
        max_tokens = int(
            Prompt.ask("[bold blue]Enter the max tokens",
                       default=str(config['generation']['max_tokens']))
        )
        max_iterations = int(
            Prompt.ask("[bold blue]Enter the max iterations",
                       default=str(config['evaluation']['max_iterations']))
        )
        min_quality = float(
            Prompt.ask(
                "[bold blue]Enter the min quality", default=str(config['evaluation']['min_quality_score'])
            )
        )
        force = Confirm.ask("Force regeneration (ignore cache)?")
    else:
        top_n = 3
        temperature = config['generation']['temperature']
        max_tokens = config['generation']['max_tokens']
        max_iterations = config['evaluation']['max_iterations']
        min_quality = config['evaluation']['min_quality_score']
        force = False

    log_level = "INFO"  # Set log level for generate_story

    try:
        with Live(console=console, refresh_per_second=4) as live:
            def update_progress(step, total, description):
                table = Table(title=description)
                table.add_column("Step", justify="right",
                                 style="cyan", no_wrap=True)
                table.add_column("Progress", style="magenta")
                table.add_row(
                    f"{step}/{total}", f"[progress.percentage]{(step + 1) / total * 100:>3.0f}%")
                live.update(table)

            for step in track(range(100), description="Generating story..."):
                # Simulate story generation process
                if step % 20 == 0:
                    update_progress(step + 1, 100, "Generating Story")

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

        console.print(
            Panel(
                f"Story generation complete. Check the output file: {
                    output_file}",
                style="bold green",
            )
        )
    except Exception as e:
        console.print(
            f"[bold red]Error during story generation: {e}[/bold red]")
