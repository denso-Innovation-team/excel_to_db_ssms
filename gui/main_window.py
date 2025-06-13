"""
Enhanced Database Configuration with Authentication & Discovery
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import logging
from typing import Optional, Dict, Any, Callable, List

logger = logging.getLogger(__name__)


class DatabaseFrame:
    """Enhanced database configuration with authentication"""

    def __init__(
        self, parent: tk.Widget, config, callback: Callable[[str, Dict[str, Any]], None]
    ):
        self.config = config
        self.callback = callback
        self.frame = ttk.LabelFrame(parent, text="🗄️ Database Connection", padding=15)

        # Connection state
        self.is_connected = False
        self.available_databases = []

        # Variables
        self.db_type = tk.StringVar(value="sqlite")
        self.sql_server = tk.StringVar(value="localhost")
        self.sql_database = tk.StringVar(value="")
        self.sql_username = tk.StringVar(value="sa")
        self.sql_password = tk.StringVar(value="")
        self.sql_windows_auth = tk.BooleanVar(value=True)
        self.sqlite_file = tk.StringVar(value="denso888_data.db")

        self._create_widgets()

    def _create_widgets(self) -> None:
        """Create enhanced database configuration UI"""

        # === Database Type Selection ===
        type_frame = ttk.LabelFrame(self.frame, text="📊 Database Type", padding=10)
        type_frame.pack(fill="x", pady=(0, 10))

        ttk.Radiobutton(
            type_frame,
            text="📁 SQLite (Local)",
            variable=self.db_type,
            value="sqlite",
            command=self._on_type_change,
        ).pack(side="left", padx=(0, 20))

        ttk.Radiobutton(
            type_frame,
            text="🏢 SQL Server",
            variable=self.db_type,
            value="sqlserver",
            command=self._on_type_change,
        ).pack(side="left")

        # === SQLite Configuration ===
        self.sqlite_frame = ttk.LabelFrame(
            self.frame, text="📁 SQLite Settings", padding=10
        )
        self.sqlite_frame.pack(fill="x", pady=(0, 10))

        sqlite_row = ttk.Frame(self.sqlite_frame)
        sqlite_row.pack(fill="x")

        ttk.Label(sqlite_row, text="Database File:").pack(side="left")
        ttk.Entry(sqlite_row, textvariable=self.sqlite_file, width=30).pack(
            side="left", padx=(10, 5), fill="x", expand=True
        )
        ttk.Button(sqlite_row, text="Browse", command=self._browse_sqlite).pack(
            side="right"
        )

        # === SQL Server Configuration ===
        self.sqlserver_frame = ttk.LabelFrame(
            self.frame, text="🏢 SQL Server Settings", padding=10
        )
        self.sqlserver_frame.pack(fill="x", pady=(0, 10))

        # Server connection
        server_frame = ttk.Frame(self.sqlserver_frame)
        server_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(server_frame, text="Server:").pack(side="left")
        server_entry = ttk.Entry(server_frame, textvariable=self.sql_server, width=25)
        server_entry.pack(side="left", padx=(10, 5))

        ttk.Button(
            server_frame, text="🔍 Discover", command=self._discover_servers
        ).pack(side="left", padx=5)

        # Authentication method
        auth_frame = ttk.LabelFrame(
            self.sqlserver_frame, text="🔐 Authentication", padding=8
        )
        auth_frame.pack(fill="x", pady=(0, 10))

        ttk.Radiobutton(
            auth_frame,
            text="Windows Authentication",
            variable=self.sql_windows_auth,
            value=True,
            command=self._on_auth_change,
        ).pack(anchor="w")

        ttk.Radiobutton(
            auth_frame,
            text="SQL Server Authentication",
            variable=self.sql_windows_auth,
            value=False,
            command=self._on_auth_change,
        ).pack(anchor="w")

        # SQL Server credentials
        self.credentials_frame = ttk.Frame(self.sqlserver_frame)
        self.credentials_frame.pack(fill="x", pady=(0, 10))

        cred_row1 = ttk.Frame(self.credentials_frame)
        cred_row1.pack(fill="x", pady=2)
        ttk.Label(cred_row1, text="Username:").pack(side="left")
        ttk.Entry(cred_row1, textvariable=self.sql_username, width=20).pack(
            side="left", padx=(10, 20)
        )

        ttk.Label(cred_row1, text="Password:").pack(side="left")
        ttk.Entry(cred_row1, textvariable=self.sql_password, width=20, show="*").pack(
            side="left", padx=(10, 0)
        )

        # Database selection
        self.db_selection_frame = ttk.Frame(self.sqlserver_frame)
        self.db_selection_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(self.db_selection_frame, text="Database:").pack(side="left")
        self.db_combo = ttk.Combobox(
            self.db_selection_frame,
            textvariable=self.sql_database,
            width=25,
            state="readonly",
        )
        self.db_combo.pack(side="left", padx=(10, 5))

        ttk.Button(
            self.db_selection_frame, text="🔄 Refresh", command=self._refresh_databases
        ).pack(side="left", padx=5)

        # === Connection Testing ===
        test_frame = ttk.Frame(self.frame)
        test_frame.pack(fill="x", pady=(10, 0))

        self.test_btn = ttk.Button(
            test_frame,
            text="🔌 Test Connection",
            command=self._test_connection,
            style="Primary.TButton",
        )
        self.test_btn.pack(side="left")

        self.connection_status = ttk.Label(
            test_frame,
            text="● Not Connected",
            foreground="red",
            font=("Segoe UI", 9, "bold"),
        )
        self.connection_status.pack(side="left", padx=(15, 0))

        # Connection info
        self.info_frame = ttk.Frame(self.frame)
        self.info_frame.pack(fill="x", pady=(5, 0))

        self.info_label = ttk.Label(
            self.info_frame, text="", foreground="gray", font=("Segoe UI", 8)
        )
        self.info_label.pack(anchor="w")

        # Initial state
        self._on_type_change()
        self._on_auth_change()

    def _on_type_change(self) -> None:
        """Handle database type change"""
        is_sqlite = self.db_type.get() == "sqlite"

        if is_sqlite:
            self.sqlite_frame.pack(fill="x", pady=(0, 10))
            self.sqlserver_frame.pack_forget()
        else:
            self.sqlite_frame.pack_forget()
            self.sqlserver_frame.pack(fill="x", pady=(0, 10))

        self.is_connected = False
        self._update_connection_status(False)
        self._notify_change()

    def _on_auth_change(self) -> None:
        """Handle authentication method change"""
        if self.sql_windows_auth.get():
            self._hide_credentials()
        else:
            self._show_credentials()

    def _show_credentials(self) -> None:
        """Show SQL Server credentials"""
        for widget in self.credentials_frame.winfo_children():
            try:
                widget.pack(fill="x", pady=2)
            except:
                pass

    def _hide_credentials(self) -> None:
        """Hide SQL Server credentials"""
        for widget in self.credentials_frame.winfo_children():
            try:
                widget.pack_forget()
            except:
                pass

    def _browse_sqlite(self) -> None:
        """Browse for SQLite file"""
        from tkinter import filedialog

        filename = filedialog.asksaveasfilename(
            title="Select SQLite Database File",
            defaultextension=".db",
            filetypes=[("SQLite files", "*.db"), ("All files", "*.*")],
        )
        if filename:
            self.sqlite_file.set(filename)
            self._notify_change()

    def _discover_servers(self) -> None:
        """Discover SQL Server instances"""
        self.test_btn.config(state="disabled", text="🔍 Discovering...")

        def discover_thread():
            try:
                import pyodbc

                # Common SQL Server instances
                servers = [
                    "localhost",
                    "localhost\\SQLEXPRESS",
                    "localhost\\MSSQLSERVER",
                    ".\\SQLEXPRESS",
                    "(local)",
                    "(local)\\SQLEXPRESS",
                ]

                # Try to discover network instances
                try:
                    # This is a simplified discovery - in production, use SQL Server Browser
                    import socket

                    hostname = socket.gethostname()
                    servers.extend(
                        [f"{hostname}\\SQLEXPRESS", f"{hostname}\\MSSQLSERVER"]
                    )
                except:
                    pass

                # Update UI
                self.root.after(0, lambda: self._on_discovery_complete(servers))

            except Exception as e:
                error_msg = f"Discovery failed: {str(e)}"
                self.root.after(0, lambda: self._on_discovery_error(error_msg))

        self.root = self.frame.winfo_toplevel()
        threading.Thread(target=discover_thread, daemon=True).start()

    def _on_discovery_complete(self, servers: List[str]) -> None:
        """Handle server discovery completion"""
        self.test_btn.config(state="normal", text="🔌 Test Connection")

        if servers:
            # Show server selection dialog
            dialog = ServerSelectionDialog(
                self.frame, servers, self._on_server_selected
            )
        else:
            messagebox.showinfo("Discovery", "No SQL Server instances found")

    def _on_discovery_error(self, error_msg: str) -> None:
        """Handle discovery error"""
        self.test_btn.config(state="normal", text="🔌 Test Connection")
        messagebox.showerror("Discovery Error", error_msg)

    def _on_server_selected(self, server: str) -> None:
        """Handle server selection from discovery"""
        self.sql_server.set(server)
        self._notify_change()

    def _refresh_databases(self) -> None:
        """Refresh available databases"""
        if not self.sql_server.get():
            messagebox.showwarning("Warning", "Please enter server name first")
            return

        self.db_combo.config(state="disabled")

        def refresh_thread():
            try:
                databases = self._get_available_databases()
                self.root.after(0, lambda: self._on_databases_refreshed(databases))
            except Exception as e:
                error_msg = f"Failed to get databases: {str(e)}"
                self.root.after(0, lambda: self._on_refresh_error(error_msg))

        self.root = self.frame.winfo_toplevel()
        threading.Thread(target=refresh_thread, daemon=True).start()

    def _get_available_databases(self) -> List[str]:
        """Get list of available databases"""
        import pyodbc

        # Build connection string for master database
        if self.sql_windows_auth.get():
            conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.sql_server.get()};DATABASE=master;Trusted_Connection=yes;"
        else:
            conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.sql_server.get()};DATABASE=master;UID={self.sql_username.get()};PWD={self.sql_password.get()};"

        # Connect and get databases
        with pyodbc.connect(conn_str, timeout=10) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sys.databases WHERE database_id > 4 ORDER BY name"
            )  # Exclude system databases
            databases = [row[0] for row in cursor.fetchall()]

            # Add common system databases that users might need
            system_dbs = ["master", "model", "msdb", "tempdb"]
            return system_dbs + databases

    def _on_databases_refreshed(self, databases: List[str]) -> None:
        """Handle database list refresh"""
        self.db_combo.config(state="readonly")
        self.db_combo["values"] = databases

        if databases:
            # Select first non-system database or first database
            user_dbs = [
                db
                for db in databases
                if db not in ["master", "model", "msdb", "tempdb"]
            ]
            if user_dbs:
                self.db_combo.set(user_dbs[0])
            else:
                self.db_combo.set(databases[0])

        self._notify_change()

    def _on_refresh_error(self, error_msg: str) -> None:
        """Handle database refresh error"""
        self.db_combo.config(state="readonly")
        messagebox.showerror("Database Refresh Error", error_msg)

    def _test_connection(self) -> None:
        """Test database connection"""
        self.test_btn.config(state="disabled", text="🔄 Testing...")

        def test_thread():
            try:
                success, info = self._perform_connection_test()
                self.root.after(0, lambda: self._on_test_complete(success, info))
            except Exception as e:
                error_msg = f"Connection test failed: {str(e)}"
                self.root.after(0, lambda: self._on_test_error(error_msg))

        self.root = self.frame.winfo_toplevel()
        threading.Thread(target=test_thread, daemon=True).start()

    def _perform_connection_test(self) -> tuple[bool, str]:
        """Perform actual connection test"""
        if self.db_type.get() == "sqlite":
            return self._test_sqlite_connection()
        else:
            return self._test_sqlserver_connection()

    def _test_sqlite_connection(self) -> tuple[bool, str]:
        """Test SQLite connection"""
        import sqlite3
        from pathlib import Path

        db_file = self.sqlite_file.get()
        if not db_file:
            return False, "Please specify database file"

        try:
            # Create directory if needed
            Path(db_file).parent.mkdir(parents=True, exist_ok=True)

            # Test connection
            with sqlite3.connect(db_file) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT sqlite_version()")
                version = cursor.fetchone()[0]

                # Get file size
                size = Path(db_file).stat().st_size if Path(db_file).exists() else 0
                size_mb = size / (1024 * 1024)

            return True, f"SQLite {version} • File: {db_file} • Size: {size_mb:.1f} MB"

        except Exception as e:
            return False, f"SQLite connection failed: {str(e)}"

    def _test_sqlserver_connection(self) -> tuple[bool, str]:
        """Test SQL Server connection"""
        import pyodbc

        server = self.sql_server.get()
        database = self.sql_database.get() or "master"

        if not server:
            return False, "Please specify server name"

        try:
            # Build connection string
            if self.sql_windows_auth.get():
                conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
            else:
                username = self.sql_username.get()
                password = self.sql_password.get()
                if not username:
                    return False, "Please specify username"
                conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};"

            # Test connection
            with pyodbc.connect(conn_str, timeout=10) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT @@SERVERNAME, @@VERSION, DB_NAME()")
                server_name, version, db_name = cursor.fetchone()

                # Extract SQL Server version
                version_info = version.split("\n")[0] if version else "Unknown"

            return (
                True,
                f"Connected to {server_name} • Database: {db_name} • {version_info}",
            )

        except pyodbc.Error as e:
            return False, f"SQL Server connection failed: {str(e)}"

    def _on_test_complete(self, success: bool, info: str) -> None:
        """Handle connection test completion"""
        self.test_btn.config(state="normal", text="🔌 Test Connection")
        self.is_connected = success
        self._update_connection_status(success, info)

        if success:
            messagebox.showinfo("Connection Successful", info)
            # Refresh databases for SQL Server
            if self.db_type.get() == "sqlserver":
                self._refresh_databases()
        else:
            messagebox.showerror("Connection Failed", info)

        self._notify_change()

    def _on_test_error(self, error_msg: str) -> None:
        """Handle connection test error"""
        self.test_btn.config(state="normal", text="🔌 Test Connection")
        self.is_connected = False
        self._update_connection_status(False, error_msg)
        messagebox.showerror("Connection Error", error_msg)

    def _update_connection_status(self, connected: bool, info: str = "") -> None:
        """Update connection status display"""
        if connected:
            self.connection_status.config(text="● Connected", foreground="green")
            self.info_label.config(text=info)
        else:
            self.connection_status.config(text="● Not Connected", foreground="red")
            self.info_label.config(text=info if info else "")

    def _notify_change(self) -> None:
        """Notify parent of changes"""
        if self.callback:
            self.callback(
                "db_changed",
                {
                    "type": self.db_type.get(),
                    "connected": self.is_connected,
                    "info": self.get_connection_info(),
                },
            )

    def get_config(self):
        """Get database configuration"""
        from config.settings import DatabaseConfig

        config = DatabaseConfig()

        if self.db_type.get() == "sqlserver":
            config.server = self.sql_server.get()
            config.database = self.sql_database.get()
            config.username = self.sql_username.get()
            config.password = self.sql_password.get()
            config.use_windows_auth = self.sql_windows_auth.get()
        else:
            config.sqlite_file = self.sqlite_file.get()

        return config

    def get_connection_info(self) -> Dict[str, Any]:
        """Get current connection information"""
        return {
            "type": self.db_type.get(),
            "connected": self.is_connected,
            "server": (
                self.sql_server.get() if self.db_type.get() == "sqlserver" else None
            ),
            "database": (
                self.sql_database.get()
                if self.db_type.get() == "sqlserver"
                else self.sqlite_file.get()
            ),
            "auth_method": (
                "Windows"
                if self.sql_windows_auth.get()
                else "SQL Server" if self.db_type.get() == "sqlserver" else "File"
            ),
        }

    def validate(self) -> bool:
        """Validate database configuration"""
        db_type = self.db_type.get()

        if db_type == "sqlserver":
            if not self.sql_server.get():
                messagebox.showerror(
                    "Validation Error", "Please specify SQL Server name"
                )
                return False
            if not self.sql_database.get():
                messagebox.showerror("Validation Error", "Please select a database")
                return False
            if not self.sql_windows_auth.get() and not self.sql_username.get():
                messagebox.showerror(
                    "Validation Error",
                    "Please specify username for SQL Server authentication",
                )
                return False
        else:
            if not self.sqlite_file.get():
                messagebox.showerror(
                    "Validation Error", "Please specify SQLite database file"
                )
                return False

        if not self.is_connected:
            result = messagebox.askyesno(
                "Connection Warning", "Database connection not tested. Continue anyway?"
            )
            return result

        return True


class ServerSelectionDialog:
    """Dialog for selecting discovered SQL Server instances"""

    def __init__(self, parent, servers: List[str], callback: Callable[[str], None]):
        self.callback = callback
        self.selected_server = None

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Select SQL Server Instance")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()

        # Center dialog
        self.dialog.transient(parent.winfo_toplevel())

        self._create_widgets(servers)

    def _create_widgets(self, servers: List[str]) -> None:
        """Create dialog widgets"""
        # Title
        title_label = ttk.Label(
            self.dialog,
            text="🔍 Discovered SQL Server Instances",
            font=("Segoe UI", 12, "bold"),
        )
        title_label.pack(pady=10)

        # Server list
        list_frame = ttk.Frame(self.dialog)
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.server_listbox = tk.Listbox(list_frame, font=("Segoe UI", 10))
        self.server_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            list_frame, orient="vertical", command=self.server_listbox.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.server_listbox.configure(yscrollcommand=scrollbar.set)

        # Populate list
        for server in servers:
            self.server_listbox.insert(tk.END, server)

        # Buttons
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(fill="x", padx=20, pady=10)

        ttk.Button(button_frame, text="Select", command=self._on_select).pack(
            side="right", padx=5
        )
        ttk.Button(button_frame, text="Cancel", command=self._on_cancel).pack(
            side="right"
        )

        # Bind double-click
        self.server_listbox.bind("<Double-Button-1>", lambda e: self._on_select())

    def _on_select(self) -> None:
        """Handle server selection"""
        selection = self.server_listbox.curselection()
        if selection:
            server = self.server_listbox.get(selection[0])
            self.callback(server)
            self.dialog.destroy()

    def _on_cancel(self) -> None:
        """Handle cancel"""
        self.dialog.destroy()
