from dataclasses import dataclass
import tkinter as tk
from tkinter import ttk
import json
from pathlib import Path


@dataclass
class ThemeColors:
    primary: str = "#3B82F6"
    secondary: str = "#6B7280"
    success: str = "#059669"
    danger: str = "#DC2626"
    warning: str = "#D97706"
    info: str = "#2563EB"
    background: str = "#FFFFFF"
    surface: str = "#F3F4F6"
    text: str = "#1F2937"
    text_secondary: str = "#6B7280"


class ThemeService:
    """Service for managing application theme"""

    def __init__(self):
        self.current_theme = "light"
        self.colors = ThemeColors()
        self._load_custom_theme()

    def _load_custom_theme(self):
        """Load custom theme if exists"""
        theme_file = Path("config/theme.json")
        if theme_file.exists():
            try:
                with open(theme_file, "r") as f:
                    custom_colors = json.load(f)
                    for key, value in custom_colors.items():
                        if hasattr(self.colors, key):
                            setattr(self.colors, key, value)
            except:
                pass

    def apply_theme(self, root: tk.Tk):
        """Apply theme to root window"""
        style = ttk.Style()

        # Configure common styles
        style.configure(
            "TLabel", background=self.colors.background, foreground=self.colors.text
        )

        style.configure("TFrame", background=self.colors.background)

        style.configure(
            "TButton", background=self.colors.primary, foreground=self.colors.background
        )

        # Add custom styles
        style.configure(
            "Success.TButton",
            background=self.colors.success,
            foreground=self.colors.background,
        )

        style.configure(
            "Danger.TButton",
            background=self.colors.danger,
            foreground=self.colors.background,
        )

        # Configure root
        root.configure(bg=self.colors.background)
