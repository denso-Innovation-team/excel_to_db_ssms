"""
gui/main_window.py - Fixed Main Window with Enhanced Error Handling
"""

# Fixed tkinter import
try:
    from tkinter_wrapper import tk, ttk, messagebox, filedialog, TKINTER_AVAILABLE
    if not TKINTER_AVAILABLE:
        raise ImportError("Tkinter not available")
except ImportError:
    print("❌ GUI not available - using console mode")
    raise
import threading
import logging
import sqlite3
import hashlib
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any

# Enhanced import handling with fallbacks
try:
    from config.settings import get_config, DatabaseConfig
    from core.database_manager import DatabaseManager
    from core.data_processor import DataProcessor
    from core.excel_handler import ExcelHandler
    from core.mock_generator import MockDataTemplates
    from utils.logger import setup_gui_logger
except ImportError as e:
    print(f"⚠️ Import warning: {e}")
    print("💡 Some features may not work correctly")

# Fallback imports with error handling
try:
    from utils.settings_manager import SettingsManager
except ImportError:
    print("⚠️ SettingsManager not found, using fallback")

    class SettingsManager:
        def load_settings(self):
            return {"window": {"geometry": "1400x900"}}

        def save_settings(self, settings):
            return True


logger = logging.getLogger(__name__)


class AuthenticationManager:
    """Enhanced authentication with better security"""

    def __init__(self):
        self.auth_db = Path("auth.db")
        self.current_user = None
        self.session_start = None
        self.session_timeout = 3600  # 1 hour
        self._init_auth_db()

    def _init_auth_db(self):
        """Initialize authentication database with enhanced schema"""
        try:
            with sqlite3.connect(self.auth_db) as conn:
                # Users table with additional fields
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        salt TEXT NOT NULL,
                        role TEXT DEFAULT 'user',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_login TIMESTAMP,
                        failed_attempts INTEGER DEFAULT 0,
                        locked_until TIMESTAMP,
                        is_active BOOLEAN DEFAULT 1
                    )
                """
                )

                # Enhanced permissions table
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
                        max_rows INTEGER DEFAULT 10000,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                """
                )

                # Session tracking
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS sessions (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        session_end TIMESTAMP,
                        ip_address TEXT,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                """
                )

                self._create_default_admin()

        except Exception as e:
            logger.error(f"Failed to initialize auth database: {e}")

    def _create_default_admin(self):
        """Create default admin with enhanced security"""
        try:
            with sqlite3.connect(self.auth_db) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")

                if cursor.fetchone()[0] == 0:
                    # Generate salt and hash password
                    salt = os.urandom(32).hex()
                    password_hash = self._hash_password_with_salt("admin123", salt)

                    cursor.execute(
                        """
                        INSERT INTO users (username, password_hash, salt, role)
                        VALUES (?, ?, ?, ?)
                    """,
                        ("admin", password_hash, salt, "admin"),
                    )

                    user_id = cursor.lastrowid

                    # Give full permissions
                    for db_type in ["sqlite", "sqlserver"]:
                        cursor.execute(
                            """
                            INSERT INTO permissions (user_id, db_type, can_read, can_write, can_delete, can_admin, max_rows)
                            VALUES (?, ?, 1, 1, 1, 1, NULL)
                        """,
                            (user_id, db_type),
                        )

                    logger.info("Default admin user created (admin/admin123)")

        except Exception as e:
            logger.error(f"Failed to create default admin: {e}")

    def _hash_password_with_salt(self, password: str, salt: str) -> str:
        """Enhanced password hashing with salt"""
        return hashlib.pbkdf2_hmac(
            "sha256", password.encode(), bytes.fromhex(salt), 100000
        ).hex()

    def authenticate(self, username: str, password: str) -> tuple[bool, str]:
        """Enhanced authentication with account lockout"""
        try:
            with sqlite3.connect(self.auth_db) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT id, username, password_hash, salt, role, is_active, failed_attempts, locked_until
                    FROM users WHERE username = ?
                """,
                    (username,),
                )

                user = cursor.fetchone()

                if not user:
                    return False, "ไม่พบผู้ใช้งาน"

                (
                    user_id,
                    username,
                    stored_hash,
                    salt,
                    role,
                    is_active,
                    failed_attempts,
                    locked_until,
                ) = user

                # Check if account is locked
                if locked_until:
                    lock_time = datetime.fromisoformat(locked_until)
                    if datetime.now() < lock_time:
                        return False, f"บัญชีถูกล็อค จนถึง {lock_time.strftime('%H:%M:%S')}"

                if not is_active:
                    return False, "บัญชีถูกระงับ"

                # Verify password
                password_hash = self._hash_password_with_salt(password, salt)
                if stored_hash != password_hash:
                    # Increment failed attempts
                    new_failed_attempts = failed_attempts + 1
                    locked_until_time = None

                    if new_failed_attempts >= 3:
                        locked_until_time = (
                            datetime.now() + timedelta(minutes=15)
                        ).isoformat()

                    cursor.execute(
                        """
                        UPDATE users SET failed_attempts = ?, locked_until = ? WHERE id = ?
                    """,
                        (new_failed_attempts, locked_until_time, user_id),
                    )

                    if locked_until_time:
                        return False, "บัญชีถูกล็อคเนื่องจากล็อกอินผิด 3 ครั้ง (15 นาที)"
                    else:
                        return (
                            False,
                            f"รหัสผ่านไม่ถูกต้อง (เหลือ {3-new_failed_attempts} ครั้ง)",
                        )

                # Reset failed attempts on successful login
                cursor.execute(
                    """
                    UPDATE users SET last_login = CURRENT_TIMESTAMP, failed_attempts = 0, locked_until = NULL 
                    WHERE id = ?
                """,
                    (user_id,),
                )

                # Create session record
                cursor.execute(
                    """
                    INSERT INTO sessions (user_id) VALUES (?)
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
        """Enhanced permission checking"""
        if not self.current_user:
            return False

        if self.current_user["role"] == "admin":
            return True

        try:
            with sqlite3.connect(self.auth_db) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT can_read, can_write, can_delete, can_admin, max_rows
                    FROM permissions 
                    WHERE user_id = ? AND db_type = ?
                """,
                    (self.current_user["id"], db_type),
                )

                perms = cursor.fetchone()
                if not perms:
                    return False

                can_read, can_write, can_delete, can_admin, max_rows = perms

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

    def get_user_restrictions(self, db_type: str) -> Dict[str, Any]:
        """Get user-specific restrictions"""
        if not self.current_user:
            return {"max_rows": 0}

        if self.current_user["role"] == "admin":
            return {"max_rows": None}  # Unlimited

        try:
            with sqlite3.connect(self.auth_db) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT max_rows FROM permissions 
                    WHERE user_id = ? AND db_type = ?
                """,
                    (self.current_user["id"], db_type),
                )

                result = cursor.fetchone()
                return {"max_rows": result[0] if result else 10000}

        except Exception as e:
            logger.error(f"Error getting restrictions: {e}")
            return {"max_rows": 10000}

    def is_session_valid(self) -> bool:
        """Check if session is still valid"""
        if not self.current_user or not self.session_start:
            return False

        return (datetime.now() - self.session_start).seconds < self.session_timeout

    def logout(self):
        """Enhanced logout with session cleanup"""
        if self.current_user:
            try:
                with sqlite3.connect(self.auth_db) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        UPDATE sessions SET session_end = CURRENT_TIMESTAMP 
                        WHERE user_id = ? AND session_end IS NULL
                    """,
                        (self.current_user["id"],),
                    )
            except Exception as e:
                logger.error(f"Error updating session: {e}")

        self.current_user = None
        self.session_start = None


