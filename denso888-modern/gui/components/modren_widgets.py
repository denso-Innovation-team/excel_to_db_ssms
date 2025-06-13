"""
Modern Reusable Widgets for DENSO888
Created by Thammaphon Chittasuwanna (SDM) | Innovation
"""

import tkinter as tk
from tkinter import ttk


class ModernScrollableFrame:
    """Modern scrollable frame with custom scrollbar"""

    def __init__(self, parent, theme_manager, height=None):
        self.parent = parent
        self.theme_manager = theme_manager
        self.colors = theme_manager.get_theme()

        # Main container
        self.container = ttk.Frame(parent, style="Modern.TFrame")
        if height:
            self.container.configure(height=height)

        # Canvas for scrolling
        self.canvas = tk.Canvas(
            self.container, bg=self.colors.surface, highlightthickness=0, bd=0
        )

        # Scrollable frame
        self.scrollable_frame = ttk.Frame(self.canvas, style="Modern.TFrame")

        # Custom scrollbar
        self.scrollbar = ModernScrollbar(self.container, self.canvas, theme_manager)

        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas_frame = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )

        # Bind canvas resize
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # Mouse wheel scrolling
        self._bind_mousewheel()

        # Pack components
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def pack(self, **kwargs):
        self.container.pack(**kwargs)

    def grid(self, **kwargs):
        self.container.grid(**kwargs)

    def _on_canvas_configure(self, event):
        """Handle canvas resize"""
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def _bind_mousewheel(self):
        """Bind mouse wheel events"""

        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _bind_to_mousewheel(event):
            self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind_from_mousewheel(event):
            self.canvas.unbind_all("<MouseWheel>")

        self.canvas.bind("<Enter>", _bind_to_mousewheel)
        self.canvas.bind("<Leave>", _unbind_from_mousewheel)


class ModernScrollbar:
    """Custom modern scrollbar"""

    def __init__(self, parent, canvas, theme_manager):
        self.parent = parent
        self.canvas = canvas
        self.colors = theme_manager.get_theme()

        # Scrollbar frame
        self.frame = tk.Frame(parent, bg=self.colors.surface, width=12)

        # Scrollbar track
        self.track = tk.Frame(self.frame, bg=self.colors.border, width=8)
        self.track.pack(fill="y", padx=2, pady=2)

        # Scrollbar thumb
        self.thumb = tk.Frame(
            self.track, bg=self.colors.text_secondary, height=30, width=6
        )

        # Bind events
        self._setup_scrolling()

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def _setup_scrolling(self):
        """Setup scrollbar functionality"""
        # This is a simplified version - full implementation would include
        # drag handling, click to scroll, etc.
        pass


