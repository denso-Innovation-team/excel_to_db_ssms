"""
gui/themes/modern_theme.py
Modern Theme System with Clean Design
"""

from tkinter import ttk
from dataclasses import dataclass


@dataclass
class ModernColors:
    """Modern color palette inspired by Tailwind CSS"""

    # Primary colors
    primary: str = "#2563EB"  # Blue 600
    primary_hover: str = "#1D4ED8"  # Blue 700
    primary_light: str = "#DBEAFE"  # Blue 100

    # Neutral colors
    white: str = "#FFFFFF"
    gray_50: str = "#F8FAFC"
    gray_100: str = "#F1F5F9"
    gray_200: str = "#E2E8F0"
    gray_300: str = "#CBD5E1"
    gray_400: str = "#94A3B8"
    gray_500: str = "#64748B"
    gray_600: str = "#475569"
    gray_700: str = "#334155"
    gray_800: str = "#1E293B"
    gray_900: str = "#0F172A"

    # Status colors
    success: str = "#059669"  # Emerald 600
    success_light: str = "#D1FAE5"  # Emerald 100
    warning: str = "#D97706"  # Amber 600
    warning_light: str = "#FEF3C7"  # Amber 100
    error: str = "#DC2626"  # Red 600
    error_light: str = "#FEE2E2"  # Red 100
    info: str = "#0891B2"  # Cyan 600
    info_light: str = "#CFFAFE"  # Cyan 100


class ModernFonts:
    """Modern font system"""

    def __init__(self):
        # Font family fallbacks
        self.sans = "Inter"  # Primary font
        self.mono = "JetBrains Mono"  # Code font

        # Font sizes and weights
        self.fonts = {
            "heading_xl": (self.sans, 24, "bold"),
            "heading_lg": (self.sans, 20, "bold"),
            "heading_md": (self.sans, 16, "bold"),
            "heading_sm": (self.sans, 14, "bold"),
            "body_lg": (self.sans, 14, "normal"),
            "body_md": (self.sans, 12, "normal"),
            "body_sm": (self.sans, 11, "normal"),
            "caption": (self.sans, 10, "normal"),
            "code": (self.mono, 11, "normal"),
        }

    def get(self, key: str) -> tuple:
        """Get font configuration"""
        return self.fonts.get(key, self.fonts["body_md"])


class ModernTheme:
    """Main theme class"""

    def __init__(self):
        self.colors = ModernColors()
        self.fonts = ModernFonts()
        self.spacing = {
            "xs": 4,
            "sm": 8,
            "md": 12,
            "lg": 16,
            "xl": 20,
            "xxl": 24,
        }

    def configure_ttk_styles(self):
        """Configure ttk widget styles"""
        style = ttk.Style()

        # Progressbar
        style.configure(
            "Modern.Horizontal.TProgressbar",
            background=self.colors.primary,
            troughcolor=self.colors.gray_200,
            borderwidth=0,
            lightcolor=self.colors.primary,
            darkcolor=self.colors.primary,
        )

        # Combobox
        style.configure(
            "Modern.TCombobox",
            fieldbackground=self.colors.white,
            background=self.colors.white,
            foreground=self.colors.gray_900,
            bordercolor=self.colors.gray_300,
            focuscolor=self.colors.primary,
        )


# Global theme instance
modern_theme = ModernTheme()
