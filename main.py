#!/usr/bin/env python3
"""
DENSO888 Excel to Database Pool System - Fixed Version
Enhanced Excel to SQL Server Import System with Connection Pooling
Created by: Thammaphon Chittasuwanna (SDM) | Innovation Department
Version: 3.0.0
"""

import sys
from pathlib import Path
import logging
from datetime import datetime

# Setup project paths FIRST
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))


def setup_environment():
    """Setup logging and required directories"""
    # Create required directories
    dirs = ["logs", "data", "backups", "exports", "temp", "config"]
    for dir_name in dirs:
        (PROJECT_ROOT / dir_name).mkdir(exist_ok=True)

    # Setup logging
    log_file = (
        PROJECT_ROOT / "logs" / f'denso888_{datetime.now().strftime("%Y%m%d")}.log'
    )
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

    logger = logging.getLogger(__name__)
    logger.info("🏭 DENSO888 Pool System Starting...")
    return logger


def check_dependencies():
    """Check critical dependencies"""
    required = {
        "pandas": "Excel processing",
        "openpyxl": "Excel reading",
        "sqlalchemy": "Database connectivity",
        "tkinter": "GUI framework",
    }

    missing = []
    for package, desc in required.items():
        try:
            if package == "tkinter":
                import tkinter
            else:
                __import__(package)
        except ImportError:
            missing.append(f"{package} ({desc})")

    if missing:
        print("❌ Missing dependencies:")
        for item in missing:
            print(f"   - {item}")
        print("\n💡 Install with: pip install pandas openpyxl sqlalchemy")
        return False
    return True


