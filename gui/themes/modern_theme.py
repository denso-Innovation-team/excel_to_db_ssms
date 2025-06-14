"""
gui/themes/modern_theme.py
Complete Modern Theme System for DENSO888 2025
Created by: Thammaphon Chittasuwanna (SDM) | Innovation Department
"""

from dataclasses import dataclass
from typing import Dict, Any, Tuple
import tkinter as tk
from tkinter import ttk


@dataclass
class ModernColors:
    """Modern color palette with enhanced design system"""

    # Primary brand colors
    primary: str = "#DC0003"
    primary_dark: str = "#B80002"
    primary_light: str = "#FF3333"
    primary_50: str = "#FEF2F2"
    primary_100: str = "#FEE2E2"
    primary_500: str = "#DC0003"
    primary_900: str = "#7F1D1D"

    # Secondary colors
    secondary: str = "#1E293B"
    secondary_dark: str = "#0F172A"
    secondary_light: str = "#334155"

    # Neutral colors (modern gray scale)
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

    # Semantic colors
    success: str = "#10B981"
    success_light: str = "#D1FAE5"
    success_dark: str = "#047857"

    warning: str = "#F59E0B"
    warning_light: str = "#FEF3C7"
    warning_dark: str = "#D97706"

    danger: str = "#EF4444"
    danger_light: str = "#FEE2E2"
    danger_dark: str = "#DC2626"

    info: str = "#3B82F6"
    info_light: str = "#DBEAFE"
    info_dark: str = "#2563EB"

    # Background colors
    background: str = "#F8FAFC"
    surface: str = "#FFFFFF"
    surface_dark: str = "#F1F5F9"
    surface_elevated: str = "#FFFFFF"

    # Text colors
    text_primary: str = "#1E293B"
    text_secondary: str = "#64748B"
    text_muted: str = "#94A3B8"
    text_inverse: str = "#FFFFFF"
    text_on_primary: str = "#FFFFFF"

    # Border colors
    border: str = "#E2E8F0"
    border_light: str = "#F1F5F9"
    border_focus: str = "#3B82F6"

    # Interactive states
    hover: str = "#F1F5F9"
    active: str = "#E2E8F0"
    focus: str = "#3B82F6"
    disabled: str = "#94A3B8"

    # Special effects
    shadow: str = "rgba(0, 0, 0, 0.1)"
    shadow_light: str = "rgba(0, 0, 0, 0.05)"
    shadow_strong: str = "rgba(0, 0, 0, 0.2)"

    # Glass morphism
    glass_bg: str = "rgba(255, 255, 255, 0.8)"
    glass_border: str = "rgba(255, 255, 255, 0.2)"


@dataclass
class ModernFonts:
    """Modern typography system"""

    # Font families
    primary_font: str = "Segoe UI"
    secondary_font: str = "Segoe UI"
    mono_font: str = "Consolas"

    # Font sizes and weights
    display_xl: Tuple[str, int, str] = ("Segoe UI", 32, "bold")
    display_lg: Tuple[str, int, str] = ("Segoe UI", 28, "bold")
    display_md: Tuple[str, int, str] = ("Segoe UI", 24, "bold")

    heading_xl: Tuple[str, int, str] = ("Segoe UI", 20, "bold")
    heading_lg: Tuple[str, int, str] = ("Segoe UI", 18, "bold")
    heading_md: Tuple[str, int, str] = ("Segoe UI", 16, "bold")
    heading_sm: Tuple[str, int, str] = ("Segoe UI", 14, "bold")
    heading_xs: Tuple[str, int, str] = ("Segoe UI", 12, "bold")

    body_xl: Tuple[str, int] = ("Segoe UI", 18)
    body_lg: Tuple[str, int] = ("Segoe UI", 16)
    body_md: Tuple[str, int] = ("Segoe UI", 14)
    body_sm: Tuple[str, int] = ("Segoe UI", 12)
    body_xs: Tuple[str, int] = ("Segoe UI", 11)

    caption_lg: Tuple[str, int] = ("Segoe UI", 12)
    caption_md: Tuple[str, int] = ("Segoe UI", 11)
    caption_sm: Tuple[str, int] = ("Segoe UI", 10)
    caption_xs: Tuple[str, int] = ("Segoe UI", 9)

    code_lg: Tuple[str, int] = ("Consolas", 14)
    code_md: Tuple[str, int] = ("Consolas", 12)
    code_sm: Tuple[str, int] = ("Consolas", 11)
    code_xs: Tuple[str, int] = ("Consolas", 10)


