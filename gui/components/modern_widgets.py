"""
gui/components/modern_widgets.py
Modern Interactive Widgets with Animations & Micro-interactions
"""

import tkinter as tk
import math
import time
from typing import Callable, Optional


class AnimatedButton:
    """Modern button with smooth animations and effects"""

    def __init__(
        self,
        parent,
        text: str,
        command: Optional[Callable] = None,
        style: str = "primary",
        size: str = "medium",
        **kwargs,
    ):
        self.parent = parent
        self.text = text
        self.command = command
        self.style = style
        self.size = size

        # Animation state
        self.is_animating = False
        self.animation_frame = 0
        self.hover_scale = 1.0

        # Style configurations
        self.styles = {
            "primary": {"bg": "#DC0003", "fg": "white", "hover_bg": "#FF1F22"},
            "secondary": {"bg": "#6C757D", "fg": "white", "hover_bg": "#545B62"},
            "success": {"bg": "#28A745", "fg": "white", "hover_bg": "#34CE57"},
            "danger": {"bg": "#DC3545", "fg": "white", "hover_bg": "#E4606D"},
            "outline": {"bg": "transparent", "fg": "#DC0003", "hover_bg": "#DC0003"},
        }

        self.sizes = {
            "small": {"font": ("Segoe UI", 9), "padding": (10, 6)},
            "medium": {"font": ("Segoe UI", 10), "padding": (15, 10)},
            "large": {"font": ("Segoe UI", 12, "bold"), "padding": (20, 15)},
        }

        self._create_button()

    def _create_button(self):
        """Create the animated button"""
        style_config = self.styles[self.style]
        size_config = self.sizes[self.size]

        # Create main button frame
        self.button_frame = tk.Frame(self.parent, bg=style_config["bg"])
        self.button_frame.pack_propagate(False)

        # Create button label
        self.button_label = tk.Label(
            self.button_frame,
            text=self.text,
            bg=style_config["bg"],
            fg=style_config["fg"],
            font=size_config["font"],
            cursor="hand2",
        )
        self.button_label.pack(
            padx=size_config["padding"][0], pady=size_config["padding"][1]
        )

        # Bind events
        self._bind_events()

        # Start pulse animation for primary buttons
        if self.style == "primary":
            self._start_pulse_animation()

    def _bind_events(self):
        """Bind mouse events for animations"""
        widgets = [self.button_frame, self.button_label]

        for widget in widgets:
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)
            widget.bind("<Button-1>", self._on_click)
            widget.bind("<ButtonRelease-1>", self._on_release)

    def _on_enter(self, event):
        """Handle mouse enter with smooth animation"""
        self._animate_hover(True)

    def _on_leave(self, event):
        """Handle mouse leave with smooth animation"""
        self._animate_hover(False)

    def _on_click(self, event):
        """Handle click with press animation"""
        self._animate_press()

    def _on_release(self, event):
        """Handle release and execute command"""
        if self.command:
            self.command()

    def _animate_hover(self, entering: bool):
        """Animate hover effect"""
        target_scale = 1.05 if entering else 1.0
        style_config = self.styles[self.style]
        target_color = style_config["hover_bg"] if entering else style_config["bg"]

        def animate_step():
            # Scale animation
            if entering:
                self.hover_scale = min(target_scale, self.hover_scale + 0.01)
            else:
                self.hover_scale = max(target_scale, self.hover_scale - 0.01)

            # Color animation would require more complex implementation
            self.button_frame.configure(bg=target_color)
            self.button_label.configure(bg=target_color)

            if abs(self.hover_scale - target_scale) > 0.001:
                self.button_frame.after(16, animate_step)  # ~60fps

        animate_step()

    def _animate_press(self):
        """Animate button press effect"""
        original_relief = self.button_frame.cget("relief")

        # Press down effect
        self.button_frame.configure(relief="sunken")
        self.button_frame.after(
            100, lambda: self.button_frame.configure(relief=original_relief)
        )

        # Add ripple effect
        self._create_ripple_effect()

    def _create_ripple_effect(self):
        """Create ripple effect on click"""
        # Create temporary canvas for ripple
        ripple_canvas = tk.Canvas(
            self.button_frame, highlightthickness=0, bg=self.styles[self.style]["bg"]
        )
        ripple_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # Animate ripple expansion
        max_radius = 50
        steps = 10

        def animate_ripple(step=0):
            if step >= steps:
                ripple_canvas.destroy()
                return

            ripple_canvas.delete("ripple")
            radius = (step / steps) * max_radius
            alpha = 1 - (step / steps)

            # Draw ripple circle
            center_x = ripple_canvas.winfo_width() // 2
            center_y = ripple_canvas.winfo_height() // 2

            ripple_canvas.create_oval(
                center_x - radius,
                center_y - radius,
                center_x + radius,
                center_y + radius,
                outline="white",
                width=2,
                tags="ripple",
            )

            ripple_canvas.after(30, lambda: animate_ripple(step + 1))

        ripple_canvas.after(10, animate_ripple)

    def _start_pulse_animation(self):
        """Start subtle pulse animation for primary buttons"""

        def pulse():
            if not self.is_animating:
                current_time = time.time()
                intensity = 0.95 + 0.05 * math.sin(current_time * 2)

                # Subtle color pulse effect would go here
                self.button_frame.after(50, pulse)

        pulse()

    def pack(self, **kwargs):
        """Pack the button"""
        self.button_frame.pack(**kwargs)

    def grid(self, **kwargs):
        """Grid the button"""
        self.button_frame.grid(**kwargs)

    def place(self, **kwargs):
        """Place the button"""
        self.button_frame.place(**kwargs)


