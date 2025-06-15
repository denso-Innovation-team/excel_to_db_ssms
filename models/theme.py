"""
models/theme.py
Fixed Theme Model for Gaming Edition
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class Colors:
    """Theme colors for gaming edition"""

    # DENSO Gaming colors
    primary: str = "#FF0066"
    primary_light: str = "#FF3388"
    primary_dark: str = "#CC0044"

    # Gaming neon accents
    neon_blue: str = "#00FFFF"
    neon_green: str = "#00FF88"
    neon_purple: str = "#8866FF"
    neon_orange: str = "#FF8800"

    # Backgrounds
    background: str = "#0A0A0F"
    surface: str = "#151521"
    surface_dark: str = "#1A1A2E"
    surface_elevated: str = "#16213E"

    # Text colors
    text_primary: str = "#FFFFFF"
    text_secondary: str = "#CCCCCC"
    text_muted: str = "#888888"
    text_error: str = "#FF4466"

    # UI elements
    border: str = "#333344"
    border_glow: str = "#00FFFF"
    hover: str = "#252540"

    # Status colors
    success: str = "#00FF88"
    warning: str = "#FFB800"
    danger: str = "#FF4466"
    info: str = "#00FFFF"

    # Achievement colors
    gold: str = "#FFD700"
    silver: str = "#C0C0C0"
    bronze: str = "#CD7F32"


@dataclass
class Fonts:
    """Font configurations"""

    # Gaming fonts
    heading_xl: tuple = ("Orbitron", 24, "bold")
    heading_lg: tuple = ("Orbitron", 18, "bold")
    heading_md: tuple = ("Orbitron", 14, "bold")
    heading_sm: tuple = ("Orbitron", 12, "bold")

    # Body fonts
    body_lg: tuple = ("Segoe UI", 14)
    body_md: tuple = ("Segoe UI", 11)
    body_sm: tuple = ("Segoe UI", 10)
    caption: tuple = ("Segoe UI", 9)

    # Monospace for code/data
    code: tuple = ("Consolas", 10)
    code_sm: tuple = ("Consolas", 9)


class ThemeManager:
    """Manages application themes"""

    def __init__(self, theme_name: str = "gaming"):
        self.theme_name = theme_name
        self.colors = Colors()
        self.fonts = Fonts()

    def get_style_config(self) -> Dict:
        """Get complete style configuration"""
        return {
            "colors": self.colors,
            "fonts": self.fonts,
            "theme_name": self.theme_name,
        }


# Global theme instance
theme = ThemeManager("gaming")