class LoginDialog:
    """Enhanced login dialog with better UX"""

    def __init__(self, parent, auth_manager: AuthenticationManager):
        self.auth_manager = auth_manager
        self.success = False
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("🔐 DENSO888 - เข้าสู่ระบบ")
        self.dialog.geometry("450x350")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()

        # Center dialog
        self.dialog.transient(parent)
        self._center_window()
        self._create_widgets()

    def _center_window(self):
        """Center dialog on screen"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (350 // 2)
        self.dialog.geometry(f"450x350+{x}+{y}")

    def _create_widgets(self):
        """Create enhanced UI"""
        # Header with better styling
        header_frame = ttk.Frame(self.dialog)
        header_frame.pack(fill="x", pady=20)

        title_label = ttk.Label(
            header_frame, text="🏭 DENSO888", font=("Segoe UI", 18, "bold")
        )
        title_label.pack()

        subtitle_label = ttk.Label(
            header_frame, text="Excel to SQL Management System", font=("Segoe UI", 10)
        )
        subtitle_label.pack()

        version_label = ttk.Label(
            header_frame,
            text="v2.0.0 - Enhanced Security",
            font=("Segoe UI", 8),
            foreground="gray",
        )
        version_label.pack()

        # Login Form with better layout
        form_frame = ttk.LabelFrame(self.dialog, text="📝 เข้าสู่ระบบ", padding=20)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Username with icon
        username_frame = ttk.Frame(form_frame)
        username_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(username_frame, text="👤 ชื่อผู้ใช้:").pack(anchor="w", pady=(0, 5))
        self.username_entry = ttk.Entry(username_frame, font=("Segoe UI", 11))
        self.username_entry.pack(fill="x")
        self.username_entry.focus()

        # Password with icon
        password_frame = ttk.Frame(form_frame)
        password_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(password_frame, text="🔒 รหัสผ่าน:").pack(anchor="w", pady=(0, 5))
        self.password_entry = ttk.Entry(password_frame, font=("Segoe UI", 11), show="*")
        self.password_entry.pack(fill="x")

        # Show password checkbox
        self.show_password_var = tk.BooleanVar()
        show_password_cb = ttk.Checkbutton(
            form_frame,
            text="แสดงรหัสผ่าน",
            variable=self.show_password_var,
            command=self._toggle_password_visibility,
        )
        show_password_cb.pack(anchor="w", pady=(5, 10))

        # Remember login
        self.remember_var = tk.BooleanVar()
        ttk.Checkbutton(
            form_frame, text="จดจำการเข้าสู่ระบบ", variable=self.remember_var
        ).pack(anchor="w", pady=(0, 15))

        # Buttons with better styling
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill="x")

        login_btn = ttk.Button(button_frame, text="🔑 เข้าสู่ระบบ", command=self._login)
        login_btn.pack(side="right", padx=(5, 0))

        cancel_btn = ttk.Button(button_frame, text="❌ ยกเลิก", command=self._cancel)
        cancel_btn.pack(side="right")

        # Info section
        info_frame = ttk.Frame(self.dialog)
        info_frame.pack(fill="x", padx=20, pady=(0, 10))

        info_text = """💡 ข้อมูลล็อกอินเริ่มต้น:
👤 Username: admin
🔒 Password: admin123

🔒 ความปลอดภัย:
• บัญชีจะถูกล็อคหากล็อกอินผิด 3 ครั้ง
• Session timeout: 1 ชั่วโมง"""

        info_label = ttk.Label(
            info_frame,
            text=info_text,
            font=("Segoe UI", 9),
            foreground="gray",
            justify="left",
        )
        info_label.pack(anchor="w")

        # Bind events
        self.dialog.bind("<Return>", lambda e: self._login())
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self._login())

        # Set default values
        self.username_entry.insert(0, "admin")

    def _toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.show_password_var.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

    def _login(self):
        """Enhanced login process"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("คำเตือน", "กรุณากรอกชื่อผู้ใช้และรหัสผ่าน")
            return

        # Disable login button during authentication
        self.dialog.configure(cursor="wait")

        try:
            success, message = self.auth_manager.authenticate(username, password)

            if success:
                self.success = True
                messagebox.showinfo("สำเร็จ", message)
                self.dialog.destroy()
            else:
                messagebox.showerror("ข้อผิดพลาด", message)
                self.password_entry.delete(0, tk.END)
                self.password_entry.focus()

        except Exception as e:
            messagebox.showerror("ข้อผิดพลาด", f"เกิดข้อผิดพลาดในการเข้าสู่ระบบ: {e}")

        finally:
            self.dialog.configure(cursor="")

    def _cancel(self):
        """Cancel login"""
        self.dialog.destroy()