class ModernButton:
    """Enhanced button with hover effects and icons"""

    def __init__(
        self,
        parent,
        text="",
        icon="",
        style="Primary",
        command=None,
        theme_manager=None,
    ):
        self.parent = parent
        self.theme_manager = theme_manager
        self.colors = theme_manager.get_theme() if theme_manager else None

        # Button frame for custom styling
        self.frame = tk.Frame(parent, relief="flat", bd=0)

        # Button content
        self.button = tk.Button(
            self.frame,
            text=f"{icon} {text}".strip(),
            command=command,
            relief="flat",
            bd=0,
            padx=20,
            pady=12,
            font=("Segoe UI", 10, "bold" if style == "Primary" else "normal"),
            cursor="hand2",
        )

        self.button.pack(fill="both", expand=True)

        # Apply styling
        self._apply_style(style)

        # Bind hover effects
        self._setup_hover_effects()

    def _apply_style(self, style):
        """Apply button styling based on type"""
        if not self.colors:
            return

        styles = {
            "Primary": {
                "bg": self.colors.primary,
                "fg": "white",
                "hover_bg": self.colors.primary_light,
                "active_bg": self.colors.primary_dark,
            },
            "Secondary": {
                "bg": self.colors.secondary,
                "fg": "white",
                "hover_bg": "#34495e",
                "active_bg": "#2c3e50",
            },
            "Success": {
                "bg": self.colors.success,
                "fg": "white",
                "hover_bg": "#2ecc71",
                "active_bg": "#229954",
            },
            "Danger": {
                "bg": self.colors.danger,
                "fg": "white",
                "hover_bg": "#e74c3c",
                "active_bg": "#c0392b",
            },
            "Ghost": {
                "bg": self.colors.surface,
                "fg": self.colors.text_primary,
                "hover_bg": self.colors.border,
                "active_bg": self.colors.border,
            },
        }

        style_config = styles.get(style, styles["Primary"])

        self.button.configure(
            bg=style_config["bg"],
            fg=style_config["fg"],
            activebackground=style_config["active_bg"],
            activeforeground=style_config["fg"],
        )

        self.frame.configure(bg=style_config["bg"])

        # Store colors for hover effects
        self.normal_bg = style_config["bg"]
        self.hover_bg = style_config["hover_bg"]
        self.active_bg = style_config["active_bg"]

    def _setup_hover_effects(self):
        """Setup hover animation effects"""

        def on_enter(event):
            self.button.configure(bg=self.hover_bg)
            self.frame.configure(bg=self.hover_bg)

        def on_leave(event):
            self.button.configure(bg=self.normal_bg)
            self.frame.configure(bg=self.normal_bg)

        def on_click(event):
            self.button.configure(bg=self.active_bg)
            self.frame.configure(bg=self.active_bg)
            self.button.after(100, lambda: self.button.configure(bg=self.hover_bg))

        self.button.bind("<Enter>", on_enter)
        self.button.bind("<Leave>", on_leave)
        self.button.bind("<Button-1>", on_click)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)

    def configure(self, **kwargs):
        self.button.configure(**kwargs)


class ModernCard:
    """Modern card component with shadow effect"""

    def __init__(self, parent, theme_manager, title="", content_frame_class=None):
        self.parent = parent
        self.theme_manager = theme_manager
        self.colors = theme_manager.get_theme()

        # Main card frame with shadow simulation
        self.shadow_frame = tk.Frame(parent, bg="#E0E0E0", relief="flat")

        # Card content frame
        self.frame = tk.Frame(
            self.shadow_frame,
            bg=self.colors.surface,
            relief="flat",
            bd=1,
            highlightbackground=self.colors.border,
            highlightthickness=1,
        )

        # Pack with slight offset for shadow effect
        self.frame.pack(padx=(0, 2), pady=(0, 2), fill="both", expand=True)

        # Title header if provided
        if title:
            self.header = tk.Frame(self.frame, bg=self.colors.surface)
            self.header.pack(fill="x", padx=15, pady=(15, 5))

            self.title_label = tk.Label(
                self.header,
                text=title,
                bg=self.colors.surface,
                fg=self.colors.text_primary,
                font=("Segoe UI", 12, "bold"),
                anchor="w",
            )
            self.title_label.pack(side="left")

        # Content area
        if content_frame_class:
            self.content = content_frame_class(self.frame, theme_manager)
        else:
            self.content = tk.Frame(self.frame, bg=self.colors.surface)

        self.content.pack(fill="both", expand=True, padx=15, pady=15)

    def pack(self, **kwargs):
        self.shadow_frame.pack(**kwargs)

    def grid(self, **kwargs):
        self.shadow_frame.grid(**kwargs)


