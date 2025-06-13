"""
gui/main_window.py - Complete Main Window with Authentication System
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import logging
import sqlite3
import hashlib
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, Callable
import pandas as pd

# Import core modules
try:
    from config.settings import get_config, DatabaseConfig
    from core.database_manager import DatabaseManager
    from core.data_processor import DataProcessor
    from core.excel_handler import ExcelHandler
    from core.mock_generator import MockDataTemplates
    from utils.logger import setup_gui_logger
    from utils.settings_manager import SettingsManager
except ImportError as e:
    print(f"Import error: {e}")

logger = logging.getLogger(__name__)


class AuthenticationManager:
    """ระบบจัดการการ Login และสิทธิ์การใช้งาน"""

    def __init__(self):
        self.auth_db = Path("auth.db")
        self.current_user = None
        self.session_start = None
        self.session_timeout = 3600  # 1 hour
        self._init_auth_db()

    def _init_auth_db(self):
        """สร้างฐานข้อมูลผู้ใช้"""
        try:
            with sqlite3.connect(self.auth_db) as conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        role TEXT DEFAULT 'user',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_login TIMESTAMP,
                        is_active BOOLEAN DEFAULT 1
                    )
                """
                )

                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS permissions (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        db_type TEXT,
                        can_read BOOLEAN DEFAULT 1,
                        can_write BOOLEAN DEFAULT 0,
                        can_delete BOOLEAN DEFAULT 0,
                        can_admin BOOLEAN DEFAULT 0,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                """
                )

                # สร้าง admin user เริ่มต้น
                self._create_default_admin()

        except Exception as e:
            logger.error(f"Failed to initialize auth database: {e}")

    def _create_default_admin(self):
        """สร้าง admin user เริ่มต้น"""
        try:
            with sqlite3.connect(self.auth_db) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")

                if cursor.fetchone()[0] == 0:
                    # สร้าง admin เริ่มต้น
                    admin_password = self._hash_password("admin123")
                    cursor.execute(
                        """
                        INSERT INTO users (username, password_hash, role)
                        VALUES (?, ?, ?)
                    """,
                        ("admin", admin_password, "admin"),
                    )

                    user_id = cursor.lastrowid

                    # ให้สิทธิ์เต็ม
                    for db_type in ["sqlite", "sqlserver"]:
                        cursor.execute(
                            """
                            INSERT INTO permissions (user_id, db_type, can_read, can_write, can_delete, can_admin)
                            VALUES (?, ?, 1, 1, 1, 1)
                        """,
                            (user_id, db_type),
                        )

                    logger.info("Default admin user created (admin/admin123)")

        except Exception as e:
            logger.error(f"Failed to create default admin: {e}")

    def _hash_password(self, password: str) -> str:
        """Hash password"""
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate(self, username: str, password: str) -> tuple[bool, str]:
        """ตรวจสอบการ Login"""
        try:
            with sqlite3.connect(self.auth_db) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT id, username, password_hash, role, is_active 
                    FROM users WHERE username = ?
                """,
                    (username,),
                )

                user = cursor.fetchone()

                if not user:
                    return False, "ไม่พบผู้ใช้งาน"

                user_id, username, stored_hash, role, is_active = user

                if not is_active:
                    return False, "บัญชีถูกระงับ"

                if stored_hash != self._hash_password(password):
                    return False, "รหัสผ่านไม่ถูกต้อง"

                # อัพเดท last login
                cursor.execute(
                    """
                    UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
                """,
                    (user_id,),
                )

                self.current_user = {"id": user_id, "username": username, "role": role}
                self.session_start = datetime.now()

                return True, f"เข้าสู่ระบบสำเร็จ - {role}"

        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return False, f"ข้อผิดพลาดระบบ: {e}"

    def check_permission(self, db_type: str, action: str) -> bool:
        """ตรวจสอบสิทธิ์การใช้งาน"""
        if not self.current_user:
            return False

        if self.current_user["role"] == "admin":
            return True

        try:
            with sqlite3.connect(self.auth_db) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT can_read, can_write, can_delete, can_admin
                    FROM permissions 
                    WHERE user_id = ? AND db_type = ?
                """,
                    (self.current_user["id"], db_type),
                )

                perms = cursor.fetchone()
                if not perms:
                    return False

                can_read, can_write, can_delete, can_admin = perms

                permission_map = {
                    "read": can_read,
                    "write": can_write,
                    "delete": can_delete,
                    "admin": can_admin,
                }

                return permission_map.get(action, False)

        except Exception as e:
            logger.error(f"Permission check error: {e}")
            return False

    def is_session_valid(self) -> bool:
        """ตรวจสอบว่า session ยังใช้งานได้หรือไม่"""
        if not self.current_user or not self.session_start:
            return False

        return (datetime.now() - self.session_start).seconds < self.session_timeout

    def logout(self):
        """ออกจากระบบ"""
        self.current_user = None
        self.session_start = None


class LoginDialog:
    """หน้าต่าง Login"""

    def __init__(self, parent, auth_manager: AuthenticationManager):
        self.auth_manager = auth_manager
        self.success = False
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("🔐 DENSO888 - เข้าสู่ระบบ")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()

        # Center dialog
        self.dialog.transient(parent)
        self._center_window()

        self._create_widgets()

    def _center_window(self):
        """จัดให้หน้าต่างอยู่กลางจอ"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (300 // 2)
        self.dialog.geometry(f"400x300+{x}+{y}")

    def _create_widgets(self):
        """สร้าง UI"""
        # Header
        header_frame = ttk.Frame(self.dialog)
        header_frame.pack(fill="x", pady=20)

        title_label = ttk.Label(
            header_frame,
            text="🏭 DENSO888",
            font=("Segoe UI", 16, "bold"),
            foreground="#DC0003",
        )
        title_label.pack()

        subtitle_label = ttk.Label(
            header_frame, text="Excel to SQL Management System", font=("Segoe UI", 10)
        )
        subtitle_label.pack()

        # Login Form
        form_frame = ttk.LabelFrame(self.dialog, text="📝 เข้าสู่ระบบ", padding=20)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Username
        ttk.Label(form_frame, text="ชื่อผู้ใช้:").pack(anchor="w", pady=(0, 5))
        self.username_entry = ttk.Entry(form_frame, font=("Segoe UI", 11))
        self.username_entry.pack(fill="x", pady=(0, 10))
        self.username_entry.focus()

        # Password
        ttk.Label(form_frame, text="รหัสผ่าน:").pack(anchor="w", pady=(0, 5))
        self.password_entry = ttk.Entry(form_frame, font=("Segoe UI", 11), show="*")
        self.password_entry.pack(fill="x", pady=(0, 10))

        # Remember checkbox
        self.remember_var = tk.BooleanVar()
        ttk.Checkbutton(
            form_frame, text="จดจำการเข้าสู่ระบบ", variable=self.remember_var
        ).pack(anchor="w", pady=(0, 15))

        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill="x")

        login_btn = ttk.Button(
            button_frame,
            text="🔑 เข้าสู่ระบบ",
            command=self._login,
            style="Accent.TButton",
        )
        login_btn.pack(side="right", padx=(5, 0))

        ttk.Button(button_frame, text="❌ ยกเลิก", command=self._cancel).pack(
            side="right"
        )

        # Default login info
        info_frame = ttk.Frame(self.dialog)
        info_frame.pack(fill="x", padx=20, pady=(0, 10))

        info_label = ttk.Label(
            info_frame,
            text="💡 Default: admin / admin123",
            font=("Segoe UI", 9),
            foreground="gray",
        )
        info_label.pack()

        # Bind Enter key
        self.dialog.bind("<Return>", lambda e: self._login())
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self._login())

        # Set default values
        self.username_entry.insert(0, "admin")

    def _login(self):
        """ดำเนินการ Login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("คำเตือน", "กรุณากรอกชื่อผู้ใช้และรหัสผ่าน")
            return

        success, message = self.auth_manager.authenticate(username, password)

        if success:
            self.success = True
            messagebox.showinfo("สำเร็จ", message)
            self.dialog.destroy()
        else:
            messagebox.showerror("ข้อผิดพลาด", message)
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()

    def _cancel(self):
        """ยกเลิก Login"""
        self.dialog.destroy()


class DatabaseTestDialog:
    """หน้าต่างทดสอบและจัดการฐานข้อมูล"""

    def __init__(self, parent, auth_manager: AuthenticationManager):
        self.auth_manager = auth_manager
        self.db_manager = None

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("🗄️ Database Connection & Permissions")
        self.dialog.geometry("700x500")
        self.dialog.grab_set()
        self.dialog.transient(parent)

        self._create_widgets()
        self._center_window()

    def _center_window(self):
        """จัดให้หน้าต่างอยู่กลางจอ"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (500 // 2)
        self.dialog.geometry(f"700x500+{x}+{y}")

    def _create_widgets(self):
        """สร้าง UI"""
        # Header
        header_frame = ttk.Frame(self.dialog)
        header_frame.pack(fill="x", pady=10, padx=20)

        ttk.Label(
            header_frame,
            text="🗄️ Database Connection & Permission Testing",
            font=("Segoe UI", 14, "bold"),
        ).pack()

        # Notebook for tabs
        notebook = ttk.Notebook(self.dialog)
        notebook.pack(fill="both", expand=True, padx=20, pady=10)

        # SQLite Tab
        sqlite_frame = ttk.Frame(notebook)
        notebook.add(sqlite_frame, text="📁 SQLite")
        self._create_sqlite_tab(sqlite_frame)

        # SQL Server Tab
        sqlserver_frame = ttk.Frame(notebook)
        notebook.add(sqlserver_frame, text="🏢 SQL Server")
        self._create_sqlserver_tab(sqlserver_frame)

        # Permissions Tab
        perms_frame = ttk.Frame(notebook)
        notebook.add(perms_frame, text="🔐 User Permissions")
        self._create_permissions_tab(perms_frame)

        # Close button
        close_frame = ttk.Frame(self.dialog)
        close_frame.pack(fill="x", padx=20, pady=10)

        ttk.Button(close_frame, text="✅ Close", command=self.dialog.destroy).pack(
            side="right"
        )

    def _create_sqlite_tab(self, parent):
        """สร้าง SQLite tab"""
        # Configuration
        config_frame = ttk.LabelFrame(
            parent, text="📁 SQLite Configuration", padding=10
        )
        config_frame.pack(fill="x", pady=10)

        file_frame = ttk.Frame(config_frame)
        file_frame.pack(fill="x")

        ttk.Label(file_frame, text="Database File:").pack(side="left")
        self.sqlite_file_var = tk.StringVar(value="denso888_data.db")
        ttk.Entry(file_frame, textvariable=self.sqlite_file_var, width=40).pack(
            side="left", padx=10, fill="x", expand=True
        )
        ttk.Button(file_frame, text="Browse", command=self._browse_sqlite).pack(
            side="right"
        )

        # Test buttons
        test_frame = ttk.Frame(config_frame)
        test_frame.pack(fill="x", pady=10)

        ttk.Button(
            test_frame,
            text="🔌 Test Connection",
            command=lambda: self._test_db("sqlite"),
        ).pack(side="left", padx=5)
        ttk.Button(
            test_frame, text="🔍 Test CRUD", command=lambda: self._test_crud("sqlite")
        ).pack(side="left", padx=5)

        # Results
        self.sqlite_results = tk.Text(parent, height=15, wrap="word")
        self.sqlite_results.pack(fill="both", expand=True, pady=10)

        scrollbar1 = ttk.Scrollbar(
            parent, orient="vertical", command=self.sqlite_results.yview
        )
        self.sqlite_results.configure(yscrollcommand=scrollbar1.set)

    def _create_sqlserver_tab(self, parent):
        """สร้าง SQL Server tab"""
        # Configuration
        config_frame = ttk.LabelFrame(
            parent, text="🏢 SQL Server Configuration", padding=10
        )
        config_frame.pack(fill="x", pady=10)

        # Server info
        server_row = ttk.Frame(config_frame)
        server_row.pack(fill="x", pady=5)

        ttk.Label(server_row, text="Server:").pack(side="left")
        self.sql_server_var = tk.StringVar(value="localhost")
        ttk.Entry(server_row, textvariable=self.sql_server_var, width=20).pack(
            side="left", padx=10
        )

        ttk.Label(server_row, text="Database:").pack(side="left", padx=(20, 0))
        self.sql_database_var = tk.StringVar(value="excel_to_db")
        ttk.Entry(server_row, textvariable=self.sql_database_var, width=20).pack(
            side="left", padx=10
        )

        # Authentication
        auth_frame = ttk.LabelFrame(config_frame, text="🔐 Authentication", padding=5)
        auth_frame.pack(fill="x", pady=5)

        self.sql_windows_auth = tk.BooleanVar(value=True)
        ttk.Radiobutton(
            auth_frame,
            text="Windows Authentication",
            variable=self.sql_windows_auth,
            value=True,
            command=self._toggle_sql_auth,
        ).pack(anchor="w")
        ttk.Radiobutton(
            auth_frame,
            text="SQL Server Authentication",
            variable=self.sql_windows_auth,
            value=False,
            command=self._toggle_sql_auth,
        ).pack(anchor="w")

        # Credentials
        self.cred_frame = ttk.Frame(auth_frame)
        self.cred_frame.pack(fill="x", pady=5)

        ttk.Label(self.cred_frame, text="Username:").pack(side="left")
        self.sql_username_var = tk.StringVar(value="sa")
        ttk.Entry(self.cred_frame, textvariable=self.sql_username_var, width=15).pack(
            side="left", padx=5
        )

        ttk.Label(self.cred_frame, text="Password:").pack(side="left", padx=(10, 0))
        self.sql_password_var = tk.StringVar()
        ttk.Entry(
            self.cred_frame, textvariable=self.sql_password_var, width=15, show="*"
        ).pack(side="left", padx=5)

        # Test buttons
        test_frame = ttk.Frame(config_frame)
        test_frame.pack(fill="x", pady=10)

        ttk.Button(
            test_frame,
            text="🔌 Test Connection",
            command=lambda: self._test_db("sqlserver"),
        ).pack(side="left", padx=5)
        ttk.Button(
            test_frame,
            text="🔍 Test CRUD",
            command=lambda: self._test_crud("sqlserver"),
        ).pack(side="left", padx=5)
        ttk.Button(
            test_frame, text="📊 List Databases", command=self._list_databases
        ).pack(side="left", padx=5)

        # Results
        self.sqlserver_results = tk.Text(parent, height=15, wrap="word")
        self.sqlserver_results.pack(fill="both", expand=True, pady=10)

        self._toggle_sql_auth()

    def _create_permissions_tab(self, parent):
        """สร้าง Permissions tab"""
        info_frame = ttk.LabelFrame(parent, text="👤 Current User", padding=10)
        info_frame.pack(fill="x", pady=10)

        user_info = f"User: {self.auth_manager.current_user['username']} | Role: {self.auth_manager.current_user['role']}"
        ttk.Label(info_frame, text=user_info, font=("Segoe UI", 10, "bold")).pack()

        # Permission matrix
        perm_frame = ttk.LabelFrame(parent, text="🔐 Database Permissions", padding=10)
        perm_frame.pack(fill="both", expand=True, pady=10)

        # Headers
        headers = ["Database Type", "Read", "Write", "Delete", "Admin"]
        for i, header in enumerate(headers):
            ttk.Label(perm_frame, text=header, font=("Segoe UI", 9, "bold")).grid(
                row=0, column=i, padx=5, pady=5, sticky="w"
            )

        # Permission rows
        db_types = ["sqlite", "sqlserver"]
        for row, db_type in enumerate(db_types, 1):
            ttk.Label(perm_frame, text=db_type.upper()).grid(
                row=row, column=0, padx=5, pady=2, sticky="w"
            )

            for col, action in enumerate(["read", "write", "delete", "admin"], 1):
                has_perm = self.auth_manager.check_permission(db_type, action)
                status = "✅" if has_perm else "❌"
                color = "green" if has_perm else "red"

                label = ttk.Label(perm_frame, text=status, foreground=color)
                label.grid(row=row, column=col, padx=5, pady=2)

    def _browse_sqlite(self):
        """เลือกไฟล์ SQLite"""
        filename = filedialog.askopenfilename(
            defaultextension=".db",
            filetypes=[("SQLite files", "*.db"), ("All files", "*.*")],
        )
        if filename:
            self.sqlite_file_var.set(filename)

    def _toggle_sql_auth(self):
        """เปลี่ยนโหมด Authentication"""
        if self.sql_windows_auth.get():
            for widget in self.cred_frame.winfo_children():
                widget.configure(state="disabled")
        else:
            for widget in self.cred_frame.winfo_children():
                if isinstance(widget, ttk.Entry):
                    widget.configure(state="normal")

    def _test_db(self, db_type: str):
        """ทดสอบการเชื่อมต่อฐานข้อมูล"""
        if not self.auth_manager.check_permission(db_type, "read"):
            messagebox.showerror("ไม่มีสิทธิ์", f"คุณไม่มีสิทธิ์เข้าถึง {db_type.upper()}")
            return

        def test_thread():
            try:
                # Create database config
                config = DatabaseConfig()

                if db_type == "sqlite":
                    config.sqlite_file = self.sqlite_file_var.get()
                else:
                    config.server = self.sql_server_var.get()
                    config.database = self.sql_database_var.get()
                    config.use_windows_auth = self.sql_windows_auth.get()
                    if not config.use_windows_auth:
                        config.username = self.sql_username_var.get()
                        config.password = self.sql_password_var.get()

                # Test connection
                self.db_manager = DatabaseManager(config)

                if db_type == "sqlite":
                    success = self.db_manager.connect(force_mode="sqlite")
                    result_widget = self.sqlite_results
                else:
                    success = self.db_manager.connect(force_mode="sqlserver")
                    result_widget = self.sqlserver_results

                if success:
                    status = self.db_manager.get_status()
                    result_text = f"✅ Connection Successful!\n"
                    result_text += (
                        f"Database Type: {status['active_database'].upper()}\n"
                    )
                    result_text += f"Connection Info: {status.get('sqlserver_info', status.get('sqlite_info', {}))}\n"
                    result_text += (
                        f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                    )
                else:
                    result_text = f"❌ Connection Failed!\n"
                    result_text += (
                        f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                    )

                # Update UI in main thread
                self.dialog.after(
                    0, lambda: self._update_results(result_widget, result_text)
                )

            except Exception as e:
                error_text = f"❌ Connection Error: {str(e)}\n"
                error_text += (
                    f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                )
                self.dialog.after(
                    0, lambda: self._update_results(result_widget, error_text)
                )

        threading.Thread(target=test_thread, daemon=True).start()

    def _test_crud(self, db_type: str):
        """ทดสอบ CRUD operations"""
        permissions_needed = ["read", "write"]
        for perm in permissions_needed:
            if not self.auth_manager.check_permission(db_type, perm):
                messagebox.showerror(
                    "ไม่มีสิทธิ์", f"คุณไม่มีสิทธิ์ {perm} สำหรับ {db_type.upper()}"
                )
                return

        def crud_thread():
            try:
                if not self.db_manager or not self.db_manager.test_connection():
                    self._test_db(db_type)
                    if not self.db_manager or not self.db_manager.test_connection():
                        raise Exception("ไม่สามารถเชื่อมต่อฐานข้อมูลได้")

                result_widget = (
                    self.sqlite_results
                    if db_type == "sqlite"
                    else self.sqlserver_results
                )

                # Test data
                test_data = pd.DataFrame(
                    {
                        "test_id": [1, 2, 3],
                        "test_name": ["Test1", "Test2", "Test3"],
                        "test_value": [100, 200, 300],
                        "created_at": [datetime.now()] * 3,
                    }
                )

                result_text = f"🔍 CRUD Testing for {db_type.upper()}...\n"

                # CREATE
                table_name = f"test_crud_{int(datetime.now().timestamp())}"
                self.db_manager.create_table_from_dataframe(table_name, test_data)
                result_text += f"✅ CREATE: Table '{table_name}' created\n"

                # INSERT
                rows_inserted = self.db_manager.bulk_insert(table_name, test_data)
                result_text += f"✅ INSERT: {rows_inserted} rows inserted\n"

                # READ
                table_info = self.db_manager.get_table_info(table_name)
                result_text += f"✅ READ: Table info retrieved - {table_info.get('row_count', 0)} rows\n"

                # UPDATE (via SQL if user has permission)
                if self.auth_manager.check_permission(db_type, "write"):
                    try:
                        update_sql = f"UPDATE {table_name} SET test_value = test_value * 2 WHERE test_id = 1"
                        self.db_manager.execute_query(update_sql)
                        result_text += f"✅ UPDATE: Record updated\n"
                    except Exception as e:
                        result_text += f"⚠️ UPDATE: {str(e)}\n"

                # DELETE (if user has permission)
                if self.auth_manager.check_permission(db_type, "delete"):
                    try:
                        delete_sql = f"DELETE FROM {table_name} WHERE test_id = 3"
                        self.db_manager.execute_query(delete_sql)
                        result_text += f"✅ DELETE: Record deleted\n"
                    except Exception as e:
                        result_text += f"⚠️ DELETE: {str(e)}\n"
                else:
                    result_text += f"⚠️ DELETE: No permission\n"

                # Cleanup
                if self.auth_manager.check_permission(db_type, "admin"):
                    try:
                        cleanup_sql = f"DROP TABLE {table_name}"
                        self.db_manager.execute_query(cleanup_sql)
                        result_text += f"✅ CLEANUP: Test table dropped\n"
                    except Exception as e:
                        result_text += f"⚠️ CLEANUP: {str(e)}\n"

                result_text += (
                    f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                )

                self.dialog.after(
                    0, lambda: self._update_results(result_widget, result_text)
                )

            except Exception as e:
                error_text = f"❌ CRUD Test Error: {str(e)}\n"
                error_text += (
                    f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                )
                result_widget = (
                    self.sqlite_results
                    if db_type == "sqlite"
                    else self.sqlserver_results
                )
                self.dialog.after(
                    0, lambda: self._update_results(result_widget, error_text)
                )

        threading.Thread(target=crud_thread, daemon=True).start()

    def _list_databases(self):
        """แสดงรายการฐานข้อมูลใน SQL Server"""
        if not self.auth_manager.check_permission("sqlserver", "read"):
            messagebox.showerror("ไม่มีสิทธิ์", "คุณไม่มีสิทธิ์เข้าถึง SQL Server")
            return

        def list_thread():
            try:
                # Test connection first
                if not self.db_manager or self.db_manager.db_type != "sqlserver":
                    self._test_db("sqlserver")

                if not self.db_manager or not self.db_manager.test_connection():
                    raise Exception("ไม่สามารถเชื่อมต่อ SQL Server ได้")

                # Get databases list
                databases_sql = "SELECT name FROM sys.databases ORDER BY name"
                databases = self.db_manager.execute_query(databases_sql)

                result_text = f"📊 Available Databases in SQL Server:\n"
                result_text += f"Server: {self.sql_server_var.get()}\n"
                result_text += "-" * 40 + "\n"

                for db in databases:
                    result_text += f"• {db[0]}\n"

                result_text += f"\nTotal: {len(databases)} databases\n"
                result_text += (
                    f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                )

                self.dialog.after(
                    0, lambda: self._update_results(self.sqlserver_results, result_text)
                )

            except Exception as e:
                error_text = f"❌ List Databases Error: {str(e)}\n"
                error_text += (
                    f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                )
                self.dialog.after(
                    0, lambda: self._update_results(self.sqlserver_results, error_text)
                )

        threading.Thread(target=list_thread, daemon=True).start()

    def _update_results(self, widget, text):
        """อัพเดทผลลัพธ์ใน Text widget"""
        widget.insert(tk.END, text)
        widget.see(tk.END)