class ModernProgressBar:
    """Modern progress bar with smooth animations"""

    def __init__(
        self,
        parent,
        width: int = 300,
        height: int = 6,
        color: str = "#DC0003",
        bg_color: str = "#E9ECEF",
    ):
        self.parent = parent
        self.width = width
        self.height = height
        self.color = color
        self.bg_color = bg_color
        self.progress = 0.0
        self.target_progress = 0.0

        self._create_progress_bar()

    def _create_progress_bar(self):
        """Create the progress bar"""
        self.canvas = tk.Canvas(
            self.parent,
            width=self.width,
            height=self.height,
            highlightthickness=0,
            bg=self.parent.cget("bg"),
        )

        # Draw background
        self.bg_rect = self.canvas.create_rectangle(
            0, 0, self.width, self.height, fill=self.bg_color, outline=""
        )

        # Draw progress
        self.progress_rect = self.canvas.create_rectangle(
            0, 0, 0, self.height, fill=self.color, outline=""
        )

    def set_progress(self, value: float):
        """Set progress with smooth animation"""
        self.target_progress = max(0.0, min(1.0, value))
        self._animate_to_target()

    def _animate_to_target(self):
        """Animate progress to target value"""
        diff = self.target_progress - self.progress

        if abs(diff) < 0.001:
            self.progress = self.target_progress
            self._update_visual()
            return

        # Smooth easing
        self.progress += diff * 0.1
        self._update_visual()

        self.canvas.after(16, self._animate_to_target)  # ~60fps

    def _update_visual(self):
        """Update visual representation"""
        progress_width = self.width * self.progress
        self.canvas.coords(self.progress_rect, 0, 0, progress_width, self.height)

    def pack(self, **kwargs):
        self.canvas.pack(**kwargs)

    def grid(self, **kwargs):
        self.canvas.grid(**kwargs)


