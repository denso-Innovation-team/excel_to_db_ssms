"""
Unified Main Window - Complete DENSO888 Excel to Database System
Combines both Pool System and General Features
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from pathlib import Path
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class MainWindow:
    """Unified main window for DENSO888 system"""

    def __init__(self, controller=None, pool_controller=None):
        # Support both controllers
        self.controller = controller  # Original app controller
        self.pool_controller = pool_controller  # Pool controller

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
        self.root.title("🏭 DENSO888 Professional - Excel to Database System v3.0")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)

        # Configure grid
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Set window icon
        try:
            self.root.iconbitmap("assets/icon.ico")
        except:
            pass

    def create_widgets(self):
        """Create and layout all widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="5")
        main_frame.grid(row=0, column=0, sticky="nsew", rowspan=2)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Header with status
        self.create_header(main_frame)

        # Main notebook with all tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky="nsew", pady=(5, 0))

        # Create all tabs
        self.create_pool_tabs()  # Pool system tabs
        self.create_general_tabs()  # General system tabs

        # Status bar
        self.create_status_bar()

    def create_header(self, parent):
        """Create header with title and connection status"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        header_frame.grid_columnconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(
            header_frame,
            text="🏭 DENSO888 Professional - Excel to Database System",
            font=("Arial", 14, "bold"),
        )
        title_label.grid(row=0, column=0, sticky="w")

        # Connection status frame
        status_frame = ttk.Frame(header_frame)
        status_frame.grid(row=0, column=1, sticky="e")

        self.conn_status = ttk.Label(
            status_frame, text="🔴 Disconnected", foreground="red"
        )
        self.conn_status.pack(side="right", padx=(10, 0))

        # Mode indicator
        self.mode_label = ttk.Label(status_frame, text="Pool Mode", foreground="blue")
        self.mode_label.pack(side="right", padx=(10, 0))

    def create_pool_tabs(self):
        """Create Pool System specific tabs"""
        
        # 1. Database Tab
        from gui.components.database_tab import DatabaseTab
        self.db_tab = DatabaseTab(
            self.notebook,
            callbacks={
                "test": self.test_connection,
                "connect": self.connect_database,
                "disconnect": self.disconnect_database
            }
        )
        self.notebook.add(self.db_tab.get_widget(), text="🔗 Database")

        # 2. EXCEL FILE TAB
        excel_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(excel_frame, text="📊 Excel File")

        # File selection
        file_frame = ttk.LabelFrame(excel_frame, text="Select Excel File", padding="10")
        file_frame.pack(fill="x", pady=(0, 10))

        file_input_frame = ttk.Frame(file_frame)
        file_input_frame.pack(fill="x")

        self.excel_path = tk.StringVar()
        ttk.Entry(file_input_frame, textvariable=self.excel_path).pack(
            side="left", fill="x", expand=True
        )
        ttk.Button(file_input_frame, text="Browse", command=self.browse_excel).pack(
            side="right", padx=(10, 0)
        )

        # Load button
        ttk.Button(
            file_frame, text="Load & Analyze File", command=self.load_excel
        ).pack(pady=(10, 0))

        # File info display
        info_frame = ttk.LabelFrame(excel_frame, text="File Information", padding="10")
        info_frame.pack(fill="both", expand=True)

        self.excel_info_text = tk.Text(
            info_frame, height=20, state="disabled", wrap="word"
        )
        info_scroll = ttk.Scrollbar(
            info_frame, orient="vertical", command=self.excel_info_text.yview
        )
        self.excel_info_text.configure(yscrollcommand=info_scroll.set)

        self.excel_info_text.pack(side="left", fill="both", expand=True)
        info_scroll.pack(side="right", fill="y")

        # 3. FIELD MAPPING TAB
        mapping_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(mapping_frame, text="🔗 Field Mapping")

        # Table selection
        table_frame = ttk.LabelFrame(mapping_frame, text="Target Table", padding="10")
        table_frame.pack(fill="x", pady=(0, 10))

        table_select_frame = ttk.Frame(table_frame)
        table_select_frame.pack(fill="x")

        self.target_table = tk.StringVar()
        self.table_combo = ttk.Combobox(
            table_select_frame, textvariable=self.target_table, state="readonly"
        )
        self.table_combo.pack(side="left", fill="x", expand=True)
        self.table_combo.bind("<<ComboboxSelected>>", self.on_table_select)

        ttk.Button(
            table_select_frame, text="Refresh", command=self.refresh_tables
        ).pack(side="right", padx=(10, 0))

        # Mapping display
        map_frame = ttk.LabelFrame(mapping_frame, text="Column Mappings", padding="10")
        map_frame.pack(fill="both", expand=True, pady=(0, 10))

        # Mapping treeview
        columns = ("excel_column", "db_column", "data_type", "sample_data")
        self.mapping_tree = ttk.Treeview(
            map_frame, columns=columns, show="headings", height=15
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

        # Mapping control buttons
        map_btn_frame = ttk.Frame(mapping_frame)
        map_btn_frame.pack(fill="x")

        ttk.Button(
            map_btn_frame, text="Auto Map Fields", command=self.auto_map_fields
        ).pack(side="left", padx=(0, 10))
        ttk.Button(
            map_btn_frame, text="Clear Mappings", command=self.clear_mappings
        ).pack(side="left", padx=(0, 10))
        ttk.Button(
            map_btn_frame, text="Validate Mappings", command=self.validate_mappings
        ).pack(side="left")

        # 4. IMPORT DATA TAB
        import_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(import_frame, text="⬆️ Import Data")

        # Import options
        options_frame = ttk.LabelFrame(
            import_frame, text="Import Options", padding="10"
        )
        options_frame.pack(fill="x", pady=(0, 10))

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
            import_frame, text="Import Progress", padding="10"
        )
        progress_frame.pack(fill="x", pady=(0, 10))

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame, variable=self.progress_var, maximum=100, length=400
        )
        self.progress_bar.pack(fill="x", pady=(0, 5))

        self.progress_label = ttk.Label(progress_frame, text="Ready to import")
        self.progress_label.pack()

        # Import controls
        import_btn_frame = ttk.Frame(import_frame)
        import_btn_frame.pack(fill="x", pady=(0, 10))

        self.import_btn = ttk.Button(
            import_btn_frame,
            text="🚀 Start Import",
            command=self.start_import,
            style="Accent.TButton",
        )
        self.import_btn.pack(side="left", padx=(0, 10))

        ttk.Button(
            import_btn_frame, text="📊 Preview Data", command=self.preview_import
        ).pack(side="left")

        # Results display
        results_frame = ttk.LabelFrame(
            import_frame, text="Import Results", padding="10"
        )
        results_frame.pack(fill="both", expand=True)

        self.results_text = tk.Text(
            results_frame, height=10, state="disabled", wrap="word"
        )
        results_scroll = ttk.Scrollbar(
            results_frame, orient="vertical", command=self.results_text.yview
        )
        self.results_text.configure(yscrollcommand=results_scroll.set)

        self.results_text.pack(side="left", fill="both", expand=True)
        results_scroll.pack(side="right", fill="y")

    def create_general_tabs(self):
        """Create general system tabs"""

        # LOGS TAB
        logs_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(logs_frame, text="📝 Logs")

        self.log_text = tk.Text(logs_frame, height=25, state="disabled", wrap="word")
        log_scroll = ttk.Scrollbar(
            logs_frame, orient="vertical", command=self.log_text.yview
        )
        self.log_text.configure(yscrollcommand=log_scroll.set)

        self.log_text.pack(side="left", fill="both", expand=True)
        log_scroll.pack(side="right", fill="y")

        # Load recent logs
        self.load_recent_logs()

    def get_connection_config(self):
        """Get connection configuration"""
        return self.db_tab.get_config()

    # Database Operations
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

    # Excel Operations
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

        content = f"""📁 File: {info.get('file_name', 'Unknown')}
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

    # Table and Mapping Operations
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

    def validate_mappings(self):
        """Validate current mappings"""
        mapped_count = 0
        errors = []

        for item in self.mapping_tree.get_children():
            values = self.mapping_tree.item(item)["values"]
            if values[1]:  # Has db_column mapping
                mapped_count += 1

        if mapped_count == 0:
            errors.append("No field mappings defined")

        if errors:
            messagebox.showwarning("Validation", "\n".join(errors))
        else:
            messagebox.showinfo(
                "Validation", f"✅ {mapped_count} field mappings are valid"
            )

    # Import Operations
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
            f"Import data to table '{table_name}'?\n"
            f"Mapped fields: {mapped_count}\n"
            f"Mode: {self.import_mode.get()}",
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

    # Event Handlers
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

        # Update connection stats
        if self.pool_controller:
            stats = self.pool_controller.get_connection_stats()
            self.stats_text.config(
                text=f"Pool: {stats.get('in_use_connections', 0)}/{stats.get('total_connections', 0)} connections"
            )

    def on_import_error(self, data):
        """Handle import error"""
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

    # Utility Methods
    def load_recent_logs(self):
        """Load recent application logs"""
        try:
            log_file = (
                Path("logs") / f"denso888_{datetime.now().strftime('%Y%m%d')}.log"
            )
            if log_file.exists():
                with open(log_file, "r", encoding="utf-8") as f:
                    logs = f.read()

                self.log_text.config(state="normal")
                self.log_text.delete(1.0, tk.END)
                self.log_text.insert(1.0, logs)
                self.log_text.config(state="disabled")
                self.log_text.see(tk.END)
        except Exception as e:
            logger.error(f"Failed to load logs: {e}")

    def update_status(self, message):
        """Update status bar"""
        self.status_text.config(text=message)

        # Auto-refresh logs periodically
        self.root.after(5000, self.refresh_logs)

    def refresh_logs(self):
        """Refresh logs display"""
        if (
            self.notebook.index(self.notebook.select()) == len(self.notebook.tabs()) - 1
        ):  # Logs tab is active
            self.load_recent_logs()

    def run(self):
        """Start the GUI application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Show startup message
        self.update_status("DENSO888 Professional System Ready")

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
            self.pool_controller.import_data(table_name, options)

    # Event Handlers
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

        # Update connection stats
        if self.pool_controller:
            stats = self.pool_controller.get_connection_stats()
            self.stats_text.config(
                text=f"Pool: {stats.get('in_use_connections', 0)}/{stats.get('total_connections', 0)} connections"
            )

    def on_import_error(self, data):
        """Handle import error"""
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

    # Utility Methods
    def update_status(self, message):
        """Update status bar"""
        self.status_text.config(text=message)

        # Auto-refresh logs periodically
        self.root.after(5000, self.refresh_logs)

    def refresh_logs(self):
        """Refresh logs display"""
        if (
            self.notebook.index(self.notebook.select()) == len(self.notebook.tabs()) - 1
        ):  # Logs tab is active
            self.load_recent_logs()

    def run(self):
        """Start the GUI application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Show startup message
        self.update_status("DENSO888 Professional System Ready")

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
            stats = self.pool_controller.get_connection_stats()
            self.stats_text.config(
                text=f"Pool: {stats.get('in_use_connections', 0)}/{stats.get('total_connections', 0)} connections"
            )

    def on_import_error(self, data):
        """Handle import error"""
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

    # Utility Methods
    def load_recent_logs(self):
        """Load recent application logs"""
        try:
            log_file = (
                Path("logs") / f"denso888_{datetime.now().strftime('%Y%m%d')}.log"
            )
            if log_file.exists():
                with open(log_file, "r", encoding="utf-8") as f:
                    logs = f.read()

                self.log_text.config(state="normal")
                self.log_text.delete(1.0, tk.END)
                self.log_text.insert(1.0, logs)
                self.log_text.config(state="disabled")
                self.log_text.see(tk.END)
        except Exception as e:
            logger.error(f"Failed to load logs: {e}")

    def update_status(self, message):
        """Update status bar"""
        self.status_text.config(text=message)

        # Auto-refresh logs periodically
        self.root.after(5000, self.refresh_logs)

    def refresh_logs(self):
        """Refresh logs display"""
        if (
            self.notebook.index(self.notebook.select()) == len(self.notebook.tabs()) - 1
        ):  # Logs tab is active
            self.load_recent_logs()

    def run(self):
        """Start the GUI application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Show startup message
        self.update_status("DENSO888 Professional System Ready")

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


# Import required modules at the top
from datetime import datetime
