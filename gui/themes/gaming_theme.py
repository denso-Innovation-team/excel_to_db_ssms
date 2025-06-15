"""
gui/themes/gaming_theme.py
Gaming-Inspired UI Theme for DENSO888
เพิ่มความน่าเล่นแบบเกมให้กับระบบ
"""

from dataclasses import dataclass
from typing import Dict
import tkinter as tk
import math
import threading
import time


@dataclass
class GamingColors:
    """Gaming color palette with neon accents"""

    # DENSO brand colors with gaming twist
    primary: str = "#FF0066"  # Neon pink DENSO
    primary_glow: str = "#FF3388"
    primary_dark: str = "#CC0044"

    # Gaming accent colors
    neon_blue: str = "#00FFFF"
    neon_green: str = "#00FF88"
    neon_purple: str = "#8866FF"
    neon_orange: str = "#FF8800"

    # Dark gaming backgrounds
    bg_primary: str = "#0A0A0F"
    bg_secondary: str = "#151521"
    bg_card: str = "#1A1A2E"
    bg_elevated: str = "#16213E"

    # Gaming UI elements
    border_glow: str = "#00FFFF"
    text_primary: str = "#FFFFFF"
    text_secondary: str = "#CCCCCC"
    text_accent: str = "#00FFFF"
    text_success: str = "#00FF88"
    text_warning: str = "#FFB800"
    text_error: str = "#FF4466"

    # Achievement colors
    gold: str = "#FFD700"
    silver: str = "#C0C0C0"
    bronze: str = "#CD7F32"

    # Progress bars
    progress_bg: str = "#2A2A3E"
    progress_fill: str = "#00FF88"
    progress_glow: str = "#88FFB8"


class GamingAnimations:
    """Gaming-style animations and effects"""

    @staticmethod
    def pulse_effect(
        widget, color_normal: str, color_highlight: str, duration: float = 1.0
    ):
        """Pulse animation for important elements"""

        def animate():
            steps = 30
            for i in range(steps):
                # Calculate pulse intensity using sine wave
                intensity = (math.sin(i * 2 * math.pi / steps) + 1) / 2

                # Interpolate between colors
                if widget.winfo_exists():
                    try:
                        widget.configure(
                            bg=color_highlight if intensity > 0.5 else color_normal
                        )
                        time.sleep(duration / steps)
                    except:
                        break
                else:
                    break

        threading.Thread(target=animate, daemon=True).start()

    @staticmethod
    def glow_on_hover(widget, normal_bg: str, glow_bg: str):
        """Add glow effect on hover"""

        def on_enter(event):
            widget.configure(bg=glow_bg)

        def on_leave(event):
            widget.configure(bg=normal_bg)

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    @staticmethod
    def typewriter_effect(text_widget, text: str, delay: float = 0.05):
        """Typewriter effect for text display"""

        def animate():
            text_widget.delete("1.0", tk.END)
            for i, char in enumerate(text):
                if text_widget.winfo_exists():
                    try:
                        text_widget.insert(tk.END, char)
                        text_widget.see(tk.END)
                        text_widget.update()
                        time.sleep(delay)
                    except:
                        break
                else:
                    break

        threading.Thread(target=animate, daemon=True).start()


