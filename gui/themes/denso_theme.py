"""
gui/themes/denso_theme.py
DENSO Brand Theme
"""

from dataclasses import dataclass


@dataclass
class ThemeColors:
    """Theme color definitions"""

    primary: str = "#DC0003"
    primary_dark: str = "#B80002"
    primary_light: str = "#FF3333"
    secondary: str = "#2C3E50"
    success: str = "#28A745"
    warning: str = "#FFC107"
    danger: str = "#DC3545"
    info: str = "#17A2B8"
    background: str = "#FFFFFF"
    surface: str = "#F8F9FA"
    text_primary: str = "#2C3E50"
    text_secondary: str = "#7F8C8D"


class DensoTheme:
    """DENSO888 theme implementation"""

    def __init__(self):
        self.colors = ThemeColors()