class FloatingNotification:
    """Modern floating notification with animations"""

    def __init__(self, parent, message: str, type: str = "info", duration: int = 3000):
        self.parent = parent
        self.message = message
        self.type = type
        self.duration = duration

        # Notification styles
        self.styles = {
            "info": {"bg": "#17A2B8", "fg": "white", "icon": "ℹ️"},
            "success": {"bg": "#28A745", "fg": "white", "icon": "✅"},
            "warning": {"bg": "#FFC107", "fg": "black", "icon": "⚠️"},
            "error": {"bg": "#DC3545", "fg": "white", "icon": "❌"},
        }

        self._create_notification()
        self._animate_in()

    def _create_notification(self):
        """Create notification widget"""
        style = self.styles[self.type]

        # Main notification frame
        self.notification = tk.Toplevel(self.parent)
        self.notification.overrideredirect(True)  # Remove window decorations
        self.notification.attributes("-topmost", True)

        # Configure background
        self.notification.configure(bg=style["bg"])

        # Content frame
        content = tk.Frame(self.notification, bg=style["bg"])
        content.pack(padx=15, pady=10)

        # Icon
        icon_label = tk.Label(
            content,
            text=style["icon"],
            bg=style["bg"],
            fg=style["fg"],
            font=("Segoe UI", 14),
        )
        icon_label.pack(side="left", padx=(0, 10))

        # Message
        msg_label = tk.Label(
            content,
            text=self.message,
            bg=style["bg"],
            fg=style["fg"],
            font=("Segoe UI", 10),
            wraplength=300,
        )
        msg_label.pack(side="left")

        # Position notification
        self._position_notification()

        # Auto-dismiss
        self.notification.after(self.duration, self._animate_out)

    def _position_notification(self):
        """Position notification in top-right corner"""
        self.notification.update_idletasks()

        # Get screen dimensions
        screen_width = self.notification.winfo_screenwidth()
        screen_height = self.notification.winfo_screenheight()

        # Get notification dimensions
        notif_width = self.notification.winfo_reqwidth()
        notif_height = self.notification.winfo_reqheight()

        # Position in top-right
        x = screen_width - notif_width - 20
        y = 20

        self.notification.geometry(f"+{x}+{y}")

    def _animate_in(self):
        """Animate notification sliding in"""
        start_x = self.notification.winfo_screenwidth()
        end_x = (
            self.notification.winfo_screenwidth()
            - self.notification.winfo_reqwidth()
            - 20
        )

        def slide_in(step=0):
            if step >= 20:
                return

            progress = step / 20
            current_x = int(start_x + (end_x - start_x) * self._ease_out(progress))

            self.notification.geometry(f"+{current_x}+20")
            self.notification.after(16, lambda: slide_in(step + 1))

        slide_in()

    def _animate_out(self):
        """Animate notification sliding out"""
        start_x = self.notification.winfo_x()
        end_x = self.notification.winfo_screenwidth()

        def slide_out(step=0):
            if step >= 20:
                self.notification.destroy()
                return

            progress = step / 20
            current_x = int(start_x + (end_x - start_x) * self._ease_in(progress))

            self.notification.geometry(f"+{current_x}+20")
            self.notification.after(16, lambda: slide_out(step + 1))

        slide_out()

    def _ease_out(self, t):
        """Ease-out animation curve"""
        return 1 - (1 - t) ** 3

    def _ease_in(self, t):
        """Ease-in animation curve"""
        return t**3


