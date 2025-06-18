"""
gui/themes/__init__.py
Theme System Initialization
"""

import sys
from pathlib import Path

# Add parent paths
sys.path.append(str(Path(__file__).parent.parent.parent))

__all__ = ["modern_theme", "apply_modern_style", "get_theme_colors", "get_theme_fonts"]

try:
    from .modern_theme import (
        modern_theme,
        apply_modern_style,
        get_theme_colors,
        get_theme_fonts,
    )
except ImportError as e:
    # Fallback theme if import fails
    class FallbackTheme:
        class colors:
            primary = "#2563EB"
            surface = "#FFFFFF"
            text_primary = "#1F2937"
            text_secondary = "#6B7280"
            success = "#059669"
            error = "#DC2626"

        class spacing:
            sidebar_width = 280
            header_height = 64

        class fonts:
            def get(self, key):
                return ("Segoe UI", 11)

    modern_theme = FallbackTheme()

    def apply_modern_style(widget, style_type="default"):
        """Fallback theme application"""
        pass

    def get_theme_colors():
        return modern_theme.colors

    def get_theme_fonts():
        return modern_theme.fonts

    print(f"Warning: Theme import failed ({e}), using fallback theme")
