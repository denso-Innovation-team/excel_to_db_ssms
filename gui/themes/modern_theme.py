"""
gui/themes/modern_theme.py
Enhanced Theme System with Professional Layout Management
"""

from tkinter import ttk
from dataclasses import dataclass

@dataclass
class ModernColors:
    """Professional Color Palette - 8px Grid System"""
    
    # Primary Colors  
    primary: str = "#2563EB"
    primary_hover: str = "#1D4ED8"
    primary_light: str = "#DBEAFE"
    primary_dark: str = "#1E40AF"

    # Neutral Palette
    white: str = "#FFFFFF"
    gray_50: str = "#F8FAFC"
    gray_100: str = "#F1F5F9"
    gray_200: str = "#E2E8F0"
    gray_300: str = "#CBD5E1"
    gray_500: str = "#64748B"
    gray_600: str = "#475569"
    gray_900: str = "#0F172A"

    # Status Colors
    success: str = "#059669"
    success_light: str = "#D1FAE5"
    warning: str = "#D97706"
    error: str = "#DC2626"
    info: str = "#0891B2"

    # Layout Colors
    surface: str = "#FFFFFF"
    surface_elevated: str = "#F8FAFC"
    border: str = "#E2E8F0"
    border_focus: str = "#2563EB"
    
    # Text Colors
    text_primary: str = "#0F172A"
    text_secondary: str = "#475569"
    text_tertiary: str = "#64748B"
    text_inverse: str = "#FFFFFF"

@dataclass 
class Spacing:
    """8px Grid System"""
    xs: int = 4
    sm: int = 8
    md: int = 16
    lg: int = 24
    xl: int = 32
    xxl: int = 48
    
    # Layout Dimensions
    sidebar_width: int = 280
    header_height: int = 64
    content_padding: int = 24
    card_padding: int = 20

class ModernFonts:
    """Typography System"""
    
    def __init__(self):
        self.fonts = {
            "heading_xl": ("Inter", 24, "bold"),
            "heading_lg": ("Inter", 20, "bold"),
            "heading_md": ("Inter", 16, "bold"),
            "heading_sm": ("Inter", 14, "bold"),
            "body_lg": ("Inter", 14, "normal"),
            "body_md": ("Inter", 12, "normal"),
            "body_sm": ("Inter", 11, "normal"),
            "caption": ("Inter", 10, "normal"),
            "code": ("JetBrains Mono", 11, "normal"),
        }

    def get(self, key: str) -> tuple:
        return self.fonts.get(key, self.fonts["body_md"])

class ModernTheme:
    """Enhanced Theme Manager"""
    
    def __init__(self):
        self.colors = ModernColors()
        self.fonts = ModernFonts()
        self.spacing = Spacing()
        
    def get_card_style(self) -> dict:
        """Standard card styling"""
        return {
            'bg': self.colors.surface,
            'relief': 'solid',
            'bd': 1,
            'highlightbackground': self.colors.border,
            'highlightthickness': 0
        }

    def get_button_style(self, variant: str = 'primary') -> dict:
        """Button styling by variant"""
        styles = {
            'primary': {
                'bg': self.colors.primary,
                'fg': self.colors.text_inverse,
                'activebackground': self.colors.primary_dark
            },
            'secondary': {
                'bg': self.colors.gray_100,
                'fg': self.colors.text_primary,
                'activebackground': self.colors.gray_200
            }
        }
        
        base_style = {
            'relief': 'flat',
            'bd': 0,
            'cursor': 'hand2',
            'font': self.fonts.get('body_md')
        }
        
        return {**base_style, **styles.get(variant, styles['primary'])}

# Global theme instance
modern_theme = ModernTheme()
