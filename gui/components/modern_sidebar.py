import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

"""
gui/components/modern_sidebar.py
Modern Sidebar with Enhanced UI for 2025
Created by: Thammaphon Chittasuwanna (SDM) | Innovation Department
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, Any, Optional
from datetime import datetime


class ModernSidebar:
    """Modern sidebar with glass effect and animations"""

    def __init__(self, parent: tk.Widget, theme, page_callback: Callable[[str], None]):
        self.parent = parent
        self.theme = theme
        self.page_callback = page_callback
        self.current_selection = "dashboard"

        # Animation properties
        self.animation_speed = 200
        self.hover_effects = {}

        # Sidebar data
        self.menu_items = self._create_menu_structure()

        self.sidebar_frame = None
        self.menu_buttons = {}

        self._create_sidebar()
        self._setup_animations()

    def _create_menu_structure(self) -> list:
        """Create modern menu structure"""
        return [
            {
                "id": "dashboard",
                "title": "Dashboard",
                "icon": "📊",
                "description": "Overview & Analytics",
                "badge": None,
                "category": "main",
            },
            {
                "id": "import",
                "title": "Import Data",
                "icon": "📁",
                "description": "Excel to Database",
                "badge": None,
                "category": "main",
            },
            {
                "id": "database",
                "title": "Database",
                "icon": "🗄️",
                "description": "Configuration & Status",
                "badge": "config",
                "category": "main",
            },
            {
                "id": "mock",
                "title": "Mock Data",
                "icon": "🎲",
                "description": "Generate Test Data",
                "badge": None,
                "category": "main",
            },
            {"id": "separator1", "type": "separator", "category": "tools"},
            {
                "id": "analytics",
                "title": "Analytics",
                "icon": "📈",
                "description": "Data Insights",
                "badge": "new",
                "category": "tools",
            },
            {
                "id": "automation",
                "title": "Automation",
                "icon": "🤖",
                "description": "Scheduled Tasks",
                "badge": "beta",
                "category": "tools",
            },
            {"id": "separator2", "type": "separator", "category": "system"},
            {
                "id": "settings",
                "title": "Settings",
                "icon": "⚙️",
                "description": "App Configuration",
                "badge": None,
                "category": "system",
            },
            {
                "id": "help",
                "title": "Help & Support",
                "icon": "❓",
                "description": "Documentation",
                "badge": None,
                "category": "system",
            },
        ]

    def _create_sidebar(self):
        """Create modern sidebar UI"""
        # Main sidebar frame with modern styling
        self.sidebar_frame = tk.Frame(
            self.parent, bg=self.theme.colors.surface, width=280, relief="flat", bd=1
        )
        self.sidebar_frame.pack_propagate(False)

        # Header section
        self._create_header()

        # Navigation menu
        self._create_navigation_menu()

        # Footer section
        self._create_footer()

    def _create_header(self):
        """Create sidebar header with user info"""
        header_frame = tk.Frame(
            self.sidebar_frame, bg=self.theme.colors.surface, height=120
        )
        header_frame.pack(fill="x", padx=15, pady=(15, 20))
        header_frame.pack_propagate(False)

        # User avatar placeholder
        avatar_frame = tk.Frame(header_frame, bg=self.theme.colors.surface)
        avatar_frame.pack(fill="x", pady=(0, 10))

        avatar_label = tk.Label(
            avatar_frame,
            text="👨‍💻",
            font=("Segoe UI", 28),
            bg=self.theme.colors.surface,
            fg=self.theme.colors.primary,
        )
        avatar_label.pack()

        # User info
        info_frame = tk.Frame(header_frame, bg=self.theme.colors.surface)
        info_frame.pack(fill="x")

        name_label = tk.Label(
            info_frame,
            text="เฮียตอม",
            font=self.theme.fonts["heading_sm"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
        )
        name_label.pack()

        role_label = tk.Label(
            info_frame,
            text="Innovation Department",
            font=self.theme.fonts["body_sm"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_secondary,
        )
        role_label.pack()

    def _create_navigation_menu(self):
        """Create navigation menu with modern styling"""
        menu_frame = tk.Frame(self.sidebar_frame, bg=self.theme.colors.surface)
        menu_frame.pack(fill="both", expand=True, padx=10)

        current_category = None

        for item in self.menu_items:
            # Category header
            if item.get("category") != current_category:
                current_category = item.get("category")
                if current_category and current_category != "main":
                    category_label = tk.Label(
                        menu_frame,
                        text=current_category.upper(),
                        font=self.theme.fonts["caption"],
                        bg=self.theme.colors.surface,
                        fg=self.theme.colors.text_muted,
                        anchor="w",
                    )
                    category_label.pack(fill="x", pady=(15, 5), padx=5)

            # Separator
            if item.get("type") == "separator":
                separator = tk.Frame(menu_frame, bg=self.theme.colors.border, height=1)
                separator.pack(fill="x", pady=10, padx=10)
                continue

            # Menu item
            self._create_menu_item(menu_frame, item)

    def _create_menu_item(self, parent, item: Dict[str, Any]):
        """Create individual menu item with modern styling"""
        item_id = item["id"]

        # Main button frame
        btn_frame = tk.Frame(parent, bg=self.theme.colors.surface)
        btn_frame.pack(fill="x", pady=2)

        # Button with hover effects
        button = tk.Button(
            btn_frame,
            text="",
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
            bd=0,
            relief="flat",
            cursor="hand2",
            command=lambda: self._on_menu_click(item_id),
            anchor="w",
            padx=15,
            pady=12,
        )
        button.pack(fill="x")

        # Custom button content
        self._setup_button_content(button, item)
        self._setup_button_events(button, item)

        self.menu_buttons[item_id] = button

    def _setup_button_content(self, button: tk.Button, item: Dict[str, Any]):
        """Setup button content with icon, text, and badge"""
        content_frame = tk.Frame(button, bg=self.theme.colors.surface)
        content_frame.pack(fill="both", expand=True)

        # Icon and text container
        main_content = tk.Frame(content_frame, bg=self.theme.colors.surface)
        main_content.pack(side="left", fill="both", expand=True)

        # Icon
        icon_label = tk.Label(
            main_content,
            text=item["icon"],
            font=("Segoe UI", 16),
            bg=self.theme.colors.surface,
            fg=self.theme.colors.primary,
        )
        icon_label.pack(side="left", padx=(0, 10))

        # Text container
        text_container = tk.Frame(main_content, bg=self.theme.colors.surface)
        text_container.pack(side="left", fill="both", expand=True)

        # Title
        title_label = tk.Label(
            text_container,
            text=item["title"],
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
            anchor="w",
        )
        title_label.pack(fill="x")

        # Description
        desc_label = tk.Label(
            text_container,
            text=item["description"],
            font=self.theme.fonts["caption"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_secondary,
            anchor="w",
        )
        desc_label.pack(fill="x")

        # Badge
        if item.get("badge"):
            badge = self._create_badge(content_frame, item["badge"])
            badge.pack(side="right", padx=(5, 0))

        # Store references for styling updates
        button.icon_label = icon_label
        button.title_label = title_label
        button.desc_label = desc_label
        button.content_frame = content_frame

    def _create_badge(self, parent, badge_text: str) -> tk.Widget:
        """Create modern badge"""
        badge_colors = {
            "new": (self.theme.colors.success, "white"),
            "beta": (self.theme.colors.warning, "white"),
            "config": (self.theme.colors.info, "white"),
            "hot": (self.theme.colors.danger, "white"),
        }

        bg_color, fg_color = badge_colors.get(
            badge_text, (self.theme.colors.text_muted, "white")
        )

        badge_frame = tk.Frame(parent, bg=self.theme.colors.surface)

        badge_label = tk.Label(
            badge_frame,
            text=badge_text.upper(),
            font=("Segoe UI", 8, "bold"),
            bg=bg_color,
            fg=fg_color,
            padx=6,
            pady=2,
        )
        badge_label.pack()

        return badge_frame

    def _setup_button_events(self, button: tk.Button, item: Dict[str, Any]):
        """Setup hover and click events"""

        def on_enter(event):
            if item["id"] != self.current_selection:
                button.configure(bg=self.theme.colors.hover)
                button.content_frame.configure(bg=self.theme.colors.hover)
                # Update all child widgets
                self._update_widget_bg(button.content_frame, self.theme.colors.hover)

        def on_leave(event):
            if item["id"] != self.current_selection:
                button.configure(bg=self.theme.colors.surface)
                button.content_frame.configure(bg=self.theme.colors.surface)
                self._update_widget_bg(button.content_frame, self.theme.colors.surface)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def _update_widget_bg(self, widget, bg_color):
        """Recursively update background color of all child widgets"""
        try:
            widget.configure(bg=bg_color)
            for child in widget.winfo_children():
                self._update_widget_bg(child, bg_color)
        except tk.TclError:
            pass

    def _create_footer(self):
        """Create sidebar footer"""
        footer_frame = tk.Frame(
            self.sidebar_frame, bg=self.theme.colors.surface, height=80
        )
        footer_frame.pack(fill="x", side="bottom", padx=15, pady=15)
        footer_frame.pack_propagate(False)

        # Version info
        version_frame = tk.Frame(footer_frame, bg=self.theme.colors.surface)
        version_frame.pack(fill="x")

        version_label = tk.Label(
            version_frame,
            text="DENSO888 v2.0.0",
            font=self.theme.fonts["caption"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_secondary,
        )
        version_label.pack()

        # Status indicator
        status_frame = tk.Frame(footer_frame, bg=self.theme.colors.surface)
        status_frame.pack(fill="x", pady=(5, 0))

        self.status_indicator = tk.Label(
            status_frame,
            text="🟢 System Ready",
            font=self.theme.fonts["caption"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.success,
        )
        self.status_indicator.pack()

    def _setup_animations(self):
        """Setup animation system"""
        # This could be enhanced with actual animations
        pass

    def _on_menu_click(self, item_id: str):
        """Handle menu item click"""
        if item_id != self.current_selection:
            # Update selection
            old_selection = self.current_selection
            self.current_selection = item_id

            # Update visual state
            self._update_selection_state(old_selection, item_id)

            # Trigger callback
            if self.page_callback:
                self.page_callback(item_id)

    def _update_selection_state(self, old_id: str, new_id: str):
        """Update visual state for selection"""
        # Reset old selection
        if old_id in self.menu_buttons:
            old_button = self.menu_buttons[old_id]
            old_button.configure(bg=self.theme.colors.surface)
            old_button.content_frame.configure(bg=self.theme.colors.surface)
            self._update_widget_bg(old_button.content_frame, self.theme.colors.surface)

        # Highlight new selection
        if new_id in self.menu_buttons:
            new_button = self.menu_buttons[new_id]
            new_button.configure(bg=self.theme.colors.primary_light)
            new_button.content_frame.configure(bg=self.theme.colors.primary_light)
            self._update_widget_bg(
                new_button.content_frame, self.theme.colors.primary_light
            )

            # Update text colors for selected state
            if hasattr(new_button, "title_label"):
                new_button.title_label.configure(fg="white")
            if hasattr(new_button, "desc_label"):
                new_button.desc_label.configure(fg="rgba(255,255,255,0.8)")

    def select_page(self, page_id: str):
        """Programmatically select a page"""
        if page_id in self.menu_buttons:
            self._on_menu_click(page_id)

    def update_badge(self, item_id: str, badge_text: Optional[str]):
        """Update badge for menu item"""
        # This could be implemented to dynamically update badges
        pass

    def update_status(self, status_text: str, status_type: str = "success"):
        """Update footer status"""
        status_colors = {
            "success": self.theme.colors.success,
            "warning": self.theme.colors.warning,
            "error": self.theme.colors.danger,
            "info": self.theme.colors.info,
        }

        status_icons = {"success": "🟢", "warning": "🟡", "error": "🔴", "info": "🔵"}

        color = status_colors.get(status_type, self.theme.colors.text_secondary)
        icon = status_icons.get(status_type, "ℹ️")

        self.status_indicator.configure(text=f"{icon} {status_text}", fg=color)

    def get_widget(self) -> tk.Widget:
        """Get the main sidebar widget"""
        return self.sidebar_frame


# Enhanced Status Bar Component
class ModernStatusBar:
    """Modern status bar with enhanced features"""

    def __init__(self, parent: tk.Widget, theme):
        self.parent = parent
        self.theme = theme
        self.status_bar = None
        self.progress_var = None
        self.progress_bar = None

        self._create_status_bar()

    def _create_status_bar(self):
        """Create modern status bar"""
        self.status_bar = tk.Frame(
            self.parent, bg=self.theme.colors.surface, height=35, relief="flat", bd=1
        )
        self.status_bar.pack_propagate(False)

        # Left section - Status text
        left_frame = tk.Frame(self.status_bar, bg=self.theme.colors.surface)
        left_frame.pack(side="left", fill="both", expand=True, padx=(15, 5))

        self.status_label = tk.Label(
            left_frame,
            text="Ready",
            font=self.theme.fonts["body_sm"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
            anchor="w",
        )
        self.status_label.pack(side="left", fill="y")

        # Center section - Progress bar
        center_frame = tk.Frame(self.status_bar, bg=self.theme.colors.surface)
        center_frame.pack(side="left", padx=10)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            center_frame,
            variable=self.progress_var,
            maximum=100,
            length=200,
            mode="determinate",
        )
        # Initially hidden

        # Right section - Connection status and time
        right_frame = tk.Frame(self.status_bar, bg=self.theme.colors.surface)
        right_frame.pack(side="right", padx=(5, 15))

        # Connection status
        self.connection_label = tk.Label(
            right_frame,
            text="🔴 Disconnected",
            font=self.theme.fonts["body_sm"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_secondary,
        )
        self.connection_label.pack(side="right", padx=(10, 0))

        # Current time
        self.time_label = tk.Label(
            right_frame,
            text="",
            font=self.theme.fonts["body_sm"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_secondary,
        )
        self.time_label.pack(side="right")

        # Start time updater
        self._update_time()

    def update_status(self, text: str, status_type: str = "info"):
        """Update status text"""
        status_colors = {
            "info": self.theme.colors.text_primary,
            "success": self.theme.colors.success,
            "warning": self.theme.colors.warning,
            "error": self.theme.colors.danger,
        }

        color = status_colors.get(status_type, self.theme.colors.text_primary)
        self.status_label.configure(text=text, fg=color)

    def update_progress(self, progress: float, text: str = ""):
        """Update progress bar"""
        self.progress_var.set(progress)

        if not self.progress_bar.winfo_viewable():
            self.progress_bar.pack(side="left", pady=5)

        if text:
            self.update_status(text)

    def clear_progress(self):
        """Clear progress bar"""
        self.progress_bar.pack_forget()
        self.progress_var.set(0)

    def update_connection_status(self, connected: bool, details: str = ""):
        """Update connection status"""
        if connected:
            icon = "🟢"
            text = f"Connected {details}".strip()
            color = self.theme.colors.success
        else:
            icon = "🔴"
            text = f"Disconnected {details}".strip()
            color = self.theme.colors.danger

        self.connection_label.configure(text=f"{icon} {text}", fg=color)

    def _update_time(self):
        """Update current time display"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=current_time)

        # Schedule next update
        self.parent.after(1000, self._update_time)

    def get_widget(self) -> tk.Widget:
        """Get the status bar widget"""
        return self.status_bar


