import logging
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError
import requests
from rich.console import Console

console = Console()

# Get logger configured by cli.py
logger = logging.getLogger('plot')


class PlotGenerationError(Exception):
    """Custom exception for plot generation errors."""
    pass


class PlotGenerator:
    def __init__(self, model):
        self.model = model

    def generate_plot_outline(self, prompt: str, max_length: int = 500) -> str:
        """Generates a plot outline based on a prompt.

        Args:
            prompt: The prompt to generate the plot outline from.
            max_length: An approximate maximum word length for the outline.

        Returns:
            The generated plot outline.

        Raises:
            PlotGenerationError: If an error occurs during plot generation.
        """
        try:
            full_prompt = f"Generate a detailed plot outline for a story based on the following prompt (in approximately less than {
                max_length} words):\n\n{prompt}"
            response = self.model.generate_content(full_prompt)
            if response.text:
                return response.text
            else:
                logger.warning(
                    f"Plot outline generation returned an empty response for prompt: {prompt}")
                console.print("[red]Failed to generate plot outline[/red]")
        except GoogleAPIError as e:
            logger.error(f"Google API error during plot outline generation for prompt: {
                         prompt}. Error: {e}")
            console.print(
                f"[bold red]Error generating plot outline: {e}[/bold red]")
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error during plot outline generation for prompt: {
                         prompt}. Error: {e}")
            console.print(
                f"[bold red]Error generating plot outline: {e}[/bold red]")
        except Exception as e:
            logger.exception(
                f"An unexpected error occurred during plot outline generation for prompt: {prompt}")
            console.print(
                f"[bold red]Error generating plot outline: {e}[/bold red]")
