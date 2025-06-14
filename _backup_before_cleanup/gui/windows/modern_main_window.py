# gui/windows/main_window.py
"""
Clean Main Window - Separated Concerns & Maintainable
แยก logic ชัดเจน ไม่มี code duplication
"""

import tkinter as tk
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass

# Import ระบบ services ใหม่
from core.services import get_service_manager

# Import UI components ใหม่
from gui.core import ComponentFactory, create_component_factory, Sidebar


@dataclass
class AppConfig:
    """Configuration for main application"""

    title: str = "🏭 DENSO888"
    version: str = "2.0.0"
    author: str = "Thammaphon Chittasuwanna (SDM)"
    window_size: tuple = (1200, 800)
    theme: str = "denso"


class NavigationState:
    """Handle navigation state management"""

    def __init__(self):
        self.current_view: str = "dashboard"
        self.view_history: list = []
        self.callbacks: Dict[str, list] = {}

    def register_callback(self, event: str, callback: Callable):
        """Register callback for navigation events"""
        if event not in self.callbacks:
            self.callbacks[event] = []
        self.callbacks[event].append(callback)

    def navigate_to(self, view: str):
        """Navigate to a view"""
        old_view = self.current_view
        self.view_history.append(old_view)
        self.current_view = view

        # Notify callbacks
        for callback in self.callbacks.get("view_changed", []):
            callback(old_view, view)

    def go_back(self):
        """Go back to previous view"""
        if self.view_history:
            previous_view = self.view_history.pop()
            self.current_view = previous_view

            for callback in self.callbacks.get("view_changed", []):
                callback(self.current_view, previous_view)


class StatusManager:
    """Handle status updates and notifications"""

    def __init__(self):
        self.current_status: str = "Ready"
        self.status_callbacks: list = []

    def register_status_callback(self, callback: Callable):
        """Register status update callback"""
        self.status_callbacks.append(callback)

    def update_status(self, message: str, status_type: str = "info"):
        """Update application status"""
        self.current_status = message

        for callback in self.status_callbacks:
            callback(message, status_type)