class DENSO888MainWindow:
    """Enhanced main window with better error handling and performance"""

    def __init__(self):
        self.root = tk.Tk()

        # Initialize with fallback handling
        try:
            self.config = get_config()
        except Exception as e:
            logger.warning(f"Config loading failed: {e}, using defaults")
            self.config = self._get_default_config()

        self.settings_manager = SettingsManager()
        self.auth_manager = AuthenticationManager()

        # UI Components
        self.db_manager = None
        self.data_processor = None
        self.current_progress = 0
        self.is_processing = False

        # Setup with error handling
        try:
            self._setup_window()
            self._setup_logging()
            self._setup_styles()

            # Authentication
            if not self._authenticate():
                self.root.destroy()
                return

            self._create_widgets()
            self._load_settings()

        except Exception as e:
            logger.error(f"Initialization error: {e}")
            messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถเริ่มต้นโปรแกรมได้: {e}")
            self.root.destroy()

    def _get_default_config(self):
        """Fallback configuration"""

        class DefaultConfig:
            app_name = "DENSO888 - Excel to SQL"
            version = "2.0.0"
            author = "เฮียตอมจัดหั้ย!!!"

            class ui:
                theme_colors = {
                    "primary": "#DC0003",
                    "secondary": "#F5F5F5",
                    "success": "#28A745",
                    "warning": "#FFC107",
                    "danger": "#DC3545",
                }

            class auth:
                enable_auth = True

            class processing:
                chunk_size = 5000

        return DefaultConfig()

    def _setup_window(self):
        """Enhanced window setup"""
        self.root.title(f"🏭 {self.config.app_name} v{self.config.version}")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)

        # Enhanced styling
        try:
            self.root.tk.call("source", "azure.tcl")
            self.root.tk.call("set_theme", "light")
        except:
            pass  # Fallback to default theme

        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (900 // 2)
        self.root.geometry(f"1400x900+{x}+{y}")

        # Handle close with confirmation
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _setup_logging(self):
        """Setup enhanced logging"""
        self.log_messages = []
        try:
            setup_gui_logger(self._on_log_message)
        except Exception as e:
            print(f"Logging setup failed: {e}")
        logger.info("DENSO888 Application Started")

    def _setup_styles(self):
        """Enhanced UI styling"""
        style = ttk.Style()

        # Enhanced color scheme
        if hasattr(self.config, "ui"):
            colors = self.config.ui.theme_colors
        else:
            colors = {"primary": "#DC0003", "success": "#28A745", "danger": "#DC3545"}

        try:
            style.configure(
                "Title.TLabel",
                font=("Segoe UI", 16, "bold"),
                foreground=colors["primary"],
            )
            style.configure("Heading.TLabel", font=("Segoe UI", 12, "bold"))
            style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"))
            style.configure("Success.TButton", foreground=colors["success"])
            style.configure("Danger.TButton", foreground=colors["danger"])
        except Exception as e:
            logger.warning(f"Style configuration failed: {e}")

    def _authenticate(self) -> bool:
        """Enhanced authentication with better error handling"""
        if not getattr(self.config.auth, "enable_auth", True):
            return True

        try:
            login_dialog = LoginDialog(self.root, self.auth_manager)
            self.root.wait_window(login_dialog.dialog)
            return login_dialog.success
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            messagebox.showerror("ข้อผิดพลาด", f"เกิดข้อผิดพลาดในการตรวจสอบสิทธิ์: {e}")
            return False

    def _create_widgets(self):
        """Create enhanced UI components"""
        try:
            self._create_header()
            self._create_main_content()
            self._create_status_bar()
        except Exception as e:
            logger.error(f"Widget creation error: {e}")
            raise

    def _create_header(self):
        """Enhanced header with user info"""
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill="x", padx=10, pady=5)

        # Title and user info
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(fill="x")

        # App title with enhanced styling
        title_label = ttk.Label(
            title_frame, text=f"🏭 {self.config.app_name}", style="Title.TLabel"
        )
        title_label.pack(side="left")

        # User info and controls
        user_frame = ttk.Frame(title_frame)
        user_frame.pack(side="right")

        # Enhanced user info
        user_info = f"👤 {self.auth_manager.current_user['username']} ({self.auth_manager.current_user['role']})"
        session_time = datetime.now().strftime("%H:%M")
        user_label = ttk.Label(user_frame, text=f"{user_info} | 🕐 {session_time}")
        user_label.pack(side="left", padx=10)

        # Control buttons
        ttk.Button(
            user_frame, text="🔐 DB Test", command=self._open_db_test, width=12
        ).pack(side="left", padx=5)
        ttk.Button(user_frame, text="🚪 Logout", command=self._logout, width=10).pack(
            side="left", padx=5
        )

        # Separator
        ttk.Separator(header_frame, orient="horizontal").pack(fill="x", pady=5)

    def _create_main_content(self):
        """Enhanced main content layout"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Create paned window for resizable layout
        paned_window = ttk.PanedWindow(main_frame, orient="horizontal")
        paned_window.pack(fill="both", expand=True)

        # Left panel (Configuration) - fixed width
        left_frame = ttk.Frame(paned_window)
        paned_window.add(left_frame, weight=0)

        self._create_data_source_config(left_frame)
        self._create_database_config(left_frame)
        self._create_process_controls(left_frame)

        # Right panel (Results & Logs) - expandable
        right_frame = ttk.Frame(paned_window)
        paned_window.add(right_frame, weight=1)

        self._create_results_panel(right_frame)

    def _create_data_source_config(self, parent):
        """Enhanced data source configuration"""
        data_frame = ttk.LabelFrame(
            parent, text="📊 Data Source Configuration", padding=10
        )
        data_frame.pack(fill="x", pady=(0, 10))

        # Data source type with better styling
        self.data_source_type = tk.StringVar(value="mock")

        source_frame = ttk.Frame(data_frame)
        source_frame.pack(fill="x", pady=(0, 10))

        ttk.Radiobutton(
            source_frame,
            text="🎲 Generate Mock Data",
            variable=self.data_source_type,
            value="mock",
            command=self._on_data_source_change,
        ).pack(anchor="w")

        ttk.Radiobutton(
            source_frame,
            text="📁 Import Excel File",
            variable=self.data_source_type,
            value="excel",
            command=self._on_data_source_change,
        ).pack(anchor="w", pady=(5, 0))

        # Mock data options with enhanced UI
        self.mock_frame = ttk.LabelFrame(
            data_frame, text="🎲 Mock Data Settings", padding=5
        )
        self.mock_frame.pack(fill="x", pady=5)

        # Template selection with descriptions
        template_frame = ttk.Frame(self.mock_frame)
        template_frame.pack(fill="x", pady=2)

        ttk.Label(template_frame, text="Template:").pack(side="left")
        self.mock_template = ttk.Combobox(
            template_frame,
            values=["employees", "sales", "inventory", "financial"],
            state="readonly",
            width=15,
        )
        self.mock_template.set("employees")
        self.mock_template.pack(side="left", padx=10)

        # Template description
        self.template_desc = ttk.Label(
            self.mock_frame,
            text="Employee records with HR information",
            font=("Segoe UI", 8),
            foreground="gray",
        )
        self.template_desc.pack(anchor="w", pady=2)

        # Enhanced rows selection
        rows_frame = ttk.Frame(self.mock_frame)
        rows_frame.pack(fill="x", pady=2)

        ttk.Label(rows_frame, text="Rows:").pack(side="left")
        self.mock_rows = tk.StringVar(value="1000")

        # Predefined options
        rows_options = ["100", "500", "1000", "5000", "10000", "25000", "50000"]
        rows_combo = ttk.Combobox(
            rows_frame, textvariable=self.mock_rows, values=rows_options, width=10
        )
        rows_combo.pack(side="left", padx=10)

        # Excel file options with enhanced features
        self.excel_frame = ttk.LabelFrame(
            data_frame, text="📁 Excel File Settings", padding=5
        )

        # File selection with recent files
        file_frame = ttk.Frame(self.excel_frame)
        file_frame.pack(fill="x", pady=2)

        self.excel_file = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.excel_file, width=30)
        file_entry.pack(side="left", fill="x", expand=True)

        ttk.Button(
            file_frame, text="Browse", command=self._browse_excel_file, width=8
        ).pack(side="right", padx=(5, 0))

        # Sheet selection with validation
        sheet_frame = ttk.Frame(self.excel_frame)
        sheet_frame.pack(fill="x", pady=2)

        ttk.Label(sheet_frame, text="Sheet:").pack(side="left")
        self.excel_sheet = ttk.Combobox(sheet_frame, state="readonly", width=20)
        self.excel_sheet.pack(side="left", padx=10)

        # File info display
        self.file_info_label = ttk.Label(
            self.excel_frame, text="", font=("Segoe UI", 8), foreground="gray"
        )
        self.file_info_label.pack(anchor="w", pady=2)

        # Bind template change to update description
        self.mock_template.bind("<<ComboboxSelected>>", self._on_template_change)

        self._on_data_source_change()

    def _on_template_change(self, event=None):
        """Update template description"""
        template_descriptions = {
            "employees": "Employee records with HR information",
            "sales": "Sales transactions and customer data",
            "inventory": "Product inventory and stock levels",
            "financial": "Financial transactions and accounting",
        }
        template = self.mock_template.get()
        desc = template_descriptions.get(template, "")
        self.template_desc.configure(text=desc)

    def _create_database_config(self, parent):
        """Enhanced database configuration"""
        db_frame = ttk.LabelFrame(parent, text="🗄️ Database Configuration", padding=10)
        db_frame.pack(fill="x", pady=(0, 10))

        # Database type with better descriptions
        self.db_type = tk.StringVar(value="sqlite")

        db_type_frame = ttk.Frame(db_frame)
        db_type_frame.pack(fill="x", pady=(0, 10))

        ttk.Radiobutton(
            db_type_frame,
            text="📁 SQLite (Local Database)",
            variable=self.db_type,
            value="sqlite",
            command=self._on_db_type_change,
        ).pack(anchor="w")

        ttk.Radiobutton(
            db_type_frame,
            text="🏢 SQL Server (Enterprise)",
            variable=self.db_type,
            value="sqlserver",
            command=self._on_db_type_change,
        ).pack(anchor="w", pady=(5, 0))

        # SQLite settings with enhanced features
        self.sqlite_frame = ttk.LabelFrame(
            db_frame, text="📁 SQLite Settings", padding=5
        )
        self.sqlite_frame.pack(fill="x", pady=5)

        sqlite_file_frame = ttk.Frame(self.sqlite_frame)
        sqlite_file_frame.pack(fill="x")

        self.sqlite_file = tk.StringVar(value="denso888_data.db")
        ttk.Entry(sqlite_file_frame, textvariable=self.sqlite_file, width=25).pack(
            side="left", fill="x", expand=True
        )
        ttk.Button(
            sqlite_file_frame, text="...", command=self._browse_sqlite_file, width=3
        ).pack(side="right")

        # SQLite info
        sqlite_info = ttk.Label(
            self.sqlite_frame,
            text="✅ No setup required • Works offline • Up to 281 TB",
            font=("Segoe UI", 8),
            foreground="green",
        )
        sqlite_info.pack(anchor="w", pady=2)

        # SQL Server settings with enhanced UI
        self.sqlserver_frame = ttk.LabelFrame(
            db_frame, text="🏢 SQL Server Settings", padding=5
        )

        # Connection grid
        conn_grid = ttk.Frame(self.sqlserver_frame)
        conn_grid.pack(fill="x", pady=5)

        # Server
        ttk.Label(conn_grid, text="Server:").grid(
            row=0, column=0, sticky="w", padx=(0, 5)
        )
        self.sql_server = tk.StringVar(value="localhost")
        ttk.Entry(conn_grid, textvariable=self.sql_server, width=20).grid(
            row=0, column=1, sticky="ew", padx=(0, 10)
        )

        # Database
        ttk.Label(conn_grid, text="Database:").grid(
            row=0, column=2, sticky="w", padx=(0, 5)
        )
        self.sql_database = tk.StringVar(value="excel_to_db")
        ttk.Entry(conn_grid, textvariable=self.sql_database, width=20).grid(
            row=0, column=3, sticky="ew"
        )

        conn_grid.columnconfigure(1, weight=1)
        conn_grid.columnconfigure(3, weight=1)

        # Authentication options
        auth_frame = ttk.LabelFrame(
            self.sqlserver_frame, text="🔐 Authentication", padding=5
        )
        auth_frame.pack(fill="x", pady=5)

        self.sql_windows_auth = tk.BooleanVar(value=True)

        ttk.Radiobutton(
            auth_frame,
            text="🔑 Windows Authentication (Recommended)",
            variable=self.sql_windows_auth,
            value=True,
            command=self._on_sql_auth_change,
        ).pack(anchor="w")

        ttk.Radiobutton(
            auth_frame,
            text="👤 SQL Server Authentication",
            variable=self.sql_windows_auth,
            value=False,
            command=self._on_sql_auth_change,
        ).pack(anchor="w", pady=(5, 0))

        # Credentials frame
        self.cred_frame = ttk.Frame(auth_frame)
        self.cred_frame.pack(fill="x", pady=5)

        cred_grid = ttk.Frame(self.cred_frame)
        cred_grid.pack(fill="x")

        ttk.Label(cred_grid, text="Username:").grid(
            row=0, column=0, sticky="w", padx=(0, 5)
        )
        self.sql_username = tk.StringVar(value="sa")
        ttk.Entry(cred_grid, textvariable=self.sql_username, width=15).grid(
            row=0, column=1, sticky="ew", padx=(0, 10)
        )

        ttk.Label(cred_grid, text="Password:").grid(
            row=0, column=2, sticky="w", padx=(0, 5)
        )
        self.sql_password = tk.StringVar()
        ttk.Entry(cred_grid, textvariable=self.sql_password, width=15, show="*").grid(
            row=0, column=3, sticky="ew"
        )

        cred_grid.columnconfigure(1, weight=1)
        cred_grid.columnconfigure(3, weight=1)

        # Connection test button
        test_frame = ttk.Frame(self.sqlserver_frame)
        test_frame.pack(fill="x", pady=5)

        ttk.Button(
            test_frame, text="🔍 Test Connection", command=self._quick_test_connection
        ).pack(side="left")

        # Table name configuration
        table_frame = ttk.Frame(db_frame)
        table_frame.pack(fill="x", pady=5)

        ttk.Label(table_frame, text="📋 Table Name:").pack(side="left")
        self.table_name = tk.StringVar(value="imported_data")
        ttk.Entry(table_frame, textvariable=self.table_name, width=20).pack(
            side="left", padx=10, fill="x", expand=True
        )

        self._on_db_type_change()
        self._on_sql_auth_change()

    def _create_process_controls(self, parent):
        """Enhanced process controls"""
        control_frame = ttk.LabelFrame(parent, text="⚙️ Process Control", padding=10)
        control_frame.pack(fill="x", pady=(0, 10))

        # Main process button with enhanced styling
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

        # Progress section
        progress_frame = ttk.Frame(control_frame)
        progress_frame.pack(fill="x", pady=5)

        # Progress bar with percentage
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame, variable=self.progress_var, maximum=100, mode="determinate"
        )
        self.progress_bar.pack(fill="x", pady=2)

        # Progress info
        info_frame = ttk.Frame(progress_frame)
        info_frame.pack(fill="x", pady=2)

        self.progress_label = ttk.Label(info_frame, text="Ready")
        self.progress_label.pack(side="left")

        self.progress_percent = ttk.Label(info_frame, text="0%")
        self.progress_percent.pack(side="right")

        # Quick actions
        quick_frame = ttk.LabelFrame(control_frame, text="⚡ Quick Actions", padding=5)
        quick_frame.pack(fill="x", pady=5)

        quick_buttons_frame = ttk.Frame(quick_frame)
        quick_buttons_frame.pack(fill="x")

        ttk.Button(
            quick_buttons_frame,
            text="📊 Sample Data",
            command=self._create_sample_data,
            width=12,
        ).pack(side="left", padx=2)
        ttk.Button(
            quick_buttons_frame,
            text="🗑️ Clear Results",
            command=self._clear_results,
            width=12,
        ).pack(side="left", padx=2)

    def _create_results_panel(self, parent):
        """Enhanced results panel with tabs"""
        # Notebook for organized results
        notebook = ttk.Notebook(parent)
        notebook.pack(fill="both", expand=True)

        # Results tab with enhanced features
        results_frame = ttk.Frame(notebook)
        notebook.add(results_frame, text="📊 Processing Results")

        # Results toolbar
        results_toolbar = ttk.Frame(results_frame)
        results_toolbar.pack(fill="x", padx=5, pady=5)

        ttk.Button(
            results_toolbar, text="💾 Save Results", command=self._save_results
        ).pack(side="left", padx=2)
        ttk.Button(
            results_toolbar, text="📋 Copy to Clipboard", command=self._copy_results
        ).pack(side="left", padx=2)
        ttk.Button(
            results_toolbar, text="🔍 Find in Results", command=self._find_in_results
        ).pack(side="left", padx=2)

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

        # Logs tab with enhanced features
        logs_frame = ttk.Frame(notebook)
        notebook.add(logs_frame, text="📋 System Logs")

        # Logs toolbar
        logs_toolbar = ttk.Frame(logs_frame)
        logs_toolbar.pack(fill="x", padx=5, pady=5)

        # Log level filter
        ttk.Label(logs_toolbar, text="Level:").pack(side="left", padx=2)
        self.log_level_filter = ttk.Combobox(
            logs_toolbar,
            values=["All", "INFO", "WARNING", "ERROR"],
            state="readonly",
            width=10,
        )
        self.log_level_filter.set("All")
        self.log_level_filter.pack(side="left", padx=2)
        self.log_level_filter.bind("<<ComboboxSelected>>", self._filter_logs)

        ttk.Button(logs_toolbar, text="🗑️ Clear Logs", command=self._clear_logs).pack(
            side="right", padx=2
        )
        ttk.Button(logs_toolbar, text="💾 Export Logs", command=self._export_logs).pack(
            side="right", padx=2
        )

        # Logs text with enhanced styling
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

    def _create_status_bar(self):
        """Enhanced status bar"""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill="x", side="bottom")

        ttk.Separator(status_frame, orient="horizontal").pack(fill="x")

        status_content = ttk.Frame(status_frame)
        status_content.pack(fill="x", padx=10, pady=2)

        # Status with icon
        self.status_label = ttk.Label(status_content, text="🟢 Ready")
        self.status_label.pack(side="left")

        # Progress info in status bar
        self.status_progress = ttk.Label(status_content, text="")
        self.status_progress.pack(side="left", padx=20)

        # Version and user info
        version_info = (
            f"v{self.config.version} | {self.auth_manager.current_user['username']}"
        )
        version_label = ttk.Label(status_content, text=version_info)
        version_label.pack(side="right")

    # Event handlers with enhanced functionality
    def _on_data_source_change(self):
        """Handle data source type change"""
        if self.data_source_type.get() == "mock":
            self.mock_frame.pack(fill="x", pady=5)
            self.excel_frame.pack_forget()
        else:
            self.mock_frame.pack_forget()
            self.excel_frame.pack(fill="x", pady=5)

    def _on_db_type_change(self):
        """Handle database type change"""
        if self.db_type.get() == "sqlite":
            self.sqlite_frame.pack(fill="x", pady=5)
            self.sqlserver_frame.pack_forget()
        else:
            self.sqlite_frame.pack_forget()
            self.sqlserver_frame.pack(fill="x", pady=5)

    def _on_sql_auth_change(self):
        """Handle SQL authentication change"""
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
        """Enhanced Excel file browser"""
        filename = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[
                ("Excel files", "*.xlsx *.xls *.xlsm"),
                ("Excel 2007+", "*.xlsx *.xlsm"),
                ("Excel 97-2003", "*.xls"),
                ("All files", "*.*"),
            ],
        )
        if filename:
            self.excel_file.set(filename)
            self._load_excel_info()

    def _load_excel_info(self):
        """Load Excel file information"""
        try:
            file_path = self.excel_file.get()
            if not file_path:
                return

            # Load sheets
            excel_handler = ExcelHandler()
            sheets = excel_handler.get_sheets(file_path)
            self.excel_sheet["values"] = sheets
            if sheets:
                self.excel_sheet.set(sheets[0])

            # Show file info
            file_info = Path(file_path).stat()
            size_mb = file_info.st_size / (1024 * 1024)
            info_text = f"📄 {len(sheets)} sheets • {size_mb:.1f} MB"
            self.file_info_label.configure(text=info_text)

        except Exception as e:
            logger.error(f"Failed to load Excel info: {e}")
            messagebox.showerror("Error", f"ไม่สามารถโหลดข้อมูล Excel ได้: {e}")
            self.file_info_label.configure(text="❌ Error loading file")

    def _browse_sqlite_file(self):
        """Enhanced SQLite file browser"""
        filename = filedialog.asksaveasfilename(
            title="Select SQLite Database File",
            defaultextension=".db",
            filetypes=[
                ("SQLite files", "*.db *.sqlite *.sqlite3"),
                ("All files", "*.*"),
            ],
        )
        if filename:
            self.sqlite_file.set(filename)

    def _quick_test_connection(self):
        """Quick connection test"""
        try:
            config = self._get_database_config()
            db_manager = DatabaseManager(config)

            if self.db_type.get() == "sqlite":
                success = db_manager.connect(force_mode="sqlite")
            else:
                success = db_manager.connect(force_mode="sqlserver")

            if success:
                messagebox.showinfo("Success", "✅ Connection successful!")
            else:
                messagebox.showerror("Error", "❌ Connection failed!")

            db_manager.close()

        except Exception as e:
            messagebox.showerror("Error", f"Connection error: {e}")

    def _open_db_test(self):
        """Open database test dialog - placeholder"""
        messagebox.showinfo("DB Test", "🔐 Database test dialog would open here")

    def _logout(self):
        """Enhanced logout with confirmation"""
        if messagebox.askyesno("Confirm Logout", "ต้องการออกจากระบบหรือไม่?"):
            self.auth_manager.logout()
            self.root.quit()

    def _start_processing(self):
        """Enhanced processing start"""
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

        # Start processing
        threading.Thread(target=self._process_data, daemon=True).start()

    def _stop_processing(self):
        """Stop processing"""
        if self.data_processor:
            self.data_processor.stop()

        self.is_processing = False
        self.process_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self._update_progress(0, "Stopped")

    def _process_data(self):
        """Enhanced data processing"""
        try:
            # Get configurations
            data_source_config = self._get_data_source_config()
            database_config = self._get_database_config()

            # Create processor
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
            error_msg = f"Processing error: {str(e)}"
            logger.error(error_msg, exc_info=True)
            self.root.after(0, lambda: self._show_error(error_msg))

        finally:
            self.root.after(0, self._processing_finished)

    def _validate_inputs(self) -> bool:
        """Enhanced input validation"""
        # Check data source
        if self.data_source_type.get() == "excel":
            if not self.excel_file.get():
                messagebox.showerror("ข้อผิดพลาด", "กรุณาเลือกไฟล์ Excel")
                return False

            if not Path(self.excel_file.get()).exists():
                messagebox.showerror("ข้อผิดพลาด", "ไม่พบไฟล์ Excel ที่ระบุ")
                return False

        # Check database config
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
        """Get data source configuration"""
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

    def _get_database_config(self):
        """Get database configuration"""
        try:
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
        except Exception as e:
            logger.error(f"Database config error: {e}")
            raise

    def _on_progress_update(self, progress_data: Dict[str, Any]):
        """Enhanced progress update"""
        progress = progress_data.get("progress", 0)
        message = progress_data.get("message", "Processing...")

        self._update_progress(progress, message)

    def _update_progress(self, progress: float, message: str):
        """Update progress display"""
        self.progress_var.set(progress)
        self.progress_label.configure(text=message)
        self.progress_percent.configure(text=f"{progress:.1f}%")
        self.status_label.configure(text=f"🔄 {message}")
        self.status_progress.configure(text=f"{progress:.1f}%")

    def _on_log_message(self, message: str, level: str = "info"):
        """Enhanced log message handling"""
        self.log_messages.append((datetime.now(), level, message))

        # Format log entry with colors
        timestamp = datetime.now().strftime("%H:%M:%S")
        level_icons = {"info": "ℹ️", "warning": "⚠️", "error": "❌", "debug": "🔍"}
        icon = level_icons.get(level, "📝")

        log_entry = f"[{timestamp}] {icon} {message}\n"

        # Add to logs with color coding
        self.logs_text.insert(tk.END, log_entry)

        # Apply color tags
        start_line = self.logs_text.index(tk.END + "-2l")
        end_line = self.logs_text.index(tk.END + "-1l")

        if level == "error":
            self.logs_text.tag_add("error", start_line, end_line)
            self.logs_text.tag_config("error", foreground="#ff6b6b")
        elif level == "warning":
            self.logs_text.tag_add("warning", start_line, end_line)
            self.logs_text.tag_config("warning", foreground="#feca57")

        self.logs_text.see(tk.END)

        # Keep only last 1000 lines
        lines = self.logs_text.get(1.0, tk.END).split("\n")
        if len(lines) > 1000:
            self.logs_text.delete(1.0, f"{len(lines) - 1000}.0")

    def _show_results(self, result: Dict[str, Any]):
        """Enhanced results display"""
        if result.get("success", False):
            self._log_result("✅ การประมวลผลสำเร็จ!\n", "success")

            # Enhanced summary with more details
            summary = f"""
