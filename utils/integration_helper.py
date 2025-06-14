"""
Integration Helper
ช่วยเชื่อม feature modules เข้ากับ main window
"""

import tkinter as tk
from tkinter import messagebox
import threading
import time
from typing import Dict, Any, List


class IntegrationHelper:
    """Helper class to integrate features with main window"""

    @staticmethod
    def integrate_mock_data_feature(parent_frame: tk.Widget, db_manager) -> tk.Widget:
        """Integrate mock data feature"""
        from features.mock_data_selector import MockDataSelector
        from features.progress_monitor import ProgressMonitor

        def on_generate_mock_data(template: str, count: int):
            if (
                not db_manager
                or not hasattr(db_manager, "connection")
                or not db_manager.connection
            ):
                messagebox.showerror(
                    "Database Error", "Please connect to database first!"
                )
                return

            # Start background task
            def generate_task():
                progress = ProgressMonitor(parent_frame, "Generating Mock Data")

                try:
                    progress.update(
                        10, "Initializing generator...", f"Template: {template}"
                    )
                    time.sleep(0.5)

                    # Import mock generator
                    from core.mock_data_generator import MockDataGenerator

                    generator = MockDataGenerator()

                    progress.update(
                        30, "Generating data...", f"Creating {count:,} records"
                    )

                    # Generate data based on template
                    if template == "employees":
                        data = generator.generate_employees(count)
                    elif template == "sales":
                        data = generator.generate_sales(count)
                    elif template == "inventory":
                        data = generator.generate_inventory(count)
                    else:
                        data = generator.generate_employees(count)  # Default

                    progress.update(60, "Creating table...", f"Table: mock_{template}")

                    # Create table
                    table_name = f"mock_{template}_{int(time.time())}"
                    success, message = db_manager.create_table_from_data(
                        table_name, data
                    )

                    if not success:
                        raise Exception(message)

                    progress.update(
                        80, "Inserting data...", f"Inserting {len(data):,} rows"
                    )

                    # Insert data
                    success, message = db_manager.insert_data(table_name, data)

                    if not success:
                        raise Exception(message)

                    progress.update(
                        100, "Complete!", f"Generated {len(data):,} records"
                    )
                    time.sleep(1)
                    progress.close()

                    messagebox.showinfo(
                        "Mock Data Generated",
                        f"✅ Successfully generated {len(data):,} {template} records in table '{table_name}'",
                    )

                except Exception as e:
                    progress.close()
                    messagebox.showerror(
                        "Generation Error",
                        f"❌ Failed to generate mock data:\n\n{str(e)}",
                    )

            threading.Thread(target=generate_task, daemon=True).start()

        # Create and return mock data selector
        mock_selector = MockDataSelector(parent_frame, on_generate_mock_data)
        return mock_selector.get_widget()

    @staticmethod
    def integrate_database_feature(
        parent_frame: tk.Widget,
    ) -> tuple[tk.Widget, callable]:
        """Integrate database feature"""
        from features.database_selector import DatabaseSelector

        def test_connection(config: Dict[str, Any]) -> tuple[bool, str]:
            try:
                # Import database manager
                from core.database_manager import DatabaseManager

                # Create temp manager for testing
                temp_manager = DatabaseManager(config)
                return temp_manager.test_connection()

            except Exception as e:
                return False, f"Test failed: {str(e)}"

        # Create and return database selector
        db_selector = DatabaseSelector(parent_frame, test_connection)
        return db_selector.get_widget(), db_selector.get_config

    @staticmethod
    def integrate_excel_feature(parent_frame: tk.Widget, db_manager) -> tk.Widget:
        """Integrate Excel import feature with column mapping"""

        excel_frame = tk.Frame(parent_frame, bg="#FFFFFF")

        # Title
        title = tk.Label(
            excel_frame,
            text="📊 Import Excel Data",
            font=("Segoe UI", 16, "bold"),
            fg="#DC0003",
            bg="#FFFFFF",
        )
        title.pack(pady=(0, 20))

        # File selection
        file_frame = tk.LabelFrame(
            excel_frame,
            text="Excel File Selection",
            font=("Segoe UI", 12, "bold"),
            fg="#2C3E50",
            bg="#FFFFFF",
            padx=20,
            pady=15,
        )
        file_frame.pack(fill="x", pady=(0, 15))

        selected_file = tk.StringVar()
        file_info = {}

        # File path display
        path_frame = tk.Frame(file_frame, bg="#FFFFFF")
        path_frame.pack(fill="x", pady=(0, 10))

        file_entry = tk.Entry(
            path_frame,
            textvariable=selected_file,
            font=("Segoe UI", 11),
            relief="solid",
            borderwidth=1,
            state="readonly",
        )
        file_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        def browse_file():
            from tkinter import filedialog

            filename = filedialog.askopenfilename(
                title="Select Excel File",
                filetypes=[
                    ("Excel files", "*.xlsx *.xls *.xlsm"),
                    ("All files", "*.*"),
                ],
            )

            if filename:
                selected_file.set(filename)

                # Get file info
                try:
                    from core.excel_processor import ExcelProcessor

                    processor = ExcelProcessor()

                    success, msg = processor.validate_file(filename)
                    if success:
                        file_info.update(processor.get_file_info(filename))
                        info_label.configure(
                            text=f"📊 {file_info.get('total_rows', 0):,} rows × {file_info.get('total_columns', 0)} columns",
                            fg="#28A745",
                        )
                    else:
                        info_label.configure(text=f"❌ {msg}", fg="#DC3545")

                except Exception as e:
                    info_label.configure(text=f"❌ Error: {str(e)}", fg="#DC3545")

        browse_btn = tk.Button(
            path_frame,
            text="📁 Browse",
            command=browse_file,
            font=("Segoe UI", 10),
            bg="#6C757D",
            fg="#FFFFFF",
            relief="flat",
            padx=15,
            pady=5,
            cursor="hand2",
        )
        browse_btn.pack(side="right")

        # File info
        info_label = tk.Label(
            file_frame,
            text="No file selected",
            font=("Segoe UI", 10),
            fg="#7F8C8D",
            bg="#FFFFFF",
        )
        info_label.pack(anchor="w")

        # Table name
        table_frame = tk.LabelFrame(
            excel_frame,
            text="Database Table",
            font=("Segoe UI", 12, "bold"),
            fg="#2C3E50",
            bg="#FFFFFF",
            padx=20,
            pady=15,
        )
        table_frame.pack(fill="x", pady=(0, 15))

        table_name = tk.StringVar(value="imported_data")

        tk.Label(
            table_frame,
            text="Table Name:",
            font=("Segoe UI", 11, "bold"),
            fg="#2C3E50",
            bg="#FFFFFF",
        ).pack(anchor="w", pady=(0, 5))

        tk.Entry(
            table_frame,
            textvariable=table_name,
            font=("Segoe UI", 11),
            relief="solid",
            borderwidth=1,
            width=40,
        ).pack(anchor="w")

        # Action buttons
        action_frame = tk.Frame(excel_frame, bg="#FFFFFF")
        action_frame.pack(fill="x", pady=20)

        def configure_columns():
            if not selected_file.get():
                messagebox.showwarning("No File", "Please select an Excel file first.")
                return

            if not file_info.get("columns"):
                messagebox.showerror("File Error", "Unable to read columns from file.")
                return

            def on_mapping_confirmed(
                selected_cols: List[str], mappings: Dict[str, str]
            ):
                # Start import process
                def import_task():
                    progress = ProgressMonitor(excel_frame, "Importing Excel Data")

                    try:
                        progress.update(
                            10, "Reading Excel file...", selected_file.get()
                        )

                        from core.excel_processor import ExcelProcessor

                        processor = ExcelProcessor()

                        # Process file with mappings
                        success, data = processor.process_file(
                            selected_file.get(),
                            column_mappings=mappings,
                            selected_columns=selected_cols,
                        )

                        if not success:
                            raise Exception(data)

                        progress.update(40, "Creating table...", table_name.get())

                        # Create table
                        success, message = db_manager.create_table_from_data(
                            table_name.get(), data, mappings
                        )

                        if not success:
                            raise Exception(message)

                        progress.update(
                            70, "Inserting data...", f"Inserting {len(data):,} rows"
                        )

                        # Insert data
                        success, message = db_manager.insert_data(
                            table_name.get(), data, mappings
                        )

                        if not success:
                            raise Exception(message)

                        progress.update(
                            100, "Import complete!", f"Imported {len(data):,} rows"
                        )
                        time.sleep(1)
                        progress.close()

                        messagebox.showinfo(
                            "Import Complete",
                            f"✅ Successfully imported {len(data):,} rows to table '{table_name.get()}'",
                        )

                    except Exception as e:
                        progress.close()
                        messagebox.showerror(
                            "Import Error", f"❌ Import failed:\n\n{str(e)}"
                        )

                threading.Thread(target=import_task, daemon=True).start()

            # Open column mapper
            from features.excel_column_mapper import ExcelColumnMapper

            ExcelColumnMapper(excel_frame, file_info["columns"], on_mapping_confirmed)

        # Configure columns button
        config_btn = tk.Button(
            action_frame,
            text="⚙️ Configure Columns",
            command=configure_columns,
            font=("Segoe UI", 12, "bold"),
            bg="#007BFF",
            fg="#FFFFFF",
            relief="flat",
            padx=30,
            pady=10,
            cursor="hand2",
        )
        config_btn.pack(side="left", padx=(0, 10))

        # Quick import button
        def quick_import():
            if not selected_file.get():
                messagebox.showwarning("No File", "Please select an Excel file first.")
                return

            if (
                not db_manager
                or not hasattr(db_manager, "connection")
                or not db_manager.connection
            ):
                messagebox.showerror(
                    "Database Error", "Please connect to database first!"
                )
                return

            # Import all columns with auto-mapping
            if file_info.get("columns"):
                auto_mappings = {}
                for col in file_info["columns"]:
                    clean_name = col.lower().replace(" ", "_").replace("-", "_")
                    auto_mappings[col] = clean_name

                def import_task():
                    progress = ProgressMonitor(excel_frame, "Quick Import")

                    try:
                        progress.update(
                            20, "Processing file...", "Auto-mapping columns"
                        )

                        from core.excel_processor import ExcelProcessor

                        processor = ExcelProcessor()

                        success, data = processor.process_file(
                            selected_file.get(), auto_mappings
                        )
                        if not success:
                            raise Exception(data)

                        progress.update(50, "Creating table...", table_name.get())

                        success, message = db_manager.create_table_from_data(
                            table_name.get(), data, auto_mappings
                        )
                        if not success:
                            raise Exception(message)

                        progress.update(80, "Inserting data...", f"{len(data):,} rows")

                        success, message = db_manager.insert_data(
                            table_name.get(), data, auto_mappings
                        )
                        if not success:
                            raise Exception(message)

                        progress.update(
                            100, "Complete!", f"Imported {len(data):,} rows"
                        )
                        time.sleep(1)
                        progress.close()

                        messagebox.showinfo(
                            "Quick Import Complete",
                            f"✅ Successfully imported {len(data):,} rows to table '{table_name.get()}'",
                        )

                    except Exception as e:
                        progress.close()
                        messagebox.showerror("Import Error", f"❌ {str(e)}")

                threading.Thread(target=import_task, daemon=True).start()

        quick_btn = tk.Button(
            action_frame,
            text="🚀 Quick Import",
            command=quick_import,
            font=("Segoe UI", 12, "bold"),
            bg="#DC0003",
            fg="#FFFFFF",
            relief="flat",
            padx=30,
            pady=10,
            cursor="hand2",
        )
        quick_btn.pack(side="left")

        return excel_frame
