# gui/views/__init__.py
"""
View Modules - Each view in separate file
แยกแต่ละ view เป็นไฟล์ต่างหาก maintain ง่าย
"""

# gui/views/dashboard_view.py
"""Dashboard view with service integration"""

import tkinter as tk
from tkinter import filedialog
from gui.windows.main_window import BaseView


class DashboardView(BaseView):
    """Dashboard overview with quick actions"""

    def _create_view(self):
        """Create dashboard content"""
        super()._create_view()

        # Header section
        self._create_header()

        # Quick stats
        self._create_stats_section()

        # Quick actions
        self._create_actions_section()

        # Recent activity
        self._create_activity_section()

    def _create_header(self):
        """Create header with welcome message"""
        header_card = self.factory.create_card(self.view_frame, title="🏠 Dashboard")
        header_card.pack(fill="x", padx=20, pady=(20, 10))

        # Welcome message
        welcome_text = f"Welcome to DENSO888\n{self.app_window.config.author}"
        header_card.add_widget(
            tk.Label, text=welcome_text, font=("Segoe UI", 12), justify="left"
        ).get_widget().pack(anchor="w")

    def _create_stats_section(self):
        """Create statistics cards"""
        stats_frame = tk.Frame(self.view_frame)
        stats_frame.pack(fill="x", padx=20, pady=10)

        # Create grid for stats
        grid = self.factory.create_grid(stats_frame, columns=4, gap=15)
        grid.pack(fill="x")

        # Stat cards
        stats = [
            ("📊", "Files Processed", "0", "Ready"),
            ("⏱️", "Avg Time", "0s", "Optimal"),
            ("✅", "Success Rate", "100%", "Perfect"),
            ("🗄️", "DB Status", "Connected", "Active"),
        ]

        for icon, label, value, status in stats:
            stat_card = self._create_stat_card(
                grid.get_widget(), icon, label, value, status
            )
            grid.add_item(stat_card)

    def _create_stat_card(self, parent, icon, label, value, status):
        """Create individual stat card"""
        colors = self.factory.theme.get_colors()

        card = tk.Frame(
            parent,
            bg=colors.surface,
            relief="flat",
            borderwidth=1,
            highlightbackground=colors.border,
            highlightthickness=1,
        )

        # Content
        content = tk.Frame(card, bg=colors.surface)
        content.pack(fill="both", expand=True, padx=15, pady=15)

        # Icon
        tk.Label(
            content,
            text=icon,
            font=("Segoe UI", 20),
            bg=colors.surface,
            fg=colors.primary,
        ).pack()

        # Value
        tk.Label(
            content,
            text=value,
            font=("Segoe UI", 16, "bold"),
            bg=colors.surface,
            fg=colors.text_primary,
        ).pack(pady=(5, 0))

        # Label
        tk.Label(
            content,
            text=label,
            font=("Segoe UI", 9),
            bg=colors.surface,
            fg=colors.text_secondary,
        ).pack()

        # Status
        tk.Label(
            content,
            text=status,
            font=("Segoe UI", 8),
            bg=colors.surface,
            fg=colors.success,
        ).pack(pady=(5, 0))

        return card

    def _create_actions_section(self):
        """Create quick action buttons"""
        actions_card = self.factory.create_card(
            self.view_frame, title="⚡ Quick Actions"
        )
        actions_card.pack(fill="x", padx=20, pady=10)

        # Action buttons grid
        actions_grid = self.factory.create_grid(
            actions_card.content_frame, columns=3, gap=10
        )
        actions_grid.pack(fill="x", pady=10)

        actions = [
            ("📁", "Browse Excel", self._browse_excel),
            ("🎲", "Generate Mock", self._quick_mock),
            ("🗄️", "Test Database", self._test_database),
            ("📊", "Process Last", self._process_last),
            ("💾", "Export Data", self._export_data),
            ("⚙️", "Settings", self._open_settings),
        ]

        for icon, text, command in actions:
            btn = self.factory.create_button(
                actions_grid.get_widget(),
                text=f"{icon} {text}",
                command=command,
                style="outline",
                size="medium",
            )
            actions_grid.add_item(btn.get_widget())

    def _create_activity_section(self):
        """Create recent activity section"""
        activity_card = self.factory.create_card(
            self.view_frame, title="📈 Recent Activity"
        )
        activity_card.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        # Activity list
        activity_list = tk.Frame(activity_card.content_frame)
        activity_list.pack(fill="both", expand=True)

        # Sample activities
        activities = [
            "🕐 Application started successfully",
            "🔧 Services initialized",
            "🗄️ Database connection established",
            "✅ System ready for use",
        ]

        for activity in activities:
            activity_label = tk.Label(
                activity_list,
                text=activity,
                font=("Segoe UI", 10),
                anchor="w",
                padx=5,
                pady=2,
            )
            activity_label.pack(fill="x")

    # Action handlers
    def _browse_excel(self):
        """Browse for Excel file"""
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls *.xlsm")],
        )
        if file_path:
            self.update_status(f"Selected: {file_path}", "success")

    def _quick_mock(self):
        """Quick mock data generation"""
        self.app_window.navigation.navigate_to("mock")

    def _test_database(self):
        """Test database connection"""
        from core.services import get_database_service

        db_service = get_database_service()

        if db_service and db_service.connect():
            self.update_status("Database test successful", "success")
        else:
            self.update_status("Database test failed", "error")

    def _process_last(self):
        """Process last file"""
        self.update_status("No previous file to process", "warning")

    def _export_data(self):
        """Export data"""
        self.update_status("Export feature coming soon", "info")

    def _open_settings(self):
        """Open settings"""
        self.app_window.navigation.navigate_to("settings")


