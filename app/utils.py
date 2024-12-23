import logging
from typing import Any, Dict, List, Optional, Tuple, Union
from pathlib import Path
import hashlib
import json

import yaml
import google.generativeai as genai

from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table
from rich.text import Text
from rich.panel import Panel

from rouge import Rouge
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from .character import load_character_profiles
from .world import load_world_details
from .semantic_search import semantic_search
from .context import prepare_context
from .prompt import create_prompt
from .session import save_session, load_session
from .export import export_story
from .path_utils import resolve_data_path
from .setup_logging import setup_logging

# Initialize console
console = Console()

# Get logger
logger = logging.getLogger('utils')

CONFIG = None

# Custom Exceptions


class APIKeyError(Exception):
    """Custom exception for API key related errors."""
    pass


class CacheError(Exception):
    """Custom exception for cache related errors."""
    pass


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class InputError(Exception):
    """Custom exception for input related errors."""
    pass


class ConfigError(Exception):
    """Custom exception for configuration related errors."""
    pass


def load_config(config_path: str = 'config.yaml'):
    """Loads the configuration from the specified YAML file."""
    global CONFIG
    if CONFIG is None:
        config_path = Path(__file__).parent.parent / config_path
        try:
            with open(config_path, 'r') as f:
                CONFIG = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {config_path}")
        except FileNotFoundError:
            logger.error(f"Config file not found at {config_path}")
            raise FileNotFoundError(f"Config file not found at {config_path}")
        except yaml.YAMLError as e:
            logger.error(f"Error parsing config file: {e}")
            raise yaml.YAMLError(f"Error parsing config file: {e}")
    return CONFIG


def get_config():
    """Returns the loaded configuration."""
    if CONFIG is None:
        raise RuntimeError(
            "Configuration has not been loaded. Call load_config() first.")
    return CONFIG


# Load config on import (optional, can be loaded explicitly elsewhere)
try:
    load_config()
except (FileNotFoundError, yaml.YAMLError) as e:
    logger.warning(f"Configuration could not be loaded on import: {e}")


