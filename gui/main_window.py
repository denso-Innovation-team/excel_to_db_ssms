"""
gui/main_window.py
DENSO888 Main Window
"""

import tkinter as tk
from tkinter import ttk
from controllers.app_controller import AppController
from models.app_config import AppConfig
from models.user_preferences import UserPreferences
from gui.themes.denso_theme import DensoTheme
from gui.pages.database_page import DatabasePage
from gui.pages.logs_page import LogsPage


class DENSO888MainWindow:
    """Main application window"""

    def __init__(self):
        # Initialize models
        self.config = AppConfig.load_from_file()
        self.preferences = UserPreferences.load_from_file()

        # Initialize controller
        self.controller = AppController(self.config)

        # Initialize UI
        self.root = tk.Tk()
        self.theme = DensoTheme()

        # Pages
        self.pages = {}

        self._setup_window()
        self._create_ui()
        self._connect_controller_events()

    def _setup_window(self):
        """Setup main window"""
        self.root.title(f"🏭 {self.config.app_name} v{self.config.version}")
        self.root.geometry(f"{self.config.window_width}x{self.config.window_height}")
        self.root.configure(bg=self.theme.colors.background)

    def _create_ui(self):
        """Create main user interface"""
        # Header
        self._create_header()

        # Main content
        self._create_main_content()

    def _create_header(self):
        """Create application header"""
        header_frame = tk.Frame(self.root, bg=self.theme.colors.primary, height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        content_frame = tk.Frame(header_frame, bg=self.theme.colors.primary)
        content_frame.pack(fill="both", expand=True, padx=30, pady=15)

        # Logo
        logo_label = tk.Label(
            content_frame,
            text="🏭",
            font=("Segoe UI", 24),
            fg="white",
            bg=self.theme.colors.primary,
        )
        logo_label.pack(side="left")

        # Title
        title_frame = tk.Frame(content_frame, bg=self.theme.colors.primary)
        title_frame.pack(side="left", fill="both", expand=True, padx=(20, 0))

        app_title = tk.Label(
            title_frame,
            text=f"{self.config.app_name} - Excel to SQL Management System",
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg=self.theme.colors.primary,
        )
        app_title.pack(anchor="w")

        subtitle = tk.Label(
            title_frame,
            text=f"Created by: {self.config.author} | {self.config.department}",
            font=("Segoe UI", 10),
            fg="#FFB3B3",
            bg=self.theme.colors.primary,
        )
        subtitle.pack(anchor="w", pady=(5, 0))

    def _create_main_content(self):
        """Create main content area"""
        main_frame = tk.Frame(self.root, bg=self.theme.colors.background)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Create notebook
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True)

        # Create pages
        self._create_pages()

    def _create_pages(self):
        """Create all pages"""
        # Database page
        database_frame = tk.Frame(self.notebook)
        self.pages["database"] = DatabasePage(
            database_frame, self.controller, self.theme
        )
        self.notebook.add(database_frame, text="🗄️ Database")

        # Logs page
        logs_frame = tk.Frame(self.notebook)
        self.pages["logs"] = LogsPage(logs_frame, self.controller, self.theme)
        self.notebook.add(logs_frame, text="📝 Logs")

    def _connect_controller_events(self):
        """Connect controller events"""
        self.controller.subscribe("log_message", self._on_log_message)

    def _on_log_message(self, log_data):
        """Handle log messages"""
        if "logs" in self.pages:
            self.pages["logs"].add_log_message(
                log_data.get("message", ""), log_data.get("level", "INFO")
            )

    def run(self):
        """Start the application"""
        self.root.mainloop()
