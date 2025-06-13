import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


def main():
    """Main application entry point"""
    try:
        # Check environment first
        import check_env

        check_env.main()

        # Import and start application
        from gui.main_window import DENSO888MainWindow

        app = DENSO888MainWindow()
        app.run()

    except Exception as e:
        logger.error(f"Fatal error occurred: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