def create_progress() -> Progress:
    """Create a rich progress bar with custom formatting."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(complete_style="green", finished_style="bright_green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
    )

# Metrics calculation


def calculate_quality_score(text: str) -> float:
    """Placeholder for a more sophisticated quality assessment."""
    # Very basic quality score based on length
    return min(1.0, len(text) / 1000.0)


def calculate_rouge_scores(text: str, embeddings_dict: Dict, top_n: int) -> Dict[str, float]:
    """Calculates ROUGE scores against top_n relevant chunks."""
    if not embeddings_dict:
        return {'rouge-1': 0.0, 'rouge-2': 0.0, 'rouge-l': 0.0}

    # Extract relevant chunks from embeddings (adapt this based on your embeddings structure)
    references = []
    for file_path, data in embeddings_dict.items():
                for chunk in data.get('chunk_content', []):
                    references.append(chunk)

    if not references:
        return {'rouge-1': 0.0, 'rouge-2': 0.0, 'rouge-l': 0.0}

    # Get top_n references if necessary
    references = references[:top_n]

    rouge = Rouge()
    try:
        scores = rouge.get_scores(text, references, avg=True)
        return {
            'rouge-1': scores['rouge-1']['f'],
            'rouge-2': scores['rouge-2']['f'],
            'rouge-l': scores['rouge-l']['f'],
        }
    except ValueError:
        logger.warning("ROUGE calculation failed due to empty reference or generated text.")
        return {'rouge-1': 0.0, 'rouge-2': 0.0, 'rouge-l': 0.0}
    except Exception as e:
        logger.error(f"Unexpected error during ROUGE calculation: {e}")
        return {'rouge-1': 0.0, 'rouge-2': 0.0, 'rouge-l': 0.0}

# Assuming you have a pre-trained SentenceTransformer model
semantic_model = SentenceTransformer('all-mpnet-base-v2')

def calculate_semantic_similarity(text: str, embeddings_dict: Dict) -> float:
    """Calculates average semantic similarity to relevant chunks using Sentence Transformers."""
    if not embeddings_dict:
        return 0.0

    # Extract chunk embeddings
    chunk_embeddings = []
    for file_path, data in embeddings_dict.items():
        chunk_embeddings.extend(data['chunk_embeddings'])

    if not chunk_embeddings:
        return 0.0

    try:
        # Generate embedding for the generated text
        text_embedding = semantic_model.encode([text])[0]  # Encode expects a list of strings

        # Calculate average cosine similarity
        similarities = cosine_similarity([text_embedding], chunk_embeddings)[0]
        avg_similarity = sum(similarities) / len(similarities)
        return avg_similarity
    except Exception as e:
        logger.error(f"Error during semantic similarity calculation: {e}")
        return 0.0

def calculate_lexical_diversity(text: str) -> float:
    """Calculates the lexical diversity of the text."""
    words = text.split()
    if not words:
        return 0.0
    return len(set(words)) / len(words)

def evaluate_story(text: str, embeddings_dict: Dict[str, Any], top_n: int, rouge_threshold: float) -> Dict[str, Any]:
    """Evaluates the generated story based on various metrics."""
    metrics = {}

    # 1. Quality Score (placeholder - replace with your actual quality metric)
    metrics['quality_score'] = calculate_quality_score(text)

    # 2. ROUGE Scores
    rouge_scores = calculate_rouge_scores(text, embeddings_dict, top_n)
    metrics.update(rouge_scores)

    # 3. Semantic Similarity
    metrics['semantic_similarity'] = calculate_semantic_similarity(
        text, embeddings_dict
    )

    # 4. Statistics
    metrics['word_count'] = len(text.split())
    sentences = text.split('.')  # Simple sentence splitting
    metrics['sentence_count'] = len(sentences)
    metrics['avg_sentence_length'] = metrics['word_count'] / \
        max(1, metrics['sentence_count'])  # Avoid division by zero
    metrics['lexical_diversity'] = calculate_lexical_diversity(text)

    return metrics

def create_metrics_table(metrics: Dict[str, float]) -> Table:
    """Create a rich table for displaying evaluation metrics."""
    table = Table(title="Generation Metrics", show_header=True,
                  header_style="bold magenta")

    table.add_column("Metric", style="cyan", width=20)
    table.add_column("Value", justify="right", style="green")
    table.add_column("Status", justify="right", style="yellow", width=10)

    categories = {
        "Quality": ["quality_score"],
        "ROUGE": ["rouge-1", "rouge-2", "rouge-l"],
        "Semantic": ["semantic_similarity", "bleu"],
        "Statistics": ["word_count", "sentence_count", "avg_sentence_length", "lexical_diversity"]
    }

    for category, metric_names in categories.items():
        table.add_row(f"[bold]{category}[/bold]", "", "", style="dim")
        for metric in metric_names:
            if metric in metrics:
                value = metrics[metric]
                if isinstance(value, float):
                    status = "✓" if value > 0.5 else "✗"
                    color = "green" if value > 0.5 else "red"
                    table.add_row(
                        f"  {metric}",
                        f"[{color}]{value:.3f}[/{color}]",
                        f"[{color}]{status}[/{color}]"
                    )
                else:
                    table.add_row(f"  {metric}", str(value), "")

    return table

def format_story_output(text: str, title: Optional[str] = None) -> Panel:
    """Format story text with enhanced rich formatting."""
    formatted_text = Text()

    for paragraph in text.split('\n\n'):
        # Add paragraph formatting
        if paragraph.startswith('"') and paragraph.endswith('"'):
            # Dialog paragraphs
            formatted_text.append(paragraph, style="yellow")
        elif any(word in paragraph.lower() for word in ["said", "asked", "replied"]):
            # Paragraphs with dialog attribution
            formatted_text.append(paragraph, style="italic")
        else:
            # Standard paragraphs
            formatted_text.append(paragraph, style="default")
        formatted_text.append("\n\n")

    return Panel(
        formatted_text,
        title=title or "Generated Story",
        title_align="left",
        border_style="cyan",
        padding=(1, 2),
        highlight=True
    )

def compute_cache_key(params: Dict[str, Any]) -> str:
    """Generate a cache key from parameters."""
    sorted_params = dict(sorted(params.items()))
    params_str = json.dumps(sorted_params, sort_keys=True)
    return hashlib.md5(params_str.encode()).hexdigest()

def load_story_cache(cache_path: Path) -> Dict[str, Any]:
    """Load the story generation cache."""
    try:
        if cache_path.exists():
            with open(cache_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except json.JSONDecodeError as e:
        raise CacheError(f"Corrupted cache file: {e}") from e
    except PermissionError as e:
        raise CacheError(f"Permission denied accessing cache: {e}") from e
    except Exception as e:
        raise CacheError(f"Unexpected error loading cache: {e}") from e
    return {}

def save_story_cache(cache: Dict[str, Any], cache_path: Path) -> None:
    """Save the story generation cache."""
    try:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except (FileNotFoundError, PermissionError) as e:
        raise CacheError(f"Failed to save cache: {e}") from e
    except Exception as e:
        raise CacheError(f"Unexpected error saving cache: {e}") from e

def validate_input(text: str, min_length: int = 1, max_length: Optional[int] = None) -> str:
    """Validate input text."""
    if not text or len(text.strip()) < min_length:
        raise ValidationError(f"Text must be at least {min_length} characters")

    text = text.strip()
    if max_length and len(text) > max_length:
        raise ValidationError(f"Text exceeds maximum length of {max_length} characters")

    return text

def ensure_directory(path: Path) -> None:
    """Ensure directory exists, create if necessary."""
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise InputError(f"Could not create directory {path}: {e}")

def _load_embeddings(embeddings_file: Path) -> dict:
    """Helper function to load embeddings."""
    try:
        with open(embeddings_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise ConfigError(f"Error loading embeddings: {e}")

def load_embeddings(path: Path) -> Dict[str, Any]:
    """Load embeddings from JSON file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid embeddings file format: {e}")
    except Exception as e:
        raise InputError(f"Could not load embeddings from {path}: {e}")

