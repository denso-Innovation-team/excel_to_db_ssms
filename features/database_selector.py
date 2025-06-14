"""
Database Type Selector Widget
ฟีเจอร์เลือก SQLite หรือ SQL Server พร้อมการตั้งค่า
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Callable, Optional, Dict, Any


class DatabaseSelector:
    """Modern Database Selection Component"""

    def __init__(self, parent: tk.Widget, test_callback: Optional[Callable] = None):
        self.parent = parent
        self.test_callback = test_callback

        # Variables
        self.db_type = tk.StringVar(value="sqlite")
        self.sqlite_file = tk.StringVar(value="denso888_data.db")
        self.sql_server = tk.StringVar()
        self.sql_database = tk.StringVar()
        self.sql_username = tk.StringVar()
        self.sql_password = tk.StringVar()
        self.use_windows_auth = tk.BooleanVar(value=True)

        self.frame = tk.Frame(parent, bg="#FFFFFF")
        self.create_widgets()

    def create_widgets(self):
        """Create database selection widgets"""
        # Title
        title = tk.Label(
            self.frame,
            text="🗄️ Database Configuration",
            font=("Segoe UI", 16, "bold"),
            fg="#DC0003",
            bg="#FFFFFF",
        )
        title.pack(pady=(0, 20))

        # Database type selection
        type_frame = tk.LabelFrame(
            self.frame,
            text="Database Type",
            font=("Segoe UI", 12, "bold"),
            fg="#2C3E50",
            bg="#FFFFFF",
            padx=20,
            pady=15,
        )
        type_frame.pack(fill="x", pady=(0, 15))

        # SQLite option
        sqlite_frame = tk.Frame(type_frame, bg="#FFFFFF")
        sqlite_frame.pack(fill="x", pady=5)

        sqlite_radio = tk.Radiobutton(
            sqlite_frame,
            text="💾 SQLite (Local Database)",
            variable=self.db_type,
            value="sqlite",
            command=self._on_type_change,
            font=("Segoe UI", 12, "bold"),
            fg="#2C3E50",
            bg="#FFFFFF",
            activebackground="#FFFFFF",
        )
        sqlite_radio.pack(anchor="w")

        sqlite_desc = tk.Label(
            sqlite_frame,
            text="    Perfect for development and small-scale applications",
            font=("Segoe UI", 10),
            fg="#7F8C8D",
            bg="#FFFFFF",
        )
        sqlite_desc.pack(anchor="w")

        # SQL Server option
        sqlserver_frame = tk.Frame(type_frame, bg="#FFFFFF")
        sqlserver_frame.pack(fill="x", pady=5)

        sqlserver_radio = tk.Radiobutton(
            sqlserver_frame,
            text="🖥️ SQL Server (Enterprise Database)",
            variable=self.db_type,
            value="sqlserver",
            command=self._on_type_change,
            font=("Segoe UI", 12, "bold"),
            fg="#2C3E50",
            bg="#FFFFFF",
            activebackground="#FFFFFF",
        )
        sqlserver_radio.pack(anchor="w")

        sqlserver_desc = tk.Label(
            sqlserver_frame,
            text="    Enterprise-grade database for production environments",
            font=("Segoe UI", 10),
            fg="#7F8C8D",
            bg="#FFFFFF",
        )
        sqlserver_desc.pack(anchor="w")

        # SQLite settings
        self.sqlite_frame = tk.LabelFrame(
            self.frame,
            text="SQLite Settings",
            font=("Segoe UI", 12, "bold"),
            fg="#2C3E50",
            bg="#FFFFFF",
            padx=20,
            pady=15,
        )
        self.sqlite_frame.pack(fill="x", pady=(0, 15))

        file_frame = tk.Frame(self.sqlite_frame, bg="#FFFFFF")
        file_frame.pack(fill="x")

        tk.Label(
            file_frame,
            text="Database File:",
            font=("Segoe UI", 11, "bold"),
            fg="#2C3E50",
            bg="#FFFFFF",
        ).pack(anchor="w", pady=(0, 5))

        entry_frame = tk.Frame(file_frame, bg="#FFFFFF")
        entry_frame.pack(fill="x")

        sqlite_entry = tk.Entry(
            entry_frame,
            textvariable=self.sqlite_file,
            font=("Segoe UI", 11),
            relief="solid",
            borderwidth=1,
        )
        sqlite_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        browse_btn = tk.Button(
            entry_frame,
            text="📁 Browse",
            command=self._browse_sqlite,
            font=("Segoe UI", 10),
            bg="#6C757D",
            fg="#FFFFFF",
            relief="flat",
            padx=15,
            pady=5,
            cursor="hand2",
        )
        browse_btn.pack(side="right")

        # SQL Server settings
        self.sqlserver_frame = tk.LabelFrame(
            self.frame,
            text="SQL Server Settings",
            font=("Segoe UI", 12, "bold"),
            fg="#2C3E50",
            bg="#FFFFFF",
            padx=20,
            pady=15,
        )
        self.sqlserver_frame.pack(fill="x", pady=(0, 15))

        # Server details
        server_frame = tk.Frame(self.sqlserver_frame, bg="#FFFFFF")
        server_frame.pack(fill="x", pady=(0, 10))

        # Server name
        tk.Label(
            server_frame,
            text="Server Name:",
            font=("Segoe UI", 11, "bold"),
            fg="#2C3E50",
            bg="#FFFFFF",
        ).grid(row=0, column=0, sticky="w", pady=2)

        tk.Entry(
            server_frame,
            textvariable=self.sql_server,
            font=("Segoe UI", 11),
            relief="solid",
            borderwidth=1,
            width=30,
        ).grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=2)

        # Database name
        tk.Label(
            server_frame,
            text="Database Name:",
            font=("Segoe UI", 11, "bold"),
            fg="#2C3E50",
            bg="#FFFFFF",
        ).grid(row=1, column=0, sticky="w", pady=2)

        tk.Entry(
            server_frame,
            textvariable=self.sql_database,
            font=("Segoe UI", 11),
            relief="solid",
            borderwidth=1,
            width=30,
        ).grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=2)

        server_frame.grid_columnconfigure(1, weight=1)

        # Authentication
        auth_frame = tk.Frame(self.sqlserver_frame, bg="#FFFFFF")
        auth_frame.pack(fill="x", pady=(10, 0))

        windows_auth_check = tk.Checkbutton(
            auth_frame,
            text="🔐 Use Windows Authentication",
            variable=self.use_windows_auth,
            command=self._on_auth_change,
            font=("Segoe UI", 11, "bold"),
            fg="#2C3E50",
            bg="#FFFFFF",
            activebackground="#FFFFFF",
        )
        windows_auth_check.pack(anchor="w", pady=(0, 10))

        # SQL Authentication (hidden by default)
        self.sql_auth_frame = tk.Frame(self.sqlserver_frame, bg="#FFFFFF")
        self.sql_auth_frame.pack(fill="x")

        tk.Label(
            self.sql_auth_frame,
            text="Username:",
            font=("Segoe UI", 11, "bold"),
            fg="#2C3E50",
            bg="#FFFFFF",
        ).grid(row=0, column=0, sticky="w", pady=2)

        tk.Entry(
            self.sql_auth_frame,
            textvariable=self.sql_username,
            font=("Segoe UI", 11),
            relief="solid",
            borderwidth=1,
            width=30,
        ).grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=2)

        tk.Label(
            self.sql_auth_frame,
            text="Password:",
            font=("Segoe UI", 11, "bold"),
            fg="#2C3E50",
            bg="#FFFFFF",
        ).grid(row=1, column=0, sticky="w", pady=2)

        tk.Entry(
            self.sql_auth_frame,
            textvariable=self.sql_password,
            font=("Segoe UI", 11),
            relief="solid",
            borderwidth=1,
            show="*",
            width=30,
        ).grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=2)

        self.sql_auth_frame.grid_columnconfigure(1, weight=1)

        # Test button
        test_btn = tk.Button(
            self.frame,
            text="🔍 Test Connection",
            command=self._test_connection,
            font=("Segoe UI", 12, "bold"),
            bg="#007BFF",
            fg="#FFFFFF",
            relief="flat",
            borderwidth=0,
            padx=30,
            pady=10,
            cursor="hand2",
        )
        test_btn.pack(pady=20)

        # Status label
        self.status_label = tk.Label(
            self.frame,
            text="🔴 Not Connected",
            font=("Segoe UI", 12, "bold"),
            fg="#DC3545",
            bg="#FFFFFF",
        )
        self.status_label.pack(pady=(0, 10))

        # Initialize UI
        self._on_type_change()
        self._on_auth_change()

    def _on_type_change(self):
        """Handle database type change"""
        if self.db_type.get() == "sqlite":
            self.sqlite_frame.pack(fill="x", pady=(0, 15))
            self.sqlserver_frame.pack_forget()
        else:
            self.sqlite_frame.pack_forget()
            self.sqlserver_frame.pack(fill="x", pady=(0, 15))

    def _on_auth_change(self):
        """Handle authentication change"""
        if self.use_windows_auth.get():
            self.sql_auth_frame.pack_forget()
        else:
            self.sql_auth_frame.pack(fill="x")

    def _browse_sqlite(self):
        """Browse for SQLite file"""
        filename = filedialog.asksaveasfilename(
            title="SQLite Database File",
            defaultextension=".db",
            filetypes=[("SQLite Database", "*.db"), ("All files", "*.*")],
        )
        if filename:
            self.sqlite_file.set(filename)

    def _test_connection(self):
        """Test database connection"""
        config = self.get_config()

        if self.test_callback:
            success, message = self.test_callback(config)

            if success:
                self.status_label.configure(text="🟢 Connected", fg="#28A745")
                messagebox.showinfo("Connection Test", f"✅ {message}")
            else:
                self.status_label.configure(text="🔴 Connection Failed", fg="#DC3545")
                messagebox.showerror("Connection Test", f"❌ {message}")

    def get_config(self) -> Dict[str, Any]:
        """Get current database configuration"""
        return {
            "db_type": self.db_type.get(),
            "sqlite_file": self.sqlite_file.get(),
            "server": self.sql_server.get(),
            "database": self.sql_database.get(),
            "username": self.sql_username.get(),
            "password": self.sql_password.get(),
            "use_windows_auth": self.use_windows_auth.get(),
        }

    def get_widget(self):
        """Get the main widget"""
        return self.frame
