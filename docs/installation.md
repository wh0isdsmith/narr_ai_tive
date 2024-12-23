# Installation Guide

## Prerequisites

- Python 3.8+
- [Hatchling](https://hatch.pypa.io/latest/)
- Google API key (Gemini access)

## Steps

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
