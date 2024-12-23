# `utils.py` Documentation

This module provides various utility functions and classes to support the story generation process. It includes functions for configuration loading, progress tracking, quality metrics calculation, and more.

## Functions

### `load_config(config_path: str = 'config.yaml') -> Dict[str, Any]`

Loads the configuration from the specified YAML file.

#### Parameters

- `config_path` (str): The path to the configuration file. Default is 'config.yaml'.

#### Returns

- `Dict[str, Any]`: The loaded configuration.

#### Usage

```python
config = load_config()
```

### `get_config() -> Dict[str, Any]`

Returns the loaded configuration.

#### Returns

- `Dict[str, Any]`: The loaded configuration.

#### Usage

```python
config = get_config()
```

### `create_progress() -> Progress`

Creates a rich progress bar with custom formatting.

#### Returns

- `Progress`: The created progress bar.

#### Usage

```python
progress = create_progress()
```

### `calculate_quality_score(text: str) -> float`

Calculates a basic quality score for the given text based on its length.

#### Parameters

- `text` (str): The text to evaluate.

#### Returns

- `float`: The calculated quality score.

#### Usage

```python
score = calculate_quality_score("This is a sample text.")
```

### `calculate_rouge_scores(text: str, embeddings_dict: Dict, top_n: int) -> Dict[str, float]`

Calculates ROUGE scores against the top_n relevant chunks.

#### Parameters

- `text` (str): The generated text.
- `embeddings_dict` (Dict): A dictionary containing embeddings.
- `top_n` (int): The number of top relevant chunks to consider.

#### Returns

- `Dict[str, float]`: The calculated ROUGE scores.

#### Usage

```python
rouge_scores = calculate_rouge_scores("This is a sample text.", embeddings_dict, top_n=3)
```

### `calculate_semantic_similarity(text: str, embeddings_dict: Dict) -> float`

Calculates average semantic similarity to relevant chunks using Sentence Transformers.

#### Parameters

- `text` (str): The generated text.
- `embeddings_dict` (Dict): A dictionary containing embeddings.

#### Returns

- `float`: The calculated semantic similarity.

#### Usage

```python
similarity = calculate_semantic_similarity("This is a sample text.", embeddings_dict)
```

### `calculate_lexical_diversity(text: str) -> float`

Calculates the lexical diversity of the text.

#### Parameters

- `text` (str): The text to evaluate.

#### Returns

- `float`: The calculated lexical diversity.

#### Usage

```python
diversity = calculate_lexical_diversity("This is a sample text.")
```

### `evaluate_story(text: str, embeddings_dict: Dict[str, Any], top_n: int, rouge_threshold: float) -> Dict[str, Any]`

Evaluates the generated story based on various metrics.

#### Parameters

- `text` (str): The generated story text.
- `embeddings_dict` (Dict[str, Any]): A dictionary containing embeddings.
- `top_n` (int): The number of top relevant chunks to consider.
- `rouge_threshold` (float): The threshold for ROUGE scores.

#### Returns

- `Dict[str, Any]`: The evaluation metrics.

#### Usage

```python
metrics = evaluate_story("This is a sample story.", embeddings_dict, top_n=3, rouge_threshold=0.5)
```

### `create_metrics_table(metrics: Dict[str, float]) -> Table`

Creates a rich table for displaying evaluation metrics.

#### Parameters

- `metrics` (Dict[str, float]): The evaluation metrics.

#### Returns

- `Table`: The created table.

#### Usage

```python
table = create_metrics_table(metrics)
```

### `format_story_output(text: str, title: Optional[str] = None) -> Panel`

Formats story text with enhanced rich formatting.

#### Parameters

- `text` (str): The story text.
- `title` (Optional[str]): The title of the panel.

#### Returns

- `Panel`: The formatted panel.

#### Usage

```python
panel = format_story_output("This is a sample story.", title="Sample Story")
```

### `compute_cache_key(params: Dict[str, Any]) -> str`

