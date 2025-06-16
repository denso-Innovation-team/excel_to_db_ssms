import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

"""
gui/components/modern_notification.py
Modern Notification Component - Complete Working Version
"""

import tkinter as tk
from typing import Dict


class ModernNotification:
    """Modern notification/toast component that actually works"""

    _instance = None
    _active_notifications = []
    _parent_window = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def initialize(cls, parent_window: tk.Widget):
        """Initialize with parent window"""
        cls._parent_window = parent_window

    @classmethod
    def show(
        cls, parent: tk.Widget, message: str, type_: str = "info", duration: int = 3000
    ) -> None:
        """Show notification - simplified but working version"""
        try:
            # Use provided parent or stored parent
            window_parent = parent or cls._parent_window
            if not window_parent:
                print(f"Notification: {message}")  # Fallback to console
                return

            # Create notification window
            notification = tk.Toplevel(window_parent)
            notification.withdraw()  # Hide initially
            notification.overrideredirect(True)
            notification.attributes("-topmost", True)

            # Get colors based on type
            colors = cls._get_notification_colors(type_)

            # Main frame
            main_frame = tk.Frame(
                notification, bg=colors["bg"], relief="solid", bd=1, padx=16, pady=12
            )
            main_frame.pack(fill="both", expand=True)

            # Content
            content_frame = tk.Frame(main_frame, bg=colors["bg"])
            content_frame.pack(fill="x")

            # Icon
            icon_label = tk.Label(
                content_frame,
                text=colors["icon"],
                font=("Segoe UI", 14),
                bg=colors["bg"],
                fg=colors["fg"],
            )
            icon_label.pack(side="left", padx=(0, 8))

            # Message
            message_label = tk.Label(
                content_frame,
                text=message,
                font=("Segoe UI", 11),
                bg=colors["bg"],
                fg=colors["fg"],
                wraplength=300,
            )
            message_label.pack(side="left", fill="x", expand=True)

            # Close button
            close_btn = tk.Button(
                content_frame,
                text="✕",
                font=("Segoe UI", 10),
                bg=colors["bg"],
                fg=colors["fg"],
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda: cls._close_notification(notification),
            )
            close_btn.pack(side="right")

            # Position notification
            cls._position_notification(notification)

            # Show notification
            notification.deiconify()
            cls._active_notifications.append(notification)

            # Auto close
            if duration > 0:
                notification.after(
                    duration, lambda: cls._close_notification(notification)
                )

            # Click to close
            notification.bind(
                "<Button-1>", lambda e: cls._close_notification(notification)
            )
            main_frame.bind(
                "<Button-1>", lambda e: cls._close_notification(notification)
            )

        except Exception as e:
            print(f"Notification error: {e}")
            print(f"Message: {message}")  # Fallback

    @classmethod
    def _get_notification_colors(cls, type_: str) -> Dict[str, str]:
        """Get colors for notification type"""
        colors = {
            "success": {"bg": "#10B981", "fg": "white", "icon": "✓"},
            "error": {"bg": "#EF4444", "fg": "white", "icon": "✕"},
            "warning": {"bg": "#F59E0B", "fg": "white", "icon": "⚠"},
            "info": {"bg": "#3B82F6", "fg": "white", "icon": "ℹ"},
        }
        return colors.get(type_, colors["info"])

    @classmethod
    def _position_notification(cls, notification: tk.Toplevel):
        """Position notification on screen"""
        notification.update_idletasks()
        width = notification.winfo_reqwidth()
        height = notification.winfo_reqheight()

        # Get screen dimensions
        screen_width = notification.winfo_screenwidth()

        # Position: top-right corner
        x = screen_width - width - 20
        y = 20 + len(cls._active_notifications) * (height + 10)

        notification.geometry(f"{width}x{height}+{x}+{y}")

    @classmethod
    def _close_notification(cls, notification: tk.Toplevel):
        """Close notification"""
        try:
            if notification in cls._active_notifications:
                cls._active_notifications.remove(notification)

            if notification.winfo_exists():
                notification.destroy()

            # Reposition remaining notifications
            cls._reposition_notifications()
        except:
            pass

    @classmethod
    def _reposition_notifications(cls):
        """Reposition remaining notifications"""
        try:
            for i, notification in enumerate(cls._active_notifications):
                if notification.winfo_exists():
                    width = notification.winfo_width()
                    height = notification.winfo_height()
                    screen_width = notification.winfo_screenwidth()

                    x = screen_width - width - 20
                    y = 20 + i * (height + 10)

                    notification.geometry(f"+{x}+{y}")
        except:
            pass

    @classmethod
    def show_success(cls, parent: tk.Widget, message: str, duration: int = 3000):
        """Show success notification"""
        cls.show(parent, message, "success", duration)

    @classmethod
    def show_error(cls, parent: tk.Widget, message: str, duration: int = 5000):
        """Show error notification"""
        cls.show(parent, message, "error", duration)

    @classmethod
    def show_warning(cls, parent: tk.Widget, message: str, duration: int = 4000):
        """Show warning notification"""
        cls.show(parent, message, "warning", duration)

    @classmethod
    def show_info(cls, parent: tk.Widget, message: str, duration: int = 3000):
        """Show info notification"""
        cls.show(parent, message, "info", duration)

    @classmethod
    def clear_all(cls):
        """Clear all notifications"""
        for notification in cls._active_notifications[:]:
            cls._close_notification(notification)


class NotificationCenter:
    """Simplified notification center for managing notifications"""

    def __init__(self, parent: tk.Widget):
        self.parent = parent
        ModernNotification.initialize(parent)

    def success(self, message: str):
        """Show success message"""
        ModernNotification.show_success(self.parent, message)

    def error(self, message: str):
        """Show error message"""
        ModernNotification.show_error(self.parent, message)

    def warning(self, message: str):
        """Show warning message"""
        ModernNotification.show_warning(self.parent, message)

    def info(self, message: str):
        """Show info message"""
        ModernNotification.show_info(self.parent, message)

    def show(self, message: str, type_: str = "info"):
        """Show general message"""
        ModernNotification.show(self.parent, message, type_)


# Global convenience functions
def init_notifications(parent_window: tk.Widget):
    """Initialize global notifications"""
    ModernNotification.initialize(parent_window)


def show_success(parent: tk.Widget, message: str):
    """Global success notification"""
    ModernNotification.show_success(parent, message)


def show_error(parent: tk.Widget, message: str):
    """Global error notification"""
    ModernNotification.show_error(parent, message)


def show_warning(parent: tk.Widget, message: str):
    """Global warning notification"""
    ModernNotification.show_warning(parent, message)


def show_info(parent: tk.Widget, message: str):
    """Global info notification"""
    ModernNotification.show_info(parent, message)
