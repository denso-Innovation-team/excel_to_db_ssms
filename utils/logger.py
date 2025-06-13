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
                # Use queue for thread safety
                self.log_queue.put(
                    (log_entry, record.levelname.lower(), record.created)
                )

                # Call GUI callback in thread-safe manner
                with self._thread_lock:
                    self.gui_callback(log_entry, record.levelname.lower())
            except Exception:
                pass  # Don't let logging errors crash the app

    def get_queued_logs(self):
        """Get all queued log entries"""
        logs = []
        while not self.log_queue.empty():
            try:
                logs.append(self.log_queue.get_nowait())
            except queue.Empty:
                break
        return logs


class ColoredConsoleHandler(logging.StreamHandler):
    """Console handler with color support"""

    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
        "RESET": "\033[0m",  # Reset
    }

    def emit(self, record):
        try:
            if sys.platform != "win32":  # Color support for non-Windows
                level_color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
                record.levelname = (
                    f"{level_color}{record.levelname}{self.COLORS['RESET']}"
                )
            super().emit(record)
        except Exception:
            super().emit(record)


def setup_gui_logger(gui_callback: Optional[Callable] = None) -> logging.Logger:
    """Setup comprehensive logging with GUI integration"""

    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Clear existing handlers
    root_logger.handlers.clear()

    # File handler with rotation
    try:
        from logging.handlers import RotatingFileHandler

        file_handler = RotatingFileHandler(
            logs_dir / "denso888.log",
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding="utf-8",
        )
    except ImportError:
        # Fallback to basic file handler
        file_handler = logging.FileHandler(
            logs_dir / "denso888.log", encoding="utf-8", mode="a"
        )

    file_handler.setLevel(logging.INFO)

    # Console handler with colors
    console_handler = ColoredConsoleHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # GUI handler (if callback provided)
    gui_handler = None
    if gui_callback:
        gui_handler = GUILogHandler(gui_callback)
        gui_handler.setLevel(logging.INFO)

    # Enhanced formatter with more info
    detailed_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Simple formatter for console
    simple_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S"
    )

    # Apply formatters
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
    logging.getLogger("PIL").setLevel(logging.WARNING)
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    # Log system info
    logger = logging.getLogger(__name__)
    logger.info("DENSO888 logging system initialized")
    logger.info(f"Log directory: {logs_dir.absolute()}")
    logger.info(f"GUI callback: {'Enabled' if gui_callback else 'Disabled'}")

    return root_logger


def get_logger(name: str) -> logging.Logger:
    """Get logger instance with proper configuration"""
    return logging.getLogger(name)


