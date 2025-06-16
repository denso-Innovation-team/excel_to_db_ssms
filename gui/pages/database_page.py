"""
gui/pages/database_page.py
Database Configuration Page
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading

from ..components.modern_button import ModernButton, ActionButton
from ..components.modern_input import LabeledInput, ModernCombobox
from ..components.modern_card import ModernCard, StatCard


class DatabasePage:
    """Database configuration and management page"""

    def __init__(self, parent: tk.Widget, controller):
        self.parent = parent
        self.controller = controller
        self.main_frame = None
        self.db_type_combo = None
        self.connection_form = None
        self.stats_cards = {}
        self.tables_tree = None

        self._create_database_page()
        self._load_current_config()

    def _create_database_page(self):
        """สร้างหน้า database configuration"""
        self.main_frame = tk.Frame(self.parent, bg="#FFFFFF")

        # Header
        self._create_header()

        # Database type selection
        self._create_type_selection()

        # Connection configuration
        self._create_connection_section()

        # Database status and stats
        self._create_status_section()

        # Tables management
        self._create_tables_section()

    def _create_header(self):
        """สร้าง header section"""
        header_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        header_frame.pack(fill="x", padx=20, pady=(20, 0))

        # Title
        title_label = tk.Label(
            header_frame,
            text="🗄️ Database Configuration",
            font=("Segoe UI", 18, "bold"),
            bg="#FFFFFF",
            fg="#1F2937",
        )
        title_label.pack(anchor="w")

        # Description
        desc_label = tk.Label(
            header_frame,
            text="Configure database connection and manage tables",
            font=("Segoe UI", 12),
            bg="#FFFFFF",
            fg="#6B7280",
        )
        desc_label.pack(anchor="w", pady=(5, 0))

    def _create_type_selection(self):
        """สร้าง database type selection"""
        type_card = ModernCard(
            self.main_frame,
            title="🎯 Database Type",
            width=800,
            height=120,
        )
        type_card.pack(fill="x", padx=20, pady=20)

        type_frame = tk.Frame(type_card.get_widget(), bg="#FFFFFF")
        type_frame.pack(fill="x", padx=20, pady=10)

        # Database type selection
        self.db_type_combo = ModernCombobox(
            type_frame,
            values=["SQLite", "SQL Server"],
            placeholder="Select database type...",
            width=30,
        )
        self.db_type_combo.bind("<<ComboboxSelected>>", self._on_type_change)
        self.db_type_combo.pack(anchor="w")

        # Type description
        self.type_desc = tk.Label(
            type_frame,
            text="Choose your database type",
            font=("Segoe UI", 10),
            bg="#FFFFFF",
            fg="#6B7280",
        )
        self.type_desc.pack(anchor="w", pady=(5, 0))

    def _create_connection_section(self):
        """สร้าง connection configuration section"""
        self.connection_card = ModernCard(
            self.main_frame,
            title="🔗 Connection Settings",
            width=800,
            height=350,
        )
        self.connection_card.pack(fill="x", padx=20, pady=(0, 20))

        # Connection form container
        self.connection_container = tk.Frame(
            self.connection_card.get_widget(), bg="#FFFFFF"
        )
        self.connection_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Initially empty - will be populated based on database type
        self._create_sqlite_form()

    def _create_sqlite_form(self):
        """สร้างฟอร์มสำหรับ SQLite"""
        self._clear_connection_form()

        # SQLite file path
        self.sqlite_file = LabeledInput(
            self.connection_container,
            "Database File:",
            "entry",
            placeholder="denso888_data.db",
            width=50,
        )
        self.sqlite_file.pack(fill="x", pady=(0, 15))

        # File location info
        info_label = tk.Label(
            self.connection_container,
            text="💡 SQLite database will be created automatically if it doesn't exist",
            font=("Segoe UI", 10),
            bg="#FFFFFF",
            fg="#059669",
        )
        info_label.pack(anchor="w", pady=(0, 15))

        # Test and connect buttons
        self._create_connection_buttons()

    def _create_sqlserver_form(self):
        """สร้างฟอร์มสำหรับ SQL Server"""
        self._clear_connection_form()

        # Server settings
        self.server_input = LabeledInput(
            self.connection_container,
            "Server Name:",
            "entry",
            placeholder="localhost\\SQLEXPRESS",
            width=40,
        )
        self.server_input.pack(fill="x", pady=(0, 15))

        self.database_input = LabeledInput(
            self.connection_container,
            "Database Name:",
            "entry",
            placeholder="denso888",
            width=40,
        )
        self.database_input.pack(fill="x", pady=(0, 15))

        # Authentication type
        auth_frame = tk.Frame(self.connection_container, bg="#FFFFFF")
        auth_frame.pack(fill="x", pady=(0, 15))

        tk.Label(
            auth_frame,
            text="Authentication:",
            font=("Segoe UI", 11, "bold"),
            bg="#FFFFFF",
            fg="#374151",
        ).pack(anchor="w")

        self.auth_var = tk.StringVar(value="windows")

        auth_options = [
            ("Windows Authentication", "windows"),
            ("SQL Server Authentication", "sql"),
        ]

        for text, value in auth_options:
            rb = tk.Radiobutton(
                auth_frame,
                text=text,
                variable=self.auth_var,
                value=value,
                font=("Segoe UI", 10),
                bg="#FFFFFF",
                activebackground="#FFFFFF",
                command=self._on_auth_change,
            )
            rb.pack(anchor="w", pady=2)

        # SQL Authentication fields (initially hidden)
        self.sql_auth_frame = tk.Frame(self.connection_container, bg="#FFFFFF")

        self.username_input = LabeledInput(
            self.sql_auth_frame,
            "Username:",
            "entry",
            placeholder="sa",
            width=30,
        )
        self.username_input.pack(fill="x", pady=(0, 10))

        self.password_input = LabeledInput(
            self.sql_auth_frame,
            "Password:",
            "entry",
            width=30,
        )
        # Make password field secure
        self.password_input.input_widget.get_widget().configure(show="*")
        self.password_input.pack(fill="x")

        # Test and connect buttons
        self._create_connection_buttons()

    def _create_connection_buttons(self):
        """สร้างปุ่ม test และ connect"""
        button_frame = tk.Frame(self.connection_container, bg="#FFFFFF")
        button_frame.pack(fill="x", pady=(20, 0))

        # Test connection button
        self.test_button = ActionButton(
            button_frame,
            "🔍 Test Connection",
            command=self._test_connection,
        )
        self.test_button.pack(side="right", padx=(10, 0))

        # Connect button
        self.connect_button = ActionButton(
            button_frame,
            "🔗 Connect",
            command=self._connect_database,
        )
        self.connect_button.pack(side="right")

    def _create_status_section(self):
        """สร้าง database status section"""
        status_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        status_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Status cards
        cards_frame = tk.Frame(status_frame, bg="#FFFFFF")
        cards_frame.pack(fill="x")

        # Configure grid
        for i in range(4):
            cards_frame.grid_columnconfigure(i, weight=1)

        # Create stat cards
        self.stats_cards["status"] = StatCard(
            cards_frame, "Connection", "Disconnected", "🔴", "danger"
        )
        self.stats_cards["status"].grid(row=0, column=0, padx=5, sticky="ew")

        self.stats_cards["tables"] = StatCard(
            cards_frame, "Tables", "0", "📊", "primary"
        )
        self.stats_cards["tables"].grid(row=0, column=1, padx=5, sticky="ew")

        self.stats_cards["records"] = StatCard(
            cards_frame, "Total Records", "0", "📝", "success"
        )
        self.stats_cards["records"].grid(row=0, column=2, padx=5, sticky="ew")

        self.stats_cards["size"] = StatCard(
            cards_frame, "Database Size", "0 MB", "💾", "warning"
        )
        self.stats_cards["size"].grid(row=0, column=3, padx=5, sticky="ew")

    def _create_tables_section(self):
        """สร้าง tables management section"""
        tables_card = ModernCard(
            self.main_frame,
            title="📋 Database Tables",
            width=800,
            height=300,
        )
        tables_card.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        tables_frame = tk.Frame(tables_card.get_widget(), bg="#FFFFFF")
        tables_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Tables treeview
        columns = ("name", "rows", "columns", "created")
        self.tables_tree = ttk.Treeview(
            tables_frame, columns=columns, show="headings", height=10
        )

        # Configure columns
        self.tables_tree.heading("name", text="Table Name")
        self.tables_tree.heading("rows", text="Rows")
        self.tables_tree.heading("columns", text="Columns")
        self.tables_tree.heading("created", text="Created")

        self.tables_tree.column("name", width=200)
        self.tables_tree.column("rows", width=100, anchor="center")
        self.tables_tree.column("columns", width=100, anchor="center")
        self.tables_tree.column("created", width=150)

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            tables_frame, orient="vertical", command=self.tables_tree.yview
        )
        self.tables_tree.configure(yscrollcommand=scrollbar.set)

        # Pack components
        self.tables_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Table actions
        actions_frame = tk.Frame(tables_frame, bg="#FFFFFF")
        actions_frame.pack(fill="x", pady=(10, 0))

        refresh_btn = ModernButton(
            actions_frame,
            "🔄 Refresh",
            command=self._refresh_tables,
            style="secondary",
        )
        refresh_btn.pack(side="right")

    def _clear_connection_form(self):
        """ล้างฟอร์ม connection"""
        for widget in self.connection_container.winfo_children():
            if not isinstance(widget, (ModernButton, ActionButton)):
                widget.destroy()

    def _on_type_change(self, event=None):
        """เมื่อเปลี่ยน database type"""
        db_type = self.db_type_combo.get_value()

        if db_type == "SQLite":
            self.type_desc.configure(
                text="Lightweight database - perfect for local development"
            )
            self._create_sqlite_form()
        elif db_type == "SQL Server":
            self.type_desc.configure(
                text="Enterprise database - for production environments"
            )
            self._create_sqlserver_form()

    def _on_auth_change(self):
        """เมื่อเปลี่ยน authentication type"""
        if self.auth_var.get() == "sql":
            self.sql_auth_frame.pack(fill="x", pady=(15, 0))
        else:
            self.sql_auth_frame.pack_forget()

    def _test_connection(self):
        """Test database connection"""
        config = self._get_connection_config()
        if not config:
            return

        def test_async():
            try:
                if hasattr(self.controller, "test_database_connection"):
                    success, message = self.controller.test_database_connection(config)

                    # Update UI in main thread
                    self.main_frame.after(
                        0, lambda: self._show_test_result(success, message)
                    )
                else:
                    self.main_frame.after(
                        0, lambda: self._show_test_result(False, "Test not available")
                    )
            except Exception as e:
                self.main_frame.after(0, lambda: self._show_test_result(False, str(e)))

        threading.Thread(target=test_async, daemon=True).start()

    def _connect_database(self):
        """Connect to database"""
        config = self._get_connection_config()
        if not config:
            return

        def connect_async():
            try:
                if hasattr(self.controller, "connect_database"):
                    success, message = self.controller.connect_database(config)

                    # Update UI in main thread
                    self.main_frame.after(
                        0, lambda: self._handle_connection_result(success, message)
                    )
                else:
                    self.main_frame.after(
                        0,
                        lambda: self._handle_connection_result(
                            False, "Connection not available"
                        ),
                    )
            except Exception as e:
                self.main_frame.after(
                    0, lambda: self._handle_connection_result(False, str(e))
                )

        threading.Thread(target=connect_async, daemon=True).start()

    def _get_connection_config(self) -> dict:
        """ได้ config สำหรับ connection"""
        db_type = self.db_type_combo.get_value()

        if not db_type:
            messagebox.showwarning("Warning", "Please select database type")
            return None

        if db_type == "SQLite":
            file_path = self.sqlite_file.get_value() or "denso888_data.db"
            return {
                "type": "sqlite",
                "file": file_path,
            }

        elif db_type == "SQL Server":
            server = self.server_input.get_value()
            database = self.database_input.get_value()

            if not server or not database:
                messagebox.showwarning(
                    "Warning", "Please fill in server and database name"
                )
                return None

            config = {
                "type": "sqlserver",
                "server": server,
                "database": database,
                "use_windows_auth": self.auth_var.get() == "windows",
            }

            if self.auth_var.get() == "sql":
                username = self.username_input.get_value()
                password = self.password_input.get_value()

                if not username or not password:
                    messagebox.showwarning(
                        "Warning", "Please provide username and password"
                    )
                    return None

                config.update(
                    {
                        "username": username,
                        "password": password,
                    }
                )

            return config

        return None

    def _show_test_result(self, success: bool, message: str):
        """แสดงผลลัพธ์การ test connection"""
        if success:
            messagebox.showinfo("Connection Test", f"✅ {message}")
        else:
            messagebox.showerror("Connection Test", f"❌ {message}")

    def _handle_connection_result(self, success: bool, message: str):
        """จัดการผลลัพธ์การ connect"""
        if success:
            messagebox.showinfo("Database Connection", f"✅ {message}")
            self._update_connection_status(True)
            self._refresh_database_stats()
            self._refresh_tables()
        else:
            messagebox.showerror("Database Connection", f"❌ {message}")
            self._update_connection_status(False)

    def _update_connection_status(self, connected: bool):
        """อัพเดทสถานะ connection"""
        if connected:
            self.stats_cards["status"].update_value("Connected")
            self.stats_cards["status"]._create_stat_layout()  # Refresh to show green
        else:
            self.stats_cards["status"].update_value("Disconnected")

    def _refresh_database_stats(self):
        """รีเฟรชสถิติฐานข้อมูล"""
        if hasattr(self.controller, "get_analytics_data"):
            try:
                stats = self.controller.get_analytics_data()

                if "error" not in stats:
                    # Update stat cards
                    self.stats_cards["tables"].update_value(
                        str(len(stats.get("tables", [])))
                    )
                    self.stats_cards["records"].update_value(
                        f"{stats.get('total_records', 0):,}"
                    )

                    # Database size (if available)
                    if hasattr(self.controller.db_service, "get_database_stats"):
                        db_stats = self.controller.db_service.get_database_stats()
                        size_bytes = db_stats.get("database_size", 0)
                        size_mb = (
                            round(size_bytes / (1024 * 1024), 2) if size_bytes else 0
                        )
                        self.stats_cards["size"].update_value(f"{size_mb} MB")
            except Exception as e:
                print(f"Error refreshing stats: {e}")

    def _refresh_tables(self):
        """รีเฟรชรายการตาราง"""
        # Clear existing items
        self.tables_tree.delete(*self.tables_tree.get_children())

        if hasattr(self.controller, "get_database_tables"):
            try:
                tables = self.controller.get_database_tables()

                for table_name in tables:
                    # Get table info
                    table_info = {}
                    if hasattr(self.controller, "get_table_info"):
                        table_info = self.controller.get_table_info(table_name)

                    rows = table_info.get("row_count", "N/A")
                    columns = table_info.get("column_count", "N/A")
                    created = "Recent"  # Could be enhanced with actual creation date

                    self.tables_tree.insert(
                        "", "end", values=(table_name, rows, columns, created)
                    )

            except Exception as e:
                print(f"Error refreshing tables: {e}")

    def _load_current_config(self):
        """โหลด config ปัจจุบัน"""
        if hasattr(self.controller, "get_database_config"):
            try:
                config = self.controller.get_database_config()

                # Set database type
                db_type = config.get("type", "").title()
                if db_type in ["Sqlite", "Sql Server"]:
                    self.db_type_combo.set_value(db_type.replace("Sql", "SQL"))
                    self._on_type_change()

                    # Load specific configuration
                    if db_type.lower() == "sqlite":
                        file_path = config.get("file", "")
                        if file_path and hasattr(self, "sqlite_file"):
                            self.sqlite_file.set_value(file_path)

                    elif db_type.lower() == "sqlserver":
                        if hasattr(self, "server_input"):
                            self.server_input.set_value(config.get("server", ""))
                            self.database_input.set_value(config.get("database", ""))

                            if config.get("use_windows_auth", True):
                                self.auth_var.set("windows")
                            else:
                                self.auth_var.set("sql")
                                if hasattr(self, "username_input"):
                                    self.username_input.set_value(
                                        config.get("username", "")
                                    )

                            self._on_auth_change()

            except Exception as e:
                print(f"Error loading config: {e}")

    def show(self):
        """Show database page"""
        if self.main_frame:
            self.main_frame.pack(fill="both", expand=True)
            self._refresh_database_stats()
            self._refresh_tables()

    def hide(self):
        """Hide database page"""
        if self.main_frame:
            self.main_frame.pack_forget()

    def get_widget(self) -> tk.Widget:
        """Get main widget"""
        return self.main_frame
