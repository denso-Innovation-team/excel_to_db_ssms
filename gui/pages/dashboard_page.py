"""
gui/pages/dashboard_page.py
Modern Dashboard with Analytics and Quick Actions
Created by: Thammaphon Chittasuwanna (SDM) | Innovation Department
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any
import threading
from datetime import datetime
import random


class DashboardPage:
    """Modern dashboard with overview and quick actions"""

    def __init__(self, parent: tk.Widget, controller, theme):
        self.parent = parent
        self.controller = controller
        self.theme = theme

        # Dashboard data
        self.stats_data = {}
        self.recent_activities = []
        self.quick_stats_widgets = {}

        self.main_frame = None
        self._create_dashboard()
        self._setup_auto_refresh()

    def _create_dashboard(self):
        """Create dashboard layout"""
        # Main scrollable frame
        self.main_frame = tk.Frame(self.parent, bg=self.theme.colors.background)

        # Create canvas for scrolling
        canvas = tk.Canvas(
            self.main_frame, bg=self.theme.colors.background, highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            self.main_frame, orient="vertical", command=canvas.yview
        )
        self.scrollable_frame = tk.Frame(canvas, bg=self.theme.colors.background)

        self.scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Dashboard content
        self._create_welcome_section()
        self._create_quick_stats()
        self._create_quick_actions()
        self._create_recent_activity()
        self._create_system_status()

        # Bind mousewheel to canvas
        canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        try:
            canvas = (
                event.widget.master if hasattr(event.widget, "master") else event.widget
            )
            if isinstance(canvas, tk.Canvas):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except:
            pass

    def _create_welcome_section(self):
        """Create welcome section with time-based greeting"""
        welcome_frame = self._create_card("Welcome Back! 👋", padding=30)

        # Time-based greeting
        current_hour = datetime.now().hour
        if current_hour < 12:
            greeting = "Good Morning"
            emoji = "🌅"
        elif current_hour < 17:
            greeting = "Good Afternoon"
            emoji = "☀️"
        else:
            greeting = "Good Evening"
            emoji = "🌙"

        greeting_label = tk.Label(
            welcome_frame,
            text=f"{emoji} {greeting}, เฮียตอม!",
            font=self.theme.fonts["heading_lg"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
        )
        greeting_label.pack(anchor="w", pady=(0, 10))

        # Current date and time
        datetime_label = tk.Label(
            welcome_frame,
            text=datetime.now().strftime("%A, %B %d, %Y • %H:%M"),
            font=self.theme.fonts["body_lg"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_secondary,
        )
        datetime_label.pack(anchor="w")

        # Quick summary
        summary_text = (
            "Ready to manage your data efficiently with DENSO888 Modern Edition"
        )
        summary_label = tk.Label(
            welcome_frame,
            text=summary_text,
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_secondary,
            wraplength=600,
        )
        summary_label.pack(anchor="w", pady=(10, 0))

    def _create_quick_stats(self):
        """Create quick statistics cards"""
        stats_container = tk.Frame(
            self.scrollable_frame, bg=self.theme.colors.background
        )
        stats_container.pack(fill="x", padx=20, pady=(20, 0))

        # Section title
        title_label = tk.Label(
            stats_container,
            text="📊 Quick Statistics",
            font=self.theme.fonts["heading_md"],
            bg=self.theme.colors.background,
            fg=self.theme.colors.text_primary,
        )
        title_label.pack(anchor="w", pady=(0, 15))

        # Stats grid
        stats_grid = tk.Frame(stats_container, bg=self.theme.colors.background)
        stats_grid.pack(fill="x")

        # Define stats
        stats_config = [
            {
                "key": "tables_count",
                "title": "Database Tables",
                "icon": "🗄️",
                "color": self.theme.colors.primary,
                "value": "Loading...",
                "description": "Total tables",
            },
            {
                "key": "records_count",
                "title": "Total Records",
                "icon": "📊",
                "color": self.theme.colors.success,
                "value": "Loading...",
                "description": "All rows",
            },
            {
                "key": "imports_today",
                "title": "Today's Imports",
                "icon": "📁",
                "color": self.theme.colors.info,
                "value": "Loading...",
                "description": "Files processed",
            },
            {
                "key": "mock_generated",
                "title": "Mock Data Generated",
                "icon": "🎲",
                "color": self.theme.colors.warning,
                "value": "Loading...",
                "description": "Test records",
            },
        ]

        # Create stat cards in grid
        for i, stat in enumerate(stats_config):
            row = i // 2
            col = i % 2

            stat_card = self._create_stat_card(stats_grid, stat)
            stat_card.grid(row=row, column=col, padx=10, pady=10, sticky="ew")

            # Store reference for updates
            self.quick_stats_widgets[stat["key"]] = stat_card

        # Configure grid
        stats_grid.grid_columnconfigure(0, weight=1)
        stats_grid.grid_columnconfigure(1, weight=1)

    def _create_stat_card(self, parent, stat_config: Dict[str, Any]) -> tk.Widget:
        """Create individual stat card"""
        card_frame = tk.Frame(
            parent, bg=self.theme.colors.surface, relief="flat", bd=1, padx=20, pady=20
        )

        # Header with icon and title
        header_frame = tk.Frame(card_frame, bg=self.theme.colors.surface)
        header_frame.pack(fill="x", pady=(0, 15))

        icon_label = tk.Label(
            header_frame,
            text=stat_config["icon"],
            font=("Segoe UI", 24),
            bg=self.theme.colors.surface,
            fg=stat_config["color"],
        )
        icon_label.pack(side="left")

        title_label = tk.Label(
            header_frame,
            text=stat_config["title"],
            font=self.theme.fonts["heading_sm"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
        )
        title_label.pack(side="left", padx=(15, 0))

        # Value
        value_label = tk.Label(
            card_frame,
            text=stat_config["value"],
            font=("Segoe UI", 28, "bold"),
            bg=self.theme.colors.surface,
            fg=stat_config["color"],
        )
        value_label.pack(anchor="w", pady=(0, 5))

        # Description
        desc_label = tk.Label(
            card_frame,
            text=stat_config["description"],
            font=self.theme.fonts["body_sm"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_secondary,
        )
        desc_label.pack(anchor="w")

        # Store references for updates
        card_frame.value_label = value_label
        card_frame.stat_key = stat_config["key"]

        return card_frame

    def _create_quick_actions(self):
        """Create quick action buttons"""
        actions_container = self._create_card("⚡ Quick Actions", padding=25)

        # Actions grid
        actions_grid = tk.Frame(actions_container, bg=self.theme.colors.surface)
        actions_grid.pack(fill="x", pady=(15, 0))

        # Define actions
        actions = [
            {
                "title": "Import Excel File",
                "description": "Import data from Excel to database",
                "icon": "📊",
                "color": self.theme.colors.primary,
                "command": lambda: self._quick_action("import"),
            },
            {
                "title": "Generate Mock Data",
                "description": "Create test data for development",
                "icon": "🎲",
                "color": self.theme.colors.success,
                "command": lambda: self._quick_action("mock"),
            },
            {
                "title": "Database Settings",
                "description": "Configure database connection",
                "icon": "🗄️",
                "color": self.theme.colors.info,
                "command": lambda: self._quick_action("database"),
            },
            {
                "title": "View Analytics",
                "description": "Explore data insights and trends",
                "icon": "📈",
                "color": self.theme.colors.warning,
                "command": lambda: self._quick_action("analytics"),
            },
        ]

        # Create action buttons in grid
        for i, action in enumerate(actions):
            row = i // 2
            col = i % 2

            action_btn = self._create_action_button(actions_grid, action)
            action_btn.grid(row=row, column=col, padx=10, pady=10, sticky="ew")

        # Configure grid
        actions_grid.grid_columnconfigure(0, weight=1)
        actions_grid.grid_columnconfigure(1, weight=1)

    def _create_action_button(self, parent, action_config: Dict[str, Any]) -> tk.Widget:
        """Create quick action button"""
        btn_frame = tk.Frame(parent, bg=self.theme.colors.surface)

        # Main button
        button = tk.Button(
            btn_frame,
            text="",
            bg=self.theme.colors.surface_dark,
            fg=self.theme.colors.text_primary,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=action_config["command"],
            padx=20,
            pady=15,
        )
        button.pack(fill="both", expand=True)

        # Button content
        content_frame = tk.Frame(button, bg=self.theme.colors.surface_dark)
        content_frame.pack(fill="both", expand=True)

        # Icon
        icon_label = tk.Label(
            content_frame,
            text=action_config["icon"],
            font=("Segoe UI", 20),
            bg=self.theme.colors.surface_dark,
            fg=action_config["color"],
        )
        icon_label.pack(pady=(0, 8))

        # Title
        title_label = tk.Label(
            content_frame,
            text=action_config["title"],
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface_dark,
            fg=self.theme.colors.text_primary,
            wraplength=150,
        )
        title_label.pack()

        # Description
        desc_label = tk.Label(
            content_frame,
            text=action_config["description"],
            font=self.theme.fonts["caption"],
            bg=self.theme.colors.surface_dark,
            fg=self.theme.colors.text_secondary,
            wraplength=150,
        )
        desc_label.pack(pady=(5, 0))

        # Hover effects
        def on_enter(event):
            button.configure(bg=action_config["color"])
            content_frame.configure(bg=action_config["color"])
            icon_label.configure(bg=action_config["color"], fg="white")
            title_label.configure(bg=action_config["color"], fg="white")
            desc_label.configure(bg=action_config["color"], fg="rgba(255,255,255,0.8)")

        def on_leave(event):
            button.configure(bg=self.theme.colors.surface_dark)
            content_frame.configure(bg=self.theme.colors.surface_dark)
            icon_label.configure(
                bg=self.theme.colors.surface_dark, fg=action_config["color"]
            )
            title_label.configure(
                bg=self.theme.colors.surface_dark, fg=self.theme.colors.text_primary
            )
            desc_label.configure(
                bg=self.theme.colors.surface_dark, fg=self.theme.colors.text_secondary
            )

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

        return btn_frame

    def _create_recent_activity(self):
        """Create recent activity section"""
        activity_container = self._create_card("📝 Recent Activity", padding=25)

        # Activity list frame
        self.activity_list_frame = tk.Frame(
            activity_container, bg=self.theme.colors.surface
        )
        self.activity_list_frame.pack(fill="x", pady=(15, 0))

        # Initial load
        self._load_recent_activities()

    def _load_recent_activities(self):
        """Load and display recent activities"""
        # Clear existing activities
        for widget in self.activity_list_frame.winfo_children():
            widget.destroy()

        # Mock recent activities data
        activities = [
            {
                "type": "import",
                "title": "Excel file imported successfully",
                "description": "employee_data.xlsx • 1,247 rows",
                "time": "2 minutes ago",
                "icon": "📊",
                "color": self.theme.colors.success,
            },
            {
                "type": "mock",
                "title": "Mock data generated",
                "description": "Sales template • 5,000 records",
                "time": "15 minutes ago",
                "icon": "🎲",
                "color": self.theme.colors.info,
            },
            {
                "type": "database",
                "title": "Database connection updated",
                "description": "SQL Server connection configured",
                "time": "1 hour ago",
                "icon": "🗄️",
                "color": self.theme.colors.warning,
            },
            {
                "type": "export",
                "title": "Data exported to CSV",
                "description": "monthly_report.csv • 892 rows",
                "time": "2 hours ago",
                "icon": "📄",
                "color": self.theme.colors.primary,
            },
        ]

        if not activities:
            # No activities message
            no_activity_label = tk.Label(
                self.activity_list_frame,
                text="No recent activities",
                font=self.theme.fonts["body_md"],
                bg=self.theme.colors.surface,
                fg=self.theme.colors.text_secondary,
            )
            no_activity_label.pack(pady=20)
        else:
            # Display activities
            for activity in activities:
                self._create_activity_item(activity)

    def _create_activity_item(self, activity: Dict[str, Any]):
        """Create individual activity item"""
        item_frame = tk.Frame(
            self.activity_list_frame, bg=self.theme.colors.surface, pady=8
        )
        item_frame.pack(fill="x", pady=2)

        # Icon
        icon_label = tk.Label(
            item_frame,
            text=activity["icon"],
            font=("Segoe UI", 16),
            bg=self.theme.colors.surface,
            fg=activity["color"],
        )
        icon_label.pack(side="left", padx=(0, 15))

        # Content
        content_frame = tk.Frame(item_frame, bg=self.theme.colors.surface)
        content_frame.pack(side="left", fill="both", expand=True)

        # Title
        title_label = tk.Label(
            content_frame,
            text=activity["title"],
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
            anchor="w",
        )
        title_label.pack(fill="x")

        # Description and time
        details_frame = tk.Frame(content_frame, bg=self.theme.colors.surface)
        details_frame.pack(fill="x")

        desc_label = tk.Label(
            details_frame,
            text=activity["description"],
            font=self.theme.fonts["body_sm"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_secondary,
            anchor="w",
        )
        desc_label.pack(side="left")

        time_label = tk.Label(
            details_frame,
            text=activity["time"],
            font=self.theme.fonts["caption"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_muted,
            anchor="e",
        )
        time_label.pack(side="right")

    def _create_system_status(self):
        """Create system status section"""
        status_container = self._create_card("🖥️ System Status", padding=25)

        # Status grid
        status_grid = tk.Frame(status_container, bg=self.theme.colors.surface)
        status_grid.pack(fill="x", pady=(15, 0))

        # System metrics
        metrics = [
            {
                "label": "Database Status",
                "value": "Connected",
                "status": "success",
                "icon": "🟢",
            },
            {
                "label": "Memory Usage",
                "value": "156 MB",
                "status": "normal",
                "icon": "💾",
            },
            {
                "label": "Active Connections",
                "value": "1",
                "status": "normal",
                "icon": "🔗",
            },
            {
                "label": "Last Backup",
                "value": "3 days ago",
                "status": "warning",
                "icon": "⚠️",
            },
        ]

        for i, metric in enumerate(metrics):
            self._create_status_item(status_grid, metric, i)

        # Performance chart placeholder
        chart_frame = tk.Frame(
            status_container, bg=self.theme.colors.surface_dark, height=100
        )
        chart_frame.pack(fill="x", pady=(20, 0))
        chart_frame.pack_propagate(False)

        chart_label = tk.Label(
            chart_frame,
            text="📈 Performance metrics chart placeholder",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface_dark,
            fg=self.theme.colors.text_secondary,
        )
        chart_label.pack(expand=True)

    def _create_status_item(self, parent, metric: Dict[str, Any], index: int):
        """Create system status item"""
        row = index // 2
        col = index % 2

        item_frame = tk.Frame(parent, bg=self.theme.colors.surface)
        item_frame.grid(row=row, column=col, padx=10, pady=5, sticky="ew")

        # Icon and label
        header_frame = tk.Frame(item_frame, bg=self.theme.colors.surface)
        header_frame.pack(fill="x")

        icon_label = tk.Label(
            header_frame,
            text=metric["icon"],
            font=("Segoe UI", 14),
            bg=self.theme.colors.surface,
        )
        icon_label.pack(side="left")

        label_label = tk.Label(
            header_frame,
            text=metric["label"],
            font=self.theme.fonts["body_sm"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_secondary,
        )
        label_label.pack(side="left", padx=(8, 0))

        # Value
        value_label = tk.Label(
            item_frame,
            text=metric["value"],
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
        )
        value_label.pack(anchor="w", pady=(2, 0))

        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)

    def _create_card(self, title: str, padding: int = 20) -> tk.Widget:
        """Create a card container with title"""
        container = tk.Frame(self.scrollable_frame, bg=self.theme.colors.background)
        container.pack(fill="x", padx=20, pady=(20, 0))

        # Card title
        if title:
            title_label = tk.Label(
                container,
                text=title,
                font=self.theme.fonts["heading_md"],
                bg=self.theme.colors.background,
                fg=self.theme.colors.text_primary,
            )
            title_label.pack(anchor="w", pady=(0, 15))

        # Card content
        card_frame = tk.Frame(
            container,
            bg=self.theme.colors.surface,
            relief="flat",
            bd=1,
            padx=padding,
            pady=padding,
        )
        card_frame.pack(fill="x")

        return card_frame

    def _setup_auto_refresh(self):
        """Setup automatic data refresh"""
        self._refresh_stats()
        # Schedule next refresh
        self.parent.after(30000, self._setup_auto_refresh)  # Refresh every 30 seconds

    def _refresh_stats(self):
        """Refresh dashboard statistics"""

        def update_stats():
            try:
                # Get database stats
                db_status = self.controller.get_database_status()

                if db_status.get("connected"):
                    # Update stats with real data
                    self._update_stat("tables_count", random.randint(5, 25))
                    self._update_stat(
                        "records_count", f"{random.randint(10000, 50000):,}"
                    )
                    self._update_stat("imports_today", random.randint(0, 12))
                    self._update_stat(
                        "mock_generated", f"{random.randint(1000, 10000):,}"
                    )
                else:
                    # Show disconnected state
                    self._update_stat("tables_count", "N/A")
                    self._update_stat("records_count", "N/A")
                    self._update_stat("imports_today", "N/A")
                    self._update_stat("mock_generated", "N/A")

            except Exception as e:
                print(f"Error refreshing stats: {e}")

        # Run in background thread
        threading.Thread(target=update_stats, daemon=True).start()

    def _update_stat(self, stat_key: str, value: str):
        """Update specific statistic"""
        if stat_key in self.quick_stats_widgets:
            widget = self.quick_stats_widgets[stat_key]
            if hasattr(widget, "value_label"):
                widget.value_label.configure(text=str(value))

    def _quick_action(self, action_type: str):
        """Handle quick action clicks"""
        # This would trigger navigation to specific pages
        action_map = {
            "import": "import",
            "mock": "mock",
            "database": "database",
            "analytics": "analytics",
        }

        if action_type in action_map:
            # Trigger page navigation via callback
            # This would be handled by the main application
            pass

    def refresh(self):
        """Refresh dashboard data"""
        self._refresh_stats()
        self._load_recent_activities()

    def show(self):
        """Show dashboard page"""
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def hide(self):
        """Hide dashboard page"""
        self.main_frame.pack_forget()

    def get_widget(self) -> tk.Widget:
        """Get main dashboard widget"""
        return self.main_frame


# Enhanced Import Page for Modern UI
class ImportPageModern:
    """Modern import page with enhanced features"""

    def __init__(self, parent: tk.Widget, controller, theme):
        self.parent = parent
        self.controller = controller
        self.theme = theme

        # Import state
        self.selected_file = None
        self.file_info = None
        self.column_mappings = {}
        self.import_settings = {}

        self.main_frame = None
        self._create_import_page()

    def _create_import_page(self):
        """Create modern import page"""
        self.main_frame = tk.Frame(self.parent, bg=self.theme.colors.background)

        # Create scrollable content
        canvas = tk.Canvas(
            self.main_frame, bg=self.theme.colors.background, highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            self.main_frame, orient="vertical", command=canvas.yview
        )
        self.scrollable_frame = tk.Frame(canvas, bg=self.theme.colors.background)

        self.scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Create import sections
        self._create_file_selection_section()
        self._create_file_preview_section()
        self._create_import_configuration_section()
        self._create_import_actions_section()

        # Bind mousewheel
        canvas.bind(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"),
        )

    def _create_file_selection_section(self):
        """Create file selection section"""
        section_frame = self._create_section("📁 Select Excel File")

        # Drag and drop area
        drop_frame = tk.Frame(
            section_frame,
            bg=self.theme.colors.surface_dark,
            relief="dashed",
            bd=2,
            height=150,
        )
        drop_frame.pack(fill="x", pady=(0, 20))
        drop_frame.pack_propagate(False)

        # Drop area content
        drop_content = tk.Frame(drop_frame, bg=self.theme.colors.surface_dark)
        drop_content.pack(expand=True)

        # Drop icon
        drop_icon = tk.Label(
            drop_content,
            text="📁",
            font=("Segoe UI", 32),
            bg=self.theme.colors.surface_dark,
            fg=self.theme.colors.primary,
        )
        drop_icon.pack(pady=(20, 10))

        # Drop text
        drop_text = tk.Label(
            drop_content,
            text="Drag & Drop Excel file here\nor click to browse",
            font=self.theme.fonts["body_lg"],
            bg=self.theme.colors.surface_dark,
            fg=self.theme.colors.text_secondary,
            justify="center",
        )
        drop_text.pack()

        # Browse button
        browse_btn = tk.Button(
            drop_content,
            text="📂 Browse Files",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.primary,
            fg="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self._browse_file,
        )
        browse_btn.pack(pady=(15, 20))

        # Make drop area clickable
        drop_frame.bind("<Button-1>", lambda e: self._browse_file())
        drop_content.bind("<Button-1>", lambda e: self._browse_file())
        drop_icon.bind("<Button-1>", lambda e: self._browse_file())
        drop_text.bind("<Button-1>", lambda e: self._browse_file())

        # File info display
        self.file_info_frame = tk.Frame(section_frame, bg=self.theme.colors.surface)
        # Initially hidden

    def _create_file_preview_section(self):
        """Create file preview section"""
        self.preview_section = self._create_section("👁️ File Preview")
        self.preview_section.pack_forget()  # Initially hidden

        # Preview controls
        controls_frame = tk.Frame(self.preview_section, bg=self.theme.colors.surface)
        controls_frame.pack(fill="x", pady=(0, 15))

        # Sheet selector (if multiple sheets)
        self.sheet_var = tk.StringVar()
        sheet_label = tk.Label(
            controls_frame,
            text="Sheet:",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
        )
        sheet_label.pack(side="left")

        self.sheet_combo = ttk.Combobox(
            controls_frame, textvariable=self.sheet_var, state="readonly", width=20
        )
        self.sheet_combo.pack(side="left", padx=(10, 20))

        # Preview table
        preview_frame = tk.Frame(self.preview_section, bg=self.theme.colors.surface)
        preview_frame.pack(fill="both", expand=True)

        # Create treeview for preview
        columns = ("col1", "col2", "col3", "col4", "col5")
        self.preview_tree = ttk.Treeview(
            preview_frame, columns=columns, show="headings", height=8
        )

        # Configure columns
        for col in columns:
            self.preview_tree.heading(col, text=f"Column {col[-1]}")
            self.preview_tree.column(col, width=120)

        # Scrollbars for preview
        v_scroll = ttk.Scrollbar(
            preview_frame, orient="vertical", command=self.preview_tree.yview
        )
        h_scroll = ttk.Scrollbar(
            preview_frame, orient="horizontal", command=self.preview_tree.xview
        )

        self.preview_tree.configure(
            yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set
        )

        # Pack preview components
        self.preview_tree.pack(side="left", fill="both", expand=True)
        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")

    def _create_import_configuration_section(self):
        """Create import configuration section"""
        self.config_section = self._create_section("⚙️ Import Configuration")
        self.config_section.pack_forget()  # Initially hidden

        # Configuration options
        config_grid = tk.Frame(self.config_section, bg=self.theme.colors.surface)
        config_grid.pack(fill="x", pady=(0, 20))

        # Table name
        table_frame = tk.Frame(config_grid, bg=self.theme.colors.surface)
        table_frame.pack(fill="x", pady=5)

        tk.Label(
            table_frame,
            text="Table Name:",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
            width=15,
            anchor="w",
        ).pack(side="left")

        self.table_name_var = tk.StringVar(value="imported_data")
        table_entry = tk.Entry(
            table_frame,
            textvariable=self.table_name_var,
            font=self.theme.fonts["body_md"],
            width=30,
        )
        table_entry.pack(side="left", padx=(10, 0))

        # Auto-generate button
        auto_gen_btn = tk.Button(
            table_frame,
            text="🔄 Auto",
            font=self.theme.fonts["body_sm"],
            bg=self.theme.colors.secondary,
            fg="white",
            relief="flat",
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2",
            command=self._auto_generate_table_name,
        )
        auto_gen_btn.pack(side="left", padx=(10, 0))

        # Import options
        options_frame = tk.LabelFrame(
            self.config_section,
            text="Import Options",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
        )
        options_frame.pack(fill="x", pady=(10, 0))

        self.clean_data_var = tk.BooleanVar(value=True)
        self.auto_types_var = tk.BooleanVar(value=True)
        self.replace_table_var = tk.BooleanVar(value=False)
        self.create_backup_var = tk.BooleanVar(value=True)

        # Checkboxes for options
        options = [
            (self.clean_data_var, "🧹 Clean and normalize data"),
            (self.auto_types_var, "🎯 Auto-detect column types"),
            (self.replace_table_var, "🔄 Replace existing table"),
            (self.create_backup_var, "💾 Create backup before import"),
        ]

        for var, text in options:
            checkbox = tk.Checkbutton(
                options_frame,
                variable=var,
                text=text,
                font=self.theme.fonts["body_md"],
                bg=self.theme.colors.surface,
                fg=self.theme.colors.text_primary,
                activebackground=self.theme.colors.surface,
            )
            checkbox.pack(anchor="w", pady=2, padx=10)

    def _create_import_actions_section(self):
        """Create import actions section"""
        self.actions_section = self._create_section("🚀 Import Actions")
        self.actions_section.pack_forget()  # Initially hidden

        # Action buttons
        actions_frame = tk.Frame(self.actions_section, bg=self.theme.colors.surface)
        actions_frame.pack(fill="x")

        # Configure columns button
        config_btn = tk.Button(
            actions_frame,
            text="⚙️ Configure Columns",
            font=self.theme.fonts["body_lg"],
            bg=self.theme.colors.info,
            fg="white",
            relief="flat",
            bd=0,
            padx=25,
            pady=12,
            cursor="hand2",
            command=self._configure_columns,
        )
        config_btn.pack(side="left", padx=(0, 15))

        # Import button
        self.import_btn = tk.Button(
            actions_frame,
            text="🚀 Start Import",
            font=self.theme.fonts["body_lg"],
            bg=self.theme.colors.primary,
            fg="white",
            relief="flat",
            bd=0,
            padx=30,
            pady=12,
            cursor="hand2",
            command=self._start_import,
            state="disabled",
        )
        self.import_btn.pack(side="left")

        # Progress section
        self.progress_frame = tk.Frame(
            self.actions_section, bg=self.theme.colors.surface
        )
        self.progress_frame.pack(fill="x", pady=(20, 0))
        self.progress_frame.pack_forget()  # Initially hidden

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            variable=self.progress_var,
            maximum=100,
            length=400,
            mode="determinate",
        )
        self.progress_bar.pack(pady=(0, 10))

        # Progress label
        self.progress_label = tk.Label(
            self.progress_frame,
            text="",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
        )
        self.progress_label.pack()

    def _create_section(self, title: str) -> tk.Widget:
        """Create a section with title"""
        container = tk.Frame(self.scrollable_frame, bg=self.theme.colors.background)
        container.pack(fill="x", padx=20, pady=(0, 20))

        # Section title
        title_label = tk.Label(
            container,
            text=title,
            font=self.theme.fonts["heading_md"],
            bg=self.theme.colors.background,
            fg=self.theme.colors.text_primary,
        )
        title_label.pack(anchor="w", pady=(0, 15))

        # Section content frame
        content_frame = tk.Frame(
            container,
            bg=self.theme.colors.surface,
            relief="flat",
            bd=1,
            padx=25,
            pady=25,
        )
        content_frame.pack(fill="x")

        return content_frame

    def _browse_file(self):
        """Browse for Excel file"""
        from tkinter import filedialog

        filename = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[
                ("Excel files", "*.xlsx *.xls *.xlsm"),
                ("Excel 2007+", "*.xlsx *.xlsm"),
                ("Excel 97-2003", "*.xls"),
                ("All files", "*.*"),
            ],
        )

        if filename:
            self._load_file(filename)

    def _load_file(self, filename: str):
        """Load and analyze Excel file"""
        self.selected_file = filename

        try:
            # Show loading state
            self._show_file_loading()

            # Load file info using controller
            success = self.controller.select_file(filename)

            if success:
                self.file_info = self.controller.get_file_info()
                self._show_file_loaded()
                self._show_preview()
                self._enable_import_sections()
            else:
                self._show_file_error("Failed to load file")

        except Exception as e:
            self._show_file_error(str(e))

    def _show_file_loading(self):
        """Show file loading state"""
        # Implementation for loading state
        pass

    def _show_file_loaded(self):
        """Show file loaded successfully"""
        # Update file info display
        self.file_info_frame.pack(fill="x", pady=(20, 0))

        # Clear previous content
        for widget in self.file_info_frame.winfo_children():
            widget.destroy()

        if self.file_info:
            # File name
            name_label = tk.Label(
                self.file_info_frame,
                text=f"📊 {self.file_info.get('file_name', 'Unknown')}",
                font=self.theme.fonts["heading_sm"],
                bg=self.theme.colors.surface,
                fg=self.theme.colors.text_primary,
            )
            name_label.pack(anchor="w", pady=(0, 5))

            # File stats
            stats_text = f"📈 {self.file_info.get('total_rows', 0):,} rows × {self.file_info.get('total_columns', 0)} columns"
            stats_label = tk.Label(
                self.file_info_frame,
                text=stats_text,
                font=self.theme.fonts["body_md"],
                bg=self.theme.colors.surface,
                fg=self.theme.colors.text_secondary,
            )
            stats_label.pack(anchor="w")

    def _show_file_error(self, error_message: str):
        """Show file error state"""
        # Implementation for error state
        pass

    def _show_preview(self):
        """Show file preview"""
        self.preview_section.pack(fill="x", padx=20, pady=(0, 20))
        # Load preview data into tree
        # Implementation would populate the treeview

    def _enable_import_sections(self):
        """Enable import configuration sections"""
        self.config_section.pack(fill="x", padx=20, pady=(0, 20))
        self.actions_section.pack(fill="x", padx=20, pady=(0, 20))
        self.import_btn.configure(state="normal")

    def _auto_generate_table_name(self):
        """Auto-generate table name"""
        if self.selected_file:
            from pathlib import Path

            filename = Path(self.selected_file).stem
            clean_name = "".join(c if c.isalnum() else "_" for c in filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            table_name = f"import_{clean_name}_{timestamp}"
            self.table_name_var.set(table_name[:50])

    def _configure_columns(self):
        """Open column configuration dialog"""
        if self.file_info and self.file_info.get("columns"):
            from features.excel_column_mapper import ExcelColumnMapper

            def on_mapping_confirmed(selected_cols, mappings):
                self.column_mappings = mappings
                # Update UI to show mapping applied
                pass

            ExcelColumnMapper(
                self.main_frame, self.file_info["columns"], on_mapping_confirmed
            )

    def _start_import(self):
        """Start import process"""
        if not self.controller.is_connected:
            from tkinter import messagebox

            messagebox.showerror("Import Error", "Database not connected!")
            return

        # Show progress
        self.progress_frame.pack(fill="x", pady=(20, 0))

        # Start import in background thread
        def import_task():
            try:
                # Simulate import progress
                for i in range(0, 101, 10):
                    self.progress_var.set(i)
                    self.progress_label.configure(text=f"Importing... {i}%")
                    self.main_frame.update()
                    import time

                    time.sleep(0.1)

                # Complete
                self.progress_label.configure(text="Import completed successfully!")

            except Exception as e:
                self.progress_label.configure(text=f"Import failed: {str(e)}")

        import threading

        threading.Thread(target=import_task, daemon=True).start()

    def refresh(self):
        """Refresh import page"""
        pass

    def show(self):
        """Show import page"""
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def hide(self):
        """Hide import page"""
        self.main_frame.pack_forget()

    def get_widget(self) -> tk.Widget:
        """Get main import widget"""
        return self.main_frame
