"""
Modern Theme Manager for DENSO888
"""

import tkinter as tk
from tkinter import ttk

class ModernThemeManager:
    """Simple theme manager"""
    
    def __init__(self):
        self.current_theme = "denso_corporate"
        self.themes = {
            "denso_corporate": {
                "primary": "#DC0003",
                "secondary": "#2C3E50", 
                "background": "#FFFFFF",
                "surface": "#F8F9FA",
                "text_primary": "#2C3E50"
            }
        }
    
    def get_theme(self, name=None):
        """Get theme colors"""
        theme_name = name or self.current_theme
        return type('Theme', (), self.themes.get(theme_name, self.themes["denso_corporate"]))()
    
    def apply_theme(self, root, theme_name):
        """Apply theme to tkinter app"""
        theme = self.get_theme(theme_name)
        root.configure(bg=theme.background)
        return True
