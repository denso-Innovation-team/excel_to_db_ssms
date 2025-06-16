"""
services/notification_service.py
Notification Service - Centralized Messaging System
"""

import tkinter as tk
from typing import Dict, List, Callable, Optional
from datetime import datetime
import queue


class NotificationService:
    """Centralized notification service"""

    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {
            "info": [],
            "success": [],
            "warning": [],
            "error": [],
            "all": [],  # Global listeners
        }
        self.notification_queue = queue.Queue()
        self.notification_history: List[Dict] = []
        self.max_history = 100

    def subscribe(self, notification_type: str, callback: Callable):
        """Subscribe to notifications"""
        if notification_type not in self.listeners:
            self.listeners[notification_type] = []

        self.listeners[notification_type].append(callback)

    def unsubscribe(self, notification_type: str, callback: Callable):
        """Unsubscribe from notifications"""
        if notification_type in self.listeners:
            try:
                self.listeners[notification_type].remove(callback)
            except ValueError:
                pass

    def notify(self, message: str, type_: str = "info", **kwargs):
        """Send notification"""
        notification = {
            "message": message,
            "type": type_,
            "timestamp": datetime.now(),
            "data": kwargs,
        }

        # Add to history
        self._add_to_history(notification)

        # Notify specific type listeners
        self._notify_listeners(type_, notification)

        # Notify global listeners
        self._notify_listeners("all", notification)

        # Add to queue for UI processing
        self.notification_queue.put(notification)

    def info(self, message: str, **kwargs):
        """Send info notification"""
        self.notify(message, "info", **kwargs)

    def success(self, message: str, **kwargs):
        """Send success notification"""
        self.notify(message, "success", **kwargs)

    def warning(self, message: str, **kwargs):
        """Send warning notification"""
        self.notify(message, "warning", **kwargs)

    def error(self, message: str, **kwargs):
        """Send error notification"""
        self.notify(message, "error", **kwargs)

    def progress(self, message: str, progress: float = 0, **kwargs):
        """Send progress notification"""
        self.notify(message, "progress", progress=progress, **kwargs)

    def _notify_listeners(self, type_: str, notification: Dict):
        """Notify all listeners of specific type"""
        for callback in self.listeners.get(type_, []):
            try:
                callback(notification)
            except Exception as e:
                print(f"Notification listener error: {e}")

    def _add_to_history(self, notification: Dict):
        """Add notification to history"""
        self.notification_history.append(notification)

        # Keep only max_history items
        if len(self.notification_history) > self.max_history:
            self.notification_history = self.notification_history[-self.max_history :]

    def get_history(
        self, type_filter: Optional[str] = None, limit: int = 50
    ) -> List[Dict]:
        """Get notification history"""
        history = self.notification_history

        # Filter by type if specified
        if type_filter:
            history = [n for n in history if n["type"] == type_filter]

        # Return most recent first, limited
        return list(reversed(history[-limit:]))

    def clear_history(self):
        """Clear notification history"""
        self.notification_history.clear()

    def get_pending_notifications(self) -> List[Dict]:
        """Get all pending notifications from queue"""
        notifications = []
        while not self.notification_queue.empty():
            try:
                notifications.append(self.notification_queue.get_nowait())
            except queue.Empty:
                break
        return notifications


class UINotificationHandler:
    """Handle notifications in UI context"""

    def __init__(
        self, parent_widget: tk.Widget, notification_service: NotificationService
    ):
        self.parent = parent_widget
        self.service = notification_service
        self.toast_notifications = []

        # Subscribe to all notifications
        self.service.subscribe("all", self._handle_notification)

        # Start UI update loop
        self._start_ui_updates()

    def _handle_notification(self, notification: Dict):
        """Handle incoming notification"""
        type_ = notification["type"]
        message = notification["message"]

        if type_ in ["info", "success", "warning", "error"]:
            self._show_toast(message, type_)
        elif type_ == "progress":
            progress = notification["data"].get("progress", 0)
            self._update_progress(message, progress)

    def _show_toast(self, message: str, type_: str):
        """Show toast notification"""
        try:
            # Try to use modern notification component
            from ..gui.components.modern_notification import ModernNotification

            ModernNotification.show(self.parent, message, type_)
        except ImportError:
            # Fallback to simple message
            self._show_simple_message(message, type_)

    def _show_simple_message(self, message: str, type_: str):
        """Simple message display fallback"""
        from tkinter import messagebox

        if type_ == "error":
            messagebox.showerror("Error", message)
        elif type_ == "warning":
            messagebox.showwarning("Warning", message)
        elif type_ == "success":
            messagebox.showinfo("Success", message)
        else:
            messagebox.showinfo("Info", message)

    def _update_progress(self, message: str, progress: float):
        """Update progress display"""
        # This could be enhanced to show actual progress bars
        print(f"Progress: {message} ({progress}%)")

    def _start_ui_updates(self):
        """Start periodic UI updates"""

        def update_ui():
            try:
                # Process pending notifications
                pending = self.service.get_pending_notifications()
                for notification in pending:
                    # Additional UI processing if needed
                    pass
            except Exception as e:
                print(f"UI update error: {e}")
            finally:
                # Schedule next update
                self.parent.after(100, update_ui)

        # Start the update loop
        update_ui()


