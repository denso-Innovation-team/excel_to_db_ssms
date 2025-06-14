"""
gui/components/modern_dashboard.py
Modern Dashboard with 3D Elements, Animations & DENSO Branding
"""

import tkinter as tk
import math
import time


class ModernDashboard:
    """Modern dashboard with DENSO branding and interactive elements"""

    def __init__(self, parent, theme_manager, config):
        self.parent = parent
        self.theme_manager = theme_manager
        self.config = config
        self.palette = theme_manager.get_current_palette()

        # Animation variables
        self.animation_running = False
        self.particles = []

        # Creator info
        self.creator_info = {
            "name": "Thammaphon Chittasuwanna",
            "title": "SDM | Innovation",
            "nickname": "เฮียตอมจัดหั้ย!!!",
            "motto": "Making Excel to SQL migration simple and powerful! 🚀",
        }

        self._create_dashboard()

    def _create_dashboard(self):
        """Create modern dashboard layout"""
        # Main container with gradient background
        self.main_frame = self._create_gradient_container()

        # Create header with DENSO branding
        self._create_branded_header()

        # Create main content area
        self._create_content_area()

        # Create footer with creator info
        self._create_creator_footer()

        # Start background animations
        self._start_background_animation()

    def _create_gradient_container(self) -> tk.Frame:
        """Create main container with gradient background"""
        container = tk.Frame(self.parent, bg=self.palette.background)
        container.pack(fill="both", expand=True)

        # Create gradient canvas background
        self.bg_canvas = tk.Canvas(container, highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)

        # Bind resize event for responsive gradient
        self.bg_canvas.bind("<Configure>", self._on_canvas_resize)

        return container

    def _on_canvas_resize(self, event):
        """Handle canvas resize for responsive design"""
        self._draw_gradient_background()
        self._draw_floating_particles()

    def _draw_gradient_background(self):
        """Draw animated gradient background"""
        self.bg_canvas.delete("gradient")

        width = self.bg_canvas.winfo_width()
        height = self.bg_canvas.winfo_height()

        if width <= 1 or height <= 1:
            return

        # Create gradient effect
        steps = 50
        for i in range(steps):
            ratio = i / steps

            # Interpolate between primary and secondary colors
            r1, g1, b1 = self.theme_manager._hex_to_rgb(self.palette.primary)
            r2, g2, b2 = self.theme_manager._hex_to_rgb(self.palette.background)

            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)

            color = f"#{r:02x}{g:02x}{b:02x}"

            y1 = int(height * i / steps)
            y2 = int(height * (i + 1) / steps)

            self.bg_canvas.create_rectangle(
                0, y1, width, y2, fill=color, outline="", tags="gradient"
            )

    def _create_branded_header(self):
        """Create header with DENSO logo and branding"""
        header_frame = tk.Frame(self.bg_canvas, bg="", height=80)
        header_window = self.bg_canvas.create_window(
            0, 0, anchor="nw", window=header_frame
        )

        # DENSO Logo section
        logo_frame = tk.Frame(header_frame, bg="")
        logo_frame.pack(side="left", padx=20, pady=10)

        # Logo placeholder (would load actual DENSO logo)
        self._create_denso_logo(logo_frame)

        # App title with animation
        title_frame = tk.Frame(header_frame, bg="")
        title_frame.pack(side="left", padx=20, pady=10, fill="both", expand=True)

        self.title_label = tk.Label(
            title_frame,
            text="🏭 DENSO888",
            font=("Segoe UI", 28, "bold"),
            fg=self.palette.text_primary,
            bg="",
        )
        self.title_label.pack(anchor="w")

        subtitle = tk.Label(
            title_frame,
            text="Excel to SQL Management System - Modern Edition",
            font=("Segoe UI", 12),
            fg=self.palette.text_secondary,
            bg="",
        )
        subtitle.pack(anchor="w", pady=(0, 5))

        # Status indicators
        self._create_status_indicators(header_frame)

        # Update header window size
        self.bg_canvas.update_idletasks()
        self.bg_canvas.itemconfig(header_window, width=self.bg_canvas.winfo_width())

    def _create_denso_logo(self, parent):
        """Create animated DENSO logo"""
        logo_canvas = tk.Canvas(
            parent, width=60, height=60, highlightthickness=0, bg=""
        )
        logo_canvas.pack(side="left", padx=(0, 15))

        # Draw DENSO-inspired logo with animation
        self._draw_animated_logo(logo_canvas)

        return logo_canvas

    def _draw_animated_logo(self, canvas):
        """Draw animated DENSO logo"""
        canvas.delete("logo")

        # Draw circular logo base
        canvas.create_oval(
            5,
            5,
            55,
            55,
            fill=self.palette.primary,
            outline=self.palette.primary_dark,
            width=2,
            tags="logo",
        )

        # Draw "D" letter in modern style
        canvas.create_text(
            30, 30, text="D", font=("Segoe UI", 24, "bold"), fill="white", tags="logo"
        )

        # Add pulsing animation
        self._animate_logo_pulse(canvas)

    def _animate_logo_pulse(self, canvas):
        """Create pulsing animation for logo"""

        def pulse():
            current_time = time.time()
            scale = 1 + 0.1 * math.sin(current_time * 3)

            # This would require more complex canvas transformations
            # For now, we'll use color animation
            alpha = int(255 * (0.7 + 0.3 * math.sin(current_time * 2)))

            if self.animation_running:
                canvas.after(50, pulse)

        pulse()

    def _create_status_indicators(self, parent):
        """Create status indicators in header"""
        status_frame = tk.Frame(parent, bg="")
        status_frame.pack(side="right", padx=20, pady=10)

        # Connection status
        conn_frame = tk.Frame(status_frame, bg="")
        conn_frame.pack(pady=2)

        self.conn_indicator = tk.Label(
            conn_frame,
            text="🟢 Connected",
            font=("Segoe UI", 10),
            fg=self.palette.success,
            bg="",
        )
        self.conn_indicator.pack(side="left")

        # User info
        user_frame = tk.Frame(status_frame, bg="")
        user_frame.pack(pady=2)

        user_label = tk.Label(
            user_frame,
            text="👤 Admin User",
            font=("Segoe UI", 10),
            fg=self.palette.text_primary,
            bg="",
        )
        user_label.pack(side="left")

    def _create_content_area(self):
        """Create main content area with cards"""
        content_frame = tk.Frame(self.bg_canvas, bg="")
        content_window = self.bg_canvas.create_window(
            0, 100, anchor="nw", window=content_frame
        )

        # Create responsive grid of feature cards
        self._create_feature_cards(content_frame)

        # Create quick stats section
        self._create_quick_stats(content_frame)

        # Update content window size
        self.bg_canvas.update_idletasks()
        self.bg_canvas.itemconfig(content_window, width=self.bg_canvas.winfo_width())

    def _create_feature_cards(self, parent):
        """Create feature cards with glassmorphism effect"""
        cards_frame = tk.Frame(parent, bg="")
        cards_frame.pack(fill="both", expand=True, padx=40, pady=20)

        # Configure grid
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)
        cards_frame.grid_columnconfigure(2, weight=1)

        # Feature cards data
        features = [
            {
                "icon": "📊",
                "title": "Smart Data Import",
                "desc": "AI-powered Excel to SQL conversion with auto-detection",
                "color": self.palette.primary,
            },
            {
                "icon": "🎲",
                "title": "Mock Data Generator",
                "desc": "Generate realistic test data for development",
                "color": self.palette.accent,
            },
            {
                "icon": "🔐",
                "title": "Enterprise Security",
                "desc": "Multi-factor authentication and audit logging",
                "color": self.palette.success,
            },
            {
                "icon": "📈",
                "title": "Real-time Analytics",
                "desc": "Live performance monitoring and insights",
                "color": self.palette.warning,
            },
            {
                "icon": "🤖",
                "title": "AI Insights",
                "desc": "Machine learning powered data analysis",
                "color": "#8B5CF6",
            },
            {
                "icon": "☁️",
                "title": "Cloud Sync",
                "desc": "Multi-platform data synchronization",
                "color": "#06B6D4",
            },
        ]

        for i, feature in enumerate(features):
            row = i // 3
            col = i % 3

            card = self._create_glass_card(cards_frame, feature)
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

    def _create_glass_card(self, parent, feature_data) -> tk.Frame:
        """Create glassmorphism effect card"""
        # Main card frame
        card = tk.Frame(
            parent,
            bg=self.palette.surface,
            relief="flat",
            borderwidth=1,
            highlightbackground=self.palette.border,
            highlightthickness=1,
        )

        # Card content
        content_frame = tk.Frame(card, bg=self.palette.surface)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Icon with background circle
        icon_frame = tk.Frame(content_frame, bg=self.palette.surface)
        icon_frame.pack(pady=(0, 15))

        icon_bg = tk.Label(
            icon_frame,
            text=feature_data["icon"],
            font=("Segoe UI", 24),
            bg=feature_data["color"],
            fg="white",
            width=3,
            height=1,
        )
        icon_bg.pack()

        # Title
        title_label = tk.Label(
            content_frame,
            text=feature_data["title"],
            font=("Segoe UI", 14, "bold"),
            fg=self.palette.text_primary,
            bg=self.palette.surface,
        )
        title_label.pack(pady=(0, 10))

        # Description
        desc_label = tk.Label(
            content_frame,
            text=feature_data["desc"],
            font=("Segoe UI", 10),
            fg=self.palette.text_secondary,
            bg=self.palette.surface,
            wraplength=200,
            justify="center",
        )
        desc_label.pack()

        # Add hover effects
        self._add_card_hover_effects(card, feature_data["color"])

        return card

    def _add_card_hover_effects(self, card, accent_color):
        """Add hover animations to cards"""
        original_bg = self.palette.surface

        def on_enter(e):
            card.configure(highlightbackground=accent_color)
            # Add subtle lift effect (visual only)

        def on_leave(e):
            card.configure(highlightbackground=self.palette.border)

        def on_click(e):
            # Add click animation
            self._animate_card_click(card)

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        card.bind("<Button-1>", on_click)

        # Make all child widgets responsive to events
        for child in card.winfo_children():
            child.bind("<Enter>", on_enter)
            child.bind("<Leave>", on_leave)
            child.bind("<Button-1>", on_click)

    def _animate_card_click(self, card):
        """Animate card click with scale effect"""
        # Simple visual feedback
        original_relief = card.cget("relief")
        card.configure(relief="sunken")
        card.after(100, lambda: card.configure(relief=original_relief))

    def _create_quick_stats(self, parent):
        """Create quick statistics section"""
        stats_frame = tk.Frame(parent, bg="")
        stats_frame.pack(fill="x", padx=40, pady=20)

        # Stats title
        title_label = tk.Label(
            stats_frame,
            text="📊 Quick Statistics",
            font=("Segoe UI", 16, "bold"),
            fg=self.palette.text_primary,
            bg="",
        )
        title_label.pack(pady=(0, 15))

        # Stats grid
        stats_grid = tk.Frame(stats_frame, bg="")
        stats_grid.pack(fill="x")

        stats_data = [
            {"label": "Files Processed", "value": "1,234", "change": "+12%"},
            {"label": "Data Records", "value": "2.5M", "change": "+25%"},
            {"label": "Success Rate", "value": "99.8%", "change": "+0.2%"},
            {"label": "Processing Time", "value": "2.3s", "change": "-15%"},
        ]

        for i, stat in enumerate(stats_data):
            stat_card = self._create_stat_card(stats_grid, stat)
            stat_card.grid(row=0, column=i, padx=10, sticky="ew")
            stats_grid.grid_columnconfigure(i, weight=1)

    def _create_stat_card(self, parent, stat_data) -> tk.Frame:
        """Create individual statistics card"""
        card = tk.Frame(
            parent,
            bg=self.palette.surface,
            relief="flat",
            borderwidth=1,
            highlightbackground=self.palette.border,
            highlightthickness=1,
        )

        # Value
        value_label = tk.Label(
            card,
            text=stat_data["value"],
            font=("Segoe UI", 20, "bold"),
            fg=self.palette.primary,
            bg=self.palette.surface,
        )
        value_label.pack(pady=(15, 5))

        # Label
        label_label = tk.Label(
            card,
            text=stat_data["label"],
            font=("Segoe UI", 10),
            fg=self.palette.text_secondary,
            bg=self.palette.surface,
        )
        label_label.pack(pady=(0, 5))

        # Change indicator
        change_color = (
            self.palette.success
            if stat_data["change"].startswith("+")
            else self.palette.danger
        )
        change_label = tk.Label(
            card,
            text=stat_data["change"],
            font=("Segoe UI", 9, "bold"),
            fg=change_color,
            bg=self.palette.surface,
        )
        change_label.pack(pady=(0, 15))

        return card

    def _create_creator_footer(self):
        """Create footer with creator information"""
        footer_frame = tk.Frame(self.bg_canvas, bg="", height=120)
        footer_window = self.bg_canvas.create_window(
            0, -120, anchor="sw", window=footer_frame
        )

        # Creator section with avatar placeholder
        creator_frame = tk.Frame(footer_frame, bg="")
        creator_frame.pack(side="left", padx=40, pady=20)

        # Avatar placeholder
        avatar_frame = tk.Frame(creator_frame, bg="")
        avatar_frame.pack(side="left", padx=(0, 20))

        self._create_creator_avatar(avatar_frame)

        # Creator info
        info_frame = tk.Frame(creator_frame, bg="")
        info_frame.pack(side="left", fill="both", expand=True)

        name_label = tk.Label(
            info_frame,
            text=f"Created by {self.creator_info['name']}",
            font=("Segoe UI", 12, "bold"),
            fg=self.palette.text_primary,
            bg="",
        )
        name_label.pack(anchor="w")

        title_label = tk.Label(
            info_frame,
            text=self.creator_info["title"],
            font=("Segoe UI", 10),
            fg=self.palette.text_secondary,
            bg="",
        )
        title_label.pack(anchor="w")

        nickname_label = tk.Label(
            info_frame,
            text=self.creator_info["nickname"],
            font=("Segoe UI", 10, "italic"),
            fg=self.palette.primary,
            bg="",
        )
        nickname_label.pack(anchor="w", pady=(5, 0))

        motto_label = tk.Label(
            info_frame,
            text=self.creator_info["motto"],
            font=("Segoe UI", 9),
            fg=self.palette.text_secondary,
            bg="",
        )
        motto_label.pack(anchor="w", pady=(5, 0))

        # Version info
        version_frame = tk.Frame(footer_frame, bg="")
        version_frame.pack(side="right", padx=40, pady=20)

        version_label = tk.Label(
            version_frame,
            text="Version 2.0.0 - Modern Edition",
            font=("Segoe UI", 10),
            fg=self.palette.text_secondary,
            bg="",
        )
        version_label.pack()

        # Update footer window size
        self.bg_canvas.update_idletasks()
        self.bg_canvas.itemconfig(footer_window, width=self.bg_canvas.winfo_width())

    def _create_creator_avatar(self, parent):
        """Create creator avatar with modern design"""
        avatar_canvas = tk.Canvas(
            parent, width=80, height=80, highlightthickness=0, bg=""
        )
        avatar_canvas.pack()

        # Draw modern avatar placeholder
        # Outer circle with gradient effect
        avatar_canvas.create_oval(
            5,
            5,
            75,
            75,
            fill=self.palette.primary,
            outline=self.palette.primary_dark,
            width=3,
        )

        # Inner circle
        avatar_canvas.create_oval(15, 15, 65, 65, fill=self.palette.surface, outline="")

        # Initial letters
        avatar_canvas.create_text(
            40, 40, text="TC", font=("Segoe UI", 16, "bold"), fill=self.palette.primary
        )

        return avatar_canvas

    def _start_background_animation(self):
        """Start background particle animation"""
        self.animation_running = True
        self._init_particles()
        self._animate_particles()

    def _init_particles(self):
        """Initialize floating particles"""
        self.particles = []
        for _ in range(20):
            particle = {
                "x": float(
                    self.bg_canvas.winfo_width() * 0.1
                    + (self.bg_canvas.winfo_width() * 0.8)
                    * (hash(str(_)) % 1000)
                    / 1000
                ),
                "y": float(
                    self.bg_canvas.winfo_height() * (hash(str(_ * 2)) % 1000) / 1000
                ),
                "vx": (hash(str(_ * 3)) % 200 - 100) / 10000,
                "vy": (hash(str(_ * 4)) % 200 - 100) / 10000,
                "size": 2 + (hash(str(_ * 5)) % 3),
                "alpha": 0.3 + (hash(str(_ * 6)) % 400) / 1000,
            }
            self.particles.append(particle)

    def _animate_particles(self):
        """Animate floating particles"""
        if not self.animation_running:
            return

        self._update_particles()
        self._draw_floating_particles()
        self.bg_canvas.after(50, self._animate_particles)

    def _update_particles(self):
        """Update particle positions"""
        width = self.bg_canvas.winfo_width()
        height = self.bg_canvas.winfo_height()

        for particle in self.particles:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]

            # Wrap around screen
            if particle["x"] < 0:
                particle["x"] = width
            elif particle["x"] > width:
                particle["x"] = 0

            if particle["y"] < 0:
                particle["y"] = height
            elif particle["y"] > height:
                particle["y"] = 0

    def _draw_floating_particles(self):
        """Draw floating particles"""
        self.bg_canvas.delete("particles")

        for particle in self.particles:
            # Calculate alpha based on distance from center
            center_x = self.bg_canvas.winfo_width() / 2
            center_y = self.bg_canvas.winfo_height() / 2

            distance = math.sqrt(
                (particle["x"] - center_x) ** 2 + (particle["y"] - center_y) ** 2
            )
            max_distance = math.sqrt(center_x**2 + center_y**2)

            alpha = max(0.1, particle["alpha"] * (1 - distance / max_distance))

            # Convert alpha to color
            r, g, b = self.theme_manager._hex_to_rgb(self.palette.primary)
            color = f"#{r:02x}{g:02x}{b:02x}"

            self.bg_canvas.create_oval(
                particle["x"] - particle["size"],
                particle["y"] - particle["size"],
                particle["x"] + particle["size"],
                particle["y"] + particle["size"],
                fill=color,
                outline="",
                tags="particles",
            )

    def stop_animations(self):
        """Stop all animations"""
        self.animation_running = False

    def update_theme(self, theme_name: str):
        """Update dashboard theme"""
        self.theme_manager.apply_theme(theme_name, self.parent.winfo_toplevel())
        self.palette = self.theme_manager.get_current_palette()

        # Redraw all elements with new theme
        self._draw_gradient_background()
        # Additional theme update logic would go here

    def show_welcome_animation(self):
        """Show welcome animation sequence"""
        # This would implement a fancy welcome sequence
        # with logo animation, text reveals, etc.
        pass

    def add_notification(self, message: str, type: str = "info"):
        """Add animated notification"""
        # This would create a modern notification popup
        # with slide-in animation
        pass