class DENSO888MainWindow:
    """หน้าต่างหลักของโปรแกรม DENSO888 พร้อมระบบ Authentication"""

    def __init__(self):
        self.root = tk.Tk()
        self.config = get_config()
        self.settings_manager = SettingsManager()
        self.auth_manager = AuthenticationManager()

        # UI Components
        self.db_manager = None
        self.data_processor = None
        self.current_progress = 0
        self.is_processing = False

        # Setup
        self._setup_window()
        self._setup_logging()
        self._setup_styles()

        # Authentication
        if not self._authenticate():
            self.root.destroy()
            return

        self._create_widgets()
        self._load_settings()

    def _setup_window(self):
        """ตั้งค่าหน้าต่างหลัก"""
        self.root.title(f"🏭 {self.config.app_name} v{self.config.version}")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)

        # Icon
        try:
            # Set window icon if available
            icon_path = Path("assets/icons/app.ico")
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except:
            pass

        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (900 // 2)
        self.root.geometry(f"1400x900+{x}+{y}")

        # Handle close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _setup_logging(self):
        """ตั้งค่า Logging"""
        self.log_messages = []
        setup_gui_logger(self._on_log_message)
        logger.info("DENSO888 Application Started")

    def _setup_styles(self):
        """ตั้งค่า UI Styles"""
        style = ttk.Style()

        # Configure colors
        colors = self.config.ui.theme_colors

        style.configure(
            "Title.TLabel", font=("Segoe UI", 16, "bold"), foreground=colors["primary"]
        )
        style.configure("Heading.TLabel", font=("Segoe UI", 12, "bold"))
        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"))
        style.configure("Success.TButton", foreground=colors["success"])
        style.configure("Danger.TButton", foreground=colors["danger"])

    def _authenticate(self) -> bool:
        """ตรวจสอบการ Login"""
        if not self.config.auth.enable_auth:
            return True

        login_dialog = LoginDialog(self.root, self.auth_manager)
        self.root.wait_window(login_dialog.dialog)

        return login_dialog.success

    def _create_widgets(self):
        """สร้าง UI หลัก"""
        # Header
        self._create_header()

        # Main content
        self._create_main_content()

        # Status bar
        self._create_status_bar()

    def _create_header(self):
        """สร้าง Header"""
        header_frame = ttk.Frame(self.root, style="Header.TFrame")
        header_frame.pack(fill="x", padx=10, pady=5)

        # Title and user info
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(fill="x")

        # App title
        title_label = ttk.Label(
            title_frame, text=f"🏭 {self.config.app_name}", style="Title.TLabel"
        )
        title_label.pack(side="left")

        # User info and logout
        user_frame = ttk.Frame(title_frame)
        user_frame.pack(side="right")

        user_info = f"👤 {self.auth_manager.current_user['username']} ({self.auth_manager.current_user['role']})"
        ttk.Label(user_frame, text=user_info).pack(side="left", padx=10)

        ttk.Button(
            user_frame, text="🔐 DB Test", command=self._open_db_test, width=12
        ).pack(side="left", padx=5)

        ttk.Button(user_frame, text="🚪 Logout", command=self._logout, width=10).pack(
            side="left", padx=5
        )

        # Separator
        ttk.Separator(header_frame, orient="horizontal").pack(fill="x", pady=5)

    def _create_main_content(self):
        """สร้างเนื้อหาหลัก"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Left panel (Configuration)
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side="left", fill="y", padx=(0, 10))

        self._create_data_source_config(left_frame)
        self._create_database_config(left_frame)
        self._create_process_controls(left_frame)

        # Right panel (Results & Logs)
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True)

        self._create_results_panel(right_frame)

    def _create_data_source_config(self, parent):
        """สร้างการกำหนดค่าแหล่งข้อมูล"""
        data_frame = ttk.LabelFrame(parent, text="📊 Data Source", padding=10)
        data_frame.pack(fill="x", pady=(0, 10))

        # Data source type
        self.data_source_type = tk.StringVar(value="mock")

        ttk.Radiobutton(
            data_frame,
            text="🎲 Generate Mock Data",
            variable=self.data_source_type,
            value="mock",
            command=self._on_data_source_change,
        ).pack(anchor="w")

        ttk.Radiobutton(
            data_frame,
            text="📁 Import Excel File",
            variable=self.data_source_type,
            value="excel",
            command=self._on_data_source_change,
        ).pack(anchor="w", pady=(5, 10))

        # Mock data options
        self.mock_frame = ttk.LabelFrame(
            data_frame, text="🎲 Mock Data Settings", padding=5
        )
        self.mock_frame.pack(fill="x", pady=5)

        # Template selection
        template_row = ttk.Frame(self.mock_frame)
        template_row.pack(fill="x", pady=2)

        ttk.Label(template_row, text="Template:").pack(side="left")
        self.mock_template = ttk.Combobox(
            template_row,
            values=["employees", "sales", "inventory", "financial"],
            state="readonly",
            width=15,
        )
        self.mock_template.set("employees")
        self.mock_template.pack(side="left", padx=10)

        # Rows count
        rows_row = ttk.Frame(self.mock_frame)
        rows_row.pack(fill="x", pady=2)

        ttk.Label(rows_row, text="Rows:").pack(side="left")
        self.mock_rows = tk.StringVar(value="1000")
        rows_spinbox = ttk.Spinbox(
            rows_row,
            from_=100,
            to=50000,
            increment=100,
            textvariable=self.mock_rows,
            width=10,
        )
        rows_spinbox.pack(side="left", padx=10)

        # Excel file options
        self.excel_frame = ttk.LabelFrame(
            data_frame, text="📁 Excel File Settings", padding=5
        )

        file_row = ttk.Frame(self.excel_frame)
        file_row.pack(fill="x", pady=2)

        self.excel_file = tk.StringVar()
        ttk.Entry(file_row, textvariable=self.excel_file, width=30).pack(
            side="left", fill="x", expand=True
        )
        ttk.Button(
            file_row, text="Browse", command=self._browse_excel_file, width=8
        ).pack(side="right", padx=(5, 0))

        # Sheet selection
        sheet_row = ttk.Frame(self.excel_frame)
        sheet_row.pack(fill="x", pady=2)

        ttk.Label(sheet_row, text="Sheet:").pack(side="left")
        self.excel_sheet = ttk.Combobox(sheet_row, state="readonly", width=20)
        self.excel_sheet.pack(side="left", padx=10)

        self._on_data_source_change()

    def _create_database_config(self, parent):
        """สร้างการกำหนดค่าฐานข้อมูล"""
        db_frame = ttk.LabelFrame(parent, text="🗄️ Database Configuration", padding=10)
        db_frame.pack(fill="x", pady=(0, 10))

        # Database type
        self.db_type = tk.StringVar(value="sqlite")

        ttk.Radiobutton(
            db_frame,
            text="📁 SQLite (Local)",
            variable=self.db_type,
            value="sqlite",
            command=self._on_db_type_change,
        ).pack(anchor="w")

        ttk.Radiobutton(
            db_frame,
            text="🏢 SQL Server",
            variable=self.db_type,
            value="sqlserver",
            command=self._on_db_type_change,
        ).pack(anchor="w", pady=(5, 10))

        # SQLite settings
        self.sqlite_frame = ttk.LabelFrame(
            db_frame, text="📁 SQLite Settings", padding=5
        )
        self.sqlite_frame.pack(fill="x", pady=5)

        sqlite_row = ttk.Frame(self.sqlite_frame)
        sqlite_row.pack(fill="x")

        self.sqlite_file = tk.StringVar(value="denso888_data.db")
        ttk.Entry(sqlite_row, textvariable=self.sqlite_file, width=25).pack(
            side="left", fill="x", expand=True
        )
        ttk.Button(
            sqlite_row, text="...", command=self._browse_sqlite_file, width=3
        ).pack(side="right")

        # SQL Server settings
        self.sqlserver_frame = ttk.LabelFrame(
            db_frame, text="🏢 SQL Server Settings", padding=5
        )

        # Server
        server_row = ttk.Frame(self.sqlserver_frame)
        server_row.pack(fill="x", pady=2)

        ttk.Label(server_row, text="Server:").grid(row=0, column=0, sticky="w")
        self.sql_server = tk.StringVar(value="localhost")
        ttk.Entry(server_row, textvariable=self.sql_server, width=20).grid(
            row=0, column=1, padx=5, sticky="ew"
        )

        # Database
        ttk.Label(server_row, text="Database:").grid(
            row=1, column=0, sticky="w", pady=(5, 0)
        )
        self.sql_database = tk.StringVar(value="excel_to_db")
        ttk.Entry(server_row, textvariable=self.sql_database, width=20).grid(
            row=1, column=1, padx=5, pady=(5, 0), sticky="ew"
        )

        server_row.columnconfigure(1, weight=1)

        # Authentication
        auth_row = ttk.Frame(self.sqlserver_frame)
        auth_row.pack(fill="x", pady=5)

        self.sql_windows_auth = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            auth_row,
            text="Use Windows Authentication",
            variable=self.sql_windows_auth,
            command=self._on_sql_auth_change,
        ).pack(anchor="w")

        # Credentials
        self.cred_frame = ttk.Frame(self.sqlserver_frame)
        self.cred_frame.pack(fill="x", pady=2)

        cred_grid = ttk.Frame(self.cred_frame)
        cred_grid.pack(fill="x")

        ttk.Label(cred_grid, text="Username:").grid(row=0, column=0, sticky="w")
        self.sql_username = tk.StringVar(value="sa")
        ttk.Entry(cred_grid, textvariable=self.sql_username, width=15).grid(
            row=0, column=1, padx=5, sticky="ew"
        )

        ttk.Label(cred_grid, text="Password:").grid(
            row=1, column=0, sticky="w", pady=(5, 0)
        )
        self.sql_password = tk.StringVar()
        ttk.Entry(cred_grid, textvariable=self.sql_password, width=15, show="*").grid(
            row=1, column=1, padx=5, pady=(5, 0), sticky="ew"
        )

        cred_grid.columnconfigure(1, weight=1)

        # Table name
        table_row = ttk.Frame(db_frame)
        table_row.pack(fill="x", pady=5)

        ttk.Label(table_row, text="Table Name:").pack(side="left")
        self.table_name = tk.StringVar(value="imported_data")
        ttk.Entry(table_row, textvariable=self.table_name, width=20).pack(
            side="left", padx=10, fill="x", expand=True
        )

        self._on_db_type_change()
        self._on_sql_auth_change()

    def _create_process_controls(self, parent):
        """สร้างปุ่มควบคุมการประมวลผล"""
        control_frame = ttk.LabelFrame(parent, text="⚙️ Process Control", padding=10)
        control_frame.pack(fill="x", pady=(0, 10))

        # Process button
        self.process_btn = ttk.Button(
            control_frame,
            text="🚀 Start Processing",
            command=self._start_processing,
            style="Primary.TButton",
        )
        self.process_btn.pack(fill="x", pady=2)

        # Stop button
        self.stop_btn = ttk.Button(
            control_frame,
            text="⏹️ Stop Processing",
            command=self._stop_processing,
            state="disabled",
        )
        self.stop_btn.pack(fill="x", pady=2)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            control_frame, variable=self.progress_var, maximum=100, mode="determinate"
        )
        self.progress_bar.pack(fill="x", pady=5)

        # Progress label
        self.progress_label = ttk.Label(control_frame, text="Ready")
        self.progress_label.pack(fill="x")

    def _create_results_panel(self, parent):
        """สร้างแผงแสดงผลลัพธ์"""
        # Notebook for tabs
        notebook = ttk.Notebook(parent)
        notebook.pack(fill="both", expand=True)

        # Results tab
        results_frame = ttk.Frame(notebook)
        notebook.add(results_frame, text="📊 Results")

        # Results text with scrollbar
        results_text_frame = ttk.Frame(results_frame)
        results_text_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.results_text = tk.Text(
            results_text_frame, wrap="word", font=("Consolas", 10), bg="#f8f9fa"
        )
        self.results_text.pack(side="left", fill="both", expand=True)

        results_scrollbar = ttk.Scrollbar(
            results_text_frame, orient="vertical", command=self.results_text.yview
        )
        results_scrollbar.pack(side="right", fill="y")
        self.results_text.configure(yscrollcommand=results_scrollbar.set)

        # Logs tab
        logs_frame = ttk.Frame(notebook)
        notebook.add(logs_frame, text="📋 Logs")

        # Logs text with scrollbar
        logs_text_frame = ttk.Frame(logs_frame)
        logs_text_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.logs_text = tk.Text(
            logs_text_frame,
            wrap="word",
            font=("Consolas", 9),
            bg="#1e1e1e",
            fg="#ffffff",
        )
        self.logs_text.pack(side="left", fill="both", expand=True)

        logs_scrollbar = ttk.Scrollbar(
            logs_text_frame, orient="vertical", command=self.logs_text.yview
        )
        logs_scrollbar.pack(side="right", fill="y")
        self.logs_text.configure(yscrollcommand=logs_scrollbar.set)

        # Clear logs button
        clear_frame = ttk.Frame(logs_frame)
        clear_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(clear_frame, text="🗑️ Clear Logs", command=self._clear_logs).pack(
            side="right"
        )

    def _create_status_bar(self):
        """สร้าง Status Bar"""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill="x", side="bottom")

        ttk.Separator(status_frame, orient="horizontal").pack(fill="x")

        status_content = ttk.Frame(status_frame)
        status_content.pack(fill="x", padx=10, pady=2)

        # Status label
        self.status_label = ttk.Label(status_content, text="Ready")
        self.status_label.pack(side="left")

        # Version info
        version_label = ttk.Label(
            status_content, text=f"v{self.config.version} by {self.config.author}"
        )
        version_label.pack(side="right")

    # Event handlers
    def _on_data_source_change(self):
        """จัดการการเปลี่ยนแหล่งข้อมูล"""
        if self.data_source_type.get() == "mock":
            self.mock_frame.pack(fill="x", pady=5)
            self.excel_frame.pack_forget()
        else:
            self.mock_frame.pack_forget()
            self.excel_frame.pack(fill="x", pady=5)

    def _on_db_type_change(self):
        """จัดการการเปลี่ยนประเภทฐานข้อมูล"""
        if self.db_type.get() == "sqlite":
            self.sqlite_frame.pack(fill="x", pady=5)
            self.sqlserver_frame.pack_forget()
        else:
            self.sqlite_frame.pack_forget()
            self.sqlserver_frame.pack(fill="x", pady=5)

    def _on_sql_auth_change(self):
        """จัดการการเปลี่ยนวิธี Authentication"""
        if self.sql_windows_auth.get():
            for widget in self.cred_frame.winfo_children():
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Entry):
                        child.configure(state="disabled")
        else:
            for widget in self.cred_frame.winfo_children():
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Entry):
                        child.configure(state="normal")

    def _browse_excel_file(self):
        """เลือกไฟล์ Excel"""
        filename = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")],
        )
        if filename:
            self.excel_file.set(filename)
            self._load_excel_sheets()

    def _load_excel_sheets(self):
        """โหลดรายการ Sheet ใน Excel"""
        try:
            excel_handler = ExcelHandler()
            sheets = excel_handler.get_sheets(self.excel_file.get())
            self.excel_sheet["values"] = sheets
            if sheets:
                self.excel_sheet.set(sheets[0])
        except Exception as e:
            logger.error(f"Failed to load Excel sheets: {e}")
            messagebox.showerror("Error", f"ไม่สามารถโหลด Excel sheets ได้: {e}")

    def _browse_sqlite_file(self):
        """เลือกไฟล์ SQLite"""
        filename = filedialog.asksaveasfilename(
            title="Select SQLite Database File",
            defaultextension=".db",
            filetypes=[("SQLite files", "*.db"), ("All files", "*.*")],
        )
        if filename:
            self.sqlite_file.set(filename)

    def _open_db_test(self):
        """เปิดหน้าต่างทดสอบฐานข้อมูล"""
        DatabaseTestDialog(self.root, self.auth_manager)

    def _logout(self):
        """ออกจากระบบ"""
        if messagebox.askyesno("Confirm Logout", "ต้องการออกจากระบบหรือไม่?"):
            self.auth_manager.logout()
            self.root.quit()

    def _start_processing(self):
        """เริ่มการประมวลผลข้อมูล"""
        if self.is_processing:
            return

        # Validate inputs
        if not self._validate_inputs():
            return

        # Check permissions
        db_type = self.db_type.get()
        if not self.auth_manager.check_permission(db_type, "write"):
            messagebox.showerror("ไม่มีสิทธิ์", f"คุณไม่มีสิทธิ์เขียนข้อมูลใน {db_type.upper()}")
            return

        self.is_processing = True
        self.process_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")

        # Clear results
        self.results_text.delete(1.0, tk.END)

        # Start processing in background thread
        threading.Thread(target=self._process_data, daemon=True).start()

    def _stop_processing(self):
        """หยุดการประมวลผล"""
        if self.data_processor:
            self.data_processor.stop()

        self.is_processing = False
        self.process_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.progress_label.configure(text="Stopped")

        self._log_result("⏹️ การประมวลผลถูกหยุด\n", "warning")

    def _process_data(self):
        """ประมวลผลข้อมูลในเบื้องหลัง"""
        try:
            # Prepare data source configuration
            data_source_config = self._get_data_source_config()

            # Prepare database configuration
            database_config = self._get_database_config()

            # Create data processor
            self.data_processor = DataProcessor(
                data_source_config, database_config, self.config.processing
            )

            # Start processing
            result = self.data_processor.process(
                progress_callback=self._on_progress_update,
                log_callback=self._on_log_message,
            )

            # Show results
            self.root.after(0, lambda: self._show_results(result))

        except Exception as e:
            error_msg = f"ข้อผิดพลาดในการประมวลผล: {str(e)}"
            logger.error(error_msg, exc_info=True)
            self.root.after(0, lambda: self._show_error(error_msg))

        finally:
            self.root.after(0, self._processing_finished)

    def _validate_inputs(self) -> bool:
        """ตรวจสอบข้อมูลที่กรอก"""
        # Check data source
        if self.data_source_type.get() == "excel":
            if not self.excel_file.get():
                messagebox.showerror("ข้อผิดพลาด", "กรุณาเลือกไฟล์ Excel")
                return False

            if not Path(self.excel_file.get()).exists():
                messagebox.showerror("ข้อผิดพลาด", "ไม่พบไฟล์ Excel ที่ระบุ")
                return False

        # Check database configuration
        if self.db_type.get() == "sqlserver":
            if not self.sql_server.get():
                messagebox.showerror("ข้อผิดพลาด", "กรุณาระบุชื่อ SQL Server")
                return False

            if not self.sql_database.get():
                messagebox.showerror("ข้อผิดพลาด", "กรุณาระบุชื่อฐานข้อมูล")
                return False

            if not self.sql_windows_auth.get():
                if not self.sql_username.get():
                    messagebox.showerror("ข้อผิดพลาด", "กรุณาระบุชื่อผู้ใช้")
                    return False
        else:
            if not self.sqlite_file.get():
                messagebox.showerror("ข้อผิดพลาด", "กรุณาระบุไฟล์ SQLite")
                return False

        # Check table name
        if not self.table_name.get():
            messagebox.showerror("ข้อผิดพลาด", "กรุณาระบุชื่อตาราง")
            return False

        return True

    def _get_data_source_config(self) -> Dict[str, Any]:
        """สร้าง configuration สำหรับแหล่งข้อมูล"""
        if self.data_source_type.get() == "mock":
            return {
                "type": "mock",
                "template": self.mock_template.get(),
                "rows": int(self.mock_rows.get()),
                "table_name": self.table_name.get(),
            }
        else:
            return {
                "type": "excel",
                "file_path": self.excel_file.get(),
                "sheet_name": (
                    self.excel_sheet.get() if self.excel_sheet.get() else None
                ),
                "table_name": self.table_name.get(),
            }

    def _get_database_config(self) -> DatabaseConfig:
        """สร้าง configuration สำหรับฐานข้อมูล"""
        config = DatabaseConfig()

        if self.db_type.get() == "sqlserver":
            config.server = self.sql_server.get()
            config.database = self.sql_database.get()
            config.use_windows_auth = self.sql_windows_auth.get()

            if not config.use_windows_auth:
                config.username = self.sql_username.get()
                config.password = self.sql_password.get()
        else:
            config.sqlite_file = self.sqlite_file.get()

        return config

    def _on_progress_update(self, progress_data: Dict[str, Any]):
        """อัพเดทความคืบหน้า"""
        progress = progress_data.get("progress", 0)
        message = progress_data.get("message", "Processing...")

        self.progress_var.set(progress)
        self.progress_label.configure(text=message)
        self.status_label.configure(text=message)

    def _on_log_message(self, message: str, level: str = "info"):
        """จัดการข้อความ log"""
        self.log_messages.append((datetime.now(), level, message))

        # Format log entry
        timestamp = datetime.now().strftime("%H:%M:%S")
        level_icon = {"info": "ℹ️", "warning": "⚠️", "error": "❌", "debug": "🔍"}.get(
            level, "📝"
        )

        log_entry = f"[{timestamp}] {level_icon} {message}\n"

        # Add to logs text
        self.logs_text.insert(tk.END, log_entry)
        self.logs_text.see(tk.END)

        # Keep only last 1000 lines
        lines = self.logs_text.get(1.0, tk.END).split("\n")
        if len(lines) > 1000:
            self.logs_text.delete(1.0, f"{len(lines) - 1000}.0")

    def _show_results(self, result: Dict[str, Any]):
        """แสดงผลลัพธ์การประมวลผล"""
        if result.get("success", False):
            self._log_result("✅ การประมวลผลสำเร็จ!\n", "success")

            # Show summary
            summary = f"""
📊 สรุปผลการประมวลผล
{'='*50}
✅ สถานะ: สำเร็จ
📝 จำนวนแถว: {result.get('rows_processed', 0):,} แถว
⏱️ เวลาที่ใช้: {result.get('duration', 0):.2f} วินาที
🗄️ ตาราง: {result.get('table_name', 'N/A')}
🏢 ฐานข้อมูล: {result.get('database_type', 'N/A').upper()}
⚡ ความเร็ว: {result.get('metrics', {}).get('rows_per_second', 0):.0f} แถว/วินาที

📈 ข้อมูลตาราง:
{self._format_table_info(result.get('table_info', {}))}
"""
            self._log_result(summary, "info")

        else:
            self._log_result("❌ การประมวลผลล้มเหลว!\n", "error")
            error_msg = result.get("error", "Unknown error")
            self._log_result(f"ข้อผิดพลาด: {error_msg}\n", "error")

    def _format_table_info(self, table_info: Dict[str, Any]) -> str:
        """จัดรูปแบบข้อมูลตาราง"""
        if not table_info or "error" in table_info:
            return "ไม่สามารถดึงข้อมูลตารางได้"

        return f"""• ชื่อตาราง: {table_info.get('table_name', 'N/A')}
• จำนวนแถว: {table_info.get('row_count', 0):,}
• จำนวนคอลัมน์: {table_info.get('column_count', 0)}
• ประเภทฐานข้อมูล: {table_info.get('database_type', 'N/A')}"""

    def _show_error(self, error_msg: str):
        """แสดงข้อผิดพลาด"""
        self._log_result(f"❌ ข้อผิดพลาด: {error_msg}\n", "error")
        messagebox.showerror("ข้อผิดพลาด", error_msg)

    def _log_result(self, message: str, level: str = "info"):
        """เพิ่มข้อความในผลลัพธ์"""
        # Color coding
        colors = {
            "success": "#28a745",
            "info": "#000000",
            "warning": "#ffc107",
            "error": "#dc3545",
        }

        # Insert with color
        start_pos = self.results_text.index(tk.END + "-1c")
        self.results_text.insert(tk.END, message)
        end_pos = self.results_text.index(tk.END + "-1c")

        # Apply color tag
        tag_name = f"color_{level}"
        self.results_text.tag_add(tag_name, start_pos, end_pos)
        self.results_text.tag_config(tag_name, foreground=colors.get(level, "#000000"))

        self.results_text.see(tk.END)

    def _processing_finished(self):
        """การประมวลผลเสร็จสิ้น"""
        self.is_processing = False
        self.process_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.progress_var.set(0)
        self.progress_label.configure(text="Ready")
        self.status_label.configure(text="Ready")

    def _clear_logs(self):
        """ล้าง Logs"""
        if messagebox.askyesno("Confirm", "ต้องการล้าง logs หรือไม่?"):
            self.logs_text.delete(1.0, tk.END)
            self.log_messages.clear()
            logger.info("Logs cleared by user")

    def _load_settings(self):
        """โหลดการตั้งค่า"""
        try:
            settings = self.settings_manager.load_settings()

            # Load window geometry
            geometry = settings.get("window", {}).get("geometry", "1400x900")
            self.root.geometry(geometry)

            # Load data source settings
            data_source = settings.get("data_source", {})
            self.data_source_type.set(data_source.get("default_type", "mock"))
            self.mock_template.set(data_source.get("default_template", "employees"))
            self.mock_rows.set(str(data_source.get("default_rows", 1000)))

            # Load database settings
            db_settings = settings.get("database", {})
            self.db_type.set(db_settings.get("default_type", "sqlite"))
            self.sqlite_file.set(db_settings.get("sqlite_file", "denso888_data.db"))

            sql_server_settings = db_settings.get("sql_server", {})
            self.sql_server.set(sql_server_settings.get("host", "localhost"))
            self.sql_database.set(sql_server_settings.get("database", "excel_to_db"))
            self.sql_username.set(sql_server_settings.get("username", "sa"))

            # Update UI
            self._on_data_source_change()
            self._on_db_type_change()
            self._on_sql_auth_change()

        except Exception as e:
            logger.warning(f"Failed to load settings: {e}")

    def _save_settings(self):
        """บันทึกการตั้งค่า"""
        try:
            settings = {
                "window": {
                    "geometry": self.root.geometry(),
                    "maximized": self.root.state() == "zoomed",
                },
                "data_source": {
                    "default_type": self.data_source_type.get(),
                    "default_template": self.mock_template.get(),
                    "default_rows": int(self.mock_rows.get()),
                    "last_excel_directory": (
                        os.path.dirname(self.excel_file.get())
                        if self.excel_file.get()
                        else ""
                    ),
                },
                "database": {
                    "default_type": self.db_type.get(),
                    "sqlite_file": self.sqlite_file.get(),
                    "sql_server": {
                        "host": self.sql_server.get(),
                        "database": self.sql_database.get(),
                        "username": self.sql_username.get(),
                    },
                },
            }

            self.settings_manager.save_settings(settings)

        except Exception as e:
            logger.warning(f"Failed to save settings: {e}")

    def _on_close(self):
        """จัดการการปิดโปรแกรม"""
        try:
            # Save settings
            self._save_settings()

            # Stop any running processes
            if self.is_processing and self.data_processor:
                self.data_processor.stop()

            # Logout
            self.auth_manager.logout()

            # Close database connections
            if self.db_manager:
                self.db_manager.close()

            logger.info("Application closed")

        except Exception as e:
            logger.error(f"Error during shutdown: {e}")

        finally:
            self.root.destroy()

    def run(self):
        """เริ่มการทำงานของโปรแกรม"""
        try:
            logger.info(f"Starting {self.config.app_name} v{self.config.version}")
            logger.info(
                f"User: {self.auth_manager.current_user['username']} ({self.auth_manager.current_user['role']})"
            )

            # Show welcome message
            welcome_msg = f"""
🏭 ยินดีต้อนรับสู่ {self.config.app_name}
{'='*60}
👤 ผู้ใช้: {self.auth_manager.current_user['username']} ({self.auth_manager.current_user['role']})
🔧 เวอร์ชัน: {self.config.version}
👨‍💻 ผู้พัฒนา: {self.config.author}

📋 ฟีเจอร์หลัก:
✅ สร้างข้อมูลจำลอง (Mock Data)
✅ นำเข้าไฟล์ Excel 
✅ รองรับ SQLite และ SQL Server
✅ ระบบตรวจสอบสิทธิ์การใช้งาน
✅ การประมวลผลแบบ Real-time

💡 เริ่มต้นใช้งาน:
1. เลือกแหล่งข้อมูล (Mock Data หรือ Excel)
2. กำหนดค่าฐานข้อมูล
3. กดปุ่ม "🚀 Start Processing"
4. ใช้ "🔐 DB Test" เพื่อทดสอบการเชื่อมต่อ

เริ่มต้นใช้งานได้เลย! 🚀
"""
            self._log_result(welcome_msg, "info")

            # Start main loop
            self.root.mainloop()

        except Exception as e:
            logger.error(f"Fatal error in main loop: {e}", exc_info=True)
            messagebox.showerror("ข้อผิดพลาดร้ายแรง", f"เกิดข้อผิดพลาดร้ายแรง:\n{str(e)}")


# Usage example
if __name__ == "__main__":
    app = DENSO888MainWindow()
    if app.root.winfo_exists():  # Check if window was created successfully
        app.run()
