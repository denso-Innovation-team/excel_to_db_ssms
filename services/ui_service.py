"""
services/ui_service.py
UI Management Service - DENSO888 Professional
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Dict, Any, Optional, Callable
import threading
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class UIService:
    """Centralized UI management service"""

    def __init__(self):
        self.main_window = None
        self.dialogs = {}
        self.progress_windows = {}
        self.notification_queue = []
        self.ui_callbacks = {}
        self.current_theme = "modern"

        # UI state management
        self.ui_state = {
            "busy": False,
            "current_operation": None,
            "progress_value": 0,
            "status_message": "Ready",
        }

    def set_main_window(self, main_window):
        """Set reference to main window"""
        self.main_window = main_window
        self._setup_ui_events()

    def _setup_ui_events(self):
        """Setup UI event handlers"""
        if self.main_window and hasattr(self.main_window, "root"):
            # Bind window events
            self.main_window.root.protocol("WM_DELETE_WINDOW", self._on_window_close)

            # Setup periodic UI updates
            self._schedule_ui_updates()

    def _schedule_ui_updates(self):
        """Schedule periodic UI updates"""
        if self.main_window and hasattr(self.main_window, "root"):
            # Process notification queue
            self._process_notifications()

            # Schedule next update
            self.main_window.root.after(100, self._schedule_ui_updates)

    def _process_notifications(self):
        """Process pending notifications"""
        while self.notification_queue:
            try:
                notification = self.notification_queue.pop(0)
                self._show_notification(notification)
            except IndexError:
                break
            except Exception as e:
                logger.error(f"Notification processing error: {e}")

    # Theme Management
    def apply_preferences(self, preferences_service):
        """Apply user preferences to UI"""
        try:
            if preferences_service:
                theme = preferences_service.get("theme", "modern")
                self.set_theme(theme)

                # Apply other UI preferences
                window_size = preferences_service.get("window_size")
                if window_size and self.main_window:
                    self.main_window.root.geometry(f"{window_size[0]}x{window_size[1]}")

        except Exception as e:
            logger.error(f"Failed to apply preferences: {e}")

    def set_theme(self, theme_name: str):
        """Set UI theme"""
        self.current_theme = theme_name
        if self.main_window:
            self._apply_theme_to_window()

    def _apply_theme_to_window(self):
        """Apply current theme to main window"""
        try:
            # Import theme
            from gui.themes.modern_theme import modern_theme

            # Apply theme colors
            if hasattr(self.main_window, "root"):
                self.main_window.root.configure(bg=modern_theme.colors.background)

        except Exception as e:
            logger.error(f"Theme application failed: {e}")

    # Dialog Management
    def show_file_dialog(self, dialog_type: str = "open", **kwargs) -> Optional[str]:
        """Show file dialog"""
        try:
            if dialog_type == "open":
                return filedialog.askopenfilename(
                    title=kwargs.get("title", "Select File"),
                    filetypes=kwargs.get("filetypes", [("All files", "*.*")]),
                    initialdir=kwargs.get("initialdir", "."),
                )
            elif dialog_type == "save":
                return filedialog.asksaveasfilename(
                    title=kwargs.get("title", "Save File"),
                    filetypes=kwargs.get("filetypes", [("All files", "*.*")]),
                    defaultextension=kwargs.get("defaultextension", ""),
                    initialdir=kwargs.get("initialdir", "."),
                )
            elif dialog_type == "directory":
                return filedialog.askdirectory(
                    title=kwargs.get("title", "Select Directory"),
                    initialdir=kwargs.get("initialdir", "."),
                )

        except Exception as e:
            logger.error(f"File dialog error: {e}")
            return None

    def show_message(
        self, message: str, title: str = "Message", msg_type: str = "info"
    ) -> Optional[bool]:
        """Show message dialog"""
        try:
            if msg_type == "info":
                messagebox.showinfo(title, message)
                return None
            elif msg_type == "warning":
                messagebox.showwarning(title, message)
                return None
            elif msg_type == "error":
                messagebox.showerror(title, message)
                return None
            elif msg_type == "question":
                return messagebox.askyesno(title, message)
            elif msg_type == "confirm":
                return messagebox.askokcancel(title, message)

        except Exception as e:
            logger.error(f"Message dialog error: {e}")
            return None

    def show_input_dialog(
        self, title: str, prompt: str, default_value: str = ""
    ) -> Optional[str]:
        """Show input dialog"""
        try:
            from tkinter import simpledialog

            return simpledialog.askstring(title, prompt, initialvalue=default_value)
        except Exception as e:
            logger.error(f"Input dialog error: {e}")
            return None

    # Progress Management
    def show_progress_dialog(self, title: str, operation_id: str) -> str:
        """Show progress dialog"""
        try:
            if operation_id in self.progress_windows:
                return operation_id

            # Create progress window
            progress_window = tk.Toplevel(
                self.main_window.root if self.main_window else None
            )
            progress_window.title(title)
            progress_window.geometry("400x150")
            progress_window.resizable(False, False)

            # Center the window
            self._center_window(progress_window, 400, 150)

            # Progress components
            main_frame = ttk.Frame(progress_window, padding="20")
            main_frame.pack(fill="both", expand=True)

            # Progress label
            progress_label = ttk.Label(main_frame, text="Starting...")
            progress_label.pack(pady=(0, 10))

            # Progress bar
            progress_var = tk.DoubleVar()
            progress_bar = ttk.Progressbar(
                main_frame, variable=progress_var, maximum=100, length=350
            )
            progress_bar.pack(pady=(0, 10))

            # Cancel button
            cancel_button = ttk.Button(
                main_frame,
                text="Cancel",
                command=lambda: self._cancel_operation(operation_id),
            )
            cancel_button.pack()

            # Store progress window components
            self.progress_windows[operation_id] = {
                "window": progress_window,
                "label": progress_label,
                "progress_var": progress_var,
                "progress_bar": progress_bar,
                "cancel_button": cancel_button,
                "cancelled": False,
            }

            return operation_id

        except Exception as e:
            logger.error(f"Progress dialog error: {e}")
            return operation_id

    def update_progress(self, operation_id: str, progress: float, message: str = ""):
        """Update progress dialog"""
        try:
            if operation_id not in self.progress_windows:
                return

            progress_info = self.progress_windows[operation_id]

            # Update progress bar
            progress_info["progress_var"].set(progress)

            # Update label
            if message:
                progress_info["label"].configure(text=message)

            # Update window
            progress_info["window"].update()

        except Exception as e:
            logger.error(f"Progress update error: {e}")

    def close_progress_dialog(self, operation_id: str):
        """Close progress dialog"""
        try:
            if operation_id in self.progress_windows:
                progress_info = self.progress_windows[operation_id]
                progress_info["window"].destroy()
                del self.progress_windows[operation_id]

        except Exception as e:
            logger.error(f"Progress close error: {e}")

    def _cancel_operation(self, operation_id: str):
        """Cancel operation"""
        if operation_id in self.progress_windows:
            self.progress_windows[operation_id]["cancelled"] = True

            # Trigger callback if registered
            if operation_id in self.ui_callbacks:
                callback = self.ui_callbacks[operation_id].get("cancel")
                if callback:
                    threading.Thread(target=callback, daemon=True).start()

    def is_operation_cancelled(self, operation_id: str) -> bool:
        """Check if operation was cancelled"""
        if operation_id in self.progress_windows:
            return self.progress_windows[operation_id]["cancelled"]
        return False

    # Notification System
    def queue_notification(self, message: str, notification_type: str = "info"):
        """Queue notification for display"""
        self.notification_queue.append(
            {
                "message": message,
                "type": notification_type,
                "timestamp": datetime.now(),
            }
        )

    def _show_notification(self, notification: Dict[str, Any]):
        """Show notification"""
        try:
            msg_type = notification["type"]
            message = notification["message"]

            if msg_type == "error":
                self.show_message(message, "Error", "error")
            elif msg_type == "warning":
                self.show_message(message, "Warning", "warning")
            elif msg_type == "success":
                self.show_message(message, "Success", "info")
            else:
                self.show_message(message, "Information", "info")

        except Exception as e:
            logger.error(f"Notification display error: {e}")

    # Status Management
    def update_status(self, message: str, busy: bool = False):
        """Update application status"""
        self.ui_state["status_message"] = message
        self.ui_state["busy"] = busy

        # Update main window status if available
        if self.main_window and hasattr(self.main_window, "update_status"):
            self.main_window.update_status(message)

    def set_busy(self, busy: bool, operation: str = None):
        """Set application busy state"""
        self.ui_state["busy"] = busy
        self.ui_state["current_operation"] = operation

        # Update cursor
        if self.main_window and hasattr(self.main_window, "root"):
            cursor = "wait" if busy else ""
            self.main_window.root.configure(cursor=cursor)

    # Callback Management
    def register_callback(self, operation_id: str, callbacks: Dict[str, Callable]):
        """Register operation callbacks"""
        self.ui_callbacks[operation_id] = callbacks

    def unregister_callback(self, operation_id: str):
        """Unregister operation callbacks"""
        if operation_id in self.ui_callbacks:
            del self.ui_callbacks[operation_id]

    # Window Management
    def _center_window(self, window, width: int, height: int):
        """Center window on screen"""
        try:
            # Get screen dimensions
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()

            # Calculate position
            x = (screen_width // 2) - (width // 2)
            y = (screen_height // 2) - (height // 2)

            # Set geometry
            window.geometry(f"{width}x{height}+{x}+{y}")

        except Exception as e:
            logger.error(f"Window centering error: {e}")

    def create_modal_dialog(
        self, title: str, content_frame_setup: Callable
    ) -> tk.Toplevel:
        """Create modal dialog"""
        try:
            dialog = tk.Toplevel(self.main_window.root if self.main_window else None)
            dialog.title(title)
            dialog.transient(self.main_window.root if self.main_window else None)
            dialog.grab_set()

            # Setup content
            content_frame_setup(dialog)

            return dialog

        except Exception as e:
            logger.error(f"Modal dialog creation error: {e}")
            return None

    # State Management
    def get_ui_state(self) -> Dict[str, Any]:
        """Get current UI state"""
        return self.ui_state.copy()

    def is_busy(self) -> bool:
        """Check if UI is busy"""
        return self.ui_state["busy"]

    # Event Handlers
    def _on_window_close(self):
        """Handle main window close event"""
        try:
            # Check if any operations are running
            if self.ui_state["busy"]:
                result = self.show_message(
                    "Operation in progress. Are you sure you want to exit?",
                    "Confirm Exit",
                    "question",
                )
                if not result:
                    return

            # Close all dialogs
            self._close_all_dialogs()

            # Destroy main window
            if self.main_window and hasattr(self.main_window, "root"):
                self.main_window.root.destroy()

        except Exception as e:
            logger.error(f"Window close error: {e}")

    def _close_all_dialogs(self):
        """Close all open dialogs"""
        try:
            # Close progress dialogs
            for operation_id in list(self.progress_windows.keys()):
                self.close_progress_dialog(operation_id)

            # Close other dialogs
            for dialog_id in list(self.dialogs.keys()):
                if self.dialogs[dialog_id]:
                    self.dialogs[dialog_id].destroy()
                    del self.dialogs[dialog_id]

        except Exception as e:
            logger.error(f"Dialog cleanup error: {e}")

    # Utility Methods
    def run_in_ui_thread(self, callback: Callable, *args, **kwargs):
        """Run callback in UI thread"""
        if self.main_window and hasattr(self.main_window, "root"):
            self.main_window.root.after(0, lambda: callback(*args, **kwargs))

    def validate_ui_ready(self) -> bool:
        """Validate UI is ready for operations"""
        return (
            self.main_window is not None
            and hasattr(self.main_window, "root")
            and not self.ui_state["busy"]
        )

    def cleanup(self):
        """Cleanup UI service"""
        try:
            self._close_all_dialogs()
            self.notification_queue.clear()
            self.ui_callbacks.clear()

            logger.info("UI service cleanup completed")

        except Exception as e:
            logger.error(f"UI cleanup error: {e}")
