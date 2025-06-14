"""
gui/pages/database_page_modern.py
Modern Database Configuration with Enhanced UI
Created by: Thammaphon Chittasuwanna (SDM) | Innovation Department
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Dict, Any, Optional
from pathlib import Path
import threading
import random
import time
from datetime import datetime


class DatabasePageModern:
    """Modern database configuration page"""

    def __init__(self, parent: tk.Widget, controller, theme):
        self.parent = parent
        self.controller = controller
        self.theme = theme

        # Database configuration variables
        self.db_type = tk.StringVar(value="sqlite")
        self.sqlite_file = tk.StringVar(value="denso888_data.db")
        self.server_name = tk.StringVar()
        self.database_name = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.use_windows_auth = tk.BooleanVar(value=True)
        self.connection_timeout = tk.IntVar(value=30)

        # UI state
        self.connection_status = "disconnected"
        self.test_results = {}

        self.main_frame = None
        self._create_database_page()

    def _create_database_page(self):
        """Create modern database configuration page"""
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

        # Database sections
        self._create_connection_status_section()
        self._create_database_type_section()
        self._create_sqlite_section()
        self._create_sqlserver_section()
        self._create_advanced_settings_section()
        self._create_test_section()
        self._create_database_tools_section()

        # Setup event handlers
        self._setup_events()

        # Bind mousewheel
        canvas.bind(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"),
        )

    def _create_connection_status_section(self):
        """Create connection status overview"""
        status_frame = self._create_section("📊 Connection Status")

        # Status card
        self.status_card = tk.Frame(
            status_frame,
            bg=self.theme.colors.surface_dark,
            relief="flat",
            bd=2,
            padx=25,
            pady=20,
        )
        self.status_card.pack(fill="x", pady=(0, 20))

        # Status indicator
        indicator_frame = tk.Frame(self.status_card, bg=self.theme.colors.surface_dark)
        indicator_frame.pack(fill="x")

        self.status_icon = tk.Label(
            indicator_frame,
            text="🔴",
            font=("Segoe UI", 24),
            bg=self.theme.colors.surface_dark,
        )
        self.status_icon.pack(side="left")

        status_text_frame = tk.Frame(indicator_frame, bg=self.theme.colors.surface_dark)
        status_text_frame.pack(side="left", fill="both", expand=True, padx=(15, 0))

        self.status_title = tk.Label(
            status_text_frame,
            text="Database Disconnected",
            font=self.theme.fonts["heading_md"],
            bg=self.theme.colors.surface_dark,
            fg=self.theme.colors.text_primary,
        )
        self.status_title.pack(anchor="w")

        self.status_details = tk.Label(
            status_text_frame,
            text="No active database connection",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface_dark,
            fg=self.theme.colors.text_secondary,
        )
        self.status_details.pack(anchor="w")

        # Connection metrics (initially hidden)
        self.metrics_frame = tk.Frame(
            self.status_card, bg=self.theme.colors.surface_dark
        )
        self.metrics_frame.pack(fill="x", pady=(15, 0))
        self.metrics_frame.pack_forget()

        # Metrics grid
        metrics_grid = tk.Frame(self.metrics_frame, bg=self.theme.colors.surface_dark)
        metrics_grid.pack(fill="x")

        self.metrics_labels = {}
        metrics = [
            "Response Time",
            "Active Connections",
            "Database Size",
            "Last Backup",
        ]

        for i, metric in enumerate(metrics):
            row = i // 2
            col = i % 2

            metric_frame = tk.Frame(metrics_grid, bg=self.theme.colors.surface_dark)
            metric_frame.grid(row=row, column=col, padx=10, pady=5, sticky="ew")

            # Metric label
            label = tk.Label(
                metric_frame,
                text=f"{metric}:",
                font=self.theme.fonts["body_sm"],
                bg=self.theme.colors.surface_dark,
                fg=self.theme.colors.text_secondary,
                anchor="w",
            )
            label.pack(fill="x")

            # Metric value
            value = tk.Label(
                metric_frame,
                text="N/A",
                font=self.theme.fonts["body_md"],
                bg=self.theme.colors.surface_dark,
                fg=self.theme.colors.text_primary,
                anchor="w",
            )
            value.pack(fill="x")

            self.metrics_labels[metric] = value

        metrics_grid.grid_columnconfigure(0, weight=1)
        metrics_grid.grid_columnconfigure(1, weight=1)

    def _create_database_type_section(self):
        """Create database type selection"""
        type_frame = self._create_section("🔧 Database Type")

        # Database type cards
        types_container = tk.Frame(type_frame, bg=self.theme.colors.surface)
        types_container.pack(fill="x")

        # SQLite card
        self.sqlite_card = self._create_db_type_card(
            types_container,
            "SQLite",
            "💾",
            "Local file-based database",
            "Perfect for development and small applications",
            self.theme.colors.success,
            "sqlite",
        )
        self.sqlite_card.pack(fill="x", pady=(0, 15))

        # SQL Server card
        self.sqlserver_card = self._create_db_type_card(
            types_container,
            "SQL Server",
            "🖥️",
            "Enterprise database server",
            "High-performance database for production environments",
            self.theme.colors.info,
            "sqlserver",
        )
        self.sqlserver_card.pack(fill="x")

        # Initially select SQLite
        self._select_db_type("sqlite")

    def _create_db_type_card(
        self, parent, title, icon, subtitle, description, color, db_type
    ):
        """Create database type selection card"""
        card_frame = tk.Frame(
            parent,
            bg=self.theme.colors.surface_dark,
            relief="flat",
            bd=2,
            padx=20,
            pady=15,
        )

        # Card content
        content_frame = tk.Frame(card_frame, bg=self.theme.colors.surface_dark)
        content_frame.pack(fill="x")

        # Radio button
        radio = tk.Radiobutton(
            content_frame,
            variable=self.db_type,
            value=db_type,
            bg=self.theme.colors.surface_dark,
            activebackground=self.theme.colors.surface_dark,
            command=lambda: self._select_db_type(db_type),
        )
        radio.pack(side="left")

        # Icon and text
        info_frame = tk.Frame(content_frame, bg=self.theme.colors.surface_dark)
        info_frame.pack(side="left", fill="both", expand=True, padx=(10, 0))

        # Header
        header_frame = tk.Frame(info_frame, bg=self.theme.colors.surface_dark)
        header_frame.pack(fill="x")

        icon_label = tk.Label(
            header_frame,
            text=icon,
            font=("Segoe UI", 20),
            bg=self.theme.colors.surface_dark,
            fg=color,
        )
        icon_label.pack(side="left")

        title_frame = tk.Frame(header_frame, bg=self.theme.colors.surface_dark)
        title_frame.pack(side="left", fill="both", expand=True, padx=(10, 0))

        title_label = tk.Label(
            title_frame,
            text=title,
            font=self.theme.fonts["heading_sm"],
            bg=self.theme.colors.surface_dark,
            fg=self.theme.colors.text_primary,
            anchor="w",
        )
        title_label.pack(fill="x")

        subtitle_label = tk.Label(
            title_frame,
            text=subtitle,
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface_dark,
            fg=color,
            anchor="w",
        )
        subtitle_label.pack(fill="x")

        # Description
        desc_label = tk.Label(
            info_frame,
            text=description,
            font=self.theme.fonts["body_sm"],
            bg=self.theme.colors.surface_dark,
            fg=self.theme.colors.text_secondary,
            anchor="w",
            wraplength=400,
            justify="left",
        )
        desc_label.pack(fill="x", pady=(5, 0))

        # Store references
        card_frame.db_type = db_type
        card_frame.radio = radio

        # Make card clickable
        def select_card(event):
            self.db_type.set(db_type)
            self._select_db_type(db_type)

        card_frame.bind("<Button-1>", select_card)
        content_frame.bind("<Button-1>", select_card)
        info_frame.bind("<Button-1>", select_card)

        return card_frame

    def _create_sqlite_section(self):
        """Create SQLite configuration section"""
        self.sqlite_section = self._create_section("📁 SQLite Configuration")

        # File selection
        file_frame = tk.Frame(self.sqlite_section, bg=self.theme.colors.surface)
        file_frame.pack(fill="x", pady=(0, 20))

        # File path
        path_label = tk.Label(
            file_frame,
            text="Database File Path:",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
        )
        path_label.pack(anchor="w", pady=(0, 8))

        path_input_frame = tk.Frame(file_frame, bg=self.theme.colors.surface)
        path_input_frame.pack(fill="x")

        self.sqlite_entry = tk.Entry(
            path_input_frame,
            textvariable=self.sqlite_file,
            font=self.theme.fonts["body_md"],
            relief="solid",
            bd=1,
        )
        self.sqlite_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        browse_btn = tk.Button(
            path_input_frame,
            text="📁 Browse",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.secondary,
            fg="white",
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self._browse_sqlite_file,
        )
        browse_btn.pack(side="right")

        # SQLite options
        options_frame = tk.LabelFrame(
            self.sqlite_section,
            text="SQLite Options",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
        )
        options_frame.pack(fill="x", pady=(10, 0))

        self.sqlite_wal_mode = tk.BooleanVar(value=True)
        self.sqlite_foreign_keys = tk.BooleanVar(value=True)
        self.sqlite_journal_mode = tk.StringVar(value="WAL")

        # Checkboxes
        wal_check = tk.Checkbutton(
            options_frame,
            variable=self.sqlite_wal_mode,
            text="🔄 Enable WAL mode (Write-Ahead Logging)",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface,
            activebackground=self.theme.colors.surface,
        )
        wal_check.pack(anchor="w", pady=5, padx=10)

        fk_check = tk.Checkbutton(
            options_frame,
            variable=self.sqlite_foreign_keys,
            text="🔗 Enable foreign key constraints",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface,
            activebackground=self.theme.colors.surface,
        )
        fk_check.pack(anchor="w", pady=5, padx=10)

        # Initially hidden
        self.sqlite_section.pack_forget()

    def _create_sqlserver_section(self):
        """Create SQL Server configuration section"""
        self.sqlserver_section = self._create_section("🖥️ SQL Server Configuration")

        # Connection details
        conn_frame = tk.Frame(self.sqlserver_section, bg=self.theme.colors.surface)
        conn_frame.pack(fill="x", pady=(0, 20))

        # Server name
        server_frame = tk.Frame(conn_frame, bg=self.theme.colors.surface)
        server_frame.pack(fill="x", pady=5)

        tk.Label(
            server_frame,
            text="Server Name:",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
            width=15,
            anchor="w",
        ).pack(side="left")

        tk.Entry(
            server_frame,
            textvariable=self.server_name,
            font=self.theme.fonts["body_md"],
            relief="solid",
            bd=1,
            width=35,
        ).pack(side="left", padx=(10, 0))

        # Database name
        db_frame = tk.Frame(conn_frame, bg=self.theme.colors.surface)
        db_frame.pack(fill="x", pady=5)

        tk.Label(
            db_frame,
            text="Database Name:",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
            width=15,
            anchor="w",
        ).pack(side="left")

        tk.Entry(
            db_frame,
            textvariable=self.database_name,
            font=self.theme.fonts["body_md"],
            relief="solid",
            bd=1,
            width=35,
        ).pack(side="left", padx=(10, 0))

        # Authentication
        auth_frame = tk.LabelFrame(
            self.sqlserver_section,
            text="Authentication",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
        )
        auth_frame.pack(fill="x", pady=(0, 20))

        # Windows authentication
        windows_auth_check = tk.Checkbutton(
            auth_frame,
            variable=self.use_windows_auth,
            text="🔐 Use Windows Authentication",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface,
            activebackground=self.theme.colors.surface,
            command=self._toggle_auth_method,
        )
        windows_auth_check.pack(anchor="w", pady=10, padx=10)

        # SQL authentication (initially hidden)
        self.sql_auth_frame = tk.Frame(auth_frame, bg=self.theme.colors.surface)
        self.sql_auth_frame.pack(fill="x", padx=10, pady=(0, 10))

        # Username
        user_frame = tk.Frame(self.sql_auth_frame, bg=self.theme.colors.surface)
        user_frame.pack(fill="x", pady=2)

        tk.Label(
            user_frame,
            text="Username:",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
            width=12,
            anchor="w",
        ).pack(side="left")

        tk.Entry(
            user_frame,
            textvariable=self.username,
            font=self.theme.fonts["body_md"],
            relief="solid",
            bd=1,
            width=30,
        ).pack(side="left", padx=(10, 0))

        # Password
        pass_frame = tk.Frame(self.sql_auth_frame, bg=self.theme.colors.surface)
        pass_frame.pack(fill="x", pady=2)

        tk.Label(
            pass_frame,
            text="Password:",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
            width=12,
            anchor="w",
        ).pack(side="left")

        tk.Entry(
            pass_frame,
            textvariable=self.password,
            font=self.theme.fonts["body_md"],
            relief="solid",
            bd=1,
            show="*",
            width=30,
        ).pack(side="left", padx=(10, 0))

        # Initially hide SQL auth and section
        self._toggle_auth_method()
        self.sqlserver_section.pack_forget()

    def _create_advanced_settings_section(self):
        """Create advanced database settings"""
        self.advanced_section = self._create_section("⚙️ Advanced Settings")

        # Connection settings
        conn_settings_frame = tk.LabelFrame(
            self.advanced_section,
            text="Connection Settings",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
        )
        conn_settings_frame.pack(fill="x", pady=(0, 15))

        # Timeout setting
        timeout_frame = tk.Frame(conn_settings_frame, bg=self.theme.colors.surface)
        timeout_frame.pack(fill="x", pady=10, padx=10)

        tk.Label(
            timeout_frame,
            text="Connection Timeout (seconds):",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
        ).pack(side="left")

        timeout_spinbox = tk.Spinbox(
            timeout_frame,
            textvariable=self.connection_timeout,
            from_=5,
            to=300,
            font=self.theme.fonts["body_md"],
            width=10,
        )
        timeout_spinbox.pack(side="left", padx=(10, 0))

        # Pool settings (for SQL Server)
        self.pool_settings_frame = tk.LabelFrame(
            self.advanced_section,
            text="Connection Pool Settings",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
        )
        self.pool_settings_frame.pack(fill="x")

        # Pool size
        pool_frame = tk.Frame(self.pool_settings_frame, bg=self.theme.colors.surface)
        pool_frame.pack(fill="x", pady=5, padx=10)

        self.pool_size = tk.IntVar(value=5)
        self.max_overflow = tk.IntVar(value=10)

        tk.Label(
            pool_frame,
            text="Pool Size:",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
            width=12,
            anchor="w",
        ).pack(side="left")

        tk.Spinbox(
            pool_frame,
            textvariable=self.pool_size,
            from_=1,
            to=50,
            font=self.theme.fonts["body_md"],
            width=10,
        ).pack(side="left", padx=(10, 20))

        tk.Label(
            pool_frame,
            text="Max Overflow:",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
            width=12,
            anchor="w",
        ).pack(side="left")

        tk.Spinbox(
            pool_frame,
            textvariable=self.max_overflow,
            from_=0,
            to=100,
            font=self.theme.fonts["body_md"],
            width=10,
        ).pack(side="left", padx=(10, 0))

    def _create_test_section(self):
        """Create connection test section"""
        test_frame = self._create_section("🔍 Connection Test")

        # Test buttons
        buttons_frame = tk.Frame(test_frame, bg=self.theme.colors.surface)
        buttons_frame.pack(fill="x", pady=(0, 20))

        self.test_btn = tk.Button(
            buttons_frame,
            text="🔍 Test Connection",
            font=self.theme.fonts["body_lg"],
            bg=self.theme.colors.info,
            fg="white",
            relief="flat",
            bd=0,
            padx=25,
            pady=12,
            cursor="hand2",
            command=self._test_connection,
        )
        self.test_btn.pack(side="left", padx=(0, 15))

        self.connect_btn = tk.Button(
            buttons_frame,
            text="🔗 Connect",
            font=self.theme.fonts["body_lg"],
            bg=self.theme.colors.success,
            fg="white",
            relief="flat",
            bd=0,
            padx=25,
            pady=12,
            cursor="hand2",
            command=self._connect_database,
            state="disabled",
        )
        self.connect_btn.pack(side="left")

        # Test results
        self.test_results_frame = tk.Frame(
            test_frame, bg=self.theme.colors.surface_dark
        )
        self.test_results_frame.pack(fill="x")
        self.test_results_frame.pack_forget()  # Initially hidden

    def _create_database_tools_section(self):
        """Create database management tools"""
        tools_frame = self._create_section("🛠️ Database Tools")

        # Tools grid
        tools_grid = tk.Frame(tools_frame, bg=self.theme.colors.surface)
        tools_grid.pack(fill="x")

        # Define tools
        tools = [
            {
                "title": "Backup Database",
                "description": "Create database backup",
                "icon": "💾",
                "color": self.theme.colors.success,
                "command": self._backup_database,
            },
            {
                "title": "Restore Database",
                "description": "Restore from backup",
                "icon": "📥",
                "color": self.theme.colors.warning,
                "command": self._restore_database,
            },
            {
                "title": "Optimize Database",
                "description": "Optimize performance",
                "icon": "⚡",
                "color": self.theme.colors.info,
                "command": self._optimize_database,
            },
            {
                "title": "View Tables",
                "description": "Browse database tables",
                "icon": "📋",
                "color": self.theme.colors.primary,
                "command": self._view_tables,
            },
        ]

        # Create tool buttons
        for i, tool in enumerate(tools):
            row = i // 2
            col = i % 2

            tool_btn = self._create_tool_button(tools_grid, tool)
            tool_btn.grid(row=row, column=col, padx=10, pady=10, sticky="ew")

        tools_grid.grid_columnconfigure(0, weight=1)
        tools_grid.grid_columnconfigure(1, weight=1)

    def _create_tool_button(self, parent, tool_config):
        """Create database tool button"""
        btn_frame = tk.Frame(parent, bg=self.theme.colors.surface)

        button = tk.Button(
            btn_frame,
            text="",
            bg=self.theme.colors.surface_dark,
            fg=self.theme.colors.text_primary,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=tool_config["command"],
            padx=15,
            pady=12,
        )
        button.pack(fill="both", expand=True)

        # Button content
        content_frame = tk.Frame(button, bg=self.theme.colors.surface_dark)
        content_frame.pack(fill="both", expand=True)

        # Icon
        icon_label = tk.Label(
            content_frame,
            text=tool_config["icon"],
            font=("Segoe UI", 18),
            bg=self.theme.colors.surface_dark,
            fg=tool_config["color"],
        )
        icon_label.pack(pady=(0, 5))

        # Title
        title_label = tk.Label(
            content_frame,
            text=tool_config["title"],
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface_dark,
            fg=self.theme.colors.text_primary,
        )
        title_label.pack()

        # Description
        desc_label = tk.Label(
            content_frame,
            text=tool_config["description"],
            font=self.theme.fonts["caption"],
            bg=self.theme.colors.surface_dark,
            fg=self.theme.colors.text_secondary,
        )
        desc_label.pack()

        # Hover effects
        def on_enter(event):
            button.configure(bg=tool_config["color"])
            content_frame.configure(bg=tool_config["color"])
            icon_label.configure(bg=tool_config["color"], fg="white")
            title_label.configure(bg=tool_config["color"], fg="white")
            desc_label.configure(bg=tool_config["color"], fg="white")

        def on_leave(event):
            button.configure(bg=self.theme.colors.surface_dark)
            content_frame.configure(bg=self.theme.colors.surface_dark)
            icon_label.configure(
                bg=self.theme.colors.surface_dark, fg=tool_config["color"]
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

    def _create_section(self, title: str) -> tk.Widget:
        """Create a section with title"""
        container = tk.Frame(self.scrollable_frame, bg=self.theme.colors.background)
        container.pack(fill="x", padx=20, pady=(0, 25))

        # Section title
        title_label = tk.Label(
            container,
            text=title,
            font=self.theme.fonts["heading_md"],
            bg=self.theme.colors.background,
            fg=self.theme.colors.text_primary,
        )
        title_label.pack(anchor="w", pady=(0, 15))

        # Section content
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

    def _setup_events(self):
        """Setup event handlers"""
        # Database type change
        self.db_type.trace("w", lambda *args: self._on_db_type_changed())

        # Authentication change
        self.use_windows_auth.trace("w", lambda *args: self._toggle_auth_method())

        # Initial setup
        self._on_db_type_changed()

    def _select_db_type(self, db_type: str):
        """Select database type"""
        self.db_type.set(db_type)

        # Update card appearances
        if hasattr(self, "sqlite_card") and hasattr(self, "sqlserver_card"):
            if db_type == "sqlite":
                self.sqlite_card.configure(relief="solid", bd=2)
                self.sqlserver_card.configure(relief="flat", bd=1)
            else:
                self.sqlite_card.configure(relief="flat", bd=1)
                self.sqlserver_card.configure(relief="solid", bd=2)

        self._on_db_type_changed()

    def _on_db_type_changed(self):
        """Handle database type change"""
        db_type = self.db_type.get()

        if db_type == "sqlite":
            self.sqlite_section.pack(fill="x", padx=20, pady=(0, 25))
            self.sqlserver_section.pack_forget()
            self.pool_settings_frame.pack_forget()
        else:
            self.sqlite_section.pack_forget()
            self.sqlserver_section.pack(fill="x", padx=20, pady=(0, 25))
            self.pool_settings_frame.pack(fill="x")

        # Reset connection status
        self._update_connection_status("disconnected")

    def _toggle_auth_method(self):
        """Toggle SQL Server authentication method"""
        if self.use_windows_auth.get():
            self.sql_auth_frame.pack_forget()
        else:
            self.sql_auth_frame.pack(fill="x", padx=10, pady=(0, 10))

    def _browse_sqlite_file(self):
        """Browse for SQLite database file"""
        filename = filedialog.asksaveasfilename(
            title="SQLite Database File",
            defaultextension=".db",
            filetypes=[
                ("SQLite Database", "*.db"),
                ("SQLite Database", "*.sqlite"),
                ("All files", "*.*"),
            ],
        )

        if filename:
            self.sqlite_file.set(filename)

    def _test_connection(self):
        """Test database connection"""
        # Disable test button during test
        self.test_btn.configure(state="disabled", text="🔄 Testing...")

        def test_task():
            try:
                # Prepare configuration
                config = self._get_current_config()

                # Update controller configuration
                self.controller.update_database_config(config)

                # Test connection
                success = self.controller.test_database_connection()

                # Update UI on main thread
                self.main_frame.after(
                    0, lambda: self._show_test_results(success, config)
                )

            except Exception as e:
                self.main_frame.after(
                    0, lambda: self._show_test_results(False, {}, str(e))
                )

            finally:
                # Re-enable button
                self.main_frame.after(
                    0,
                    lambda: self.test_btn.configure(
                        state="normal", text="🔍 Test Connection"
                    ),
                )

        # Run test in background
        threading.Thread(target=test_task, daemon=True).start()

    def _show_test_results(
        self, success: bool, config: Dict[str, Any], error: str = ""
    ):
        """Show connection test results"""
        # Clear previous results
        for widget in self.test_results_frame.winfo_children():
            widget.destroy()

        # Show results frame
        self.test_results_frame.pack(fill="x", pady=(15, 0))

        # Results header
        header_frame = tk.Frame(
            self.test_results_frame, bg=self.theme.colors.surface_dark
        )
        header_frame.pack(fill="x", padx=15, pady=15)

        if success:
            icon = "✅"
            title = "Connection Test Successful"
            color = self.theme.colors.success
            self.connect_btn.configure(state="normal")
        else:
            icon = "❌"
            title = "Connection Test Failed"
            color = self.theme.colors.danger
            self.connect_btn.configure(state="disabled")

        # Result icon and title
        result_header = tk.Frame(header_frame, bg=self.theme.colors.surface_dark)
        result_header.pack(fill="x")

        icon_label = tk.Label(
            result_header,
            text=icon,
            font=("Segoe UI", 20),
            bg=self.theme.colors.surface_dark,
            fg=color,
        )
        icon_label.pack(side="left")

        title_label = tk.Label(
            result_header,
            text=title,
            font=self.theme.fonts["heading_sm"],
            bg=self.theme.colors.surface_dark,
            fg=color,
        )
        title_label.pack(side="left", padx=(10, 0))

        # Connection details
        if success:
            details_text = (
                f"Database Type: {config.get('db_type', 'Unknown').upper()}\n"
            )

            if config.get("db_type") == "sqlite":
                details_text += f"File: {config.get('sqlite_file', 'Unknown')}"
            else:
                details_text += f"Server: {config.get('server', 'Unknown')}\n"
                details_text += f"Database: {config.get('database', 'Unknown')}"

            # Mock performance metrics
            details_text += f"\n\nPerformance:\n"
            details_text += f"Response Time: {random.randint(10, 50)}ms\n"
            details_text += f"Connection Pool: Ready"
        else:
            details_text = f"Error: {error}" if error else "Connection failed"

        details_label = tk.Label(
            header_frame,
            text=details_text,
            font=self.theme.fonts["body_sm"],
            bg=self.theme.colors.surface_dark,
            fg=self.theme.colors.text_secondary,
            anchor="w",
            justify="left",
        )
        details_label.pack(fill="x", pady=(10, 0))

    def _connect_database(self):
        """Connect to database"""

        def connect_task():
            try:
                # Get configuration
                config = self._get_current_config()

                # Update controller
                self.controller.update_database_config(config)

                # Connect
                success = self.controller.connect_database()

                # Update UI
                if success:
                    self.main_frame.after(
                        0, lambda: self._update_connection_status("connected", config)
                    )
                else:
                    self.main_frame.after(
                        0, lambda: self._update_connection_status("failed")
                    )

            except Exception as e:
                self.main_frame.after(
                    0, lambda: self._update_connection_status("error", error=str(e))
                )

        # Run connection in background
        threading.Thread(target=connect_task, daemon=True).start()

    def _update_connection_status(
        self, status: str, config: Optional[Dict[str, Any]] = None, error: str = ""
    ):
        """Update connection status display"""
        self.connection_status = status

        if status == "connected":
            self.status_icon.configure(text="🟢")
            self.status_title.configure(
                text="Database Connected", fg=self.theme.colors.success
            )

            if config:
                if config.get("db_type") == "sqlite":
                    details = f"SQLite: {Path(config.get('sqlite_file', '')).name}"
                else:
                    details = f"SQL Server: {config.get('server', '')}/{config.get('database', '')}"
            else:
                details = "Active database connection"

            self.status_details.configure(text=details)

            # Show metrics
            self.metrics_frame.pack(fill="x", pady=(15, 0))
            self._update_connection_metrics()

            # Update status card color
            self.status_card.configure(bg=self.theme.colors.success, fg="white")

        elif status == "disconnected":
            self.status_icon.configure(text="🔴")
            self.status_title.configure(
                text="Database Disconnected", fg=self.theme.colors.danger
            )
            self.status_details.configure(text="No active database connection")
            self.metrics_frame.pack_forget()
            self.status_card.configure(bg=self.theme.colors.surface_dark)

        elif status == "failed" or status == "error":
            self.status_icon.configure(text="⚠️")
            self.status_title.configure(
                text="Connection Failed", fg=self.theme.colors.warning
            )
            self.status_details.configure(
                text=error or "Failed to establish connection"
            )
            self.metrics_frame.pack_forget()
            self.status_card.configure(bg=self.theme.colors.surface_dark)

    def _update_connection_metrics(self):
        """Update connection performance metrics"""
        import random

        metrics_data = {
            "Response Time": f"{random.randint(5, 25)}ms",
            "Active Connections": f"{random.randint(1, 5)}",
            "Database Size": f"{random.randint(10, 500)}MB",
            "Last Backup": f"{random.randint(1, 30)} days ago",
        }

        for metric, value in metrics_data.items():
            if metric in self.metrics_labels:
                self.metrics_labels[metric].configure(text=value)

    def _get_current_config(self) -> Dict[str, Any]:
        """Get current database configuration"""
        return {
            "db_type": self.db_type.get(),
            "sqlite_file": self.sqlite_file.get(),
            "server": self.server_name.get(),
            "database": self.database_name.get(),
            "username": self.username.get(),
            "password": self.password.get(),
            "use_windows_auth": self.use_windows_auth.get(),
            "connection_timeout": self.connection_timeout.get(),
            "pool_size": self.pool_size.get(),
            "max_overflow": self.max_overflow.get(),
        }

    def _backup_database(self):
        """Backup database"""
        messagebox.showinfo("Backup", "Database backup feature coming soon!")

    def _restore_database(self):
        """Restore database"""
        messagebox.showinfo("Restore", "Database restore feature coming soon!")

    def _optimize_database(self):
        """Optimize database"""
        messagebox.showinfo("Optimize", "Database optimization feature coming soon!")

    def _view_tables(self):
        """View database tables"""
        messagebox.showinfo("Tables", "Database table viewer coming soon!")

    def refresh(self):
        """Refresh database page"""
        # Update connection status
        db_status = self.controller.get_database_status()
        connected = db_status.get("connected", False)

        if connected:
            self._update_connection_status("connected")
        else:
            self._update_connection_status("disconnected")

    def show(self):
        """Show database page"""
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def hide(self):
        """Hide database page"""
        self.main_frame.pack_forget()

    def get_widget(self) -> tk.Widget:
        """Get main database widget"""
        return self.main_frame


# Mock Page Modern
class MockPageModern:
    """Modern mock data generation page"""

    def __init__(self, parent: tk.Widget, controller, theme):
        self.parent = parent
        self.controller = controller
        self.theme = theme

        # Mock data settings
        self.template_type = tk.StringVar(value="employees")
        self.record_count = tk.IntVar(value=1000)
        self.custom_count = tk.StringVar()

        # Available templates
        self.templates = {
            "employees": {
                "title": "👥 Employee Records",
                "description": "Generate realistic employee data with departments, salaries, and personal information",
                "icon": "👥",
                "color": self.theme.colors.primary,
                "fields": [
                    "ID",
                    "Name",
                    "Email",
                    "Department",
                    "Position",
                    "Salary",
                    "Hire Date",
                    "Status",
                ],
                "sample_count": "1,000 - 50,000",
            },
            "sales": {
                "title": "💰 Sales Transactions",
                "description": "Create sales data with products, customers, and transaction details",
                "icon": "💰",
                "color": self.theme.colors.success,
                "fields": [
                    "Transaction ID",
                    "Customer",
                    "Product",
                    "Quantity",
                    "Price",
                    "Total",
                    "Date",
                ],
                "sample_count": "5,000 - 100,000",
            },
            "inventory": {
                "title": "📦 Inventory Items",
                "description": "Generate product inventory with stock levels and supplier information",
                "icon": "📦",
                "color": self.theme.colors.info,
                "fields": [
                    "Product ID",
                    "Name",
                    "Category",
                    "Stock",
                    "Price",
                    "Supplier",
                    "Location",
                ],
                "sample_count": "500 - 10,000",
            },
            "financial": {
                "title": "💳 Financial Records",
                "description": "Create financial transactions with accounts and payment details",
                "icon": "💳",
                "color": self.theme.colors.warning,
                "fields": [
                    "Account",
                    "Transaction",
                    "Amount",
                    "Type",
                    "Date",
                    "Reference",
                    "Balance",
                ],
                "sample_count": "1,000 - 25,000",
            },
        }

        self.main_frame = None
        self._create_mock_page()

    def _create_mock_page(self):
        """Create modern mock data page"""
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

        # Mock data sections
        self._create_template_selection_section()
        self._create_quantity_selection_section()
        self._create_preview_section()
        self._create_generation_section()

        # Bind mousewheel
        canvas.bind(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"),
        )

    def _create_template_selection_section(self):
        """Create template selection section"""
        template_frame = self._create_section("🎲 Select Data Template")

        # Template cards grid
        templates_grid = tk.Frame(template_frame, bg=self.theme.colors.surface)
        templates_grid.pack(fill="x")

        self.template_cards = {}

        for i, (template_id, template_info) in enumerate(self.templates.items()):
            row = i // 2
            col = i % 2

            card = self._create_template_card(
                templates_grid, template_id, template_info
            )
            card.grid(row=row, column=col, padx=10, pady=10, sticky="ew")

            self.template_cards[template_id] = card

        # Configure grid
        templates_grid.grid_columnconfigure(0, weight=1)
        templates_grid.grid_columnconfigure(1, weight=1)

        # Initially select employees template
        self._select_template("employees")

    def _create_template_card(
        self, parent, template_id: str, template_info: Dict[str, Any]
    ):
        """Create template selection card"""
        card_frame = tk.Frame(
            parent,
            bg=self.theme.colors.surface_dark,
            relief="flat",
            bd=2,
            padx=20,
            pady=20,
        )

        # Radio button
        radio = tk.Radiobutton(
            card_frame,
            variable=self.template_type,
            value=template_id,
            bg=self.theme.colors.surface_dark,
            activebackground=self.theme.colors.surface_dark,
            command=lambda: self._select_template(template_id),
        )
        radio.pack(anchor="w", pady=(0, 10))

        # Template info
        info_frame = tk.Frame(card_frame, bg=self.theme.colors.surface_dark)
        info_frame.pack(fill="x")

        # Icon and title
        header_frame = tk.Frame(info_frame, bg=self.theme.colors.surface_dark)
        header_frame.pack(fill="x", pady=(0, 8))

        icon_label = tk.Label(
            header_frame,
            text=template_info["icon"],
            font=("Segoe UI", 24),
            bg=self.theme.colors.surface_dark,
            fg=template_info["color"],
        )
        icon_label.pack(side="left")

        title_label = tk.Label(
            header_frame,
            text=template_info["title"],
            font=self.theme.fonts["heading_sm"],
            bg=self.theme.colors.surface_dark,
            fg=self.theme.colors.text_primary,
        )
        title_label.pack(side="left", padx=(10, 0))

        # Description
        desc_label = tk.Label(
            info_frame,
            text=template_info["description"],
            font=self.theme.fonts["body_sm"],
            bg=self.theme.colors.surface_dark,
            fg=self.theme.colors.text_secondary,
            wraplength=250,
            justify="left",
        )
        desc_label.pack(fill="x", pady=(0, 10))

        # Sample count
        count_label = tk.Label(
            info_frame,
            text=f"Recommended: {template_info['sample_count']} records",
            font=self.theme.fonts["caption"],
            bg=self.theme.colors.surface_dark,
            fg=template_info["color"],
        )
        count_label.pack(fill="x")

        # Store references
        card_frame.template_id = template_id
        card_frame.radio = radio

        # Make card clickable
        def select_card(event):
            self.template_type.set(template_id)
            self._select_template(template_id)

        card_frame.bind("<Button-1>", select_card)
        info_frame.bind("<Button-1>", select_card)

        return card_frame

    def _create_quantity_selection_section(self):
        """Create quantity selection section"""
        quantity_frame = self._create_section("📊 Select Record Quantity")

        # Preset quantities
        presets_frame = tk.Frame(quantity_frame, bg=self.theme.colors.surface)
        presets_frame.pack(fill="x", pady=(0, 20))

        presets_label = tk.Label(
            presets_frame,
            text="Quick Select:",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
        )
        presets_label.pack(anchor="w", pady=(0, 10))

        # Preset buttons
        preset_values = [100, 500, 1000, 5000, 10000, 50000]
        presets_grid = tk.Frame(presets_frame, bg=self.theme.colors.surface)
        presets_grid.pack(fill="x")

        for i, value in enumerate(preset_values):
            row = i // 3
            col = i % 3

            preset_btn = tk.Radiobutton(
                presets_grid,
                text=f"{value:,}",
                variable=self.record_count,
                value=value,
                font=self.theme.fonts["body_md"],
                bg=self.theme.colors.info,
                fg="white",
                selectcolor=self.theme.colors.primary,
                activebackground=self.theme.colors.info,
                activeforeground="white",
                relief="flat",
                bd=0,
                padx=15,
                pady=8,
                width=10,
                command=self._on_quantity_changed,
            )
            preset_btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")

        # Configure grid
        for col in range(3):
            presets_grid.grid_columnconfigure(col, weight=1)

        # Custom quantity
        custom_frame = tk.Frame(quantity_frame, bg=self.theme.colors.surface)
        custom_frame.pack(fill="x", pady=(10, 0))

        custom_label = tk.Label(
            custom_frame,
            text="Custom Quantity:",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
        )
        custom_label.pack(side="left")

        custom_entry = tk.Entry(
            custom_frame,
            textvariable=self.custom_count,
            font=self.theme.fonts["body_md"],
            width=15,
            relief="solid",
            bd=1,
        )
        custom_entry.pack(side="left", padx=(15, 10))

        custom_entry.bind("<Return>", self._apply_custom_count)
        custom_entry.bind("<FocusOut>", self._apply_custom_count)

        apply_btn = tk.Button(
            custom_frame,
            text="Apply",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.secondary,
            fg="white",
            relief="flat",
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self._apply_custom_count,
        )
        apply_btn.pack(side="left")

        # Quantity info
        self.quantity_info = tk.Label(
            quantity_frame,
            text="",
            font=self.theme.fonts["body_sm"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_secondary,
        )
        self.quantity_info.pack(anchor="w", pady=(15, 0))

        self._update_quantity_info()

    def _create_preview_section(self):
        """Create template preview section"""
        self.preview_section = self._create_section("👁️ Template Preview")

        # Template details
        self.details_frame = tk.Frame(
            self.preview_section, bg=self.theme.colors.surface
        )
        self.details_frame.pack(fill="x", pady=(0, 20))

        # Sample fields display
        self.fields_frame = tk.Frame(
            self.preview_section, bg=self.theme.colors.surface_dark
        )
        self.fields_frame.pack(fill="x")

        self._update_preview()

    def _create_generation_section(self):
        """Create data generation section"""
        generation_frame = self._create_section("🚀 Generate Mock Data")

        # Generation options
        options_frame = tk.Frame(generation_frame, bg=self.theme.colors.surface)
        options_frame.pack(fill="x", pady=(0, 20))

        # Output table name
        table_frame = tk.Frame(options_frame, bg=self.theme.colors.surface)
        table_frame.pack(fill="x", pady=5)

        tk.Label(
            table_frame,
            text="Table Name:",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
            width=12,
            anchor="w",
        ).pack(side="left")

        self.table_name = tk.StringVar()
        self._generate_table_name()

        table_entry = tk.Entry(
            table_frame,
            textvariable=self.table_name,
            font=self.theme.fonts["body_md"],
            width=35,
            relief="solid",
            bd=1,
        )
        table_entry.pack(side="left", padx=(10, 0))

        # Generation options
        gen_options_frame = tk.LabelFrame(
            generation_frame,
            text="Generation Options",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
        )
        gen_options_frame.pack(fill="x", pady=(10, 20))

        self.include_nulls = tk.BooleanVar(value=False)
        self.realistic_data = tk.BooleanVar(value=True)
        self.consistent_relationships = tk.BooleanVar(value=True)

        options = [
            (self.include_nulls, "🔹 Include some null values (realistic data)"),
            (self.realistic_data, "🎯 Use realistic data patterns"),
            (self.consistent_relationships, "🔗 Maintain data relationships"),
        ]

        for var, text in options:
            checkbox = tk.Checkbutton(
                gen_options_frame,
                variable=var,
                text=text,
                font=self.theme.fonts["body_md"],
                bg=self.theme.colors.surface,
                activebackground=self.theme.colors.surface,
            )
            checkbox.pack(anchor="w", pady=5, padx=15)

        # Generation button
        self.generate_btn = tk.Button(
            generation_frame,
            text="🎲 Generate Mock Data",
            font=self.theme.fonts["body_lg"],
            bg=self.theme.colors.primary,
            fg="white",
            relief="flat",
            bd=0,
            padx=30,
            pady=15,
            cursor="hand2",
            command=self._generate_mock_data,
        )
        self.generate_btn.pack(pady=20)

        # Progress section
        self.progress_frame = tk.Frame(generation_frame, bg=self.theme.colors.surface)
        self.progress_frame.pack(fill="x", pady=(15, 0))
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
        container.pack(fill="x", padx=20, pady=(0, 25))

        # Section title
        title_label = tk.Label(
            container,
            text=title,
            font=self.theme.fonts["heading_md"],
            bg=self.theme.colors.background,
            fg=self.theme.colors.text_primary,
        )
        title_label.pack(anchor="w", pady=(0, 15))

        # Section content
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

    def _select_template(self, template_id: str):
        """Select mock data template"""
        self.template_type.set(template_id)

        # Update card appearances
        for tid, card in self.template_cards.items():
            if tid == template_id:
                card.configure(relief="solid", bd=3)
            else:
                card.configure(relief="flat", bd=2)

        # Update preview
        self._update_preview()

        # Generate new table name
        self._generate_table_name()

    def _update_preview(self):
        """Update template preview"""
        template_id = self.template_type.get()
        template_info = self.templates.get(template_id, {})

        # Clear previous details
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        # Template details
        detail_text = f"Template: {template_info.get('title', 'Unknown')}\n"
        detail_text += (
            f"Description: {template_info.get('description', 'No description')}"
        )

        details_label = tk.Label(
            self.details_frame,
            text=detail_text,
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
            anchor="w",
            justify="left",
        )
        details_label.pack(fill="x")

        # Clear previous fields
        for widget in self.fields_frame.winfo_children():
            widget.destroy()

        # Fields header
        fields_header = tk.Label(
            self.fields_frame,
            text="📋 Sample Fields:",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.surface_dark,
            fg=self.theme.colors.text_primary,
        )
        fields_header.pack(anchor="w", pady=(10, 5), padx=15)

        # Fields list
        fields = template_info.get("fields", [])
        fields_text = " • ".join(fields)

        fields_label = tk.Label(
            self.fields_frame,
            text=fields_text,
            font=self.theme.fonts["body_sm"],
            bg=self.theme.colors.surface_dark,
            fg=self.theme.colors.text_secondary,
            wraplength=600,
            justify="left",
        )
        fields_label.pack(anchor="w", padx=15, pady=(0, 10))

    def _on_quantity_changed(self):
        """Handle quantity change"""
        self._update_quantity_info()

    def _apply_custom_count(self, event=None):
        """Apply custom count"""
        try:
            custom_value = int(self.custom_count.get())
            if 1 <= custom_value <= 1000000:
                self.record_count.set(custom_value)
                self._update_quantity_info()
            else:
                messagebox.showwarning(
                    "Invalid Quantity", "Please enter a number between 1 and 1,000,000"
                )
        except ValueError:
            pass

    def _update_quantity_info(self):
        """Update quantity information"""
        count = self.record_count.get()

        # Estimate generation time
        if count <= 1000:
            time_estimate = "< 1 second"
        elif count <= 10000:
            time_estimate = "1-5 seconds"
        elif count <= 50000:
            time_estimate = "5-30 seconds"
        else:
            time_estimate = "30+ seconds"

        # Estimate data size
        size_mb = (count * 100) / (1024 * 1024)  # Rough estimate
        if size_mb < 1:
            size_estimate = f"{size_mb * 1024:.0f} KB"
        else:
            size_estimate = f"{size_mb:.1f} MB"

        info_text = f"Will generate {count:,} records • Estimated time: {time_estimate} • Size: ~{size_estimate}"
        self.quantity_info.configure(text=info_text)

    def _generate_table_name(self):
        """Generate table name based on template and timestamp"""
        template_id = self.template_type.get()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        table_name = f"mock_{template_id}_{timestamp}"
        self.table_name.set(table_name)

    def _generate_mock_data(self):
        """Generate mock data"""
        if not self.controller.is_connected:
            messagebox.showerror("Generation Error", "Database not connected!")
            return

        # Disable generate button
        self.generate_btn.configure(state="disabled", text="🔄 Generating...")

        # Show progress
        self.progress_frame.pack(fill="x", pady=(15, 0))

        def generation_task():
            try:
                template = self.template_type.get()
                count = self.record_count.get()
                table_name = self.table_name.get()

                # Simulate generation progress
                for i in range(0, 101, 5):
                    self.progress_var.set(i)
                    if i < 20:
                        status = "Initializing generator..."
                    elif i < 50:
                        status = f"Generating {template} data..."
                    elif i < 80:
                        status = "Creating database table..."
                    else:
                        status = "Inserting records..."

                    self.progress_label.configure(text=f"{status} ({i}%)")
                    self.main_frame.update()
                    time.sleep(0.1)

                # Call controller to generate data
                success = self.controller.generate_mock_data(
                    template, count, table_name
                )

                if success:
                    self.progress_label.configure(
                        text=f"✅ Successfully generated {count:,} {template} records!"
                    )
                    messagebox.showinfo(
                        "Generation Complete",
                        f"Successfully generated {count:,} {template} records in table '{table_name}'",
                    )
                else:
                    self.progress_label.configure(text="❌ Generation failed!")
                    messagebox.showerror(
                        "Generation Error", "Failed to generate mock data"
                    )

            except Exception as e:
                self.progress_label.configure(text=f"❌ Error: {str(e)}")
                messagebox.showerror("Generation Error", f"Generation failed: {str(e)}")

            finally:
                # Re-enable button
                self.generate_btn.configure(
                    state="normal", text="🎲 Generate Mock Data"
                )

        # Run generation in background
        threading.Thread(target=generation_task, daemon=True).start()

    def refresh(self):
        """Refresh mock page"""
        pass

    def show(self):
        """Show mock page"""
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def hide(self):
        """Hide mock page"""
        self.main_frame.pack_forget()

    def get_widget(self) -> tk.Widget:
        """Get main mock widget"""
        return self.main_frame


# Analytics Page for insights
class AnalyticsPage:
    """Modern analytics page with data insights"""

    def __init__(self, parent: tk.Widget, controller, theme):
        self.parent = parent
        self.controller = controller
        self.theme = theme

        self.main_frame = None
        self._create_analytics_page()

    def _create_analytics_page(self):
        """Create analytics page"""
        self.main_frame = tk.Frame(self.parent, bg=self.theme.colors.background)

        # Analytics content
        content_frame = tk.Frame(self.main_frame, bg=self.theme.colors.background)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Coming soon message
        coming_soon_frame = tk.Frame(
            content_frame,
            bg=self.theme.colors.surface,
            relief="flat",
            bd=1,
            padx=50,
            pady=50,
        )
        coming_soon_frame.pack(expand=True)

        # Icon
        icon_label = tk.Label(
            coming_soon_frame,
            text="📈",
            font=("Segoe UI", 48),
            bg=self.theme.colors.surface,
            fg=self.theme.colors.primary,
        )
        icon_label.pack(pady=(0, 20))

        # Title
        title_label = tk.Label(
            coming_soon_frame,
            text="Analytics Dashboard",
            font=self.theme.fonts["heading_xl"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
        )
        title_label.pack(pady=(0, 10))

        # Description
        desc_label = tk.Label(
            coming_soon_frame,
            text="Advanced data analytics and insights coming soon!\nExplore trends, patterns, and generate reports from your data.",
            font=self.theme.fonts["body_lg"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_secondary,
            justify="center",
        )
        desc_label.pack()

    def refresh(self):
        """Refresh analytics page"""
        pass

    def show(self):
        """Show analytics page"""
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def hide(self):
        """Hide analytics page"""
        self.main_frame.pack_forget()

    def get_widget(self) -> tk.Widget:
        """Get main analytics widget"""
        return self.main_frame


# Settings Page
class SettingsPage:
    """Modern settings page"""

    def __init__(self, parent: tk.Widget, controller, theme, preferences):
        self.parent = parent
        self.controller = controller
        self.theme = theme
        self.preferences = preferences

        self.main_frame = None
        self._create_settings_page()

    def _create_settings_page(self):
        """Create settings page"""
        self.main_frame = tk.Frame(self.parent, bg=self.theme.colors.background)

        # Settings content
        content_frame = tk.Frame(self.main_frame, bg=self.theme.colors.background)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Coming soon message
        coming_soon_frame = tk.Frame(
            content_frame,
            bg=self.theme.colors.surface,
            relief="flat",
            bd=1,
            padx=50,
            pady=50,
        )
        coming_soon_frame.pack(expand=True)

        # Icon
        icon_label = tk.Label(
            coming_soon_frame,
            text="⚙️",
            font=("Segoe UI", 48),
            bg=self.theme.colors.surface,
            fg=self.theme.colors.primary,
        )
        icon_label.pack(pady=(0, 20))

        # Title
        title_label = tk.Label(
            coming_soon_frame,
            text="Application Settings",
            font=self.theme.fonts["heading_xl"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
        )
        title_label.pack(pady=(0, 10))

        # Description
        desc_label = tk.Label(
            coming_soon_frame,
            text="Customize your DENSO888 experience!\nThemes, preferences, and advanced settings coming soon.",
            font=self.theme.fonts["body_lg"],
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_secondary,
            justify="center",
        )
        desc_label.pack()

    def refresh(self):
        """Refresh settings page"""
        pass

    def show(self):
        """Show settings page"""
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def hide(self):
        """Hide settings page"""
        self.main_frame.pack_forget()

    def get_widget(self) -> tk.Widget:
        """Get main settings widget"""
        return self.main_frame
