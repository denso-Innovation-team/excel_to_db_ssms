"""
gui/main_application.py
DENSO888 Main Application - Redesigned for 2025
Modern UI with enhanced features and robust architecture
Created by: Thammaphon Chittasuwanna (SDM) | Innovation Department
เฮียตอมจัดหั้ย!!! 🚀
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from typing import Dict, Any

from controllers.app_controller import AppController
from models.app_config import AppConfig
from models.user_preferences import UserPreferences
from gui.themes.modern_theme import ModernTheme
from gui.pages.dashboard_page import DashboardPage
from gui.pages.import_page_modern import ImportPageModern
from gui.pages.database_page_modern import DatabasePageModern
from gui.pages.mock_page_modern import MockPageModern
from gui.pages.analytics_page import AnalyticsPage
from gui.pages.settings_page import SettingsPage
from gui.components.modern_sidebar import ModernSidebar
from gui.components.status_bar_modern import ModernStatusBar
from gui.components.notification_system import NotificationSystem


class DENSO888Application:
    """Modern DENSO888 Application with enhanced UI"""

    def __init__(self):
        # Initialize core components
        self.config = AppConfig.load_from_file()
        self.preferences = UserPreferences.load_from_file()
        self.controller = AppController(self.config)

        # UI components
        self.root = None
        self.theme = ModernTheme()
        self.sidebar = None
        self.content_area = None
        self.status_bar = None
        self.notification_system = None

        # Page management
        self.pages = {}
        self.current_page = "dashboard"

        # Application state
        self.is_fullscreen = False
        self.window_state = {}

        self._initialize_ui()
        self._setup_event_system()

    def _initialize_ui(self):
        """Initialize modern UI components"""
        self.root = tk.Tk()
        self._setup_window()
        self._apply_modern_styling()
        self._create_layout()
        self._create_pages()
        self._setup_keyboard_shortcuts()

    def _setup_window(self):
        """Setup main window with modern properties"""
        self.root.title(
            f"🏭 {self.config.app_name} v{self.config.version} - Modern Edition"
        )

        # Window geometry
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = min(1400, int(screen_width * 0.85))
        window_height = min(900, int(screen_height * 0.85))

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(1200, 800)

        # Window properties
        self.root.configure(bg=self.theme.colors.background)

        # Window icon
        try:
            self.root.iconbitmap("assets/icons/app_icon.ico")
        except:
            pass

    def _apply_modern_styling(self):
        """Apply modern styling and theme"""
        style = ttk.Style()

        # Configure modern themes
        style.theme_use("clam")

        # Modern button styles
        style.configure(
            "Modern.TButton",
            background=self.theme.colors.primary,
            foreground="white",
            borderwidth=0,
            focuscolor="none",
            padding=(20, 10),
        )

        style.map(
            "Modern.TButton",
            background=[
                ("active", self.theme.colors.primary_dark),
                ("pressed", self.theme.colors.primary_light),
            ],
        )

        # Modern frame styles
        style.configure(
            "Card.TFrame",
            background=self.theme.colors.surface,
            relief="flat",
            borderwidth=1,
        )

        # Modern notebook
        style.configure(
            "Modern.TNotebook", background=self.theme.colors.background, borderwidth=0
        )

        style.configure(
            "Modern.TNotebook.Tab",
            background=self.theme.colors.surface,
            foreground=self.theme.colors.text_primary,
            padding=(20, 15),
            borderwidth=0,
        )

        style.map(
            "Modern.TNotebook.Tab",
            background=[
                ("selected", self.theme.colors.primary),
                ("active", self.theme.colors.primary_light),
            ],
            foreground=[("selected", "white"), ("active", "white")],
        )

    def _create_layout(self):
        """Create modern layout structure"""
        # Main container
        main_container = tk.Frame(self.root, bg=self.theme.colors.background)
        main_container.pack(fill="both", expand=True)

        # Header section
        self._create_header(main_container)

        # Content area with sidebar
        content_container = tk.Frame(main_container, bg=self.theme.colors.background)
        content_container.pack(fill="both", expand=True, padx=5, pady=5)

        # Sidebar
        self.sidebar = ModernSidebar(
            content_container, self.theme, self._on_page_changed
        )
        sidebar_widget = self.sidebar.get_widget()
        sidebar_widget.pack(side="left", fill="y", padx=(0, 5))

        # Main content area
        self.content_area = tk.Frame(content_container, bg=self.theme.colors.background)
        self.content_area.pack(side="right", fill="both", expand=True)

        # Status bar
        self.status_bar = ModernStatusBar(main_container, self.theme)
        status_widget = self.status_bar.get_widget()
        status_widget.pack(side="bottom", fill="x")

        # Notification system
        self.notification_system = NotificationSystem(self.root, self.theme)

    def _create_header(self, parent):
        """Create modern header with enhanced features"""
        header_frame = tk.Frame(parent, bg=self.theme.colors.primary, height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        # Header content
        header_content = tk.Frame(header_frame, bg=self.theme.colors.primary)
        header_content.pack(fill="both", expand=True, padx=30, pady=15)

        # Left section - Logo and title
        left_section = tk.Frame(header_content, bg=self.theme.colors.primary)
        left_section.pack(side="left", fill="y")

        # App logo with modern styling
        logo_frame = tk.Frame(left_section, bg=self.theme.colors.primary)
        logo_frame.pack(side="left")

        logo_label = tk.Label(
            logo_frame,
            text="🏭",
            font=("Segoe UI", 28, "bold"),
            fg="white",
            bg=self.theme.colors.primary,
        )
        logo_label.pack()

        # Title section
        title_frame = tk.Frame(left_section, bg=self.theme.colors.primary)
        title_frame.pack(side="left", fill="y", padx=(20, 0))

        app_title = tk.Label(
            title_frame,
            text=f"{self.config.app_name} 2025",
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg=self.theme.colors.primary,
        )
        app_title.pack(anchor="w")

        subtitle = tk.Label(
            title_frame,
            text="Modern Excel to Database Management System",
            font=("Segoe UI", 11),
            fg="#FFB3B3",
            bg=self.theme.colors.primary,
        )
        subtitle.pack(anchor="w", pady=(2, 0))

        # Right section - Controls
        right_section = tk.Frame(header_content, bg=self.theme.colors.primary)
        right_section.pack(side="right", fill="y")

        # Connection status indicator
        self.connection_indicator = tk.Label(
            right_section,
            text="🔴 Disconnected",
            font=("Segoe UI", 11, "bold"),
            fg="white",
            bg=self.theme.colors.primary,
        )
        self.connection_indicator.pack(side="right", padx=(0, 20))

        # Window controls
        controls_frame = tk.Frame(right_section, bg=self.theme.colors.primary)
        controls_frame.pack(side="right")

        # Minimize button
        minimize_btn = tk.Button(
            controls_frame,
            text="─",
            font=("Segoe UI", 12, "bold"),
            bg=self.theme.colors.primary,
            fg="white",
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self._minimize_window,
        )
        minimize_btn.pack(side="left", padx=2)

        # Maximize/Restore button
        self.maximize_btn = tk.Button(
            controls_frame,
            text="□",
            font=("Segoe UI", 12, "bold"),
            bg=self.theme.colors.primary,
            fg="white",
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self._toggle_maximize,
        )
        self.maximize_btn.pack(side="left", padx=2)

        # Close button
        close_btn = tk.Button(
            controls_frame,
            text="✕",
            font=("Segoe UI", 12, "bold"),
            bg="#DC3545",
            fg="white",
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self._close_application,
        )
        close_btn.pack(side="left", padx=2)

    def _create_pages(self):
        """Create all application pages"""
        # Dashboard page
        self.pages["dashboard"] = DashboardPage(
            self.content_area, self.controller, self.theme
        )

        # Import page
        self.pages["import"] = ImportPageModern(
            self.content_area, self.controller, self.theme
        )

        # Database page
        self.pages["database"] = DatabasePageModern(
            self.content_area, self.controller, self.theme
        )

        # Mock data page
        self.pages["mock"] = MockPageModern(
            self.content_area, self.controller, self.theme
        )

        # Analytics page
        self.pages["analytics"] = AnalyticsPage(
            self.content_area, self.controller, self.theme
        )

        # Settings page
        self.pages["settings"] = SettingsPage(
            self.content_area, self.controller, self.theme, self.preferences
        )

        # Show default page
        self._show_page("dashboard")

    def _setup_event_system(self):
        """Setup application event system"""
        # Controller events
        self.controller.subscribe("db_status_changed", self._on_db_status_changed)
        self.controller.subscribe("file_selected", self._on_file_selected)
        self.controller.subscribe("progress_update", self._on_progress_update)
        self.controller.subscribe("operation_complete", self._on_operation_complete)
        self.controller.subscribe("error_occurred", self._on_error_occurred)
        self.controller.subscribe("log_message", self._on_log_message)

        # Window events
        self.root.protocol("WM_DELETE_WINDOW", self._close_application)
        self.root.bind("<Configure>", self._on_window_configure)

    def _setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Global shortcuts
        self.root.bind("<Control-q>", lambda e: self._close_application())
        self.root.bind("<Control-r>", lambda e: self._refresh_current_page())
        self.root.bind("<Control-o>", lambda e: self._show_page("import"))
        self.root.bind("<Control-d>", lambda e: self._show_page("database"))
        self.root.bind("<Control-m>", lambda e: self._show_page("mock"))
        self.root.bind("<F11>", lambda e: self._toggle_fullscreen())
        self.root.bind("<F5>", lambda e: self._refresh_current_page())

        # Developer shortcuts
        self.root.bind("<Control-Shift-D>", lambda e: self._toggle_debug_mode())

    def _on_page_changed(self, page_name: str):
        """Handle page change from sidebar"""
        self._show_page(page_name)

    def _show_page(self, page_name: str):
        """Show specific page"""
        if page_name not in self.pages:
            self.notification_system.show_error(f"Page '{page_name}' not found")
            return

        # Hide current page
        for name, page in self.pages.items():
            if hasattr(page, "hide"):
                page.hide()
            else:
                page.get_widget().pack_forget()

        # Show new page
        page = self.pages[page_name]
        if hasattr(page, "show"):
            page.show()
        else:
            page.get_widget().pack(fill="both", expand=True)

        # Update sidebar selection
        if self.sidebar:
            self.sidebar.select_page(page_name)

        # Update status
        self.current_page = page_name
        self.status_bar.update_status(f"Viewing: {page_name.title()}")

        # Refresh page if needed
        if hasattr(page, "refresh"):
            page.refresh()

    def _on_db_status_changed(self, connected: bool):
        """Handle database status change"""
        if connected:
            self.connection_indicator.configure(text="🟢 Connected", fg="#90EE90")
            self.notification_system.show_success("Database connected successfully")
        else:
            self.connection_indicator.configure(text="🔴 Disconnected", fg="#FFB3B3")

        # Update status bar
        status = "Connected" if connected else "Disconnected"
        self.status_bar.update_connection_status(connected, status)

    def _on_file_selected(self, file_info: Dict[str, Any]):
        """Handle file selection"""
        filename = file_info.get("file_name", "Unknown")
        self.notification_system.show_info(f"File selected: {filename}")
        self.status_bar.update_status(f"File: {filename}")

    def _on_progress_update(self, progress_data: Dict[str, Any]):
        """Handle progress updates"""
        progress = progress_data.get("progress", 0)
        status = progress_data.get("status", "Processing...")
        self.status_bar.update_progress(progress, status)

    def _on_operation_complete(self, operation_data: Dict[str, Any]):
        """Handle operation completion"""
        operation = operation_data.get("operation", "Operation")
        success = operation_data.get("success", False)

        if success:
            self.notification_system.show_success(f"{operation} completed successfully")
        else:
            self.notification_system.show_error(f"{operation} failed")

        self.status_bar.clear_progress()

    def _on_error_occurred(self, error_message: str):
        """Handle error events"""
        self.notification_system.show_error(error_message)
        self.status_bar.update_status("Error occurred", "error")

    def _on_log_message(self, log_data: Dict[str, Any]):
        """Handle log messages"""
        message = log_data.get("message", "")
        level = log_data.get("level", "INFO")

        # Update status bar for important messages
        if level in ["ERROR", "WARNING"]:
            self.status_bar.update_status(
                message, "error" if level == "ERROR" else "warning"
            )

    def _minimize_window(self):
        """Minimize window"""
        self.root.iconify()

    def _toggle_maximize(self):
        """Toggle window maximize state"""
        if self.root.state() == "zoomed":
            self.root.state("normal")
            self.maximize_btn.configure(text="□")
        else:
            self.root.state("zoomed")
            self.maximize_btn.configure(text="❐")

    def _toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)

        if self.is_fullscreen:
            self.notification_system.show_info("Press F11 to exit fullscreen")

    def _refresh_current_page(self):
        """Refresh current page"""
        current_page = self.pages.get(self.current_page)
        if current_page and hasattr(current_page, "refresh"):
            current_page.refresh()
            self.notification_system.show_info("Page refreshed")

    def _toggle_debug_mode(self):
        """Toggle debug mode"""
        # This could enable debug features, logging, etc.
        self.notification_system.show_info("Debug mode toggled")

    def _on_window_configure(self, event):
        """Handle window configuration changes"""
        if event.widget == self.root:
            # Save window state
            self.window_state = {
                "width": self.root.winfo_width(),
                "height": self.root.winfo_height(),
                "x": self.root.winfo_x(),
                "y": self.root.winfo_y(),
            }

    def _close_application(self):
        """Close application with cleanup"""
        try:
            # Ask for confirmation
            if messagebox.askyesno(
                "Exit Application",
                "Are you sure you want to exit DENSO888?",
                icon="question",
            ):
                # Save preferences
                self._save_preferences()

                # Cleanup controller
                if self.controller:
                    self.controller.shutdown()

                # Close notification system
                if self.notification_system:
                    self.notification_system.close()

                # Destroy window
                self.root.quit()
                self.root.destroy()

        except Exception as e:
            print(f"Error during application close: {e}")
            self.root.quit()

    def _save_preferences(self):
        """Save user preferences"""
        try:
            # Update preferences with current state
            self.preferences.window_state = self.window_state

            # Save to file
            prefs_path = Path("config/preferences.json")
            prefs_path.parent.mkdir(exist_ok=True)

            import json

            with open(prefs_path, "w", encoding="utf-8") as f:
                json.dump(self.preferences.__dict__, f, indent=2, ensure_ascii=False)

        except Exception as e:
            print(f"Failed to save preferences: {e}")

    def run(self):
        """Start the application"""
        try:
            # Show welcome notification
            self.root.after(
                1000,
                lambda: self.notification_system.show_success(
                    "Welcome to DENSO888 Modern Edition!"
                ),
            )

            # Start main loop
            self.root.mainloop()

        except KeyboardInterrupt:
            print("\nApplication interrupted by user")
        except Exception as e:
            print(f"Application error: {e}")
            messagebox.showerror("Application Error", f"Critical error:\n\n{str(e)}")
        finally:
            # Ensure cleanup
            if self.controller:
                self.controller.shutdown()


# Enhanced theme for modern UI
class ModernTheme:
    """Modern theme with enhanced color palette and styling"""

    def __init__(self):
        self.colors = self._create_modern_colors()
        self.fonts = self._create_font_system()
        self.spacing = self._create_spacing_system()
        self.shadows = self._create_shadow_system()

    def _create_modern_colors(self):
        """Create modern color palette"""
        from dataclasses import dataclass

        @dataclass
        class ModernColors:
            # Primary colors
            primary: str = "#DC0003"
            primary_dark: str = "#B80002"
            primary_light: str = "#FF3333"
            primary_gradient: tuple = ("#DC0003", "#FF3333")

            # Secondary colors
            secondary: str = "#2C3E50"
            secondary_dark: str = "#1A252F"
            secondary_light: str = "#34495E"

            # Status colors
            success: str = "#10B981"
            warning: str = "#F59E0B"
            danger: str = "#EF4444"
            info: str = "#3B82F6"

            # Neutral colors
            background: str = "#F8FAFC"
            surface: str = "#FFFFFF"
            surface_dark: str = "#F1F5F9"
            border: str = "#E2E8F0"

            # Text colors
            text_primary: str = "#1E293B"
            text_secondary: str = "#64748B"
            text_muted: str = "#94A3B8"
            text_inverse: str = "#FFFFFF"

            # Interactive colors
            hover: str = "#F1F5F9"
            active: str = "#E2E8F0"
            focus: str = "#3B82F6"

            # Glass effect colors
            glass_bg: str = "rgba(255, 255, 255, 0.1)"
            glass_border: str = "rgba(255, 255, 255, 0.2)"

        return ModernColors()

    def _create_font_system(self):
        """Create modern font system"""
        return {
            "heading_xl": ("Segoe UI", 24, "bold"),
            "heading_lg": ("Segoe UI", 20, "bold"),
            "heading_md": ("Segoe UI", 16, "bold"),
            "heading_sm": ("Segoe UI", 14, "bold"),
            "body_lg": ("Segoe UI", 12),
            "body_md": ("Segoe UI", 11),
            "body_sm": ("Segoe UI", 10),
            "caption": ("Segoe UI", 9),
            "code": ("Consolas", 10),
            "code_sm": ("Consolas", 9),
        }

    def _create_spacing_system(self):
        """Create consistent spacing system"""
        return {
            "xs": 4,
            "sm": 8,
            "md": 16,
            "lg": 24,
            "xl": 32,
            "xxl": 48,
        }

    def _create_shadow_system(self):
        """Create shadow system for depth"""
        return {
            "sm": "0 1px 2px rgba(0, 0, 0, 0.05)",
            "md": "0 4px 6px rgba(0, 0, 0, 0.1)",
            "lg": "0 10px 15px rgba(0, 0, 0, 0.1)",
            "xl": "0 20px 25px rgba(0, 0, 0, 0.1)",
        }


if __name__ == "__main__":
    app = DENSO888Application()
    app.run()