class LogManager:
    """Advanced log management for DENSO888"""

    def __init__(self):
        self.log_buffer = []
        self.max_buffer_size = 1000
        self.gui_callback = None

    def set_gui_callback(self, callback: Callable):
        """Set GUI callback for real-time logging"""
        self.gui_callback = callback

    def add_log_entry(self, message: str, level: str = "info", source: str = "system"):
        """Add log entry to buffer"""
        entry = {
            "timestamp": datetime.now(),
            "level": level.upper(),
            "message": message,
            "source": source,
        }

        self.log_buffer.append(entry)

        # Trim buffer if too large
        if len(self.log_buffer) > self.max_buffer_size:
            self.log_buffer = self.log_buffer[-self.max_buffer_size :]

        # Send to GUI if callback available
        if self.gui_callback:
            try:
                formatted_message = (
                    f"[{entry['timestamp'].strftime('%H:%M:%S')}] {message}"
                )
                self.gui_callback(formatted_message, level)
            except Exception as e:
                logging.getLogger(__name__).warning(f"GUI callback failed: {e}")

    def get_logs(
        self, level_filter: Optional[str] = None, limit: Optional[int] = None
    ) -> list:
        """Get filtered logs"""
        logs = self.log_buffer

        # Filter by level
        if level_filter and level_filter.upper() != "ALL":
            logs = [log for log in logs if log["level"] == level_filter.upper()]

        # Apply limit
        if limit:
            logs = logs[-limit:]

        return logs

    def export_logs(self, filepath: str, format_type: str = "txt") -> bool:
        """Export logs to file"""
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                if format_type == "json":
                    import json

                    # Convert datetime to string for JSON serialization
                    serializable_logs = []
                    for log in self.log_buffer:
                        log_copy = log.copy()
                        log_copy["timestamp"] = log_copy["timestamp"].isoformat()
                        serializable_logs.append(log_copy)
                    json.dump(serializable_logs, f, indent=2, ensure_ascii=False)
                else:
                    # Plain text format
                    f.write("DENSO888 Application Logs\n")
                    f.write("=" * 50 + "\n\n")

                    for log in self.log_buffer:
                        timestamp = log["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
                        f.write(f"[{timestamp}] {log['level']} - {log['message']}\n")

            return True

        except Exception as e:
            logging.getLogger(__name__).error(f"Log export failed: {e}")
            return False

    def clear_logs(self):
        """Clear log buffer"""
        self.log_buffer.clear()
        self.add_log_entry("Log buffer cleared", "info", "log_manager")


# Performance monitoring logger
class PerformanceLogger:
    """Logger for performance metrics"""

    def __init__(self):
        self.logger = get_logger("performance")
        self.metrics = {}

    def start_timer(self, operation: str):
        """Start timing an operation"""
        self.metrics[operation] = {
            "start_time": datetime.now(),
            "end_time": None,
            "duration": None,
        }

    def end_timer(self, operation: str):
        """End timing and log duration"""
        if operation in self.metrics:
            self.metrics[operation]["end_time"] = datetime.now()
            duration = (
                self.metrics[operation]["end_time"]
                - self.metrics[operation]["start_time"]
            ).total_seconds()
            self.metrics[operation]["duration"] = duration

            self.logger.info(
                f"Operation '{operation}' completed in {duration:.2f} seconds"
            )
            return duration
        return None

    def log_memory_usage(self, operation: str):
        """Log memory usage"""
        try:
            import psutil

            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            self.logger.info(f"Memory usage during '{operation}': {memory_mb:.1f} MB")
            return memory_mb
        except ImportError:
            self.logger.warning("psutil not available for memory monitoring")
            return None

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get summary of performance metrics"""
        summary = {
            "total_operations": len(self.metrics),
            "completed_operations": len(
                [m for m in self.metrics.values() if m["duration"] is not None]
            ),
            "average_duration": 0,
            "slowest_operation": None,
            "fastest_operation": None,
        }

        completed = [m for m in self.metrics.values() if m["duration"] is not None]
        if completed:
            durations = [m["duration"] for m in completed]
            summary["average_duration"] = sum(durations) / len(durations)

            slowest = max(completed, key=lambda x: x["duration"])
            fastest = min(completed, key=lambda x: x["duration"])

            summary["slowest_operation"] = {
                "duration": slowest["duration"],
                "operation": [k for k, v in self.metrics.items() if v == slowest][0],
            }
            summary["fastest_operation"] = {
                "duration": fastest["duration"],
                "operation": [k for k, v in self.metrics.items() if v == fastest][0],
            }

        return summary


# Context manager for automatic performance logging
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
            self.logger.info(
                f"Operation '{self.operation_name}' completed successfully in {duration:.2f}s"
            )
        else:
            self.logger.error(
                f"Operation '{self.operation_name}' failed after {duration:.2f}s: {exc_val}"
            )

        return False  # Don't suppress exceptions


# Usage examples and utilities
def log_system_info():
    """Log system information for debugging"""
    logger = get_logger("system")

    try:
        import platform
        import sys

        logger.info(f"Python version: {sys.version}")
        logger.info(f"Platform: {platform.platform()}")
        logger.info(f"Architecture: {platform.architecture()}")
        logger.info(f"Processor: {platform.processor()}")

        try:
            import psutil

            logger.info(f"CPU cores: {psutil.cpu_count()}")
            logger.info(f"Memory: {psutil.virtual_memory().total / (1024**3):.1f} GB")
        except ImportError:
            logger.info("psutil not available for detailed system info")

    except Exception as e:
        logger.warning(f"Could not gather system info: {e}")


def setup_error_logging():
    """Setup comprehensive error logging"""

    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        logger = get_logger("exceptions")
        logger.critical(
            "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
        )

    sys.excepthook = handle_exception


# Initialize performance logger instance
performance_logger = PerformanceLogger()
log_manager = LogManager()