class ModernCard:
    """Modern card component with hover effects"""

    def __init__(
        self,
        parent,
        title: str = "",
        content: str = "",
        accent_color: str = "#DC0003",
        **kwargs,
    ):
        self.parent = parent
        self.title = title
        self.content = content
        self.accent_color = accent_color

        self._create_card()

    def _create_card(self):
        """Create the card widget"""
        # Main card frame with shadow effect
        self.card_frame = tk.Frame(
            self.parent,
            bg="white",
            relief="flat",
            borderwidth=1,
            highlightbackground="#E9ECEF",
            highlightthickness=1,
        )

        # Accent bar
        accent_bar = tk.Frame(self.card_frame, bg=self.accent_color, height=4)
        accent_bar.pack(fill="x")

        # Content area
        content_frame = tk.Frame(self.card_frame, bg="white")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        if self.title:
            title_label = tk.Label(
                content_frame,
                text=self.title,
                font=("Segoe UI", 14, "bold"),
                fg="#2C3E50",
                bg="white",
            )
            title_label.pack(anchor="w", pady=(0, 10))

        # Content
        if self.content:
            content_label = tk.Label(
                content_frame,
                text=self.content,
                font=("Segoe UI", 10),
                fg="#6C757D",
                bg="white",
                justify="left",
                wraplength=250,
            )
            content_label.pack(anchor="w")

        # Add hover effects
        self._add_hover_effects()

    def _add_hover_effects(self):
        """Add hover animations"""

        def on_enter(e):
            self.card_frame.configure(highlightbackground=self.accent_color)

        def on_leave(e):
            self.card_frame.configure(highlightbackground="#E9ECEF")

        # Bind to all widgets in card
        widgets = [self.card_frame] + list(self._get_all_children(self.card_frame))
        for widget in widgets:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    def _get_all_children(self, widget):
        """Get all child widgets recursively"""
        children = []
        for child in widget.winfo_children():
            children.append(child)
            children.extend(self._get_all_children(child))
        return children

    def pack(self, **kwargs):
        self.card_frame.pack(**kwargs)

    def grid(self, **kwargs):
        self.card_frame.grid(**kwargs)

    def add_button(self, text: str, command: Callable):
        """Add action button to card"""
        button = AnimatedButton(
            self.card_frame, text=text, command=command, style="outline", size="small"
        )
        button.pack(pady=(10, 0))