# Modern Notification System
class NotificationSystem:
    """Modern notification system with toast messages"""

    def __init__(self, parent: tk.Widget, theme):
        self.parent = parent
        self.theme = theme
        self.notifications = []
        self.notification_queue = []

    def show_success(self, message: str, duration: int = 3000):
        """Show success notification"""
        self._show_notification(message, "success", duration)

    def show_error(self, message: str, duration: int = 5000):
        """Show error notification"""
        self._show_notification(message, "error", duration)

    def show_warning(self, message: str, duration: int = 4000):
        """Show warning notification"""
        self._show_notification(message, "warning", duration)

    def show_info(self, message: str, duration: int = 3000):
        """Show info notification"""
        self._show_notification(message, "info", duration)

    def _show_notification(self, message: str, type_: str, duration: int):
        """Show notification toast"""
        # Create notification window
        notification = tk.Toplevel(self.parent)
        notification.withdraw()
        notification.overrideredirect(True)
        notification.attributes("-topmost", True)

        # Configure based on type
        type_config = {
            "success": {"bg": self.theme.colors.success, "icon": "✅"},
            "error": {"bg": self.theme.colors.danger, "icon": "❌"},
            "warning": {"bg": self.theme.colors.warning, "icon": "⚠️"},
            "info": {"bg": self.theme.colors.info, "icon": "ℹ️"},
        }

        config = type_config.get(type_, type_config["info"])

        # Notification frame
        frame = tk.Frame(notification, bg=config["bg"], padx=20, pady=15)
        frame.pack(fill="both", expand=True)

        # Icon and message
        content_frame = tk.Frame(frame, bg=config["bg"])
        content_frame.pack(fill="both", expand=True)

        icon_label = tk.Label(
            content_frame,
            text=config["icon"],
            font=("Segoe UI", 16),
            bg=config["bg"],
            fg="white",
        )
        icon_label.pack(side="left", padx=(0, 10))

        text_label = tk.Label(
            content_frame,
            text=message,
            font=self.theme.fonts["body_md"],
            bg=config["bg"],
            fg="white",
            wraplength=300,
        )
        text_label.pack(side="left", fill="both", expand=True)

        # Position notification
        notification.update_idletasks()
        width = notification.winfo_reqwidth()
        height = notification.winfo_reqheight()

        screen_width = notification.winfo_screenwidth()
        x = screen_width - width - 20
        y = 20 + len(self.notifications) * (height + 10)

        notification.geometry(f"{width}x{height}+{x}+{y}")
        notification.deiconify()

        # Add to active notifications
        self.notifications.append(notification)

        # Auto-hide after duration
        def hide_notification():
            try:
                if notification.winfo_exists():
                    notification.destroy()
                if notification in self.notifications:
                    self.notifications.remove(notification)
                self._reposition_notifications()
            except:
                pass

        notification.after(duration, hide_notification)

        # Click to dismiss
        def on_click(event):
            hide_notification()

        notification.bind("<Button-1>", on_click)
        frame.bind("<Button-1>", on_click)
        content_frame.bind("<Button-1>", on_click)

    def _reposition_notifications(self):
        """Reposition remaining notifications"""
        for i, notification in enumerate(self.notifications):
            if notification.winfo_exists():
                height = notification.winfo_reqheight()
                y = 20 + i * (height + 10)
                x = notification.winfo_x()
                notification.geometry(f"+{x}+{y}")

    def close(self):
        """Close all notifications"""
        for notification in self.notifications[:]:
            try:
                if notification.winfo_exists():
                    notification.destroy()
            except:
                pass
        self.notifications.clear()


