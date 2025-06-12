"""
utils/logger.py
GUI-integrated logging system for DENSO888
"""

import logging
import sys
from pathlib import Path
from typing import Optional, Callable
from datetime import datetime


class GUILogHandler(logging.Handler):
    """Custom log handler that sends logs to GUI"""

    def __init__(self, gui_callback: Optional[Callable] = None):
        super().__init__()
        self.gui_callback = gui_callback

    def emit(self, record):
        """Emit log record to GUI"""
        if self.gui_callback:
            try:
                log_entry = self.format(record)
                self.gui_callback(log_entry, record.levelname.lower())
            except Exception:
                pass  # Don't let logging errors crash the app


def setup_gui_logger(gui_callback: Optional[Callable] = None) -> logging.Logger:
    """Setup logging with GUI integration"""

    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Clear existing handlers
    root_logger.handlers.clear()

    # File handler
    file_handler = logging.FileHandler(
        logs_dir / "denso888.log", encoding="utf-8", mode="a"
    )
    file_handler.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # GUI handler (if callback provided)
    gui_handler = None
    if gui_callback:
        gui_handler = GUILogHandler(gui_callback)
        gui_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    if gui_handler:
        gui_handler.setFormatter(formatter)

    # Add handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    if gui_handler:
        root_logger.addHandler(gui_handler)

    # Set specific logger levels
    logging.getLogger("Pillow").setLevel(logging.WARNING)
    logging.getLogger("matplotlib").setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)
    logger.info("DENSO888 logging system initialized")

    return root_logger


def get_logger(name: str) -> logging.Logger:
    """Get logger instance"""
    return logging.getLogger(name)