class MainApplicationWindow:
    """Clean main window with separated concerns"""

    def __init__(self, config: AppConfig = None):
        self.config = config or AppConfig()

        # Core managers
        self.navigation = NavigationState()
        self.status_manager = StatusManager()

        # UI components
        self.root: Optional[tk.Tk] = None
        self.component_factory: Optional[ComponentFactory] = None
        self.sidebar: Optional[Sidebar] = None
        self.content_area: Optional[tk.Frame] = None
        self.status_bar: Optional[tk.Frame] = None

        # View managers
        self.view_managers: Dict[str, Any] = {}

        # Setup callbacks
        self._setup_callbacks()

    def _setup_callbacks(self):
        """Setup internal callbacks"""
        self.navigation.register_callback("view_changed", self._on_view_changed)
        self.status_manager.register_status_callback(self._on_status_update)

    def initialize(self) -> bool:
        """Initialize the application"""
        try:
            # Initialize services
            service_results = get_service_manager().initialize_all()

            # Create UI
            self._create_window()
            self._create_ui_components()
            self._setup_views()

            # Show initial view
            self.navigation.navigate_to("dashboard")

            self.status_manager.update_status("Application ready", "success")
            return True

        except Exception as e:
            self.status_manager.update_status(f"Initialization failed: {e}", "error")
            return False

    def _create_window(self):
        """Create main window"""
        self.root = tk.Tk()
        self.root.title(f"{self.config.title} v{self.config.version}")
        self.root.geometry(f"{self.config.window_size[0]}x{self.config.window_size[1]}")

        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.config.window_size[0] // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.config.window_size[1] // 2)
        self.root.geometry(f"+{x}+{y}")

        # Setup component factory with theme
        self.component_factory = create_component_factory(self.config.theme)

        # Apply theme to root
        colors = self.component_factory.theme.get_colors()
        self.root.configure(bg=colors.background)

    def _create_ui_components(self):
        """Create main UI layout"""
        # Main container
        main_container = tk.Frame(self.root)
        main_container.pack(fill="both", expand=True)

        # Create sidebar
        self.sidebar = self.component_factory.create_sidebar(main_container, width=250)
        self.sidebar.pack(side="left", fill="y")

        # Add navigation items
        nav_items = [
            ("🏠", "Dashboard", lambda: self.navigation.navigate_to("dashboard")),
            ("📊", "Excel Import", lambda: self.navigation.navigate_to("excel")),
            ("🎲", "Mock Data", lambda: self.navigation.navigate_to("mock")),
            ("🗄️", "Database", lambda: self.navigation.navigate_to("database")),
            ("📈", "Analytics", lambda: self.navigation.navigate_to("analytics")),
            ("⚙️", "Settings", lambda: self.navigation.navigate_to("settings")),
        ]

        for icon, text, command in nav_items:
            self.sidebar.add_nav_item(icon, text, command)

        # Create content area
        self.content_area = tk.Frame(main_container)
        self.content_area.pack(side="right", fill="both", expand=True)

        # Create status bar
        self._create_status_bar()

    def _create_status_bar(self):
        """Create status bar"""
        colors = self.component_factory.theme.get_colors()

        self.status_bar = tk.Frame(
            self.root, bg=colors.surface, height=30, relief="flat", borderwidth=1
        )
        self.status_bar.pack(side="bottom", fill="x")
        self.status_bar.pack_propagate(False)

        # Status content
        status_content = tk.Frame(self.status_bar, bg=colors.surface)
        status_content.pack(fill="both", expand=True, padx=10, pady=5)

        # Status label
        self.status_label = tk.Label(
            status_content,
            text="🟢 Ready",
            font=("Segoe UI", 9),
            fg=colors.text_primary,
            bg=colors.surface,
        )
        self.status_label.pack(side="left")

        # Version info
        version_label = tk.Label(
            status_content,
            text=f"v{self.config.version} | {self.config.author}",
            font=("Segoe UI", 9),
            fg=colors.text_secondary,
            bg=colors.surface,
        )
        version_label.pack(side="right")

    def _setup_views(self):
        """Setup view managers"""
        from gui.views import (
            DashboardView,
            ExcelImportView,
            MockDataView,
            DatabaseView,
            AnalyticsView,
            SettingsView,
        )

        self.view_managers = {
            "dashboard": DashboardView(self.content_area, self.component_factory, self),
            "excel": ExcelImportView(self.content_area, self.component_factory, self),
            "mock": MockDataView(self.content_area, self.component_factory, self),
            "database": DatabaseView(self.content_area, self.component_factory, self),
            "analytics": AnalyticsView(self.content_area, self.component_factory, self),
            "settings": SettingsView(self.content_area, self.component_factory, self),
        }

    def _on_view_changed(self, old_view: str, new_view: str):
        """Handle view changes"""
        # Hide old view
        if old_view in self.view_managers:
            self.view_managers[old_view].hide()

        # Show new view
        if new_view in self.view_managers:
            self.view_managers[new_view].show()

        # Update sidebar highlighting
        self._update_sidebar_highlight(new_view)

    def _update_sidebar_highlight(self, active_view: str):
        """Update sidebar to show active view"""
        # Implementation would highlight the active navigation item
        pass

    def _on_status_update(self, message: str, status_type: str):
        """Handle status updates"""
        status_icons = {"info": "🔵", "success": "🟢", "warning": "🟡", "error": "🔴"}

        icon = status_icons.get(status_type, "🔵")
        self.status_label.configure(text=f"{icon} {message}")

    def run(self):
        """Run the application"""
        if self.root:
            self.root.mainloop()

    def close(self):
        """Clean shutdown"""
        if self.root:
            self.root.destroy()


# ===== VIEW BASE CLASS =====
class BaseView:
    """Base class for all views"""

    def __init__(self, parent: tk.Widget, factory: ComponentFactory, app_window):
        self.parent = parent
        self.factory = factory
        self.app_window = app_window
        self.view_frame: Optional[tk.Frame] = None
        self.is_created = False

    def show(self):
        """Show the view"""
        if not self.is_created:
            self._create_view()
            self.is_created = True

        if self.view_frame:
            self.view_frame.pack(fill="both", expand=True)

    def hide(self):
        """Hide the view"""
        if self.view_frame:
            self.view_frame.pack_forget()

    def _create_view(self):
        """Create view content - implement in subclasses"""
        colors = self.factory.theme.get_colors()
        self.view_frame = tk.Frame(self.parent, bg=colors.background)

    def update_status(self, message: str, status_type: str = "info"):
        """Update application status"""
        self.app_window.status_manager.update_status(message, status_type)


# ===== ENTRY POINT =====
def create_application(config: AppConfig = None) -> MainApplicationWindow:
    """Create and initialize application"""
    app = MainApplicationWindow(config)

    if app.initialize():
        return app
    else:
        raise RuntimeError("Failed to initialize application")


def main():
    """Main entry point"""
    try:
        # Create configuration
        config = AppConfig(
            title="🏭 DENSO888",
            version="2.0.0 - Clean Edition",
            author="Thammaphon Chittasuwanna (SDM) | เฮียตอมจัดหั้ย!!!",
            theme="denso",
        )

        # Create and run application
        app = create_application(config)
        print(f"🚀 Starting {config.title}")
        print(f"Created by: {config.author}")

        app.run()

    except Exception as e:
        print(f"❌ Application failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