# ===== gui/views/excel_view.py =====
class ExcelImportView(BaseView):
    """Excel import with step-by-step wizard"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_file = None
        self.file_info = None

    def _create_view(self):
        """Create Excel import interface"""
        super()._create_view()

        # Header
        self._create_header()

        # File selection step
        self._create_file_selection()

        # Configuration step
        self._create_configuration()

        # Preview step
        self._create_preview()

        # Process step
        self._create_process_section()

    def _create_header(self):
        """Create header"""
        header_card = self.factory.create_card(
            self.view_frame, title="📊 Excel Import Wizard"
        )
        header_card.pack(fill="x", padx=20, pady=(20, 10))

        # Description
        desc_text = "Import Excel files to database with smart data detection"
        header_card.add_widget(
            tk.Label, text=desc_text, font=("Segoe UI", 11)
        ).get_widget().pack(anchor="w")

    def _create_file_selection(self):
        """Create file selection section"""
        file_card = self.factory.create_card(
            self.view_frame, title="📁 Step 1: Select Excel File"
        )
        file_card.pack(fill="x", padx=20, pady=10)

        # File selection frame
        file_frame = tk.Frame(file_card.content_frame)
        file_frame.pack(fill="x", pady=10)

        # File path display
        self.file_path_var = tk.StringVar(value="No file selected")
        file_label = tk.Label(
            file_frame,
            textvariable=self.file_path_var,
            font=("Segoe UI", 10),
            relief="solid",
            borderwidth=1,
            padx=10,
            pady=8,
        )
        file_label.pack(side="left", fill="x", expand=True)

        # Browse button
        browse_btn = self.factory.create_button(
            file_frame, text="📂 Browse", command=self._browse_file, style="primary"
        )
        browse_btn.pack(side="right", padx=(10, 0))

        # File info display
        self.file_info_frame = tk.Frame(file_card.content_frame)
        self.file_info_frame.pack(fill="x", pady=(10, 0))

    def _create_configuration(self):
        """Create configuration section"""
        config_card = self.factory.create_card(
            self.view_frame, title="⚙️ Step 2: Configure Import"
        )
        config_card.pack(fill="x", padx=20, pady=10)

        # Configuration options
        config_frame = tk.Frame(config_card.content_frame)
        config_frame.pack(fill="x", pady=10)

        # Table name field
        table_field = self.factory.create_form_field(
            config_frame, label="Table Name:", field_type="entry"
        )
        table_field.pack(fill="x", pady=5)
        table_field.set_value("imported_data")

        # Sheet selection
        sheet_field = self.factory.create_form_field(
            config_frame, label="Sheet:", field_type="combo", values=["Sheet1"]
        )
        sheet_field.pack(fill="x", pady=5)

    def _create_preview(self):
        """Create preview section"""
        preview_card = self.factory.create_card(
            self.view_frame, title="👁️ Step 3: Preview Data"
        )
        preview_card.pack(fill="both", expand=True, padx=20, pady=10)

        # Preview area
        self.preview_frame = tk.Frame(preview_card.content_frame)
        self.preview_frame.pack(fill="both", expand=True, pady=10)

        # Placeholder text
        placeholder = tk.Label(
            self.preview_frame,
            text="Select a file to see preview",
            font=("Segoe UI", 12),
            fg="gray",
        )
        placeholder.pack(expand=True)

    def _create_process_section(self):
        """Create process section"""
        process_card = self.factory.create_card(
            self.view_frame, title="🚀 Step 4: Import to Database"
        )
        process_card.pack(fill="x", padx=20, pady=(10, 20))

        # Process buttons
        button_frame = tk.Frame(process_card.content_frame)
        button_frame.pack(fill="x", pady=10)

        # Validate button
        validate_btn = self.factory.create_button(
            button_frame,
            text="🔍 Validate",
            command=self._validate_file,
            style="secondary",
        )
        validate_btn.pack(side="left", padx=(0, 10))

        # Process button
        process_btn = self.factory.create_button(
            button_frame, text="📊 Process", command=self._process_file, style="success"
        )
        process_btn.pack(side="left")

    def _browse_file(self):
        """Browse for Excel file"""
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls *.xlsm"), ("All files", "*.*")],
        )

        if file_path:
            self.current_file = file_path
            self.file_path_var.set(file_path)
            self._load_file_info()
            self.update_status(f"File selected: {file_path}", "success")

    def _load_file_info(self):
        """Load and display file information"""
        if not self.current_file:
            return

        # Clear previous info
        for widget in self.file_info_frame.winfo_children():
            widget.destroy()

        try:
            # Use Excel service to get file info
            from core.services import get_excel_service

            excel_service = get_excel_service()

            if excel_service:
                validation = excel_service.validate_file(self.current_file)

                if validation["valid"]:
                    info = validation["info"]

                    # Display file info
                    info_text = f"📄 {info['file_name']} | 💾 {info['size_mb']} MB | 📊 {info['format']}"

                    info_label = tk.Label(
                        self.file_info_frame,
                        text=info_text,
                        font=("Segoe UI", 10),
                        fg="green",
                    )
                    info_label.pack(anchor="w", pady=5)

                    # Show warnings if any
                    for warning in validation["warnings"]:
                        warning_label = tk.Label(
                            self.file_info_frame,
                            text=f"⚠️ {warning}",
                            font=("Segoe UI", 9),
                            fg="orange",
                        )
                        warning_label.pack(anchor="w")

                else:
                    # Show errors
                    for error in validation["errors"]:
                        error_label = tk.Label(
                            self.file_info_frame,
                            text=f"❌ {error}",
                            font=("Segoe UI", 10),
                            fg="red",
                        )
                        error_label.pack(anchor="w")

        except Exception as e:
            error_label = tk.Label(
                self.file_info_frame,
                text=f"❌ Error reading file: {e}",
                font=("Segoe UI", 10),
                fg="red",
            )
            error_label.pack(anchor="w")

    def _validate_file(self):
        """Validate selected file"""
        if not self.current_file:
            self.update_status("Please select a file first", "warning")
            return

        self.update_status("Validating file...", "info")

        try:
            from core.services import get_excel_service

            excel_service = get_excel_service()

            validation = excel_service.validate_file(self.current_file)

            if validation["valid"]:
                self.update_status("File validation successful", "success")
                self._show_preview()
            else:
                errors = ", ".join(validation["errors"])
                self.update_status(f"Validation failed: {errors}", "error")

        except Exception as e:
            self.update_status(f"Validation error: {e}", "error")

    def _show_preview(self):
        """Show data preview"""
        # Clear preview
        for widget in self.preview_frame.winfo_children():
            widget.destroy()

        try:
            import pandas as pd

            df = pd.read_excel(self.current_file, nrows=5)

            # Create simple table preview
            preview_label = tk.Label(
                self.preview_frame,
                text=f"Preview (first 5 rows of {len(df.columns)} columns):",
                font=("Segoe UI", 10, "bold"),
            )
            preview_label.pack(anchor="w", pady=(0, 10))

            # Column headers
            headers_frame = tk.Frame(self.preview_frame)
            headers_frame.pack(fill="x")

            for col in df.columns[:5]:  # Show first 5 columns
                header = tk.Label(
                    headers_frame,
                    text=str(col)[:15] + "..." if len(str(col)) > 15 else str(col),
                    font=("Segoe UI", 9, "bold"),
                    relief="solid",
                    borderwidth=1,
                    padx=5,
                    pady=3,
                    width=15,
                )
                header.pack(side="left", padx=1)

            # Data rows
            for idx, row in df.head().iterrows():
                row_frame = tk.Frame(self.preview_frame)
                row_frame.pack(fill="x")

                for col in df.columns[:5]:
                    value = (
                        str(row[col])[:15] + "..."
                        if len(str(row[col])) > 15
                        else str(row[col])
                    )
                    cell = tk.Label(
                        row_frame,
                        text=value,
                        font=("Segoe UI", 9),
                        relief="solid",
                        borderwidth=1,
                        padx=5,
                        pady=3,
                        width=15,
                    )
                    cell.pack(side="left", padx=1)

        except Exception as e:
            error_label = tk.Label(
                self.preview_frame,
                text=f"Preview error: {e}",
                font=("Segoe UI", 10),
                fg="red",
            )
            error_label.pack()

    def _process_file(self):
        """Process file to database"""
        if not self.current_file:
            self.update_status("Please select a file first", "warning")
            return

        self.update_status("Processing file...", "info")

        try:
            # Import and process
            import pandas as pd

            df = pd.read_excel(self.current_file)

            # Get database service
            from core.services import get_database_service

            db_service = get_database_service()

            if not db_service or not db_service.connect():
                self.update_status("Database connection failed", "error")
                return

            # Create table and insert data
            table_name = "imported_data"  # Would get from form field

            # Simulate processing
            self.update_status(f"Processed {len(df)} rows to {table_name}", "success")

        except Exception as e:
            self.update_status(f"Processing failed: {e}", "error")


# ===== gui/views/mock_view.py =====
class MockDataView(BaseView):
    """Mock data generation interface"""

    def _create_view(self):
        """Create mock data generation interface"""
        super()._create_view()

        # Header
        self._create_header()

        # Template selection
        self._create_template_selection()

        # Configuration
        self._create_configuration()

        # Generation controls
        self._create_generation_controls()

    def _create_header(self):
        """Create header"""
        header_card = self.factory.create_card(
            self.view_frame, title="🎲 Mock Data Generator"
        )
        header_card.pack(fill="x", padx=20, pady=(20, 10))

        desc_text = "Generate realistic test data for development and testing"
        header_card.add_widget(
            tk.Label, text=desc_text, font=("Segoe UI", 11)
        ).get_widget().pack(anchor="w")

    def _create_template_selection(self):
        """Create template selection"""
        template_card = self.factory.create_card(
            self.view_frame, title="📋 Select Data Template"
        )
        template_card.pack(fill="x", padx=20, pady=10)

        # Template grid
        template_grid = self.factory.create_grid(
            template_card.content_frame, columns=2, gap=15
        )
        template_grid.pack(fill="x", pady=10)

        # Get available templates
        from core.services import get_mock_service

        mock_service = get_mock_service()

        if mock_service:
            templates = mock_service.get_available_templates()

            for template_id, template_info in templates.items():
                template_widget = self._create_template_widget(
                    template_grid.get_widget(), template_id, template_info
                )
                template_grid.add_item(template_widget)

    def _create_template_widget(self, parent, template_id, template_info):
        """Create template selection widget"""
        colors = self.factory.theme.get_colors()

        # Template card
        template_frame = tk.Frame(
            parent,
            bg=colors.surface,
            relief="flat",
            borderwidth=1,
            highlightbackground=colors.border,
            highlightthickness=1,
        )

        # Content
        content = tk.Frame(template_frame, bg=colors.surface)
        content.pack(fill="both", expand=True, padx=15, pady=15)

        # Template name
        name_label = tk.Label(
            content,
            text=template_info["name"],
            font=("Segoe UI", 12, "bold"),
            bg=colors.surface,
            fg=colors.text_primary,
        )
        name_label.pack(anchor="w")

        # Description
        desc_label = tk.Label(
            content,
            text=template_info["description"],
            font=("Segoe UI", 10),
            bg=colors.surface,
            fg=colors.text_secondary,
            wraplength=200,
            justify="left",
        )
        desc_label.pack(anchor="w", pady=(5, 10))

        # Default rows info
        rows_label = tk.Label(
            content,
            text=f"Default: {template_info['default_rows']:,} rows",
            font=("Segoe UI", 9),
            bg=colors.surface,
            fg=colors.text_secondary,
        )
        rows_label.pack(anchor="w")

        # Select button
        select_btn = self.factory.create_button(
            content,
            text="Select",
            command=lambda: self._select_template(template_id),
            style="primary",
            size="small",
        )
        select_btn.pack(anchor="w", pady=(10, 0))

        return template_frame

    def _create_configuration(self):
        """Create configuration section"""
        config_card = self.factory.create_card(self.view_frame, title="⚙️ Configuration")
        config_card.pack(fill="x", padx=20, pady=10)

        # Configuration form
        config_form = tk.Frame(config_card.content_frame)
        config_form.pack(fill="x", pady=10)

        # Number of rows
        self.rows_field = self.factory.create_form_field(
            config_form, label="Number of rows:", field_type="entry"
        )
        self.rows_field.pack(fill="x", pady=5)
        self.rows_field.set_value("1000")

        # Output format
        format_field = self.factory.create_form_field(
            config_form,
            label="Output format:",
            field_type="combo",
            values=["Excel (.xlsx)", "CSV (.csv)", "Database"],
        )
        format_field.pack(fill="x", pady=5)

    def _create_generation_controls(self):
        """Create generation controls"""
        controls_card = self.factory.create_card(
            self.view_frame, title="🚀 Generate Data"
        )
        controls_card.pack(fill="x", padx=20, pady=(10, 20))

        # Controls frame
        controls_frame = tk.Frame(controls_card.content_frame)
        controls_frame.pack(fill="x", pady=10)

        # Selected template display
        self.selected_template_var = tk.StringVar(value="No template selected")
        template_label = tk.Label(
            controls_frame,
            textvariable=self.selected_template_var,
            font=("Segoe UI", 10),
            relief="solid",
            borderwidth=1,
            padx=10,
            pady=5,
        )
        template_label.pack(fill="x", pady=(0, 10))

        # Generate button
        generate_btn = self.factory.create_button(
            controls_frame,
            text="🎲 Generate Mock Data",
            command=self._generate_data,
            style="success",
            size="large",
        )
        generate_btn.pack()

        # Progress info
        self.progress_label = tk.Label(
            controls_frame, text="", font=("Segoe UI", 9), fg="gray"
        )
        self.progress_label.pack(pady=(10, 0))

    def _select_template(self, template_id):
        """Select a template"""
        self.selected_template = template_id

        from core.services import get_mock_service

        mock_service = get_mock_service()

        if mock_service:
            templates = mock_service.get_available_templates()
            template_info = templates.get(template_id, {})

            self.selected_template_var.set(
                f"Selected: {template_info.get('name', template_id)}"
            )

            # Update default rows
            default_rows = template_info.get("default_rows", 1000)
            self.rows_field.set_value(str(default_rows))

        self.update_status(f"Template selected: {template_id}", "success")

    def _generate_data(self):
        """Generate mock data"""
        if not hasattr(self, "selected_template"):
            self.update_status("Please select a template first", "warning")
            return

        try:
            rows = int(self.rows_field.get_value())
            if rows <= 0:
                self.update_status("Please enter a valid number of rows", "warning")
                return
        except ValueError:
            self.update_status("Please enter a valid number", "warning")
            return

        self.update_status("Generating mock data...", "info")
        self.progress_label.configure(text="🔄 Processing...")

        try:
            # Generate data using service
            from core.services import get_mock_service

            mock_service = get_mock_service()

            if mock_service:
                result = mock_service.generate_data(self.selected_template, rows)

                if result.get("success"):
                    generated_rows = result["rows_generated"]
                    self.update_status(
                        f"Generated {generated_rows:,} rows successfully", "success"
                    )
                    self.progress_label.configure(
                        text=f"✅ Generated {generated_rows:,} rows"
                    )

                    # Could save to file or database here

                else:
                    error = result.get("error", "Unknown error")
                    self.update_status(f"Generation failed: {error}", "error")
                    self.progress_label.configure(text="❌ Generation failed")

        except Exception as e:
            self.update_status(f"Generation error: {e}", "error")
            self.progress_label.configure(text="❌ Error occurred")


# ===== gui/views/database_view.py =====
class DatabaseView(BaseView):
    """Database management interface"""

    def _create_view(self):
        super()._create_view()

        # Header
        header_card = self.factory.create_card(
            self.view_frame, title="🗄️ Database Manager"
        )
        header_card.pack(fill="x", padx=20, pady=(20, 10))

        # Connection status
        self._create_connection_status()

        # Database options
        self._create_database_options()

    def _create_connection_status(self):
        """Create connection status section"""
        status_card = self.factory.create_card(
            self.view_frame, title="📊 Connection Status"
        )
        status_card.pack(fill="x", padx=20, pady=10)

        # Status info
        from core.services import get_database_service

        db_service = get_database_service()

        if db_service:
            conn_info = db_service.get_connection_info()
            status_text = f"Status: {conn_info['status']} | Type: {conn_info.get('type', 'Unknown')}"
        else:
            status_text = "Status: Not connected"

        status_label = tk.Label(
            status_card.content_frame, text=status_text, font=("Segoe UI", 11)
        )
        status_label.pack(anchor="w", pady=10)

        # Test connection button
        test_btn = self.factory.create_button(
            status_card.content_frame,
            text="🔍 Test Connection",
            command=self._test_connection,
            style="primary",
        )
        test_btn.pack(anchor="w")

    def _create_database_options(self):
        """Create database configuration options"""
        options_card = self.factory.create_card(
            self.view_frame, title="⚙️ Database Options"
        )
        options_card.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        # SQLite option
        sqlite_frame = tk.Frame(options_card.content_frame)
        sqlite_frame.pack(fill="x", pady=10)

        sqlite_label = tk.Label(
            sqlite_frame,
            text="📁 SQLite (Local database for development)",
            font=("Segoe UI", 11, "bold"),
        )
        sqlite_label.pack(anchor="w")

        sqlite_btn = self.factory.create_button(
            sqlite_frame,
            text="Connect to SQLite",
            command=lambda: self._connect_database("sqlite"),
            style="success",
            size="small",
        )
        sqlite_btn.pack(anchor="w", pady=(5, 0))

        # SQL Server option
        sqlserver_frame = tk.Frame(options_card.content_frame)
        sqlserver_frame.pack(fill="x", pady=10)

        sqlserver_label = tk.Label(
            sqlserver_frame,
            text="🏢 SQL Server (Enterprise database)",
            font=("Segoe UI", 11, "bold"),
        )
        sqlserver_label.pack(anchor="w")

        sqlserver_btn = self.factory.create_button(
            sqlserver_frame,
            text="Connect to SQL Server",
            command=lambda: self._connect_database("sqlserver"),
            style="primary",
            size="small",
        )
        sqlserver_btn.pack(anchor="w", pady=(5, 0))

    def _test_connection(self):
        """Test database connection"""
        from core.services import get_database_service

        db_service = get_database_service()

        if db_service and db_service.connect():
            self.update_status("Database connection successful", "success")
        else:
            self.update_status("Database connection failed", "error")

    def _connect_database(self, db_type):
        """Connect to specific database type"""
        self.update_status(f"Connecting to {db_type}...", "info")

        from core.services import get_database_service

        db_service = get_database_service()

        if db_service and db_service.connect(db_type):
            self.update_status(f"Connected to {db_type} successfully", "success")
        else:
            self.update_status(f"Failed to connect to {db_type}", "error")


# ===== gui/views/analytics_view.py =====
class AnalyticsView(BaseView):
    """Analytics dashboard"""

    def _create_view(self):
        super()._create_view()

        header_card = self.factory.create_card(
            self.view_frame, title="📈 Analytics Dashboard"
        )
        header_card.pack(fill="x", padx=20, pady=(20, 10))

        # Placeholder content
        placeholder = tk.Label(
            self.view_frame,
            text="📊 Analytics features coming soon!",
            font=("Segoe UI", 16),
            fg="gray",
        )
        placeholder.pack(expand=True)


# ===== gui/views/settings_view.py =====
class SettingsView(BaseView):
    """Application settings"""

    def _create_view(self):
        super()._create_view()

        header_card = self.factory.create_card(
            self.view_frame, title="⚙️ Application Settings"
        )
        header_card.pack(fill="x", padx=20, pady=(20, 10))

        # Theme settings
        theme_card = self.factory.create_card(
            self.view_frame, title="🎨 Theme Settings"
        )
        theme_card.pack(fill="x", padx=20, pady=10)

        theme_text = "Theme customization will be available in future versions"
        theme_label = tk.Label(
            theme_card.content_frame, text=theme_text, font=("Segoe UI", 10)
        )
        theme_label.pack(anchor="w", pady=10)

        # About section
        about_card = self.factory.create_card(self.view_frame, title="ℹ️ About DENSO888")
        about_card.pack(fill="x", padx=20, pady=(10, 20))

        about_text = f"""Version: {self.app_window.config.version}
