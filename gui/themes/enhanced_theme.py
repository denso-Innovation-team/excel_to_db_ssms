"""
gui/themes/enhanced_theme.py
Enhanced Theme System with Better Contrast and Responsiveness
เฮียตอมปรับปรุงสีสันและการใช้งาน 🎨
"""

import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass
from typing import Callable
import time


@dataclass
class EnhancedColors:
    """Enhanced color palette with better contrast ratios"""

    # Primary DENSO colors - Enhanced contrast
    primary: str = "#FF0066"  # Bright pink - DENSO signature
    primary_light: str = "#FF3388"  # Lighter pink for hover
    primary_dark: str = "#CC0044"  # Darker pink for active

    # Secondary colors - High contrast
    secondary: str = "#00E5FF"  # Bright cyan - excellent contrast
    secondary_light: str = "#4FFFFF"  # Light cyan
    secondary_dark: str = "#00B8CC"  # Dark cyan

    # Background colors - Better depth
    bg_primary: str = "#0D1117"  # Very dark blue-gray (GitHub dark)
    bg_secondary: str = "#161B22"  # Dark blue-gray
    bg_card: str = "#21262D"  # Card background
    bg_elevated: str = "#2D333B"  # Elevated elements
    bg_input: str = "#1C2128"  # Input backgrounds

    # Text colors - Excellent contrast
    text_primary: str = "#F0F6FC"  # Primary text (AAA contrast)
    text_secondary: str = "#7D8590"  # Secondary text (AA contrast)
    text_muted: str = "#656D76"  # Muted text
    text_accent: str = "#00D7FF"  # Accent text
    text_link: str = "#58A6FF"  # Links

    # Status colors - Clear and distinct
    success: str = "#26D944"  # Bright green
    warning: str = "#FFD93D"  # Bright yellow
    error: str = "#FF4757"  # Bright red
    info: str = "#17A2B8"  # Blue info

    # Border and UI elements
    border: str = "#30363D"  # Border color
    border_focus: str = "#388BFD"  # Focus border
    border_error: str = "#FF4757"  # Error border

    # Interactive states
    hover: str = "#292E36"  # Hover state
    pressed: str = "#1C2128"  # Pressed state
    selected: str = "#373E47"  # Selected state

    # Special gaming colors
    neon_blue: str = "#00FFFF"  # Pure cyan
    neon_green: str = "#39FF14"  # Electric green
    neon_pink: str = "#FF007F"  # Electric pink
    neon_orange: str = "#FF8C00"  # Electric orange


class EnhancedFonts:
    """Enhanced font system with proper hierarchy"""

    def __init__(self):
        # Modern font stack
        self.font_family = "Segoe UI"
        self.mono_family = "JetBrains Mono"  # Fallback to Consolas

        # Font sizes - Better hierarchy
        self.size_xs = 8
        self.size_sm = 10
        self.size_md = 11
        self.size_lg = 12
        self.size_xl = 14
        self.size_2xl = 16
        self.size_3xl = 18
        self.size_4xl = 20
        self.size_5xl = 24

        # Font configurations
        self.heading_xl = (self.font_family, self.size_5xl, "bold")
        self.heading_lg = (self.font_family, self.size_4xl, "bold")
        self.heading_md = (self.font_family, self.size_3xl, "bold")
        self.heading_sm = (self.font_family, self.size_2xl, "bold")

        self.body_xl = (self.font_family, self.size_xl)
        self.body_lg = (self.font_family, self.size_lg)
        self.body_md = (self.font_family, self.size_md)
        self.body_sm = (self.font_family, self.size_sm)

        self.caption = (self.font_family, self.size_sm)
        self.caption_sm = (self.font_family, self.size_xs)

        self.code = (self.mono_family, self.size_md)
        self.code_sm = (self.mono_family, self.size_sm)

    def __getitem__(self, key):
        """Allow dictionary-style access"""
        return getattr(self, key, self.body_md)