class MetricCard:
    """Specialized card for displaying metrics"""

    def __init__(self, parent, theme_manager, config):
        self.parent = parent
        self.theme_manager = theme_manager
        self.colors = theme_manager.get_theme()
        self.config = config

        # Main frame
        self.frame = tk.Frame(
            parent,
            bg=self.colors.surface,
            relief="solid",
            bd=1,
            highlightbackground=self.colors.border,
            highlightthickness=1,
        )

        # Card content
        self._create_content()

        # Hover effects
        self._setup_hover_effects()

    def _create_content(self):
        """Create metric card content"""
        # Content container
        content = tk.Frame(self.frame, bg=self.colors.surface)
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # Header with title and icon
        header = tk.Frame(content, bg=self.colors.surface)
        header.pack(fill="x", pady=(0, 10))

        # Title
        self.title_label = tk.Label(
            header,
            text=self.config["title"],
            bg=self.colors.surface,
            fg=self.colors.text_secondary,
            font=("Segoe UI", 9),
            anchor="w",
        )
        self.title_label.pack(side="left")

        # Icon
        self.icon_label = tk.Label(
            header,
            text=self.config["icon"],
            bg=self.colors.surface,
            font=("Segoe UI", 16),
            anchor="e",
        )
        self.icon_label.pack(side="right")

        # Main value
        self.value_label = tk.Label(
            content,
            text=self.config["value_func"](),
            bg=self.colors.surface,
            fg=self.colors.text_primary,
            font=("Segoe UI", 24, "bold"),
            anchor="w",
        )
        self.value_label.pack(anchor="w", pady=(5, 10))

        # Change indicator
        change_frame = tk.Frame(content, bg=self.colors.surface)
        change_frame.pack(fill="x")

        trend_icon = "📈" if self.config["trend"] == "up" else "📉"
        change_color = (
            self.colors.success if self.config["trend"] == "up" else self.colors.danger
        )

        self.change_label = tk.Label(
            change_frame,
            text=f"{trend_icon} {self.config['change']} from last month",
            bg=self.colors.surface,
            fg=change_color,
            font=("Segoe UI", 8),
            anchor="w",
        )
        self.change_label.pack(side="left")

    def _setup_hover_effects(self):
        """Setup card hover effects"""

        def on_enter(event):
            self.frame.configure(highlightbackground=self.colors.primary)

        def on_leave(event):
            self.frame.configure(highlightbackground=self.colors.border)

        self.frame.bind("<Enter>", on_enter)
        self.frame.bind("<Leave>", on_leave)

        # Bind to all child widgets
        for widget in self.frame.winfo_children():
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    def update_value(self):
        """Update metric value"""
        try:
            new_value = self.config["value_func"]()
            self.value_label.configure(text=new_value)
        except Exception as e:
            print(f"Error updating metric {self.config['key']}: {e}")

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)


class ModernProgressBar:
    """Custom progress bar with modern styling"""

    def __init__(self, parent, theme_manager, mode="determinate"):
        self.parent = parent
        self.theme_manager = theme_manager
        self.colors = theme_manager.get_theme()
        self.mode = mode
        self.value = 0
        self.max_value = 100

        # Progress container
        self.frame = tk.Frame(parent, bg=self.colors.surface)

        # Progress track
        self.track = tk.Frame(
            self.frame, bg=self.colors.border, height=8, relief="flat"
        )
        self.track.pack(fill="x", pady=5)
        self.track.pack_propagate(False)

        # Progress bar
        self.bar = tk.Frame(self.track, bg=self.colors.primary, height=8, relief="flat")

        # Progress text
        self.text_label = tk.Label(
            self.frame,
            text="0%",
            bg=self.colors.surface,
            fg=self.colors.text_secondary,
            font=("Segoe UI", 8),
        )
        self.text_label.pack(anchor="e")

        # Animation for indeterminate mode
        self.animation_step = 0
        self.animation_running = False

        if mode == "indeterminate":
            self.start_animation()

    def set_value(self, value):
        """Set progress value (0-100)"""
        self.value = max(0, min(100, value))

        # Update bar width
        self.track.update()
        track_width = self.track.winfo_width()
        bar_width = int((self.value / 100) * track_width)

        self.bar.place(x=0, y=0, width=bar_width, height=8)

        # Update text
        self.text_label.configure(text=f"{self.value:.1f}%")

    def start_animation(self):
        """Start indeterminate animation"""
        if self.mode == "indeterminate" and not self.animation_running:
            self.animation_running = True
            self._animate()

    def stop_animation(self):
        """Stop indeterminate animation"""
        self.animation_running = False

    def _animate(self):
        """Animate indeterminate progress"""
        if not self.animation_running:
            return

        self.track.update()
        track_width = self.track.winfo_width()
        bar_width = 50  # Fixed bar width for animation

        # Calculate position
        position = (self.animation_step % (track_width + bar_width)) - bar_width

        self.bar.place(x=position, y=0, width=bar_width, height=8)

        self.animation_step += 3
        self.frame.after(50, self._animate)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)