"""
gui/components/modern_sidebar.py
Modern Sidebar Component - Complete Working Version
"""

import tkinter as tk
from typing import List, Dict, Any, Callable, Optional
from datetime import datetime


class ModernSidebar:
    """Modern sidebar with navigation menu"""

    def __init__(
        self,
        parent: tk.Widget,
        menu_items: List[Dict[str, Any]],
        callback: Callable[[str], None],
        theme=None,
    ):
        self.parent = parent
        self.menu_items = menu_items
        self.callback = callback
        self.theme = theme or self._get_default_theme()
        self.current_selection = None
        self.menu_buttons = {}

        self.widget = None
        self._create_sidebar()

    def _get_default_theme(self):
        """Get default theme"""

        class DefaultTheme:
            class colors:
                white = "#FFFFFF"
                gray_50 = "#F9FAFB"
                gray_100 = "#F3F4F6"
                gray_200 = "#E5E7EB"
                gray_600 = "#4B5563"
                gray_900 = "#111827"
                primary = "#2563EB"
                primary_light = "#DBEAFE"

        return DefaultTheme()

    def _create_sidebar(self):
        """Create sidebar widget"""
        # Main sidebar frame
        self.widget = tk.Frame(
            self.parent, bg=self.theme.colors.gray_50, width=280, relief="flat", bd=0
        )
        self.widget.pack_propagate(False)

        # Header section
        self._create_header()

        # Navigation menu
        self._create_navigation()

        # Footer section
        self._create_footer()

    def _create_header(self):
        """Create sidebar header"""
        header_frame = tk.Frame(self.widget, bg=self.theme.colors.gray_50, height=100)
        header_frame.pack(fill="x", padx=20, pady=20)
        header_frame.pack_propagate(False)

        # App logo/title
        title_label = tk.Label(
            header_frame,
            text="🏭 DENSO888",
            font=("Segoe UI", 18, "bold"),
            bg=self.theme.colors.gray_50,
            fg=self.theme.colors.primary,
        )
        title_label.pack(anchor="w")

        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Modern Edition",
            font=("Segoe UI", 11),
            bg=self.theme.colors.gray_50,
            fg=self.theme.colors.gray_600,
        )
        subtitle_label.pack(anchor="w", pady=(2, 0))

        # User info
        user_label = tk.Label(
            header_frame,
            text="👨‍💻 เฮียตอม | Innovation Dept.",
            font=("Segoe UI", 10),
            bg=self.theme.colors.gray_50,
            fg=self.theme.colors.gray_600,
        )
        user_label.pack(anchor="w", pady=(10, 0))

    def _create_navigation(self):
        """Create navigation menu"""
        nav_frame = tk.Frame(self.widget, bg=self.theme.colors.gray_50)
        nav_frame.pack(fill="both", expand=True, padx=10)

        # Menu title
        menu_title = tk.Label(
            nav_frame,
            text="NAVIGATION",
            font=("Segoe UI", 9, "bold"),
            bg=self.theme.colors.gray_50,
            fg=self.theme.colors.gray_600,
        )
        menu_title.pack(anchor="w", padx=10, pady=(0, 10))

        # Menu items
        for item in self.menu_items:
            self._create_menu_item(nav_frame, item)

    def _create_menu_item(self, parent: tk.Widget, item: Dict[str, Any]):
        """Create individual menu item"""
        item_id = item["id"]

        # Menu button frame
        btn_frame = tk.Frame(parent, bg=self.theme.colors.gray_50)
        btn_frame.pack(fill="x", pady=2)

        # Main button
        button = tk.Button(
            btn_frame,
            text="",
            bg=self.theme.colors.gray_50,
            fg=self.theme.colors.gray_900,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda: self._on_menu_click(item_id),
            anchor="w",
            padx=15,
            pady=12,
        )
        button.pack(fill="x")

        # Button content frame
        content_frame = tk.Frame(button, bg=self.theme.colors.gray_50)
        content_frame.pack(fill="x")

        # Icon and text container
        main_content = tk.Frame(content_frame, bg=self.theme.colors.gray_50)
        main_content.pack(fill="x")

        # Icon
        icon_label = tk.Label(
            main_content,
            text=item.get("icon", "📋"),
            font=("Segoe UI", 16),
            bg=self.theme.colors.gray_50,
            fg=self.theme.colors.primary,
        )
        icon_label.pack(side="left", padx=(0, 12))

        # Text container
        text_container = tk.Frame(main_content, bg=self.theme.colors.gray_50)
        text_container.pack(side="left", fill="x", expand=True)

        # Title
        title_label = tk.Label(
            text_container,
            text=item.get("title", "Menu Item"),
            font=("Segoe UI", 12, "bold"),
            bg=self.theme.colors.gray_50,
            fg=self.theme.colors.gray_900,
            anchor="w",
        )
        title_label.pack(fill="x")

        # Description
        if item.get("description"):
            desc_label = tk.Label(
                text_container,
                text=item["description"],
                font=("Segoe UI", 9),
                bg=self.theme.colors.gray_50,
                fg=self.theme.colors.gray_600,
                anchor="w",
            )
            desc_label.pack(fill="x")

        # Store references
        button.content_frame = content_frame
        button.icon_label = icon_label
        button.title_label = title_label
        button.main_content = main_content
        button.text_container = text_container

        self.menu_buttons[item_id] = button

        # Hover effects
        self._setup_hover_effects(button, item_id)

    def _setup_hover_effects(self, button: tk.Button, item_id: str):
        """Setup hover effects for menu item"""

        def on_enter(event):
            if item_id != self.current_selection:
                self._update_button_colors(button, self.theme.colors.gray_100)

        def on_leave(event):
            if item_id != self.current_selection:
                self._update_button_colors(button, self.theme.colors.gray_50)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def _update_button_colors(self, button: tk.Button, bg_color: str):
        """Update button colors recursively"""
        try:
            button.configure(bg=bg_color)
            if hasattr(button, "content_frame"):
                self._update_widget_bg_recursive(button.content_frame, bg_color)
        except:
            pass

    def _update_widget_bg_recursive(self, widget, bg_color: str):
        """Recursively update background color"""
        try:
            widget.configure(bg=bg_color)
            for child in widget.winfo_children():
                if isinstance(child, (tk.Frame, tk.Label)):
                    self._update_widget_bg_recursive(child, bg_color)
        except:
            pass

    def _on_menu_click(self, item_id: str):
        """Handle menu item click"""
        if item_id == self.current_selection:
            return

        # Update selection
        old_selection = self.current_selection
        self.current_selection = item_id

        # Update visual state
        self._update_selection_state(old_selection, item_id)

        # Call callback
        if self.callback:
            try:
                self.callback(item_id)
            except Exception as e:
                print(f"Menu callback error: {e}")

    def _update_selection_state(self, old_id: Optional[str], new_id: str):
        """Update visual selection state"""
        # Reset old selection
        if old_id and old_id in self.menu_buttons:
            old_button = self.menu_buttons[old_id]
            self._update_button_colors(old_button, self.theme.colors.gray_50)

        # Highlight new selection
        if new_id in self.menu_buttons:
            new_button = self.menu_buttons[new_id]
            self._update_button_colors(new_button, self.theme.colors.primary_light)

    def _create_footer(self):
        """Create sidebar footer"""
        footer_frame = tk.Frame(self.widget, bg=self.theme.colors.gray_50, height=80)
        footer_frame.pack(fill="x", side="bottom", padx=20, pady=20)
        footer_frame.pack_propagate(False)

        # Version info
        version_label = tk.Label(
            footer_frame,
            text="DENSO888 v3.0",
            font=("Segoe UI", 9),
            bg=self.theme.colors.gray_50,
            fg=self.theme.colors.gray_600,
        )
        version_label.pack(anchor="w")

        # Status
        self.status_label = tk.Label(
            footer_frame,
            text="🟢 System Ready",
            font=("Segoe UI", 9),
            bg=self.theme.colors.gray_50,
            fg=self.theme.colors.gray_600,
        )
        self.status_label.pack(anchor="w", pady=(5, 0))

        # Current time
        self.time_label = tk.Label(
            footer_frame,
            text="",
            font=("Segoe UI", 9),
            bg=self.theme.colors.gray_50,
            fg=self.theme.colors.gray_600,
        )
        self.time_label.pack(anchor="w", pady=(5, 0))

        # Update time
        self._update_time()

    def _update_time(self):
        """Update current time display"""
        current_time = datetime.now().strftime("%H:%M:%S")
        if hasattr(self, "time_label"):
            self.time_label.configure(text=current_time)

        # Schedule next update
        self.widget.after(1000, self._update_time)

    def select_item(self, item_id: str):
        """Programmatically select menu item"""
        if item_id in self.menu_buttons:
            self._on_menu_click(item_id)

    def update_status(self, status: str, status_type: str = "info"):
        """Update status display"""
        status_icons = {"info": "🔵", "success": "🟢", "warning": "🟡", "error": "🔴"}

        icon = status_icons.get(status_type, "🔵")
        if hasattr(self, "status_label"):
            self.status_label.configure(text=f"{icon} {status}")

    def get_widget(self) -> tk.Widget:
        """Get main sidebar widget"""
        return self.widget


