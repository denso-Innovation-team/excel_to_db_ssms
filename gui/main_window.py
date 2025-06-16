"""
gui/main_window.py
Main Window - Layout Manager Only
"""

import tkinter as tk
from typing import Dict, Any

from .themes.modern_theme import modern_theme
from .components.modern_sidebar import ModernSidebar
from .components.modern_notification import ModernNotification

# Import all pages
from .pages.dashboard_page import DashboardPage
from .pages.import_page import ImportPage
from .pages.database_page import DatabasePage
from .pages.mock_page import MockPage
from .pages.analytics_page import AnalyticsPage
from .pages.settings_page import SettingsPage

# Import controller
from ..controllers.app_controller import AppController


class MainWindow:
    """Main application window - handles layout and navigation only"""

    def __init__(self):
        self.root = tk.Tk()
        self.controller = AppController()
        self.current_page = None
        self.pages = {}

        self.setup_window()
        self.create_layout()
        self.initialize_pages()
        self.show_page("dashboard")

    def setup_window(self):
        """Configure main window"""
        self.root.title("🏭 DENSO888 Modern Edition")
        self.root.configure(bg=modern_theme.colors.white)

        # Window size and position
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = min(1400, int(screen_width * 0.85))
        window_height = min(900, int(screen_height * 0.85))

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(1200, 800)

        # Configure grid
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def create_layout(self):
        """Create main layout structure"""
        # Header
        self.create_header()

        # Sidebar
        self.create_sidebar()

        # Content area
        self.create_content_area()

        # Status bar
        self.create_status_bar()

    def create_header(self):
        """Create application header"""
        header = tk.Frame(
            self.root,
            bg=modern_theme.colors.white,
            height=70,
            relief="flat",
            bd=1,
            highlightbackground=modern_theme.colors.gray_200,
            highlightthickness=1,
        )
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        header.pack_propagate(False)

        # Header content
        content = tk.Frame(header, bg=modern_theme.colors.white)
        content.pack(fill="both", expand=True, padx=24, pady=16)

        # Brand
        brand_label = tk.Label(
            content,
            text="🏭 DENSO888 Modern",
            font=modern_theme.fonts.get("heading_lg"),
            bg=modern_theme.colors.white,
            fg=modern_theme.colors.primary,
        )
        brand_label.pack(side="left")

        # User info
        user_label = tk.Label(
            content,
            text="👨‍💻 เฮียตอม | Innovation Dept.",
            font=modern_theme.fonts.get("body_md"),
            bg=modern_theme.colors.white,
            fg=modern_theme.colors.gray_600,
        )
        user_label.pack(side="right")

    def create_sidebar(self):
        """Create navigation sidebar"""
        nav_items = [
            {
                "id": "dashboard",
                "title": "Dashboard",
                "description": "Overview & Analytics",
                "icon": "📊",
            },
            {
                "id": "import",
                "title": "Import Data",
                "description": "Excel to Database",
                "icon": "📁",
            },
            {
                "id": "database",
                "title": "Database",
                "description": "Connection Setup",
                "icon": "🗄️",
            },
            {
                "id": "mock",
                "title": "Mock Data",
                "description": "Generate Test Data",
                "icon": "🎲",
            },
            {
                "id": "analytics",
                "title": "Analytics",
                "description": "Data Insights",
                "icon": "📈",
            },
            {
                "id": "settings",
                "title": "Settings",
                "description": "Configuration",
                "icon": "⚙️",
            },
        ]

        self.sidebar = ModernSidebar(self.root, nav_items, self.navigate_to)
        sidebar_widget = self.sidebar.get_widget()
        sidebar_widget.grid(row=1, column=0, sticky="nsew")

    def create_content_area(self):
        """Create main content area"""
        self.content_frame = tk.Frame(self.root, bg=modern_theme.colors.gray_50)
        self.content_frame.grid(row=1, column=1, sticky="nsew", padx=24, pady=24)

    def create_status_bar(self):
        """Create status bar"""
        status_bar = tk.Frame(
            self.root,
            bg=modern_theme.colors.gray_50,
            height=40,
            relief="flat",
            bd=1,
            highlightbackground=modern_theme.colors.gray_200,
            highlightthickness=1,
        )
        status_bar.grid(row=2, column=0, columnspan=2, sticky="ew")
        status_bar.pack_propagate(False)

        # Status content
        content = tk.Frame(status_bar, bg=modern_theme.colors.gray_50)
        content.pack(fill="both", expand=True, padx=20, pady=8)

        # Left - Status
        self.status_label = tk.Label(
            content,
            text="🟢 Ready",
            font=modern_theme.fonts.get("body_sm"),
            bg=modern_theme.colors.gray_50,
            fg=modern_theme.colors.success,
        )
        self.status_label.pack(side="left")

        # Right - Info
        right_frame = tk.Frame(content, bg=modern_theme.colors.gray_50)
        right_frame.pack(side="right")

        # Database status
        self.db_status_label = tk.Label(
            right_frame,
            text="🔴 Database: Disconnected",
            font=modern_theme.fonts.get("body_sm"),
            bg=modern_theme.colors.gray_50,
            fg=modern_theme.colors.error,
        )
        self.db_status_label.pack(side="right", padx=(0, 16))

        # Time
        from datetime import datetime

        self.time_label = tk.Label(
            right_frame,
            text=datetime.now().strftime("%H:%M:%S"),
            font=modern_theme.fonts.get("body_sm"),
            bg=modern_theme.colors.gray_50,
            fg=modern_theme.colors.gray_500,
        )
        self.time_label.pack(side="right")
        self.update_time()

    def update_time(self):
        """Update time display"""
        from datetime import datetime

        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=current_time)
        self.root.after(1000, self.update_time)

    def initialize_pages(self):
        """Initialize all page instances"""
        self.pages = {
            "dashboard": DashboardPage(self.content_frame, self.controller),
            "import": ImportPage(self.content_frame, self.controller),
            "database": DatabasePage(self.content_frame, self.controller),
            "mock": MockPage(self.content_frame, self.controller),
            "analytics": AnalyticsPage(self.content_frame, self.controller),
            "settings": SettingsPage(self.content_frame, self.controller),
        }

        # Subscribe to controller events
        self.controller.subscribe("status_changed", self.update_status)
        self.controller.subscribe("db_status_changed", self.update_db_status)
        self.controller.subscribe("notification", self.show_notification)

    def navigate_to(self, page_id: str):
        """Navigate to specific page"""
        if page_id == self.current_page:
            return

        # Hide current page
        if self.current_page and self.current_page in self.pages:
            self.pages[self.current_page].hide()

        # Show new page
        if page_id in self.pages:
            self.pages[page_id].show()
            self.current_page = page_id

            # Update sidebar selection
            self.sidebar.select_item(page_id)

            # Show notification
            page_titles = {
                "dashboard": "📊 Dashboard",
                "import": "📁 Import Data",
                "database": "🗄️ Database",
                "mock": "🎲 Mock Data",
                "analytics": "📈 Analytics",
                "settings": "⚙️ Settings",
            }

            title = page_titles.get(page_id, "Page")
            ModernNotification.show(self.root, f"Switched to {title}", "info", 2000)

    def show_page(self, page_id: str):
        """Show specific page (initial load)"""
        self.navigate_to(page_id)
        self.sidebar.select_item(page_id)

    def update_status(self, status_data: Dict[str, Any]):
        """Update status bar"""
        status_text = status_data.get("text", "Ready")
        status_type = status_data.get("type", "info")

        colors = {
            "success": modern_theme.colors.success,
            "warning": modern_theme.colors.warning,
            "error": modern_theme.colors.error,
            "info": modern_theme.colors.gray_600,
        }

        color = colors.get(status_type, colors["info"])
        self.status_label.configure(text=status_text, fg=color)

    def update_db_status(self, connected: bool):
        """Update database status"""
        if connected:
            self.db_status_label.configure(
                text="🟢 Database: Connected", fg=modern_theme.colors.success
            )
        else:
            self.db_status_label.configure(
                text="🔴 Database: Disconnected", fg=modern_theme.colors.error
            )

    def show_notification(self, notification_data: Dict[str, Any]):
        """Show notification"""
        message = notification_data.get("message", "")
        type_ = notification_data.get("type", "info")
        duration = notification_data.get("duration", 3000)

        ModernNotification.show(self.root, message, type_, duration)

    def run(self):
        """Start the application"""
        try:
            print("🎨 Starting DENSO888 Modern Edition...")

            # Show welcome notification
            self.root.after(
                1000,
                lambda: ModernNotification.show(
                    self.root, "Welcome to DENSO888 Modern Edition!", "success"
                ),
            )

            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.root.mainloop()

        except Exception as e:
            print(f"❌ Application error: {e}")
            import traceback

            traceback.print_exc()

    def on_closing(self):
        """Handle application closing"""
        from tkinter import messagebox

        result = messagebox.askyesno(
            "Exit Application", "Are you sure you want to exit DENSO888?"
        )

        if result:
            print("👋 Thanks for using DENSO888 Modern Edition!")
            self.root.destroy()
