"""
gui/themes/gaming_theme.py
Fixed Gaming-Inspired UI Theme for DENSO888
"""

from dataclasses import dataclass
import tkinter as tk
import math
import threading
import time


@dataclass
class GamingColors:
    """Gaming color palette with neon accents"""

    # DENSO brand colors with gaming twist
    primary: str = "#FF0066"
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


class GamingAnimations:
    """Gaming-style animations and effects"""

    @staticmethod
    def pulse_effect(
        widget, color_normal: str, color_highlight: str, duration: float = 1.0
    ):
        """Pulse animation for important elements"""

        def animate():
            try:
                steps = 30
                for i in range(steps):
                    if not widget.winfo_exists():
                        break
                    # Calculate pulse intensity using sine wave
                    intensity = (math.sin(i * 2 * math.pi / steps) + 1) / 2
                    color = color_highlight if intensity > 0.5 else color_normal
                    widget.configure(bg=color)
                    time.sleep(duration / steps)
            except Exception:
                pass

        threading.Thread(target=animate, daemon=True).start()

    @staticmethod
    def glow_on_hover(widget, normal_bg: str, glow_bg: str):
        """Add glow effect on hover"""

        def on_enter(event):
            try:
                widget.configure(bg=glow_bg)
            except Exception:
                pass

        def on_leave(event):
            try:
                widget.configure(bg=normal_bg)
            except Exception:
                pass

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)


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

    def create_notification_toast(
        self, parent, message: str, toast_type: str = "info", duration: int = 3000
    ):
        """Create gaming-style notification toast - Fixed Version"""
        print(f"🔔 Creating notification: {message}")  # Debug log

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

        try:
            # Create toast window
            toast = tk.Toplevel(parent)
            toast.withdraw()
            toast.overrideredirect(True)
            toast.attributes("-topmost", True)

            # Force focus on parent first
            parent.focus_force()
            parent.update()

            # Toast frame with better styling
            toast_frame = tk.Frame(
                toast,
                bg=config["bg"],
                padx=25,
                pady=18,
                relief="solid",
                bd=2,
                highlightbackground=self.colors.border_glow,
                highlightthickness=2,
            )
            toast_frame.pack()

            # Content frame
            content_frame = tk.Frame(toast_frame, bg=config["bg"])
            content_frame.pack(fill="both", expand=True)

            # Icon
            icon_label = tk.Label(
                content_frame,
                text=config["icon"],
                font=("Segoe UI", 18),
                bg=config["bg"],
                fg=config["fg"],
            )
            icon_label.pack(side="left", padx=(0, 12))

            # Message
            message_label = tk.Label(
                content_frame,
                text=message,
                font=("Orbitron", 11, "bold"),
                bg=config["bg"],
                fg=config["fg"],
                wraplength=320,
                justify="left",
            )
            message_label.pack(side="left", fill="both", expand=True)

            # Update and position toast
            toast.update_idletasks()
            width = toast.winfo_reqwidth()
            height = toast.winfo_reqheight()

            # Calculate position - top right corner
            screen_width = toast.winfo_screenwidth()
            screen_height = toast.winfo_screenheight()

            x = screen_width - width - 30
            y = 60  # Fixed position from top

            toast.geometry(f"{width}x{height}+{x}+{y}")

            # Show toast
            toast.deiconify()
            toast.lift()
            toast.focus_force()

            print(f"✅ Toast positioned at: {x}, {y} (size: {width}x{height})")

            # Auto-hide function
            def hide_toast():
                try:
                    if toast.winfo_exists():
                        toast.destroy()
                        print(f"🗑️ Toast destroyed: {message[:30]}...")
                except Exception as e:
                    print(f"⚠️ Error destroying toast: {e}")

            # Schedule auto-hide
            toast.after(duration, hide_toast)

            # Manual dismiss on click
            def on_click(event):
                hide_toast()

            toast.bind("<Button-1>", on_click)
            toast_frame.bind("<Button-1>", on_click)
            content_frame.bind("<Button-1>", on_click)
            icon_label.bind("<Button-1>", on_click)
            message_label.bind("<Button-1>", on_click)

            # Return toast reference for debugging
            return toast

        except Exception as e:
            print(f"❌ Error creating notification: {e}")
            import traceback

            traceback.print_exc()
            return None


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
            root.attributes("-alpha", 0.98)  # Slight transparency
        except Exception:
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
            for child in text_frame.winfo_children():
                try:
                    child.configure(bg=self.colors.bg_elevated)
                except Exception:
                    pass

        def on_leave(event):
            button.configure(bg=self.colors.bg_secondary)
            content_frame.configure(bg=self.colors.bg_secondary)
            icon_label.configure(bg=self.colors.bg_secondary)
            text_frame.configure(bg=self.colors.bg_secondary)
            title_label.configure(
                bg=self.colors.bg_secondary, fg=self.colors.text_primary
            )
            for child in text_frame.winfo_children():
                try:
                    child.configure(bg=self.colors.bg_secondary)
                except Exception:
                    pass

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

        # Auto-hide after 4 seconds
        def hide_popup():
            try:
                if popup.winfo_exists():
                    popup.destroy()
            except Exception:
                pass

        popup.after(4000, hide_popup)


# Create global gaming theme instance
gaming_theme = GamingTheme()
