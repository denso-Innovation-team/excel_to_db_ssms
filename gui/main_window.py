"""
gui/main_window.py
Main window controller for DENSO888 GUI application
ปรับปรุงให้เป็นระบบที่สมบูรณ์และแยกโมดูลชัดเจน
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import logging
from typing import Optional, Dict, Any, Callable
from pathlib import Path
import sys
import os

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import components
from config.settings import get_config, AppConfig
from utils.logger import setup_gui_logger
from utils.error_handler import setup_error_handling
from utils.settings_manager import SettingsManager

logger = logging.getLogger(__name__)


class DENSO888Theme:
    """Application theme manager"""

    def __init__(self, config: AppConfig):
        self.config = config
        self.colors = config.ui.theme_colors

    def apply_to_root(self, root):
        """Apply theme to root window"""
        style = ttk.Style(root)

        # ใช้ clam theme เป็น base
        style.theme_use("clam")

        # Configure custom styles
        style.configure(
            "Primary.TButton",
            background=self.colors["primary"],
            foreground=self.colors["white"],
            font=("Segoe UI", 10, "bold"),
        )

        style.configure(
            "Success.TButton",
            background=self.colors["success"],
            foreground=self.colors["white"],
        )

        style.configure(
            "Warning.TButton",
            background=self.colors["warning"],
            foreground=self.colors["accent"],
        )

        style.configure(
            "Danger.TButton",
            background=self.colors["danger"],
            foreground=self.colors["white"],
        )

        # Configure notebook style
        style.configure("Custom.TNotebook.Tab", padding=[12, 8], font=("Segoe UI", 9))


class HeaderComponent:
    """Application header with logo and title"""

    def __init__(self, parent, config: AppConfig):
        self.config = config
        self.frame = ttk.Frame(parent, style="Header.TFrame")

        # Left side - Logo and title
        left_frame = ttk.Frame(self.frame)
        left_frame.pack(side="left", fill="x", expand=True)

        # Logo (emoji for now, can be replaced with image)
        logo_label = ttk.Label(left_frame, text="🏭", font=("Segoe UI", 24))
        logo_label.pack(side="left", padx=(0, 10))

        # App name and tagline
        title_frame = ttk.Frame(left_frame)
        title_frame.pack(side="left", fill="x", expand=True)

        title_label = ttk.Label(
            title_frame,
            text=config.app_name,
            font=("Segoe UI", 16, "bold"),
            foreground=self.config.ui.theme_colors["primary"],
        )
        title_label.pack(anchor="w")

        subtitle_label = ttk.Label(
            title_frame,
            text=f"by {config.author}",
            font=("Segoe UI", 10),
            foreground=self.config.ui.theme_colors["accent"],
        )
        subtitle_label.pack(anchor="w")

        # Right side - Version and status
        right_frame = ttk.Frame(self.frame)
        right_frame.pack(side="right")

        version_label = ttk.Label(
            right_frame,
            text=f"v{config.version}",
            font=("Segoe UI", 9),
            foreground=self.config.ui.theme_colors["accent"],
        )
        version_label.pack(anchor="e")

    def pack(self, **kwargs):
        """Pack the header frame"""
        self.frame.pack(**kwargs)


class DataSourceTab:
    """Data source configuration tab"""

    def __init__(self, parent, config: AppConfig, callback: Callable):
        self.config = config
        self.callback = callback
        self.frame = ttk.Frame(parent)

        # Variables
        self.source_type = tk.StringVar(value="mock")
        self.mock_template = tk.StringVar(value="employees")
        self.mock_rows = tk.IntVar(value=1000)
        self.excel_file = tk.StringVar()
        self.excel_sheet = tk.StringVar()
        self.table_name = tk.StringVar(value="imported_data")

        self._create_widgets()

    def _create_widgets(self):
        """Create tab widgets"""
        # Data source type selection
        type_frame = ttk.LabelFrame(self.frame, text="📊 เลือกประเภทข้อมูล", padding=10)
        type_frame.pack(fill="x", padx=10, pady=10)

        # Mock data option
        mock_frame = ttk.Frame(type_frame)
        mock_frame.pack(fill="x", pady=5)

        ttk.Radiobutton(
            mock_frame,
            text="🎲 Mock ข้อมูลจำลอง",
            variable=self.source_type,
            value="mock",
            command=self._on_source_type_changed,
        ).pack(side="left")

        # Mock data controls
        self.mock_controls = ttk.Frame(type_frame)
        self.mock_controls.pack(fill="x", padx=20, pady=5)

        # Template selection
        template_frame = ttk.Frame(self.mock_controls)
        template_frame.pack(fill="x", pady=2)

        ttk.Label(template_frame, text="Template:").pack(side="left")
        template_combo = ttk.Combobox(
            template_frame,
            textvariable=self.mock_template,
            values=["employees", "sales", "inventory", "financial"],
            state="readonly",
            width=15,
        )
        template_combo.pack(side="left", padx=5)

        # Row count selection
        rows_frame = ttk.Frame(self.mock_controls)
        rows_frame.pack(fill="x", pady=2)

        ttk.Label(rows_frame, text="จำนวนแถว:").pack(side="left")

        # Quick selection buttons
        row_counts = [100, 500, 1000, 5000, 10000, 50000]
        for count in row_counts:
            ttk.Button(
                rows_frame,
                text=f"{count:,}",
                width=8,
                command=lambda c=count: self.mock_rows.set(c),
            ).pack(side="left", padx=2)

        # Custom row count entry
        ttk.Entry(rows_frame, textvariable=self.mock_rows, width=10).pack(
            side="left", padx=5
        )

        # Excel file option
        excel_frame = ttk.Frame(type_frame)
        excel_frame.pack(fill="x", pady=5)

        ttk.Radiobutton(
            excel_frame,
            text="📁 ไฟล์ Excel",
            variable=self.source_type,
            value="excel",
            command=self._on_source_type_changed,
        ).pack(side="left")

        # Excel file controls
        self.excel_controls = ttk.Frame(type_frame)
        self.excel_controls.pack(fill="x", padx=20, pady=5)

        file_frame = ttk.Frame(self.excel_controls)
        file_frame.pack(fill="x", pady=2)

        ttk.Entry(file_frame, textvariable=self.excel_file, width=50).pack(
            side="left", fill="x", expand=True
        )

        ttk.Button(file_frame, text="Browse...", command=self._browse_excel_file).pack(
            side="right", padx=5
        )

        # Sheet selection
        sheet_frame = ttk.Frame(self.excel_controls)
        sheet_frame.pack(fill="x", pady=2)

        ttk.Label(sheet_frame, text="Sheet:").pack(side="left")
        self.sheet_combo = ttk.Combobox(
            sheet_frame, textvariable=self.excel_sheet, width=20
        )
        self.sheet_combo.pack(side="left", padx=5)

        # Table name
        table_frame = ttk.LabelFrame(self.frame, text="🗄️ ชื่อตารางในฐานข้อมูล", padding=10)
        table_frame.pack(fill="x", padx=10, pady=5)

        ttk.Entry(table_frame, textvariable=self.table_name, width=30).pack(anchor="w")

        # Preview section
        preview_frame = ttk.LabelFrame(self.frame, text="👁️ ตัวอย่างข้อมูล", padding=10)
        preview_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Preview tree
        self.preview_tree = ttk.Treeview(preview_frame, height=8)
        self.preview_tree.pack(fill="both", expand=True)

        # Scrollbar for preview
        preview_scroll = ttk.Scrollbar(
            preview_frame, orient="vertical", command=self.preview_tree.yview
        )
        preview_scroll.pack(side="right", fill="y")
        self.preview_tree.configure(yscrollcommand=preview_scroll.set)

        # Initial state
        self._on_source_type_changed()

    def _on_source_type_changed(self):
        """Handle data source type change"""
        source = self.source_type.get()

        if source == "mock":
            self._show_frame(self.mock_controls)
            self._hide_frame(self.excel_controls)
            self._generate_mock_preview()
        else:
            self._hide_frame(self.mock_controls)
            self._show_frame(self.excel_controls)

        self._notify_change()

    def _show_frame(self, frame):
        """Show frame"""
        for widget in frame.winfo_children():
            widget.configure(state="normal")

    def _hide_frame(self, frame):
        """Hide frame"""
        for widget in frame.winfo_children():
            widget.configure(state="disabled")

    def _browse_excel_file(self):
        """Browse for Excel file"""
        file_types = [
            ("Excel files", "*.xlsx *.xls"),
            ("Excel 2007+", "*.xlsx"),
            ("Excel 97-2003", "*.xls"),
            ("All files", "*.*"),
        ]

        filename = filedialog.askopenfilename(
            title="เลือกไฟล์ Excel",
            filetypes=file_types,
            initialdir=str(Path.cwd() / "assets" / "samples"),
        )

        if filename:
            self.excel_file.set(filename)
            self._load_excel_sheets(filename)
            self._notify_change()

    def _load_excel_sheets(self, file_path: str):
        """Load Excel sheet names"""
        try:
            from core.excel_handler import ExcelHandler

            handler = ExcelHandler()
            sheets = handler.get_sheets(file_path)

            self.sheet_combo["values"] = sheets
            if sheets:
                self.excel_sheet.set(sheets[0])

        except Exception as e:
            logger.error(f"Failed to load Excel sheets: {e}")
            messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดรายชื่อ Sheet ได้:\n{e}")

    def _generate_mock_preview(self):
        """Generate mock data preview"""
        try:
            from core.mock_generator import MockDataGenerator

            template = self.mock_template.get()

            if template == "employees":
                df = MockDataGenerator.generate_employee_data(5)
            elif template == "sales":
                df = MockDataGenerator.generate_sales_data(5)
            elif template == "inventory":
                df = MockDataGenerator.generate_inventory_data(5)
            elif template == "financial":
                df = MockDataGenerator.generate_financial_data(5)
            else:
                df = MockDataGenerator.generate_custom_data(5)

            self._update_preview(df)

        except Exception as e:
            logger.error(f"Failed to generate mock preview: {e}")

    def _update_preview(self, df):
        """Update preview treeview"""
        # Clear existing data
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)

        if df is None or df.empty:
            return

        # Configure columns
        columns = list(df.columns)
        self.preview_tree["columns"] = columns
        self.preview_tree["show"] = "headings"

        # Configure column headers
        for col in columns:
            self.preview_tree.heading(col, text=col)
            self.preview_tree.column(col, width=100, minwidth=50)

        # Add data rows
        for _, row in df.iterrows():
            values = [str(row[col]) for col in columns]
            self.preview_tree.insert("", "end", values=values)

    def _notify_change(self):
        """Notify parent of changes"""
        if self.callback:
            self.callback("data_source_changed", self.get_data_info())

    def get_config(self) -> Dict[str, Any]:
        """Get data source configuration"""
        source = self.source_type.get()

        config = {
            "type": source,
            "table_name": self.table_name.get() or "imported_data",
        }

        if source == "mock":
            config.update(
                {"template": self.mock_template.get(), "rows": self.mock_rows.get()}
            )
        else:
            config.update(
                {
                    "file_path": self.excel_file.get(),
                    "sheet_name": self.excel_sheet.get(),
                }
            )

        return config

    def get_data_info(self) -> Dict[str, Any]:
        """Get current data information"""
        source = self.source_type.get()

        if source == "mock":
            return {
                "type": "mock",
                "template": self.mock_template.get(),
                "rows": self.mock_rows.get(),
                "has_valid_data": True,
            }
        else:
            file_path = self.excel_file.get()
            return {
                "type": "excel",
                "file_path": file_path,
                "sheet_name": self.excel_sheet.get(),
                "has_valid_data": bool(file_path and Path(file_path).exists()),
            }

    def validate(self) -> bool:
        """Validate current configuration"""
        source = self.source_type.get()

        if source == "mock":
            rows = self.mock_rows.get()
            if rows < 1 or rows > 1000000:
                messagebox.showerror("ข้อผิดพลาด", "จำนวนแถวต้องอยู่ระหว่าง 1 - 1,000,000")
                return False
        else:
            file_path = self.excel_file.get()
            if not file_path:
                messagebox.showerror("ข้อผิดพลาด", "กรุณาเลือกไฟล์ Excel")
                return False
            if not Path(file_path).exists():
                messagebox.showerror("ข้อผิดพลาด", "ไม่พบไฟล์ที่เลือก")
                return False

        table_name = self.table_name.get()
        if not table_name or not table_name.replace("_", "").isalnum():
            messagebox.showerror("ข้อผิดพลาด", "ชื่อตารางต้องประกอบด้วยตัวอักษรและตัวเลขเท่านั้น")
            return False

        return True


class DatabaseTab:
    """Database configuration tab"""

    def __init__(self, parent, config: AppConfig, callback: Callable):
        self.config = config
        self.callback = callback
        self.frame = ttk.Frame(parent)

        # Variables
        self.db_type = tk.StringVar(value="sqlite")
        self.sql_server = tk.StringVar(value=config.database.server)
        self.sql_database = tk.StringVar(value=config.database.database)
        self.sql_username = tk.StringVar(value=config.database.username)
        self.sql_password = tk.StringVar()
        self.sql_windows_auth = tk.BooleanVar(value=config.database.use_windows_auth)
        self.sqlite_file = tk.StringVar(value=config.database.sqlite_file)

        self._create_widgets()

    def _create_widgets(self):
        """Create tab widgets"""
        # Database type selection
        type_frame = ttk.LabelFrame(self.frame, text="🗄️ เลือกประเภทฐานข้อมูล", padding=10)
        type_frame.pack(fill="x", padx=10, pady=10)

        # SQLite option
        sqlite_frame = ttk.Frame(type_frame)
        sqlite_frame.pack(fill="x", pady=5)

        ttk.Radiobutton(
            sqlite_frame,
            text="📁 SQLite (Local Database)",
            variable=self.db_type,
            value="sqlite",
            command=self._on_db_type_changed,
        ).pack(side="left")

        # SQLite controls
        self.sqlite_controls = ttk.Frame(type_frame)
        self.sqlite_controls.pack(fill="x", padx=20, pady=5)

        sqlite_file_frame = ttk.Frame(self.sqlite_controls)
        sqlite_file_frame.pack(fill="x", pady=2)

        ttk.Label(sqlite_file_frame, text="ไฟล์ฐานข้อมูล:").pack(side="left")
        ttk.Entry(sqlite_file_frame, textvariable=self.sqlite_file, width=30).pack(
            side="left", padx=5, fill="x", expand=True
        )

        ttk.Button(
            sqlite_file_frame, text="Browse...", command=self._browse_sqlite_file
        ).pack(side="right")

        # SQL Server option
        sqlserver_frame = ttk.Frame(type_frame)
        sqlserver_frame.pack(fill="x", pady=5)

        ttk.Radiobutton(
            sqlserver_frame,
            text="🏢 SQL Server",
            variable=self.db_type,
            value="sqlserver",
            command=self._on_db_type_changed,
        ).pack(side="left")

        # SQL Server controls
        self.sqlserver_controls = ttk.Frame(type_frame)
        self.sqlserver_controls.pack(fill="x", padx=20, pady=5)

        # Server and Database
        server_frame = ttk.Frame(self.sqlserver_controls)
        server_frame.pack(fill="x", pady=2)

        ttk.Label(server_frame, text="Server:").pack(side="left")
        ttk.Entry(server_frame, textvariable=self.sql_server, width=20).pack(
            side="left", padx=5
        )

        ttk.Label(server_frame, text="Database:").pack(side="left", padx=(20, 0))
        ttk.Entry(server_frame, textvariable=self.sql_database, width=20).pack(
            side="left", padx=5
        )

        # Authentication
        auth_frame = ttk.Frame(self.sqlserver_controls)
        auth_frame.pack(fill="x", pady=2)

        ttk.Checkbutton(
            auth_frame,
            text="ใช้ Windows Authentication",
            variable=self.sql_windows_auth,
            command=self._on_auth_changed,
        ).pack(anchor="w")

        # Username/Password
        self.credentials_frame = ttk.Frame(self.sqlserver_controls)
        self.credentials_frame.pack(fill="x", pady=2)

        ttk.Label(self.credentials_frame, text="Username:").pack(side="left")
        ttk.Entry(
            self.credentials_frame, textvariable=self.sql_username, width=15
        ).pack(side="left", padx=5)

        ttk.Label(self.credentials_frame, text="Password:").pack(
            side="left", padx=(20, 0)
        )
        ttk.Entry(
            self.credentials_frame, textvariable=self.sql_password, width=15, show="*"
        ).pack(side="left", padx=5)

        # Connection test
        test_frame = ttk.Frame(self.frame)
        test_frame.pack(fill="x", padx=10, pady=5)

        self.test_btn = ttk.Button(
            test_frame, text="🔌 ทดสอบการเชื่อมต่อ", command=self._test_connection
        )
        self.test_btn.pack(side="left")

        self.connection_status = ttk.Label(
            test_frame, text="ยังไม่ได้ทดสอบ", foreground="gray"
        )
        self.connection_status.pack(side="left", padx=10)

        # Initial state
        self._on_db_type_changed()
        self._on_auth_changed()

    def _on_db_type_changed(self):
        """Handle database type change"""
        db_type = self.db_type.get()

        if db_type == "sqlite":
            self._show_frame(self.sqlite_controls)
            self._hide_frame(self.sqlserver_controls)
        else:
            self._hide_frame(self.sqlite_controls)
            self._show_frame(self.sqlserver_controls)

        self._notify_change()

    def _on_auth_changed(self):
        """Handle authentication method change"""
        if self.sql_windows_auth.get():
            self._hide_frame(self.credentials_frame)
        else:
            self._show_frame(self.credentials_frame)

    def _show_frame(self, frame):
        """Show frame"""
        for widget in frame.winfo_children():
            if hasattr(widget, "configure"):
                widget.configure(state="normal")

    def _hide_frame(self, frame):
        """Hide frame"""
        for widget in frame.winfo_children():
            if hasattr(widget, "configure"):
                widget.configure(state="disabled")

    def _browse_sqlite_file(self):
        """Browse for SQLite file"""
        filename = filedialog.asksaveasfilename(
            title="เลือกไฟล์ SQLite",
            defaultextension=".db",
            filetypes=[("SQLite files", "*.db"), ("All files", "*.*")],
        )

        if filename:
            self.sqlite_file.set(filename)
            self._notify_change()

    def _test_connection(self):
        """Test database connection"""
        self.test_btn.configure(state="disabled")
        self.connection_status.configure(text="กำลังทดสอบ...", foreground="orange")

        # Run test in background thread
        def test_thread():
            try:
                from core.database_manager import DatabaseManager

                # Create temporary database manager
                db_config = self.get_config()
                db_manager = DatabaseManager(db_config)

                # Test connection
                success = db_manager.connect(force_mode=self.db_type.get())

                if success:
                    status = db_manager.get_status()
                    self.root.after(0, lambda: self._on_test_success(status))
                else:
                    self.root.after(
                        0, lambda: self._on_test_failed("Connection failed")
                    )

                db_manager.close()

            except Exception as e:
                self.root.after(0, lambda: self._on_test_failed(str(e)))

        self.root = self.frame.winfo_toplevel()
        threading.Thread(target=test_thread, daemon=True).start()

    def _on_test_success(self, status):
        """Handle successful connection test"""
        self.test_btn.configure(state="normal")
        self.connection_status.configure(text="✅ เชื่อมต่อสำเร็จ", foreground="green")

        db_type = status.get("active_database", "unknown")
        messagebox.showinfo("การเชื่อมต่อสำเร็จ", f"เชื่อมต่อ {db_type.upper()} สำเร็จ!")

        self._notify_change()

    def _on_test_failed(self, error_msg):
        """Handle failed connection test"""
        self.test_btn.configure(state="normal")
        self.connection_status.configure(text="❌ เชื่อมต่อล้มเหลว", foreground="red")

        messagebox.showerror(
            "การเชื่อมต่อล้มเหลว", f"ไม่สามารถเชื่อมต่อฐานข้อมูลได้:\n{error_msg}"
        )

    def _notify_change(self):
        """Notify parent of changes"""
        if self.callback:
            self.callback("database_changed", self.get_database_info())

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

    def get_database_info(self) -> Dict[str, Any]:
        """Get current database information"""
        return {
            "type": self.db_type.get(),
            "connection_tested": self.connection_status.cget("text") != "ยังไม่ได้ทดสอบ",
            "connection_status": {
                "connected": "✅" in self.connection_status.cget("text")
            },
        }

    def validate(self) -> bool:
        """Validate database configuration"""
        db_type = self.db_type.get()

        if db_type == "sqlserver":
            if not self.sql_server.get():
                messagebox.showerror("ข้อผิดพลาด", "กรุณาระบุชื่อ Server")
                return False
            if not self.sql_database.get():
                messagebox.showerror("ข้อผิดพลาด", "กรุณาระบุชื่อ Database")
                return False
            if not self.sql_windows_auth.get():
                if not self.sql_username.get():
                    messagebox.showerror("ข้อผิดพลาด", "กรุณาระบุ Username")
                    return False
        else:
            if not self.sqlite_file.get():
                messagebox.showerror("ข้อผิดพลาด", "กรุณาระบุไฟล์ SQLite")
                return False

        return True


class ProcessingTab:
    """Data processing tab"""

    def __init__(self, parent, config: AppConfig, callback: Callable):
        self.config = config
        self.callback = callback
        self.frame = ttk.Frame(parent)

        # Processing state
        self.is_processing = False
        self.current_progress = 0

        self._create_widgets()

    def _create_widgets(self):
        """Create tab widgets"""
        # Control panel
        control_frame = ttk.LabelFrame(self.frame, text="⚡ การควบคุม", padding=10)
        control_frame.pack(fill="x", padx=10, pady=10)

        # Main buttons
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(fill="x")

        self.start_btn = ttk.Button(
            btn_frame,
            text="🚀 เริ่มประมวลผล",
            command=self._start_processing,
            style="Primary.TButton",
        )
        self.start_btn.pack(side="left", padx=5)

        self.stop_btn = ttk.Button(
            btn_frame,
            text="⏹️ หยุด",
            command=self._stop_processing,
            state="disabled",
            style="Danger.TButton",
        )
        self.stop_btn.pack(side="left", padx=5)

        self.clear_btn = ttk.Button(
            btn_frame, text="🗑️ ล้างผลลัพธ์", command=self._clear_results
        )
        self.clear_btn.pack(side="right", padx=5)

        # Progress section
        progress_frame = ttk.LabelFrame(self.frame, text="📊 ความคืบหน้า", padding=10)
        progress_frame.pack(fill="x", padx=10, pady=5)

        self.progress_bar = ttk.Progressbar(
            progress_frame, length=500, mode="determinate"
        )
        self.progress_bar.pack(fill="x", pady=5)

        self.status_label = ttk.Label(
            progress_frame, text="พร้อมประมวลผล", font=("Segoe UI", 10)
        )
        self.status_label.pack(anchor="w", pady=2)

        # Data preview section
        preview_frame = ttk.LabelFrame(self.frame, text="👁️ ข้อมูลต้นทาง", padding=10)
        preview_frame.pack(fill="x", padx=10, pady=5)

        self.data_info_label = ttk.Label(
            preview_frame, text="ยังไม่ได้เลือกข้อมูล", foreground="gray"
        )
        self.data_info_label.pack(anchor="w")

        # Database status section
        db_frame = ttk.LabelFrame(self.frame, text="🗄️ สถานะฐานข้อมูล", padding=10)
        db_frame.pack(fill="x", padx=10, pady=5)

        self.db_info_label = ttk.Label(
            db_frame, text="ยังไม่ได้กำหนดฐานข้อมูล", foreground="gray"
        )
        self.db_info_label.pack(anchor="w")

        # Results section
        results_frame = ttk.LabelFrame(self.frame, text="📋 ผลลัพธ์", padding=10)
        results_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Results text with scrollbar
        text_frame = ttk.Frame(results_frame)
        text_frame.pack(fill="both", expand=True)

        self.results_text = tk.Text(
            text_frame, height=12, wrap=tk.WORD, font=("Consolas", 9)
        )
        self.results_text.pack(side="left", fill="both", expand=True)

        results_scroll = ttk.Scrollbar(
            text_frame, orient="vertical", command=self.results_text.yview
        )
        results_scroll.pack(side="right", fill="y")
        self.results_text.configure(yscrollcommand=results_scroll.set)

    def _start_processing(self):
        """Start processing"""
        if self.callback:
            self.callback("start_processing", {})

    def _stop_processing(self):
        """Stop processing"""
        if self.callback:
            self.callback("stop_processing", {})

    def _clear_results(self):
        """Clear results"""
        self.results_text.delete(1.0, tk.END)
        self.progress_bar["value"] = 0
        self.status_label.configure(text="พร้อมประมวลผล")

    def set_processing_state(self, processing: bool):
        """Set processing state"""
        self.is_processing = processing

        if processing:
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
        else:
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")

    def update_progress(self, progress_data: Dict[str, Any]):
        """Update progress display"""
        progress = progress_data.get("progress", 0)
        message = progress_data.get("message", "")

        self.progress_bar["value"] = progress
        self.status_label.configure(text=message)

        # Update results text
        if message:
            self.results_text.insert(tk.END, f"[{progress:.1f}%] {message}\n")
            self.results_text.see(tk.END)

    def update_data_preview(self, data_info: Dict[str, Any]):
        """Update data preview"""
        if data_info.get("type") == "mock":
            template = data_info.get("template", "unknown")
            rows = data_info.get("rows", 0)
            text = f"📊 Mock Data: {template} ({rows:,} rows)"
        else:
            file_path = data_info.get("file_path", "")
            sheet = data_info.get("sheet_name", "")
            text = f"📁 Excel: {Path(file_path).name} (Sheet: {sheet})"

        self.data_info_label.configure(text=text, foreground="black")

    def update_database_status(self, db_info: Dict[str, Any]):
        """Update database status"""
        db_type = db_info.get("type", "unknown")
        connected = db_info.get("connection_status", {}).get("connected", False)

        if connected:
            text = f"🗄️ {db_type.upper()}: เชื่อมต่อแล้ว"
            color = "green"
        else:
            text = f"🗄️ {db_type.upper()}: ยังไม่ได้เชื่อมต่อ"
            color = "orange"

        self.db_info_label.configure(text=text, foreground=color)

    def show_results(self, result: Dict[str, Any]):
        """Show processing results"""
        if result.get("success", False):
            self.results_text.insert(tk.END, "\n" + "=" * 50 + "\n")
            self.results_text.insert(tk.END, "🎉 ประมวลผลสำเร็จ!\n")
            self.results_text.insert(
                tk.END, f"📊 จำนวนแถวที่ประมวลผล: {result.get('rows_processed', 0):,}\n"
            )
            self.results_text.insert(
                tk.END, f"⏱️ เวลาที่ใช้: {result.get('duration', 0):.2f} วินาที\n"
            )
            self.results_text.insert(
                tk.END, f"🗄️ ตาราง: {result.get('table_name', 'N/A')}\n"
            )
            self.results_text.insert(
                tk.END, f"💾 ฐานข้อมูล: {result.get('database_type', 'N/A')}\n"
            )

            if result.get("metrics"):
                metrics = result["metrics"]
                rps = metrics.get("rows_per_second", 0)
                self.results_text.insert(tk.END, f"⚡ ความเร็ว: {rps:.0f} rows/sec\n")

            self.results_text.insert(tk.END, "=" * 50 + "\n")
        else:
            self.show_error(result.get("error", "Unknown error"))

        self.results_text.see(tk.END)

    def show_error(self, error_message: str):
        """Show error message"""
        self.results_text.insert(tk.END, "\n" + "=" * 50 + "\n")
        self.results_text.insert(tk.END, "❌ เกิดข้อผิดพลาด!\n")
        self.results_text.insert(tk.END, f"💬 {error_message}\n")
        self.results_text.insert(tk.END, "=" * 50 + "\n")
        self.results_text.see(tk.END)

    def set_processing_enabled(self, enabled: bool):
        """Enable/disable processing"""
        state = "normal" if enabled else "disabled"
        self.start_btn.configure(state=state)


class LogsTab:
    """Application logs tab"""

    def __init__(self, parent, config: AppConfig):
        self.config = config
        self.frame = ttk.Frame(parent)
        self.max_lines = 1000

        self._create_widgets()

    def _create_widgets(self):
        """Create tab widgets"""
        # Control panel
        control_frame = ttk.Frame(self.frame)
        control_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(control_frame, text="📋 บันทึกการทำงาน").pack(side="left")

        # Control buttons
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(side="right")

        ttk.Button(btn_frame, text="🗑️ ล้างบันทึก", command=self.clear_logs).pack(
            side="right", padx=2
        )

        ttk.Button(btn_frame, text="💾 บันทึกไฟล์", command=self.save_logs).pack(
            side="right", padx=2
        )

        ttk.Button(btn_frame, text="🔄 รีเฟรช", command=self.refresh_logs).pack(
            side="right", padx=2
        )

        # Log display
        log_frame = ttk.Frame(self.frame)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_text = tk.Text(
            log_frame,
            height=20,
            wrap=tk.WORD,
            font=("Consolas", 9),
            bg="#f8f9fa",
            fg="#333333",
        )
        self.log_text.pack(side="left", fill="both", expand=True)

        # Scrollbar
        log_scroll = ttk.Scrollbar(
            log_frame, orient="vertical", command=self.log_text.yview
        )
        log_scroll.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=log_scroll.set)

        # Configure text tags for different log levels
        self.log_text.tag_configure("ERROR", foreground="#dc3545")
        self.log_text.tag_configure("WARNING", foreground="#ffc107")
        self.log_text.tag_configure("INFO", foreground="#17a2b8")
        self.log_text.tag_configure("DEBUG", foreground="#6c757d")

    def add_log(self, message: str, level: str = "info"):
        """Add log message"""
        import datetime

        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"

        # Insert with appropriate color
        tag = level.upper()
        self.log_text.insert(tk.END, log_entry, tag)

        # Limit number of lines
        lines = int(self.log_text.index(tk.END).split(".")[0])
        if lines > self.max_lines:
            self.log_text.delete(1.0, f"{lines - self.max_lines}.0")

        self.log_text.see(tk.END)

    def clear_logs(self):
        """Clear all logs"""
        self.log_text.delete(1.0, tk.END)
        self.add_log("บันทึกถูกล้างแล้ว", "info")

    def save_logs(self):
        """Save logs to file"""
        import datetime

        filename = filedialog.asksaveasfilename(
            title="บันทึกไฟล์ Log",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialname=f"denso888_logs_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        )

        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(self.log_text.get(1.0, tk.END))

                self.add_log(f"บันทึกไฟล์ Log: {filename}", "info")
                messagebox.showinfo("สำเร็จ", f"บันทึกไฟล์ Log เรียบร้อย:\n{filename}")

            except Exception as e:
                self.add_log(f"ไม่สามารถบันทึกไฟล์ Log: {e}", "error")
                messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถบันทึกไฟล์ได้:\n{e}")

    def refresh_logs(self):
        """Refresh logs from file"""
        try:
            log_file = Path(self.config.logging.log_file)
            if log_file.exists():
                with open(log_file, "r", encoding="utf-8") as f:
                    # Read last 50 lines
                    lines = f.readlines()
                    recent_lines = lines[-50:] if len(lines) > 50 else lines

                self.log_text.delete(1.0, tk.END)
                for line in recent_lines:
                    self.log_text.insert(tk.END, line)

                self.log_text.see(tk.END)
                self.add_log("รีเฟรช Log เรียบร้อย", "info")

        except Exception as e:
            self.add_log(f"ไม่สามารถรีเฟรช Log: {e}", "error")


class DENSO888MainWindow:
    """Main application window controller"""

    def __init__(self):
        # Initialize configuration
        try:
            self.config = get_config()
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            # Fallback configuration
            from config.settings import AppConfig

            self.config = AppConfig()

        # Initialize main window
        self.root = tk.Tk()
        self.theme = DENSO888Theme(self.config)

        # Initialize settings manager
        self.settings_manager = SettingsManager()

        # Processing components
        self.data_processor: Optional[Any] = None
        self.processing_thread: Optional[threading.Thread] = None

        # Setup application
        self._setup_error_handling()
        self._setup_logging()
        self._setup_window()
        self._init_components()
        self._setup_events()
        self._load_settings()

        logger.info("DENSO888 Application initialized successfully")

    def _setup_error_handling(self):
        """Setup global error handling"""
        setup_error_handling()

    def _setup_logging(self):
        """Setup logging with GUI integration"""

        def log_callback(message, level):
            """Callback for GUI log integration"""
            if hasattr(self, "logs_tab"):
                self.logs_tab.add_log(message, level)

        setup_gui_logger(log_callback)

    def _setup_window(self):
        """Initialize main window properties"""
        self.root.title(f"{self.config.app_name} v{self.config.version}")
        self.root.geometry(
            f"{self.config.ui.window_width}x{self.config.ui.window_height}"
        )
        self.root.minsize(self.config.ui.min_width, self.config.ui.min_height)

        # Apply theme
        self.theme.apply_to_root(self.root)

        # Center window
        self._center_window()

        # Set window icon (if available)
        self._set_window_icon()

    def _center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (self.config.ui.window_width // 2)
        y = (screen_height // 2) - (self.config.ui.window_height // 2)

        self.root.geometry(f"+{x}+{y}")

    def _set_window_icon(self):
        """Set window icon"""
        try:
            icon_path = Path("assets/icons/denso_icon.ico")
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except Exception as e:
            logger.debug(f"Could not set window icon: {e}")

    def _init_components(self):
        """Initialize GUI components"""
        # Header
        self.header = HeaderComponent(self.root, self.config)
        self.header.pack(fill="x", padx=20, pady=(20, 10))

        # Main notebook
        self.notebook = ttk.Notebook(self.root, style="Custom.TNotebook")
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)

        # Initialize tabs
        self.data_source_tab = DataSourceTab(
            self.notebook, self.config, self._on_tab_event
        )
        self.database_tab = DatabaseTab(self.notebook, self.config, self._on_tab_event)
        self.processing_tab = ProcessingTab(
            self.notebook, self.config, self._on_tab_event
        )
        self.logs_tab = LogsTab(self.notebook, self.config)

        # Add tabs to notebook
        self.notebook.add(self.data_source_tab.frame, text="📊 ข้อมูลต้นทาง")
        self.notebook.add(self.database_tab.frame, text="🗄️ ฐานข้อมูล")
        self.notebook.add(self.processing_tab.frame, text="⚡ ประมวลผล")
        self.notebook.add(self.logs_tab.frame, text="📋 บันทึก")

        # Footer
        self._create_footer()

    def _create_footer(self):
        """Create application footer"""
        footer_frame = ttk.Frame(self.root)
        footer_frame.pack(fill="x", side="bottom", padx=20, pady=(0, 20))

        # Status indicator
        status_frame = ttk.Frame(footer_frame)
        status_frame.pack(side="left")

        ttk.Label(status_frame, text="สถานะ:").pack(side="left")
        self.status_label = ttk.Label(
            status_frame,
            text="พร้อมใช้งาน",
            foreground=self.config.ui.theme_colors["success"],
        )
        self.status_label.pack(side="left", padx=(5, 0))

        # Version info
        version_info = f"{self.config.app_name} v{self.config.version}"
        ttk.Label(
            footer_frame,
            text=version_info,
            foreground=self.config.ui.theme_colors["accent"],
        ).pack(side="right")

    def _setup_events(self):
        """Setup event handlers"""
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    def _load_settings(self):
        """Load saved settings"""
        try:
            settings = self.settings_manager.load_settings()

            # Apply window settings
            window_settings = settings.get("window", {})
            if window_settings.get("geometry"):
                self.root.geometry(window_settings["geometry"])
            if window_settings.get("maximized"):
                self.root.state("zoomed")

        except Exception as e:
            logger.warning(f"Failed to load settings: {e}")

    def _save_settings(self):
        """Save current settings"""
        try:
            current_settings = self.settings_manager.load_settings()

            # Update window settings
            current_settings["window"]["geometry"] = self.root.geometry()
            current_settings["window"]["maximized"] = self.root.state() == "zoomed"

            self.settings_manager.save_settings(current_settings)

        except Exception as e:
            logger.warning(f"Failed to save settings: {e}")

    def _on_tab_event(self, event_type: str, data: Dict[str, Any]):
        """Handle tab events"""
        logger.debug(f"Tab event: {event_type}")

        if event_type == "data_source_changed":
            self.processing_tab.update_data_preview(data)
            self._check_processing_ready()

        elif event_type == "database_changed":
            self.processing_tab.update_database_status(data)
            self._check_processing_ready()

        elif event_type == "start_processing":
            self._start_processing()

        elif event_type == "stop_processing":
            self._stop_processing()

    def _check_processing_ready(self):
        """Check if processing is ready"""
        data_info = self.data_source_tab.get_data_info()
        db_info = self.database_tab.get_database_info()

        ready = data_info.get("has_valid_data", False) and db_info.get(
            "connection_status", {}
        ).get("connected", False)

        self.processing_tab.set_processing_enabled(ready)

        if ready:
            self._update_status("พร้อมประมวลผล", "success")
        else:
            self._update_status("ตรวจสอบข้อมูลและการเชื่อมต่อ", "warning")

    def _on_tab_changed(self, event):
        """Handle tab selection changes"""
        try:
            selected_tab = self.notebook.select()
            tab_text = self.notebook.tab(selected_tab, "text")
            logger.debug(f"Tab changed to: {tab_text}")
        except Exception as e:
            logger.warning(f"Tab change event error: {e}")

    def _start_processing(self):
        """Start data processing"""
        if self.processing_thread and self.processing_thread.is_alive():
            messagebox.showwarning("กำลังประมวลผล", "มีการประมวลผลข้อมูลอยู่แล้ว")
            return

        # Validate configurations
        if not self.data_source_tab.validate():
            return
        if not self.database_tab.validate():
            return

        try:
            # Import data processor
            from core.data_processor import DataProcessor

            # Create data processor with configurations
            self.data_processor = DataProcessor(
                data_source_config=self.data_source_tab.get_config(),
                database_config=self.database_tab.get_config(),
                processing_config=self.config.processing,
            )

            # Start processing thread
            self.processing_thread = threading.Thread(
                target=self._process_data_thread, daemon=True
            )
            self.processing_thread.start()

            # Update UI state
            self.processing_tab.set_processing_state(True)
            self._update_status("เริ่มประมวลผลข้อมูล...", "warning")

            # Switch to processing tab
            self.notebook.select(2)  # Processing tab index

            logger.info("Data processing started")

        except Exception as e:
            logger.error(f"Failed to start processing: {e}")
            messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถเริ่มการประมวลผลได้:\n{str(e)}")

    def _stop_processing(self):
        """Stop data processing"""
        if self.data_processor:
            self.data_processor.stop()

        self.processing_tab.set_processing_state(False)
        self._update_status("หยุดการประมวลผล", "warning")

        logger.info("Data processing stop requested")

    def _process_data_thread(self):
        """Data processing thread function"""
        try:
            # Setup callbacks for UI updates
            def progress_callback(progress_data):
                self.root.after(
                    0, lambda: self.processing_tab.update_progress(progress_data)
                )

            def log_callback(message, level="info"):
                self.root.after(0, lambda: self.logs_tab.add_log(message, level))

            # Run processing
            if not self.data_processor:
                raise RuntimeError("Data processor not initialized")

            result = self.data_processor.process(
                progress_callback=progress_callback, log_callback=log_callback
            )

            # Handle completion on main thread
            self.root.after(0, lambda: self._on_processing_complete(result))

        except Exception as e:
            logger.error(f"Processing thread error: {e}")
            self.root.after(0, lambda: self._on_processing_error(str(e)))

    def _on_processing_complete(self, result: Dict[str, Any]):
        """Handle processing completion"""
        self.processing_tab.set_processing_state(False)

        if result.get("success", False):
            self.processing_tab.show_results(result)
            self._update_status("ประมวลผลสำเร็จ", "success")

            # Show success notification
            rows_processed = result.get("rows_processed", 0)
            duration = result.get("duration", 0)
            table_name = result.get("table_name", "N/A")

            messagebox.showinfo(
                "ประมวลผลสำเร็จ",
                f"นำเข้าข้อมูลสำเร็จ!\n\n"
                f"📊 จำนวนแถว: {rows_processed:,}\n"
                f"⏱️ เวลาที่ใช้: {duration:.2f} วินาที\n"
                f"🗄️ ตาราง: {table_name}\n"
                f"⚡ ความเร็ว: {(rows_processed/duration if duration > 0 else 0):.0f} rows/sec",
            )

        else:
            error_msg = result.get("error", "Unknown error")
            self.processing_tab.show_error(error_msg)
            self._update_status("ประมวลผลล้มเหลว", "danger")

            messagebox.showerror("ข้อผิดพลาด", f"การประมวลผลล้มเหลว:\n{error_msg}")

        logger.info(f"Processing completed: {result.get('success', False)}")

    def _on_processing_error(self, error_message: str):
        """Handle processing error"""
        self.processing_tab.set_processing_state(False)
        self.processing_tab.show_error(error_message)
        self._update_status("เกิดข้อผิดพลาดในการประมวลผล", "danger")

        messagebox.showerror("ข้อผิดพลาด", f"เกิดข้อผิดพลาดในการประมวลผล:\n{error_message}")

        logger.error(f"Processing error: {error_message}")

    def _update_status(self, message: str, status_type: str = "info"):
        """Update footer status"""
        color_map = {
            "info": self.config.ui.theme_colors["accent"],
            "success": self.config.ui.theme_colors["success"],
            "warning": self.config.ui.theme_colors["warning"],
            "danger": self.config.ui.theme_colors["danger"],
        }

        self.status_label.configure(
            text=message, foreground=color_map.get(status_type, color_map["info"])
        )
        self.root.update_idletasks()

    def _on_closing(self):
        """Handle application closing"""
        try:
            # Check if processing is running
            if self.processing_thread and self.processing_thread.is_alive():
                result = messagebox.askyesnocancel(
                    "กำลังประมวลผล", "มีการประมวลผลข้อมูลอยู่ ต้องการหยุดและปิดโปรแกรมหรือไม่?"
                )

                if result is None:  # Cancel
                    return
                elif result:  # Yes - stop and close
                    self._stop_processing()
                    # Wait a moment for cleanup
                    self.root.after(1000, self._force_close)
                    return
                else:  # No - don't close
                    return

            self._force_close()

        except Exception as e:
            logger.error(f"Error during application closing: {e}")
            self._force_close()

    def _force_close(self):
        """Force close application"""
        try:
            # Save settings
            self._save_settings()

            # Close database connections
            if self.data_processor:
                self.data_processor.cleanup()

            # Close application
            self.root.destroy()
            logger.info("Application closed successfully")

        except Exception as e:
            logger.error(f"Error during force close: {e}")
            self.root.destroy()

    def run(self):
        """Start the application main loop"""
        try:
            logger.info("Starting DENSO888 GUI application")
            self.logs_tab.add_log("🚀 DENSO888 Application started", "info")

            # Show welcome message
            self.logs_tab.add_log("📋 เลือกประเภทข้อมูลในแท็บ 'ข้อมูลต้นทาง'", "info")
            self.logs_tab.add_log("🗄️ กำหนดค่าฐานข้อมูลในแท็บ 'ฐานข้อมูล'", "info")
            self.logs_tab.add_log("⚡ เริ่มประมวลผลในแท็บ 'ประมวลผล'", "info")

            # Start main loop
            self.root.mainloop()

        except KeyboardInterrupt:
            logger.info("Application interrupted by user")
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}")
            messagebox.showerror("ข้อผิดพลาดร้ายแรง", f"เกิดข้อผิดพลาดร้ายแรง:\n{str(e)}")
        finally:
            logger.info("Application terminated")


# Helper functions for standalone testing
def test_window():
    """Test window functionality"""
    try:
        app = DENSO888MainWindow()
        app.run()
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_window()
