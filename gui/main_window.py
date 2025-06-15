"""
gui/main_window.py
DENSO888 Gaming Edition Main Window - COMPLETE FIXED VERSION
เฮียตอมจัดหั้ย!!! - ไฟล์สมบูรณ์แบบ 🎮🚀
"""

import tkinter as tk
from tkinter import messagebox
import threading
import traceback
from typing import Dict, Any, Optional

# Core imports
from models.app_config import AppConfig
from models.user_preferences import UserPreferences
from controllers.app_controller import AppController

# UI imports
from gui.themes.gaming_theme import gaming_theme


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
                "id": "logs",
                "title": "System Logs",
                "description": "Activity Monitor",
                "icon": "📝",
                "color": gaming_theme.colors.gold,
                "badge": None,
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

        # *** Test Panel for Notifications ***
        test_panel = tk.Frame(self.content_area, bg="#FF0066", height=60)
        test_panel.pack(fill="x", pady=(0, 10))
        test_panel.pack_propagate(False)

        # Test buttons
        test_label = tk.Label(
            test_panel,
            text="🧪 NOTIFICATION TEST PANEL",
            font=("Orbitron", 12, "bold"),
            bg="#FF0066",
            fg="white",
        )
        test_label.pack(side="left", padx=10, pady=15)

        # Test Success Notification
        success_btn = tk.Button(
            test_panel,
            text="✅ Test Success",
            font=("Arial", 10, "bold"),
            bg="#00FF88",
            fg="black",
            relief="flat",
            command=self._test_success_notification,
            cursor="hand2",
        )
        success_btn.pack(side="left", padx=5, pady=15)

        # Test Error Notification
        error_btn = tk.Button(
            test_panel,
            text="❌ Test Error",
            font=("Arial", 10, "bold"),
            bg="#FF4466",
            fg="white",
            relief="flat",
            command=self._test_error_notification,
            cursor="hand2",
        )
        error_btn.pack(side="left", padx=5, pady=15)

        # Test Info Notification
        info_btn = tk.Button(
            test_panel,
            text="ℹ️ Test Info",
            font=("Arial", 10, "bold"),
            bg="#00FFFF",
            fg="black",
            relief="flat",
            command=self._test_info_notification,
            cursor="hand2",
        )
        info_btn.pack(side="left", padx=5, pady=15)

    def _test_success_notification(self):
        """Test success notification"""
        print("🧪 Testing SUCCESS notification...")
        try:
            result = gaming_theme.components.create_notification_toast(
                self.root,
                "🎯 Success notification test! เฮียตอมเทสต์สำเร็จ!",
                "success",
                5000,
            )
            print(f"✅ Success notification created: {result}")
        except Exception as e:
            print(f"❌ Error in success notification: {e}")
            import traceback

            traceback.print_exc()

    def _test_error_notification(self):
        """Test error notification"""
        print("🧪 Testing ERROR notification...")
        try:
            result = gaming_theme.components.create_notification_toast(
                self.root,
                "💥 Error notification test! Something went wrong!",
                "error",
                5000,
            )
            print(f"✅ Error notification created: {result}")
        except Exception as e:
            print(f"❌ Error in error notification: {e}")
            import traceback

            traceback.print_exc()

    def _test_info_notification(self):
        """Test info notification"""
        print("🧪 Testing INFO notification...")
        try:
            result = gaming_theme.components.create_notification_toast(
                self.root,
                "📘 Info notification test! This is an information message.",
                "info",
                5000,
            )
            print(f"✅ Info notification created: {result}")
        except Exception as e:
            print(f"❌ Error in info notification: {e}")
            import traceback

            traceback.print_exc()

    def _create_gaming_status_bar(self):
        """Create gaming-style status bar"""
        self.status_bar = tk.Frame(
            self.root,
            bg=gaming_theme.colors.bg_secondary,
            height=35,
            relief="flat",
            bd=0,
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
            # Create simple gaming pages
            self.pages = {}

            # Dashboard page
            self.pages["dashboard"] = self._create_dashboard_page()
            self.pages["import"] = self._create_import_page()
            self.pages["database"] = self._create_database_page()
            self.pages["mock"] = self._create_mock_page()
            self.pages["logs"] = self._create_logs_page()

            print("✅ All gaming pages initialized successfully")

        except Exception as e:
            print(f"❌ Error creating pages: {e}")
            print(f"🔍 Stack trace: {traceback.format_exc()}")

    def _create_dashboard_page(self):
        """Create dashboard page"""

        class DashboardPage:
            def __init__(self, parent):
                self.parent = parent
                self.main_frame = gaming_theme.components.create_gaming_card(
                    parent.content_area,
                    "🎯 Command Center",
                    "Your mission control interface",
                )
                self._setup_content()

            def _setup_content(self):
                content_frame = tk.Frame(
                    self.main_frame, bg=gaming_theme.colors.bg_card
                )
                content_frame.pack(fill="both", expand=True, padx=20, pady=20)

                # Icon
                icon_label = tk.Label(
                    content_frame,
                    text="🎯",
                    font=("Segoe UI", 48),
                    bg=gaming_theme.colors.bg_card,
                    fg=gaming_theme.colors.neon_orange,
                )
                icon_label.pack(pady=20)

                # Welcome message
                message_label = tk.Label(
                    content_frame,
                    text="🎮 Welcome to DENSO888 Gaming Edition!\n\n• Database Status: Ready for connection\n• System: All components loaded\n• Mission: Transform your Excel data!",
                    font=("Orbitron", 12),
                    bg=gaming_theme.colors.bg_card,
                    fg=gaming_theme.colors.text_primary,
                    justify="center",
                )
                message_label.pack()

                # Action button
                action_btn = gaming_theme.components.create_neon_button(
                    content_frame,
                    "🚀 View System Status",
                    command=lambda: self._show_action_message(),
                    style="primary",
                    size="large",
                )
                action_btn.pack(pady=20)

            def _show_action_message(self):
                gaming_theme.components.create_notification_toast(
                    self.parent.root,
                    "🎯 Dashboard ready! Connect database to unlock full features.",
                    "info",
                    3000,
                )

            def show(self):
                self.main_frame.pack(fill="both", expand=True)

            def hide(self):
                self.main_frame.pack_forget()

            def refresh(self):
                pass

        return DashboardPage(self)

    def _create_import_page(self):
        """Create import page"""

        class ImportPage:
            def __init__(self, parent):
                self.parent = parent
                self.main_frame = gaming_theme.components.create_gaming_card(
                    parent.content_area,
                    "📊 Data Injection",
                    "Transform Excel into database power",
                )
                self._setup_content()

            def _setup_content(self):
                content_frame = tk.Frame(
                    self.main_frame, bg=gaming_theme.colors.bg_card
                )
                content_frame.pack(fill="both", expand=True, padx=20, pady=20)

                icon_label = tk.Label(
                    content_frame,
                    text="📊",
                    font=("Segoe UI", 48),
                    bg=gaming_theme.colors.bg_card,
                    fg=gaming_theme.colors.neon_orange,
                )
                icon_label.pack(pady=20)

                message_label = tk.Label(
                    content_frame,
                    text="📊 Excel Data Injection Portal\n\n• Select your Excel files\n• Configure import settings\n• Launch data transformation!",
                    font=("Orbitron", 12),
                    bg=gaming_theme.colors.bg_card,
                    fg=gaming_theme.colors.text_primary,
                    justify="center",
                )
                message_label.pack()

                action_btn = gaming_theme.components.create_neon_button(
                    content_frame,
                    "📁 Select Excel File",
                    command=lambda: self._show_action_message(),
                    style="primary",
                    size="large",
                )
                action_btn.pack(pady=20)

            def _show_action_message(self):
                gaming_theme.components.create_notification_toast(
                    self.parent.root,
                    "📊 Import feature ready! Connect database first to begin data injection.",
                    "info",
                    3000,
                )

            def show(self):
                self.main_frame.pack(fill="both", expand=True)

            def hide(self):
                self.main_frame.pack_forget()

            def refresh(self):
                pass

        return ImportPage(self)

    def _create_database_page(self):
        """Create database page"""

        class DatabasePage:
            def __init__(self, parent):
                self.parent = parent
                self.main_frame = gaming_theme.components.create_gaming_card(
                    parent.content_area, "🗄️ Data Vault", "Configure your data fortress"
                )
                self._setup_content()

            def _setup_content(self):
                content_frame = tk.Frame(
                    self.main_frame, bg=gaming_theme.colors.bg_card
                )
                content_frame.pack(fill="both", expand=True, padx=20, pady=20)

                icon_label = tk.Label(
                    content_frame,
                    text="🗄️",
                    font=("Segoe UI", 48),
                    bg=gaming_theme.colors.bg_card,
                    fg=gaming_theme.colors.neon_orange,
                )
                icon_label.pack(pady=20)

                message_label = tk.Label(
                    content_frame,
                    text="🗄️ Database Vault Control\n\n• Configure SQLite or SQL Server\n• Test connections\n• Manage your data fortress!",
                    font=("Orbitron", 12),
                    bg=gaming_theme.colors.bg_card,
                    fg=gaming_theme.colors.text_primary,
                    justify="center",
                )
                message_label.pack()

                action_btn = gaming_theme.components.create_neon_button(
                    content_frame,
                    "🔗 Configure Database",
                    command=lambda: self._show_action_message(),
                    style="primary",
                    size="large",
                )
                action_btn.pack(pady=20)

            def _show_action_message(self):
                gaming_theme.components.create_notification_toast(
                    self.parent.root,
                    "🗄️ Database configuration ready! Choose SQLite for quick start.",
                    "info",
                    3000,
                )

            def show(self):
                self.main_frame.pack(fill="both", expand=True)

            def hide(self):
                self.main_frame.pack_forget()

            def refresh(self):
                pass

        return DatabasePage(self)

    def _create_mock_page(self):
        """Create mock data page"""

        class MockPage:
            def __init__(self, parent):
                self.parent = parent
                self.main_frame = gaming_theme.components.create_gaming_card(
                    parent.content_area, "🎲 Data Forge", "Generate unlimited test data"
                )
                self._setup_content()

            def _setup_content(self):
                content_frame = tk.Frame(
                    self.main_frame, bg=gaming_theme.colors.bg_card
                )
                content_frame.pack(fill="both", expand=True, padx=20, pady=20)

                icon_label = tk.Label(
                    content_frame,
                    text="🎲",
                    font=("Segoe UI", 48),
                    bg=gaming_theme.colors.bg_card,
                    fg=gaming_theme.colors.neon_orange,
                )
                icon_label.pack(pady=20)

                message_label = tk.Label(
                    content_frame,
                    text="🎲 Data Forge Laboratory\n\n• Generate employee records\n• Create sales data\n• Build inventory systems!",
                    font=("Orbitron", 12),
                    bg=gaming_theme.colors.bg_card,
                    fg=gaming_theme.colors.text_primary,
                    justify="center",
                )
                message_label.pack()

                action_btn = gaming_theme.components.create_neon_button(
                    content_frame,
                    "🎲 Generate Data",
                    command=lambda: self._show_action_message(),
                    style="primary",
                    size="large",
                )
                action_btn.pack(pady=20)

            def _show_action_message(self):
                gaming_theme.components.create_notification_toast(
                    self.parent.root,
                    "🎲 Mock data forge ready! Connect database to start generating data.",
                    "info",
                    3000,
                )

            def show(self):
                self.main_frame.pack(fill="both", expand=True)

            def hide(self):
                self.main_frame.pack_forget()

            def refresh(self):
                pass

        return MockPage(self)

    def _create_logs_page(self):
        """Create logs page"""

        class LogsPage:
            def __init__(self, parent):
                self.parent = parent
                self.main_frame = gaming_theme.components.create_gaming_card(
                    parent.content_area,
                    "📝 System Logs",
                    "Monitor all system activities",
                )
                self._setup_content()

            def _setup_content(self):
                content_frame = tk.Frame(
                    self.main_frame, bg=gaming_theme.colors.bg_card
                )
                content_frame.pack(fill="both", expand=True, padx=20, pady=20)

                icon_label = tk.Label(
                    content_frame,
                    text="📝",
                    font=("Segoe UI", 48),
                    bg=gaming_theme.colors.bg_card,
                    fg=gaming_theme.colors.neon_orange,
                )
                icon_label.pack(pady=20)

                message_label = tk.Label(
                    content_frame,
                    text="📝 System Logs Monitor\n\n• Real-time activity tracking\n• Error monitoring\n• Performance metrics!",
                    font=("Orbitron", 12),
                    bg=gaming_theme.colors.bg_card,
                    fg=gaming_theme.colors.text_primary,
                    justify="center",
                )
                message_label.pack()

                action_btn = gaming_theme.components.create_neon_button(
                    content_frame,
                    "📝 View Logs",
                    command=lambda: self._show_action_message(),
                    style="primary",
                    size="large",
                )
                action_btn.pack(pady=20)

            def _show_action_message(self):
                gaming_theme.components.create_notification_toast(
                    self.parent.root,
                    "📝 System logs active! Real-time monitoring enabled.",
                    "info",
                    3000,
                )

            def show(self):
                self.main_frame.pack(fill="both", expand=True)

            def hide(self):
                self.main_frame.pack_forget()

            def refresh(self):
                pass

        return LogsPage(self)

    def _setup_event_handlers(self):
        """Setup gaming event handlers - FINAL FIX"""

        def prevent_accidental_close():
            """Prevent accidental window close"""
            from tkinter import messagebox

            result = messagebox.askyesnocancel(
                "🎮 DENSO888 Gaming Edition",
                "ต้องการทำอะไร?\n\n"
                + "🔴 YES = ปิดแอป\n"
                + "🟢 NO = ใช้งานต่อ\n"
                + "🟡 CANCEL = ย่อหน้าต่าง",
                icon="question",
            )

            if result is True:
                # ปิดจริง
                if self.controller:
                    self.controller.shutdown()
                self.root.quit()
                self.root.destroy()
            elif result is False:
                # ใช้งานต่อ - ไม่ทำอะไร
                self._show_gaming_notification(
                    "🎮 Welcome back! เฮียตอมกลับมาแล้ว!", "success"
                )
            else:
                # ย่อหน้าต่าง
                self.root.iconify()

        # Apply protection
        self.root.protocol("WM_DELETE_WINDOW", prevent_accidental_close)

        # Controller events with gaming enhancements
        self.controller.subscribe("db_status_changed", self._on_db_status_changed)
        self.controller.subscribe("operation_complete", self._on_operation_complete)
        self.controller.subscribe("error_occurred", self._on_error_occurred)
        self.controller.subscribe("log_message", self._on_log_message)
        self.controller.subscribe("achievement_unlocked", self._on_achievement_unlocked)
        self.controller.subscribe("progress_update", self._on_progress_update)

        # Gaming keyboard shortcuts
        self.root.bind("<Control-q>", lambda e: prevent_accidental_close())
        self.root.bind("<F5>", lambda e: self._refresh_current_page())
        self.root.bind("<F11>", lambda e: self._toggle_fullscreen())

    def _show_welcome_animation(self):
        """Show welcome animation on startup - SAFE VERSION"""

        def safe_animate():
            try:
                print("🎮 Starting welcome animation...")
                self.root.deiconify()  # Force visible
                self.root.lift()
                # Show page first (more important than notification)
                self._show_page("dashboard")

                # Then show notification (less critical)
                try:
                    gaming_theme.components.create_notification_toast(
                        self.root,
                        "🎮 DENSO888 Gaming Edition Activated! 🚀",
                        "success",
                        3000,
                    )
                except Exception as e:
                    print(f"⚠️ Notification warning (non-critical): {e}")

                print("✅ Welcome animation completed")

            except Exception as e:
                print(f"❌ Animation error: {e}")
                # Still show dashboard even if animation fails
                try:
                    self._show_page("dashboard")
                except:
                    pass

        # Schedule animation safely
        self.root.after(200, safe_animate)

        # Show default page
        self._show_page("dashboard")

    # *** CRITICAL: Missing _on_page_changed method implementation ***
    def _on_page_changed(self, page_id: str):
        """Handle page navigation with gaming effects - FIXED METHOD"""
        try:
            print(f"🎯 Switching to page: {page_id}")

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
                    "logs": "SYSTEM LOGS",
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
        else:
            self.connection_label.configure(
                text="🔴 OFFLINE", fg=gaming_theme.colors.text_error
            )

    def _on_operation_complete(self, data: Dict[str, Any]):
        """Handle operation completion with gaming celebration"""
        operation = data.get("operation", "Operation")
        success = data.get("success", False)

        if success:
            self._show_gaming_notification(
                f"🚀 {operation} completed successfully!", "success"
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
        gaming_theme.create_achievement_popup(
            self.root, title, description, achievement_type
        )

    def _on_progress_update(self, progress_data: Dict[str, Any]):
        """Handle progress updates with gaming UI"""
        progress = progress_data.get("progress", 0)
        status = progress_data.get("status", "Processing...")

        # Update status bar with progress
        self._update_status(f"⚡ {status} ({progress:.0f}%)")

    def _show_gaming_notification(self, message: str, notification_type: str = "info"):
        """Show gaming-style notification - THREAD-SAFE VERSION"""

        def safe_notification():
            try:
                # Only create notification if window still exists
                if self.root.winfo_exists():
                    gaming_theme.components.create_notification_toast(
                        self.root, message, notification_type, 3000
                    )
            except Exception as e:
                print(f"⚠️ Notification warning (non-critical): {e}")

        # Schedule in main thread
        try:
            self.root.after_idle(safe_notification)
        except:
            # If even scheduling fails, just ignore notification
            print(f"⚠️ Could not schedule notification: {message}")

    def _update_status(self, message: str):
        """Update status bar with gaming style"""
        self.status_label.configure(text=message)

    def _show_page(self, page_id: str):
        """Programmatically show a page"""
        self._on_page_changed(page_id)

    def _refresh_current_page(self):
        """Refresh current page with visual feedback"""
        if self.current_page and self.current_page in self.pages:
            page = self.pages[self.current_page]
            if hasattr(page, "refresh"):
                self._show_gaming_notification("🔄 Refreshing data...", "info")
                threading.Thread(target=page.refresh, daemon=True).start()

    def _toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        try:
            current_state = self.root.attributes("-fullscreen")
            self.root.attributes("-fullscreen", not current_state)

            if not current_state:
                self._show_gaming_notification("🖥️ Fullscreen mode activated", "info")
            else:
                self._show_gaming_notification("🖥️ Windowed mode activated", "info")
        except Exception:
            self._show_gaming_notification("🖥️ Fullscreen not supported", "warning")

    def _on_closing(self):
        """Handle application closing with gaming farewell - FIXED VERSION"""
        try:
            result = messagebox.askyesno(
                "Exit Gaming Edition",
                "🎮 Exit DENSO888 Gaming Edition?\n\nAll your progress will be saved!",
            )

            if result:
                print("👋 User confirmed exit")

                # Show farewell message (แต่ไม่รอ)
                try:
                    gaming_theme.components.create_notification_toast(
                        self.root,
                        "👋 Thanks for playing! See you next time!",
                        "info",
                        1000,
                    )
                except:
                    pass  # ไม่สำคัญถ้า notification ไม่แสดง

                # Cleanup
                if self.controller:
                    self.controller.shutdown()

                # *** CRITICAL: ปิดแอปทันที ***
                self._final_shutdown()
            else:
                print("🎮 User cancelled exit")

        except Exception as e:
            print(f"Error during shutdown: {e}")
            # *** Force quit ถ้ามีปัญหา ***
            self._final_shutdown()

    def _final_shutdown(self):
        """Final shutdown procedure - SAFE VERSION"""
        print("🔄 Executing final shutdown...")
        try:
            # Try graceful shutdown first
            if hasattr(self, "root") and self.root:
                self.root.quit()
                self.root.destroy()
        except Exception as e:
            print(f"⚠️ Graceful shutdown failed: {e}")
            # Force exit
            import sys

            sys.exit(0)

    def run(self):
        """Start the gaming edition application - FORCE VISIBLE VERSION"""
        try:
            print("🎮 Starting DENSO888 Gaming Edition...")

            def auto_restore():
                if self.root.state() == "iconic":
                    self.root.deiconify()
                    print("🔄 Auto-restored window")
                self.root.after(500, auto_restore)

            # *** CRITICAL: Force window to stay visible ***
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            self.root.attributes("-topmost", True)

            # Force update
            self.root.update_idletasks()
            self.root.update()

            # Remove topmost after showing
            self.root.after(2000, lambda: self.root.attributes("-topmost", False))

            # *** ADD: Prevent auto-minimize ***
            def keep_visible():
                if self.root.state() == "iconic":  # If minimized
                    self.root.deiconify()  # Show again
                    print("🔄 Window was minimized, restoring...")
                self.root.after(1000, keep_visible)  # Check every second

            self.root.after(1000, keep_visible)

            print("🎯 Window forced visible, starting mainloop...")
            self.root.mainloop()

        except Exception as e:
            print(f"❌ Error: {e}")
            traceback.print_exc()
