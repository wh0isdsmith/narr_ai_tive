# Installation Guide

## Critical Prerequisites

### 1. Document Embeddings
Before installation, you **must** have:
- Generated document embeddings using sentence-transformers
- Placed them in `data/embeddings.json`
- See [Embeddings Setup Guide](embeddings_setup.md) for details

### 2. System Requirements
- Python 3.8+
- [Hatchling](https://hatch.pypa.io/latest/)
- Google API key (Gemini access)
- 16GB RAM recommended
- 2GB free disk space

### 3. Required Files
Ensure these files exist:
```
data/
├── embeddings.json           # Required before first run
├── character_profiles.json   # Can be empty, but must exist
└── world_details.json       # Can be empty, but must exist
```

## Installation Steps

1. **Clone the repository**

    ```bash
    git clone https://github.com/yourusername/Narr_ai_tive.git
    cd Narr_ai_tive
    ```

2. **Create a virtual environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    # OR
    venv\Scripts\activate     # Windows
    ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Setup configuration**

    ```bash
    cp config.yaml.example config.yaml
    # Add your API key to secrets.yaml
    ```

5. **Install Hatch**

    ```bash
    pip install hatch
    ```

6. **Enter Hatch shell**

    ```bash
    hatch shell
    ```

You are now ready to use Narr_ai_tive!
