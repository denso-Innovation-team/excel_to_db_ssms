"""
fallback_main.py
Simple Fallback Interface for DENSO888
เฮียตอมจัดหั้ย!!! - Emergency Mode
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import sqlite3
import os
from datetime import datetime
from pathlib import Path


class DENSO888Simple:
    """Simple fallback interface when main app fails"""

    def __init__(self):
        self.root = None
        self.db_path = "denso888_emergency.db"
        self.current_file = None

    def run(self):
        """Run simple interface"""
        self.root = tk.Tk()
        self.root.title("🏭 DENSO888 - Emergency Mode")
        self.root.geometry("800x600")
        self.root.configure(bg="#1A1A2E")

        self.create_ui()
        self.root.mainloop()

    def create_ui(self):
        """Create simple UI"""
        # Header
        header = tk.Frame(self.root, bg="#FF0066", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="🏭 DENSO888 EMERGENCY MODE",
            font=("Arial", 16, "bold"),
            bg="#FF0066",
            fg="white",
        )
        title.pack(expand=True)

        subtitle = tk.Label(
            header,
            text="Created by: Thammaphon Chittasuwanna (SDM) | เฮียตอมจัดหั้ย!!! 🚀",
            font=("Arial", 10),
            bg="#FF0066",
            fg="white",
        )
        subtitle.pack()

        # Main content
        main_frame = tk.Frame(self.root, bg="#1A1A2E")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # File selection
        file_frame = tk.LabelFrame(
            main_frame,
            text="📁 Select Excel File",
            font=("Arial", 12, "bold"),
            bg="#1A1A2E",
            fg="white",
        )
        file_frame.pack(fill="x", pady=(0, 20))

        self.file_label = tk.Label(
            file_frame,
            text="No file selected",
            font=("Arial", 10),
            bg="#1A1A2E",
            fg="#CCCCCC",
        )
        self.file_label.pack(pady=10)

        select_btn = tk.Button(
            file_frame,
            text="📂 Browse Excel File",
            command=self.select_file,
            font=("Arial", 11),
            bg="#007BFF",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
        )
        select_btn.pack(pady=10)

        # Import settings
        settings_frame = tk.LabelFrame(
            main_frame,
            text="⚙️ Import Settings",
            font=("Arial", 12, "bold"),
            bg="#1A1A2E",
            fg="white",
        )
        settings_frame.pack(fill="x", pady=(0, 20))

        # Table name
        name_frame = tk.Frame(settings_frame, bg="#1A1A2E")
        name_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(
            name_frame, text="Table Name:", font=("Arial", 10), bg="#1A1A2E", fg="white"
        ).pack(side="left")

        self.table_name = tk.StringVar(value="imported_data")
        name_entry = tk.Entry(
            name_frame, textvariable=self.table_name, font=("Arial", 10), width=30
        )
        name_entry.pack(side="left", padx=(10, 0))

        # Actions
        actions_frame = tk.Frame(main_frame, bg="#1A1A2E")
        actions_frame.pack(fill="x", pady=20)

        import_btn = tk.Button(
            actions_frame,
            text="🚀 Import to SQLite",
            command=self.import_data,
            font=("Arial", 12, "bold"),
            bg="#28A745",
            fg="white",
            relief="flat",
            padx=30,
            pady=15,
            cursor="hand2",
        )
        import_btn.pack(side="left", padx=(0, 10))

        view_btn = tk.Button(
            actions_frame,
            text="👁️ View Database",
            command=self.view_database,
            font=("Arial", 11),
            bg="#FFC107",
            fg="black",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
        )
        view_btn.pack(side="left", padx=(0, 10))

        # Status
        self.status_label = tk.Label(
            main_frame,
            text="💡 Emergency mode ready - select Excel file to begin",
            font=("Arial", 10),
            bg="#1A1A2E",
            fg="#00FF88",
            anchor="w",
        )
        self.status_label.pack(fill="x", pady=(20, 0))

        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode="determinate", length=400)
        self.progress.pack(pady=10)
        self.progress.pack_forget()  # Hide initially

    def select_file(self):
        """Select Excel file"""
        filename = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")],
        )

        if filename:
            self.current_file = filename
            file_name = os.path.basename(filename)
            self.file_label.configure(text=f"📊 {file_name}")

            # Auto-generate table name
            clean_name = Path(filename).stem
            clean_name = "".join(c if c.isalnum() else "_" for c in clean_name)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            table_name = f"import_{clean_name}_{timestamp}"
            self.table_name.set(table_name[:50])

            self.status_label.configure(
                text=f"✅ File loaded: {file_name}", fg="#00FF88"
            )

    def import_data(self):
        """Import Excel data to SQLite"""
        if not self.current_file:
            messagebox.showwarning("No File", "Please select an Excel file first")
            return

        table_name = self.table_name.get().strip()
        if not table_name:
            messagebox.showwarning("No Table Name", "Please enter a table name")
            return

        try:
            # Show progress
            self.progress.pack(pady=10)
            self.progress["value"] = 0
            self.root.update()

            # Read Excel file
            self.status_label.configure(text="📖 Reading Excel file...", fg="#007BFF")
            self.root.update()

            df = pd.read_excel(self.current_file)
            self.progress["value"] = 30
            self.root.update()

            # Connect to SQLite
            self.status_label.configure(
                text="🗄️ Connecting to database...", fg="#007BFF"
            )
            self.root.update()

            conn = sqlite3.connect(self.db_path)
            self.progress["value"] = 50
            self.root.update()

            # Import data
            self.status_label.configure(text="📊 Importing data...", fg="#007BFF")
            self.root.update()

            df.to_sql(table_name, conn, if_exists="replace", index=False)
            self.progress["value"] = 90
            self.root.update()

            # Complete
            conn.close()
            self.progress["value"] = 100
            self.root.update()

            self.status_label.configure(
                text=f"✅ Success! Imported {len(df):,} rows to '{table_name}'",
                fg="#00FF88",
            )

            # Show success dialog
            db_path = os.path.abspath(self.db_path)
            messagebox.showinfo(
                "Import Complete",
                f"Successfully imported {len(df):,} rows!\n\n"
                f"Table: {table_name}\n"
                f"Database: {db_path}\n\n"
                f"เฮียตอมจัดหั้ย!!! 🚀",
            )

        except Exception as e:
            self.status_label.configure(text=f"❌ Error: {str(e)}", fg="#FF4466")
            messagebox.showerror("Import Error", f"Failed to import data:\n\n{str(e)}")

        finally:
            # Hide progress bar
            self.progress.pack_forget()

    def view_database(self):
        """View database contents"""
        if not os.path.exists(self.db_path):
            messagebox.showinfo("No Database", "No database found. Import data first.")
            return

        try:
            # Create viewer window
            viewer = tk.Toplevel(self.root)
            viewer.title("🗄️ Database Viewer")
            viewer.geometry("800x600")
            viewer.configure(bg="#1A1A2E")

            # Header
            header = tk.Frame(viewer, bg="#1A1A2E")
            header.pack(fill="x", padx=10, pady=10)

            tk.Label(
                header,
                text="🗄️ Database Contents",
                font=("Arial", 14, "bold"),
                bg="#1A1A2E",
                fg="white",
            ).pack(side="left")

            # Get tables
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]

            if not tables:
                tk.Label(
                    viewer,
                    text="📄 No tables found in database",
                    font=("Arial", 12),
                    bg="#1A1A2E",
                    fg="#CCCCCC",
                ).pack(expand=True)
                conn.close()
                return

            # Table selector
            selector_frame = tk.Frame(viewer, bg="#1A1A2E")
            selector_frame.pack(fill="x", padx=10, pady=(0, 10))

            tk.Label(
                selector_frame,
                text="Select Table:",
                font=("Arial", 10),
                bg="#1A1A2E",
                fg="white",
            ).pack(side="left")

            table_var = tk.StringVar(value=tables[0])
            table_combo = ttk.Combobox(
                selector_frame, textvariable=table_var, values=tables, state="readonly"
            )
            table_combo.pack(side="left", padx=(10, 0))

            # Data display
            data_frame = tk.Frame(viewer, bg="#1A1A2E")
            data_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

            # Treeview for data
            tree_frame = tk.Frame(data_frame, bg="#1A1A2E")
            tree_frame.pack(fill="both", expand=True)

            tree = ttk.Treeview(tree_frame, show="headings")

            # Scrollbars
            v_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
            h_scroll = ttk.Scrollbar(
                tree_frame, orient="horizontal", command=tree.xview
            )
            tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

            # Pack scrollbars and tree
            tree.pack(side="left", fill="both", expand=True)
            v_scroll.pack(side="right", fill="y")
            h_scroll.pack(side="bottom", fill="x")

            def load_table_data():
                """Load data for selected table"""
                table_name = table_var.get()

                # Clear tree
                tree.delete(*tree.get_children())

                # Get data
                cursor.execute(f"SELECT * FROM `{table_name}` LIMIT 1000")
                data = cursor.fetchall()

                if data:
                    # Get column names
                    cursor.execute(f"PRAGMA table_info(`{table_name}`)")
                    columns = [row[1] for row in cursor.fetchall()]

                    # Configure tree columns
                    tree["columns"] = columns
                    for col in columns:
                        tree.heading(col, text=col)
                        tree.column(col, width=100)

                    # Insert data
                    for row in data:
                        tree.insert("", "end", values=row)

                    # Show row count
                    cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
                    total_rows = cursor.fetchone()[0]

                    status_text = f"📊 Showing {len(data):,} of {total_rows:,} rows"
                    if len(data) == 1000 and total_rows > 1000:
                        status_text += " (limited to first 1000)"

                    if hasattr(load_table_data, "status_label"):
                        load_table_data.status_label.configure(text=status_text)

            # Status label
            load_table_data.status_label = tk.Label(
                viewer, text="", font=("Arial", 10), bg="#1A1A2E", fg="#CCCCCC"
            )
            load_table_data.status_label.pack(padx=10, pady=(0, 10))

            # Bind table selection
            table_combo.bind("<<ComboboxSelected>>", lambda e: load_table_data())

            # Load initial data
            load_table_data()

            conn.close()

        except Exception as e:
            messagebox.showerror(
                "Database Error", f"Failed to view database:\n\n{str(e)}"
            )


if __name__ == "__main__":
    app = DENSO888Simple()
    app.run()
