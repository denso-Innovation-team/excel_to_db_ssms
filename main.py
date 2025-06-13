#!/usr/bin/env python3
"""
DENSO888 - Excel to SQL GUI Application
Optimized entry point with minimal resource usage
"""

import sys
import os
import logging
from pathlib import Path

# Setup minimal logging
logging.basicConfig(
    level=logging.ERROR,  # Only errors during startup
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log", encoding="utf-8")],
)


def check_environment():
    """Quick environment validation"""
    try:
        import tkinter

        root = tkinter.Tk()
        root.withdraw()
        root.destroy()
        return True
    except Exception as e:
        print(f"❌ GUI Environment Error: {e}")
        return False


def main():
    """Streamlined application entry"""
    try:
        if not check_environment():
            input("Press Enter to exit...")
            return

        from gui.main_window import DENSO888MainWindow

        app = DENSO888MainWindow()
        app.run()

    except ImportError as e:
        print(f"❌ Missing Dependencies: {e}")
        print("Run: pip install -r requirements.txt")
        input("Press Enter to exit...")
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        print(f"❌ Application Error: {e}")
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
