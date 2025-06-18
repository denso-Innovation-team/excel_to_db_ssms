import logging
import traceback
import tkinter.messagebox as msgbox
from typing import Optional, Dict, Any
from pathlib import Path
import json
from datetime import datetime


class ErrorHandler:
    """Centralized error handling"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.error_log = Path("logs/errors.json")
        self.error_log.parent.mkdir(exist_ok=True)

    def handle_error(self, error: Exception, context: str = ""):
        """Handle an error with appropriate logging and user feedback"""
        # Log error
        logging.error(f"Error in {context}: {str(error)}", exc_info=True)

        # Save error details
        self._save_error(error, context)

        # Show user-friendly message
        self._show_error_dialog(error, context)

    def _save_error(self, error: Exception, context: str):
        """Save error details to JSON log"""
        error_data = {
            "timestamp": datetime.now().isoformat(),
            "type": error.__class__.__name__,
            "message": str(error),
            "context": context,
            "traceback": traceback.format_exc(),
        }

        try:
            if self.error_log.exists():
                with open(self.error_log, "r", encoding="utf-8") as f:
                    errors = json.load(f)
            else:
                errors = []

            errors.append(error_data)

            # Keep last 100 errors
            errors = errors[-100:]

            with open(self.error_log, "w", encoding="utf-8") as f:
                json.dump(errors, f, indent=2, ensure_ascii=False)

        except Exception as e:
            logging.error(f"Failed to save error log: {e}")

    def _show_error_dialog(self, error: Exception, context: str):
        """Show user-friendly error dialog"""
        error_type = error.__class__.__name__

        # Get user-friendly message based on error type
        message = self._get_friendly_message(error_type, str(error))

        # Show dialog with recovery suggestion
        msgbox.showerror(
            "Error",
            f"An error occurred in {context}\n\n"
            f"{message}\n\n"
            f"Suggestion: {self._get_recovery_suggestion(error_type)}",
        )

    def _get_friendly_message(self, error_type: str, error_msg: str) -> str:
        """Get user-friendly error message"""
        messages = {
            "ConnectionError": "Failed to connect to database. Please check your connection settings.",
            "FileNotFoundError": "Required file not found. Please verify the file exists.",
            "PermissionError": "Access denied. Please check your permissions.",
            "ValueError": "Invalid value or format.",
            "MemoryError": "Not enough memory to complete operation.",
        }

        return messages.get(error_type, str(error_msg))

    def _get_recovery_suggestion(self, error_type: str) -> str:
        """Get recovery suggestion based on error type"""
        suggestions = {
            "ConnectionError": "Try reconnecting or verify database settings",
            "FileNotFoundError": "Check file path and try again",
            "PermissionError": "Run as administrator or check file permissions",
            "ValueError": "Verify input values and formats",
            "MemoryError": "Close other applications and try again",
        }

        return suggestions.get(error_type, "Please try again or contact support")


def setup_error_handling(config: Optional[Dict[str, Any]] = None) -> ErrorHandler:
    """Setup global error handler"""
    handler = ErrorHandler(config)

    # Set as default exception handler
    def global_exception_handler(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            # Don't handle keyboard interrupt
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        handler.handle_error(exc_value)

    import sys

    sys.excepthook = global_exception_handler

    return handler
