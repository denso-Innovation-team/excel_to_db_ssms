"""
gui/windows/modern_main_window.py
Modern DENSO888 Main Window with Enhanced UI/UX
"""

import tkinter as tk
from tkinter import messagebox, filedialog
from pathlib import Path

# Modern components imports
from ..themes.theme_manager import ModernThemeManager
from ..components.modern_dashboard import ModernDashboard
from ..components.modern_widgets import (
    AnimatedButton,
    FloatingNotification,
    ModernCard,
    ModernToggleSwitch,
)
from ..components.splash_screen import DENSOSplashScreen


class ModernDENSO888MainWindow:
    """Modern main window with enhanced UI/UX and DENSO branding"""

    def __init__(self, config=None):
        self.config = config or self._get_default_config()

        # Initialize managers
        self.theme_manager = ModernThemeManager()
        self.current_theme = "denso_corporate"

        # Application state
        self.is_processing = False
        self.current_progress = 0.0
        self.notifications_queue = []

        # UI Components
        self.root = None
        self.dashboard = None
        self.sidebar = None
        self.main_content = None
        self.status_bar = None

        # Show splash screen first
        self._show_splash_screen()

    def _get_default_config(self):
        """Get default configuration"""

        class DefaultConfig:
            app_name = "DENSO888"
            version = "2.0.0 - Modern Edition"
            author = "Thammaphon Chittasuwanna (SDM) | Innovation"
            nickname = "เฮียตอมจัดหั้ย!!!"

        return DefaultConfig()

    def _show_splash_screen(self):
        """Show splash screen before main window"""
        splash = DENSOSplashScreen(callback=self._initialize_main_window)

    def _initialize_main_window(self):
        """Initialize main application window after splash"""
        self._create_main_window()
        self._setup_themes()
        self._create_menu_system()
        self._create_ui_layout()
        self._setup_shortcuts()
        self._show_welcome_sequence()

    def _create_main_window(self):
        """Create and configure main window"""
        self.root = tk.Tk()
        self.root.title(f"🏭 {self.config.app_name} {self.config.version}")

        # Window configuration
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        self.root.state("zoomed")  # Start maximized on Windows

        # Center window if not maximized
        self._center_window()

        # Configure window icon (would load actual DENSO icon)
        try:
            # self.root.iconbitmap("assets/images/denso_icon.ico")
            pass
        except:
            pass

        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

        # Apply theme
        self.theme_manager.apply_theme(self.current_theme, self.root)

    def _center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _setup_themes(self):
        """Setup theme system"""
        # Apply initial theme
        self.theme_manager.apply_theme(self.current_theme, self.root)

        # Configure window background
        palette = self.theme_manager.get_current_palette()
        self.root.configure(bg=palette.background)

    def _create_menu_system(self):
        """Create modern menu system"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📁 File", menu=file_menu)
        file_menu.add_command(label="🔄 New Project", command=self._new_project)
        file_menu.add_command(label="📂 Open Project", command=self._open_project)
        file_menu.add_separator()
        file_menu.add_command(label="📊 Import Excel", command=self._import_excel)
        file_menu.add_command(label="💾 Export Data", command=self._export_data)
        file_menu.add_separator()
        file_menu.add_command(label="🚪 Exit", command=self._on_closing)

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="🛠️ Tools", menu=tools_menu)
        tools_menu.add_command(
            label="🎲 Mock Data Generator", command=self._open_mock_generator
        )
        tools_menu.add_command(
            label="🔐 Database Manager", command=self._open_database_manager
        )
        tools_menu.add_command(
            label="📈 Analytics Dashboard", command=self._open_analytics
        )
        tools_menu.add_separator()
        tools_menu.add_command(label="⚙️ Settings", command=self._open_settings)

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="👁️ View", menu=view_menu)

        # Theme submenu
        theme_submenu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="🎨 Themes", menu=theme_submenu)

        themes = self.theme_manager.get_available_themes()
        for theme_id, theme_name in themes.items():
            theme_submenu.add_command(
                label=theme_name, command=lambda t=theme_id: self._change_theme(t)
            )

        view_menu.add_separator()
        view_menu.add_command(label="🖥️ Full Screen", command=self._toggle_fullscreen)
        view_menu.add_command(label="🔍 Zoom In", command=self._zoom_in)
        view_menu.add_command(label="🔍 Zoom Out", command=self._zoom_out)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="❓ Help", menu=help_menu)
        help_menu.add_command(label="📖 User Guide", command=self._show_user_guide)
        help_menu.add_command(
            label="🔧 Troubleshooting", command=self._show_troubleshooting
        )
        help_menu.add_separator()
        help_menu.add_command(label="ℹ️ About", command=self._show_about)

    def _create_ui_layout(self):
        """Create main UI layout with modern design"""
        # Main container
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill="both", expand=True)

        # Create sidebar navigation
        self._create_sidebar()

        # Create main content area
        self._create_main_content()

        # Create status bar
        self._create_status_bar()

        # Initialize with dashboard view
        self._show_dashboard()

    def _create_sidebar(self):
        """Create modern sidebar navigation"""
        palette = self.theme_manager.get_current_palette()

        # Sidebar frame
        self.sidebar = tk.Frame(
            self.main_container, bg=palette.surface, width=280, relief="flat"
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # DENSO Logo section
        self._create_sidebar_header()

        # Navigation menu
        self._create_navigation_menu()

        # Quick actions
        self._create_quick_actions()

        # Creator info section
        self._create_sidebar_footer()

    def _create_sidebar_header(self):
        """Create sidebar header with DENSO branding"""
        palette = self.theme_manager.get_current_palette()

        header_frame = tk.Frame(self.sidebar, bg=palette.surface)
        header_frame.pack(fill="x", padx=20, pady=20)

        # Logo area (placeholder for actual DENSO logo)
        logo_frame = tk.Frame(header_frame, bg=palette.primary, width=60, height=60)
        logo_frame.pack_propagate(False)
        logo_frame.pack()

        logo_label = tk.Label(
            logo_frame, text="🏭", font=("Segoe UI", 24), bg=palette.primary, fg="white"
        )
        logo_label.pack(expand=True)

        # App title
        title_label = tk.Label(
            header_frame,
            text="DENSO888",
            font=("Segoe UI", 18, "bold"),
            fg=palette.text_primary,
            bg=palette.surface,
        )
        title_label.pack(pady=(10, 0))

        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Modern Edition",
            font=("Segoe UI", 10),
            fg=palette.text_secondary,
            bg=palette.surface,
        )
        subtitle_label.pack()

    def _create_navigation_menu(self):
        """Create navigation menu with modern styling"""
        palette = self.theme_manager.get_current_palette()

        nav_frame = tk.Frame(self.sidebar, bg=palette.surface)
        nav_frame.pack(fill="x", padx=10, pady=20)

        # Navigation items
        nav_items = [
            ("🏠", "Dashboard", self._show_dashboard),
            ("📊", "Data Import", self._show_data_import),
            ("🎲", "Mock Generator", self._show_mock_generator),
            ("🗄️", "Database", self._show_database),
            ("📈", "Analytics", self._show_analytics),
            ("⚙️", "Settings", self._show_settings),
        ]

        self.nav_buttons = {}
        for icon, text, command in nav_items:
            btn_frame = tk.Frame(nav_frame, bg=palette.surface)
            btn_frame.pack(fill="x", pady=2)

            button = self.theme_manager.create_animated_hover_button(
                btn_frame, f"{icon}  {text}", command
            )
            button.pack(fill="x", padx=5)

            self.nav_buttons[text] = button

    def _create_quick_actions(self):
        """Create quick action buttons"""
        palette = self.theme_manager.get_current_palette()

        actions_frame = tk.LabelFrame(
            self.sidebar,
            text="⚡ Quick Actions",
            bg=palette.surface,
            fg=palette.text_primary,
            font=("Segoe UI", 11, "bold"),
        )
        actions_frame.pack(fill="x", padx=10, pady=10)

        # Quick action buttons
        actions = [
            ("📁 Browse Excel", self._quick_browse_excel),
            ("🚀 Quick Process", self._quick_process),
            ("📊 View Last Results", self._view_last_results),
        ]

        for text, command in actions:
            btn = AnimatedButton(
                actions_frame, text=text, command=command, style="outline", size="small"
            )
            btn.pack(fill="x", padx=10, pady=5)

    def _create_sidebar_footer(self):
        """Create sidebar footer with creator info"""
        palette = self.theme_manager.get_current_palette()

        footer_frame = tk.Frame(self.sidebar, bg=palette.surface)
        footer_frame.pack(side="bottom", fill="x", padx=20, pady=20)

        # Creator avatar (placeholder)
        avatar_frame = tk.Frame(footer_frame, bg=palette.primary, width=40, height=40)
        avatar_frame.pack_propagate(False)
        avatar_frame.pack()

        avatar_label = tk.Label(
            avatar_frame,
            text="TC",
            font=("Segoe UI", 12, "bold"),
            bg=palette.primary,
            fg="white",
        )
        avatar_label.pack(expand=True)

        # Creator info
        creator_label = tk.Label(
            footer_frame,
            text="Created by",
            font=("Segoe UI", 8),
            fg=palette.text_secondary,
            bg=palette.surface,
        )
        creator_label.pack(pady=(10, 0))

        name_label = tk.Label(
            footer_frame,
            text="Thammaphon C.",
            font=("Segoe UI", 10, "bold"),
            fg=palette.text_primary,
            bg=palette.surface,
        )
        name_label.pack()

        nickname_label = tk.Label(
            footer_frame,
            text=self.config.nickname,
            font=("Segoe UI", 8, "italic"),
            fg=palette.primary,
            bg=palette.surface,
        )
        nickname_label.pack()

    def _create_main_content(self):
        """Create main content area"""
        palette = self.theme_manager.get_current_palette()

        self.main_content = tk.Frame(self.main_container, bg=palette.background)
        self.main_content.pack(side="right", fill="both", expand=True)

    def _create_status_bar(self):
        """Create modern status bar"""
        palette = self.theme_manager.get_current_palette()

        self.status_bar = tk.Frame(
            self.root, bg=palette.surface, height=30, relief="flat", borderwidth=1
        )
        self.status_bar.pack(side="bottom", fill="x")
        self.status_bar.pack_propagate(False)

        # Status elements
        status_content = tk.Frame(self.status_bar, bg=palette.surface)
        status_content.pack(fill="both", expand=True, padx=10, pady=5)

        # Left side - Status
        self.status_label = tk.Label(
            status_content,
            text="🟢 Ready",
            font=("Segoe UI", 9),
            fg=palette.text_primary,
            bg=palette.surface,
        )
        self.status_label.pack(side="left")

        # Progress info
        self.progress_label = tk.Label(
            status_content,
            text="",
            font=("Segoe UI", 9),
            fg=palette.text_secondary,
            bg=palette.surface,
        )
        self.progress_label.pack(side="left", padx=(20, 0))

        # Right side - System info
        self.system_label = tk.Label(
            status_content,
            text=f"v{self.config.version.split()[0]} | Ready",
            font=("Segoe UI", 9),
            fg=palette.text_secondary,
            bg=palette.surface,
        )
        self.system_label.pack(side="right")

    def _setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        shortcuts = {
            "<Control-n>": self._new_project,
            "<Control-o>": self._open_project,
            "<Control-i>": self._import_excel,
            "<Control-s>": self._save_project,
            "<Control-q>": self._on_closing,
            "<F11>": self._toggle_fullscreen,
            "<Control-plus>": self._zoom_in,
            "<Control-minus>": self._zoom_out,
            "<Control-1>": self._show_dashboard,
            "<Control-2>": self._show_data_import,
            "<Control-3>": self._show_mock_generator,
        }

        for key, command in shortcuts.items():
            self.root.bind(key, lambda e, cmd=command: cmd())

    # Navigation Methods
    def _show_dashboard(self):
        """Show dashboard view"""
        self._clear_main_content()
        self._highlight_nav_button("Dashboard")

        # Create dashboard
        self.dashboard = ModernDashboard(
            self.main_content, self.theme_manager, self.config
        )

        self._update_status("Dashboard loaded")

    def _show_data_import(self):
        """Show data import interface"""
        self._clear_main_content()
        self._highlight_nav_button("Data Import")

        # Create data import interface
        self._create_data_import_interface()
        self._update_status("Data Import ready")

    def _show_mock_generator(self):
        """Show mock data generator"""
        self._clear_main_content()
        self._highlight_nav_button("Mock Generator")

        # Create mock generator interface
        self._create_mock_generator_interface()
        self._update_status("Mock Generator ready")

    def _show_database(self):
        """Show database management"""
        self._clear_main_content()
        self._highlight_nav_button("Database")

        # Create database interface
        self._create_database_interface()
        self._update_status("Database Manager ready")

    def _show_analytics(self):
        """Show analytics dashboard"""
        self._clear_main_content()
        self._highlight_nav_button("Analytics")

        # Create analytics interface
        self._create_analytics_interface()
        self._update_status("Analytics ready")

    def _show_settings(self):
        """Show settings panel"""
        self._clear_main_content()
        self._highlight_nav_button("Settings")

        # Create settings interface
        self._create_settings_interface()
        self._update_status("Settings panel loaded")

    def _clear_main_content(self):
        """Clear main content area"""
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def _highlight_nav_button(self, active_button):
        """Highlight active navigation button"""
        palette = self.theme_manager.get_current_palette()

        for name, button in self.nav_buttons.items():
            if name == active_button:
                # Highlight active button
                button.configure(bg=palette.primary, fg="white")
            else:
                # Reset other buttons
                button.configure(bg=palette.surface, fg=palette.text_primary)

    # Interface Creation Methods
    def _create_data_import_interface(self):
        """Create modern data import interface"""
        palette = self.theme_manager.get_current_palette()

        # Header
        header_frame = tk.Frame(self.main_content, bg=palette.background)
        header_frame.pack(fill="x", padx=30, pady=20)

        title_label = tk.Label(
            header_frame,
            text="📊 Data Import Wizard",
            font=("Segoe UI", 24, "bold"),
            fg=palette.text_primary,
            bg=palette.background,
        )
        title_label.pack(anchor="w")

        subtitle_label = tk.Label(
            header_frame,
            text="Import Excel files with AI-powered data detection",
            font=("Segoe UI", 12),
            fg=palette.text_secondary,
            bg=palette.background,
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))

        # Content area with cards
        content_frame = tk.Frame(self.main_content, bg=palette.background)
        content_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # File selection card
        file_card = ModernCard(
            content_frame,
            title="📁 Select Excel File",
            content="Choose your Excel file to import",
            accent_color=palette.primary,
        )
        file_card.pack(fill="x", pady=10)

        # Configuration card
        config_card = ModernCard(
            content_frame,
            title="⚙️ Import Configuration",
            content="Configure import settings and data mapping",
            accent_color=palette.accent,
        )
        config_card.pack(fill="x", pady=10)

        # Preview card
        preview_card = ModernCard(
            content_frame,
            title="👁️ Data Preview",
            content="Preview your data before importing",
            accent_color=palette.success,
        )
        preview_card.pack(fill="x", pady=10)

    def _create_mock_generator_interface(self):
        """Create mock data generator interface"""
        palette = self.theme_manager.get_current_palette()

        # Header
        header_frame = tk.Frame(self.main_content, bg=palette.background)
        header_frame.pack(fill="x", padx=30, pady=20)

        title_label = tk.Label(
            header_frame,
            text="🎲 Mock Data Generator",
            font=("Segoe UI", 24, "bold"),
            fg=palette.text_primary,
            bg=palette.background,
        )
        title_label.pack(anchor="w")

        subtitle_label = tk.Label(
            header_frame,
            text="Generate realistic test data for development and testing",
            font=("Segoe UI", 12),
            fg=palette.text_secondary,
            bg=palette.background,
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))

        # Content with template selection
        content_frame = tk.Frame(self.main_content, bg=palette.background)
        content_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # Template grid
        templates_frame = tk.Frame(content_frame, bg=palette.background)
        templates_frame.pack(fill="both", expand=True)

        templates = [
            ("👥", "Employees", "HR records with departments and salaries"),
            ("💰", "Sales", "Transaction data with customers and products"),
            ("📦", "Inventory", "Product catalog with stock levels"),
            ("💳", "Financial", "Accounting records and transactions"),
        ]

        for i, (icon, name, desc) in enumerate(templates):
            row = i // 2
            col = i % 2

            template_card = self._create_template_card(
                templates_frame, icon, name, desc
            )
            template_card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

        # Configure grid weights
        templates_frame.grid_columnconfigure(0, weight=1)
        templates_frame.grid_columnconfigure(1, weight=1)

    def _create_template_card(self, parent, icon, name, desc):
        """Create template selection card"""
        palette = self.theme_manager.get_current_palette()

        card_frame = tk.Frame(
            parent,
            bg=palette.surface,
            relief="flat",
            borderwidth=1,
            highlightbackground=palette.border,
            highlightthickness=1,
        )

        # Card content
        content = tk.Frame(card_frame, bg=palette.surface)
        content.pack(fill="both", expand=True, padx=25, pady=25)

        # Icon
        icon_label = tk.Label(
            content,
            text=icon,
            font=("Segoe UI", 36),
            bg=palette.surface,
            fg=palette.primary,
        )
        icon_label.pack(pady=(0, 15))

        # Title
        title_label = tk.Label(
            content,
            text=name,
            font=("Segoe UI", 16, "bold"),
            fg=palette.text_primary,
            bg=palette.surface,
        )
        title_label.pack(pady=(0, 10))

        # Description
        desc_label = tk.Label(
            content,
            text=desc,
            font=("Segoe UI", 10),
            fg=palette.text_secondary,
            bg=palette.surface,
            wraplength=200,
            justify="center",
        )
        desc_label.pack(pady=(0, 20))

        # Generate button
        generate_btn = AnimatedButton(
            content,
            text="Generate",
            command=lambda: self._generate_mock_data(name.lower()),
            style="primary",
            size="medium",
        )
        generate_btn.pack()

        # Add hover effects
        def on_enter(e):
            card_frame.configure(highlightbackground=palette.primary)

        def on_leave(e):
            card_frame.configure(highlightbackground=palette.border)

        widgets = [card_frame] + self._get_all_children(card_frame)
        for widget in widgets:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

        return card_frame

    def _create_database_interface(self):
        """Create database management interface"""
        palette = self.theme_manager.get_current_palette()

        # Header
        header_frame = tk.Frame(self.main_content, bg=palette.background)
        header_frame.pack(fill="x", padx=30, pady=20)

        title_label = tk.Label(
            header_frame,
            text="🗄️ Database Manager",
            font=("Segoe UI", 24, "bold"),
            fg=palette.text_primary,
            bg=palette.background,
        )
        title_label.pack(anchor="w")

        # Connection status
        status_frame = tk.Frame(header_frame, bg=palette.background)
        status_frame.pack(anchor="w", pady=(10, 0))

        self.db_status_label = tk.Label(
            status_frame,
            text="🟢 Connected to SQLite",
            font=("Segoe UI", 12),
            fg=palette.success,
            bg=palette.background,
        )
        self.db_status_label.pack(side="left")

        # Connection toggle
        self.db_toggle = ModernToggleSwitch(
            status_frame, initial_state=True, on_change=self._toggle_database_connection
        )
        self.db_toggle.pack(side="left", padx=(20, 0))

        # Database options
        options_frame = tk.Frame(self.main_content, bg=palette.background)
        options_frame.pack(fill="x", padx=30, pady=20)

        # SQLite option
        sqlite_card = ModernCard(
            options_frame,
            title="📁 SQLite Database",
            content="Local database for development and testing",
            accent_color="#4CAF50",
        )
        sqlite_card.pack(fill="x", pady=10)
        sqlite_card.add_button("Configure", self._configure_sqlite)

        # SQL Server option
        sqlserver_card = ModernCard(
            options_frame,
            title="🏢 SQL Server",
            content="Enterprise database for production use",
            accent_color="#2196F3",
        )
        sqlserver_card.pack(fill="x", pady=10)
        sqlserver_card.add_button("Configure", self._configure_sqlserver)

    def _create_analytics_interface(self):
        """Create analytics dashboard interface"""
        palette = self.theme_manager.get_current_palette()

        # Header
        header_frame = tk.Frame(self.main_content, bg=palette.background)
        header_frame.pack(fill="x", padx=30, pady=20)

        title_label = tk.Label(
            header_frame,
            text="📈 Analytics Dashboard",
            font=("Segoe UI", 24, "bold"),
            fg=palette.text_primary,
            bg=palette.background,
        )
        title_label.pack(anchor="w")

        # Metrics grid
        metrics_frame = tk.Frame(self.main_content, bg=palette.background)
        metrics_frame.pack(fill="x", padx=30, pady=20)

        # Create metric cards
        metrics = [
            ("📊", "Files Processed", "1,234", "+12%"),
            ("⏱️", "Avg Process Time", "2.3s", "-15%"),
            ("✅", "Success Rate", "99.8%", "+0.2%"),
            ("💾", "Data Volume", "2.5GB", "+25%"),
        ]

        for i, (icon, label, value, change) in enumerate(metrics):
            metric_card = self._create_metric_card(
                metrics_frame, icon, label, value, change
            )
            metric_card.grid(row=0, column=i, padx=10, sticky="ew")
            metrics_frame.grid_columnconfigure(i, weight=1)

    def _create_metric_card(self, parent, icon, label, value, change):
        """Create metric display card"""
        palette = self.theme_manager.get_current_palette()

        card = tk.Frame(
            parent,
            bg=palette.surface,
            relief="flat",
            borderwidth=1,
            highlightbackground=palette.border,
            highlightthickness=1,
        )

        content = tk.Frame(card, bg=palette.surface)
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # Icon
        icon_label = tk.Label(
            content,
            text=icon,
            font=("Segoe UI", 20),
            fg=palette.primary,
            bg=palette.surface,
        )
        icon_label.pack()

        # Value
        value_label = tk.Label(
            content,
            text=value,
            font=("Segoe UI", 18, "bold"),
            fg=palette.text_primary,
            bg=palette.surface,
        )
        value_label.pack(pady=(5, 0))

        # Label
        label_label = tk.Label(
            content,
            text=label,
            font=("Segoe UI", 10),
            fg=palette.text_secondary,
            bg=palette.surface,
        )
        label_label.pack()

        # Change indicator
        change_color = palette.success if change.startswith("+") else palette.danger
        change_label = tk.Label(
            content,
            text=change,
            font=("Segoe UI", 9),
            fg=change_color,
            bg=palette.surface,
        )
        change_label.pack(pady=(5, 0))

        return card

    def _create_settings_interface(self):
        """Create settings interface"""
        palette = self.theme_manager.get_current_palette()

        # Header
        header_frame = tk.Frame(self.main_content, bg=palette.background)
        header_frame.pack(fill="x", padx=30, pady=20)

        title_label = tk.Label(
            header_frame,
            text="⚙️ Application Settings",
            font=("Segoe UI", 24, "bold"),
            fg=palette.text_primary,
            bg=palette.background,
        )
        title_label.pack(anchor="w")

        # Settings sections
        sections_frame = tk.Frame(self.main_content, bg=palette.background)
        sections_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # Theme settings
        theme_card = ModernCard(
            sections_frame,
            title="🎨 Appearance",
            content="Customize the application theme and colors",
            accent_color=palette.primary,
        )
        theme_card.pack(fill="x", pady=10)

        # Performance settings
        perf_card = ModernCard(
            sections_frame,
            title="⚡ Performance",
            content="Configure processing and memory settings",
            accent_color=palette.warning,
        )
        perf_card.pack(fill="x", pady=10)

        # Security settings
        security_card = ModernCard(
            sections_frame,
            title="🔐 Security",
            content="Manage authentication and data protection",
            accent_color=palette.danger,
        )
        security_card.pack(fill="x", pady=10)

    # Utility Methods
    def _get_all_children(self, widget):
        """Get all child widgets recursively"""
        children = []
        for child in widget.winfo_children():
            children.append(child)
            children.extend(self._get_all_children(child))
        return children

    def _update_status(self, message):
        """Update status bar message"""
        self.status_label.configure(text=f"🟢 {message}")

    def _show_notification(self, message, type="info"):
        """Show floating notification"""
        notification = FloatingNotification(self.root, message, type)

    def _show_welcome_sequence(self):
        """Show welcome animation sequence"""
        # Welcome message
        self._show_notification("Welcome to DENSO888 Modern Edition! 🎉", "success")

        # Creator greeting
        self.root.after(
            2000,
            lambda: self._show_notification(
                f"Created by {self.config.author} 🚀", "info"
            ),
        )

    # Event Handlers
    def _change_theme(self, theme_name):
        """Change application theme"""
        self.current_theme = theme_name
        self.theme_manager.apply_theme(theme_name, self.root)
        self._show_notification(f"Theme changed to {theme_name}", "success")

        # Refresh current view
        current_view = "Dashboard"  # Would track current view
        getattr(self, f"_show_{current_view.lower().replace(' ', '_')}")()

    def _toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        current_state = self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", not current_state)

    def _zoom_in(self):
        """Increase UI scale"""
        # Would implement UI scaling
        self._show_notification("Zoomed in", "info")

    def _zoom_out(self):
        """Decrease UI scale"""
        # Would implement UI scaling
        self._show_notification("Zoomed out", "info")

    def _on_closing(self):
        """Handle application closing"""
        if messagebox.askyesno(
            "Confirm Exit", "Are you sure you want to exit DENSO888?"
        ):
            # Stop any background processes
            if hasattr(self, "dashboard") and self.dashboard:
                self.dashboard.stop_animations()

            self.root.destroy()

    # Action Methods (placeholders for actual functionality)
    def _new_project(self):
        self._show_notification("New project created", "success")

    def _open_project(self):
        self._show_notification("Opening project...", "info")

    def _save_project(self):
        self._show_notification("Project saved", "success")

    def _import_excel(self):
        file_path = filedialog.askopenfilename(
            title="Select Excel File", filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if file_path:
            self._show_notification(f"Selected: {Path(file_path).name}", "info")

    def _export_data(self):
        self._show_notification("Exporting data...", "info")

    def _generate_mock_data(self, template):
        self._show_notification(f"Generating {template} data...", "info")

    def _configure_sqlite(self):
        self._show_notification("SQLite configuration opened", "info")

    def _configure_sqlserver(self):
        self._show_notification("SQL Server configuration opened", "info")

    def _toggle_database_connection(self, state):
        if state:
            self.db_status_label.configure(text="🟢 Connected", fg="#28A745")
        else:
            self.db_status_label.configure(text="🔴 Disconnected", fg="#DC3545")

    def _quick_browse_excel(self):
        self._import_excel()

    def _quick_process(self):
        self._show_notification("Quick processing started", "info")

    def _view_last_results(self):
        self._show_notification("Loading last results...", "info")

    def _open_mock_generator(self):
        self._show_mock_generator()

    def _open_database_manager(self):
        self._show_database()

    def _open_analytics(self):
        self._show_analytics()

    def _open_settings(self):
        self._show_settings()

    def _show_user_guide(self):
        self._show_notification("Opening user guide...", "info")

    def _show_troubleshooting(self):
        self._show_notification("Opening troubleshooting guide...", "info")

    def _show_about(self):
        """Show about dialog with creator info"""
        about_text = f"""
🏭 {self.config.app_name} {self.config.version}

Excel to SQL Management System with Modern UI

Created by: {self.config.author}
Nickname: {self.config.nickname}

© 2024 DENSO Corporation
Innovation Department
        """
        messagebox.showinfo("About DENSO888", about_text.strip())

    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self._on_closing()
        except Exception as e:
            messagebox.showerror("Error", f"Application error: {e}")


# Entry point for modern application
def main():
    """Main entry point for modern DENSO888"""
    try:
        app = ModernDENSO888MainWindow()
        app.run()
    except Exception as e:
        print(f"Failed to start DENSO888: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
