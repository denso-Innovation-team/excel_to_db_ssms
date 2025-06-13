"""Simplified logging for DENSO888"""

import logging
from pathlib import Path

def setup_logger(name: str = "denso888") -> logging.Logger:
    """Setup basic logger"""
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Console handler
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    
    # File handler
    file_handler = logging.FileHandler(logs_dir / "denso888.log", encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console)
    logger.addHandler(file_handler)
    
    return logger
