"""
gui/components/modern_components.py
Modern UI Components
"""

import tkinter as tk
from typing import Callable, Optional
from abc import ABC, abstractmethod


class BaseComponent(ABC):
    """Base class for all UI components"""

    def __init__(self, parent: tk.Widget, **kwargs):
        self.parent = parent
        self.widget: Optional[tk.Widget] = None

    @abstractmethod
    def create_widget(self) -> tk.Widget:
        """Create the main widget"""
        pass

    def get_widget(self) -> tk.Widget:
        """Get or create the widget"""
        if self.widget is None:
            self.widget = self.create_widget()
        return self.widget


class ModernButton(BaseComponent):
    """Modern styled button"""

    STYLES = {
        "primary": {"bg": "#DC0003", "fg": "white", "hover": "#B80002"},
        "secondary": {"bg": "#6C757D", "fg": "white", "hover": "#545B62"},
        "success": {"bg": "#28A745", "fg": "white", "hover": "#218838"},
        "danger": {"bg": "#DC3545", "fg": "white", "hover": "#C82333"},
        "info": {"bg": "#17A2B8", "fg": "white", "hover": "#138496"},
    }

    def __init__(
        self,
        parent: tk.Widget,
        text: str = "",
        icon: str = "",
        style: str = "primary",
        size: str = "medium",
        command: Callable = None,
    ):
        super().__init__(parent)
        self.text = text
        self.icon = icon
        self.style_name = style
        self.size = size
        self.command = command

        self.sizes = {
            "small": {"font": ("Segoe UI", 9), "padx": 12, "pady": 6},
            "medium": {"font": ("Segoe UI", 10), "padx": 16, "pady": 8},
            "large": {"font": ("Segoe UI", 12, "bold"), "padx": 20, "pady": 12},
        }

    def create_widget(self) -> tk.Widget:
        """Create modern button"""
        style_config = self.STYLES.get(self.style_name, self.STYLES["primary"])
        size_config = self.sizes.get(self.size, self.sizes["medium"])

        display_text = f"{self.icon} {self.text}".strip() if self.icon else self.text

        button = tk.Button(
            self.parent,
            text=display_text,
            command=self.command,
            font=size_config["font"],
            bg=style_config["bg"],
            fg=style_config["fg"],
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            padx=size_config["padx"],
            pady=size_config["pady"],
        )

        # Add hover effects
        def on_enter(e):
            button.configure(bg=style_config["hover"])

        def on_leave(e):
            button.configure(bg=style_config["bg"])

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

        return button

    def set_enabled(self, enabled: bool):
        """Enable/disable button"""
        if self.widget:
            state = "normal" if enabled else "disabled"
            self.widget.configure(state=state)
