# Narr_ai_tive/app/main.py
from .tui import main_menu
from .setup_logging import setup_logging  # Import the function directly from the module

def main():
    """Main function to run the TUI application."""
    setup_logging()  # Now this will work as expected
    main_menu()

if __name__ == "__main__":
    main()