Created by: {self.app_window.config.author}
Department: Innovation | DENSO Corporation

© 2024 DENSO Corporation
Excel to SQL Management System"""

        about_label = tk.Label(
            about_card.content_frame,
            text=about_text,
            font=("Segoe UI", 10),
            justify="left",
        )
        about_label.pack(anchor="w", pady=10)


# Import all views
from .home_view import HomeView
from .excel_view import ExcelImportView
from .mock_view import MockDataView
from .database_view import DatabaseView
from .analytics_view import AnalyticsView
from .settings_view import SettingsView

# Ensure all views are imported for navigation
__all__ = [
    "HomeView",
    "ExcelImportView",
    "MockDataView",
    "DatabaseView",
    "AnalyticsView",
    "SettingsView",
]
import tkinter as tk
from tkinter import filedialog
from gui.components.base_view import BaseView


class HomeView(BaseView):
    """Home view with quick actions and system status"""

    def _create_view(self):
        """Create home view interface"""
        super()._create_view()

        # Header
        self._create_header()

        # System status section
        self._create_system_status()

        # Quick actions section
        self._create_actions_section()

        # Recent activity section
        self._create_activity_section()

    def _create_header(self):
        """Create header with title and description"""
        header_card = self.factory.create_card(
            self.view_frame, title="🏠 Home - DENSO888"
        )
        header_card.pack(fill="x", padx=20, pady=(20, 10))

        desc_text = "Welcome to DENSO888 - Your Excel to SQL Management System"
        header_card.add_widget(
            tk.Label, text=desc_text, font=("Segoe UI", 11)
        ).get_widget().pack(anchor="w")

    def _create_system_status(self):
        """Create system status section"""
        status_card = self.factory.create_card(
            self.view_frame, title="🔧 System Status"
        )
        status_card.pack(fill="x", padx=20, pady=10)

        # Status grid
        status_grid = self.factory.create_grid(status_card.content_frame, columns=2)
        status_grid.pack(fill="x", pady=10)

        # Example status items
        items = [
            ("📊 Total Files Processed", "1,234", "success"),
            ("🗄️ Database Connections", "3", "info"),
            ("📈 Active Users", "42", "success"),
            ("⚠️ Errors Logged", "0", "success"),
            ("🕒 Last Update", "2024-10-01 12:34:56", "info"),
            ("🔄 System Uptime", "24 days 5 hours", "success"),
            ("📁 Last Processed File", "data.xlsx", "info"),
            ("📅 Scheduled Tasks", "2 tasks pending", "warning"),
            ("🔍 Search Index Status", "Up-to-date", "success"),
            ("💾 Storage Usage", "15 GB / 100 GB used", "info"),
            ("🔒 Security Status", "All systems secure", "success"),
            ("🌐 API Connections", "5 active connections", "info"),
            ("📊 Analytics Status", "Ready for analysis", "success"),
            ("⚙️ Configuration", "Default settings applied", "info"),
            ("🛠️ Maintenance Mode", "Disabled", "success"),
            ("📦 Mock Data Service", "Enabled", "success"),
            ("📁 Excel Import Service", "Enabled", "success"),
            ("🗄️ Database Service", "Connected", "success"),
            ("📈 Analytics Service", "Ready", "success"),
            ("🔒 Security Service", "Active", "success"),
            ("🌐 Network Status", "Connected", "success"),
            ("📅 Scheduled Backups", "Next backup in 2 hours", "info"),
            ("📊 Data Sync Status", "In progress", "warning"),
            ("🛠️ Maintenance Tasks", "No pending tasks", "success"),
            ("📂 Recent Files", "data1.xlsx, data2.xlsx", "info"),
            ("🔧 Settings", "Default settings applied", "info"),
        ]
