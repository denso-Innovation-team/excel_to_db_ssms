"""
gui/pages/database_page.py
Database Configuration Page Module - Complete Implementation
Created by: Thammaphon Chittasuwanna (SDM) | Innovation Department
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Dict, Any
from pathlib import Path
from gui.components.modern_components import ModernButton
from controllers.app_controller import AppController


class DatabasePage:
    """Database configuration page with complete functionality"""
    
    def __init__(self, parent: tk.Widget, controller: AppController, theme):
        self.parent = parent
        self.controller = controller
        self.theme = theme
        
        # Variables for database settings
        self.db_type_var = tk.StringVar(value="sqlite")
        self.sqlite_file_var = tk.StringVar(value="denso888_data.db")
        self.server_var = tk.StringVar()
        self.database_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.windows_auth_var = tk.BooleanVar(value=True)
        
        # UI Components
        self.sqlite_section: tk.Frame = None
        self.sqlserver_section: tk.Frame = None
        self.credentials_frame: tk.Frame = None
        self.test_button: ModernButton = None
        self.status_label: tk.Label = None
        self.details_frame: tk.Frame = None
        
        self._create_ui()
        self._setup_event_handlers()
    
    def _create_ui(self):
        """Create database configuration UI"""
        main_frame = tk.Frame(self.parent, bg=self.theme.colors.background)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create scrollable frame
        canvas = tk.Canvas(main_frame, bg=self.theme.colors.background)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=self.theme.colors.background)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Database type selection
        self._create_db_type_section()
        
        # SQLite settings
        self._create_sqlite_section()
        
        # SQL Server settings
        self._create_sqlserver_section()
        
        # Test connection and status
        self._create_test_section()
        
        # Connection status display
        self._create_status_section()
    
    def _create_db_type_section(self):
        """Create database type selection section"""
        section_frame = self._create_section("🔧 Database Type")
        
        type_frame = tk.Frame(section_frame, bg=self.theme.colors.background)
        type_frame.pack(fill="x", pady=10)
        
        # SQLite option
        sqlite_frame = tk.Frame(type_frame, bg=self.theme.colors.background)
        sqlite_frame.pack(fill="x", pady=5)
        
        sqlite_radio = tk.Radiobutton(
            sqlite_frame,
            text="SQLite (Local Database)",
            variable=self.db_type_var,
            value="sqlite",
            command=self._on_db_type_changed,
            font=("Segoe UI", 12, "bold"),
            bg=self.theme.colors.background,
            activebackground=self.theme.colors.background
        )
        sqlite_radio.pack(anchor="w")
        
        sqlite_desc = tk.Label(
            sqlite_frame,
            text="   💾 Local file-based database, perfect for single-user scenarios",
            font=("Segoe UI", 10),
            fg=self.theme.colors.text_secondary,
            bg=self.theme.colors.background
        )
        sqlite_desc.pack(anchor="w", padx=(20, 0))
        
        # SQL Server option
        sqlserver_frame = tk.Frame(type_frame, bg=self.theme.colors.background)
        sqlserver_frame.pack(fill="x", pady=5)
        
        sqlserver_radio = tk.Radiobutton(
            sqlserver_frame,
            text="SQL Server (Network Database)",
            variable=self.db_type_var,
            value="sqlserver",
            command=self._on_db_type_changed,
            font=("Segoe UI", 12, "bold"),
            bg=self.theme.colors.background,
            activebackground=self.theme.colors.background
        )
        sqlserver_radio.pack(anchor="w")
        
        sqlserver_desc = tk.Label(
            sqlserver_frame,
            text="   🖥️ Enterprise database for multi-user environments and large datasets",
            font=("Segoe UI", 10),
            fg=self.theme.colors.text_secondary,
            bg=self.theme.colors.background
        )
        sqlserver_desc.pack(anchor="w", padx=(20, 0))
    
    def _create_sqlite_section(self):
        """Create SQLite settings section"""
        self.sqlite_section = self._create_section("📁 SQLite Settings")
        
        file_frame = tk.Frame(self.sqlite_section, bg=self.theme.colors.background)
        file_frame.pack(fill="x", pady=10)
        
        tk.Label(
            file_frame,
            text="Database File:",
            font=("Segoe UI", 11, "bold"),
            fg=self.theme.colors.text_primary,
            bg=self.theme.colors.background
        ).pack(anchor="w")
        
        input_frame = tk.Frame(file_frame, bg=self.theme.colors.background)
        input_frame.pack(fill="x", pady=(5, 0))
        
        sqlite_entry = tk.Entry(
            input_frame,
            textvariable=self.sqlite_file_var,
            font=("Segoe UI", 11),
            relief="solid",
            borderwidth=1
        )
        sqlite_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_btn = ModernButton(
            input_frame,
            text="📁 Browse",
            style="secondary",
            size="small",
            command=self._browse_sqlite_file
        )
        browse_btn.get_widget().pack(side="right")
        
        # SQLite info
        info_frame = tk.Frame(self.sqlite_section, bg=self.theme.colors.background)
        info_frame.pack(fill="x", pady=(10, 0))
        
        info_text = "ℹ️ SQLite is a lightweight, file-based database perfect for development and small-scale applications."
        tk.Label(
            info_frame,
            text=info_text,
            font=("Segoe UI", 9),
            fg=self.theme.colors.text_secondary,
            bg=self.theme.colors.background,
            wraplength=500,
            justify="left"
        ).pack(anchor="w")
    
    def _create_sqlserver_section(self):
        """Create SQL Server settings section"""
        self.sqlserver_section = self._create_section("🖥️ SQL Server Settings")
        
        # Server and database
        conn_frame = tk.Frame(self.sqlserver_section, bg=self.theme.colors.background)
        conn_frame.pack(fill="x", pady=10)
        
        # Server name
        server_frame = tk.Frame(conn_frame, bg=self.theme.colors.background)
        server_frame.pack(fill="x", pady=5)
        
        tk.Label(
            server_frame,
            text="Server Name:",
            font=("Segoe UI", 11, "bold"),
            fg=self.theme.colors.text_primary,
            bg=self.theme.colors.background,
            width=15,
            anchor="w"
        ).pack(side="left")
        
        server_entry = tk.Entry(
            server_frame,
            textvariable=self.server_var,
            font=("Segoe UI", 11),
            relief="solid",
            borderwidth=1
        )
        server_entry.pack(side="left", fill="x", expand=True, padx=(10, 0))
        
        # Database name
        db_frame = tk.Frame(conn_frame, bg=self.theme.colors.background)
        db_frame.pack(fill="x", pady=5)
        
        tk.Label(
            db_frame,
            text="Database Name:",
            font=("Segoe UI", 11, "bold"),
            fg=self.theme.colors.text_primary,
            bg=self.theme.colors.background,
            width=15,
            anchor="w"
        ).pack(side="left")
        
        db_entry = tk.Entry(
            db_frame,
            textvariable=self.database_var,
            font=("Segoe UI", 11),
            relief="solid",
            borderwidth=1
        )
        db_entry.pack(side="left", fill="x", expand=True, padx=(10, 0))
        
        # Authentication method
        auth_frame = tk.Frame(self.sqlserver_section, bg=self.theme.colors.background)
        auth_frame.pack(fill="x", pady=15)
        
        windows_auth_check = tk.Checkbutton(
            auth_frame,
            text="🔐 Use Windows Authentication",
            variable=self.windows_auth_var,
            command=self._on_auth_changed,
            font=("Segoe UI", 11, "bold"),
            bg=self.theme.colors.background,
            activebackground=self.theme.colors.background
        )
        windows_auth_check.pack(anchor="w")
        
        # Username/Password (hidden by default)
        self.credentials_frame = tk.Frame(self.sqlserver_section, bg=self.theme.colors.background)
        self.credentials_frame.pack(fill="x", pady=10)
        
        # Username
        user_frame = tk.Frame(self.credentials_frame, bg=self.theme.colors.background)
        user_frame.pack(fill="x", pady=2)
        
        tk.Label(
            user_frame,
            text="Username:",
            font=("Segoe UI", 11, "bold"),
            fg=self.theme.colors.text_primary,
            bg=self.theme.colors.background,
            width=15,
            anchor="w"
        ).pack(side="left")
        
        user_entry = tk.Entry(
            user_frame,
            textvariable=self.username_var,
            font=("Segoe UI", 11),
            relief="solid",
            borderwidth=1
        )
        user_entry.pack(side="left", fill="x", expand=True, padx=(10, 0))
        
        # Password
        pass_frame = tk.Frame(self.credentials_frame, bg=self.theme.colors.background)
        pass_frame.pack(fill="x", pady=2)
        
        tk.Label(
            pass_frame,
            text="Password:",
            font=("Segoe UI", 11, "bold"),
            fg=self.theme.colors.text_primary,
            bg=self.theme.colors.background,
            width=15,
            anchor="w"
        ).pack(side="left")
        
        pass_entry = tk.Entry(
            pass_frame,
            textvariable=self.password_var,
            font=("Segoe UI", 11),
            relief="solid",
            borderwidth=1,
            show="*"
        )
        pass_entry.pack(side="left", fill="x", expand=True, padx=(10, 0))
        
        # Connection options
        options_frame = tk.Frame(self.sqlserver_section, bg=self.theme.colors.background)
        options_frame.pack(fill="x", pady=15)
        
        tk.Label(
            options_frame,
            text="Connection Options:",
            font=("Segoe UI", 11, "bold"),
            fg=self.theme.colors.text_primary,
            bg=self.theme.colors.background
        ).pack(anchor="w", pady=(0, 5))
        
        self.encrypt_var = tk.BooleanVar(value=True)
        self.trust_cert_var = tk.BooleanVar(value=True)
        
        encrypt_check = tk.Checkbutton(
            options_frame,
            text="🔒 Encrypt connection",
            variable=self.encrypt_var,
            font=("Segoe UI", 10),
            bg=self.theme.colors.background,
            activebackground=self.theme.colors.background
        )
        encrypt_check.pack(anchor="w", padx=(20, 0))
        
        trust_check = tk.Checkbutton(
            options_frame,
            text="🛡️ Trust server certificate",
            variable=self.trust_cert_var,
            font=("Segoe UI", 10),
            bg=self.theme.colors.background,
            activebackground=self.theme.colors.background
        )
        trust_check.pack(anchor="w", padx=(20, 0))
        
        # Initially hide SQL Server settings
        self.sqlserver_section.pack_forget()
    
    def _create_test_section(self):
        """Create test connection section"""
        test_frame = tk.Frame(self.scrollable_frame, bg=self.theme.colors.background)
        test_frame.pack(fill="x", pady=30)
        
        button_container = tk.Frame(test_frame, bg=self.theme.colors.background)
        button_container.pack()
        
        self.test_button = ModernButton(
            button_container,
            text="🔍 Test Connection",
            style="info",
            size="large",
            command=self._test_connection
        )
        test_widget = self.test_button.get_widget()
        test_widget.pack(side="left", padx=(0, 10))
        
        # Save config button
        self.save_button = ModernButton(
            button_container,
            text="💾 Save Configuration",
            style="success",
            size="large",
            command=self._save_configuration
        )
        save_widget = self.save_button.get_widget()
        save_widget.pack(side="left")
    
    def _create_status_section(self):
        """Create connection status display section"""
        section_frame = self._create_section("📊 Connection Status")
        
        self.status_label = tk.Label(
            section_frame,
            text="🔴 Not Connected",
            font=("Segoe UI", 12, "bold"),
            fg=self.theme.colors.danger,
            bg=self.theme.colors.background
        )
        self.status_label.pack(pady=10)
        
        # Connection details frame
        self.details_frame = tk.Frame(section_frame, bg=self.theme.colors.background)
        self.details_frame.pack(fill="x", pady=10)
        
        # Performance info frame
        self.perf_frame = tk.Frame(section_frame, bg=self.theme.colors.surface)
        self.perf_frame.pack(fill="x", pady=10)
        self.perf_frame.pack_propagate(False)
    
    def _create_section(self, title: str) -> tk.Frame:
        """Create a section with title"""
        section_frame = tk.Frame(self.scrollable_frame, bg=self.theme.colors.background)
        section_frame.pack(fill="x", pady=(0, 25))
        
        title_label = tk.Label(
            section_frame,
            text=title,
            font=("Segoe UI", 14, "bold"),
            fg=self.theme.colors.text_primary,
            bg=self.theme.colors.background
        )
        title_label.pack(anchor="w", pady=(0, 15))
        
        return section_frame
    
    def _setup_event_handlers(self):
        """Setup event handlers"""
        # Initially set up UI based on default selection
        self._on_db_type_changed()
        self._on_auth_changed()
        
        # Variable traces
        self.db_type_var.trace('w', lambda *args: self._on_db_type_changed())
        self.windows_auth_var.trace('w', lambda *args: self._on_auth_changed())
    
    def _on_db_type_changed(self):
        """Handle database type change"""
        db_type = self.db_type_var.get()
        
        if db_type == "sqlite":
            self.sqlite_section.pack(fill="x", pady=(0, 25))
            self.sqlserver_section.pack_forget()
        else:
            self.sqlite_section.pack_forget()
            self.sqlserver_section.pack(fill="x", pady=(0, 25))
        
        # Reset status
        self._update_status(False, "Configuration changed")
    
    def _on_auth_changed(self):
        """Handle authentication method change"""
        use_windows_auth = self.windows_auth_var.get()
        
        if use_windows_auth:
            self.credentials_frame.pack_forget()
        else:
            self.credentials_frame.pack(fill="x", pady=10)
    
    def _browse_sqlite_file(self):
        """Browse for SQLite database file"""
        filename = filedialog.asksaveasfilename(
            title="SQLite Database File",
            defaultextension=".db",
            filetypes=[
                ("SQLite Database", "*.db"),
                ("SQLite Database", "*.sqlite"),
                ("All files", "*.*")
            ],
            initialdir=Path.cwd()
        )
        
        if filename:
            self.sqlite_file_var.set(filename)
            self._update_status(False, "Database file changed")
    
    def _test_connection(self):
        """Test database connection"""
        # Prepare configuration
        config_data = self._get_current_config()
        
        # Validate configuration
        if not self._validate_config(config_data):
            return
        
        # Update controller config
        self.controller.update_database_config(config_data)
        
        # Disable test button during testing
        self.test_button.set_enabled(False)
        self._update_status(False, "Testing connection...")
        
        try:
            # Test connection
            success = self.controller.test_database_connection()
            
            if success:
                self._update_status(True, "Connection successful!")
                messagebox.showinfo("Connection Test", "✅ Database connection successful!")
                
                # Show connection performance
                self._show_connection_performance()
            else:
                self._update_status(False, "Connection failed!")
                messagebox.showerror(
                    "Connection Test", 
                    "❌ Database connection failed!\n\nPlease check your settings and try again."
                )
        
        except Exception as e:
            error_msg = f"Connection test error: {str(e)}"
            self._update_status(False, error_msg)
            messagebox.showerror("Connection Test", f"❌ {error_msg}")
        
        finally:
            # Re-enable test button
            self.test_button.set_enabled(True)
    
    def _save_configuration(self):
        """Save current database configuration"""
        config_data = self._get_current_config()
        
        if not self._validate_config(config_data):
            return
        
        try:
            # Update controller configuration
            self.controller.update_database_config(config_data)
            
            # Save to file (if needed)
            # self._save_config_to_file(config_data)
            
            messagebox.showinfo("Save Configuration", "✅ Configuration saved successfully!")
            
        except Exception as e:
            error_msg = f"Failed to save configuration: {str(e)}"
            messagebox.showerror("Save Configuration", f"❌ {error_msg}")
    
    def _get_current_config(self) -> Dict[str, Any]:
        """Get current configuration from UI"""
        config_data = {
            'db_type': self.db_type_var.get(),
            'sqlite_file': self.sqlite_file_var.get(),
            'server': self.server_var.get(),
            'database': self.database_var.get(),
            'username': self.username_var.get(),
            'password': self.password_var.get(),
            'use_windows_auth': self.windows_auth_var.get(),
            'encrypt': getattr(self, 'encrypt_var', tk.BooleanVar()).get(),
            'trust_certificate': getattr(self, 'trust_cert_var', tk.BooleanVar()).get()
        }
        return config_data
    
    def _validate_config(self, config_data: Dict[str, Any]) -> bool:
        """Validate configuration data"""
        db_type = config_data['db_type']
        
        if db_type == "sqlite":
            if not config_data['sqlite_file']:
                messagebox.showerror("Validation Error", "SQLite file path is required")
                return False
        
        elif db_type == "sqlserver":
            if not config_data['server']:
                messagebox.showerror("Validation Error", "Server name is required")
                return False
            
            if not config_data['database']:
                messagebox.showerror("Validation Error", "Database name is required")
                return False
            
            if not config_data['use_windows_auth']:
                if not config_data['username']:
                    messagebox.showerror("Validation Error", "Username is required for SQL Server authentication")
                    return False
                if not config_data['password']:
                    messagebox.showerror("Validation Error", "Password is required for SQL Server authentication")
                    return False
        
        return True
    
    def _update_status(self, connected: bool, message: str = ""):
        """Update connection status display"""
        if connected:
            self.status_label.configure(
                text="🟢 Connected",
                fg=self.theme.colors.success
            )
        else:
            self.status_label.configure(
                text="🔴 Disconnected",
                fg=self.theme.colors.danger
            )
        
        # Clear existing details
        for widget in self.details_frame.winfo_children():
            widget.destroy()
        
        if message:
            detail_label = tk.Label(
                self.details_frame,
                text=message,
                font=("Segoe UI", 10),
                fg=self.theme.colors.text_secondary,
                bg=self.theme.colors.background
            )
            detail_label.pack(anchor="w")
        
        if connected:
            # Show connection details
            self._show_connection_details()
    
    def _show_connection_details(self):
        """Show detailed connection information"""
        db_status = self.controller.get_database_status()
        
        details_text = f"Type: {db_status.get('type', 'Unknown')}"
        
        if db_status.get('type') == 'sqlite':
            file_path = self.sqlite_file_var.get()
            if Path(file_path).exists():
                file_size = Path(file_path).stat().st_size / (1024 * 1024)
                details_text += f"\nFile: {file_path}\nSize: {file_size:.2f} MB"
            else:
                details_text += f"\nFile: {file_path} (new file)"
                
        elif db_status.get('type') == 'sqlserver':
            details_text += f"\nServer: {self.server_var.get()}"
            details_text += f"\nDatabase: {self.database_var.get()}"
            auth_type = "Windows Auth" if self.windows_auth_var.get() else "SQL Auth"
            details_text += f"\nAuthentication: {auth_type}"
        
        detail_label = tk.Label(
            self.details_frame,
            text=details_text,
            font=("Segoe UI", 9),
            fg=self.theme.colors.text_secondary,
            bg=self.theme.colors.background,
            justify="left"
        )
        detail_label.pack(anchor="w", pady=(5, 0))
    
    def _show_connection_performance(self):
        """Show connection performance metrics"""
        # Clear existing performance info
        for widget in self.perf_frame.winfo_children():
            widget.destroy()
        
        # Performance header
        perf_title = tk.Label(
            self.perf_frame,
            text="⚡ Connection Performance",
            font=("Segoe UI", 11, "bold"),
            fg=self.theme.colors.text_primary,
            bg=self.theme.colors.surface
        )
        perf_title.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Mock performance data (replace with real data)
        import time
        start_time = time.time()
        
        # Simple connection test
        try:
            self.controller.test_database_connection()
            response_time = (time.time() - start_time) * 1000  # ms
            
            perf_text = f"Response Time: {response_time:.2f} ms"
            if response_time < 100:
                perf_text += " (Excellent)"
                color = self.theme.colors.success
            elif response_time < 500:
                perf_text += " (Good)"
                color = self.theme.colors.warning
            else:
                perf_text += " (Needs optimization)"
                color = self.theme.colors.danger
            
            perf_label = tk.Label(
                self.perf_frame,
                text=perf_text,
                font=("Segoe UI", 10),
                fg=color,
                bg=self.theme.colors.surface
            )
            perf_label.pack(anchor="w", padx=20, pady=(0, 10))
            
        except Exception:
            pass
    
    def on_db_status_changed(self, connected: bool):
        """Handle database status change from controller"""
        self._update_status(connected)
    
    def refresh(self):
        """Refresh the page"""
        db_status = self.controller.get_database_status()
        connected = db_status.get('connected', False)
        self._update_status(connected)
    
    def get_connection_info(self) -> Dict[str, Any]:
        """Get current connection information"""
        return {
            'db_type': self.db_type_var.get(),
            'connected': self.controller.is_connected,
            'config': self._get_current_config()
        }