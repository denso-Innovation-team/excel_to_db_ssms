"""
gui/pages/analytics_page.py
Analytics & Reporting Page
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import datetime

from ..components.modern_button import ModernButton
from ..components.modern_card import ModernCard, StatCard
from ..components.modern_input import ModernCombobox


class AnalyticsPage:
    """Analytics and data insights page"""

    def __init__(self, parent: tk.Widget, controller):
        self.parent = parent
        self.controller = controller
        self.main_frame = None
        self.table_selector = None
        self.analytics_data = {}

        self._create_analytics_page()
        self._load_initial_data()

    def _create_analytics_page(self):
        """สร้างหน้า analytics"""
        self.main_frame = tk.Frame(self.parent, bg="#FFFFFF")

        # Header
        self._create_header()

        # Table selection
        self._create_table_selection()

        # Quick stats
        self._create_quick_stats()

        # Data analysis
        self._create_analysis_section()

        # Export options
        self._create_export_section()

    def _create_header(self):
        """สร้าง header section"""
        header_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        header_frame.pack(fill="x", padx=20, pady=(20, 0))

        # Title
        title_label = tk.Label(
            header_frame,
            text="📈 Data Analytics",
            font=("Segoe UI", 18, "bold"),
            bg="#FFFFFF",
            fg="#1F2937",
        )
        title_label.pack(anchor="w")

        # Description
        desc_label = tk.Label(
            header_frame,
            text="Analyze and explore your data with insights and reports",
            font=("Segoe UI", 12),
            bg="#FFFFFF",
            fg="#6B7280",
        )
        desc_label.pack(anchor="w", pady=(5, 0))

    def _create_table_selection(self):
        """สร้าง table selection section"""
        table_card = ModernCard(
            self.main_frame,
            title="🎯 Select Table for Analysis",
            width=800,
            height=120,
        )
        table_card.pack(fill="x", padx=20, pady=20)

        selection_frame = tk.Frame(table_card.get_widget(), bg="#FFFFFF")
        selection_frame.pack(fill="x", padx=20, pady=10)

        # Table selector
        self.table_selector = ModernCombobox(
            selection_frame,
            values=[],
            placeholder="Select a table to analyze...",
            width=40,
        )
        self.table_selector.bind("<<ComboboxSelected>>", self._on_table_select)
        self.table_selector.pack(side="left", padx=(0, 15))

        # Refresh button
        refresh_btn = ModernButton(
            selection_frame,
            "🔄 Refresh Tables",
            command=self._refresh_tables,
            style="secondary",
        )
        refresh_btn.pack(side="left")

        # Table info
        self.table_info_label = tk.Label(
            selection_frame,
            text="Select a table to see analytics",
            font=("Segoe UI", 10),
            bg="#FFFFFF",
            fg="#6B7280",
        )
        self.table_info_label.pack(side="right")

    def _create_quick_stats(self):
        """สร้าง quick statistics section"""
        stats_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        stats_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Stats title
        stats_title = tk.Label(
            stats_frame,
            text="📊 Quick Statistics",
            font=("Segoe UI", 14, "bold"),
            bg="#FFFFFF",
            fg="#1F2937",
        )
        stats_title.pack(anchor="w", pady=(0, 10))

        # Stats cards container
        self.stats_container = tk.Frame(stats_frame, bg="#FFFFFF")
        self.stats_container.pack(fill="x")

        # Configure grid
        for i in range(4):
            self.stats_container.grid_columnconfigure(i, weight=1)

        # Create stat cards
        self.stat_cards = {}
        self._create_empty_stats()

    def _create_empty_stats(self):
        """สร้าง empty stat cards"""
        stats_data = [
            ("rows", "Total Rows", "0", "📊", "primary"),
            ("columns", "Columns", "0", "📋", "success"),
            ("size", "Data Size", "0 KB", "💾", "warning"),
            ("modified", "Last Modified", "Never", "🕒", "secondary"),
        ]

        for i, (key, title, value, icon, color) in enumerate(stats_data):
            card = StatCard(self.stats_container, title, value, icon, color)
            card.grid(row=0, column=i, padx=5, sticky="ew")
            self.stat_cards[key] = card

    def _create_analysis_section(self):
        """สร้าง data analysis section"""
        analysis_card = ModernCard(
            self.main_frame,
            title="🔍 Data Analysis",
            width=800,
            height=400,
        )
        analysis_card.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        analysis_frame = tk.Frame(analysis_card.get_widget(), bg="#FFFFFF")
        analysis_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Analysis notebook
        self.analysis_notebook = ttk.Notebook(analysis_frame)
        self.analysis_notebook.pack(fill="both", expand=True)

        # Create tabs
        self._create_overview_tab()
        self._create_columns_tab()
        self._create_quality_tab()

    def _create_overview_tab(self):
        """สร้าง overview tab"""
        overview_frame = tk.Frame(self.analysis_notebook, bg="#FFFFFF")
        self.analysis_notebook.add(overview_frame, text="📈 Overview")

        # Data preview
        preview_label = tk.Label(
            overview_frame,
            text="Data Preview (First 10 rows)",
            font=("Segoe UI", 12, "bold"),
            bg="#FFFFFF",
            fg="#1F2937",
        )
        preview_label.pack(anchor="w", padx=10, pady=(10, 5))

        # Data treeview
        self.data_tree = ttk.Treeview(overview_frame, show="headings", height=8)

        # Scrollbars
        data_scroll_v = ttk.Scrollbar(
            overview_frame, orient="vertical", command=self.data_tree.yview
        )
        data_scroll_h = ttk.Scrollbar(
            overview_frame, orient="horizontal", command=self.data_tree.xview
        )

        self.data_tree.configure(
            yscrollcommand=data_scroll_v.set, xscrollcommand=data_scroll_h.set
        )

        # Pack components
        self.data_tree.pack(
            side="left", fill="both", expand=True, padx=(10, 0), pady=10
        )
        data_scroll_v.pack(side="right", fill="y", pady=10)

        # No data message
        self.no_data_label = tk.Label(
            overview_frame,
            text="Select a table to view data preview",
            font=("Segoe UI", 12),
            bg="#FFFFFF",
            fg="#9CA3AF",
        )

    def _create_columns_tab(self):
        """สร้าง columns analysis tab"""
        columns_frame = tk.Frame(self.analysis_notebook, bg="#FFFFFF")
        self.analysis_notebook.add(columns_frame, text="📋 Columns")

        # Columns info
        self.columns_tree = ttk.Treeview(
            columns_frame,
            columns=("name", "type", "nulls", "unique", "sample"),
            show="headings",
            height=12,
        )

        # Configure columns
        self.columns_tree.heading("name", text="Column Name")
        self.columns_tree.heading("type", text="Data Type")
        self.columns_tree.heading("nulls", text="Null Count")
        self.columns_tree.heading("unique", text="Unique Values")
        self.columns_tree.heading("sample", text="Sample Value")

        self.columns_tree.column("name", width=150)
        self.columns_tree.column("type", width=100)
        self.columns_tree.column("nulls", width=80, anchor="center")
        self.columns_tree.column("unique", width=100, anchor="center")
        self.columns_tree.column("sample", width=200)

        # Scrollbar
        columns_scroll = ttk.Scrollbar(
            columns_frame, orient="vertical", command=self.columns_tree.yview
        )
        self.columns_tree.configure(yscrollcommand=columns_scroll.set)

        # Pack components
        self.columns_tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        columns_scroll.pack(side="right", fill="y", pady=10)

    def _create_quality_tab(self):
        """สร้าง data quality tab"""
        quality_frame = tk.Frame(self.analysis_notebook, bg="#FFFFFF")
        self.analysis_notebook.add(quality_frame, text="✅ Data Quality")

        # Quality metrics
        self.quality_text = tk.Text(
            quality_frame,
            font=("Consolas", 10),
            bg="#F8F9FA",
            fg="#1F2937",
            relief="flat",
            bd=1,
            wrap=tk.WORD,
            height=15,
        )

        quality_scroll = ttk.Scrollbar(
            quality_frame, orient="vertical", command=self.quality_text.yview
        )
        self.quality_text.configure(yscrollcommand=quality_scroll.set)

        self.quality_text.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        quality_scroll.pack(side="right", fill="y", pady=10)

    def _create_export_section(self):
        """สร้าง export section"""
        export_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        export_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Export title
        export_title = tk.Label(
            export_frame,
            text="📊 Export Options",
            font=("Segoe UI", 14, "bold"),
            bg="#FFFFFF",
            fg="#1F2937",
        )
        export_title.pack(anchor="w", pady=(0, 10))

        # Export buttons
        export_buttons = tk.Frame(export_frame, bg="#FFFFFF")
        export_buttons.pack(fill="x")

        # Export data button
        export_data_btn = ModernButton(
            export_buttons,
            "📄 Export Data",
            command=self._export_data,
            style="primary",
        )
        export_data_btn.pack(side="left", padx=(0, 10))

        # Export report button
        export_report_btn = ModernButton(
            export_buttons,
            "📈 Export Report",
            command=self._export_report,
            style="success",
        )
        export_report_btn.pack(side="left")

    def _refresh_tables(self):
        """รีเฟรชรายการตาราง"""
        try:
            if hasattr(self.controller, "get_database_tables"):
                tables = self.controller.get_database_tables()
                self.table_selector.update_values(tables)

                if tables:
                    self.table_info_label.configure(text=f"Found {len(tables)} tables")
                else:
                    self.table_info_label.configure(text="No tables found")
            else:
                self.table_info_label.configure(text="Database not connected")

        except Exception as e:
            self.table_info_label.configure(text="Error loading tables")
            messagebox.showerror("Error", f"Failed to load tables: {str(e)}")

    def _on_table_select(self, event=None):
        """เมื่อเลือกตาราง"""
        selected_table = self.table_selector.get_value()

        if not selected_table:
            return

        # Show loading
        self.table_info_label.configure(text="Loading table data...")

        def load_async():
            try:
                self._load_table_analytics(selected_table)
                self.main_frame.after(
                    0,
                    lambda: self.table_info_label.configure(
                        text=f"Analyzing table: {selected_table}"
                    ),
                )
            except Exception as e:
                self.main_frame.after(
                    0,
                    lambda: self.table_info_label.configure(
                        text=f"Error loading table: {str(e)}"
                    ),
                )

        threading.Thread(target=load_async, daemon=True).start()

    def _load_table_analytics(self, table_name: str):
        """โหลด analytics สำหรับตาราง"""
        try:
            # Get table info
            if hasattr(self.controller, "get_table_info"):
                table_info = self.controller.get_table_info(table_name)

                if "error" in table_info:
                    raise Exception(table_info["error"])

                # Update statistics
                self.main_frame.after(0, lambda: self._update_stats(table_info))

                # Load data preview
                self.main_frame.after(0, lambda: self._load_data_preview(table_name))

                # Load column analysis
                self.main_frame.after(
                    0, lambda: self._load_column_analysis(table_name, table_info)
                )

                # Load quality analysis
                self.main_frame.after(
                    0, lambda: self._load_quality_analysis(table_name)
                )

        except Exception as e:
            print(f"Error loading table analytics: {e}")
            raise

    def _update_stats(self, table_info: dict):
        """อัพเดทสถิติ"""
        row_count = table_info.get("row_count", 0)
        column_count = table_info.get("column_count", 0)

        # Estimate data size (rough calculation)
        estimated_size = row_count * column_count * 50  # rough bytes per cell
        if estimated_size < 1024:
            size_text = f"{estimated_size} B"
        elif estimated_size < 1024 * 1024:
            size_text = f"{estimated_size // 1024} KB"
        else:
            size_text = f"{estimated_size // (1024 * 1024)} MB"

        # Update stat cards
        self.stat_cards["rows"].update_value(f"{row_count:,}")
        self.stat_cards["columns"].update_value(str(column_count))
        self.stat_cards["size"].update_value(size_text)
        self.stat_cards["modified"].update_value("Recently")

    def _load_data_preview(self, table_name: str):
        """โหลด data preview"""
        try:
            # Get sample data
            if hasattr(self.controller.db_service, "get_table_data"):
                data = self.controller.db_service.get_table_data(table_name, limit=10)

                if data:
                    # Clear existing data
                    self.data_tree.delete(*self.data_tree.get_children())

                    # Configure columns
                    columns = list(data[0].keys())
                    self.data_tree["columns"] = columns

                    for col in columns:
                        self.data_tree.heading(col, text=str(col))
                        self.data_tree.column(col, width=150, minwidth=100)

                    # Insert data
                    for row in data:
                        values = [str(row.get(col, "")) for col in columns]
                        self.data_tree.insert("", "end", values=values)

                    # Hide no data message
                    self.no_data_label.pack_forget()
                else:
                    # Show no data message
                    self.no_data_label.pack(expand=True)

        except Exception as e:
            print(f"Error loading data preview: {e}")

    def _load_column_analysis(self, table_name: str, table_info: dict):
        """โหลด column analysis"""
        try:
            # Clear existing data
            self.columns_tree.delete(*self.columns_tree.get_children())

            columns = table_info.get("columns", [])

            # Get sample data for analysis
            sample_data = []
            if hasattr(self.controller.db_service, "get_table_data"):
                sample_data = self.controller.db_service.get_table_data(
                    table_name, limit=100
                )

            for col_info in columns:
                col_name = col_info.get("name", "Unknown")
                col_type = col_info.get("type", "Unknown")

                # Analyze column if we have sample data
                null_count = 0
                unique_count = 0
                sample_value = "N/A"

                if sample_data:
                    values = [
                        row.get(col_name) for row in sample_data if col_name in row
                    ]
                    null_count = sum(
                        1 for v in values if v is None or str(v).strip() == ""
                    )
                    unique_values = set(str(v) for v in values if v is not None)
                    unique_count = len(unique_values)

                    if unique_values:
                        sample_value = str(list(unique_values)[0])[:50]

                self.columns_tree.insert(
                    "",
                    "end",
                    values=(col_name, col_type, null_count, unique_count, sample_value),
                )

        except Exception as e:
            print(f"Error loading column analysis: {e}")

    def _load_quality_analysis(self, table_name: str):
        """โหลด data quality analysis"""
        try:
            self.quality_text.delete(1.0, tk.END)

            # Get table info
            if hasattr(self.controller, "get_table_info"):
                table_info = self.controller.get_table_info(table_name)

                report = []
                report.append(f"DATA QUALITY REPORT FOR: {table_name}")
                report.append("=" * 50)
                report.append("")

                # Basic stats
                report.append("BASIC STATISTICS:")
                report.append(f"• Total Rows: {table_info.get('row_count', 0):,}")
                report.append(f"• Total Columns: {table_info.get('column_count', 0)}")
                report.append("")

                # Column analysis
                columns = table_info.get("columns", [])
                report.append("COLUMN ANALYSIS:")
                for col in columns:
                    name = col.get("name", "Unknown")
                    data_type = col.get("type", "Unknown")
                    nullable = col.get("nullable", True)

                    report.append(f"• {name}")
                    report.append(f"  - Type: {data_type}")
                    report.append(f"  - Nullable: {'Yes' if nullable else 'No'}")

                report.append("")

                # Data quality checks
                report.append("QUALITY ASSESSMENT:")

                # Get sample data for quality checks
                if hasattr(self.controller.db_service, "get_table_data"):
                    sample_data = self.controller.db_service.get_table_data(
                        table_name, limit=1000
                    )

                    if sample_data:
                        total_cells = len(sample_data) * len(columns)
                        empty_cells = 0

                        for row in sample_data:
                            for col in columns:
                                col_name = col.get("name")
                                value = row.get(col_name)
                                if value is None or str(value).strip() == "":
                                    empty_cells += 1

                        completeness = (
                            ((total_cells - empty_cells) / total_cells) * 100
                            if total_cells > 0
                            else 0
                        )

                        report.append(f"• Data Completeness: {completeness:.1f}%")
                        report.append(
                            f"• Empty Cells: {empty_cells:,} / {total_cells:,}"
                        )

                        # Check for duplicates
                        unique_rows = len(set(str(row) for row in sample_data))
                        duplicate_rows = len(sample_data) - unique_rows
                        report.append(f"• Duplicate Rows: {duplicate_rows}")

                        # Data type consistency
                        report.append("")
                        report.append("RECOMMENDATIONS:")

                        if completeness < 90:
                            report.append(
                                "⚠️  Low data completeness detected - consider data cleaning"
                            )

                        if duplicate_rows > 0:
                            report.append(
                                "⚠️  Duplicate rows found - consider deduplication"
                            )

                        if completeness >= 95 and duplicate_rows == 0:
                            report.append("✅ Good data quality - ready for analysis")

                # Display report
                report_text = "\n".join(report)
                self.quality_text.insert(1.0, report_text)

        except Exception as e:
            error_text = f"Error generating quality report: {str(e)}"
            self.quality_text.insert(1.0, error_text)

    def _export_data(self):
        """Export table data"""
        selected_table = self.table_selector.get_value()

        if not selected_table:
            messagebox.showwarning("Warning", "Please select a table first")
            return

        from tkinter import filedialog

        file_path = filedialog.asksaveasfilename(
            title="Export Data",
            defaultextension=".xlsx",
            filetypes=[
                ("Excel files", "*.xlsx"),
                ("CSV files", "*.csv"),
                ("All files", "*.*"),
            ],
        )

        if file_path:
            try:
                if hasattr(self.controller, "export_data"):
                    format_type = "xlsx" if file_path.endswith(".xlsx") else "csv"
                    success = self.controller.export_data(
                        selected_table, format_type, file_path
                    )

                    if success:
                        messagebox.showinfo("Success", f"Data exported to {file_path}")
                    else:
                        messagebox.showerror("Error", "Export failed")
                else:
                    messagebox.showinfo("Info", "Export functionality not available")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")

    def _export_report(self):
        """Export analytics report"""
        selected_table = self.table_selector.get_value()

        if not selected_table:
            messagebox.showwarning("Warning", "Please select a table first")
            return

        from tkinter import filedialog

        file_path = filedialog.asksaveasfilename(
            title="Export Report",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*"),
            ],
        )

        if file_path:
            try:
                # Get quality report text
                report_content = self.quality_text.get(1.0, tk.END)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(f"ANALYTICS REPORT\n")
                    f.write(
                        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    )
                    f.write(f"Table: {selected_table}\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(report_content)

                messagebox.showinfo("Success", f"Report exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Report export failed: {str(e)}")

    def _load_initial_data(self):
        """โหลดข้อมูลเริ่มต้น"""
        self._refresh_tables()

    def show(self):
        """Show analytics page"""
        if self.main_frame:
            self.main_frame.pack(fill="both", expand=True)
            self._refresh_tables()

    def hide(self):
        """Hide analytics page"""
        if self.main_frame:
            self.main_frame.pack_forget()

    def get_widget(self) -> tk.Widget:
        """Get main widget"""
        return self.main_frame
