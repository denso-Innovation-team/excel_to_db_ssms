"""Enhanced GUI-integrated logging system for DENSO888"""

import logging
import sys
from pathlib import Path
from typing import Optional, Callable, Dict, Any
from datetime import datetime
import threading
import queue


class GUILogHandler(logging.Handler):
    """Thread-safe log handler for GUI integration"""

    def __init__(self, gui_callback: Optional[Callable] = None):
        super().__init__()
        self.gui_callback = gui_callback
        self.log_queue = queue.Queue()
        self._thread_lock = threading.Lock()

    def emit(self, record):
        """Thread-safe log emission"""
        if self.gui_callback:
            try:
                log_entry = self.format(record)
                self.log_queue.put((log_entry, record.levelname.lower(), record.created))

                with self._thread_lock:
                    self.gui_callback(log_entry, record.levelname.lower())
            except Exception:
                pass


class ColoredConsoleHandler(logging.StreamHandler):
    """Console handler with color support"""

    COLORS = {
        "DEBUG": "\033[36m", "INFO": "\033[32m", "WARNING": "\033[33m",
        "ERROR": "\033[31m", "CRITICAL": "\033[35m", "RESET": "\033[0m"
    }

    def emit(self, record):
        try:
            if sys.platform != "win32":
                level_color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
                record.levelname = f"{level_color}{record.levelname}{self.COLORS['RESET']}"
            super().emit(record)
        except Exception:
            super().emit(record)


def setup_gui_logger(gui_callback: Optional[Callable] = None) -> logging.Logger:
    """Setup comprehensive logging with GUI integration"""
    
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.handlers.clear()

    # File handler
    try:
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(
            logs_dir / "denso888.log", maxBytes=10*1024*1024, backupCount=5, encoding="utf-8"
        )
    except ImportError:
        file_handler = logging.FileHandler(logs_dir / "denso888.log", encoding="utf-8", mode="a")

    file_handler.setLevel(logging.INFO)

    # Console handler
    console_handler = ColoredConsoleHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # GUI handler
    gui_handler = None
    if gui_callback:
        gui_handler = GUILogHandler(gui_callback)
        gui_handler.setLevel(logging.INFO)

    # Formatters
    detailed_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    simple_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S")

    file_handler.setFormatter(detailed_formatter)
    console_handler.setFormatter(simple_formatter)
    if gui_handler:
        gui_handler.setFormatter(simple_formatter)

    # Add handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    if gui_handler:
        root_logger.addHandler(gui_handler)

    # Configure specific loggers
    for logger_name in ["PIL", "matplotlib", "urllib3", "sqlalchemy.engine"]:
        logging.getLogger(logger_name).setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)
    logger.info("DENSO888 logging system initialized")
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """Get logger instance"""
    return logging.getLogger(name)


class PerformanceLogger:
    """Simple performance logger without psutil"""

    def __init__(self):
        self.logger = get_logger("performance")
        self.metrics = {}

    def start_timer(self, operation: str):
        """Start timing an operation"""
        self.metrics[operation] = {"start_time": datetime.now(), "end_time": None, "duration": None}

    def end_timer(self, operation: str):
        """End timing and log duration"""
        if operation in self.metrics:
            self.metrics[operation]["end_time"] = datetime.now()
            duration = (self.metrics[operation]["end_time"] - self.metrics[operation]["start_time"]).total_seconds()
            self.metrics[operation]["duration"] = duration
            self.logger.info(f"Operation '{operation}' completed in {duration:.2f} seconds")
            return duration
        return None


class LoggedOperation:
    """Context manager for automatic operation logging"""

    def __init__(self, operation_name: str, logger: Optional[logging.Logger] = None):
        self.operation_name = operation_name
        self.logger = logger or get_logger("operations")
        self.start_time = None

    def __enter__(self):
        self.start_time = datetime.now()
        self.logger.info(f"Starting operation: {self.operation_name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (datetime.now() - self.start_time).total_seconds()
        if exc_type is None:
            self.logger.info(f"Operation '{self.operation_name}' completed in {duration:.2f}s")
        else:
            self.logger.error(f"Operation '{self.operation_name}' failed after {duration:.2f}s: {exc_val}")
        return False


def log_system_info():
    """Log basic system information"""
    logger = get_logger("system")
    try:
        import platform
        logger.info(f"Python: {sys.version}")
        logger.info(f"Platform: {platform.platform()}")
        logger.info(f"Architecture: {platform.architecture()}")
    except Exception as e:
        logger.warning(f"Could not gather system info: {e}")


def setup_error_logging():
    """Setup error logging"""
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger = get_logger("exceptions")
        logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    sys.excepthook = handle_exception


# Initialize instances
performance_logger = PerformanceLogger()
