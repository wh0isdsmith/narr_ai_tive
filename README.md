# Narr_AI_tive 🤖📚

[![Visual Studio](https://custom-icon-badges.demolab.com/badge/Visual%20Studio-5C2D91.svg?&logo=visual-studio&logoColor=white)](#)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-886FBF?logo=googlegemini&logoColor=fff)](#)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?logo=huggingface&logoColor=000)](#)
[![GitHub Copilot](https://img.shields.io/badge/GitHub%20Copilot-000?logo=githubcopilot&logoColor=fff)](#)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#)
[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 🚀 A next-generation AI story generator powered by Google's Gemini model

## 📖 Overview

**Narr_ai_tive** is an advanced AI-powered story generator that leverages Google's Gemini model to create rich, engaging narratives. Here is a detailed overview of its features and functionalities:

## 📚 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
  - [Advanced Story Generation](#-advanced-story-generation)
  - [Smart Content Management](#-smart-content-management)
  - [Quality Metrics](#-quality-metrics)
  - [Multiple Interfaces](#-multiple-interfaces)
- [Quick Start](#-quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#-usage)
  - [Interactive TUI](#interactive-tui)
  - [CLI Generation](#cli-generation)
  - [Python API](#python-api)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [License](#-license)
- [Show Your Support](#-show-your-support)

### Key Features

1. **Advanced Story Generation**
   - **Gemini-Powered Generation**: Utilizes Google's cutting-edge language model for generating high-quality stories.
   - **Multiple Story Styles**: Supports various storytelling styles such as dark fantasy, sci-fi, mystery, and more.
   - **Character Integration**: Ensures deep character development and consistency throughout the story.
   - **World Building**: Provides rich details about the story's environment and settings.
   - **Plot Management**: Tracks context and story progression intelligently.

2. **Smart Content Management**
   - **Semantic Search**: Uses advanced embeddings to find relevant context for the story.
   - **Auto-Chunking**: Organizes content intelligently into manageable chunks.
   - **Caching System**: Efficiently generates stories with smart caching to avoid redundant computations.
   - **Character Profiles**: Manages detailed character profiles to maintain consistency.
   - **World Details**: Comprehensive system for managing world-building elements.

3. **Quality Metrics**
   - **Multi-Metric Evaluation**: Evaluates generated content using metrics like ROUGE, BLEU, and semantic similarity.
   - **Lexical Analysis**: Checks vocabulary richness and diversity.
   - **Iterative Improvement**: Regenerates content based on quality metrics to improve the story.
   - **Configurable Thresholds**: Allows customization of quality standards.

4. **Multiple Interfaces**
   - **Rich TUI**: Provides a beautiful terminal interface with progress tracking.
   - **CLI Support**: Supports command-line automation for generating stories.
   - **Interactive Mode**: Offers dynamic story development through an interactive loop.
   - **Export Options**: Supports multiple output formats including TXT, MD, and HTML.

### Summary

**Narr_ai_tive** is a comprehensive AI story generation tool that combines advanced language models, rich character and world-building details, and multiple interfaces to create engaging and high-quality narratives.

## ✨ Features

### 🧠 Advanced Story Generation
- 🤖 **Gemini-Powered Generation** - Leverage Google's cutting-edge language model
- 🎭 **Multiple Story Styles** - From dark fantasy to sci-fi and beyond
- 👥 **Character Integration** - Deep character development and consistency
- 🌍 **World Building** - Rich world details and environment descriptions
- 📚 **Plot Management** - Smart context tracking and story progression

### 🔍 Smart Content Management
- 🧮 **Semantic Search** - Find relevant context using advanced embeddings
- 📝 **Auto-Chunking** - Intelligent content organization
- 💾 **Caching System** - Efficient generation with smart caching
- 🎭 **Character Profiles** - Detailed character management
- 🌟 **World Details** - Comprehensive world-building system

### 📊 Quality Metrics
- 📈 **Multi-Metric Evaluation** - ROUGE, BLEU, semantic similarity
- 📚 **Lexical Analysis** - Vocabulary richness and diversity checks
- 🔄 **Iterative Improvement** - Quality-based regeneration
- ⚖️ **Configurable Thresholds** - Customizable quality standards

### 🖥️ Multiple Interfaces
- 🎨 **Rich TUI** - Beautiful terminal interface with progress tracking
- ⌨️ **CLI Support** - Command-line automation capabilities
- 📱 **Interactive Mode** - Dynamic story development
- 📝 **Export Options** - Multiple output formats (TXT, MD, HTML)

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- [Hatchling](https://hatch.pypa.io/latest/)
- Google API key (Gemini access)

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/Narr_ai_tive.git
cd Narr_ai_tive

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Setup configuration
cp config.yaml.example config.yaml
# Add your API key to secrets.yaml
```

## 💻 Usage

### Interactive TUI
```bash
python -m app.main
```

### CLI Generation
```bash
# Generate a single chapter
narr_ai_tive generate --query "A mystical journey begins" --style "epic fantasy"

# Generate with character focus
narr_ai_tive generate --input story.txt --character "Elena" --situation "dark forest"
```

### Python API
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

## 🎯 Project Structure

```
📦 Narr_ai_tive
 ┣ 📂 app
 ┃ ┣ 📜 chapter.py      # Chapter generation
 ┃ ┣ 📜 character.py    # Character management
 ┃ ┣ 📜 context.py      # Context handling
 ┃ ┣ 📜 export.py       # Story export functionality
 ┃ ┣ 📜 interactive.py  # Interactive story mode
 ┃ ┣ 📜 main.py        # Application entry point
 ┃ ┣ 📜 path_utils.py   # Path resolution utilities
 ┃ ┣ 📜 plot.py         # Plot management
 ┃ ┣ 📜 prompt.py       # Prompt engineering
 ┃ ┣ 📜 semantic_search.py  # Content search
 ┃ ┣ 📜 session.py      # Session management
 ┃ ┣ 📜 setup_logging.py # Logging configuration
 ┃ ┣ 📜 story.py        # Story generation core
 ┃ ┣ 📜 text_processing.py # Text processing utilities
 ┃ ┣ 📜 tui.py          # Terminal user interface
 ┃ ┣ 📜 utils.py        # Utility functions
 ┃ ┗ 📜 world.py        # World-building management
 ┣ 📂 data
 ┃ ┣ 📜 character_profiles.json
 ┃ ┣ 📜 embeddings.json
 ┃ ┗ 📜 world_details.json
 ┣ 📜 config.yaml       # Configuration
 ┗ 📜 secrets.yaml      # API keys
```

## 🛠️ Configuration

```yaml
api:
  batch_size: 10
  rate_limit: 10
embedding:
  chunk_size: 5000
  model: models/embedding-001
generation:
  temperature: 0.7
  model: models/gemini-exp-1206
```

## 📝 License

MIT License - feel free to use in your own projects!

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

---
Made with ❤️ using Google's Gemini