def create_missing_files():
    """Create missing files with basic implementations"""

    # Create basic pool_controller if missing
    pool_controller_path = Path("controllers/pool_controller.py")
    if not pool_controller_path.exists():
        pool_controller_path.parent.mkdir(exist_ok=True)
        with open(pool_controller_path, "w", encoding="utf-8") as f:
            f.write(
                '''"""
Enhanced Pool Controller - Production Ready
"""

import threading
from typing import Dict, Any, Callable
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class PoolController:
    """Enhanced Pool Controller with real functionality"""
    
    def __init__(self, pool_service):
        self.pool_service = pool_service
        self.event_callbacks = {}
        self.current_excel_file = None
        self.field_mappings = {}
        self.is_connected = False
        
    def register_callback(self, event, callback):
        """Register event callback"""
        if event not in self.event_callbacks:
            self.event_callbacks[event] = []
        self.event_callbacks[event].append(callback)
    
    def emit_event(self, event, data=None):
        """Emit event to callbacks"""
        if event in self.event_callbacks:
            for callback in self.event_callbacks[event]:
                try:
                    callback(data)
                except Exception as e:
                    logger.error(f"Event callback error: {e}")
    
    def test_database_connection(self, config):
        """Test database connection"""
        try:
            success = self.pool_service.connect_database(config)
            if success:
                self.pool_service.close_all_pools()  # Close test connection
                return True, "Connection test successful"
            return False, "Connection test failed"
        except Exception as e:
            return False, f"Connection error: {str(e)}"
    
    def connect_database(self, config):
        """Connect to database"""
        try:
            success = self.pool_service.connect_database(config)
            self.is_connected = success
            if success:
                self.emit_event("database_connected", config)
                return True, "Database connected successfully"
            return False, "Failed to connect to database"
        except Exception as e:
            return False, f"Connection error: {str(e)}"
        
    def disconnect(self):
        """Disconnect from database"""
        self.pool_service.close_all_pools()
        self.is_connected = False
        
    def cleanup(self):
        """Cleanup resources"""
        self.disconnect()
        
    def load_excel_file(self, file_path):
        """Load Excel file for analysis"""
        try:
            import pandas as pd
            
            # Read Excel file
            df = pd.read_excel(file_path, nrows=10)  # Sample for analysis
            
            file_info = {
                "file_path": file_path,
                "columns": list(df.columns),
                "sample_data": df.head(5).to_dict("records"),
                "total_rows": len(pd.read_excel(file_path)),
                "total_columns": len(df.columns)
            }
            
            self.current_excel_file = file_info
            self.emit_event("excel_loaded", file_info)
            return True, file_info
            
        except Exception as e:
            return False, {"error": str(e)}
        
    def get_tables(self):
        """Get database tables"""
        if not self.is_connected:
            return []
        return self.pool_service.get_tables()
        
    def get_table_schema(self, table_name):
        """Get table schema"""
        if not self.is_connected:
            return []
        return self.pool_service.get_table_schema(table_name)
        
    def auto_map_fields(self, table_name):
        """Auto-map Excel fields to database columns"""
        if not self.current_excel_file:
            return {}
            
        excel_columns = self.current_excel_file["columns"]
        db_columns = [col["name"] for col in self.get_table_schema(table_name)]
        
        mappings = {}
        for excel_col in excel_columns:
            # Simple matching logic
            excel_clean = excel_col.lower().replace(" ", "_")
            for db_col in db_columns:
                if excel_clean == db_col.lower():
                    mappings[excel_col] = db_col
                    break
                    
        self.field_mappings = mappings
        return mappings
        
    def get_import_preview(self, limit=5):
        """Get import preview data"""
        if not self.current_excel_file:
            return []
            
        sample_data = self.current_excel_file["sample_data"][:limit]
        return sample_data
        
    def import_data(self, table_name, options):
        """Import data to database"""
        def import_async():
            try:
                self.emit_event("import_progress", {"progress": 10, "status": "Starting import..."})
                
                # Read full Excel file
                import pandas as pd
                df = pd.read_excel(self.current_excel_file["file_path"])
                
                self.emit_event("import_progress", {"progress": 30, "status": "Processing data..."})
                
                # Apply field mappings
                if self.field_mappings:
                    df = df.rename(columns=self.field_mappings)
                
                # Convert to records
                data = df.to_dict("records")
                
                self.emit_event("import_progress", {"progress": 60, "status": "Importing to database..."})
                
                # Import using pool service
                success = self.pool_service.bulk_insert(table_name, data)
                
                if success:
                    self.emit_event("import_progress", {"progress": 100, "status": "Import completed!"})
                    self.emit_event("import_completed", {"table": table_name, "rows": len(data)})
                else:
                    self.emit_event("import_error", {"error": "Import failed"})
                    
            except Exception as e:
                self.emit_event("import_error", {"error": str(e)})
        
        threading.Thread(target=import_async, daemon=True).start()
        return True
        
    def get_connection_stats(self):
        """Get connection pool statistics"""
        return {
            "connected": self.is_connected,
            "total_connections": 5,  # Mock data
            "in_use_connections": 2,
            "available_connections": 3
        }
'''
            )

    # Create enhanced main_window if missing
    main_window_path = Path("gui/main_window.py")
    if not main_window_path.exists():
        main_window_path.parent.mkdir(exist_ok=True)
        with open(main_window_path, "w", encoding="utf-8") as f:
            f.write(
                '''"""
Enhanced Main Window - Production Ready
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class MainWindow:
    """Enhanced main window with pool functionality"""
    
    def __init__(self, controller=None, pool_controller=None):
        self.controller = controller
        self.pool_controller = pool_controller
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        self.setup_events()
        
        # State variables
        self.connected = False
        self.excel_loaded = False
        self.import_in_progress = False
        
    def setup_window(self):
        """Configure main window"""
        self.root.title("🏭 DENSO888 Professional - Excel to Database Pool System v3.0")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        
        # Configure grid
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
    def create_widgets(self):
        """Create and layout all widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew", rowspan=2)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Header with status
        self.create_header(main_frame)
        
        # Main notebook with all tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        
        # Create tabs
        self.create_database_tab()
        self.create_excel_tab()
        self.create_mapping_tab()
        self.create_import_tab()
        
        # Status bar
        self.create_status_bar()
        
    def create_header(self, parent):
        """Create header with title and connection status"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(
            header_frame,
            text="🏭 DENSO888 Professional - Excel to Database Pool System",
            font=("Arial", 16, "bold"),
        )
        title_label.grid(row=0, column=0, sticky="w")
        
        # Connection status
        status_frame = ttk.Frame(header_frame)
        status_frame.grid(row=0, column=1, sticky="e")
        
        self.conn_status = ttk.Label(
            status_frame, text="🔴 Disconnected", foreground="red"
        )
        self.conn_status.pack(side="right", padx=(10, 0))
        
    def create_database_tab(self):
        """Create database connection tab"""
        db_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(db_frame, text="🔗 Database Connection")
        
        # Database type selection
        type_frame = ttk.LabelFrame(db_frame, text="Database Type", padding="15")
        type_frame.pack(fill="x", pady=(0, 15))
        
        self.db_type = tk.StringVar(value="sqlite")
        ttk.Radiobutton(
            type_frame,
            text="SQLite (Local Database)",
            variable=self.db_type,
            value="sqlite",
            command=self.on_db_type_change,
        ).pack(anchor="w", pady=5)
        ttk.Radiobutton(
            type_frame,
            text="SQL Server (SSMS)",
            variable=self.db_type,
            value="sqlserver",
            command=self.on_db_type_change,
        ).pack(anchor="w", pady=5)
        
        # Connection details
        self.conn_details_frame = ttk.LabelFrame(
            db_frame, text="Connection Details", padding="15"
        )
        self.conn_details_frame.pack(fill="x", pady=(0, 15))
        self.create_connection_fields()
        
        # Connection buttons
        btn_frame = ttk.Frame(db_frame)
        btn_frame.pack(fill="x")
        
        ttk.Button(
            btn_frame, text="🔍 Test Connection", command=self.test_connection
        ).pack(side="left", padx=(0, 10))
        ttk.Button(btn_frame, text="🔗 Connect", command=self.connect_database).pack(
            side="left", padx=(0, 10)
        )
        ttk.Button(
            btn_frame, text="❌ Disconnect", command=self.disconnect_database
        ).pack(side="left")
        
    def create_excel_tab(self):
        """Create Excel file tab"""
        excel_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(excel_frame, text="📊 Excel File")
        
        # File selection
        file_frame = ttk.LabelFrame(excel_frame, text="Select Excel File", padding="15")
        file_frame.pack(fill="x", pady=(0, 15))
        
        file_input_frame = ttk.Frame(file_frame)
        file_input_frame.pack(fill="x")
        
        self.excel_path = tk.StringVar()
        ttk.Entry(file_input_frame, textvariable=self.excel_path).pack(
            side="left", fill="x", expand=True
        )
        ttk.Button(file_input_frame, text="📁 Browse", command=self.browse_excel).pack(
            side="right", padx=(10, 0)
        )
        
        # Load button
        ttk.Button(
            file_frame, text="📊 Load & Analyze File", command=self.load_excel
        ).pack(pady=(15, 0))
        
        # File info display
        info_frame = ttk.LabelFrame(excel_frame, text="File Information", padding="15")
        info_frame.pack(fill="both", expand=True)
        
        self.excel_info_text = tk.Text(
            info_frame, height=15, state="disabled", wrap="word"
        )
        info_scroll = ttk.Scrollbar(
            info_frame, orient="vertical", command=self.excel_info_text.yview
        )
        self.excel_info_text.configure(yscrollcommand=info_scroll.set)
        
        self.excel_info_text.pack(side="left", fill="both", expand=True)
        info_scroll.pack(side="right", fill="y")
        
    def create_mapping_tab(self):
        """Create field mapping tab"""
        mapping_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(mapping_frame, text="🔗 Field Mapping")
        
        # Table selection
        table_frame = ttk.LabelFrame(mapping_frame, text="Target Table", padding="15")
        table_frame.pack(fill="x", pady=(0, 15))
        
        table_select_frame = ttk.Frame(table_frame)
        table_select_frame.pack(fill="x")
        
        self.target_table = tk.StringVar()
        self.table_combo = ttk.Combobox(
            table_select_frame, textvariable=self.target_table, state="readonly"
        )
        self.table_combo.pack(side="left", fill="x", expand=True)
        self.table_combo.bind("<<ComboboxSelected>>", self.on_table_select)
        
        ttk.Button(
            table_select_frame, text="🔄 Refresh", command=self.refresh_tables
        ).pack(side="right", padx=(10, 0))
        
        # Mapping display
        map_frame = ttk.LabelFrame(mapping_frame, text="Column Mappings", padding="15")
        map_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Mapping treeview
        columns = ("excel_column", "db_column", "data_type", "sample_data")
        self.mapping_tree = ttk.Treeview(
            map_frame, columns=columns, show="headings", height=12
        )
        
        self.mapping_tree.heading("excel_column", text="Excel Column")
        self.mapping_tree.heading("db_column", text="Database Column")
        self.mapping_tree.heading("data_type", text="Data Type")
        self.mapping_tree.heading("sample_data", text="Sample Data")
        
        self.mapping_tree.column("excel_column", width=200)
        self.mapping_tree.column("db_column", width=200)
        self.mapping_tree.column("data_type", width=100)
        self.mapping_tree.column("sample_data", width=250)
        
        map_scroll = ttk.Scrollbar(
            map_frame, orient="vertical", command=self.mapping_tree.yview
        )
        self.mapping_tree.configure(yscrollcommand=map_scroll.set)
        
        self.mapping_tree.pack(side="left", fill="both", expand=True)
        map_scroll.pack(side="right", fill="y")
        
        # Mapping buttons
        map_btn_frame = ttk.Frame(mapping_frame)
        map_btn_frame.pack(fill="x")
        
        ttk.Button(
            map_btn_frame, text="🎯 Auto Map Fields", command=self.auto_map_fields
        ).pack(side="left", padx=(0, 10))
        ttk.Button(
            map_btn_frame, text="🗑️ Clear Mappings", command=self.clear_mappings
        ).pack(side="left")
        
    def create_import_tab(self):
        """Create data import tab"""
        import_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(import_frame, text="⬆️ Import Data")
        
        # Import options
        options_frame = ttk.LabelFrame(
            import_frame, text="Import Options", padding="15"
        )
        options_frame.pack(fill="x", pady=(0, 15))
        
        options_grid = ttk.Frame(options_frame)
        options_grid.pack(fill="x")
        
        ttk.Label(options_grid, text="Batch Size:").grid(
            row=0, column=0, sticky="w", padx=(0, 10)
        )
        self.batch_size = tk.StringVar(value="1000")
        ttk.Entry(options_grid, textvariable=self.batch_size, width=10).grid(
            row=0, column=1, sticky="w"
        )
        
        ttk.Label(options_grid, text="Import Mode:").grid(
            row=0, column=2, sticky="w", padx=(20, 10)
        )
        self.import_mode = tk.StringVar(value="append")
        mode_combo = ttk.Combobox(
            options_grid,
            textvariable=self.import_mode,
            values=["append", "replace", "update"],
            state="readonly",
            width=10,
        )
        mode_combo.grid(row=0, column=3, sticky="w")
        
        # Progress section
        progress_frame = ttk.LabelFrame(
            import_frame, text="Import Progress", padding="15"
        )
        progress_frame.pack(fill="x", pady=(0, 15))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame, variable=self.progress_var, maximum=100, length=500
        )
        self.progress_bar.pack(fill="x", pady=(0, 10))
        
        self.progress_label = ttk.Label(progress_frame, text="Ready to import")
        self.progress_label.pack()
        
        # Import controls
        import_btn_frame = ttk.Frame(import_frame)
        import_btn_frame.pack(fill="x", pady=(0, 15))
        
        self.import_btn = ttk.Button(
            import_btn_frame,
            text="🚀 Start Import",
            command=self.start_import,
        )
        self.import_btn.pack(side="left", padx=(0, 10))
        
        ttk.Button(
            import_btn_frame, text="👁️ Preview Data", command=self.preview_import
        ).pack(side="left")
        
        # Results display
        results_frame = ttk.LabelFrame(
            import_frame, text="Import Results", padding="15"
        )
        results_frame.pack(fill="both", expand=True)
        
        self.results_text = tk.Text(
            results_frame, height=8, state="disabled", wrap="word"
        )
        results_scroll = ttk.Scrollbar(
            results_frame, orient="vertical", command=self.results_text.yview
        )
        self.results_text.configure(yscrollcommand=results_scroll.set)
        
        self.results_text.pack(side="left", fill="both", expand=True)
        results_scroll.pack(side="right", fill="y")
        
    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        
        self.status_text = ttk.Label(
            self.status_bar, text="🏭 DENSO888 Professional System Ready"
        )
        self.status_text.pack(side="left")
        
    def setup_events(self):
        """Setup event handlers"""
        if self.pool_controller:
            self.pool_controller.register_callback(
                "database_connected", self.on_database_connected
            )
            self.pool_controller.register_callback("excel_loaded", self.on_excel_loaded)
            self.pool_controller.register_callback(
                "import_progress", self.on_import_progress
            )
            self.pool_controller.register_callback(
                "import_completed", self.on_import_completed
            )
            self.pool_controller.register_callback("import_error", self.on_import_error)
            
    # [Additional methods for database operations, file handling, etc.]
    def on_db_type_change(self):
        """Handle database type change"""
        self.create_connection_fields()
        
    def create_connection_fields(self):
        """Create connection input fields based on database type"""
        # Clear existing widgets
        for widget in self.conn_details_frame.winfo_children():
            widget.destroy()
            
        if self.db_type.get() == "sqlite":
            ttk.Label(self.conn_details_frame, text="Database File:").grid(
                row=0, column=0, sticky="w", pady=5
            )
            self.sqlite_path = tk.StringVar(value="data/denso888.db")
            ttk.Entry(
                self.conn_details_frame, textvariable=self.sqlite_path, width=50
            ).grid(row=0, column=1, sticky="ew", padx=(10, 0))
            
            self.conn_details_frame.grid_columnconfigure(1, weight=1)
            
        else:  # SQL Server
            ttk.Label(self.conn_details_frame, text="Server:").grid(
                row=0, column=0, sticky="w", pady=2
            )
            self.server = tk.StringVar(value="localhost\\\\SQLEXPRESS")
            ttk.Entry(self.conn_details_frame, textvariable=self.server, width=40).grid(
                row=0, column=1, sticky="ew", padx=(10, 0)
            )
            
            ttk.Label(self.conn_details_frame, text="Database:").grid(
                row=1, column=0, sticky="w", pady=2
            )
            self.database = tk.StringVar()
            ttk.Entry(self.conn_details_frame, textvariable=self.database, width=40).grid(
                row=1, column=1, sticky="ew", padx=(10, 0)
            )
            
            self.conn_details_frame.grid_columnconfigure(1, weight=1)
            
    def get_connection_config(self):
        """Get connection configuration"""
        if self.db_type.get() == "sqlite":
            return {"type": "sqlite", "file": self.sqlite_path.get()}
        else:
            return {
                "type": "sqlserver",
                "server": self.server.get(),
                "database": self.database.get(),
                "use_windows_auth": True,
            }
            
    def test_connection(self):
        """Test database connection"""
        config = self.get_connection_config()
        if not config:
            return
            
        def test_async():
            if self.pool_controller:
                success, message = self.pool_controller.test_database_connection(config)
            else:
                success, message = False, "Pool controller not available"
            self.root.after(0, lambda: self.show_test_result(success, message))
            
        threading.Thread(target=test_async, daemon=True).start()
        self.update_status("Testing connection...")
        
    def connect_database(self):
        """Connect to database"""
        config = self.get_connection_config()
        if not config:
            return
            
        def connect_async():
            if self.pool_controller:
                success, message = self.pool_controller.connect_database(config)
            else:
                success, message = False, "Pool controller not available"
            self.root.after(0, lambda: self.handle_connect_result(success, message))
            
        threading.Thread(target=connect_async, daemon=True).start()
        self.update_status("Connecting to database...")
        
    def disconnect_database(self):
        """Disconnect from database"""
        if self.pool_controller:
            self.pool_controller.disconnect()
        self.connected = False
        self.conn_status.config(text="🔴 Disconnected", foreground="red")
        self.update_status("Disconnected from database")
        
    def show_test_result(self, success, message):
        """Show connection test result"""
        if success:
            messagebox.showinfo("Connection Test", f"✅ {message}")
        else:
            messagebox.showerror("Connection Test", f"❌ {message}")
        self.update_status("Ready")
        
    def handle_connect_result(self, success, message):
        """Handle connection result"""
        if success:
            self.connected = True
            self.conn_status.config(text="🟢 Connected", foreground="green")
            self.update_status("Database connected successfully")
            self.refresh_tables()
        else:
            messagebox.showerror("Connection Error", f"❌ {message}")
            self.update_status("Connection failed")
            
    def browse_excel(self):
        """Browse for Excel file"""
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls *.xlsm"), ("All files", "*.*")],
        )
        if file_path:
            self.excel_path.set(file_path)
            
    def load_excel(self):
        """Load Excel file"""
        file_path = self.excel_path.get()
        if not file_path:
            messagebox.showwarning("Warning", "Please select an Excel file")
            return
            
        def load_async():
            if self.pool_controller:
                success, result = self.pool_controller.load_excel_file(file_path)
            else:
                success, result = False, {"error": "Pool controller not available"}
            self.root.after(0, lambda: self.handle_excel_result(success, result))
            
        threading.Thread(target=load_async, daemon=True).start()
        self.update_status("Loading Excel file...")
        
    def handle_excel_result(self, success, result):
        """Handle Excel load result"""
        if success:
            self.excel_loaded = True
            self.display_excel_info(result)
            self.update_status(f"Excel loaded: {result.get('total_rows', 0)} rows")
        else:
            messagebox.showerror(
                "Excel Error", f"❌ {result.get('error', 'Unknown error')}"
            )
            self.update_status("Excel load failed")
            
    def display_excel_info(self, info):
        """Display Excel file information"""
        self.excel_info_text.config(state="normal")
        self.excel_info_text.delete(1.0, tk.END)
        
        content = f"""📁 File: {Path(info.get('file_path', '')).name}
📊 Total Rows: {info.get('total_rows', 0):,}
📋 Columns: {len(info.get('columns', []))}

📝 Column Details:
"""
        for i, col in enumerate(info.get("columns", []), 1):
            content += f"  {i:2d}. {col}\n"

        content += f"\n🔍 Sample Data (first 5 rows):\n"
        for i, row in enumerate(info.get("sample_data", []), 1):
            content += f"\n--- Row {i} ---\n"
            for col, value in row.items():
                content += f"{col}: {value}\n"

        self.excel_info_text.insert(1.0, content)
        self.excel_info_text.config(state="disabled")
        
    def refresh_tables(self):
        """Refresh table list"""
        if not self.connected or not self.pool_controller:
            return
            
        def refresh_async():
            tables = self.pool_controller.get_tables()
            self.root.after(0, lambda: self.update_table_list(tables))
            
        threading.Thread(target=refresh_async, daemon=True).start()
        
    def update_table_list(self, tables):
        """Update table combobox"""
        self.table_combo["values"] = tables
        if tables:
            self.table_combo.current(0)
            self.update_status(f"Found {len(tables)} tables")
            
    def on_table_select(self, event=None):
        """Handle table selection"""
        table_name = self.target_table.get()
        if table_name and self.excel_loaded:
            self.populate_mappings(table_name)
            
    def populate_mappings(self, table_name):
        """Populate field mappings"""
        # Clear existing
        for item in self.mapping_tree.get_children():
            self.mapping_tree.delete(item)
            
        def populate_async():
            if self.pool_controller:
                schema = self.pool_controller.get_table_schema(table_name)
                excel_columns = (
                    self.pool_controller.current_excel_file.get("columns", [])
                    if self.pool_controller.current_excel_file
                    else []
                )
                sample_data = (
                    self.pool_controller.current_excel_file.get("sample_data", [])
                    if self.pool_controller.current_excel_file
                    else []
                )
                self.root.after(
                    0, lambda: self.display_mappings(excel_columns, schema, sample_data)
                )
                
        threading.Thread(target=populate_async, daemon=True).start()
        
    def display_mappings(self, excel_columns, schema, sample_data):
        """Display mapping options"""
        db_columns = [col["name"] for col in schema]
        
        for i, excel_col in enumerate(excel_columns):
            # Get sample data for this column
            sample_value = ""
            if sample_data and len(sample_data) > 0:
                sample_value = str(sample_data[0].get(excel_col, ""))[:50]
                
            # Auto-suggest mapping
            suggested_db_col = ""
            for db_col in db_columns:
                if excel_col.lower().replace(" ", "_") == db_col.lower():
                    suggested_db_col = db_col
                    break
                    
            self.mapping_tree.insert(
                "", "end", values=(excel_col, suggested_db_col, "AUTO", sample_value)
            )
            
    def auto_map_fields(self):
        """Auto-map fields"""
        table_name = self.target_table.get()
        if not table_name:
            messagebox.showwarning("Warning", "Please select a target table")
            return
            
        def map_async():
            if self.pool_controller:
                mappings = self.pool_controller.auto_map_fields(table_name)
                self.root.after(0, lambda: self.update_mappings_display(mappings))
                
        threading.Thread(target=map_async, daemon=True).start()
        
    def update_mappings_display(self, mappings):
        """Update mappings display"""
        for item in self.mapping_tree.get_children():
            excel_col = self.mapping_tree.item(item)["values"][0]
            if excel_col in mappings:
                values = list(self.mapping_tree.item(item)["values"])
                values[1] = mappings[excel_col]  # Update db_column
                self.mapping_tree.item(item, values=values)
                
        self.update_status(f"Auto-mapped {len(mappings)} fields")
        
    def clear_mappings(self):
        """Clear all mappings"""
        for item in self.mapping_tree.get_children():
            values = list(self.mapping_tree.item(item)["values"])
            values[1] = ""  # Clear db_column
            self.mapping_tree.item(item, values=values)
            
        self.update_status("Mappings cleared")
        
    def preview_import(self):
        """Preview import data"""
        if not self.excel_loaded:
            messagebox.showwarning("Warning", "Please load Excel file first")
            return
            
        if self.pool_controller:
            preview_data = self.pool_controller.get_import_preview(5)
            if preview_data:
                preview_text = "Preview of mapped data:\n\n"
                for i, row in enumerate(preview_data, 1):
                    preview_text += f"Row {i}:\n"
                    for col, value in row.items():
                        preview_text += f"  {col}: {value}\n"
                    preview_text += "\n"
                messagebox.showinfo("Import Preview", preview_text)
            else:
                messagebox.showinfo("Preview", "No preview data available")
                
    def start_import(self):
        """Start data import"""
        if not self.connected:
            messagebox.showwarning("Warning", "Please connect to database first")
            return
            
        if not self.excel_loaded:
            messagebox.showwarning("Warning", "Please load Excel file first")
            return
            
        table_name = self.target_table.get()
        if not table_name:
            messagebox.showwarning("Warning", "Please select target table")
            return
            
        # Validate mappings
        mapped_count = 0
        for item in self.mapping_tree.get_children():
            if self.mapping_tree.item(item)["values"][1]:
                mapped_count += 1
                
        if mapped_count == 0:
            messagebox.showwarning("Warning", "Please map at least one field")
            return
            
        # Confirm import
        if not messagebox.askyesno(
            "Confirm Import",
            f"Import data to table '{table_name}'?\nMapped fields: {mapped_count}\nMode: {self.import_mode.get()}",
        ):
            return
            
        # Start import
        self.import_in_progress = True
        self.import_btn.config(state="disabled", text="Importing...")
        
        options = {
            "batch_size": int(self.batch_size.get() or 1000),
            "mode": self.import_mode.get(),
        }
        
        if self.pool_controller:
            self.pool_controller.import_data(table_name, options)
            
    # Event handlers
    def on_database_connected(self, data):
        """Handle database connected event"""
        pass  # Already handled in handle_connect_result
        
    def on_excel_loaded(self, data):
        """Handle Excel loaded event"""
        pass  # Already handled in handle_excel_result
        
    def on_import_progress(self, data):
        """Handle import progress"""
        progress = data.get("progress", 0)
        status = data.get("status", "Processing...")
        
        self.progress_var.set(progress)
        self.progress_label.config(text=status)
        self.update_status(f"Import: {progress}% - {status}")
        
    def on_import_completed(self, data):
        """Handle import completion"""
        from datetime import datetime
        
        self.import_in_progress = False
        self.import_btn.config(state="normal", text="🚀 Start Import")
        
        rows = data.get("rows", 0)
        table = data.get("table", "")
        
        result_msg = f"✅ Import completed successfully!\nTable: {table}\nRows imported: {rows:,}"
        
        self.results_text.config(state="normal")
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.results_text.insert(
            tk.END, f"\n[{timestamp}] {result_msg}\n" + "=" * 60 + "\n"
        )
        self.results_text.config(state="disabled")
        self.results_text.see(tk.END)
        
        self.update_status("Import completed successfully")
        messagebox.showinfo("Import Complete", result_msg)
        
    def on_import_error(self, data):
        """Handle import error"""
        from datetime import datetime
        
        self.import_in_progress = False
        self.import_btn.config(state="normal", text="🚀 Start Import")
        
        error = data.get("error", "Unknown error")
        error_msg = f"❌ Import failed: {error}"
        
        self.results_text.config(state="normal")
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.results_text.insert(
            tk.END, f"\n[{timestamp}] {error_msg}\n" + "=" * 60 + "\n"
        )
        self.results_text.config(state="disabled")
        self.results_text.see(tk.END)
        
        self.update_status("Import failed")
        messagebox.showerror("Import Error", error_msg)
        
    def update_status(self, message):
        """Update status bar"""
        self.status_text.config(text=message)
        
    def run(self):
        """Start the GUI application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Show startup message
        self.update_status("🏭 DENSO888 Professional System Ready")
        
        # Start main loop
        self.root.mainloop()
        
    def on_closing(self):
        """Handle window closing"""
        if self.import_in_progress:
            if not messagebox.askyesno(
                "Exit", "Import in progress. Are you sure you want to exit?"
            ):
                return
                
        try:
            # Cleanup controllers
            if self.pool_controller:
                self.pool_controller.cleanup()
            if self.controller:
                self.controller.cleanup()
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
            
        self.root.destroy()
'''
            )