Generates a cache key from parameters.

#### Parameters

- `params` (Dict[str, Any]): The parameters to generate the cache key from.

#### Returns

- `str`: The generated cache key.

#### Usage

```python
cache_key = compute_cache_key({"param1": "value1", "param2": "value2"})
```

### `load_story_cache(cache_path: Path) -> Dict[str, Any]`

Loads the story generation cache.

#### Parameters

- `cache_path` (Path): The path to the cache file.

#### Returns

- `Dict[str, Any]`: The loaded cache.

#### Usage

```python
cache = load_story_cache(Path("cache.json"))
```

### `save_story_cache(cache: Dict[str, Any], cache_path: Path) -> None`

Saves the story generation cache.

#### Parameters

- `cache` (Dict[str, Any]): The cache to save.
- `cache_path` (Path): The path to the cache file.

#### Usage

```python
save_story_cache(cache, Path("cache.json"))
```

### `validate_input(text: str, min_length: int = 1, max_length: Optional[int] = None) -> str`

Validates input text.

#### Parameters

- `text` (str): The text to validate.
- `min_length` (int): The minimum length of the text. Default is 1.
- `max_length` (Optional[int]): The maximum length of the text.

#### Returns

- `str`: The validated text.

#### Usage

```python
validated_text = validate_input("This is a sample text.", min_length=10, max_length=100)
```

### `ensure_directory(path: Path) -> None`

Ensures the directory exists, creates it if necessary.

#### Parameters

- `path` (Path): The path to the directory.

#### Usage

```python
ensure_directory(Path("output"))
```

### `_load_embeddings(embeddings_file: Path) -> dict`

Helper function to load embeddings.

#### Parameters

- `embeddings_file` (Path): The path to the embeddings file.

#### Returns

- `dict`: The loaded embeddings.

#### Usage

```python
embeddings = _load_embeddings(Path("embeddings.json"))
```

### `load_embeddings(path: Path) -> Dict[str, Any]`

Loads embeddings from a JSON file.

#### Parameters

- `path` (Path): The path to the embeddings file.

#### Returns

- `Dict[str, Any]`: The loaded embeddings.

#### Usage

```python
embeddings = load_embeddings(Path("embeddings.json"))
```

### `load_api_key(config: Dict = None, api_key: Optional[str] = None) -> str`

Loads the API key from config, secrets file, or command line.

#### Parameters

- `config` (Dict, optional): The configuration dictionary.
- `api_key` (Optional[str]): The API key.

#### Returns

- `str`: The loaded API key.

#### Usage

```python
api_key = load_api_key(config)
```

## Dependencies

- `logging`: For logging messages and errors.
- `typing`: For type hints.
- `pathlib`: For handling file paths.
- `hashlib`: For generating hash values.
- `json`: For handling JSON data.
- `yaml`: For handling YAML data.
- `google.generativeai`: For the generative model.
- `rich.console.Console`: For creating a rich console interface.
- `rich.progress.Progress`: For creating progress bars.
- `rich.table.Table`: For displaying tables in the console.
- `rich.text.Text`: For creating rich text.
- `rich.panel.Panel`: For displaying panels in the console.
- `rouge`: For calculating ROUGE scores.
- `sklearn.metrics.pairwise`: For calculating cosine similarity.
- `sentence_transformers`: For generating text embeddings.

## Example Usage

To use the utility functions, simply import them and call them in your script:

```python
from utils import load_config, create_progress, calculate_quality_score

config = load_config()
progress = create_progress()
score = calculate_quality_score("This is a sample text.")
```

## Error Handling

The functions include error handling to catch and log any exceptions that occur during their execution. Errors are logged using the `logging` module.

## Conclusion

The `utils.py` module provides a comprehensive set of utility functions to support the story generation process. By leveraging various libraries and tools, it ensures efficient and effective handling of configuration, progress tracking, quality metrics calculation, and more.
