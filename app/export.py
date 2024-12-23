import logging
from typing import Optional
from pathlib import Path
from datetime import datetime
import markdown

# Set up a logger for this module.
logger = logging.getLogger('export')
logger.info("Export module initialized")


def export_story(text: str, format: str = "txt", filename: Optional[str] = None):
    """Exports the story in the specified format.

    Args:
        text: The story text to export.
        format: The format to export the story in (txt, md, or html).
        filename: The name of the file to export the story to. If None, a timestamped filename is generated.
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"story_{timestamp}.{format}"

    filepath = Path(__file__).parent / filename

    try:
        with open(filepath, 'w') as f:
            if format == "txt":
                f.write(text)
            elif format == "md":
                f.write(markdown.markdown(text))
            elif format == "html":
                f.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Story Export</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 20px;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #0056b3;
        }}
        p {{
            margin-bottom: 1em;
        }}
    </style>
</head>
<body>
    {markdown.markdown(text)}
</body>
</html>
                """)
            else:
                logger.error(f"Unsupported format: {format}")
                return
        logger.info(f"Story exported to {filename} in {format} format")
    except Exception as e:
        logger.error(f"Error exporting story to {filename}: {e}")
