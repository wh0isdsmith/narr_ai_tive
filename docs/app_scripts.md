# App Scripts Documentation

## Overview

The Narr_ai_tive application is organized into specialized modules that handle different aspects of story generation. Each module is designed with specific responsibilities and integrates with others to create a cohesive story generation system.

---

## Module Summaries

### `chapter.py` - Story Chapter Generation

**Purpose**: Handles the generation and management of individual story chapters with quality control and caching.

**Key Features**:
- Smart caching system to avoid regenerating similar content
- Quality metrics validation for generated text
- Progressive enhancement of weak sections
- Character voice consistency checking
- Length and pacing control

**Integration Points**:
- Works with `prompt.py` for input preparation
- Uses `character.py` for character consistency
- Interfaces with `context.py` for story continuity

```python
class ChapterGenerator:
    def __init__(self, model: GeminiModel, config: Config):
        self.model = model
        self.config = config
        self.cache = ChapterCache()
        
    def generate_chapter(
        self,
        query: str,
        style: str,
        character: str,
        length: int = 1000
    ) -> str:
        """
        Generate a story chapter with caching and validation.
        
        Example:
            generator = ChapterGenerator(model, config)
            chapter = generator.generate_chapter(
                query="A detective finds a mysterious package",
                style="noir",
                character="Mike Stone",
                length=2000
            )
        """
        # Check cache first
        cache_key = self._generate_cache_key(query, style, character)
        if cached := self.cache.get(cache_key):
            return cached
            
        # Generate fresh content
        prompt = self._build_prompt(query, style, character)
        content = self.model.generate(prompt, max_length=length)
        
        # Validate and enhance
        content = self._validate_chapter(content)
        content = self._enhance_quality(content)
        
        # Cache result
        self.cache.set(cache_key, content)
        return content
        
    def _validate_chapter(self, content: str) -> str:
        """Ensure chapter meets quality standards"""
        metrics = QualityMetrics(content)
        if not metrics.meets_standards():
            content = self._regenerate_weak_sections(content)
        return content
```

---

### `character.py` - Character Management System

**Purpose**: Manages the creation, evolution, and interaction of story characters with complex personality systems.

**Key Features**:
- Dynamic personality trait system
- Memory management with emotional impact tracking
- Relationship graph management
- Character arc development
- Behavioral consistency enforcement
- Semantic memory search for relevant past events

**Technical Details**:
- Uses embedding-based memory system
- Implements personality drift based on experiences
- Maintains relationship graphs
- Tracks character development arcs

```python
class Character:
    def __init__(
        self,
        name: str,
        personality: Dict[str, float],
        backstory: str
    ):
        self.name = name
        self.personality = personality
        self.backstory = backstory
        self.memory = CharacterMemory()
        self.relationships: Dict[str, Relationship] = {}
        
    def add_memory(self, event: Event):
        """Add event to character's memory with emotional impact"""
        self.memory.add(event)
        self.update_personality(event)
    
    def get_reaction(self, situation: str) -> str:
        """Generate character's reaction based on personality"""
        context = self.memory.get_relevant_context(situation)
        return self._generate_reaction(situation, context)
        
class CharacterMemory:
    def __init__(self):
        self.events: List[Event] = []
        self.embeddings = SemanticIndex()
        
    def add(self, event: Event):
        """Add event with semantic indexing"""
        self.events.append(event)
        self.embeddings.add(event)
        
    def get_relevant_context(self, situation: str) -> List[Event]:
        """Find relevant past events using semantic search"""
        return self.embeddings.search(situation)
```

---

### `context.py` - Story Context Management

**Purpose**: Maintains and manages the story's context, ensuring narrative consistency and coherent progression.

**Key Features**:
- Real-time context tracking
- Semantic relationship mapping
- Timeline management
- Plot point tracking
- World state management

**Integration Points**:
- Powers the story continuity system
- Feeds into character decision making
- Influences plot development

---

### `export.py` - Content Export System

**Purpose**: Handles the export of generated content in various formats with formatting and metadata.

**Supported Formats**:
- Markdown (`.md`)
- Plain text (`.txt`)
- Rich Text Format (`.rtf`)
- HTML with styling (`.html`)
- PDF with formatting (`.pdf`)
- ePub for e-readers (`.epub`)

**Features**:
- Template-based formatting
- Metadata inclusion
- Table of contents generation
- Cross-reference handling
- Asset management

---

### `interactive.py` - Interactive Story Mode

**Purpose**: Manages real-time interaction between users and the story generation system.

**Features**:
- Dynamic story branching
- Real-time user input processing
- Context-aware suggestions
- Story state management
- Session persistence

---

### `main.py` - Application Entry Point

**Purpose**: Coordinates the initialization and operation of all system components.

**Responsibilities**:
- Configuration loading
- Component initialization
- Error handling
- Resource management
- Session coordination

---

### `path_utils.py` - Path Management

**Purpose**: Handles all filesystem operations and path resolutions across different platforms.

**Features**:
- Cross-platform path normalization
- Resource location management
- Asset path resolution
- Temporary file handling
- Cache directory management

---

### `plot.py`

Manages plot development.

#### Functions

- `create_plot_outline(query: str) -> dict`
  - Creates a plot outline based on the given query.
  - **Parameters:**
    - `query` (str): The initial prompt or query for the plot.
  - **Returns:**
    - `dict`: The plot outline.

---

### `prompt.py`

Handles prompt engineering.

#### Functions

- `generate_prompt(query: str) -> str`
  - Generates a prompt based on the given query.
  - **Parameters:**
    - `query` (str): The initial prompt or query.
  - **Returns:**
    - `str`: The generated prompt.

---

### `semantic_search.py`

Handles content search using semantic embeddings.

#### Functions

- `search_content(query: str) -> list`
  - Searches for content relevant to the given query.
  - **Parameters:**
    - `query` (str): The search query.
  - **Returns:**
    - `list`: A list of relevant content.

---

### `session.py`

Manages user sessions.

#### Functions

- `create_session(user_id: str) -> dict`
  - Creates a new session for the user.
  - **Parameters:**
    - `user_id` (str): The user ID.
  - **Returns:**
    - `dict`: The session details.

---

### `setup_logging.py`

Configures logging for the application.

#### Functions

- `setup_logging() -> None`
  - Sets up logging for the application.

---

### `story.py`

The core of story generation.

#### Functions

- `generate_story(query: str, style: str, character: str) -> str`
  - Generates a story based on the given query, style, and character.
  - **Parameters:**
    - `query` (str): The initial prompt or query for the story.
    - `style` (str): The storytelling style (e.g., "mystery", "sci-fi").
    - `character` (str): The main character's name.
  - **Returns:**
    - `str`: The generated story.

---

### `text_processing.py`

Provides text processing utilities.

#### Functions

- `process_text(text: str) -> str`
  - Processes the given text.
  - **Parameters:**
    - `text` (str): The text to process.
  - **Returns:**
    - `str`: The processed text.

---

### `tui.py`

Manages the terminal user interface.

#### Functions

- `start_tui() -> None`
  - Starts the terminal user interface.

---

### `utils.py`

Provides utility functions.

#### Functions

- `load_config() -> dict`
  - Loads the configuration file.
  - **Returns:**
    - `dict`: The configuration.

---

### `world.py`

Manages world-building elements.

#### Functions

- `create_world_detail(name: str, description: str, significance: str) -> dict`
  - Creates a world detail.
  - **Parameters:**
    - `name` (str): The name of the location.
    - `description` (str): A brief description of the location.
    - `significance` (str): The significance of the location in the story.
  - **Returns:**
    - `dict`: The world detail.

---