class ModernToggleSwitch:
    """Modern toggle switch component"""

    def __init__(self, parent, theme_manager, text="", variable=None, command=None):
        self.parent = parent
        self.theme_manager = theme_manager
        self.colors = theme_manager.get_theme()
        self.variable = variable or tk.BooleanVar()
        self.command = command

        # Main frame
        self.frame = tk.Frame(parent, bg=self.colors.surface)

        # Text label
        if text:
            self.label = tk.Label(
                self.frame,
                text=text,
                bg=self.colors.surface,
                fg=self.colors.text_primary,
                font=("Segoe UI", 9),
            )
            self.label.pack(side="left", padx=(0, 10))

        # Switch container
        self.switch_frame = tk.Frame(self.frame, bg=self.colors.surface)
        self.switch_frame.pack(side="left")

        # Switch track
        self.track = tk.Canvas(
            self.switch_frame,
            width=40,
            height=20,
            bg=self.colors.surface,
            highlightthickness=0,
        )
        self.track.pack()

        # Draw switch
        self._draw_switch()

        # Bind events
        self.track.bind("<Button-1>", self._toggle)
        self.variable.trace("w", self._on_variable_change)

    def _draw_switch(self):
        """Draw the toggle switch"""
        self.track.delete("all")

        is_on = self.variable.get()

        # Track background
        track_color = self.colors.primary if is_on else self.colors.border
        self.track.create_oval(2, 2, 38, 18, fill=track_color, outline="")

        # Switch knob
        knob_x = 28 if is_on else 12
        self.track.create_oval(
            knob_x - 6, 4, knob_x + 6, 16, fill="white", outline="", width=2
        )

    def _toggle(self, event=None):
        """Toggle switch state"""
        self.variable.set(not self.variable.get())
        if self.command:
            self.command()

    def _on_variable_change(self, *args):
        """Handle variable change"""
        self._draw_switch()

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)


class ModernNotification:
    """Toast-style notification component"""

    def __init__(self, parent, theme_manager, message="", type="info", duration=3000):
        self.parent = parent
        self.theme_manager = theme_manager
        self.colors = theme_manager.get_theme()
        self.duration = duration

        # Notification types
        types_config = {
            "info": {"icon": "ℹ️", "color": self.colors.primary},
            "success": {"icon": "✅", "color": self.colors.success},
            "warning": {"icon": "⚠️", "color": self.colors.warning},
            "error": {"icon": "❌", "color": self.colors.danger},
        }

        config = types_config.get(type, types_config["info"])

        # Notification frame
        self.frame = tk.Toplevel(parent)
        self.frame.withdraw()  # Hide initially
        self.frame.overrideredirect(True)  # Remove window decorations
        self.frame.configure(bg=config["color"])

        # Content frame
        content = tk.Frame(self.frame, bg=config["color"])
        content.pack(fill="both", expand=True, padx=2, pady=2)

        # Icon and message
        content_inner = tk.Frame(content, bg=self.colors.surface)
        content_inner.pack(fill="both", expand=True, padx=15, pady=10)

        # Icon
        icon_label = tk.Label(
            content_inner,
            text=config["icon"],
            bg=self.colors.surface,
            font=("Segoe UI", 14),
        )
        icon_label.pack(side="left", padx=(0, 10))

        # Message
        message_label = tk.Label(
            content_inner,
            text=message,
            bg=self.colors.surface,
            fg=self.colors.text_primary,
            font=("Segoe UI", 9),
            wraplength=250,
        )
        message_label.pack(side="left", fill="x", expand=True)

        # Close button
        close_btn = tk.Label(
            content_inner,
            text="✕",
            bg=self.colors.surface,
            fg=self.colors.text_secondary,
            font=("Segoe UI", 10),
            cursor="hand2",
        )
        close_btn.pack(side="right")
        close_btn.bind("<Button-1>", lambda e: self.hide())

        # Position notification
        self._position_notification()

        # Show notification
        self.show()

    def _position_notification(self):
        """Position notification in top-right corner"""
        self.frame.update_idletasks()

        # Get screen dimensions
        screen_width = self.frame.winfo_screenwidth()
        screen_height = self.frame.winfo_screenheight()

        # Get notification dimensions
        width = self.frame.winfo_reqwidth()
        height = self.frame.winfo_reqheight()

        # Position in top-right corner
        x = screen_width - width - 20
        y = 20

        self.frame.geometry(f"{width}x{height}+{x}+{y}")

    def show(self):
        """Show notification with animation"""
        self.frame.deiconify()
        self.frame.lift()

        # Auto-hide after duration
        if self.duration > 0:
            self.frame.after(self.duration, self.hide)

    def hide(self):
        """Hide notification"""
        try:
            self.frame.destroy()
        except:
            pass


