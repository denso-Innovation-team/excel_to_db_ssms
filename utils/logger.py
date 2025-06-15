"""
utils/logger.py
Logging Configuration
"""

import logging
import logging.handlers
from pathlib import Path


def setup_logger(
    name: str = "denso888", level: str = "INFO", log_file: str = None
) -> logging.Logger:
    """Setup application logger"""
    logger = logging.getLogger(name)

    # Clear existing handlers
    logger.handlers.clear()

    # Set level
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    if log_file:
        # Ensure log directory exists
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # Rotating file handler
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"  # 10MB
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str = "denso888") -> logging.Logger:
    """Get existing logger"""
    return logging.getLogger(name)