@dataclass
class ModernSpacing:
    """Modern spacing system based on 4px grid"""

    # Base unit (4px)
    unit: int = 4

    # Spacing scale
    xs: int = 4  # 4px
    sm: int = 8  # 8px
    md: int = 16  # 16px
    lg: int = 24  # 24px
    xl: int = 32  # 32px
    xxl: int = 48  # 48px
    xxxl: int = 64  # 64px

    # Component specific spacing
    component_padding: int = 16
    card_padding: int = 24
    section_padding: int = 32
    page_padding: int = 40


@dataclass
class ModernBorderRadius:
    """Modern border radius system"""

    none: int = 0
    sm: int = 4
    md: int = 6
    lg: int = 8
    xl: int = 12
    xxl: int = 16
    full: int = 9999


@dataclass
class ModernShadows:
    """Modern shadow system for depth"""

    sm: str = "0 1px 2px rgba(0, 0, 0, 0.05)"
    md: str = "0 4px 6px rgba(0, 0, 0, 0.07), 0 2px 4px rgba(0, 0, 0, 0.06)"
    lg: str = "0 10px 15px rgba(0, 0, 0, 0.1), 0 4px 6px rgba(0, 0, 0, 0.05)"
    xl: str = "0 20px 25px rgba(0, 0, 0, 0.1), 0 10px 10px rgba(0, 0, 0, 0.04)"
    xxl: str = "0 25px 50px rgba(0, 0, 0, 0.25)"

    # Colored shadows
    primary: str = "0 4px 14px rgba(220, 0, 3, 0.25)"
    success: str = "0 4px 14px rgba(16, 185, 129, 0.25)"
    warning: str = "0 4px 14px rgba(245, 158, 11, 0.25)"
    danger: str = "0 4px 14px rgba(239, 68, 68, 0.25)"