class LogNotificationHandler:
    """Handle notifications by logging them"""

    def __init__(self, notification_service: NotificationService):
        import logging

        self.logger = logging.getLogger("notifications")
        self.service = notification_service

        # Subscribe to all notifications
        self.service.subscribe("all", self._log_notification)

    def _log_notification(self, notification: Dict):
        """Log notification"""
        type_ = notification["type"]
        message = notification["message"]
        timestamp = notification["timestamp"].strftime("%Y-%m-%d %H:%M:%S")

        log_message = f"[{timestamp}] {type_.upper()}: {message}"

        if type_ == "error":
            self.logger.error(log_message)
        elif type_ == "warning":
            self.logger.warning(log_message)
        elif type_ == "success":
            self.logger.info(log_message)
        else:
            self.logger.info(log_message)


class FileNotificationHandler:
    """Handle notifications by writing to file"""

    def __init__(
        self,
        notification_service: NotificationService,
        file_path: str = "logs/notifications.log",
    ):
        self.file_path = file_path
        self.service = notification_service

        # Ensure log directory exists
        from pathlib import Path

        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        # Subscribe to all notifications
        self.service.subscribe("all", self._write_notification)

    def _write_notification(self, notification: Dict):
        """Write notification to file"""
        try:
            type_ = notification["type"]
            message = notification["message"]
            timestamp = notification["timestamp"].strftime("%Y-%m-%d %H:%M:%S")

            log_line = f"[{timestamp}] {type_.upper()}: {message}\n"

            with open(self.file_path, "a", encoding="utf-8") as f:
                f.write(log_line)
        except Exception as e:
            print(f"File notification error: {e}")


class OperationNotifier:
    """Convenience class for operation notifications"""

    def __init__(self, service: NotificationService, operation_name: str):
        self.service = service
        self.operation_name = operation_name
        self.start_time = None

    def start(self, message: str = None):
        """Start operation notification"""
        self.start_time = datetime.now()
        msg = message or f"Starting {self.operation_name}..."
        self.service.info(msg)

    def progress(self, message: str, progress: float):
        """Progress notification"""
        self.service.progress(f"{self.operation_name}: {message}", progress)

    def success(self, message: str = None):
        """Success notification"""
        duration = self._get_duration()
        msg = message or f"{self.operation_name} completed successfully"
        if duration:
            msg += f" (took {duration})"
        self.service.success(msg)

    def error(self, message: str = None, error: Exception = None):
        """Error notification"""
        if error:
            msg = message or f"{self.operation_name} failed: {str(error)}"
        else:
            msg = message or f"{self.operation_name} failed"
        self.service.error(msg)

    def warning(self, message: str):
        """Warning notification"""
        self.service.warning(f"{self.operation_name}: {message}")

    def _get_duration(self) -> Optional[str]:
        """Get operation duration"""
        if not self.start_time:
            return None

        duration = datetime.now() - self.start_time
        seconds = duration.total_seconds()

        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}m"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}h"


# Global notification service instance
notification_service = NotificationService()


# Convenience functions
def notify_info(message: str, **kwargs):
    """Global info notification"""
    notification_service.info(message, **kwargs)


def notify_success(message: str, **kwargs):
    """Global success notification"""
    notification_service.success(message, **kwargs)


def notify_warning(message: str, **kwargs):
    """Global warning notification"""
    notification_service.warning(message, **kwargs)


def notify_error(message: str, **kwargs):
    """Global error notification"""
    notification_service.error(message, **kwargs)


def notify_progress(message: str, progress: float, **kwargs):
    """Global progress notification"""
    notification_service.progress(message, progress, **kwargs)


def create_operation_notifier(operation_name: str) -> OperationNotifier:
    """Create operation notifier"""
    return OperationNotifier(notification_service, operation_name)


# Context manager for operations
class NotificationContext:
    """Context manager for operation notifications"""

    def __init__(
        self,
        operation_name: str,
        start_message: str = None,
        success_message: str = None,
    ):
        self.notifier = OperationNotifier(notification_service, operation_name)
        self.start_message = start_message
        self.success_message = success_message

    def __enter__(self):
        self.notifier.start(self.start_message)
        return self.notifier

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.notifier.success(self.success_message)
        else:
            self.notifier.error(error=exc_val)
        return False  # Don't suppress exceptions


# Usage example in other files:
# with NotificationContext("Excel Import", "Starting import...", "Import completed!") as notifier:
#     notifier.progress("Reading file...", 25)
#     # do work
#     notifier.progress("Processing data...", 75)
#     # more work