def load_api_key(config: Dict = None, api_key: Optional[str] = None) -> str:
    """Load API key from config, secrets file or command line."""
    if api_key:
        return api_key

    if config is None:
        config = get_config()

    secrets_path = Path(config['secrets']['api_key_file'])
    if not secrets_path.is_absolute():
        secrets_path = Path(__file__).parent.parent / secrets_path

    try:
        with open(secrets_path, 'r') as f:
            secrets = yaml.safe_load(f)
            return secrets['api_key']
    except Exception as e:
        raise APIKeyError(f"Error loading API key: {e}") from e

def resolve_data_path(data_path: str) -> Path:
    """Resolves the absolute path to a data file."""
    path = Path(data_path)
    if not path.is_absolute():
        # Resolve relative to project root
        return Path(__file__).parent.parent / path
    return path

def resolve_config_path(config_path: Union[str, Path]) -> Path:
    """Resolve config path to absolute Path object."""
    config_path = Path(config_path)
    if not config_path.is_absolute():
        config_path = Path(__file__).parent.parent / config_path  # Updated
    if not config_path.exists():
        raise ConfigError(f"Config file not found: {config_path}")
    return config_path

def _override_config(config: dict, temperature: Optional[float], max_tokens: Optional[int],
                     max_iterations: Optional[int], min_quality: Optional[float]) -> None:
    """Helper function to override config values."""
    if temperature is not None:
        config['generation']['temperature'] = temperature
    if max_tokens is not None:
        config['generation']['max_tokens'] = max_tokens
    if max_iterations is not None:
        config['evaluation']['max_iterations'] = max_iterations
    if min_quality is not None:
        config['evaluation']['min_quality_score'] = min_quality