def ensure_basic_structure():
    """Ensure basic project structure exists"""
    dirs = ["controllers", "gui", "services", "core", "logs", "data"]
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)

    # Create __init__.py files
    for dir_name in ["controllers", "gui", "services", "core"]:
        init_file = Path(dir_name) / "__init__.py"
        if not init_file.exists():
            init_file.touch()


def main():
    """Main application entry point"""
    try:
        # Setup environment first
        logger = setup_environment()

        # Ensure basic structure
        ensure_basic_structure()

        # Check dependencies
        if not check_dependencies():
            input("Press Enter to exit...")
            sys.exit(1)

        # Import main application (after dependency check)
        try:
            from gui.main_window import MainWindow
            from services.connection_pool_service import ConnectionPoolService
            from controllers.pool_controller import PoolController
            from controllers.app_controller import AppController
        except ImportError as e:
            logger.error(f"Failed to import modules: {e}")
            print("❌ Import failed. Creating missing files...")
            create_missing_files()

            # Try importing again after creating files
            try:
                from gui.main_window import MainWindow
                from services.connection_pool_service import ConnectionPoolService
                from controllers.pool_controller import PoolController
            except ImportError as e2:
                logger.error(f"Still failed to import after creating files: {e2}")
                print("❌ Critical import failure. Please check file structure.")
                input("Press Enter to exit...")
                sys.exit(1)

        logger.info("✅ Dependencies OK - Initializing System")

        # Initialize services
        pool_service = ConnectionPoolService()
        pool_controller = PoolController(pool_service)

        # Try to create app controller (fallback if not available)
        try:
            app_controller = AppController()
        except Exception as e:
            logger.warning(f"AppController not available: {e}")
            app_controller = None

        # Create and run main window
        app = MainWindow(controller=app_controller, pool_controller=pool_controller)
        logger.info("🚀 Starting DENSO888 System GUI")
        app.run()

    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("🔧 Please check file structure and dependencies")
        input("Press Enter to exit...")
        sys.exit(1)

    except Exception as e:
        logger.error(f"❌ Application Error: {e}")
        print(f"❌ Error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    main()
