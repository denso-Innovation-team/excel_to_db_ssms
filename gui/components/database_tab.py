import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Callable


class DatabaseTab:
    """Database connection tab component"""

    def __init__(self, parent: ttk.Notebook, callbacks: Dict[str, Callable]):
        self.frame = ttk.Frame(parent, padding="10")
        self.callbacks = callbacks
        self._create_widgets()

    def _create_widgets(self):
        # Database type selection
        type_frame = ttk.LabelFrame(self.frame, text="Database Type", padding="10")
        type_frame.pack(fill="x", pady=(0, 10))

        self.db_type = tk.StringVar(value="sqlite")
        ttk.Radiobutton(
            type_frame,
            text="SQLite (Local File)",
            variable=self.db_type,
            value="sqlite",
            command=self._on_type_change,
        ).pack(anchor="w")

        ttk.Radiobutton(
            type_frame,
            text="SQL Server (SSMS)",
            variable=self.db_type,
            value="sqlserver",
            command=self._on_type_change,
        ).pack(anchor="w")

        # Connection details frame
        self.conn_frame = ttk.LabelFrame(
            self.frame, text="Connection Details", padding="10"
        )
        self.conn_frame.pack(fill="x", pady=(0, 10))

        # Initial form
        self._create_sqlite_form()

        # Buttons
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill="x")

        ttk.Button(
            btn_frame, text="Test Connection", command=lambda: self.callbacks["test"]()
        ).pack(side="left", padx=(0, 10))

        ttk.Button(
            btn_frame, text="Connect", command=lambda: self.callbacks["connect"]()
        ).pack(side="left", padx=(0, 10))

        ttk.Button(
            btn_frame, text="Disconnect", command=lambda: self.callbacks["disconnect"]()
        ).pack(side="left")

    def _create_sqlite_form(self):
        # Clear existing
        for widget in self.conn_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.conn_frame, text="Database File:").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.sqlite_path = tk.StringVar(value="data/denso888.db")
        ttk.Entry(self.conn_frame, textvariable=self.sqlite_path, width=60).grid(
            row=0, column=1, sticky="ew", padx=(10, 0)
        )

        self.conn_frame.grid_columnconfigure(1, weight=1)

    def _create_sqlserver_form(self):
        # Clear existing
        for widget in self.conn_frame.winfo_children():
            widget.destroy()

        # Server settings
        ttk.Label(self.conn_frame, text="Server:").grid(
            row=0, column=0, sticky="w", pady=2
        )
        self.server = tk.StringVar(value="localhost\\SQLEXPRESS")
        ttk.Entry(self.conn_frame, textvariable=self.server, width=40).grid(
            row=0, column=1, sticky="ew", padx=(10, 0)
        )

        # Database
        ttk.Label(self.conn_frame, text="Database:").grid(
            row=1, column=0, sticky="w", pady=2
        )
        self.database = tk.StringVar()
        self.db_combo = ttk.Combobox(
            self.conn_frame, textvariable=self.database, width=38
        )
        self.db_combo.grid(row=1, column=1, sticky="ew", padx=(10, 0))

        # Authentication
        ttk.Label(self.conn_frame, text="Authentication:").grid(
            row=2, column=0, sticky="w", pady=2
        )
        self.auth_type = tk.StringVar(value="windows")
        auth_frame = ttk.Frame(self.conn_frame)
        auth_frame.grid(row=2, column=1, sticky="w", padx=(10, 0))

        ttk.Radiobutton(
            auth_frame,
            text="Windows Authentication",
            variable=self.auth_type,
            value="windows",
            command=self._toggle_sql_auth,
        ).pack(side="left", padx=(0, 10))

        ttk.Radiobutton(
            auth_frame,
            text="SQL Server Authentication",
            variable=self.auth_type,
            value="sql",
            command=self._toggle_sql_auth,
        ).pack(side="left")

        # SQL Authentication fields
        self.sql_auth_frame = ttk.Frame(self.conn_frame)
        self.sql_auth_frame.grid(
            row=3, column=0, columnspan=2, sticky="ew", pady=(10, 0)
        )
        self.sql_auth_frame.grid_remove()

        ttk.Label(self.sql_auth_frame, text="Username:").grid(
            row=0, column=0, sticky="w"
        )
        self.username = tk.StringVar()
        ttk.Entry(self.sql_auth_frame, textvariable=self.username, width=30).grid(
            row=0, column=1, sticky="w", padx=(10, 0)
        )

        ttk.Label(self.sql_auth_frame, text="Password:").grid(
            row=1, column=0, sticky="w", pady=(5, 0)
        )
        self.password = tk.StringVar()
        ttk.Entry(
            self.sql_auth_frame, textvariable=self.password, show="*", width=30
        ).grid(row=1, column=1, sticky="w", padx=(10, 0), pady=(5, 0))

        self.conn_frame.grid_columnconfigure(1, weight=1)

    def _on_type_change(self, *args):
        if self.db_type.get() == "sqlite":
            self._create_sqlite_form()
        else:
            self._create_sqlserver_form()

    def _toggle_sql_auth(self, *args):
        if self.auth_type.get() == "sql":
            self.sql_auth_frame.grid()
        else:
            self.sql_auth_frame.grid_remove()

    def get_config(self) -> Dict[str, Any]:
        """Get current connection configuration"""
        if self.db_type.get() == "sqlite":
            return {"type": "sqlite", "file": self.sqlite_path.get()}
        else:
            config = {
                "type": "sqlserver",
                "server": self.server.get(),
                "database": self.database.get(),
                "use_windows_auth": self.auth_type.get() == "windows",
            }

            if self.auth_type.get() == "sql":
                config.update(
                    {"username": self.username.get(), "password": self.password.get()}
                )

            return config

    def get_widget(self) -> ttk.Frame:
        return self.frame
