import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

"""
gui/components/modern_button.py
Modern Button Component - Clean & Reusable
"""

import tkinter as tk
from typing import Callable, Optional


class ModernButton:
    """Modern button with hover effects"""

    def __init__(
        self,
        parent: tk.Widget,
        text: str,
        command: Optional[Callable] = None,
        style: str = "primary",
        icon: Optional[str] = None,
        width: int = None,
        height: int = None,
    ):
        self.parent = parent
        self.text = text
        self.command = command
        self.style = style
        self.icon = icon

        # Colors by style
        self.colors = self._get_colors(style)

        # Create button
        self.button = self._create_button(width, height)
        self._setup_events()

    def _get_colors(self, style: str) -> dict:
        """Get colors for button style"""
        styles = {
            "primary": {
                "bg": "#2563EB",
                "hover": "#1D4ED8",
                "text": "white",
            },
            "success": {
                "bg": "#059669",
                "hover": "#047857",
                "text": "white",
            },
            "warning": {
                "bg": "#D97706",
                "hover": "#B45309",
                "text": "white",
            },
            "danger": {
                "bg": "#DC2626",
                "hover": "#B91C1C",
                "text": "white",
            },
            "secondary": {
                "bg": "#F1F5F9",
                "hover": "#E2E8F0",
                "text": "#1E293B",
            },
        }
        return styles.get(style, styles["primary"])

    def _create_button(self, width: int, height: int) -> tk.Button:
        """Create button widget"""
        # Button text with icon
        display_text = f"{self.icon} {self.text}" if self.icon else self.text

        button = tk.Button(
            self.parent,
            text=display_text,
            command=self.command,
            bg=self.colors["bg"],
            fg=self.colors["text"],
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=20,
            pady=10,
        )

        if width:
            button.configure(width=width)
        if height:
            button.configure(height=height)

        return button

    def _setup_events(self):
        """Setup hover events"""

        def on_enter(event):
            self.button.configure(bg=self.colors["hover"])

        def on_leave(event):
            self.button.configure(bg=self.colors["bg"])

        self.button.bind("<Enter>", on_enter)
        self.button.bind("<Leave>", on_leave)

    def pack(self, **kwargs):
        """Pack button"""
        self.button.pack(**kwargs)

    def grid(self, **kwargs):
        """Grid button"""
        self.button.grid(**kwargs)

    def configure(self, **kwargs):
        """Configure button"""
        self.button.configure(**kwargs)

    def get_widget(self) -> tk.Button:
        """Get button widget"""
        return self.button


class IconButton(ModernButton):
    """Icon-only button"""

    def __init__(
        self, parent: tk.Widget, icon: str, command: Optional[Callable] = None, **kwargs
    ):
        super().__init__(parent, "", command, icon=icon, **kwargs)
        self.button.configure(padx=10, pady=10)


class ActionButton:
    """Action button with loading state"""

    def __init__(
        self, parent: tk.Widget, text: str, command: Optional[Callable] = None
    ):
        self.parent = parent
        self.text = text
        self.command = command
        self.is_loading = False

        self.button = ModernButton(parent, text, self._handle_click, "primary")

    def _handle_click(self):
        """Handle button click with loading state"""
        if self.is_loading or not self.command:
            return

        self.set_loading(True)
        try:
            self.command()
        finally:
            self.set_loading(False)

    def set_loading(self, loading: bool):
        """Set loading state"""
        self.is_loading = loading
        if loading:
            self.button.configure(text="🔄 Loading...")
            self.button.button.configure(state="disabled")
        else:
            self.button.configure(text=self.text)
            self.button.button.configure(state="normal")

    def pack(self, **kwargs):
        self.button.pack(**kwargs)

    def grid(self, **kwargs):
        self.button.grid(**kwargs)