# Utility functions
def show_notification(parent, message, type="info", duration=3000):
    """Show a notification toast"""
    from ..themes.theme_manager import ModernThemeManager

    theme_manager = ModernThemeManager()  # This should be passed in real usage
    return ModernNotification(parent, theme_manager, message, type, duration)


def create_modern_button(
    parent, text, icon="", style="Primary", command=None, theme_manager=None
):
    """Factory function for creating modern buttons"""
    return ModernButton(parent, text, icon, style, command, theme_manager)


# Animation utilities
class SmoothAnimator:
    """Smooth animation utility for widgets"""

    @staticmethod
    def fade_in(widget, duration=300, steps=20):
        """Fade in animation"""
        step_time = duration // steps

        def animate(step=0):
            if step <= steps:
                # Simulate fade effect
                try:
                    alpha = step / steps
                    # This is a simplified version - real fade would use transparency
                    widget.after(step_time, lambda: animate(step + 1))
                except:
                    pass

        animate()

    @staticmethod
    def slide_in(widget, direction="left", duration=400, distance=50):
        """Slide in animation"""
        # This would implement actual sliding animation
        # For now, just show the widget
        pass

    @staticmethod
    def pulse(widget, color="#DC0003", duration=1000):
        """Pulse effect animation"""
        original_bg = widget.cget("bg") if hasattr(widget, "cget") else None

        def animate(step=0):
            if step <= 30:
                try:
                    # Simple pulse simulation
                    if hasattr(widget, "configure"):
                        if step < 15:
                            widget.configure(relief="raised")
                        else:
                            widget.configure(relief="flat")
                    widget.after(duration // 30, lambda: animate(step + 1))
                except:
                    pass

        animate()


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Modern Widgets Demo")
    root.geometry("800x600")

    from ..themes.theme_manager import ModernThemeManager

    theme_manager = ModernThemeManager()
    theme_manager.apply_theme(root, "denso_corporate")

    # Demo different widgets
    main_frame = tk.Frame(root, bg=theme_manager.get_theme().surface)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Modern buttons
    btn_frame = tk.Frame(main_frame, bg=theme_manager.get_theme().surface)
    btn_frame.pack(fill="x", pady=10)

    ModernButton(
        btn_frame, "Primary Button", "🚀", "Primary", theme_manager=theme_manager
    ).pack(side="left", padx=5)
    ModernButton(
        btn_frame, "Secondary", "⚙️", "Secondary", theme_manager=theme_manager
    ).pack(side="left", padx=5)
    ModernButton(
        btn_frame, "Success", "✅", "Success", theme_manager=theme_manager
    ).pack(side="left", padx=5)

    # Progress bar
    progress = ModernProgressBar(main_frame, theme_manager)
    progress.pack(fill="x", pady=10)
    progress.set_value(75)

    # Toggle switch
    toggle = ModernToggleSwitch(main_frame, theme_manager, "Enable Feature")
    toggle.pack(pady=10)

    # Metric card
    metric_config = {
        "title": "Demo Metric",
        "icon": "📊",
        "value_func": lambda: "1,234",
        "change": "+15%",
        "trend": "up",
        "color": "primary",
    }

    metric = MetricCard(main_frame, theme_manager, metric_config)
    metric.pack(fill="x", pady=10)

    # Notification button
    def show_demo_notification():
        show_notification(root, "This is a demo notification!", "success")

    ModernButton(
        main_frame,
        "Show Notification",
        "🔔",
        "Ghost",
        show_demo_notification,
        theme_manager,
    ).pack(pady=10)

    root.mainloop()
