"""
gui/main_application.py
Main Application Entry Point for DENSO888 Modern Edition
Created by: Thammaphon Chittasuwanna (SDM) | Innovation Department
"""

import tkinter as tk
from tkinter import messagebox
import threading
import traceback
from typing import Dict, Any, Optional
from pathlib import Path

# Import core components
from models.app_config import AppConfig
from models.user_preferences import UserPreferences
from gui.themes.modern_theme import ModernTheme
from controllers.app_controller import AppController

# Import UI components
from gui.components.modern_sidebar import (
    ModernSidebar,
    ModernStatusBar,
    NotificationSystem,
)

# Import pages
from gui.pages.dashboard_page import DashboardPage
from gui.pages.database_page_modern import DatabasePageModern, MockPageModern
from gui.pages.admin_page import AdminPage


class DENSO888Application:
    """Main application class with modern architecture"""

    def __init__(self):
        """Initialize application"""
        try:
            # Load configuration
            self.config = AppConfig.load_from_file()
            self.preferences = UserPreferences.load_from_file()

            # Initialize theme
            self.theme = ModernTheme()

            # Initialize controller
            self.controller = AppController(self.config)

            # UI Components
            self.root: Optional[tk.Tk] = None
            self.sidebar: Optional[ModernSidebar] = None
            self.status_bar: Optional[ModernStatusBar] = None
            self.notification_system: Optional[NotificationSystem] = None

            # Pages
            self.pages: Dict[str, Any] = {}
            self.current_page: Optional[str] = None

            # Initialize UI
            self._create_main_window()
            self._setup_components()
            self._setup_event_handlers()

            print("✅ Application initialized successfully")

        except Exception as e:
            print(f"❌ Application initialization failed: {e}")
            print(f"🔍 Stack trace: {traceback.format_exc()}")
            raise

    def _create_main_window(self):
        """Create main application window"""
        self.root = tk.Tk()
        self.root.title(f"🏭 {self.config.app_name} v{self.config.version}")
        self.root.geometry(f"{self.config.window_width}x{self.config.window_height}")
        self.root.minsize(1000, 700)

        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.config.window_width // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.config.window_height // 2)
        self.root.geometry(
            f"{self.config.window_width}x{self.config.window_height}+{x}+{y}"
        )

        # Apply theme
        self.theme.apply_to_root(self.root)

        # Configure grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Set window icon (if available)
        try:
            icon_path = Path("assets/icons/denso888.ico")
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except:
            pass

    def _setup_components(self):
        """Setup main UI components"""
        # Create main layout frames
        self._create_layout()

        # Initialize sidebar
        self.sidebar = ModernSidebar(
            self.sidebar_frame, self.theme, self._on_page_changed
        )
        sidebar_widget = self.sidebar.get_widget()
        sidebar_widget.pack(fill="both", expand=True)

        # Initialize status bar
        self.status_bar = ModernStatusBar(self.status_frame, self.theme)
        status_widget = self.status_bar.get_widget()
        status_widget.pack(fill="x")

        # Initialize notification system
        self.notification_system = NotificationSystem(self.root, self.theme)

        # Initialize pages
        self._create_pages()

        # Show default page
        self._show_page("dashboard")

    def _create_layout(self):
        """Create main application layout"""
        # Sidebar frame
        self.sidebar_frame = tk.Frame(
            self.root, bg=self.theme.colors.surface, width=280, relief="flat", bd=1
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_propagate(False)

        # Main content area
        self.content_frame = tk.Frame(self.root, bg=self.theme.colors.background)
        self.content_frame.grid(row=0, column=1, sticky="nsew")

        # Status bar frame
        self.status_frame = tk.Frame(self.root, bg=self.theme.colors.surface, height=35)
        self.status_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.status_frame.grid_propagate(False)

    def _create_pages(self):
        """Initialize all application pages"""
        try:
            # Dashboard page
            self.pages["dashboard"] = DashboardPage(
                self.content_frame, self.controller, self.theme
            )

            # Import page (using modern version from database_page_modern.py)
            from gui.pages.database_page_modern import ImportPageModern

            self.pages["import"] = ImportPageModern(
                self.content_frame, self.controller, self.theme
            )

            # Database page
            self.pages["database"] = DatabasePageModern(
                self.content_frame, self.controller, self.theme
            )

            # Mock data page
            self.pages["mock"] = MockPageModern(
                self.content_frame, self.controller, self.theme
            )

            # Analytics page
            from gui.pages.database_page_modern import AnalyticsPage

            self.pages["analytics"] = AnalyticsPage(
                self.content_frame, self.controller, self.theme
            )

            # Settings page
            from gui.pages.database_page_modern import SettingsPage

            self.pages["settings"] = SettingsPage(
                self.content_frame, self.controller, self.theme, self.preferences
            )

            # Admin page
            self.pages["admin"] = AdminPage(
                self.content_frame, self.controller, self.theme
            )

            # Help page (simple)
            self.pages["help"] = self._create_help_page()

            print("✅ All pages initialized successfully")

        except Exception as e:
            print(f"❌ Error creating pages: {e}")
            print(f"🔍 Stack trace: {traceback.format_exc()}")
            # Create minimal fallback pages
            self._create_fallback_pages()

    def _create_help_page(self):
        """Create help page"""

        class HelpPage:
            def __init__(self, parent, controller, theme):
                self.parent = parent
                self.theme = theme
                self.main_frame = None
                self._create_help_content()

            def _create_help_content(self):
                self.main_frame = tk.Frame(self.parent, bg=self.theme.colors.background)

                content_frame = tk.Frame(
                    self.main_frame, bg=self.theme.colors.background
                )
                content_frame.pack(fill="both", expand=True, padx=40, pady=40)

                # Help content
                help_frame = tk.Frame(
                    content_frame,
                    bg=self.theme.colors.surface,
                    relief="flat",
                    bd=1,
                    padx=50,
                    pady=50,
                )
                help_frame.pack(expand=True)

                # Icon
                icon_label = tk.Label(
                    help_frame,
                    text="❓",
                    font=("Segoe UI", 48),
                    bg=self.theme.colors.surface,
                    fg=self.theme.colors.primary,
                )
                icon_label.pack(pady=(0, 20))

                # Title
                title_label = tk.Label(
                    help_frame,
                    text="Help & Documentation",
                    font=self.theme.fonts.heading_xl,
                    bg=self.theme.colors.surface,
                    fg=self.theme.colors.text_primary,
                )
                title_label.pack(pady=(0, 20))

                # Help content
                help_text = """
🏭 DENSO888 Modern Edition v2.0.0
Excel to SQL Management System

📋 Quick Start Guide:
1. Configure database connection in Database tab
2. Import Excel files or generate mock data
3. Monitor progress and view logs

💡 Features:
• Modern UI with responsive design
• SQLite and SQL Server support
• Excel column mapping
• Mock data generation
• Real-time progress monitoring
• Admin activity tracking

👨‍💻 Created by: Thammaphon Chittasuwanna (SDM)
🏢 Innovation Department | DENSO Corporation

เฮียตอมจัดหั้ย!!! 🚀
                """

                content_label = tk.Label(
                    help_frame,
                    text=help_text.strip(),
                    font=self.theme.fonts.body_md,
                    bg=self.theme.colors.surface,
                    fg=self.theme.colors.text_secondary,
                    justify="left",
                )
                content_label.pack()

            def show(self):
                self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

            def hide(self):
                self.main_frame.pack_forget()

            def refresh(self):
                pass

            def get_widget(self):
                return self.main_frame

        return HelpPage(self.content_frame, self.controller, self.theme)

    def _create_fallback_pages(self):
        """Create minimal fallback pages if main pages fail"""
        for page_id in [
            "dashboard",
            "import",
            "database",
            "mock",
            "analytics",
            "settings",
            "help",
        ]:
            if page_id not in self.pages:
                self.pages[page_id] = self._create_simple_page(page_id)

    def _create_simple_page(self, page_id: str):
        """Create simple fallback page"""

        class SimplePage:
            def __init__(self, parent, page_id, theme):
                self.parent = parent
                self.page_id = page_id
                self.theme = theme
                self.main_frame = tk.Frame(parent, bg=theme.colors.background)

                # Simple content
                label = tk.Label(
                    self.main_frame,
                    text=f"📄 {page_id.title()} Page\n\nThis page is under development.",
                    font=theme.fonts.heading_md,
                    bg=theme.colors.background,
                    fg=theme.colors.text_primary,
                    justify="center",
                )
                label.pack(expand=True)

            def show(self):
                self.main_frame.pack(fill="both", expand=True)

            def hide(self):
                self.main_frame.pack_forget()

            def refresh(self):
                pass

        return SimplePage(self.content_frame, page_id, self.theme)

    def _setup_event_handlers(self):
        """Setup application event handlers"""
        # Window events
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

        # Controller events
        self.controller.subscribe("db_status_changed", self._on_db_status_changed)
        self.controller.subscribe("operation_complete", self._on_operation_complete)
        self.controller.subscribe("error_occurred", self._on_error_occurred)
        self.controller.subscribe("log_message", self._on_log_message)

        # Keyboard shortcuts
        self.root.bind("<Control-q>", lambda e: self._on_closing())
        self.root.bind("<F5>", lambda e: self._refresh_current_page())

    def _on_page_changed(self, page_id: str):
        """Handle page navigation"""
        try:
            # Hide current page
            if self.current_page and self.current_page in self.pages:
                self.pages[self.current_page].hide()

            # Show new page
            if page_id in self.pages:
                self.pages[page_id].show()
                self.current_page = page_id

                # Refresh page data
                if hasattr(self.pages[page_id], "refresh"):
                    threading.Thread(
                        target=self.pages[page_id].refresh, daemon=True
                    ).start()

                # Update status
                self.status_bar.update_status(f"Viewing {page_id.title()} page")

            else:
                print(f"⚠️ Page '{page_id}' not found")

        except Exception as e:
            print(f"❌ Error changing page: {e}")
            self.notification_system.show_error(f"Failed to load {page_id} page")

    def _show_page(self, page_id: str):
        """Programmatically show a page"""
        if self.sidebar:
            self.sidebar.select_page(page_id)

    def _refresh_current_page(self):
        """Refresh current page"""
        if self.current_page and self.current_page in self.pages:
            page = self.pages[self.current_page]
            if hasattr(page, "refresh"):
                threading.Thread(target=page.refresh, daemon=True).start()

    def _on_db_status_changed(self, connected: bool):
        """Handle database status change"""
        if connected:
            self.status_bar.update_connection_status(True, "Database")
            self.notification_system.show_success("Database connected successfully!")
        else:
            self.status_bar.update_connection_status(False, "Database")

    def _on_operation_complete(self, data: Dict[str, Any]):
        """Handle operation completion"""
        operation = data.get("operation", "Operation")
        success = data.get("success", False)

        if success:
            self.notification_system.show_success(
                f"{operation} completed successfully!"
            )
        else:
            self.notification_system.show_error(f"{operation} failed!")

    def _on_error_occurred(self, error_message: str):
        """Handle application errors"""
        self.notification_system.show_error(error_message)
        self.status_bar.update_status(f"Error: {error_message}", "error")

    def _on_log_message(self, log_data: Dict[str, Any]):
        """Handle log messages"""
        message = log_data.get("message", "")
        level = log_data.get("level", "INFO")

        if level == "ERROR":
            self.status_bar.update_status(message, "error")
        elif level == "WARNING":
            self.status_bar.update_status(message, "warning")
        else:
            self.status_bar.update_status(message, "info")

    def _on_closing(self):
        """Handle application closing"""
        try:
            if messagebox.askokcancel("Quit", "Do you want to quit DENSO888?"):
                # Cleanup
                if self.controller:
                    self.controller.shutdown()

                if self.notification_system:
                    self.notification_system.close()

                # Save preferences
                # self.preferences.save_to_file()

                self.root.quit()
                self.root.destroy()

        except Exception as e:
            print(f"Error during shutdown: {e}")
            self.root.quit()

    def run(self):
        """Start the application"""
        try:
            print("🚀 Starting DENSO888 application...")

            # Show startup notification
            self.notification_system.show_info("DENSO888 started successfully!")

            # Start main loop
            self.root.mainloop()

        except KeyboardInterrupt:
            print("\n⚠️ Application interrupted by user")
        except Exception as e:
            print(f"❌ Application runtime error: {e}")
            print(f"🔍 Stack trace: {traceback.format_exc()}")
            messagebox.showerror("Runtime Error", f"Application error:\n\n{str(e)}")
        finally:
            print("✅ Application shutdown completed")


# Export for main.py
__all__ = ["DENSO888Application"]