class ModernStatusBar:
    """Modern status bar component"""

    def __init__(self, parent: tk.Widget, theme=None):
        self.parent = parent
        self.theme = theme or self._get_default_theme()
        self.widget = None
        self._create_status_bar()

    def _get_default_theme(self):
        """Get default theme"""

        class DefaultTheme:
            class colors:
                gray_50 = "#F9FAFB"
                gray_600 = "#4B5563"
                gray_900 = "#111827"
                success = "#10B981"
                error = "#EF4444"

        return DefaultTheme()

    def _create_status_bar(self):
        """Create status bar"""
        self.widget = tk.Frame(
            self.parent, bg=self.theme.colors.gray_50, height=35, relief="flat", bd=0
        )
        self.widget.pack_propagate(False)

        # Left section - Status
        left_frame = tk.Frame(self.widget, bg=self.theme.colors.gray_50)
        left_frame.pack(side="left", fill="y", padx=20)

        self.status_label = tk.Label(
            left_frame,
            text="Ready",
            font=("Segoe UI", 10),
            bg=self.theme.colors.gray_50,
            fg=self.theme.colors.gray_900,
        )
        self.status_label.pack(side="left", pady=8)

        # Right section - Info
        right_frame = tk.Frame(self.widget, bg=self.theme.colors.gray_50)
        right_frame.pack(side="right", fill="y", padx=20)

        # Database status
        self.db_status = tk.Label(
            right_frame,
            text="🔴 Database: Disconnected",
            font=("Segoe UI", 10),
            bg=self.theme.colors.gray_50,
            fg=self.theme.colors.error,
        )
        self.db_status.pack(side="right", pady=8, padx=(0, 10))

        # Current time
        self.time_label = tk.Label(
            right_frame,
            text="",
            font=("Segoe UI", 10),
            bg=self.theme.colors.gray_50,
            fg=self.theme.colors.gray_600,
        )
        self.time_label.pack(side="right", pady=8)

        self._update_time()

    def _update_time(self):
        """Update time display"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=current_time)
        self.widget.after(1000, self._update_time)

    def update_status(self, text: str, status_type: str = "info"):
        """Update status text"""
        self.status_label.configure(text=text)

    def update_db_status(self, connected: bool):
        """Update database status"""
        if connected:
            self.db_status.configure(
                text="🟢 Database: Connected", fg=self.theme.colors.success
            )
        else:
            self.db_status.configure(
                text="🔴 Database: Disconnected", fg=self.theme.colors.error
            )

    def get_widget(self) -> tk.Widget:
        """Get status bar widget"""
        return self.widget