📊 สรุปผลการประมวลผล
{'='*60}
✅ สถานะ: สำเร็จ
📝 จำนวนแถว: {result.get('rows_processed', 0):,} แถว
⏱️ เวลาที่ใช้: {result.get('duration', 0):.2f} วินาที
🗄️ ตาราง: {result.get('table_name', 'N/A')}
🏢 ฐานข้อมูล: {result.get('database_type', 'N/A').upper()}
⚡ ความเร็ว: {result.get('metrics', {}).get('rows_per_second', 0):.0f} แถว/วินาที
💾 ขนาดข้อมูล: {self._estimate_data_size(result.get('rows_processed', 0))}

📈 ข้อมูลตาราง:
{self._format_table_info(result.get('table_info', {}))}

🎯 คำแนะนำ:
• ใช้ "🔐 DB Test" เพื่อดูข้อมูลในตาราง
• สามารถนำเข้าข้อมูลเพิ่มเติมได้
• ตรวจสอบ Logs สำหรับรายละเอียดเพิ่มเติม
"""
            self._log_result(summary, "info")

        else:
            self._log_result("❌ การประมวลผลล้มเหลว!\n", "error")
            error_msg = result.get("error", "Unknown error")
            self._log_result(f"ข้อผิดพลาด: {error_msg}\n", "error")

    def _estimate_data_size(self, rows: int) -> str:
        """Estimate data size"""
        estimated_kb = rows * 0.5  # Rough estimate
        if estimated_kb < 1024:
            return f"~{estimated_kb:.0f} KB"
        else:
            return f"~{estimated_kb/1024:.1f} MB"

    def _format_table_info(self, table_info: Dict[str, Any]) -> str:
        """Enhanced table info formatting"""
        if not table_info or "error" in table_info:
            return "ไม่สามารถดึงข้อมูลตารางได้"

        info = f"""• ชื่อตาราง: {table_info.get('table_name', 'N/A')}