class GamingComponents:
    """Gaming-style UI components"""

    def __init__(self, colors: GamingColors):
        self.colors = colors

    def create_neon_button(
        self,
        parent,
        text: str,
        command=None,
        style: str = "primary",
        size: str = "medium",
    ) -> tk.Button:
        """Create neon-style gaming button"""

        style_configs = {
            "primary": {
                "bg": self.colors.primary,
                "fg": self.colors.text_primary,
                "glow": self.colors.primary_glow,
            },
            "success": {
                "bg": self.colors.neon_green,
                "fg": self.colors.bg_primary,
                "glow": "#88FFB8",
            },
            "warning": {
                "bg": self.colors.neon_orange,
                "fg": self.colors.bg_primary,
                "glow": "#FFAA44",
            },
            "info": {
                "bg": self.colors.neon_blue,
                "fg": self.colors.bg_primary,
                "glow": "#44FFFF",
            },
        }

        size_configs = {
            "small": {"font": ("Orbitron", 10, "bold"), "padx": 15, "pady": 8},
            "medium": {"font": ("Orbitron", 12, "bold"), "padx": 20, "pady": 10},
            "large": {"font": ("Orbitron", 14, "bold"), "padx": 25, "pady": 12},
        }

        style_config = style_configs.get(style, style_configs["primary"])
        size_config = size_configs.get(size, size_configs["medium"])

        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=size_config["font"],
            bg=style_config["bg"],
            fg=style_config["fg"],
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=size_config["padx"],
            pady=size_config["pady"],
        )

        # Add glow effect
        GamingAnimations.glow_on_hover(button, style_config["bg"], style_config["glow"])

        return button

    def create_gaming_card(
        self, parent, title: str = "", subtitle: str = "", **kwargs
    ) -> tk.Frame:
        """Create gaming-style card with neon borders"""

        card_frame = tk.Frame(
            parent,
            bg=self.colors.bg_card,
            relief="flat",
            bd=2,
            highlightbackground=self.colors.border_glow,
            highlightthickness=1,
            **kwargs,
        )

        if title:
            header_frame = tk.Frame(card_frame, bg=self.colors.bg_card)
            header_frame.pack(fill="x", padx=15, pady=(15, 10))

            title_label = tk.Label(
                header_frame,
                text=title,
                font=("Orbitron", 14, "bold"),
                bg=self.colors.bg_card,
                fg=self.colors.text_accent,
            )
            title_label.pack(anchor="w")

            if subtitle:
                subtitle_label = tk.Label(
                    header_frame,
                    text=subtitle,
                    font=("Segoe UI", 10),
                    bg=self.colors.bg_card,
                    fg=self.colors.text_secondary,
                )
                subtitle_label.pack(anchor="w")

        return card_frame

    def create_progress_bar(self, parent, width: int = 300, height: int = 20) -> Dict:
        """Create gaming-style progress bar with glow effect"""

        container = tk.Frame(parent, bg=self.colors.bg_primary)

        # Background bar
        bg_canvas = tk.Canvas(
            container,
            width=width,
            height=height,
            bg=self.colors.progress_bg,
            highlightthickness=0,
        )
        bg_canvas.pack()

        # Progress fill
        progress_canvas = tk.Canvas(
            container,
            width=width,
            height=height,
            bg=self.colors.progress_bg,
            highlightthickness=0,
        )
        progress_canvas.place(x=0, y=0)

        # Progress text
        text_label = tk.Label(
            container,
            text="0%",
            font=("Orbitron", 10, "bold"),
            bg=self.colors.progress_bg,
            fg=self.colors.text_primary,
        )
        text_label.place(x=width // 2, y=height // 2, anchor="center")

        def update_progress(value: float):
            """Update progress (0-100)"""
            if 0 <= value <= 100:
                fill_width = int(width * value / 100)
                progress_canvas.delete("all")

                if fill_width > 0:
                    # Main progress bar
                    progress_canvas.create_rectangle(
                        0,
                        0,
                        fill_width,
                        height,
                        fill=self.colors.progress_fill,
                        outline="",
                    )

                    # Glow effect
                    if fill_width > 10:
                        progress_canvas.create_rectangle(
                            0,
                            2,
                            fill_width,
                            height - 2,
                            fill=self.colors.progress_glow,
                            outline="",
                        )

                text_label.configure(text=f"{value:.1f}%")

        return {
            "container": container,
            "update": update_progress,
            "canvas": progress_canvas,
            "text": text_label,
        }

    def create_stat_display(
        self, parent, icon: str, label: str, value: str, color: str = None
    ) -> tk.Frame:
        """Create gaming-style stat display"""

        if color is None:
            color = self.colors.text_accent

        stat_frame = tk.Frame(
            parent,
            bg=self.colors.bg_elevated,
            relief="flat",
            bd=1,
            highlightbackground=color,
            highlightthickness=1,
            padx=15,
            pady=10,
        )

        # Icon
        icon_label = tk.Label(
            stat_frame,
            text=icon,
            font=("Segoe UI", 24),
            bg=self.colors.bg_elevated,
            fg=color,
        )
        icon_label.pack()

        # Value
        value_label = tk.Label(
            stat_frame,
            text=value,
            font=("Orbitron", 18, "bold"),
            bg=self.colors.bg_elevated,
            fg=self.colors.text_primary,
        )
        value_label.pack()

        # Label
        label_label = tk.Label(
            stat_frame,
            text=label,
            font=("Segoe UI", 10),
            bg=self.colors.bg_elevated,
            fg=self.colors.text_secondary,
        )
        label_label.pack()

        # Store references for updates
        stat_frame.value_label = value_label
        stat_frame.icon_label = icon_label

        return stat_frame

    def create_notification_toast(
        self, parent, message: str, toast_type: str = "info", duration: int = 3000
    ):
        """Create gaming-style notification toast"""

        type_configs = {
            "success": {
                "bg": self.colors.neon_green,
                "fg": self.colors.bg_primary,
                "icon": "✅",
            },
            "warning": {
                "bg": self.colors.neon_orange,
                "fg": self.colors.bg_primary,
                "icon": "⚠️",
            },
            "error": {
                "bg": self.colors.text_error,
                "fg": self.colors.text_primary,
                "icon": "❌",
            },
            "info": {
                "bg": self.colors.neon_blue,
                "fg": self.colors.bg_primary,
                "icon": "ℹ️",
            },
        }

        config = type_configs.get(toast_type, type_configs["info"])

        # Create toast window
        toast = tk.Toplevel(parent)
        toast.withdraw()
        toast.overrideredirect(True)
        toast.attributes("-topmost", True)

        # Toast frame
        toast_frame = tk.Frame(
            toast,
            bg=config["bg"],
            padx=20,
            pady=15,
            relief="flat",
            bd=2,
            highlightbackground=self.colors.border_glow,
            highlightthickness=1,
        )
        toast_frame.pack()

        # Content
        content_frame = tk.Frame(toast_frame, bg=config["bg"])
        content_frame.pack()

        # Icon
        icon_label = tk.Label(
            content_frame,
            text=config["icon"],
            font=("Segoe UI", 16),
            bg=config["bg"],
            fg=config["fg"],
        )
        icon_label.pack(side="left", padx=(0, 10))

        # Message
        message_label = tk.Label(
            content_frame,
            text=message,
            font=("Orbitron", 11, "bold"),
            bg=config["bg"],
            fg=config["fg"],
            wraplength=300,
        )
        message_label.pack(side="left")

        # Position toast
        toast.update_idletasks()
        width = toast.winfo_reqwidth()
        height = toast.winfo_reqheight()

        screen_width = toast.winfo_screenwidth()
        x = screen_width - width - 20
        y = 50

        toast.geometry(f"{width}x{height}+{x}+{y}")
        toast.deiconify()

        # Auto-hide
        def hide_toast():
            try:
                if toast.winfo_exists():
                    toast.destroy()
            except:
                pass

        toast.after(duration, hide_toast)

        # Add pulse effect
        GamingAnimations.pulse_effect(
            toast_frame, config["bg"], self.colors.border_glow, 0.5
        )


class GamingTheme:
    """Complete gaming theme for DENSO888"""

    def __init__(self):
        self.colors = GamingColors()
        self.animations = GamingAnimations()
        self.components = GamingComponents(self.colors)

        # Theme metadata
        self.name = "DENSO888 Gaming Edition"
        self.version = "2.0.0"
        self.style = "Cyberpunk Gaming"

    def apply_to_root(self, root: tk.Tk):
        """Apply gaming theme to root window"""
        root.configure(bg=self.colors.bg_primary)

        # Configure window properties
        try:
            # Try to make window look more gaming-like
            root.attributes("-alpha", 0.98)  # Slight transparency
        except:
            pass

    def create_gaming_sidebar(self, parent, items: list, callback) -> tk.Frame:
        """Create gaming-style sidebar with neon effects"""

        sidebar = tk.Frame(
            parent,
            bg=self.colors.bg_secondary,
            width=280,
            relief="flat",
            bd=0,
            highlightbackground=self.colors.border_glow,
            highlightthickness=1,
        )
        sidebar.pack_propagate(False)

        # Sidebar header
        header_frame = tk.Frame(sidebar, bg=self.colors.bg_secondary, height=100)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        # Gaming logo/title
        logo_frame = tk.Frame(header_frame, bg=self.colors.bg_secondary)
        logo_frame.pack(expand=True)

        logo_label = tk.Label(
            logo_frame,
            text="🏭 DENSO888",
            font=("Orbitron", 16, "bold"),
            bg=self.colors.bg_secondary,
            fg=self.colors.primary,
        )
        logo_label.pack(pady=10)

        subtitle_label = tk.Label(
            logo_frame,
            text="GAMING EDITION",
            font=("Orbitron", 8, "bold"),
            bg=self.colors.bg_secondary,
            fg=self.colors.neon_blue,
        )
        subtitle_label.pack()

        # Menu items
        menu_frame = tk.Frame(sidebar, bg=self.colors.bg_secondary)
        menu_frame.pack(fill="both", expand=True, padx=10)

        for item in items:
            self._create_sidebar_item(menu_frame, item, callback)

        return sidebar

    def _create_sidebar_item(self, parent, item: dict, callback):
        """Create individual sidebar menu item"""

        item_frame = tk.Frame(parent, bg=self.colors.bg_secondary)
        item_frame.pack(fill="x", pady=2)

        button = tk.Button(
            item_frame,
            text="",
            bg=self.colors.bg_secondary,
            fg=self.colors.text_primary,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda: callback(item.get("id", "")),
            anchor="w",
            padx=15,
            pady=12,
        )
        button.pack(fill="x")

        # Button content
        content_frame = tk.Frame(button, bg=self.colors.bg_secondary)
        content_frame.pack(fill="x")

        # Icon
        icon_label = tk.Label(
            content_frame,
            text=item.get("icon", "•"),
            font=("Segoe UI", 16),
            bg=self.colors.bg_secondary,
            fg=item.get("color", self.colors.neon_blue),
        )
        icon_label.pack(side="left", padx=(0, 10))

        # Text container
        text_frame = tk.Frame(content_frame, bg=self.colors.bg_secondary)
        text_frame.pack(side="left", fill="x", expand=True)

        # Title
        title_label = tk.Label(
            text_frame,
            text=item.get("title", "Menu Item"),
            font=("Orbitron", 11, "bold"),
            bg=self.colors.bg_secondary,
            fg=self.colors.text_primary,
            anchor="w",
        )
        title_label.pack(fill="x")

        # Description
        if item.get("description"):
            desc_label = tk.Label(
                text_frame,
                text=item.get("description", ""),
                font=("Segoe UI", 9),
                bg=self.colors.bg_secondary,
                fg=self.colors.text_secondary,
                anchor="w",
            )
            desc_label.pack(fill="x")

        # Badge
        if item.get("badge"):
            badge_label = tk.Label(
                content_frame,
                text=item.get("badge", "").upper(),
                font=("Orbitron", 8, "bold"),
                bg=self.colors.neon_green,
                fg=self.colors.bg_primary,
                padx=6,
                pady=2,
            )
            badge_label.pack(side="right")

        # Hover effects
        def on_enter(event):
            button.configure(bg=self.colors.bg_elevated)
            content_frame.configure(bg=self.colors.bg_elevated)
            icon_label.configure(bg=self.colors.bg_elevated)
            text_frame.configure(bg=self.colors.bg_elevated)
            title_label.configure(
                bg=self.colors.bg_elevated, fg=item.get("color", self.colors.neon_blue)
            )
            if "desc_label" in locals():
                desc_label.configure(bg=self.colors.bg_elevated)

        def on_leave(event):
            button.configure(bg=self.colors.bg_secondary)
            content_frame.configure(bg=self.colors.bg_secondary)
            icon_label.configure(bg=self.colors.bg_secondary)
            text_frame.configure(bg=self.colors.bg_secondary)
            title_label.configure(
                bg=self.colors.bg_secondary, fg=self.colors.text_primary
            )
            if "desc_label" in locals():
                desc_label.configure(bg=self.colors.bg_secondary)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def create_gaming_header(self, parent, title: str, subtitle: str = "") -> tk.Frame:
        """Create gaming-style header with animated elements"""

        header = tk.Frame(
            parent,
            bg=self.colors.bg_primary,
            height=80,
            relief="flat",
            bd=0,
            highlightbackground=self.colors.primary,
            highlightthickness=2,
        )
        header.pack_propagate(False)

        # Header content
        content_frame = tk.Frame(header, bg=self.colors.bg_primary)
        content_frame.pack(expand=True, fill="both")

        # Title with glow effect
        title_label = tk.Label(
            content_frame,
            text=title,
            font=("Orbitron", 20, "bold"),
            bg=self.colors.bg_primary,
            fg=self.colors.primary,
        )
        title_label.pack(pady=(15, 5))

        if subtitle:
            subtitle_label = tk.Label(
                content_frame,
                text=subtitle,
                font=("Segoe UI", 12),
                bg=self.colors.bg_primary,
                fg=self.colors.text_secondary,
            )
            subtitle_label.pack()

        # Add pulse animation to title
        GamingAnimations.pulse_effect(
            title_label, self.colors.primary, self.colors.primary_glow, 2.0
        )

        return header

    def create_achievement_popup(
        self, parent, title: str, description: str, achievement_type: str = "gold"
    ):
        """Create achievement notification popup"""

        colors_map = {
            "gold": self.colors.gold,
            "silver": self.colors.silver,
            "bronze": self.colors.bronze,
        }

        achievement_color = colors_map.get(achievement_type, self.colors.gold)

        # Create popup window
        popup = tk.Toplevel(parent)
        popup.withdraw()
        popup.overrideredirect(True)
        popup.attributes("-topmost", True)

        # Main frame
        main_frame = tk.Frame(
            popup,
            bg=self.colors.bg_card,
            padx=20,
            pady=15,
            relief="flat",
            bd=2,
            highlightbackground=achievement_color,
            highlightthickness=2,
        )
        main_frame.pack()

        # Achievement content
        content_frame = tk.Frame(main_frame, bg=self.colors.bg_card)
        content_frame.pack()

        # Achievement icon
        icon_label = tk.Label(
            content_frame,
            text="🏆",
            font=("Segoe UI", 32),
            bg=self.colors.bg_card,
            fg=achievement_color,
        )
        icon_label.pack()

        # Achievement text
        title_label = tk.Label(
            content_frame,
            text="ACHIEVEMENT UNLOCKED!",
            font=("Orbitron", 10, "bold"),
            bg=self.colors.bg_card,
            fg=achievement_color,
        )
        title_label.pack()

        name_label = tk.Label(
            content_frame,
            text=title,
            font=("Orbitron", 14, "bold"),
            bg=self.colors.bg_card,
            fg=self.colors.text_primary,
        )
        name_label.pack(pady=(5, 0))

        desc_label = tk.Label(
            content_frame,
            text=description,
            font=("Segoe UI", 10),
            bg=self.colors.bg_card,
            fg=self.colors.text_secondary,
            wraplength=250,
        )
        desc_label.pack(pady=(5, 0))

        # Position popup (center of screen)
        popup.update_idletasks()
        width = popup.winfo_reqwidth()
        height = popup.winfo_reqheight()

        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2 - 100

        popup.geometry(f"{width}x{height}+{x}+{y}")
        popup.deiconify()

        # Animate popup
        GamingAnimations.pulse_effect(
            main_frame, self.colors.bg_card, achievement_color, 1.0
        )

        # Auto-hide after 4 seconds
        def hide_popup():
            try:
                if popup.winfo_exists():
                    popup.destroy()
            except:
                pass

        popup.after(4000, hide_popup)


# Create global gaming theme instance
gaming_theme = GamingTheme()