class ModernTooltip:
    """Modern tooltip with smooth animations"""

    def __init__(self, widget, text: str, delay: int = 500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip_window = None
        self.after_id = None

        self.widget.bind("<Enter>", self._on_enter)
        self.widget.bind("<Leave>", self._on_leave)

    def _on_enter(self, event):
        """Handle mouse enter"""
        self.after_id = self.widget.after(self.delay, self._show_tooltip)

    def _on_leave(self, event):
        """Handle mouse leave"""
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
        self._hide_tooltip()

    def _show_tooltip(self):
        """Show tooltip with animation"""
        if self.tooltip_window:
            return

        x = self.widget.winfo_rootx() + self.widget.winfo_width() // 2
        y = self.widget.winfo_rooty() - 30

        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        # Style tooltip
        label = tk.Label(
            self.tooltip_window,
            text=self.text,
            background="#2C3E50",
            foreground="white",
            font=("Segoe UI", 9),
            padx=8,
            pady=4,
            relief="flat",
        )
        label.pack()

        # Animate fade in
        self._animate_fade_in()

    def _hide_tooltip(self):
        """Hide tooltip"""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

    def _animate_fade_in(self):
        """Animate tooltip fade in"""
        # Simple fade effect using alpha (if supported)
        try:
            self.tooltip_window.attributes("-alpha", 0.0)

            def fade_in(alpha=0.0):
                if alpha >= 1.0:
                    return
                alpha += 0.1
                self.tooltip_window.attributes("-alpha", alpha)
                self.tooltip_window.after(20, lambda: fade_in(alpha))

            fade_in()
        except:
            # Fallback if alpha not supported
            pass


class ModernSpinner:
    """Modern loading spinner"""

    def __init__(self, parent, size: int = 32, color: str = "#DC0003"):
        self.parent = parent
        self.size = size
        self.color = color
        self.angle = 0
        self.is_spinning = False

        self._create_spinner()

    def _create_spinner(self):
        """Create spinner widget"""
        self.canvas = tk.Canvas(
            self.parent,
            width=self.size,
            height=self.size,
            highlightthickness=0,
            bg=self.parent.cget("bg"),
        )

    def start(self):
        """Start spinning animation"""
        self.is_spinning = True
        self._animate_spin()

    def stop(self):
        """Stop spinning animation"""
        self.is_spinning = False
        self.canvas.delete("spinner")

    def _animate_spin(self):
        """Animate spinner rotation"""
        if not self.is_spinning:
            return

        self.canvas.delete("spinner")

        # Draw spinning arcs
        center = self.size // 2
        radius = center - 4

        for i in range(8):
            angle = self.angle + i * 45
            alpha = 1.0 - (i * 0.125)

            # Calculate arc position
            start_angle = angle
            extent = 30

            # Draw arc segment
            self.canvas.create_arc(
                center - radius,
                center - radius,
                center + radius,
                center + radius,
                start=start_angle,
                extent=extent,
                outline=self.color,
                width=3,
                style="arc",
                tags="spinner",
            )

        self.angle = (self.angle + 10) % 360
        self.canvas.after(50, self._animate_spin)

    def pack(self, **kwargs):
        self.canvas.pack(**kwargs)

    def grid(self, **kwargs):
        self.canvas.grid(**kwargs)


class ModernToggleSwitch:
    """Modern toggle switch with smooth animation"""

    def __init__(
        self, parent, initial_state: bool = False, on_change: Optional[Callable] = None
    ):
        self.parent = parent
        self.state = initial_state
        self.on_change = on_change
        self.is_animating = False

        # Colors
        self.on_color = "#28A745"
        self.off_color = "#6C757D"
        self.knob_color = "white"

        self._create_switch()

    def _create_switch(self):
        """Create toggle switch"""
        self.canvas = tk.Canvas(
            self.parent,
            width=50,
            height=24,
            highlightthickness=0,
            bg=self.parent.cget("bg"),
            cursor="hand2",
        )

        # Draw switch background
        self.bg_rect = self.canvas.create_rectangle(
            2,
            2,
            48,
            22,
            fill=self.on_color if self.state else self.off_color,
            outline="",
            width=0,
        )

        # Draw switch knob
        knob_x = 36 if self.state else 14
        self.knob = self.canvas.create_oval(
            knob_x - 8,
            4,
            knob_x + 8,
            20,
            fill=self.knob_color,
            outline="#CCCCCC",
            width=1,
        )

        # Bind click event
        self.canvas.bind("<Button-1>", self._on_click)

    def _on_click(self, event):
        """Handle toggle click"""
        if self.is_animating:
            return

        self.toggle()

    def toggle(self):
        """Toggle switch state with animation"""
        self.state = not self.state
        self._animate_toggle()

        if self.on_change:
            self.on_change(self.state)

    def _animate_toggle(self):
        """Animate toggle transition"""
        self.is_animating = True

        # Animation parameters
        start_x = 36 if not self.state else 14
        end_x = 14 if not self.state else 36
        start_color = self.on_color if not self.state else self.off_color
        end_color = self.off_color if not self.state else self.on_color

        steps = 15

        def animate_step(step=0):
            if step >= steps:
                self.is_animating = False
                return

            progress = step / steps

            # Ease-out animation
            eased_progress = 1 - (1 - progress) ** 3

            # Interpolate knob position
            current_x = start_x + (end_x - start_x) * eased_progress

            # Update knob position
            self.canvas.coords(self.knob, current_x - 8, 4, current_x + 8, 20)

            # Update background color (simplified)
            if step > steps // 2:
                self.canvas.itemconfig(self.bg_rect, fill=end_color)

            self.canvas.after(16, lambda: animate_step(step + 1))

        animate_step()

    def set_state(self, state: bool):
        """Set switch state without animation"""
        if self.state != state:
            self.toggle()

    def pack(self, **kwargs):
        self.canvas.pack(**kwargs)

    def grid(self, **kwargs):
        self.canvas.grid(**kwargs)
