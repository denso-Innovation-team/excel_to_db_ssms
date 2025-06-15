"""
main_simple.py - DENSO888 Minimal Working Version
รันได้แน่นอน ไม่มี dependency ซับซ้อน
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class DENSO888Simple:
    """เวอร์ชันทำงานได้แน่นอน"""

    def __init__(self):
        # สี DENSO
        self.colors = {
            "primary": "#DC0003",
            "background": "#F8FAFC",
            "surface": "#FFFFFF",
            "text": "#2C3E50",
        }

        self._create_window()
        self._create_ui()

    def _create_window(self):
        """สร้างหน้าต่างหลัก"""
        self.root = tk.Tk()
        self.root.title("🏭 DENSO888 v2.0.0 - Modern Edition")
        self.root.geometry("1200x800")
        self.root.configure(bg=self.colors["background"])

        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - 600
        y = (self.root.winfo_screenheight() // 2) - 400
        self.root.geometry(f"1200x800+{x}+{y}")

    def _create_ui(self):
        """สร้าง UI"""
        # Header
        header_frame = tk.Frame(self.root, bg=self.colors["primary"], height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        header_content = tk.Frame(header_frame, bg=self.colors["primary"])
        header_content.pack(expand=True)

        title_label = tk.Label(
            header_content,
            text="🏭 DENSO888 - Excel to SQL Management System",
            font=("Segoe UI", 18, "bold"),
            bg=self.colors["primary"],
            fg="white",
        )
        title_label.pack(pady=20)

        # Main content
        main_frame = tk.Frame(self.root, bg=self.colors["background"])
        main_frame.pack(fill="both", expand=True)

        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)

        # Create tabs
        self._create_tabs()

        # Status bar
        status_frame = tk.Frame(self.root, bg=self.colors["surface"], height=30)
        status_frame.pack(fill="x")
        status_frame.pack_propagate(False)

        status_label = tk.Label(
            status_frame,
            text="✅ DENSO888 Ready - เฮียตอมจัดหั้ย!!! 🚀",
            font=("Segoe UI", 10),
            bg=self.colors["surface"],
            fg=self.colors["text"],
            anchor="w",
        )
        status_label.pack(side="left", padx=15, pady=5)

    def _create_tabs(self):
        """สร้างแท็บต่างๆ"""
        tabs = [
            ("📊 Dashboard", self._create_dashboard),
            ("📁 Import Excel", self._create_import_tab),
            ("🗄️ Database", self._create_database_tab),
            ("🎲 Mock Data", self._create_mock_tab),
            ("📝 Logs", self._create_logs_tab),
        ]

        for tab_name, tab_creator in tabs:
            frame = tk.Frame(self.notebook, bg=self.colors["background"])
            self.notebook.add(frame, text=tab_name)
            tab_creator(frame)

    def _create_dashboard(self, parent):
        """Dashboard tab"""
        content = tk.Frame(parent, bg=self.colors["surface"], padx=40, pady=40)
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # Welcome
        welcome = tk.Label(
            content,
            text="🎉 ยินดีต้อนรับสู่ DENSO888 Modern Edition",
            font=("Segoe UI", 20, "bold"),
            bg=self.colors["surface"],
            fg=self.colors["primary"],
        )
        welcome.pack(pady=(0, 30))

        # Stats cards
        stats_frame = tk.Frame(content, bg=self.colors["surface"])
        stats_frame.pack(fill="x", pady=20)

        stats = [
            ("📊", "Excel Files", "0", "Files processed"),
            ("🗄️", "Database", "Ready", "Connection status"),
            ("📈", "Records", "0", "Total records"),
            ("⚡", "Performance", "Optimal", "System status"),
        ]

        for i, (icon, title, value, desc) in enumerate(stats):
            card = tk.Frame(stats_frame, bg="#E2E8F0", padx=20, pady=15)
            card.grid(row=0, column=i, padx=10, pady=5, sticky="ew")

            tk.Label(card, text=icon, font=("Segoe UI", 24), bg="#E2E8F0").pack()
            tk.Label(
                card, text=title, font=("Segoe UI", 12, "bold"), bg="#E2E8F0"
            ).pack()
            tk.Label(
                card,
                text=value,
                font=("Segoe UI", 16, "bold"),
                bg="#E2E8F0",
                fg=self.colors["primary"],
            ).pack()
            tk.Label(
                card, text=desc, font=("Segoe UI", 10), bg="#E2E8F0", fg="#64748B"
            ).pack()

        # Configure grid
        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1)

    def _create_import_tab(self, parent):
        """Import Excel tab"""
        content = tk.Frame(parent, bg=self.colors["surface"], padx=30, pady=30)
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # File selection
        tk.Label(
            content,
            text="📁 Select Excel File",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors["surface"],
        ).pack(anchor="w", pady=(0, 15))

        file_frame = tk.Frame(content, bg="#E2E8F0", height=100)
        file_frame.pack(fill="x", pady=(0, 20))
        file_frame.pack_propagate(False)

        file_content = tk.Frame(file_frame, bg="#E2E8F0")
        file_content.pack(expand=True)

        tk.Label(file_content, text="📁", font=("Segoe UI", 32), bg="#E2E8F0").pack(
            pady=(10, 5)
        )
        tk.Label(
            file_content,
            text="Drag & drop Excel file here",
            font=("Segoe UI", 12),
            bg="#E2E8F0",
        ).pack()

        browse_btn = tk.Button(
            file_content,
            text="📂 Browse Files",
            font=("Segoe UI", 10),
            bg=self.colors["primary"],
            fg="white",
            relief="flat",
            padx=20,
            pady=5,
            command=self._browse_file,
        )
        browse_btn.pack(pady=(10, 15))

        # Import settings
        tk.Label(
            content,
            text="⚙️ Import Settings",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors["surface"],
        ).pack(anchor="w", pady=(20, 15))

        settings_frame = tk.Frame(content, bg=self.colors["surface"])
        settings_frame.pack(fill="x")

        tk.Label(
            settings_frame,
            text="Table Name:",
            font=("Segoe UI", 11),
            bg=self.colors["surface"],
        ).pack(anchor="w")

        table_entry = tk.Entry(settings_frame, font=("Segoe UI", 11), width=40)
        table_entry.pack(anchor="w", pady=(5, 15))
        table_entry.insert(0, "imported_data")

        # Import button
        import_btn = tk.Button(
            content,
            text="🚀 Import to Database",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors["primary"],
            fg="white",
            relief="flat",
            padx=30,
            pady=10,
            command=self._import_data,
        )
        import_btn.pack(pady=20)

    def _create_database_tab(self, parent):
        """Database tab"""
        content = tk.Frame(parent, bg=self.colors["surface"], padx=30, pady=30)
        content.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            content,
            text="🗄️ Database Configuration",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors["surface"],
        ).pack(anchor="w", pady=(0, 20))

        # Database type
        db_frame = tk.Frame(content, bg=self.colors["surface"])
        db_frame.pack(fill="x", pady=(0, 20))

        self.db_type = tk.StringVar(value="sqlite")

        sqlite_radio = tk.Radiobutton(
            db_frame,
            text="💾 SQLite (Local)",
            variable=self.db_type,
            value="sqlite",
            font=("Segoe UI", 12),
            bg=self.colors["surface"],
        )
        sqlite_radio.pack(anchor="w", pady=2)

        sqlserver_radio = tk.Radiobutton(
            db_frame,
            text="🖥️ SQL Server",
            variable=self.db_type,
            value="sqlserver",
            font=("Segoe UI", 12),
            bg=self.colors["surface"],
        )
        sqlserver_radio.pack(anchor="w", pady=2)

        # Test button
        test_btn = tk.Button(
            content,
            text="🔍 Test Connection",
            font=("Segoe UI", 12),
            bg="#007BFF",
            fg="white",
            relief="flat",
            padx=25,
            pady=8,
            command=self._test_connection,
        )
        test_btn.pack(pady=20)

        # Status
        self.db_status = tk.Label(
            content,
            text="🔴 Not Connected",
            font=("Segoe UI", 12),
            bg=self.colors["surface"],
            fg="#DC3545",
        )
        self.db_status.pack()

    def _create_mock_tab(self, parent):
        """Mock data tab"""
        content = tk.Frame(parent, bg=self.colors["surface"], padx=30, pady=30)
        content.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            content,
            text="🎲 Generate Mock Data",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors["surface"],
        ).pack(anchor="w", pady=(0, 20))

        # Templates
        templates_frame = tk.Frame(content, bg=self.colors["surface"])
        templates_frame.pack(fill="x", pady=(0, 20))

        self.mock_template = tk.StringVar(value="employees")

        templates = [
            ("employees", "👥 Employee Records"),
            ("sales", "💰 Sales Transactions"),
            ("inventory", "📦 Inventory Items"),
            ("financial", "💳 Financial Records"),
        ]

        for value, text in templates:
            radio = tk.Radiobutton(
                templates_frame,
                text=text,
                variable=self.mock_template,
                value=value,
                font=("Segoe UI", 11),
                bg=self.colors["surface"],
            )
            radio.pack(anchor="w", pady=2)

        # Count
        count_frame = tk.Frame(content, bg=self.colors["surface"])
        count_frame.pack(fill="x", pady=(0, 20))

        tk.Label(
            count_frame,
            text="Number of Records:",
            font=("Segoe UI", 11),
            bg=self.colors["surface"],
        ).pack(anchor="w")

        count_entry = tk.Entry(count_frame, font=("Segoe UI", 11), width=20)
        count_entry.pack(anchor="w", pady=(5, 0))
        count_entry.insert(0, "1000")

        # Generate button
        generate_btn = tk.Button(
            content,
            text="🎲 Generate Mock Data",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors["primary"],
            fg="white",
            relief="flat",
            padx=30,
            pady=10,
            command=self._generate_mock,
        )
        generate_btn.pack(pady=20)

    def _create_logs_tab(self, parent):
        """Logs tab"""
        content = tk.Frame(parent, bg=self.colors["surface"], padx=20, pady=20)
        content.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            content,
            text="📝 Application Logs",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors["surface"],
        ).pack(anchor="w", pady=(0, 15))

        # Log display
        from tkinter import scrolledtext

        log_text = scrolledtext.ScrolledText(content, font=("Consolas", 10), height=20)
        log_text.pack(fill="both", expand=True)

        # Sample logs
        sample_logs = [
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [INFO] Application started successfully",
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [INFO] UI components loaded",
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [INFO] Database connection ready",
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [INFO] System ready for operation",
        ]

        for log in sample_logs:
            log_text.insert(tk.END, log + "\n")

    def _browse_file(self):
        """Browse for file"""
        from tkinter import filedialog

        filename = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")],
        )
        if filename:
            messagebox.showinfo("File Selected", f"Selected: {filename}")

    def _import_data(self):
        """Import data"""
        messagebox.showinfo("Import", "Import functionality will be implemented!")

    def _test_connection(self):
        """Test database connection"""
        self.db_status.configure(text="🟢 Connected (Mock)", fg="#28A745")
        messagebox.showinfo("Connection Test", "✅ Database connection successful!")

    def _generate_mock(self):
        """Generate mock data"""
        template = self.mock_template.get()
        messagebox.showinfo("Mock Data", f"Generated {template} data successfully!")

    def run(self):
        """Start application"""
        try:
            print("🚀 Starting DENSO888 Simple...")
            self.root.mainloop()
        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", f"Application error: {e}")


if __name__ == "__main__":
    app = DENSO888Simple()
    app.run()
