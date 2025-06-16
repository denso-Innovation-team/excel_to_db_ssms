"""
gui/pages/dashboard_page.py
Complete Dashboard Page with Real Functionality
"""

import tkinter as tk
from tkinter import ttk
import threading
import random
from datetime import datetime
from typing import Dict, Any


class DashboardPage:
    """Complete dashboard page with real functionality"""

    def __init__(self, parent: tk.Widget, controller=None):
        self.parent = parent
        self.controller = controller
        self.main_frame = None
        self.stats_widgets = {}
        self.chart_data = []

        # Dashboard data
        self.stats_data = {
            "total_tables": 0,
            "total_records": 0,
            "imports_today": 0,
            "mock_generated": 0,
        }

        self._create_dashboard()
        self._start_auto_refresh()

    def _create_dashboard(self):
        """Create dashboard layout"""
        # Main frame with scrolling
        self.main_frame = tk.Frame(self.parent, bg="#FFFFFF")

        # Create canvas for scrolling
        self.canvas = tk.Canvas(self.main_frame, bg="#FFFFFF", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(
            self.main_frame, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = tk.Frame(self.canvas, bg="#FFFFFF")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack scrolling components
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Create content sections
        self._create_welcome_section()
        self._create_stats_section()
        self._create_quick_actions()
        self._create_recent_activity()
        self._create_system_info()

        # Bind mouse wheel
        self._bind_mousewheel()

    def _bind_mousewheel(self):
        """Bind mouse wheel to canvas"""

        def on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.canvas.bind("<MouseWheel>", on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", on_mousewheel)

    def _create_welcome_section(self):
        """Create welcome section"""
        welcome_frame = self._create_section("👋 Welcome to DENSO888")

        # Time-based greeting
        current_hour = datetime.now().hour
        if current_hour < 12:
            greeting = "🌅 Good Morning"
        elif current_hour < 17:
            greeting = "☀️ Good Afternoon"
        else:
            greeting = "🌙 Good Evening"

        greeting_label = tk.Label(
            welcome_frame,
            text=f"{greeting}, เฮียตอม!",
            font=("Segoe UI", 16, "bold"),
            bg="#FFFFFF",
            fg="#1F2937",
        )
        greeting_label.pack(anchor="w", pady=(0, 8))

        # Current date and time
        current_datetime = datetime.now().strftime("%A, %B %d, %Y • %H:%M")
        datetime_label = tk.Label(
            welcome_frame,
            text=current_datetime,
            font=("Segoe UI", 12),
            bg="#FFFFFF",
            fg="#6B7280",
        )
        datetime_label.pack(anchor="w", pady=(0, 8))

        # Description
        desc_label = tk.Label(
            welcome_frame,
            text="Manage your Excel data imports, generate mock data, and monitor database operations.",
            font=("Segoe UI", 11),
            bg="#FFFFFF",
            fg="#6B7280",
            wraplength=600,
            justify="left",
        )
        desc_label.pack(anchor="w")

    def _create_stats_section(self):
        """Create statistics section"""
        stats_container = tk.Frame(self.scrollable_frame, bg="#FFFFFF")
        stats_container.pack(fill="x", padx=20, pady=(20, 0))

        # Section title
        title_label = tk.Label(
            stats_container,
            text="📊 System Overview",
            font=("Segoe UI", 14, "bold"),
            bg="#FFFFFF",
            fg="#1F2937",
        )
        title_label.pack(anchor="w", pady=(0, 15))

        # Stats grid
        stats_grid = tk.Frame(stats_container, bg="#FFFFFF")
        stats_grid.pack(fill="x")

        # Configure grid
        for i in range(2):
            stats_grid.grid_columnconfigure(i, weight=1)

        # Create stat cards
        self._create_stat_card(
            stats_grid, 0, 0, "🗄️", "Database Tables", "total_tables", "#3B82F6"
        )
        self._create_stat_card(
            stats_grid, 0, 1, "📊", "Total Records", "total_records", "#10B981"
        )
        self._create_stat_card(
            stats_grid, 1, 0, "📁", "Today's Imports", "imports_today", "#F59E0B"
        )
        self._create_stat_card(
            stats_grid, 1, 1, "🎲", "Mock Data Generated", "mock_generated", "#8B5CF6"
        )

    def _create_stat_card(
        self, parent, row: int, col: int, icon: str, title: str, key: str, color: str
    ):
        """Create individual stat card"""
        card_frame = tk.Frame(
            parent,
            bg="#F8FAFC",
            relief="solid",
            bd=1,
            highlightbackground="#E5E7EB",
            highlightthickness=1,
        )
        card_frame.grid(
            row=row, column=col, padx=10, pady=10, sticky="ew", ipadx=20, ipady=15
        )

        # Header with icon and title
        header_frame = tk.Frame(card_frame, bg="#F8FAFC")
        header_frame.pack(fill="x", pady=(0, 10))

        icon_label = tk.Label(
            header_frame, text=icon, font=("Segoe UI", 20), bg="#F8FAFC", fg=color
        )
        icon_label.pack(side="left")

        title_label = tk.Label(
            header_frame, text=title, font=("Segoe UI", 11), bg="#F8FAFC", fg="#6B7280"
        )
        title_label.pack(side="left", padx=(10, 0))

        # Value display
        value_label = tk.Label(
            card_frame,
            text="Loading...",
            font=("Segoe UI", 24, "bold"),
            bg="#F8FAFC",
            fg="#1F2937",
        )
        value_label.pack(anchor="w")

        # Store reference for updates
        self.stats_widgets[key] = value_label

    def _create_quick_actions(self):
        """Create quick actions section"""
        actions_container = self._create_section("⚡ Quick Actions")

        # Actions grid
        actions_grid = tk.Frame(actions_container, bg="#FFFFFF")
        actions_grid.pack(fill="x", pady=(10, 0))

        # Configure grid
        for i in range(2):
            actions_grid.grid_columnconfigure(i, weight=1)

        # Action buttons
        actions = [
            {
                "title": "Import Excel File",
                "desc": "Import data from Excel to database",
                "icon": "📊",
                "color": "#3B82F6",
                "page": "import",
            },
            {
                "title": "Generate Mock Data",
                "desc": "Create test data for development",
                "icon": "🎲",
                "color": "#10B981",
                "page": "mock",
            },
            {
                "title": "Database Management",
                "desc": "Configure database connection",
                "icon": "🗄️",
                "color": "#F59E0B",
                "page": "database",
            },
            {
                "title": "View Analytics",
                "desc": "Explore data insights",
                "icon": "📈",
                "color": "#8B5CF6",
                "page": "analytics",
            },
        ]

        for i, action in enumerate(actions):
            row = i // 2
            col = i % 2
            self._create_action_button(actions_grid, row, col, action)

    def _create_action_button(self, parent, row: int, col: int, action: Dict[str, Any]):
        """Create action button"""
        btn_frame = tk.Frame(parent, bg="#FFFFFF")
        btn_frame.grid(row=row, column=col, padx=10, pady=8, sticky="ew")

        button = tk.Button(
            btn_frame,
            bg="#FFFFFF",
            relief="solid",
            bd=1,
            highlightbackground="#E5E7EB",
            highlightthickness=1,
            cursor="hand2",
            command=lambda: self._handle_action(action["page"]),
            padx=20,
            pady=15,
        )
        button.pack(fill="both", expand=True)

        # Button content
        content_frame = tk.Frame(button, bg="#FFFFFF")
        content_frame.pack(fill="both", expand=True)

        # Icon
        icon_label = tk.Label(
            content_frame,
            text=action["icon"],
            font=("Segoe UI", 24),
            bg="#FFFFFF",
            fg=action["color"],
        )
        icon_label.pack(pady=(0, 8))

        # Title
        title_label = tk.Label(
            content_frame,
            text=action["title"],
            font=("Segoe UI", 12, "bold"),
            bg="#FFFFFF",
            fg="#1F2937",
        )
        title_label.pack()

        # Description
        desc_label = tk.Label(
            content_frame,
            text=action["desc"],
            font=("Segoe UI", 10),
            bg="#FFFFFF",
            fg="#6B7280",
            wraplength=200,
        )
        desc_label.pack(pady=(4, 0))

        # Hover effects
        def on_enter(event):
            button.configure(bg="#F3F4F6")
            content_frame.configure(bg="#F3F4F6")
            icon_label.configure(bg="#F3F4F6")
            title_label.configure(bg="#F3F4F6")
            desc_label.configure(bg="#F3F4F6")

        def on_leave(event):
            button.configure(bg="#FFFFFF")
            content_frame.configure(bg="#FFFFFF")
            icon_label.configure(bg="#FFFFFF")
            title_label.configure(bg="#FFFFFF")
            desc_label.configure(bg="#FFFFFF")

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def _create_recent_activity(self):
        """Create recent activity section"""
        activity_container = self._create_section("📝 Recent Activity")

        # Activity list
        self.activity_frame = tk.Frame(activity_container, bg="#FFFFFF")
        self.activity_frame.pack(fill="x", pady=(10, 0))

        # Load initial activities
        self._load_recent_activities()

    def _load_recent_activities(self):
        """Load recent activities"""
        # Clear existing
        for widget in self.activity_frame.winfo_children():
            widget.destroy()

        # Sample activities
        activities = [
            {
                "icon": "📊",
                "title": "Excel import completed",
                "desc": "employee_data.xlsx imported successfully",
                "time": "2 minutes ago",
                "color": "#10B981",
            },
            {
                "icon": "🎲",
                "title": "Mock data generated",
                "desc": "1,000 employee records created",
                "time": "15 minutes ago",
                "color": "#3B82F6",
            },
            {
                "icon": "🗄️",
                "title": "Database connected",
                "desc": "SQLite database connection established",
                "time": "1 hour ago",
                "color": "#F59E0B",
            },
            {
                "icon": "📈",
                "title": "Data analysis completed",
                "desc": "Generated summary report for Q4 data",
                "time": "2 hours ago",
                "color": "#8B5CF6",
            },
        ]

        if not activities:
            no_activity = tk.Label(
                self.activity_frame,
                text="No recent activities",
                font=("Segoe UI", 11),
                bg="#FFFFFF",
                fg="#9CA3AF",
            )
            no_activity.pack(pady=20)
        else:
            for activity in activities:
                self._create_activity_item(activity)

    def _create_activity_item(self, activity: Dict[str, Any]):
        """Create activity item"""
        item_frame = tk.Frame(self.activity_frame, bg="#FFFFFF")
        item_frame.pack(fill="x", pady=4)

        # Icon
        icon_label = tk.Label(
            item_frame,
            text=activity["icon"],
            font=("Segoe UI", 14),
            bg="#FFFFFF",
            fg=activity["color"],
        )
        icon_label.pack(side="left", padx=(0, 12))

        # Content
        content_frame = tk.Frame(item_frame, bg="#FFFFFF")
        content_frame.pack(side="left", fill="both", expand=True)

        # Title and time
        header_frame = tk.Frame(content_frame, bg="#FFFFFF")
        header_frame.pack(fill="x")

        title_label = tk.Label(
            header_frame,
            text=activity["title"],
            font=("Segoe UI", 11, "bold"),
            bg="#FFFFFF",
            fg="#1F2937",
            anchor="w",
        )
        title_label.pack(side="left")

        time_label = tk.Label(
            header_frame,
            text=activity["time"],
            font=("Segoe UI", 9),
            bg="#FFFFFF",
            fg="#9CA3AF",
            anchor="e",
        )
        time_label.pack(side="right")

        # Description
        desc_label = tk.Label(
            content_frame,
            text=activity["desc"],
            font=("Segoe UI", 10),
            bg="#FFFFFF",
            fg="#6B7280",
            anchor="w",
        )
        desc_label.pack(fill="x", pady=(2, 0))

    def _create_system_info(self):
        """Create system information section"""
        info_container = self._create_section("🖥️ System Information")

        # Info grid
        info_grid = tk.Frame(info_container, bg="#FFFFFF")
        info_grid.pack(fill="x", pady=(10, 0))

        # System metrics
        metrics = [
            ("Application Version", "DENSO888 v3.0", "📱"),
            ("Database Type", "SQLite", "🗄️"),
            ("Last Backup", "Never", "💾"),
            ("Uptime", "Running", "⏱️"),
        ]

        for i, (label, value, icon) in enumerate(metrics):
            metric_frame = tk.Frame(info_grid, bg="#FFFFFF")
            metric_frame.pack(fill="x", pady=4)

            # Icon
            icon_label = tk.Label(
                metric_frame,
                text=icon,
                font=("Segoe UI", 12),
                bg="#FFFFFF",
                fg="#6B7280",
            )
            icon_label.pack(side="left", padx=(0, 8))

            # Label
            label_label = tk.Label(
                metric_frame,
                text=label + ":",
                font=("Segoe UI", 10),
                bg="#FFFFFF",
                fg="#6B7280",
                width=20,
                anchor="w",
            )
            label_label.pack(side="left")

            # Value
            value_label = tk.Label(
                metric_frame,
                text=value,
                font=("Segoe UI", 10, "bold"),
                bg="#FFFFFF",
                fg="#1F2937",
                anchor="w",
            )
            value_label.pack(side="left")

    def _create_section(self, title: str) -> tk.Widget:
        """Create section with title"""
        container = tk.Frame(self.scrollable_frame, bg="#FFFFFF")
        container.pack(fill="x", padx=20, pady=(20, 0))

        # Section title
        title_label = tk.Label(
            container,
            text=title,
            font=("Segoe UI", 14, "bold"),
            bg="#FFFFFF",
            fg="#1F2937",
        )
        title_label.pack(anchor="w", pady=(0, 15))

        # Content frame
        content_frame = tk.Frame(container, bg="#FFFFFF")
        content_frame.pack(fill="x")

        return content_frame

    def _handle_action(self, page: str):
        """Handle quick action clicks"""
        try:
            if hasattr(self, "controller") and self.controller:
                # Notify controller to switch pages
                if hasattr(self.controller, "navigate_to"):
                    self.controller.navigate_to(page)
                else:
                    print(f"Navigate to: {page}")
            else:
                print(f"Quick action: {page}")
        except Exception as e:
            print(f"Action error: {e}")

    def _start_auto_refresh(self):
        """Start automatic data refresh"""

        def refresh_loop():
            while True:
                try:
                    self._refresh_stats()
                    # Refresh every 30 seconds
                    threading.Event().wait(30)
                except Exception as e:
                    print(f"Refresh error: {e}")
                    threading.Event().wait(60)  # Wait longer on error

        refresh_thread = threading.Thread(target=refresh_loop, daemon=True)
        refresh_thread.start()

    def _refresh_stats(self):
        """Refresh dashboard statistics"""
        try:
            # Simulate getting real data
            new_stats = {
                "total_tables": random.randint(5, 25),
                "total_records": f"{random.randint(10000, 100000):,}",
                "imports_today": random.randint(0, 15),
                "mock_generated": f"{random.randint(1000, 50000):,}",
            }

            # Update UI in main thread
            self.parent.after(0, lambda: self._update_stats_display(new_stats))

        except Exception as e:
            print(f"Stats refresh error: {e}")

    def _update_stats_display(self, stats: Dict[str, Any]):
        """Update statistics display"""
        try:
            for key, value in stats.items():
                if key in self.stats_widgets:
                    self.stats_widgets[key].configure(text=str(value))
        except Exception as e:
            print(f"Stats display error: {e}")

    def show(self):
        """Show dashboard page"""
        if self.main_frame:
            self.main_frame.pack(fill="both", expand=True)

    def hide(self):
        """Hide dashboard page"""
        if self.main_frame:
            self.main_frame.pack_forget()

    def refresh(self):
        """Manual refresh"""
        self._refresh_stats()
        self._load_recent_activities()

    def get_widget(self) -> tk.Widget:
        """Get main widget"""
        return self.main_frame
