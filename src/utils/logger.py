import logging
import logging.handlers
from pathlib import Path
import sys

def setup_logger(name: str = "excel_to_db") -> logging.Logger:
    """Setup logger with UTF-8 encoding for Windows"""

    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "excel_to_ssms.log"

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # Create formatter (NO EMOJIS for file logging)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    console_formatter = logging.Formatter(
        "%(levelname)s - %(message)s"
    )

    # File handler with UTF-8 encoding
    try:
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, 
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'  # Force UTF-8
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Warning: Could not setup file logging: {e}")

    # Console handler with UTF-8 for Windows
    try:
        console_handler = logging.StreamHandler(sys.stdout)
        
        # Force UTF-8 encoding for Windows console
        if sys.platform == "win32":
            try:
                # Try to set console to UTF-8
                import locale
                console_handler.stream.reconfigure(encoding='utf-8')
            except:
                # Fallback: use basic formatter without emojis
                pass
        
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    except Exception as e:
        print(f"Warning: Console logging issue: {e}")

    return logger