class ModernTheme:
    """Complete modern theme system for DENSO888"""

    def __init__(self):
        self.colors = ModernColors()
        self.fonts = ModernFonts()
        self.spacing = ModernSpacing()
        self.radius = ModernBorderRadius()
        self.shadows = ModernShadows()

        # Theme metadata
        self.name = "DENSO888 Modern"
        self.version = "2.0.0"
        self.author = "Thammaphon Chittasuwanna (SDM)"

        # Component presets
        self.button_styles = self._create_button_styles()
        self.card_styles = self._create_card_styles()
        self.input_styles = self._create_input_styles()

    def _create_button_styles(self) -> Dict[str, Dict[str, Any]]:
        """Create button style presets"""
        return {
            "primary": {
                "bg": self.colors.primary,
                "fg": self.colors.text_on_primary,
                "hover_bg": self.colors.primary_dark,
                "active_bg": self.colors.primary_light,
                "border": "none",
                "padding": (self.spacing.md, self.spacing.lg),
                "font": self.fonts.body_md + ("bold",),
                "radius": self.radius.md,
            },
            "secondary": {
                "bg": self.colors.secondary,
                "fg": self.colors.text_inverse,
                "hover_bg": self.colors.secondary_dark,
                "active_bg": self.colors.secondary_light,
                "border": "none",
                "padding": (self.spacing.md, self.spacing.lg),
                "font": self.fonts.body_md + ("bold",),
                "radius": self.radius.md,
            },
            "success": {
                "bg": self.colors.success,
                "fg": self.colors.text_inverse,
                "hover_bg": self.colors.success_dark,
                "active_bg": self.colors.success_light,
                "border": "none",
                "padding": (self.spacing.md, self.spacing.lg),
                "font": self.fonts.body_md + ("bold",),
                "radius": self.radius.md,
            },
            "warning": {
                "bg": self.colors.warning,
                "fg": self.colors.text_inverse,
                "hover_bg": self.colors.warning_dark,
                "active_bg": self.colors.warning_light,
                "border": "none",
                "padding": (self.spacing.md, self.spacing.lg),
                "font": self.fonts.body_md + ("bold",),
                "radius": self.radius.md,
            },
            "danger": {
                "bg": self.colors.danger,
                "fg": self.colors.text_inverse,
                "hover_bg": self.colors.danger_dark,
                "active_bg": self.colors.danger_light,
                "border": "none",
                "padding": (self.spacing.md, self.spacing.lg),
                "font": self.fonts.body_md + ("bold",),
                "radius": self.radius.md,
            },
            "outline": {
                "bg": "transparent",
                "fg": self.colors.text_primary,
                "hover_bg": self.colors.hover,
                "active_bg": self.colors.active,
                "border": f"1px solid {self.colors.border}",
                "padding": (self.spacing.md, self.spacing.lg),
                "font": self.fonts.body_md + ("bold",),
                "radius": self.radius.md,
            },
            "ghost": {
                "bg": "transparent",
                "fg": self.colors.text_primary,
                "hover_bg": self.colors.hover,
                "active_bg": self.colors.active,
                "border": "none",
                "padding": (self.spacing.sm, self.spacing.md),
                "font": self.fonts.body_md,
                "radius": self.radius.sm,
            },
        }

    def _create_card_styles(self) -> Dict[str, Dict[str, Any]]:
        """Create card style presets"""
        return {
            "default": {
                "bg": self.colors.surface,
                "border": f"1px solid {self.colors.border}",
                "radius": self.radius.lg,
                "padding": self.spacing.card_padding,
                "shadow": self.shadows.sm,
            },
            "elevated": {
                "bg": self.colors.surface_elevated,
                "border": "none",
                "radius": self.radius.lg,
                "padding": self.spacing.card_padding,
                "shadow": self.shadows.md,
            },
            "outlined": {
                "bg": self.colors.surface,
                "border": f"2px solid {self.colors.border}",
                "radius": self.radius.lg,
                "padding": self.spacing.card_padding,
                "shadow": "none",
            },
            "glass": {
                "bg": self.colors.glass_bg,
                "border": f"1px solid {self.colors.glass_border}",
                "radius": self.radius.lg,
                "padding": self.spacing.card_padding,
                "shadow": self.shadows.lg,
                "backdrop_filter": "blur(10px)",
            },
        }

    def _create_input_styles(self) -> Dict[str, Dict[str, Any]]:
        """Create input style presets"""
        return {
            "default": {
                "bg": self.colors.surface,
                "fg": self.colors.text_primary,
                "border": f"1px solid {self.colors.border}",
                "focus_border": f"2px solid {self.colors.focus}",
                "radius": self.radius.md,
                "padding": (self.spacing.sm, self.spacing.md),
                "font": self.fonts.body_md,
                "placeholder_color": self.colors.text_muted,
            },
            "filled": {
                "bg": self.colors.surface_dark,
                "fg": self.colors.text_primary,
                "border": "none",
                "focus_border": f"2px solid {self.colors.focus}",
                "radius": self.radius.md,
                "padding": (self.spacing.sm, self.spacing.md),
                "font": self.fonts.body_md,
                "placeholder_color": self.colors.text_muted,
            },
        }

    def apply_to_root(self, root: tk.Tk):
        """Apply theme to root window"""
        root.configure(bg=self.colors.background)

        # Configure ttk styles
        style = ttk.Style()

        # Configure modern styles
        self._configure_ttk_styles(style)

    def _configure_ttk_styles(self, style: ttk.Style):
        """Configure ttk widget styles"""
        # Button styles
        style.configure(
            "Modern.TButton",
            background=self.colors.primary,
            foreground=self.colors.text_on_primary,
            borderwidth=0,
            focuscolor="none",
            padding=(self.spacing.md, self.spacing.sm),
        )

        style.map(
            "Modern.TButton",
            background=[
                ("active", self.colors.primary_dark),
                ("pressed", self.colors.primary_light),
            ],
        )

        # Frame styles
        style.configure(
            "Card.TFrame", background=self.colors.surface, relief="flat", borderwidth=1
        )

        style.configure(
            "Sidebar.TFrame", background=self.colors.surface_dark, relief="flat"
        )

        # Entry styles
        style.configure(
            "Modern.TEntry",
            fieldbackground=self.colors.surface,
            borderwidth=1,
            insertcolor=self.colors.text_primary,
        )

        # Notebook styles
        style.configure(
            "Modern.TNotebook", background=self.colors.background, borderwidth=0
        )

        style.configure(
            "Modern.TNotebook.Tab",
            background=self.colors.surface,
            foreground=self.colors.text_primary,
            padding=(self.spacing.lg, self.spacing.md),
            borderwidth=0,
        )

        style.map(
            "Modern.TNotebook.Tab",
            background=[
                ("selected", self.colors.primary),
                ("active", self.colors.hover),
            ],
            foreground=[
                ("selected", self.colors.text_on_primary),
                ("active", self.colors.text_primary),
            ],
        )

        # Progressbar styles
        style.configure(
            "Modern.Horizontal.TProgressbar",
            background=self.colors.primary,
            troughcolor=self.colors.surface_dark,
            borderwidth=0,
            lightcolor=self.colors.primary,
            darkcolor=self.colors.primary,
        )

        # Scrollbar styles
        style.configure(
            "Modern.Vertical.TScrollbar",
            background=self.colors.surface_dark,
            troughcolor=self.colors.background,
            borderwidth=0,
            arrowcolor=self.colors.text_muted,
        )

        # Combobox styles
        style.configure(
            "Modern.TCombobox",
            fieldbackground=self.colors.surface,
            borderwidth=1,
            arrowcolor=self.colors.text_secondary,
        )

    def create_modern_button(
        self, parent, text: str, style: str = "primary", size: str = "md", **kwargs
    ) -> tk.Button:
        """Create a modern styled button"""
        button_style = self.button_styles.get(style, self.button_styles["primary"])

        # Size variations
        size_configs = {
            "xs": {"font": self.fonts.caption_md, "padding": (6, 12)},
            "sm": {"font": self.fonts.body_sm, "padding": (8, 16)},
            "md": {"font": self.fonts.body_md, "padding": (12, 20)},
            "lg": {"font": self.fonts.body_lg, "padding": (16, 24)},
            "xl": {"font": self.fonts.body_xl, "padding": (20, 32)},
        }

        size_config = size_configs.get(size, size_configs["md"])

        button = tk.Button(
            parent,
            text=text,
            font=size_config["font"],
            bg=button_style["bg"],
            fg=button_style["fg"],
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=size_config["padding"][1],
            pady=size_config["padding"][0],
            **kwargs,
        )

        # Add hover effects
        def on_enter(event):
            button.configure(bg=button_style["hover_bg"])

        def on_leave(event):
            button.configure(bg=button_style["bg"])

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

        return button

    def create_modern_card(self, parent, style: str = "default", **kwargs) -> tk.Frame:
        """Create a modern styled card"""
        card_style = self.card_styles.get(style, self.card_styles["default"])

        card = tk.Frame(
            parent,
            bg=card_style["bg"],
            relief="flat",
            bd=0,
            padx=card_style["padding"],
            pady=card_style["padding"],
            **kwargs,
        )

        return card

    def create_modern_entry(self, parent, style: str = "default", **kwargs) -> tk.Entry:
        """Create a modern styled entry"""
        entry_style = self.input_styles.get(style, self.input_styles["default"])

        entry = tk.Entry(
            parent,
            font=entry_style["font"],
            bg=entry_style["bg"],
            fg=entry_style["fg"],
            relief="solid",
            bd=1,
            **kwargs,
        )

        # Add focus effects
        def on_focus_in(event):
            entry.configure(relief="solid", bd=2)

        def on_focus_out(event):
            entry.configure(relief="solid", bd=1)

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

        return entry

    def get_color_palette(self) -> Dict[str, str]:
        """Get complete color palette as dictionary"""
        return {
            "primary": self.colors.primary,
            "primary_dark": self.colors.primary_dark,
            "primary_light": self.colors.primary_light,
            "secondary": self.colors.secondary,
            "success": self.colors.success,
            "warning": self.colors.warning,
            "danger": self.colors.danger,
            "info": self.colors.info,
            "background": self.colors.background,
            "surface": self.colors.surface,
            "text_primary": self.colors.text_primary,
            "text_secondary": self.colors.text_secondary,
            "border": self.colors.border,
        }

    def export_css_variables(self) -> str:
        """Export theme as CSS custom properties"""
        css_vars = ":root {\n"

        # Colors
        for attr_name in dir(self.colors):
            if not attr_name.startswith("_"):
                color_value = getattr(self.colors, attr_name)
                if isinstance(color_value, str) and color_value.startswith("#"):
                    css_vars += f"  --{attr_name.replace('_', '-')}: {color_value};\n"

        # Spacing
        for attr_name in dir(self.spacing):
            if not attr_name.startswith("_") and attr_name != "unit":
                spacing_value = getattr(self.spacing, attr_name)
                if isinstance(spacing_value, int):
                    css_vars += f"  --spacing-{attr_name}: {spacing_value}px;\n"

        # Border radius
        for attr_name in dir(self.radius):
            if not attr_name.startswith("_"):
                radius_value = getattr(self.radius, attr_name)
                if isinstance(radius_value, int):
                    css_vars += f"  --radius-{attr_name}: {radius_value}px;\n"

        css_vars += "}\n"
        return css_vars


# Theme instances
default_theme = ModernTheme()


# Color constants for backward compatibility
class ThemeColors:
    """Backward compatible color class"""

    def __init__(self):
        theme = default_theme
        self.primary = theme.colors.primary
        self.primary_dark = theme.colors.primary_dark
        self.primary_light = theme.colors.primary_light
        self.secondary = theme.colors.secondary
        self.success = theme.colors.success
        self.warning = theme.colors.warning
        self.danger = theme.colors.danger
        self.info = theme.colors.info
        self.background = theme.colors.background
        self.surface = theme.colors.surface
        self.surface_dark = theme.colors.surface_dark
        self.text_primary = theme.colors.text_primary
        self.text_secondary = theme.colors.text_secondary
        self.text_muted = theme.colors.text_muted
        self.border = theme.colors.border


# Export commonly used items
__all__ = [
    "ModernTheme",
    "ModernColors",
    "ModernFonts",
    "ModernSpacing",
    "ModernBorderRadius",
    "ModernShadows",
    "ThemeColors",
    "default_theme",
]
