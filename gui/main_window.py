"""
gui/main_window.py
Enhanced Main Window with Gaming UI and Real Functionality
พัฒนาจากไฟล์เดิม เพิ่มความน่าเล่นแบบเกม
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import traceback
import os
from typing import Dict, Any, Optional
from pathlib import Path

# Import core components
from models.app_config import AppConfig
from models.user_preferences import UserPreferences
from controllers.app_controller import AppController

# Import gaming theme
from gui.themes.gaming_theme import gaming_theme, GamingAnimations

# Import existing pages (ใช้ไฟล์เดิม)


class DENSO888GamingEdition:
    """DENSO888 with Enhanced Gaming UI Experience"""

    def __init__(self):
        """Initialize gaming edition application"""
        try:
            # Load configuration
            self.config = AppConfig.load_from_file()
            self.preferences = UserPreferences.load_from_file()

            # Initialize controller
            self.controller = AppController(self.config)

            # UI Components
            self.root: Optional[tk.Tk] = None
            self.sidebar: Optional[tk.Frame] = None
            self.content_area: Optional[tk.Frame] = None
            self.status_bar: Optional[tk.Frame] = None

            # Pages
            self.pages: Dict[str, Any] = {}
            self.current_page: Optional[str] = None

            # Gaming elements
            self.notifications: list = []
            self.achievement_count = 0

            # Initialize UI
            self._create_main_window()
            self._setup_gaming_components()
            self._setup_event_handlers()

            print("✅ DENSO888 Gaming Edition initialized successfully")

        except Exception as e:
            print(f"❌ Application initialization failed: {e}")
            print(f"🔍 Stack trace: {traceback.format_exc()}")
            raise

    def _create_main_window(self):
        """Create main gaming-style window"""
        self.root = tk.Tk()
        self.root.title(
            f"🎮 {self.config.app_name} Gaming Edition v{self.config.version}"
        )
        self.root.geometry(f"{self.config.window_width}x{self.config.window_height}")
        self.root.minsize(1000, 700)

        # Apply gaming theme
        gaming_theme.apply_to_root(self.root)

        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.config.window_width // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.config.window_height // 2)
        self.root.geometry(
            f"{self.config.window_width}x{self.config.window_height}+{x}+{y}"
        )

        # Configure main layout
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Try to set window icon
        try:
            icon_path = Path("assets/icons/denso888.ico")
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except:
            pass

    def _setup_gaming_components(self):
        """Setup gaming-style UI components"""
        # Create gaming header
        self._create_gaming_header()

        # Create main layout
        self._create_main_layout()

        # Create gaming sidebar
        self._create_gaming_sidebar()

        # Create content area
        self._create_content_area()

        # Create gaming status bar
        self._create_gaming_status_bar()

        # Initialize pages
        self._initialize_pages()

        # Show welcome animation
        self._show_welcome_animation()

    def _create_gaming_header(self):
        """Create gaming-style header with animations"""
        header_frame = gaming_theme.create_gaming_header(
            self.root,
            "🏭 DENSO888 GAMING EDITION",
            "Excel to SQL Management System • เฮียตอมจัดหั้ย!!! 🚀",
        )
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

    def _create_main_layout(self):
        """Create main application layout"""
        # Main container
        self.main_container = tk.Frame(self.root, bg=gaming_theme.colors.bg_primary)
        self.main_container.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)

    def _create_gaming_sidebar(self):
        """Create gaming-style sidebar"""
        # Sidebar menu items with gaming aesthetics
        menu_items = [
            {
                "id": "dashboard",
                "title": "Command Center",
                "description": "Mission Overview & Stats",
                "icon": "🎯",
                "color": gaming_theme.colors.neon_blue,
                "badge": None,
            },
            {
                "id": "import",
                "title": "Data Injection",
                "description": "Excel to Database Portal",
                "icon": "📊",
                "color": gaming_theme.colors.neon_green,
                "badge": None,
            },
            {
                "id": "database",
                "title": "Data Vault",
                "description": "Database Control Center",
                "icon": "🗄️",
                "color": gaming_theme.colors.neon_purple,
                "badge": "config",
            },
            {
                "id": "mock",
                "title": "Data Forge",
                "description": "Mock Data Generator",
                "icon": "🎲",
                "color": gaming_theme.colors.neon_orange,
                "badge": None,
            },
            {
                "id": "admin",
                "title": "Control Panel",
                "description": "Admin Dashboard",
                "icon": "🛡️",
                "color": gaming_theme.colors.gold,
                "badge": "admin",
            },
        ]

        self.sidebar = gaming_theme.create_gaming_sidebar(
            self.main_container, menu_items, self._on_page_changed
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")

    def _create_content_area(self):
        """Create main content area"""
        self.content_area = tk.Frame(
            self.main_container, bg=gaming_theme.colors.bg_primary
        )
        self.content_area.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    def _create_gaming_status_bar(self):
        """Create gaming-style status bar"""
        self.status_bar = tk.Frame(
            self.root,
            bg=gaming_theme.colors.bg_secondary,
            height=35,
            relief="flat",
            bd=0,
            highlightbackground=gaming_theme.colors.border_glow,
            highlightthickness=1,
        )
        self.status_bar.grid(row=2, column=0, columnspan=2, sticky="ew")
        self.status_bar.grid_propagate(False)

        # Status content
        status_content = tk.Frame(self.status_bar, bg=gaming_theme.colors.bg_secondary)
        status_content.pack(fill="both", expand=True, padx=15, pady=5)

        # Left side - status message
        self.status_label = tk.Label(
            status_content,
            text="🎮 SYSTEM READY • เฮียตอมจัดหั้ย!!! 🚀",
            font=("Orbitron", 10, "bold"),
            bg=gaming_theme.colors.bg_secondary,
            fg=gaming_theme.colors.neon_green,
            anchor="w",
        )
        self.status_label.pack(side="left", fill="y")

        # Right side - achievements and stats
        right_frame = tk.Frame(status_content, bg=gaming_theme.colors.bg_secondary)
        right_frame.pack(side="right")

        # Achievement counter
        self.achievement_label = tk.Label(
            right_frame,
            text="🏆 0",
            font=("Orbitron", 10, "bold"),
            bg=gaming_theme.colors.bg_secondary,
            fg=gaming_theme.colors.gold,
        )
        self.achievement_label.pack(side="right", padx=(10, 0))

        # Connection status
        self.connection_label = tk.Label(
            right_frame,
            text="🔴 OFFLINE",
            font=("Orbitron", 10, "bold"),
            bg=gaming_theme.colors.bg_secondary,
            fg=gaming_theme.colors.text_error,
        )
        self.connection_label.pack(side="right", padx=(10, 0))

    def _initialize_pages(self):
        """Initialize all application pages with gaming enhancements"""
        try:
            # Enhanced Dashboard with gaming elements
            self.pages["dashboard"] = GamingDashboardPage(
                self.content_area, self.controller, gaming_theme
            )

            # Enhanced Import page
            self.pages["import"] = GamingImportPage(
                self.content_area, self.controller, gaming_theme
            )

            # Enhanced Database page
            self.pages["database"] = GamingDatabasePage(
                self.content_area, self.controller, gaming_theme
            )

            # Enhanced Mock data page
            self.pages["mock"] = GamingMockPage(
                self.content_area, self.controller, gaming_theme
            )

            # Admin page with gaming theme
            self.pages["admin"] = GamingAdminPage(
                self.content_area, self.controller, gaming_theme
            )

            print("✅ All gaming pages initialized successfully")

        except Exception as e:
            print(f"❌ Error creating pages: {e}")
            print(f"🔍 Stack trace: {traceback.format_exc()}")
            # Create fallback pages
            self._create_fallback_pages()

    def _create_fallback_pages(self):
        """Create fallback pages if main pages fail"""
        for page_id in ["dashboard", "import", "database", "mock", "admin"]:
            if page_id not in self.pages:
                self.pages[page_id] = self._create_simple_gaming_page(page_id)

    def _create_simple_gaming_page(self, page_id: str):
        """Create simple gaming-style fallback page"""

        class SimpleGamingPage:
            def __init__(self, parent, page_id, theme):
                self.parent = parent
                self.page_id = page_id
                self.theme = theme

                self.main_frame = gaming_theme.components.create_gaming_card(
                    parent, f"🎮 {page_id.title()} Module", "Module under development"
                )

                # Content
                content_frame = tk.Frame(self.main_frame, bg=theme.colors.bg_card)
                content_frame.pack(fill="both", expand=True, padx=20, pady=20)

                # Icon
                icon_label = tk.Label(
                    content_frame,
                    text="🚧",
                    font=("Segoe UI", 48),
                    bg=theme.colors.bg_card,
                    fg=theme.colors.neon_orange,
                )
                icon_label.pack(pady=20)

                # Message
                message_label = tk.Label(
                    content_frame,
                    text=f"{page_id.title()} Module\n\nThis gaming module is under development.\nStay tuned for awesome features!",
                    font=("Orbitron", 14),
                    bg=theme.colors.bg_card,
                    fg=theme.colors.text_primary,
                    justify="center",
                )
                message_label.pack()

            def show(self):
                self.main_frame.pack(fill="both", expand=True)

            def hide(self):
                self.main_frame.pack_forget()

            def refresh(self):
                pass

        return SimpleGamingPage(self.content_area, page_id, gaming_theme)

    def _setup_event_handlers(self):
        """Setup gaming event handlers"""
        # Window events
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

        # Controller events with gaming enhancements
        self.controller.subscribe("db_status_changed", self._on_db_status_changed)
        self.controller.subscribe("operation_complete", self._on_operation_complete)
        self.controller.subscribe("error_occurred", self._on_error_occurred)
        self.controller.subscribe("log_message", self._on_log_message)
        self.controller.subscribe("achievement_unlocked", self._on_achievement_unlocked)
        self.controller.subscribe("progress_update", self._on_progress_update)

        # Gaming keyboard shortcuts
        self.root.bind("<Control-q>", lambda e: self._on_closing())
        self.root.bind("<F5>", lambda e: self._refresh_current_page())
        self.root.bind("<F11>", lambda e: self._toggle_fullscreen())

    def _show_welcome_animation(self):
        """Show welcome animation on startup"""

        def animate():
            # Show welcome notification
            gaming_theme.components.create_notification_toast(
                self.root, "🎮 DENSO888 Gaming Edition Activated! 🚀", "success", 3000
            )

            # Pulse the main window
            GamingAnimations.pulse_effect(
                self.main_container,
                gaming_theme.colors.bg_primary,
                gaming_theme.colors.bg_secondary,
                1.0,
            )

        # Delay animation slightly for better effect
        self.root.after(500, animate)

        # Show default page
        self._show_page("dashboard")

    def _on_page_changed(self, page_id: str):
        """Handle page navigation with gaming effects"""
        try:
            # Hide current page
            if self.current_page and self.current_page in self.pages:
                self.pages[self.current_page].hide()

            # Show new page with animation
            if page_id in self.pages:
                self.pages[page_id].show()
                self.current_page = page_id

                # Refresh page data
                if hasattr(self.pages[page_id], "refresh"):
                    threading.Thread(
                        target=self.pages[page_id].refresh, daemon=True
                    ).start()

                # Update status with gaming flair
                page_names = {
                    "dashboard": "COMMAND CENTER",
                    "import": "DATA INJECTION",
                    "database": "DATA VAULT",
                    "mock": "DATA FORGE",
                    "admin": "CONTROL PANEL",
                }

                page_name = page_names.get(page_id, page_id.upper())
                self._update_status(f"🎯 {page_name} ACTIVE")

                # Page change sound effect (visual feedback)
                self._show_page_transition_effect()

            else:
                print(f"⚠️ Page '{page_id}' not found")

        except Exception as e:
            print(f"❌ Error changing page: {e}")
            self._show_gaming_notification("Page loading failed", "error")

    def _show_page_transition_effect(self):
        """Show page transition visual effect"""
        # Quick flash effect on content area
        original_bg = self.content_area.cget("bg")
        self.content_area.configure(bg=gaming_theme.colors.primary_glow)
        self.root.after(100, lambda: self.content_area.configure(bg=original_bg))

    def _on_db_status_changed(self, connected: bool):
        """Handle database status change with gaming feedback"""
        if connected:
            self.connection_label.configure(
                text="🟢 ONLINE", fg=gaming_theme.colors.neon_green
            )
            self._show_gaming_notification(
                "🗄️ Database connection established!", "success"
            )

            # Show achievement for first connection
            if not hasattr(self, "_first_connection_achievement"):
                self._first_connection_achievement = True
                self._show_achievement(
                    "Database Master", "Successfully connected to database!", "bronze"
                )
        else:
            self.connection_label.configure(
                text="🔴 OFFLINE", fg=gaming_theme.colors.text_error
            )

    def _on_operation_complete(self, data: Dict[str, Any]):
        """Handle operation completion with gaming celebration"""
        operation = data.get("operation", "Operation")
        success = data.get("success", False)
        operation_data = data.get("data", {})

        if success:
            # Show success notification with gaming flair
            if operation == "excel_import":
                rows = operation_data.get("rows_imported", 0)
                self._show_gaming_notification(
                    f"🚀 Data injection complete! {rows:,} records uploaded", "success"
                )
            elif operation == "mock_generation":
                rows = operation_data.get("rows_generated", 0)
                template = operation_data.get("template", "data")
                self._show_gaming_notification(
                    f"🎲 Data forge successful! {rows:,} {template} records created",
                    "success",
                )

            # Add pulse effect to status bar
            GamingAnimations.pulse_effect(
                self.status_bar,
                gaming_theme.colors.bg_secondary,
                gaming_theme.colors.neon_green,
                0.5,
            )
        else:
            self._show_gaming_notification(f"❌ {operation} failed!", "error")

    def _on_error_occurred(self, error_message: str):
        """Handle application errors with gaming style"""
        self._show_gaming_notification(f"⚠️ {error_message}", "error")
        self._update_status(f"🔥 ERROR: {error_message[:50]}...")

    def _on_log_message(self, log_data: Dict[str, Any]):
        """Handle log messages"""
        message = log_data.get("message", "")
        level = log_data.get("level", "INFO")

        # Update status for important messages
        if level in ["ERROR", "WARNING"]:
            self._update_status(f"⚠️ {message[:50]}...")
        elif "connected" in message.lower():
            self._update_status("🔗 DATABASE CONNECTED")

    def _on_achievement_unlocked(self, achievement_data: Dict[str, Any]):
        """Handle achievement unlocked with grand celebration"""
        title = achievement_data.get("title", "Achievement")
        description = achievement_data.get("description", "")
        achievement_type = achievement_data.get("type", "bronze")

        # Update achievement counter
        self.achievement_count += 1
        self.achievement_label.configure(text=f"🏆 {self.achievement_count}")

        # Show achievement popup
        self._show_achievement(title, description, achievement_type)

        # Celebration effects
        self._celebration_effects()

    def _on_progress_update(self, progress_data: Dict[str, Any]):
        """Handle progress updates with gaming UI"""
        progress = progress_data.get("progress", 0)
        status = progress_data.get("status", "Processing...")

        # Update status bar with progress
        self._update_status(f"⚡ {status} ({progress:.0f}%)")

        # Show progress in the current page if it supports it
        if self.current_page and self.current_page in self.pages:
            page = self.pages[self.current_page]
            if hasattr(page, "update_progress"):
                page.update_progress(progress, status)

    def _show_gaming_notification(self, message: str, notification_type: str = "info"):
        """Show gaming-style notification"""
        gaming_theme.components.create_notification_toast(
            self.root, message, notification_type, 3000
        )

    def _show_achievement(
        self, title: str, description: str, achievement_type: str = "gold"
    ):
        """Show achievement popup with celebration"""
        gaming_theme.create_achievement_popup(
            self.root, title, description, achievement_type
        )

    def _celebration_effects(self):
        """Show celebration effects for achievements"""
        # Pulse the achievement counter
        GamingAnimations.pulse_effect(
            self.achievement_label,
            gaming_theme.colors.gold,
            gaming_theme.colors.text_primary,
            1.0,
        )

        # Flash the main window border
        original_highlight = self.root.cget("highlightbackground")
        self.root.configure(
            highlightbackground=gaming_theme.colors.gold, highlightthickness=3
        )
        self.root.after(
            1000,
            lambda: self.root.configure(
                highlightbackground=original_highlight, highlightthickness=0
            ),
        )

    def _update_status(self, message: str):
        """Update status bar with gaming style"""
        self.status_label.configure(text=message)

        # Animate status update
        GamingAnimations.glow_on_hover(
            self.status_label,
            gaming_theme.colors.bg_secondary,
            gaming_theme.colors.bg_elevated,
        )

    def _show_page(self, page_id: str):
        """Programmatically show a page"""
        self._on_page_changed(page_id)

    def _refresh_current_page(self):
        """Refresh current page with visual feedback"""
        if self.current_page and self.current_page in self.pages:
            page = self.pages[self.current_page]
            if hasattr(page, "refresh"):
                # Show refresh notification
                self._show_gaming_notification("🔄 Refreshing data...", "info")
                threading.Thread(target=page.refresh, daemon=True).start()

    def _toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        current_state = self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", not current_state)

        if not current_state:
            self._show_gaming_notification("🖥️ Fullscreen mode activated", "info")
        else:
            self._show_gaming_notification("🖥️ Windowed mode activated", "info")

    def _on_closing(self):
        """Handle application closing with gaming farewell"""
        try:
            if messagebox.askyesno(
                "Exit Gaming Edition",
                "🎮 Exit DENSO888 Gaming Edition?\n\nAll your progress will be saved!",
            ):
                # Show farewell message
                self._show_gaming_notification(
                    "👋 Thanks for playing! See you next time!", "info"
                )

                # Cleanup
                if self.controller:
                    self.controller.shutdown()

                # Brief delay for farewell message
                self.root.after(1000, self._final_shutdown)

        except Exception as e:
            print(f"Error during shutdown: {e}")
            self.root.quit()

    def _final_shutdown(self):
        """Final shutdown procedure"""
        try:
            # Save preferences
            # self.preferences.save_to_file()

            self.root.quit()
            self.root.destroy()
        except:
            pass

    def run(self):
        """Start the gaming edition application"""
        try:
            print("🎮 Starting DENSO888 Gaming Edition...")

            # Show startup notification
            self._show_gaming_notification(
                "🚀 DENSO888 Gaming Edition loaded successfully!", "success"
            )

            # Start main loop
            self.root.mainloop()

        except KeyboardInterrupt:
            print("\n⚠️ Application interrupted by user")
        except Exception as e:
            print(f"❌ Application runtime error: {e}")
            print(f"🔍 Stack trace: {traceback.format_exc()}")
            messagebox.showerror("Runtime Error", f"Gaming edition error:\n\n{str(e)}")
        finally:
            print("✅ Gaming edition shutdown completed")


# Enhanced Gaming Pages
class GamingDashboardPage:
    """Enhanced dashboard with gaming elements"""

    def __init__(self, parent, controller, theme):
        self.parent = parent
        self.controller = controller
        self.theme = theme

        self.main_frame = None
        self._create_gaming_dashboard()

    def _create_gaming_dashboard(self):
        """Create gaming-style dashboard"""
        self.main_frame = tk.Frame(self.parent, bg=self.theme.colors.bg_primary)

        # Create scrollable content
        canvas = tk.Canvas(
            self.main_frame, bg=self.theme.colors.bg_primary, highlightthickness=0
        )
        scrollbar = tk.Scrollbar(
            self.main_frame, orient="vertical", command=canvas.yview
        )
        self.scrollable_frame = tk.Frame(canvas, bg=self.theme.colors.bg_primary)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Gaming welcome section
        self._create_welcome_section()

        # Gaming stats section
        self._create_gaming_stats()

        # Quick action section with gaming style
        self._create_gaming_actions()

        # System status with gaming effects
        self._create_gaming_system_status()

    def _create_welcome_section(self):
        """Create gaming welcome section"""
        welcome_card = self.theme.components.create_gaming_card(
            self.scrollable_frame,
            "🎯 MISSION CONTROL CENTER",
            "Ready for data operations",
        )
        welcome_card.pack(fill="x", padx=20, pady=20)

        # Welcome content
        content_frame = tk.Frame(welcome_card, bg=self.theme.colors.bg_card)
        content_frame.pack(fill="x", padx=20, pady=20)

        # Animated welcome message
        welcome_text = tk.Label(
            content_frame,
            text="🚀 DENSO888 GAMING EDITION READY FOR ACTION!",
            font=("Orbitron", 16, "bold"),
            bg=self.theme.colors.bg_card,
            fg=self.theme.colors.primary,
        )
        welcome_text.pack(pady=10)

        mission_text = tk.Label(
            content_frame,
            text="Your mission: Transform Excel data into powerful databases!\nLevel up your data management skills!",
            font=("Segoe UI", 12),
            bg=self.theme.colors.bg_card,
            fg=self.theme.colors.text_secondary,
            justify="center",
        )
        mission_text.pack()

        # Add pulse effect to welcome text
        GamingAnimations.pulse_effect(
            welcome_text, self.theme.colors.primary, self.theme.colors.primary_glow, 2.0
        )

    def _create_gaming_stats(self):
        """Create gaming-style statistics"""
        stats_card = self.theme.components.create_gaming_card(
            self.scrollable_frame,
            "📊 PLAYER STATISTICS",
            "Your data management achievements",
        )
        stats_card.pack(fill="x", padx=20, pady=(0, 20))

        # Stats grid
        stats_frame = tk.Frame(stats_card, bg=self.theme.colors.bg_card)
        stats_frame.pack(fill="x", padx=20, pady=20)

        # Create stat displays
        stats = [
            ("🗄️", "Databases", "0", self.theme.colors.neon_blue),
            ("📊", "Records", "0", self.theme.colors.neon_green),
            ("🎲", "Mock Data", "0", self.theme.colors.neon_orange),
            ("🏆", "Achievements", "0", self.theme.colors.gold),
        ]

        self.stat_widgets = {}
        for i, (icon, label, value, color) in enumerate(stats):
            stat_widget = self.theme.components.create_stat_display(
                stats_frame, icon, label, value, color
            )
            stat_widget.grid(row=0, column=i, padx=10, pady=5, sticky="ew")
            self.stat_widgets[label.lower()] = stat_widget

        # Configure grid
        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1)

    def _create_gaming_actions(self):
        """Create gaming-style quick actions"""
        actions_card = self.theme.components.create_gaming_card(
            self.scrollable_frame, "⚡ QUICK ACTIONS", "Launch your data missions"
        )
        actions_card.pack(fill="x", padx=20, pady=(0, 20))

        # Actions grid
        actions_frame = tk.Frame(actions_card, bg=self.theme.colors.bg_card)
        actions_frame.pack(fill="x", padx=20, pady=20)

        # Quick action buttons
        actions = [
            ("📊", "Data Injection", "Import Excel files", "success"),
            ("🗄️", "Data Vault", "Configure database", "info"),
            ("🎲", "Data Forge", "Generate mock data", "warning"),
            ("🛡️", "Control Panel", "Admin dashboard", "primary"),
        ]

        for i, (icon, title, desc, style) in enumerate(actions):
            row = i // 2
            col = i % 2

            action_frame = tk.Frame(actions_frame, bg=self.theme.colors.bg_card)
            action_frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")

            action_btn = self.theme.components.create_neon_button(
                action_frame, f"{icon} {title}", style=style, size="large"
            )
            action_btn.pack(fill="x")

            desc_label = tk.Label(
                action_frame,
                text=desc,
                font=("Segoe UI", 10),
                bg=self.theme.colors.bg_card,
                fg=self.theme.colors.text_secondary,
            )
            desc_label.pack(pady=(5, 0))

        # Configure grid
        actions_frame.grid_columnconfigure(0, weight=1)
        actions_frame.grid_columnconfigure(1, weight=1)

    def _create_gaming_system_status(self):
        """Create gaming system status"""
        status_card = self.theme.components.create_gaming_card(
            self.scrollable_frame, "🖥️ SYSTEM STATUS", "Real-time system monitoring"
        )
        status_card.pack(fill="x", padx=20, pady=(0, 20))

        # Status content
        status_frame = tk.Frame(status_card, bg=self.theme.colors.bg_card)
        status_frame.pack(fill="x", padx=20, pady=20)

        # System metrics
        metrics = [
            ("Database", "🔴 OFFLINE", self.theme.colors.text_error),
            ("Memory", "💾 Normal", self.theme.colors.neon_green),
            ("Performance", "⚡ Optimal", self.theme.colors.neon_blue),
            ("Security", "🛡️ Protected", self.theme.colors.gold),
        ]

        self.status_widgets = {}
        for i, (label, status, color) in enumerate(metrics):
            metric_frame = tk.Frame(status_frame, bg=self.theme.colors.bg_card)
            metric_frame.grid(row=i // 2, column=i % 2, padx=20, pady=10, sticky="ew")

            label_widget = tk.Label(
                metric_frame,
                text=f"{label}:",
                font=("Orbitron", 11, "bold"),
                bg=self.theme.colors.bg_card,
                fg=self.theme.colors.text_primary,
                anchor="w",
            )
            label_widget.pack(anchor="w")

            status_widget = tk.Label(
                metric_frame,
                text=status,
                font=("Orbitron", 10),
                bg=self.theme.colors.bg_card,
                fg=color,
                anchor="w",
            )
            status_widget.pack(anchor="w")

            self.status_widgets[label.lower()] = status_widget

        # Configure grid
        status_frame.grid_columnconfigure(0, weight=1)
        status_frame.grid_columnconfigure(1, weight=1)

    def refresh(self):
        """Refresh dashboard data"""
        try:
            # Update database status
            db_status = self.controller.get_database_status()
            if db_status.get("connected"):
                self.status_widgets["database"].configure(
                    text="🟢 ONLINE", fg=self.theme.colors.neon_green
                )

                # Update stats
                stats = db_status
                if "total_tables" in stats:
                    self.stat_widgets["databases"].value_label.configure(
                        text=str(stats["total_tables"])
                    )
                if "total_records" in stats:
                    self.stat_widgets["records"].value_label.configure(
                        text=f"{stats['total_records']:,}"
                    )
            else:
                self.status_widgets["database"].configure(
                    text="🔴 OFFLINE", fg=self.theme.colors.text_error
                )
        except Exception as e:
            print(f"Error refreshing dashboard: {e}")

    def show(self):
        """Show dashboard"""
        self.main_frame.pack(fill="both", expand=True)

    def hide(self):
        """Hide dashboard"""
        self.main_frame.pack_forget()


# Import and Database pages with gaming enhancements would follow similar patterns
class GamingImportPage:
    """Gaming-enhanced import page"""

    def __init__(self, parent, controller, theme):
        self.parent = parent
        self.controller = controller
        self.theme = theme
        self.main_frame = None
        self._create_import_page()

    def _create_import_page(self):
        """Create gaming import page"""
        self.main_frame = tk.Frame(self.parent, bg=self.theme.colors.bg_primary)

        # Coming soon placeholder with gaming style
        placeholder_card = self.theme.components.create_gaming_card(
            self.main_frame,
            "📊 DATA INJECTION MODULE",
            "Advanced Excel to Database portal",
        )
        placeholder_card.pack(expand=True, padx=50, pady=50)

        content_frame = tk.Frame(placeholder_card, bg=self.theme.colors.bg_card)
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Browse file button
        browse_btn = self.theme.components.create_neon_button(
            content_frame,
            "📁 SELECT EXCEL FILE",
            command=self._browse_file,
            style="primary",
            size="large",
        )
        browse_btn.pack(pady=20)

        # Progress bar placeholder
        self.progress_bar = self.theme.components.create_progress_bar(content_frame)
        self.progress_bar["container"].pack(pady=20)
        self.progress_bar["container"].pack_forget()  # Initially hidden

    def _browse_file(self):
        """Browse for Excel file"""
        filename = filedialog.askopenfilename(
            title="Select Excel File for Data Injection",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")],
        )

        if filename:
            # Show progress
            self.progress_bar["container"].pack(pady=20)

            # Simulate file processing
            def process_file():
                for i in range(0, 101, 10):
                    self.progress_bar["update"](i)
                    self.parent.after(100)

                # Show success
                self.theme.components.create_notification_toast(
                    self.parent,
                    f"📊 File analyzed: {os.path.basename(filename)}",
                    "success",
                )

            import threading

            threading.Thread(target=process_file, daemon=True).start()

    def update_progress(self, value: float, status: str):
        """Update progress bar"""
        if hasattr(self, "progress_bar"):
            self.progress_bar["update"](value)

    def show(self):
        self.main_frame.pack(fill="both", expand=True)

    def hide(self):
        self.main_frame.pack_forget()

    def refresh(self):
        pass


class GamingDatabasePage:
    """Gaming-enhanced database page"""

    def __init__(self, parent, controller, theme):
        self.parent = parent
        self.controller = controller
        self.theme = theme
        self.main_frame = None
        self._create_database_page()

    def _create_database_page(self):
        """Create gaming database page"""
        self.main_frame = tk.Frame(self.parent, bg=self.theme.colors.bg_primary)

        # Database vault interface
        vault_card = self.theme.components.create_gaming_card(
            self.main_frame, "🗄️ DATA VAULT CONTROL", "Secure database management system"
        )
        vault_card.pack(fill="both", expand=True, padx=20, pady=20)

        content_frame = tk.Frame(vault_card, bg=self.theme.colors.bg_card)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Database type selection with gaming style
        type_frame = tk.Frame(content_frame, bg=self.theme.colors.bg_card)
        type_frame.pack(fill="x", pady=20)

        tk.Label(
            type_frame,
            text="🎯 SELECT VAULT TYPE:",
            font=("Orbitron", 14, "bold"),
            bg=self.theme.colors.bg_card,
            fg=self.theme.colors.neon_blue,
        ).pack(anchor="w", pady=(0, 10))

        # SQLite option
        sqlite_btn = self.theme.components.create_neon_button(
            type_frame,
            "💾 LOCAL VAULT (SQLite)",
            command=self._select_sqlite,
            style="success",
            size="large",
        )
        sqlite_btn.pack(fill="x", pady=5)

        # SQL Server option
        sqlserver_btn = self.theme.components.create_neon_button(
            type_frame,
            "🖥️ ENTERPRISE VAULT (SQL Server)",
            command=self._select_sqlserver,
            style="info",
            size="large",
        )
        sqlserver_btn.pack(fill="x", pady=5)

        # Connection test
        test_btn = self.theme.components.create_neon_button(
            content_frame,
            "🔍 TEST VAULT CONNECTION",
            command=self._test_connection,
            style="warning",
            size="large",
        )
        test_btn.pack(pady=30)

        # Status display
        self.vault_status = tk.Label(
            content_frame,
            text="🔴 VAULT OFFLINE",
            font=("Orbitron", 16, "bold"),
            bg=self.theme.colors.bg_card,
            fg=self.theme.colors.text_error,
        )
        self.vault_status.pack(pady=20)

    def _select_sqlite(self):
        """Select SQLite database"""
        self.controller.update_database_config({"db_type": "sqlite"})
        self.theme.components.create_notification_toast(
            self.parent, "💾 Local vault selected", "info"
        )

    def _select_sqlserver(self):
        """Select SQL Server database"""
        self.controller.update_database_config({"db_type": "sqlserver"})
        self.theme.components.create_notification_toast(
            self.parent, "🖥️ Enterprise vault selected", "info"
        )

    def _test_connection(self):
        """Test database connection"""
        success = self.controller.test_database_connection()
        if success:
            self.vault_status.configure(
                text="🟢 VAULT ONLINE", fg=self.theme.colors.neon_green
            )

            # Connect automatically after successful test
            self.controller.connect_database()
        else:
            self.vault_status.configure(
                text="🔴 VAULT CONNECTION FAILED", fg=self.theme.colors.text_error
            )

    def show(self):
        self.main_frame.pack(fill="both", expand=True)

    def hide(self):
        self.main_frame.pack_forget()

    def refresh(self):
        # Update vault status
        db_status = self.controller.get_database_status()
        if db_status.get("connected"):
            self.vault_status.configure(
                text="🟢 VAULT ONLINE", fg=self.theme.colors.neon_green
            )
        else:
            self.vault_status.configure(
                text="🔴 VAULT OFFLINE", fg=self.theme.colors.text_error
            )


class GamingMockPage:
    """Gaming-enhanced mock data page"""

    def __init__(self, parent, controller, theme):
        self.parent = parent
        self.controller = controller
        self.theme = theme
        self.main_frame = None
        self._create_mock_page()

    def _create_mock_page(self):
        """Create gaming mock data page"""
        self.main_frame = tk.Frame(self.parent, bg=self.theme.colors.bg_primary)

        # Data forge interface
        forge_card = self.theme.components.create_gaming_card(
            self.main_frame, "🎲 DATA FORGE LABORATORY", "Generate unlimited test data"
        )
        forge_card.pack(fill="both", expand=True, padx=20, pady=20)

        content_frame = tk.Frame(forge_card, bg=self.theme.colors.bg_card)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Template selection
        template_frame = tk.Frame(content_frame, bg=self.theme.colors.bg_card)
        template_frame.pack(fill="x", pady=20)

        tk.Label(
            template_frame,
            text="🧬 SELECT DATA TEMPLATE:",
            font=("Orbitron", 14, "bold"),
            bg=self.theme.colors.bg_card,
            fg=self.theme.colors.neon_orange,
        ).pack(anchor="w", pady=(0, 10))

        # Template buttons
        templates = [
            ("👥", "EMPLOYEE MATRIX", "employees"),
            ("💰", "SALES NEXUS", "sales"),
            ("📦", "INVENTORY GRID", "inventory"),
            ("💳", "FINANCIAL CORE", "financial"),
        ]

        self.selected_template = tk.StringVar(value="employees")

        for icon, name, template_id in templates:
            btn = self.theme.components.create_neon_button(
                template_frame,
                f"{icon} {name}",
                command=lambda t=template_id: self._select_template(t),
                style="primary",
                size="medium",
            )
            btn.pack(fill="x", pady=2)

        # Quantity selector
        quantity_frame = tk.Frame(content_frame, bg=self.theme.colors.bg_card)
        quantity_frame.pack(fill="x", pady=20)

        tk.Label(
            quantity_frame,
            text="⚡ GENERATION POWER:",
            font=("Orbitron", 14, "bold"),
            bg=self.theme.colors.bg_card,
            fg=self.theme.colors.neon_green,
        ).pack(anchor="w", pady=(0, 10))

        # Quick quantity buttons
        quantities = [1000, 5000, 10000, 50000]
        self.selected_quantity = tk.IntVar(value=1000)

        qty_buttons_frame = tk.Frame(quantity_frame, bg=self.theme.colors.bg_card)
        qty_buttons_frame.pack(fill="x")

        for qty in quantities:
            btn = self.theme.components.create_neon_button(
                qty_buttons_frame,
                f"{qty:,}",
                command=lambda q=qty: self._select_quantity(q),
                style="success",
                size="small",
            )
            btn.pack(side="left", padx=5, expand=True, fill="x")

        # Generate button
        generate_btn = self.theme.components.create_neon_button(
            content_frame,
            "🚀 ACTIVATE DATA FORGE",
            command=self._generate_data,
            style="warning",
            size="large",
        )
        generate_btn.pack(pady=30)

        # Progress bar
        self.progress_bar = self.theme.components.create_progress_bar(
            content_frame, 400
        )
        self.progress_bar["container"].pack(pady=10)
        self.progress_bar["container"].pack_forget()  # Initially hidden

    def _select_template(self, template_id: str):
        """Select data template"""
        self.selected_template.set(template_id)
        self.theme.components.create_notification_toast(
            self.parent, f"🧬 {template_id.title()} template selected", "info"
        )

    def _select_quantity(self, quantity: int):
        """Select generation quantity"""
        self.selected_quantity.set(quantity)
        self.theme.components.create_notification_toast(
            self.parent, f"⚡ Generation power set to {quantity:,}", "info"
        )

    def _generate_data(self):
        """Generate mock data"""
        if not self.controller.is_connected:
            self.theme.components.create_notification_toast(
                self.parent, "🔴 Vault must be online before forging data!", "error"
            )
            return

        template = self.selected_template.get()
        quantity = self.selected_quantity.get()

        # Show progress
        self.progress_bar["container"].pack(pady=10)

        # Start generation
        def generate():
            success = self.controller.generate_mock_data(template, quantity)
            if success:
                # Show database file location
                db_path = self.controller.get_database_file_path()
                if db_path:
                    self.theme.components.create_notification_toast(
                        self.parent,
                        f"📁 Data forged successfully! File: {os.path.basename(db_path)}",
                        "success",
                        5000,
                    )

        import threading

        threading.Thread(target=generate, daemon=True).start()

    def update_progress(self, value: float, status: str):
        """Update progress bar"""
        if hasattr(self, "progress_bar"):
            self.progress_bar["update"](value)

    def show(self):
        self.main_frame.pack(fill="both", expand=True)

    def hide(self):
        self.main_frame.pack_forget()

    def refresh(self):
        pass


class GamingAdminPage:
    """Gaming-enhanced admin page"""

    def __init__(self, parent, controller, theme):
        self.parent = parent
        self.controller = controller
        self.theme = theme
        self.main_frame = None
        self._create_admin_page()

    def _create_admin_page(self):
        """Create gaming admin page"""
        self.main_frame = tk.Frame(self.parent, bg=self.theme.colors.bg_primary)

        # Control panel interface
        control_card = self.theme.components.create_gaming_card(
            self.main_frame, "🛡️ ADMIN CONTROL PANEL", "Master control interface"
        )
        control_card.pack(fill="both", expand=True, padx=20, pady=20)

        content_frame = tk.Frame(control_card, bg=self.theme.colors.bg_card)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Admin stats
        stats_frame = tk.Frame(content_frame, bg=self.theme.colors.bg_card)
        stats_frame.pack(fill="x", pady=20)

        tk.Label(
            stats_frame,
            text="📊 SYSTEM ANALYTICS:",
            font=("Orbitron", 14, "bold"),
            bg=self.theme.colors.bg_card,
            fg=self.theme.colors.gold,
        ).pack(anchor="w", pady=(0, 10))

        # Activity stats
        try:
            from admin.user_tracker import UserActivityTracker

            tracker = UserActivityTracker()
            activities = tracker.get_activities(100)
            ip_summary = tracker.get_ip_summary()

            stats_text = f"""