• จำนวนแถว: {table_info.get('row_count', 0):,}
• จำนวนคอลัมน์: {table_info.get('column_count', 0)}
• ขนาดตาราง: {table_info.get('size_mb', 0)} MB
• ประเภทฐานข้อมูล: {table_info.get('database_type', 'N/A')}"""

        return info

    def _show_error(self, error_msg: str):
        """Enhanced error display"""
        self._log_result(f"❌ ข้อผิดพลาด: {error_msg}\n", "error")
        messagebox.showerror("ข้อผิดพลาด", error_msg)

    def _log_result(self, message: str, level: str = "info"):
        """Enhanced result logging with colors"""
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
        """Enhanced processing completion"""
        self.is_processing = False
        self.process_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self._update_progress(0, "Ready")
        self.status_label.configure(text="🟢 Ready")

    # Additional helper methods
    def _create_sample_data(self):
        """Create sample Excel file"""
        try:
            from core.excel_handler import FileUtils

            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                title="Save Sample Excel File",
            )
            if filename:
                if FileUtils.create_sample_excel(filename, "employees", 100):
                    messagebox.showinfo("Success", f"Sample file created: {filename}")
                    self.excel_file.set(filename)
                    self._load_excel_info()
                else:
                    messagebox.showerror("Error", "Failed to create sample file")
        except Exception as e:
            messagebox.showerror("Error", f"Sample creation error: {e}")

    def _clear_results(self):
        """Clear results display"""
        if messagebox.askyesno("Confirm", "ต้องการล้างผลลัพธ์หรือไม่?"):
            self.results_text.delete(1.0, tk.END)

    def _clear_logs(self):
        """Enhanced log clearing"""
        if messagebox.askyesno("Confirm", "ต้องการล้าง logs หรือไม่?"):
            self.logs_text.delete(1.0, tk.END)
            self.log_messages.clear()
            logger.info("Logs cleared by user")

    def _save_results(self):
        """Save results to file"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Save Results",
            )
            if filename:
                content = self.results_text.get(1.0, tk.END)
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(content)
                messagebox.showinfo("Success", f"Results saved: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Save error: {e}")

    def _copy_results(self):
        """Copy results to clipboard"""
        try:
            content = self.results_text.get(1.0, tk.END)
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            messagebox.showinfo("Success", "Results copied to clipboard")
        except Exception as e:
            messagebox.showerror("Error", f"Copy error: {e}")

    def _find_in_results(self):
        """Find text in results"""
        search_text = tk.simpledialog.askstring("Find", "Enter text to search:")
        if search_text:
            # Simple search implementation
            content = self.results_text.get(1.0, tk.END)
            if search_text.lower() in content.lower():
                messagebox.showinfo("Found", f"Text '{search_text}' found in results")
            else:
                messagebox.showinfo("Not Found", f"Text '{search_text}' not found")

    def _filter_logs(self, event=None):
        """Filter logs by level"""
        # Simple filter implementation - would need enhancement
        level_filter = self.log_level_filter.get()
        if level_filter == "All":
            return  # Show all logs

        # This is a placeholder - full implementation would re-populate logs
        logger.info(f"Filtering logs by level: {level_filter}")

    def _export_logs(self):
        """Export logs to file"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".log",
                filetypes=[("Log files", "*.log"), ("Text files", "*.txt")],
                title="Export Logs",
            )
            if filename:
                content = self.logs_text.get(1.0, tk.END)
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(content)
                messagebox.showinfo("Success", f"Logs exported: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Export error: {e}")

    def _load_settings(self):
        """Enhanced settings loading"""
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
        """Enhanced settings saving"""
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
                    "last_excel_file": self.excel_file.get(),
                },
                "database": {
                    "default_type": self.db_type.get(),
                    "sqlite_file": self.sqlite_file.get(),
                    "sql_server": {
                        "host": self.sql_server.get(),
                        "database": self.sql_database.get(),
                        "username": self.sql_username.get(),
                        "use_windows_auth": self.sql_windows_auth.get(),
                    },
                },
                "last_table_name": self.table_name.get(),
            }

            self.settings_manager.save_settings(settings)

        except Exception as e:
            logger.warning(f"Failed to save settings: {e}")

    def _on_close(self):
        """Enhanced close handling"""
        try:
            # Check if processing
            if self.is_processing:
                if not messagebox.askyesno(
                    "Confirm", "การประมวลผลกำลังทำงาน ต้องการปิดโปรแกรมหรือไม่?"
                ):
                    return

            # Save settings
            self._save_settings()

            # Stop processing
            if self.is_processing and self.data_processor:
                self.data_processor.stop()

            # Logout
            self.auth_manager.logout()

            # Close database connections
            if self.db_manager:
                self.db_manager.close()

            logger.info("Application closed gracefully")

        except Exception as e:
            logger.error(f"Error during shutdown: {e}")

        finally:
            self.root.destroy()

    def run(self):
        """Enhanced application runner"""
        try:
            logger.info(f"Starting {self.config.app_name} v{self.config.version}")
            logger.info(
                f"User: {self.auth_manager.current_user['username']} ({self.auth_manager.current_user['role']})"
            )

            # Show enhanced welcome message
            welcome_msg = f"""