class ResponsiveLayoutManager:
    """Responsive layout management for different screen sizes"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.current_breakpoint = "desktop"
        self.breakpoints = {
            "mobile": (0, 768),
            "tablet": (768, 1024),
            "desktop": (1024, 1920),
            "wide": (1920, float("inf")),
        }

        # Bind resize event
        self.root.bind("<Configure>", self._on_window_resize)

    def _on_window_resize(self, event):
        """Handle window resize events"""
        if event.widget == self.root:
            width = event.width
            new_breakpoint = self._get_breakpoint(width)

            if new_breakpoint != self.current_breakpoint:
                self.current_breakpoint = new_breakpoint
                self._trigger_layout_update()

    def _get_breakpoint(self, width: int) -> str:
        """Determine current breakpoint based on width"""
        for name, (min_width, max_width) in self.breakpoints.items():
            if min_width <= width < max_width:
                return name
        return "desktop"

    def _trigger_layout_update(self):
        """Trigger layout updates for responsive design"""
        # This would trigger callbacks for layout adjustments
        pass

    def get_sidebar_width(self) -> int:
        """Get responsive sidebar width"""
        widths = {
            "mobile": 0,  # Hidden on mobile
            "tablet": 250,
            "desktop": 280,
            "wide": 320,
        }
        return widths.get(self.current_breakpoint, 280)

    def should_show_sidebar(self) -> bool:
        """Determine if sidebar should be shown"""
        return self.current_breakpoint != "mobile"


class EnhancedNotificationSystem:
    """Enhanced notification system with better UX"""

    def __init__(self, parent: tk.Tk, colors: EnhancedColors):
        self.parent = parent
        self.colors = colors
        self.notifications = []
        self.queue = []
        self.processing = False

    def show_notification(
        self, message: str, type_: str = "info", duration: int = 4000
    ):
        """Show enhanced notification with better styling"""
        notification_data = {
            "message": message,
            "type": type_,
            "duration": duration,
            "timestamp": time.time(),
        }

        self.queue.append(notification_data)

        if not self.processing:
            self._process_queue()

    def _process_queue(self):
        """Process notification queue"""
        if not self.queue:
            self.processing = False
            return

        self.processing = True
        notification = self.queue.pop(0)

        try:
            self._create_notification(notification)
        except Exception as e:
            print(f"Notification error: {e}")

        # Process next after delay
        self.parent.after(200, self._process_queue)

    def _create_notification(self, notification):
        """Create notification toast with enhanced styling"""
        type_configs = {
            "success": {
                "bg": self.colors.success,
                "fg": self.colors.bg_primary,
                "icon": "✅",
                "border": self.colors.success,
            },
            "error": {
                "bg": self.colors.error,
                "fg": self.colors.text_primary,
                "icon": "❌",
                "border": self.colors.error,
            },
            "warning": {
                "bg": self.colors.warning,
                "fg": self.colors.bg_primary,
                "icon": "⚠️",
                "border": self.colors.warning,
            },
            "info": {
                "bg": self.colors.info,
                "fg": self.colors.text_primary,
                "icon": "ℹ️",
                "border": self.colors.info,
            },
        }

        config = type_configs.get(notification["type"], type_configs["info"])

        # Create notification window
        toast = tk.Toplevel(self.parent)
        toast.withdraw()
        toast.overrideredirect(True)
        toast.attributes("-topmost", True)

        # Enhanced notification frame with shadow effect
        toast_frame = tk.Frame(
            toast,
            bg=config["bg"],
            relief="solid",
            bd=1,
            highlightbackground=config["border"],
            highlightthickness=2,
        )
        toast_frame.pack(fill="both", expand=True, padx=2, pady=2)

        # Content container
        content_frame = tk.Frame(toast_frame, bg=config["bg"])
        content_frame.pack(fill="both", expand=True, padx=15, pady=12)

        # Icon and message layout
        layout_frame = tk.Frame(content_frame, bg=config["bg"])
        layout_frame.pack(fill="x")

        # Icon
        icon_label = tk.Label(
            layout_frame,
            text=config["icon"],
            font=("Segoe UI", 16),
            bg=config["bg"],
            fg=config["fg"],
        )
        icon_label.pack(side="left", padx=(0, 12))

        # Message
        message_label = tk.Label(
            layout_frame,
            text=notification["message"],
            font=("Segoe UI", 11),
            bg=config["bg"],
            fg=config["fg"],
            wraplength=350,
            justify="left",
        )
        message_label.pack(side="left", fill="x", expand=True)

        # Close button
        close_btn = tk.Label(
            layout_frame,
            text="×",
            font=("Segoe UI", 14, "bold"),
            bg=config["bg"],
            fg=config["fg"],
            cursor="hand2",
        )
        close_btn.pack(side="right", padx=(10, 0))

        # Position notification
        self._position_notification(toast)

        # Show with fade-in effect
        toast.deiconify()
        self.notifications.append(toast)

        # Auto-hide
        toast.after(notification["duration"], lambda: self._hide_notification(toast))

        # Click handlers
        def hide_on_click(event):
            self._hide_notification(toast)

        close_btn.bind("<Button-1>", hide_on_click)
        toast_frame.bind("<Button-1>", hide_on_click)

    def _position_notification(self, toast):
        """Position notification in top-right corner"""
        toast.update_idletasks()
        width = toast.winfo_reqwidth()
        height = toast.winfo_reqheight()

        screen_width = toast.winfo_screenwidth()
        x = screen_width - width - 20
        y = 20 + len(self.notifications) * (height + 10)

        toast.geometry(f"{width}x{height}+{x}+{y}")

    def _hide_notification(self, toast):
        """Hide notification with cleanup"""
        try:
            if toast in self.notifications:
                self.notifications.remove(toast)

            if toast.winfo_exists():
                toast.destroy()

            self._reposition_notifications()
        except:
            pass

    def _reposition_notifications(self):
        """Reposition remaining notifications"""
        for i, toast in enumerate(self.notifications):
            try:
                if toast.winfo_exists():
                    height = toast.winfo_reqheight()
                    y = 20 + i * (height + 10)
                    x = toast.winfo_x()
                    toast.geometry(f"+{x}+{y}")
            except:
                pass


class EnhancedComponentFactory:
    """Factory for creating enhanced UI components"""

    def __init__(self, colors: EnhancedColors, fonts: EnhancedFonts):
        self.colors = colors
        self.fonts = fonts

    def create_button(
        self,
        parent,
        text: str,
        command: Callable = None,
        style: str = "primary",
        size: str = "medium",
    ) -> tk.Button:
        """Create enhanced button with proper styling"""

        style_configs = {
            "primary": {
                "bg": self.colors.primary,
                "fg": self.colors.text_primary,
                "hover_bg": self.colors.primary_light,
                "active_bg": self.colors.primary_dark,
            },
            "secondary": {
                "bg": self.colors.secondary,
                "fg": self.colors.bg_primary,
                "hover_bg": self.colors.secondary_light,
                "active_bg": self.colors.secondary_dark,
            },
            "success": {
                "bg": self.colors.success,
                "fg": self.colors.bg_primary,
                "hover_bg": "#40E762",
                "active_bg": "#1FC93D",
            },
            "danger": {
                "bg": self.colors.error,
                "fg": self.colors.text_primary,
                "hover_bg": "#FF6B7A",
                "active_bg": "#FF2D42",
            },
            "ghost": {
                "bg": "transparent",
                "fg": self.colors.text_primary,
                "hover_bg": self.colors.hover,
                "active_bg": self.colors.pressed,
            },
        }

        size_configs = {
            "small": {"font": self.fonts.body_sm, "padx": 12, "pady": 6},
            "medium": {"font": self.fonts.body_md, "padx": 16, "pady": 8},
            "large": {"font": self.fonts.body_lg, "padx": 20, "pady": 12},
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

        # Enhanced hover effects
        def on_enter(event):
            button.configure(bg=style_config["hover_bg"])

        def on_leave(event):
            button.configure(bg=style_config["bg"])

        def on_press(event):
            button.configure(bg=style_config["active_bg"])

        def on_release(event):
            button.configure(bg=style_config["hover_bg"])

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        button.bind("<Button-1>", on_press)
        button.bind("<ButtonRelease-1>", on_release)

        return button

    def create_card(self, parent, title: str = "", padding: int = 20) -> tk.Frame:
        """Create enhanced card component"""
        container = tk.Frame(parent, bg=self.colors.bg_primary)

        if title:
            title_label = tk.Label(
                container,
                text=title,
                font=self.fonts.heading_sm,
                bg=self.colors.bg_primary,
                fg=self.colors.text_primary,
            )
            title_label.pack(anchor="w", pady=(0, 10))

        card = tk.Frame(
            container,
            bg=self.colors.bg_card,
            relief="solid",
            bd=1,
            highlightbackground=self.colors.border,
            highlightthickness=1,
        )
        card.pack(fill="x", pady=(0, 0))

        # Content frame with padding
        content = tk.Frame(card, bg=self.colors.bg_card)
        content.pack(fill="both", expand=True, padx=padding, pady=padding)

        return content

    def create_input(self, parent, placeholder: str = "", width: int = 20) -> tk.Entry:
        """Create enhanced input field"""
        input_field = tk.Entry(
            parent,
            font=self.fonts.body_md,
            bg=self.colors.bg_input,
            fg=self.colors.text_primary,
            insertbackground=self.colors.text_primary,
            relief="solid",
            bd=1,
            highlightbackground=self.colors.border,
            highlightcolor=self.colors.border_focus,
            highlightthickness=1,
            width=width,
        )

        # Placeholder functionality
        if placeholder:

            def on_focus_in(event):
                if input_field.get() == placeholder:
                    input_field.delete(0, tk.END)
                    input_field.configure(fg=self.colors.text_primary)

            def on_focus_out(event):
                if not input_field.get():
                    input_field.insert(0, placeholder)
                    input_field.configure(fg=self.colors.text_secondary)

            input_field.insert(0, placeholder)
            input_field.configure(fg=self.colors.text_secondary)
            input_field.bind("<FocusIn>", on_focus_in)
            input_field.bind("<FocusOut>", on_focus_out)

        return input_field


class EnhancedTheme:
    """Main enhanced theme class"""

    def __init__(self):
        self.colors = EnhancedColors()
        self.fonts = EnhancedFonts()
        self.components = EnhancedComponentFactory(self.colors, self.fonts)
        self.notifications = None
        self.layout_manager = None

        # Theme metadata
        self.name = "DENSO888 Enhanced"
        self.version = "2.1.0"
        self.description = "Enhanced theme with better contrast and UX"

    def apply_to_window(self, root: tk.Tk):
        """Apply theme to main window"""
        try:
            root.configure(bg=self.colors.bg_primary)

            # Initialize systems
            self.layout_manager = ResponsiveLayoutManager(root)
            self.notifications = EnhancedNotificationSystem(root, self.colors)

            # Configure ttk styles
            self._configure_ttk_styles()

            print("✅ Enhanced theme applied successfully")

        except Exception as e:
            print(f"❌ Theme application failed: {e}")

    def _configure_ttk_styles(self):
        """Configure ttk widget styles"""
        style = ttk.Style()

        # Progressbar style
        style.configure(
            "Enhanced.Horizontal.TProgressbar",
            background=self.colors.primary,
            troughcolor=self.colors.bg_secondary,
            borderwidth=0,
            lightcolor=self.colors.primary,
            darkcolor=self.colors.primary,
        )

        # Combobox style
        style.configure(
            "Enhanced.TCombobox",
            fieldbackground=self.colors.bg_input,
            background=self.colors.bg_card,
            foreground=self.colors.text_primary,
            bordercolor=self.colors.border,
            focuscolor=self.colors.border_focus,
        )

    def show_notification(
        self, message: str, type_: str = "info", duration: int = 4000
    ):
        """Show notification if system is available"""
        if self.notifications:
            self.notifications.show_notification(message, type_, duration)
        else:
            print(f"Notification: {message}")

    def create_button(
        self,
        parent,
        text: str,
        command: Callable = None,
        style: str = "primary",
        size: str = "medium",
    ) -> tk.Button:
        """Create themed button"""
        return self.components.create_button(parent, text, command, style, size)

    def create_card(self, parent, title: str = "", padding: int = 20) -> tk.Frame:
        """Create themed card"""
        return self.components.create_card(parent, title, padding)

    def create_input(self, parent, placeholder: str = "", width: int = 20) -> tk.Entry:
        """Create themed input"""
        return self.components.create_input(parent, placeholder, width)


# Global enhanced theme instance
enhanced_theme = EnhancedTheme()