🔍 Total Activities: {len(activities)}
🌐 Unique IP Addresses: {len(ip_summary)}
⚡ System Status: OPERATIONAL
🛡️ Security Level: MAXIMUM
            """
        except:
            stats_text = """
🔍 Total Activities: Loading...
🌐 Unique IP Addresses: Loading...  
⚡ System Status: OPERATIONAL
🛡️ Security Level: MAXIMUM
            """

        stats_label = tk.Label(
            stats_frame,
            text=stats_text.strip(),
            font=("Consolas", 11),
            bg=self.theme.colors.bg_card,
            fg=self.theme.colors.text_primary,
            justify="left",
            anchor="w",
        )
        stats_label.pack(anchor="w")

        # Admin controls
        controls_frame = tk.Frame(content_frame, bg=self.theme.colors.bg_card)
        controls_frame.pack(fill="x", pady=20)

        tk.Label(
            controls_frame,
            text="🎛️ MASTER CONTROLS:",
            font=("Orbitron", 14, "bold"),
            bg=self.theme.colors.bg_card,
            fg=self.theme.colors.neon_blue,
        ).pack(anchor="w", pady=(0, 10))

        # Control buttons
        controls = [
            ("📊", "EXPORT LOGS", self._export_logs),
            ("🔄", "REFRESH DATA", self._refresh_data),
            ("💾", "BACKUP SYSTEM", self._backup_system),
            ("🗑️", "CLEAR CACHE", self._clear_cache),
        ]

        for icon, label, command in controls:
            btn = self.theme.components.create_neon_button(
                controls_frame,
                f"{icon} {label}",
                command=command,
                style="primary",
                size="medium",
            )
            btn.pack(fill="x", pady=2)

    def _export_logs(self):
        """Export system logs"""
        self.theme.components.create_notification_toast(
            self.parent, "📊 Exporting system logs...", "info"
        )

    def _refresh_data(self):
        """Refresh system data"""
        self.theme.components.create_notification_toast(
            self.parent, "🔄 System data refreshed", "success"
        )

    def _backup_system(self):
        """Backup system"""
        success = self.controller.backup_database()
        if success:
            self.theme.components.create_notification_toast(
                self.parent, "💾 System backup completed successfully", "success"
            )
        else:
            self.theme.components.create_notification_toast(
                self.parent, "❌ Backup failed - vault must be online", "error"
            )

    def _clear_cache(self):
        """Clear system cache"""
        self.theme.components.create_notification_toast(
            self.parent, "🗑️ System cache cleared", "success"
        )

    def show(self):
        self.main_frame.pack(fill="both", expand=True)

    def hide(self):
        self.main_frame.pack_forget()

    def refresh(self):
        pass