🏭 ยินดีต้อนรับสู่ {self.config.app_name}
{'='*70}
👤 ผู้ใช้: {self.auth_manager.current_user['username']} ({self.auth_manager.current_user['role']})
🔧 เวอร์ชัน: {self.config.version} - Enhanced Security Edition
👨‍💻 ผู้พัฒนา: {self.config.author}
🕐 เซสชัน: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📋 ฟีเจอร์ใหม่ในเวอร์ชันนี้:
✅ ระบบรักษาความปลอดภัยที่ปรับปรุงแล้ว
✅ การจัดการฐานข้อมูลที่ดีขึ้น
✅ ส่วนติดต่อผู้ใช้ที่สวยงามขึ้น
✅ การรายงานผลลัพธ์ที่ละเอียดขึ้น
✅ ระบบล็อกการใช้งานที่ครบถ้วน

💡 วิธีเริ่มต้นใช้งาน:
1. 📊 เลือกแหล่งข้อมูล (Mock Data หรือ Excel File)
2. 🗄️ กำหนดค่าฐานข้อมูล (SQLite หรือ SQL Server)  
3. 🚀 กดปุ่ม "Start Processing"
4. 🔐 ใช้ "DB Test" เพื่อทดสอบการเชื่อมต่อ
5. 📊 ใช้ "Sample Data" เพื่อสร้างไฟล์ทดสอบ

เริ่มต้นใช้งานได้เลย! 🎯
"""
            self._log_result(welcome_msg, "info")

            # Start main loop
            self.root.mainloop()

        except Exception as e:
            logger.error(f"Fatal error in main loop: {e}", exc_info=True)
            messagebox.showerror("ข้อผิดพลาดร้ายแรง", f"เกิดข้อผิดพลาดร้ายแรง:\n{str(e)}")


# Usage example with error handling
if __name__ == "__main__":
    try:
        app = DENSO888MainWindow()
        if hasattr(app, "root") and app.root.winfo_exists():
            app.run()
    except Exception as e:
        print(f"Failed to start application: {e}")
        import traceback

        traceback.print_exc()
