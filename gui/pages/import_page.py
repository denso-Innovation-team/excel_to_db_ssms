"""
gui/pages/import_page.py
Excel Import Page - Clean & Functional
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from ..components.modern_button import ModernButton, ActionButton
from ..components.modern_input import FileSelector, LabeledInput
from ..components.modern_card import ModernCard


class ImportPage:
    """Excel import page with file selection and preview"""

    def __init__(self, parent: tk.Widget, controller):
        self.parent = parent
        self.controller = controller
        self.main_frame = None
        self.file_selector = None
        self.preview_tree = None
        self.table_name_entry = None
        self.selected_file = None
        self.file_info = {}

        self._create_import_page()

    def _create_import_page(self):
        """สร้างหน้า import"""
        self.main_frame = tk.Frame(self.parent, bg="#FFFFFF")

        # Header
        self._create_header()

        # File selection section
        self._create_file_section()

        # Options section
        self._create_options_section()

        # Preview section
        self._create_preview_section()

        # Action buttons
        self._create_action_section()

    def _create_header(self):
        """สร้าง header section"""
        header_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        header_frame.pack(fill="x", padx=20, pady=(20, 0))

        # Title
        title_label = tk.Label(
            header_frame,
            text="📊 Excel Import",
            font=("Segoe UI", 18, "bold"),
            bg="#FFFFFF",
            fg="#1F2937",
        )
        title_label.pack(anchor="w")

        # Description
        desc_label = tk.Label(
            header_frame,
            text="Import Excel data into database tables",
            font=("Segoe UI", 12),
            bg="#FFFFFF",
            fg="#6B7280",
        )
        desc_label.pack(anchor="w", pady=(5, 0))

    def _create_file_section(self):
        """สร้าง file selection section"""
        # Section card
        file_card = ModernCard(
            self.main_frame,
            title="📁 Select Excel File",
            width=800,
            height=150,
        )
        file_card.pack(fill="x", padx=20, pady=20)

        # File selector
        self.file_selector = FileSelector(
            file_card.get_widget(),
            placeholder="Choose Excel file (.xlsx, .xls)...",
            file_types=[
                ("Excel files", "*.xlsx *.xls"),
                ("All files", "*.*"),
            ],
            width=50,
        )
        self.file_selector.pack(fill="x", padx=20, pady=10)

        # File info display
        self.file_info_frame = tk.Frame(file_card.get_widget(), bg="#FFFFFF")
        self.file_info_frame.pack(fill="x", padx=20, pady=(0, 10))

    def _create_options_section(self):
        """สร้าง import options section"""
        options_card = ModernCard(
            self.main_frame,
            title="⚙️ Import Options",
            width=800,
            height=200,
        )
        options_card.pack(fill="x", padx=20, pady=(0, 20))

        options_frame = tk.Frame(options_card.get_widget(), bg="#FFFFFF")
        options_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Table name input
        self.table_name_entry = LabeledInput(
            options_frame,
            "Table Name:",
            "entry",
            placeholder="Enter table name...",
            width=30,
        )
        self.table_name_entry.pack(fill="x", pady=(0, 15))

        # Options checkboxes
        self.options_frame = tk.Frame(options_frame, bg="#FFFFFF")
        self.options_frame.pack(fill="x")

        # Create option variables
        self.has_header = tk.BooleanVar(value=True)
        self.clean_data = tk.BooleanVar(value=True)
        self.replace_table = tk.BooleanVar(value=False)

        # Option checkboxes
        options = [
            ("First row contains headers", self.has_header),
            ("Clean data automatically", self.clean_data),
            ("Replace existing table", self.replace_table),
        ]

        for i, (text, var) in enumerate(options):
            cb = tk.Checkbutton(
                self.options_frame,
                text=text,
                variable=var,
                font=("Segoe UI", 11),
                bg="#FFFFFF",
                activebackground="#FFFFFF",
            )
            cb.grid(row=i // 2, column=i % 2, sticky="w", padx=(0, 20), pady=2)

    def _create_preview_section(self):
        """สร้าง data preview section"""
        preview_card = ModernCard(
            self.main_frame,
            title="👁️ Data Preview",
            width=800,
            height=300,
        )
        preview_card.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Preview treeview
        preview_frame = tk.Frame(preview_card.get_widget(), bg="#FFFFFF")
        preview_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.preview_tree = ttk.Treeview(preview_frame, show="headings", height=10)

        # Scrollbars
        v_scroll = ttk.Scrollbar(
            preview_frame, orient="vertical", command=self.preview_tree.yview
        )
        h_scroll = ttk.Scrollbar(
            preview_frame, orient="horizontal", command=self.preview_tree.xview
        )

        self.preview_tree.configure(
            yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set
        )

        # Pack scrollbars and treeview
        self.preview_tree.pack(side="left", fill="both", expand=True)
        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")

        # No data message
        self.no_data_label = tk.Label(
            preview_frame,
            text="Select an Excel file to preview data",
            font=("Segoe UI", 12),
            bg="#FFFFFF",
            fg="#9CA3AF",
        )

    def _create_action_section(self):
        """สร้าง action buttons"""
        action_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        action_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Button container
        button_frame = tk.Frame(action_frame, bg="#FFFFFF")
        button_frame.pack(anchor="e")

        # Preview button
        self.preview_button = ModernButton(
            button_frame,
            "👁️ Preview",
            command=self._preview_file,
            style="secondary",
        )
        self.preview_button.pack(side="right", padx=(10, 0))

        # Import button
        self.import_button = ActionButton(
            button_frame,
            "📊 Import Data",
            command=self._import_data,
        )
        self.import_button.pack(side="right")

    def _preview_file(self):
        """Preview Excel file"""
        file_path = self.file_selector.get_file_path()

        if not file_path:
            messagebox.showwarning("Warning", "Please select an Excel file first")
            return

        try:
            # Use controller to analyze file
            if hasattr(self.controller, "select_excel_file"):
                success, file_info = self.controller.select_excel_file(file_path)

                if success:
                    self.file_info = file_info
                    self._display_file_info()
                    self._display_preview_data()
                    self._suggest_table_name()
                else:
                    messagebox.showerror("Error", f"Failed to read file: {file_info}")
            else:
                # Fallback: basic file reading
                self._basic_file_preview(file_path)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to preview file: {str(e)}")

    def _basic_file_preview(self, file_path: str):
        """Basic file preview without controller"""
        try:
            import pandas as pd

            # Read first few rows
            df = pd.read_excel(file_path, nrows=10)

            self.file_info = {
                "file_name": Path(file_path).name,
                "total_rows": len(df),
                "total_columns": len(df.columns),
                "columns": list(df.columns),
                "sample_data": df.head(5).to_dict("records"),
            }

            self._display_file_info()
            self._display_preview_data()
            self._suggest_table_name()

        except Exception as e:
            raise Exception(f"Error reading Excel file: {str(e)}")

    def _display_file_info(self):
        """แสดงข้อมูลไฟล์"""
        # Clear existing info
        for widget in self.file_info_frame.winfo_children():
            widget.destroy()

        if not self.file_info:
            return

        info_text = (
            f"📄 {self.file_info.get('file_name', 'Unknown')} | "
            f"📊 {self.file_info.get('total_rows', 0):,} rows | "
            f"📋 {self.file_info.get('total_columns', 0)} columns"
        )

        info_label = tk.Label(
            self.file_info_frame,
            text=info_text,
            font=("Segoe UI", 10),
            bg="#FFFFFF",
            fg="#059669",
        )
        info_label.pack(anchor="w")

    def _display_preview_data(self):
        """แสดง preview data"""
        if not self.file_info or "sample_data" not in self.file_info:
            return

        # Hide no data message
        self.no_data_label.pack_forget()

        # Clear existing columns
        self.preview_tree.delete(*self.preview_tree.get_children())

        columns = self.file_info.get("columns", [])
        sample_data = self.file_info.get("sample_data", [])

        if not columns or not sample_data:
            return

        # Configure columns
        self.preview_tree["columns"] = columns
        for col in columns:
            self.preview_tree.heading(col, text=str(col))
            self.preview_tree.column(col, width=150, minwidth=100)

        # Insert sample data
        for row_data in sample_data:
            values = [str(row_data.get(col, "")) for col in columns]
            self.preview_tree.insert("", "end", values=values)

    def _suggest_table_name(self):
        """แนะนำชื่อตาราง"""
        if not self.file_info:
            return

        file_name = self.file_info.get("file_name", "")
        if file_name:
            # Remove extension and clean name
            table_name = Path(file_name).stem
            table_name = table_name.lower().replace(" ", "_").replace("-", "_")
            # Remove special characters
            import re

            table_name = re.sub(r"[^\w]", "_", table_name)
            table_name = re.sub(r"_+", "_", table_name).strip("_")

            self.table_name_entry.set_value(table_name)

    def _import_data(self):
        """Import data to database"""
        file_path = self.file_selector.get_file_path()
        table_name = self.table_name_entry.get_value()

        if not file_path:
            messagebox.showwarning("Warning", "Please select an Excel file first")
            return

        if not table_name:
            messagebox.showwarning("Warning", "Please enter a table name")
            return

        # Prepare import options
        options = {
            "has_header": self.has_header.get(),
            "clean_data": self.clean_data.get(),
            "replace_table": self.replace_table.get(),
        }

        try:
            if hasattr(self.controller, "import_excel_data"):
                success = self.controller.import_excel_data(table_name, options)

                if success:
                    messagebox.showinfo(
                        "Success", f"Data imported successfully to table: {table_name}"
                    )
                    self._clear_form()
                else:
                    messagebox.showerror(
                        "Error", "Import failed. Check logs for details."
                    )
            else:
                messagebox.showinfo("Info", "Import functionality not available")

        except Exception as e:
            messagebox.showerror("Error", f"Import failed: {str(e)}")

    def _clear_form(self):
        """ล้างฟอร์ม"""
        self.file_selector.clear()
        self.table_name_entry.set_value("")
        self.preview_tree.delete(*self.preview_tree.get_children())

        # Clear file info
        for widget in self.file_info_frame.winfo_children():
            widget.destroy()

        # Show no data message
        self.no_data_label.pack(expand=True)

    def show(self):
        """Show import page"""
        if self.main_frame:
            self.main_frame.pack(fill="both", expand=True)

    def hide(self):
        """Hide import page"""
        if self.main_frame:
            self.main_frame.pack_forget()

    def get_widget(self) -> tk.Widget:
        """Get main widget"""
        return self.main_frame
