"""
gui/components/splash_screen.py
Modern DENSO Splash Screen with Animations
"""

import tkinter as tk
import math
import time
from typing import Callable, Optional


class DENSOSplashScreen:
    """Modern animated splash screen for DENSO888"""

    def __init__(self, callback: Optional[Callable] = None, duration: int = 3000):
        self.callback = callback
        self.duration = duration
        self.splash = None
        self.progress = 0
        self.animation_running = True

        self._create_splash()
        self._start_animations()

    def _create_splash(self):
        """Create splash screen window"""
        self.splash = tk.Toplevel()
        self.splash.title("DENSO888")
        self.splash.geometry("500x350")
        self.splash.resizable(False, False)
        self.splash.overrideredirect(True)  # Remove window decorations

        # Center on screen
        self._center_window()

        # Configure background gradient
        self.splash.configure(bg="#1a1a1a")

        # Create main canvas
        self.canvas = tk.Canvas(
            self.splash, width=500, height=350, bg="#1a1a1a", highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # Draw initial elements
        self._draw_background()
        self._draw_logo()
        self._draw_text_elements()
        self._draw_progress_bar()

    def _center_window(self):
        """Center splash screen on screen"""
        self.splash.update_idletasks()
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()

        x = (screen_width - 500) // 2
        y = (screen_height - 350) // 2

        self.splash.geometry(f"500x350+{x}+{y}")

    def _draw_background(self):
        """Draw animated background"""
        # Gradient background
        for i in range(350):
            ratio = i / 350
            # Dark gradient from top to bottom
            gray_val = int(26 + ratio * 20)  # From #1a1a1a to #2e2e2e
            color = f"#{gray_val:02x}{gray_val:02x}{gray_val:02x}"

            self.canvas.create_line(0, i, 500, i, fill=color, tags="background")

        # Animated particles
        self.particles = []
        for _ in range(15):
            particle = {
                "x": float(500 * (_ * 0.1)),
                "y": float(350 * ((_ * 7) % 10 / 10)),
                "vx": ((_ * 3) % 5 - 2) * 0.5,
                "vy": ((_ * 5) % 5 - 2) * 0.3,
                "size": 2 + (_ % 3),
            }
            self.particles.append(particle)

    def _draw_logo(self):
        """Draw DENSO logo with animation"""
        # Main logo circle
        self.logo_circle = self.canvas.create_oval(
            200, 80, 300, 180, fill="#DC0003", outline="#FF3333", width=3, tags="logo"
        )

        # DENSO text in logo
        self.logo_text = self.canvas.create_text(
            250,
            130,
            text="D888",
            font=("Segoe UI", 24, "bold"),
            fill="white",
            tags="logo",
        )

        # Outer glow effect
        for i in range(5):
            alpha = 0.1 - i * 0.02
            radius_offset = i * 3
            self.canvas.create_oval(
                200 - radius_offset,
                80 - radius_offset,
                300 + radius_offset,
                180 + radius_offset,
                outline="#DC0003",
                width=1,
                tags="glow",
            )

    def _draw_text_elements(self):
        """Draw text elements"""
        # Main title
        self.title = self.canvas.create_text(
            250,
            220,
            text="🏭 DENSO888",
            font=("Segoe UI", 20, "bold"),
            fill="white",
            tags="title",
        )

        # Subtitle
        self.subtitle = self.canvas.create_text(
            250,
            245,
            text="Excel to SQL Management System",
            font=("Segoe UI", 11),
            fill="#CCCCCC",
            tags="subtitle",
        )

        # Version
        self.version = self.canvas.create_text(
            250,
            265,
            text="Version 2.0.0 - Modern Edition",
            font=("Segoe UI", 9),
            fill="#888888",
            tags="version",
        )

        # Creator info
        self.creator = self.canvas.create_text(
            250,
            290,
            text="Created by Thammaphon Chittasuwanna (SDM)",
            font=("Segoe UI", 8),
            fill="#666666",
            tags="creator",
        )

        # Loading text
        self.loading_text = self.canvas.create_text(
            250,
            315,
            text="กำลังเริ่มต้นระบบ...",
            font=("Segoe UI", 9),
            fill="#AAAAAA",
            tags="loading",
        )

    def _draw_progress_bar(self):
        """Draw animated progress bar"""
        # Progress bar background
        self.progress_bg = self.canvas.create_rectangle(
            150, 325, 350, 335, fill="#333333", outline="#555555", tags="progress"
        )

        # Progress bar fill
        self.progress_fill = self.canvas.create_rectangle(
            150, 325, 150, 335, fill="#DC0003", outline="", tags="progress"
        )

    def _start_animations(self):
        """Start all animations"""
        self._animate_logo()
        self._animate_particles()
        self._animate_progress()

        # Auto close after duration
        self.splash.after(self.duration, self._close_splash)

    def _animate_logo(self):
        """Animate logo pulsing effect"""
        if not self.animation_running:
            return

        current_time = time.time()
        scale = 1 + 0.05 * math.sin(current_time * 3)

        # Create pulsing effect by changing outline width
        outline_width = int(3 + 2 * math.sin(current_time * 2))
        self.canvas.itemconfig(self.logo_circle, width=outline_width)

        self.splash.after(50, self._animate_logo)

    def _animate_particles(self):
        """Animate background particles"""
        if not self.animation_running:
            return

        self.canvas.delete("particles")

        for particle in self.particles:
            # Update position
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]

            # Wrap around edges
            if particle["x"] < 0:
                particle["x"] = 500
            elif particle["x"] > 500:
                particle["x"] = 0

            if particle["y"] < 0:
                particle["y"] = 350
            elif particle["y"] > 350:
                particle["y"] = 0

            # Draw particle
            self.canvas.create_oval(
                particle["x"] - particle["size"],
                particle["y"] - particle["size"],
                particle["x"] + particle["size"],
                particle["y"] + particle["size"],
                fill="#444444",
                outline="",
                tags="particles",
            )

        self.splash.after(50, self._animate_particles)

    def _animate_progress(self):
        """Animate progress bar"""
        if not self.animation_running:
            return

        # Update progress
        self.progress += 2
        if self.progress > 100:
            self.progress = 100

        # Update progress bar
        progress_width = (self.progress / 100) * 200
        self.canvas.coords(self.progress_fill, 150, 325, 150 + progress_width, 335)

        # Update loading text based on progress
        loading_messages = [
            "กำลังเริ่มต้นระบบ...",
            "กำลังโหลดโมดูล...",
            "กำลังเชื่อมต่อฐานข้อมูล...",
            "กำลังตั้งค่าธีม...",
            "เกือบเสร็จแล้ว...",
            "พร้อมใช้งาน!",
        ]

        message_index = min(self.progress // 20, len(loading_messages) - 1)
        self.canvas.itemconfig(self.loading_text, text=loading_messages[message_index])

        if self.progress < 100:
            self.splash.after(30, self._animate_progress)

    def _close_splash(self):
        """Close splash screen and call callback"""
        self.animation_running = False

        # Fade out effect
        self._fade_out()

    def _fade_out(self, alpha=1.0):
        """Fade out animation"""
        if alpha <= 0:
            self.splash.destroy()
            if self.callback:
                self.callback()
            return

        # Simulate fade by changing colors to darker
        fade_factor = alpha

        # Update text colors
        gray_val = int(255 * fade_factor)
        fade_color = f"#{gray_val:02x}{gray_val:02x}{gray_val:02x}"

        try:
            self.canvas.itemconfig(self.title, fill=fade_color)
            self.canvas.itemconfig(self.subtitle, fill=fade_color)
            self.canvas.itemconfig(self.version, fill=fade_color)
            self.canvas.itemconfig(self.creator, fill=fade_color)
            self.canvas.itemconfig(self.loading_text, fill=fade_color)
        except:
            pass

        # Continue fading
        self.splash.after(50, lambda: self._fade_out(alpha - 0.1))


# Factory function for easy use
def show_splash_screen(callback: Optional[Callable] = None, duration: int = 3000):
    """Show splash screen with callback"""
    return DENSOSplashScreen(callback, duration)
