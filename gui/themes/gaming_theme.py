"""
gui/themes/gaming_theme.py
Enhanced Gaming-Inspired UI Theme for DENSO888 - Fixed Version
เฮียตอมจัดหั้ย!!! - Stable Gaming Theme 🎮🚀
"""

from dataclasses import dataclass
import tkinter as tk
import math
import threading
import time
from typing import Optional, Callable, Dict, Any, List


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


class SafeAnimations:
    """Thread-safe gaming animations with proper error handling"""

    @staticmethod
    def pulse_effect(
        widget, color_normal: str, color_highlight: str, duration: float = 1.0
    ):
        """Safe pulse animation with error handling"""

        def animate():
            try:
                if not widget or not hasattr(widget, "winfo_exists"):
                    return

                steps = 20  # Reduced for better performance
                for i in range(steps):
                    if not widget.winfo_exists():
                        break

                    # Calculate pulse intensity
                    intensity = (math.sin(i * 2 * math.pi / steps) + 1) / 2
                    color = color_highlight if intensity > 0.5 else color_normal

                    # Safe color update
                    widget.after_idle(
                        lambda c=color: (
                            widget.configure(bg=c) if widget.winfo_exists() else None
                        )
                    )
                    time.sleep(duration / steps)

            except Exception as e:
                print(f"⚠️ Animation error (non-critical): {e}")

        # Run in daemon thread
        animation_thread = threading.Thread(target=animate, daemon=True)
        animation_thread.start()

    @staticmethod
    def safe_glow_on_hover(widget, normal_bg: str, glow_bg: str):
        """Safe hover effect with error handling"""

        def on_enter(event):
            try:
                if widget.winfo_exists():
                    widget.configure(bg=glow_bg)
            except Exception:
                pass

        def on_leave(event):
            try:
                if widget.winfo_exists():
                    widget.configure(bg=normal_bg)
            except Exception:
                pass

        try:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
        except Exception:
            pass


class NotificationManager:
    """Centralized notification management with queue system"""

    def __init__(self):
        self.active_notifications: List[tk.Toplevel] = []
        self.notification_queue: List[Dict[str, Any]] = []
        self.processing = False

    def show_notification(
        self, parent, message: str, toast_type: str = "info", duration: int = 3000
    ):
        """Queue and show notification safely"""
        notification_data = {
            "parent": parent,
            "message": message,
            "type": toast_type,
            "duration": duration,
        }

        self.notification_queue.append(notification_data)

        if not self.processing:
            self._process_queue()

    def _process_queue(self):
        """Process notification queue"""
        if not self.notification_queue:
            return

        self.processing = True
        notification = self.notification_queue.pop(0)

        try:
            self._create_toast(**notification)
        except Exception as e:
            print(f"❌ Notification error: {e}")
        finally:
            self.processing = False
            # Process next if any
            if self.notification_queue:
                threading.Timer(0.1, self._process_queue).start()

    def _create_toast(self, parent, message: str, type: str, duration: int):
        """Create actual notification toast"""
        if (
            not parent
            or not hasattr(parent, "winfo_exists")
            or not parent.winfo_exists()
        ):
            print(f"⚠️ Parent window unavailable for: {message}")
            return None

        type_configs = {
            "success": {"bg": "#00FF88", "fg": "#000000", "icon": "✅"},
            "warning": {"bg": "#FFB800", "fg": "#000000", "icon": "⚠️"},
            "error": {"bg": "#FF4466", "fg": "#FFFFFF", "icon": "❌"},
            "info": {"bg": "#00FFFF", "fg": "#000000", "icon": "ℹ️"},
        }

        config = type_configs.get(type, type_configs["info"])

        try:
            # Create toast window
            toast = tk.Toplevel(parent)
            toast.withdraw()
            toast.overrideredirect(True)
            toast.attributes("-topmost", True)

            # Toast frame
            toast_frame = tk.Frame(
                toast, bg=config["bg"], padx=20, pady=15, relief="solid", bd=1
            )
            toast_frame.pack()

            # Content frame
            content_frame = tk.Frame(toast_frame, bg=config["bg"])
            content_frame.pack(fill="both", expand=True)

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
                font=("Orbitron", 10, "bold"),
                bg=config["bg"],
                fg=config["fg"],
                wraplength=300,
                justify="left",
            )
            message_label.pack(side="left", fill="both", expand=True)

            # Position toast
            self._position_toast(toast)

            # Show toast
            toast.deiconify()
            toast.lift()

            # Add to active list
            self.active_notifications.append(toast)

            # Schedule auto-hide
            def hide_toast():
                self._hide_toast(toast)

            toast.after(duration, hide_toast)

            # Click to dismiss
            def on_click(event):
                hide_toast()

            for widget in [
                toast,
                toast_frame,
                content_frame,
                icon_label,
                message_label,
            ]:
                widget.bind("<Button-1>", on_click)

            print(f"✅ Notification shown: {message[:30]}...")
            return toast

        except Exception as e:
            print(f"❌ Toast creation error: {e}")
            return None

    def _position_toast(self, toast):
        """Position toast in top-right corner"""
        try:
            toast.update_idletasks()
            width = toast.winfo_reqwidth()
            height = toast.winfo_reqheight()

            screen_width = toast.winfo_screenwidth()
            x = screen_width - width - 20
            y = 20 + len(self.active_notifications) * (height + 10)

            toast.geometry(f"{width}x{height}+{x}+{y}")
        except Exception as e:
            print(f"⚠️ Toast positioning error: {e}")

    def _hide_toast(self, toast):
        """Hide and remove toast"""
        try:
            if toast in self.active_notifications:
                self.active_notifications.remove(toast)

            if toast.winfo_exists():
                toast.destroy()

            # Reposition remaining toasts
            self._reposition_toasts()

        except Exception as e:
            print(f"⚠️ Toast hiding error: {e}")

    def _reposition_toasts(self):
        """Reposition remaining toasts"""
        try:
            for i, toast in enumerate(self.active_notifications):
                if toast.winfo_exists():
                    height = toast.winfo_reqheight()
                    y = 20 + i * (height + 10)
                    x = toast.winfo_x()
                    toast.geometry(f"+{x}+{y}")
        except Exception:
            pass

    def clear_all(self):
        """Clear all notifications"""
        for toast in self.active_notifications[:]:
            self._hide_toast(toast)


