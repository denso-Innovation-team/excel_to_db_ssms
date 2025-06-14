"""
gui/themes/theme_manager.py
Modern Theme Manager with DENSO Branding & Advanced Effects
"""

import json
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass
import colorsys


@dataclass
class ColorPalette:
    """Modern color palette with accessibility support"""

    primary: str
    primary_dark: str
    primary_light: str
    secondary: str
    accent: str
    success: str
    warning: str
    danger: str
    background: str
    surface: str
    text_primary: str
    text_secondary: str
    border: str
    shadow: str

    def to_dict(self) -> Dict[str, str]:
        return {k: v for k, v in self.__dict__.items()}


class ModernThemeManager:
    """Advanced theme manager with animation and effects"""

    def __init__(self):
        self.themes_dir = Path("assets/themes")
        self.themes_dir.mkdir(parents=True, exist_ok=True)
        self.current_theme = "denso_corporate"
        self.themes: Dict[str, ColorPalette] = {}
        self.style: Optional[ttk.Style] = None
        self._load_built_in_themes()

    def _load_built_in_themes(self):
        """Load built-in DENSO themes"""

        # DENSO Corporate Theme - Professional Red
        self.themes["denso_corporate"] = ColorPalette(
            primary="#DC0003",  # DENSO Red
            primary_dark="#B80002",  # Darker red for depth
            primary_light="#FF1F22",  # Lighter red for highlights
            secondary="#2C3E50",  # Dark blue-grey
            accent="#E74C3C",  # Accent red
            success="#27AE60",  # Success green
            warning="#F39C12",  # Warning orange
            danger="#E74C3C",  # Error red
            background="#FFFFFF",  # Clean white
            surface="#F8F9FA",  # Light grey surface
            text_primary="#2C3E50",  # Dark text
            text_secondary="#7F8C8D",  # Grey text
            border="#E5E8EB",  # Light border
            shadow="rgba(44, 62, 80, 0.1)",  # Subtle shadow
        )

        # Dark Premium Theme - Modern Dark
        self.themes["dark_premium"] = ColorPalette(
            primary="#6366F1",  # Indigo
            primary_dark="#4F46E5",  # Dark indigo
            primary_light="#8B5CF6",  # Purple
            secondary="#1F2937",  # Dark grey
            accent="#F59E0B",  # Amber
            success="#10B981",  # Emerald
            warning="#F59E0B",  # Amber warning
            danger="#EF4444",  # Red
            background="#111827",  # Very dark
            surface="#1F2937",  # Dark surface
            text_primary="#F9FAFB",  # Light text
            text_secondary="#D1D5DB",  # Grey text
            border="#374151",  # Dark border
            shadow="rgba(0, 0, 0, 0.3)",  # Dark shadow
        )

        # Ocean Blue Theme - Fresh & Clean
        self.themes["ocean_blue"] = ColorPalette(
            primary="#0EA5E9",  # Sky blue
            primary_dark="#0284C7",  # Dark blue
            primary_light="#38BDF8",  # Light blue
            secondary="#1E293B",  # Slate grey
            accent="#06B6D4",  # Cyan
            success="#22C55E",  # Green
            warning="#F59E0B",  # Amber
            danger="#EF4444",  # Red
            background="#F8FAFC",  # Very light blue
            surface="#FFFFFF",  # White
            text_primary="#1E293B",  # Dark slate
            text_secondary="#64748B",  # Slate
            border="#E2E8F0",  # Light border
            shadow="rgba(30, 41, 59, 0.1)",  # Blue shadow
        )

        # Innovation Theme - Modern Gradient
        self.themes["innovation"] = ColorPalette(
            primary="#8B5CF6",  # Purple
            primary_dark="#7C3AED",  # Dark purple
            primary_light="#A78BFA",  # Light purple
            secondary="#0F172A",  # Very dark
            accent="#14B8A6",  # Teal
            success="#22C55E",  # Green
            warning="#EAB308",  # Yellow
            danger="#EF4444",  # Red
            background="#FAFBFF",  # Light purple tint
            surface="#FFFFFF",  # White
            text_primary="#0F172A",  # Very dark
            text_secondary="#475569",  # Slate
            border="#E2E8F0",  # Light border
            shadow="rgba(139, 92, 246, 0.1)",  # Purple shadow
        )

    def apply_theme(self, theme_name: str, root: tk.Tk) -> bool:
        """Apply theme with modern effects"""
        if theme_name not in self.themes:
            return False

        self.current_theme = theme_name
        palette = self.themes[theme_name]

        # Initialize ttk.Style
        if not self.style:
            self.style = ttk.Style()

        # Configure modern styles
        self._configure_modern_styles(palette)

        # Apply to root window
        self._apply_root_styles(root, palette)

        return True

    def _configure_modern_styles(self, palette: ColorPalette):
        """Configure TTK styles with modern effects"""

        # Configure modern button styles
        self.style.configure(
            "Modern.TButton",
            background=palette.primary,
            foreground="white",
            borderwidth=0,
            focuscolor="none",
            padding=(15, 10),
            font=("Segoe UI", 10, "normal"),
        )

        self.style.map(
            "Modern.TButton",
            background=[
                ("active", palette.primary_light),
                ("pressed", palette.primary_dark),
                ("disabled", palette.border),
            ],
            foreground=[("disabled", palette.text_secondary)],
        )

        # Primary button with gradient effect
        self.style.configure(
            "Primary.TButton",
            background=palette.primary,
            foreground="white",
            borderwidth=0,
            relief="flat",
            padding=(20, 12),
            font=("Segoe UI", 11, "bold"),
        )

        # Success button
        self.style.configure(
            "Success.TButton",
            background=palette.success,
            foreground="white",
            borderwidth=0,
            padding=(15, 10),
        )

        # Danger button
        self.style.configure(
            "Danger.TButton",
            background=palette.danger,
            foreground="white",
            borderwidth=0,
            padding=(15, 10),
        )

        # Modern frame styles
        self.style.configure(
            "Modern.TFrame",
            background=palette.surface,
            borderwidth=1,
            relief="solid",
            bordercolor=palette.border,
        )

        # Glass effect frame
        self.style.configure(
            "Glass.TFrame",
            background=palette.surface,
            borderwidth=1,
            relief="solid",
            bordercolor=palette.border,
        )

        # Modern label styles
        self.style.configure(
            "Title.TLabel",
            background=palette.surface,
            foreground=palette.text_primary,
            font=("Segoe UI", 18, "bold"),
        )

        self.style.configure(
            "Heading.TLabel",
            background=palette.surface,
            foreground=palette.text_primary,
            font=("Segoe UI", 14, "bold"),
        )

        self.style.configure(
            "Body.TLabel",
            background=palette.surface,
            foreground=palette.text_primary,
            font=("Segoe UI", 10, "normal"),
        )

        self.style.configure(
            "Caption.TLabel",
            background=palette.surface,
            foreground=palette.text_secondary,
            font=("Segoe UI", 9, "normal"),
        )

        # Modern entry styles
        self.style.configure(
            "Modern.TEntry",
            borderwidth=1,
            relief="solid",
            bordercolor=palette.border,
            padding=(10, 8),
            font=("Segoe UI", 10),
        )

        self.style.map(
            "Modern.TEntry",
            bordercolor=[("focus", palette.primary), ("active", palette.primary_light)],
        )

        # Modern combobox
        self.style.configure(
            "Modern.TCombobox",
            borderwidth=1,
            relief="solid",
            bordercolor=palette.border,
            arrowcolor=palette.text_secondary,
            padding=(10, 8),
        )

        # Modern progressbar
        self.style.configure(
            "Modern.Horizontal.TProgressbar",
            background=palette.primary,
            troughcolor=palette.border,
            borderwidth=0,
            lightcolor=palette.primary_light,
            darkcolor=palette.primary_dark,
        )

        # Modern notebook (tabs)
        self.style.configure(
            "Modern.TNotebook", background=palette.surface, borderwidth=0
        )

        self.style.configure(
            "Modern.TNotebook.Tab",
            background=palette.background,
            foreground=palette.text_secondary,
            padding=(15, 10),
            font=("Segoe UI", 10),
            borderwidth=0,
        )

        self.style.map(
            "Modern.TNotebook.Tab",
            background=[("selected", palette.surface), ("active", palette.border)],
            foreground=[
                ("selected", palette.text_primary),
                ("active", palette.primary),
            ],
        )

        # Modern separator
        self.style.configure("Modern.TSeparator", background=palette.border)

        # Modern checkbutton
        self.style.configure(
            "Modern.TCheckbutton",
            background=palette.surface,
            foreground=palette.text_primary,
            focuscolor="none",
            font=("Segoe UI", 10),
        )

        # Modern radiobutton
        self.style.configure(
            "Modern.TRadiobutton",
            background=palette.surface,
            foreground=palette.text_primary,
            focuscolor="none",
            font=("Segoe UI", 10),
        )

    def _apply_root_styles(self, root: tk.Tk, palette: ColorPalette):
        """Apply styles to root window"""
        root.configure(bg=palette.background)

        # Configure default fonts
        default_font = ("Segoe UI", 10)
        root.option_add("*Font", default_font)

        # Configure selection colors
        root.option_add("*selectBackground", palette.primary)
        root.option_add("*selectForeground", "white")

    def create_gradient_frame(
        self,
        parent,
        width: int,
        height: int,
        colors: tuple,
        direction: str = "vertical",
    ) -> tk.Canvas:
        """Create gradient background frame"""
        canvas = tk.Canvas(parent, width=width, height=height, highlightthickness=0)

        # Calculate gradient steps
        steps = 100
        color1 = colors[0]
        color2 = colors[1]

        # Convert hex to RGB
        rgb1 = self._hex_to_rgb(color1)
        rgb2 = self._hex_to_rgb(color2)

        # Create gradient
        for i in range(steps):
            ratio = i / steps
            r = int(rgb1[0] + (rgb2[0] - rgb1[0]) * ratio)
            g = int(rgb1[1] + (rgb2[1] - rgb1[1]) * ratio)
            b = int(rgb1[2] + (rgb2[2] - rgb1[2]) * ratio)

            color = f"#{r:02x}{g:02x}{b:02x}"

            if direction == "vertical":
                y1 = int(height * i / steps)
                y2 = int(height * (i + 1) / steps)
                canvas.create_rectangle(0, y1, width, y2, fill=color, outline="")
            else:  # horizontal
                x1 = int(width * i / steps)
                x2 = int(width * (i + 1) / steps)
                canvas.create_rectangle(x1, 0, x2, height, fill=color, outline="")

        return canvas

    def _hex_to_rgb(self, hex_color: str) -> tuple:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    def create_glass_effect(self, parent, **kwargs) -> tk.Frame:
        """Create glass morphism effect frame"""
        palette = self.themes[self.current_theme]

        frame = tk.Frame(
            parent, bg=palette.surface, relief="flat", borderwidth=1, **kwargs
        )

        # Add subtle border for glass effect
        frame.configure(highlightbackground=palette.border, highlightthickness=1)

        return frame

    def create_neumorphic_button(
        self, parent, text: str, command=None, **kwargs
    ) -> tk.Button:
        """Create neumorphic design button"""
        palette = self.themes[self.current_theme]

        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=palette.surface,
            fg=palette.text_primary,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            pady=12,
            padx=20,
            **kwargs,
        )

        # Add hover effects
        def on_enter(e):
            button.configure(bg=palette.primary, fg="white")

        def on_leave(e):
            button.configure(bg=palette.surface, fg=palette.text_primary)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

        return button

    def get_accent_colors(self, base_color: str, count: int = 5) -> list:
        """Generate accent color palette from base color"""
        # Convert hex to HSV
        rgb = self._hex_to_rgb(base_color)
        hsv = colorsys.rgb_to_hsv(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)

        colors = []
        for i in range(count):
            # Vary saturation and value
            s = max(0.3, hsv[1] - 0.1 * i)
            v = min(1.0, hsv[2] + 0.1 * i)

            rgb_new = colorsys.hsv_to_rgb(hsv[0], s, v)
            hex_color = "#{:02x}{:02x}{:02x}".format(
                int(rgb_new[0] * 255), int(rgb_new[1] * 255), int(rgb_new[2] * 255)
            )
            colors.append(hex_color)

        return colors

    def save_custom_theme(self, name: str, palette: ColorPalette):
        """Save custom theme to file"""
        theme_file = self.themes_dir / f"{name}.json"
        theme_data = {
            "name": name,
            "colors": palette.to_dict(),
            "created_by": "DENSO888 Theme Creator",
        }

        with open(theme_file, "w", encoding="utf-8") as f:
            json.dump(theme_data, f, indent=2, ensure_ascii=False)

        self.themes[name] = palette

    def load_custom_theme(self, file_path: str) -> bool:
        """Load custom theme from file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                theme_data = json.load(f)

            colors = theme_data["colors"]
            palette = ColorPalette(**colors)

            theme_name = theme_data.get("name", Path(file_path).stem)
            self.themes[theme_name] = palette

            return True
        except Exception as e:
            print(f"Failed to load theme: {e}")
            return False

    def get_available_themes(self) -> Dict[str, str]:
        """Get list of available themes with descriptions"""
        return {
            "denso_corporate": "DENSO Corporate - Professional red theme",
            "dark_premium": "Dark Premium - Modern dark interface",
            "ocean_blue": "Ocean Blue - Fresh and clean design",
            "innovation": "Innovation - Creative purple gradient",
        }

    def get_current_palette(self) -> ColorPalette:
        """Get current theme palette"""
        return self.themes[self.current_theme]

    def create_animated_hover_button(self, parent, text: str, command=None) -> tk.Label:
        """Create button with smooth hover animation"""
        palette = self.themes[self.current_theme]

        # Use Label for more control over appearance
        button = tk.Label(
            parent,
            text=text,
            bg=palette.surface,
            fg=palette.text_primary,
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
            pady=15,
            padx=25,
            relief="flat",
        )

        # Animation variables
        button._hover_job = None
        button._current_bg = palette.surface
        button._target_bg = palette.primary

        def animate_color(widget, current, target, steps=10, step=0):
            if step >= steps:
                widget.configure(bg=target)
                return

            # Interpolate between colors
            current_rgb = self._hex_to_rgb(current)
            target_rgb = self._hex_to_rgb(target)

            ratio = step / steps
            new_rgb = tuple(
                int(current_rgb[i] + (target_rgb[i] - current_rgb[i]) * ratio)
                for i in range(3)
            )

            new_color = "#{:02x}{:02x}{:02x}".format(*new_rgb)
            widget.configure(bg=new_color)

            # Schedule next frame
            widget.after(
                20, lambda: animate_color(widget, current, target, steps, step + 1)
            )

        def on_enter(e):
            if button._hover_job:
                button.after_cancel(button._hover_job)
            animate_color(button, button._current_bg, palette.primary)
            button.configure(fg="white")
            button._current_bg = palette.primary

        def on_leave(e):
            if button._hover_job:
                button.after_cancel(button._hover_job)
            animate_color(button, button._current_bg, palette.surface)
            button.configure(fg=palette.text_primary)
            button._current_bg = palette.surface

        def on_click(e):
            if command:
                command()

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        button.bind("<Button-1>", on_click)

        return button