def _display_story_output(result: Dict[str, Any], output_file: Optional[Path]) -> None:
    """Helper function to display or save story output."""
    story = result['text']
    if output_file:
        with open(output_file, 'w') as f:
            f.write(story)
        console.print(f"[green]✓[/green] Story saved to {output_file}")
    else:
        console.print(format_story_output(story))

class StoryGenerator:
    def __init__(self, model: genai.GenerativeModel, character_profiles: Dict[str, Any], world_details: Dict[str, Any]):
        """Initialize story generator with character profiles, and world details."""
        logger.info("Initializing StoryGenerator")
        self.model = model
        self.character_profiles = character_profiles
        self.world_details = world_details

    def semantic_search(self, query: str, embeddings_dict: Dict[str, Any], top_n: int = 3) -> List[Tuple[str, int, float]]:
        return semantic_search(self.model, query, embeddings_dict, top_n)

    def prepare_context(self, embeddings_dict: Dict[str, Any], relevant_chunks: List[Tuple[str, int, float]]) -> str:
        return prepare_context(embeddings_dict, relevant_chunks)

    def _create_prompt(self, style: str, character: str, situation: str, context: str,
                       previous_attempt: str = None, feedback: Dict[str, Any] = None, style_prompt: str = None) -> str:
        return create_prompt(style, character, situation, context, self.character_profiles, self.world_details, previous_attempt, feedback, style_prompt)

    def generate_chapter(self, queries: List[str], embeddings_dict: Dict[str, Any],
                         style: str = "dark fantasy", character: Optional[str] = None,
                         situation: Optional[str] = None, top_n: int = 3,
                         style_prompt: str = None, plot_outline: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a chapter using multiple queries and optional plot outline.

        The semantic search retrieves the top_n most relevant chunks for each query.
        These chunks are then deduplicated to avoid redundancy. The intention is to
        gather potentially relevant information based on different aspects of the
        current goal (represented by the queries). The final list of relevant chunks
        used for context might be less than the initial sum of top_n per query due to
        deduplication.
        """
        all_relevant_chunks = []
        for query in queries:
            relevant_chunks = self.semantic_search(
                query, embeddings_dict, top_n)
            all_relevant_chunks.extend(relevant_chunks)

        # Deduplicate chunks based on file path and chunk index
        unique_chunks = {(file_path, chunk_idx): (file_path, chunk_idx, similarity)
                         for file_path, chunk_idx, similarity in all_relevant_chunks}
        all_relevant_chunks = list(unique_chunks.values())

        # Sort by similarity after deduplication
        all_relevant_chunks.sort(key=lambda x: x[2], reverse=True)

        # Limit to top_n unique chunks based on highest similarity.
        # This ensures that even after considering multiple queries, the context
        # is limited to the most relevant pieces of information.
        all_relevant_chunks = all_relevant_chunks[:top_n]

        context = self.prepare_context(embeddings_dict, all_relevant_chunks)

        # Add plot outline to prompt if provided
        if plot_outline:
            prompt = f"Plot Outline:\n{plot_outline}\n\n"
            prompt += self._create_prompt(style, character,
                                          situation, context, style_prompt=style_prompt)
        else:
            prompt = self._create_prompt(
                style, character, situation, context, style_prompt=style_prompt)

        logger.info("Generating initial draft...")
        response = self.model.generate_content(prompt)
        if not response.text:
            logger.warning("Empty response from the language model.")
            return None

        logger.info("Story generation complete.")
        return {
            'text': response.text,
            'prompt': prompt
        }

    def save_session(self, session_data: Dict[str, Any], filename: str = None):
        save_session(session_data, filename)

    def load_session(self, filename: str) -> Dict[str, Any]:
        return load_session(filename)

    def export_story(self, text: str, format: str = "txt", filename: str = None):
        export_story(text, format, filename)

def generate_story(
    query: str,
    embeddings_file: Path,
    output_file: Optional[Path],
    config_path: str,
    style: str,
    character: Optional[str],
    situation: Optional[str],
    top_n: int,
    temperature: Optional[float],
    max_tokens: Optional[int],
    max_iterations: Optional[int],
    min_quality: Optional[float],
    api_key: Optional[str],
    log_level: str,
    force: bool
) -> None:
    """Generate a story chapter using embeddings."""
    setup_logging(log_level)

    logger = logging.getLogger('generate_story')
    logger.info("Starting story generation")

    try:
        # Load configuration
        config = load_config(config_path)
    except ConfigError as e:
        console.print(f"[bold red]{e}[/bold red]")
        return

    try:
        api_key = load_api_key(config, api_key)
        genai.configure(api_key=api_key)
    except APIKeyError as e:
        console.print(f"[bold red]{e}[/bold red]")
        return

    try:
        _override_config(config, temperature, max_tokens, max_iterations, min_quality)

        generation_config = {
            "temperature": config['generation']['temperature'],
            "top_p": config['generation']['top_p'],
            "max_output_tokens": config['generation']['max_tokens']
        }

        model = genai.GenerativeModel(
            model_name=config['generation']['model'],
            generation_config=generation_config
        )

        embeddings_dict = _load_embeddings(embeddings_file)
        if not embeddings_dict:
            raise FileNotFoundError(f"Embeddings file not found or empty at {embeddings_file}")

        character_profiles = load_character_profiles(config['paths']['character_profiles'])
        world_details = load_world_details(config['paths']['world_details'])

        story_gen = StoryGenerator(model, character_profiles, world_details)

        cache_path = Path(config['paths']['cache_file'])
        story_cache = load_story_cache(cache_path)
        cache_params = {
            'query': query,
            'style': style,
            'character': character,
            'situation': situation,
            'top_n': top_n,
            'temperature': config['generation']['temperature'],
            'max_tokens': config['generation']['max_tokens']
        }
        cache_key = compute_cache_key(cache_params)

        if cache_key in story_cache and not force:
            console.print("[bold blue]Using cached story...[/bold blue] (use --force to regenerate)")
            result = story_cache[cache_key]
            _display_story_output(result, output_file)
            return

        best_story = None
        best_quality = -1
        metrics_history = []

        with create_progress() as progress:
            task = progress.add_task("Generating story...", total=config['evaluation']['max_iterations'])
            for i in range(config['evaluation']['max_iterations']):
                progress.update(task, advance=1, description=f"Generating story iteration {i + 1}...")
                result = story_gen.generate_chapter(
                    queries=[query],
                    embeddings_dict=embeddings_dict,
                    style=style,
                    character=character,
                    situation=situation,
                    top_n=top_n
                )

                if result:
                    metrics = evaluate_story(result['text'], embeddings_dict, top_n, config['evaluation']['rouge_threshold'])
                    metrics_history.append(metrics)

                    if metrics['quality_score'] > best_quality:
                        best_quality = metrics['quality_score']
                        best_story = result

                    if best_quality >= config['evaluation']['min_quality_score']:
                        progress.update(task, description="[bold green]Minimum quality achieved![/bold green]")
                        break

        if best_story:
            story_cache[cache_key] = best_story
            save_story_cache(story_cache, cache_path)
            _display_story_output(best_story, output_file)

            if metrics_history:
                metrics_table = create_metrics_table(metrics_history[-1])
                console.print(metrics_table)
        else:
            console.print("[bold red]Story generation failed. No acceptable story found.[/bold red]")

    except Exception as e:
        logger.exception("An error occurred during story generation")
        console.print(f"[bold red]An error occurred: {e}[/bold red]")
        raise