class GamingComponents:
    """Enhanced gaming UI components with robust error handling"""

    def __init__(self, colors: GamingColors):
        self.colors = colors
        self.notification_manager = NotificationManager()

    def create_neon_button(
        self,
        parent,
        text: str,
        command: Optional[Callable] = None,
        style: str = "primary",
        size: str = "medium",
    ) -> tk.Button:
        """Create neon-style gaming button with safe interactions"""

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

        # Add safe glow effect
        SafeAnimations.safe_glow_on_hover(
            button, style_config["bg"], style_config["glow"]
        )
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
        """Create notification using centralized manager"""
        return self.notification_manager.show_notification(
            parent, message, toast_type, duration
        )


class GamingTheme:
    """Complete gaming theme for DENSO888 with enhanced stability"""

    def __init__(self):
        self.colors = GamingColors()
        self.animations = SafeAnimations()
        self.components = GamingComponents(self.colors)

        # Theme metadata
        self.name = "DENSO888 Gaming Edition"
        self.version = "2.0.1"
        self.style = "Cyberpunk Gaming Enhanced"

    def apply_to_root(self, root: tk.Tk):
        """Apply gaming theme safely"""
        try:
            print("🎨 Applying gaming theme...")
            root.configure(bg=self.colors.bg_primary)

            # Skip transparency on Windows if problematic
            try:
                root.attributes("-alpha", 0.98)
            except Exception as e:
                print(f"⚠️ Transparency not supported: {e}")

            print("✅ Gaming theme applied")

        except Exception as e:
            print(f"❌ Theme application failed: {e}")
            # Fallback to basic theme
            root.configure(bg="#1A1A2E")

    def create_gaming_sidebar(
        self, parent, items: List[Dict], callback: Callable
    ) -> tk.Frame:
        """Create gaming-style sidebar with enhanced error handling"""
        try:
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
            self._create_sidebar_header(sidebar)

            # Menu items
            menu_frame = tk.Frame(sidebar, bg=self.colors.bg_secondary)
            menu_frame.pack(fill="both", expand=True, padx=10)

            for item in items:
                self._create_sidebar_item(menu_frame, item, callback)

            return sidebar

        except Exception as e:
            print(f"❌ Sidebar creation error: {e}")
            # Return fallback sidebar
            return tk.Frame(parent, bg=self.colors.bg_secondary)

    def _create_sidebar_header(self, sidebar):
        """Create sidebar header safely"""
        try:
            header_frame = tk.Frame(sidebar, bg=self.colors.bg_secondary, height=100)
            header_frame.pack(fill="x")
            header_frame.pack_propagate(False)

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
        except Exception as e:
            print(f"⚠️ Header creation warning: {e}")

    def _create_sidebar_item(self, parent, item: Dict[str, Any], callback: Callable):
        """Create individual sidebar menu item safely"""
        try:
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
                command=lambda: self._safe_callback(callback, item.get("id", "")),
                anchor="w",
                padx=15,
                pady=12,
            )
            button.pack(fill="x")

            # Button content
            self._setup_button_content(button, item)
            self._setup_button_events(button, item)

        except Exception as e:
            print(f"⚠️ Sidebar item creation warning: {e}")

    def _safe_callback(self, callback: Callable, item_id: str):
        """Execute callback safely"""
        try:
            if callback and callable(callback):
                callback(item_id)
        except Exception as e:
            print(f"❌ Callback error: {e}")

    def _setup_button_content(self, button: tk.Button, item: Dict[str, Any]):
        """Setup button content safely"""
        try:
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

        except Exception as e:
            print(f"⚠️ Button content setup warning: {e}")

    def _setup_button_events(self, button: tk.Button, item: Dict[str, Any]):
        """Setup hover events safely"""
        try:

            def safe_on_enter(event):
                try:
                    if button.winfo_exists():
                        button.configure(bg=self.colors.bg_elevated)
                        # Update child widgets safely
                        for child in button.winfo_children():
                            if hasattr(child, "configure"):
                                child.configure(bg=self.colors.bg_elevated)
                except Exception:
                    pass

            def safe_on_leave(event):
                try:
                    if button.winfo_exists():
                        button.configure(bg=self.colors.bg_secondary)
                        # Update child widgets safely
                        for child in button.winfo_children():
                            if hasattr(child, "configure"):
                                child.configure(bg=self.colors.bg_secondary)
                except Exception:
                    pass

            button.bind("<Enter>", safe_on_enter)
            button.bind("<Leave>", safe_on_leave)

        except Exception as e:
            print(f"⚠️ Button events setup warning: {e}")

    def create_gaming_header(self, parent, title: str, subtitle: str = "") -> tk.Frame:
        """Create gaming-style header safely"""
        try:
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

            content_frame = tk.Frame(header, bg=self.colors.bg_primary)
            content_frame.pack(expand=True, fill="both")

            # Title
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

            # Add safe pulse animation
            SafeAnimations.pulse_effect(
                title_label, self.colors.primary, self.colors.primary_glow, 2.0
            )
            return header

        except Exception as e:
            print(f"❌ Header creation error: {e}")
            return tk.Frame(parent, bg=self.colors.bg_primary)

    def create_achievement_popup(
        self, parent, title: str, description: str, achievement_type: str = "gold"
    ):
        """Create achievement notification popup safely"""
        try:
            colors_map = {
                "gold": self.colors.gold,
                "silver": self.colors.silver,
                "bronze": self.colors.bronze,
            }
            achievement_color = colors_map.get(achievement_type, self.colors.gold)

            # Create popup
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

            # Content
            content_frame = tk.Frame(main_frame, bg=self.colors.bg_card)
            content_frame.pack()

            # Icon
            icon_label = tk.Label(
                content_frame,
                text="🏆",
                font=("Segoe UI", 32),
                bg=self.colors.bg_card,
                fg=achievement_color,
            )
            icon_label.pack()

            # Text
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

            # Position popup
            popup.update_idletasks()
            width = popup.winfo_reqwidth()
            height = popup.winfo_reqheight()

            screen_width = popup.winfo_screenwidth()
            screen_height = popup.winfo_screenheight()
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2 - 100

            popup.geometry(f"{width}x{height}+{x}+{y}")
            popup.deiconify()

            # Auto-hide
            def safe_hide():
                try:
                    if popup.winfo_exists():
                        popup.destroy()
                except Exception:
                    pass

            popup.after(4000, safe_hide)

        except Exception as e:
            print(f"❌ Achievement popup error: {e}")

    def cleanup(self):
        """Cleanup theme resources"""
        try:
            self.components.notification_manager.clear_all()
        except Exception:
            pass


# Create global gaming theme instance
gaming_theme = GamingTheme()
