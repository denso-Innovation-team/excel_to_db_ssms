"""
gui/themes/modern_theme.py
Modern Theme for DENSO888 Professional - Production Ready
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class Colors:
    """Modern theme colors optimized for professional use"""

    # Primary colors
    primary: str = "#2563EB"
    primary_light: str = "#DBEAFE"
    primary_dark: str = "#1E40AF"

    # Surface colors
    surface: str = "#FFFFFF"
    surface_dark: str = "#F8FAFC"
    background: str = "#FFFFFF"

    # Text colors
    text_primary: str = "#1F2937"
    text_secondary: str = "#6B7280"
    text_tertiary: str = "#9CA3AF"

    # Status colors
    success: str = "#059669"
    warning: str = "#D97706"
    error: str = "#DC2626"
    info: str = "#2563EB"

    # Neutral grays
    gray_50: str = "#F9FAFB"
    gray_100: str = "#F3F4F6"
    gray_200: str = "#E5E7EB"


@dataclass
class Spacing:
    """Consistent spacing values"""

    xs: int = 4
    sm: int = 8
    md: int = 16
    lg: int = 24
    xl: int = 32

    # Component specific
    sidebar_width: int = 280
    header_height: int = 64


class Fonts:
    """Font configurations with fallbacks"""

    def __init__(self):
        self._fonts = {
            "heading_xl": ("Segoe UI", 20, "bold"),
            "heading_lg": ("Segoe UI", 16, "bold"),
            "heading_md": ("Segoe UI", 14, "bold"),
            "body_lg": ("Segoe UI", 12),
            "body_md": ("Segoe UI", 11),
            "body_sm": ("Segoe UI", 10),
            "caption": ("Segoe UI", 9),
            "code": ("Consolas", 10),
        }

    def get(self, key: str) -> tuple:
        """Get font configuration with fallback"""
        return self._fonts.get(key, ("Segoe UI", 11))


class ModernTheme:
    """Complete modern theme configuration"""

    def __init__(self):
        self.colors = Colors()
        self.spacing = Spacing()
        self.fonts = Fonts()

    def get_button_style(self, variant: str = "primary") -> Dict[str, str]:
        """Get button style configuration"""
        styles = {
            "primary": {
                "bg": self.colors.primary,
                "fg": "white",
                "hover_bg": self.colors.primary_dark,
            },
            "secondary": {
                "bg": self.colors.gray_100,
                "fg": self.colors.text_primary,
                "hover_bg": self.colors.gray_200,
            },
            "success": {
                "bg": self.colors.success,
                "fg": "white",
                "hover_bg": "#047857",
            },
            "danger": {
                "bg": self.colors.error,
                "fg": "white",
                "hover_bg": "#B91C1C",
            },
        }
        return styles.get(variant, styles["primary"])

    def get_card_style(self) -> Dict[str, str]:
        """Get card style configuration"""
        return {
            "bg": self.colors.surface,
            "border": self.colors.gray_200,
            "shadow": "#00000010",
            "radius": "8",
        }


# Global theme instance
modern_theme = ModernTheme()


# Utility functions for theme application
def apply_modern_style(widget, style_type: str = "default"):
    """Apply modern styling to tkinter widgets"""
    theme = modern_theme

    style_configs = {
        "default": {
            "bg": theme.colors.surface,
            "fg": theme.colors.text_primary,
            "font": theme.fonts.get("body_md"),
        },
        "header": {
            "bg": theme.colors.primary,
            "fg": "white",
            "font": theme.fonts.get("heading_lg"),
        },
        "card": {
            "bg": theme.colors.surface,
            "fg": theme.colors.text_primary,
            "relief": "solid",
            "bd": 1,
            "highlightbackground": theme.colors.gray_200,
        },
    }

    config = style_configs.get(style_type, style_configs["default"])

    try:
        widget.configure(**config)
    except Exception:
        # Fallback for incompatible widgets
        pass


def get_theme_colors() -> Colors:
    """Get theme colors for external use"""
    return modern_theme.colors


def get_theme_fonts() -> Fonts:
    """Get theme fonts for external use"""
    return modern_theme.fonts
