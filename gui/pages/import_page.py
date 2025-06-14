"""
gui/pages/import_page.py
Excel Import Page Module
Created by: Thammaphon Chittasuwanna (SDM) | Innovation Department
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from typing import Optional, Dict, Any
from gui.components.modern_components import ModernButton, FileSelector
from controllers.app_controller import AppController


class ImportPage:
    """Excel import page with modern UI"""
    
    def __init__(self, parent: tk.Widget, controller: AppController, theme):
        self.parent = parent
        self.controller = controller
        self.theme = theme
        
        # Variables
        self.table_name = tk.StringVar(value="imported_data")
        self.file_info: Optional[Dict[str, Any]] = None
        
        # UI Components
        self.file_selector: Optional[FileSelector] = None
        self.file_info_text: Optional[tk.Text] = None
        self.import_button: Optional[ModernButton] = None
        
        self._create_ui()
        self._setup_event_handlers()
    
    def _create_ui(self):
        """Create import page UI"""
        # Main container
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
        
        # File selection section
        self._create_file_selection_section()
        
        # File information section
        self._create_file_info_section()
        
        # Import settings section
        self._create_import_settings_section()
        
        # Action buttons section
        self._create_action_buttons_section()
    
    def _create_file_selection_section(self):
        """Create file selection section"""
        section_frame = self._create_section("📁 Select Excel File")
        
        # File selector
        filetypes = [
            ("Excel files", "*.xlsx *.xls *.xlsm"),
            ("Excel 2007+", "*.xlsx *.xlsm"),
            ("Excel 97-2003", "*.xls"),
            ("All files", "*.*")
        ]
        
        self.file_selector = FileSelector(
            section_frame,
            title="Choose Excel file to import",
            filetypes=filetypes
        )
        
        file_widget = self.file_selector.get_widget()
        file_widget.pack(fill="x", pady=10)
        
        # Bind file selection event
        self.file_selector.bind_event('file_selected', self._on_file_selected)
    
    def _create_file_info_section(self):
        """Create file information display section"""
        self.info_section = self._create_section("📋 File Information")
        
        # Info text widget
        self.file_info_text = tk.Text(
            self.info_section,
            height=8,
            font=("Consolas", 9),
            relief="solid",
            borderwidth=1,
            state="disabled",
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary
        )
        self.file_info_text.pack(fill="x", pady=10)
        
        # Initially hide this section
        self.info_section.pack_forget()
    
    def _create_import_settings_section(self):
        """Create import settings section"""
        section_frame = self._create_section("⚙️ Import Settings")
        
        # Table name setting
        table_frame = tk.Frame(section_frame, bg=self.theme.colors.background)
        table_frame.pack(fill="x", pady=10)
        
        tk.Label(
            table_frame,
            text="Table Name:",
            font=("Segoe UI", 11, "bold"),
            fg=self.theme.colors.text_primary,
            bg=self.theme.colors.background
        ).pack(side="left")
        
        table_entry = tk.Entry(
            table_frame,
            textvariable=self.table_name,
            font=("Segoe UI", 11),
            relief="solid",
            borderwidth=1,
            width=30
        )
        table_entry.pack(side="left", padx=(15, 0))
        
        # Auto-generate button
        auto_btn = ModernButton(
            table_frame,
            text="🔄 Auto Generate",
            style="secondary",
            size="small",
            command=self._auto_generate_table_name
        )
        auto_btn.get_widget().pack(side="left", padx=(10, 0))
        
        # Additional settings
        settings_frame = tk.Frame(section_frame, bg=self.theme.colors.background)
        settings_frame.pack(fill="x", pady=(10, 0))
        
        # Options checkboxes
        self.clean_data_var = tk.BooleanVar(value=True)
        self.auto_types_var = tk.BooleanVar(value=True)
        self.backup_var = tk.BooleanVar(value=False)
        
        clean_check = tk.Checkbutton(
            settings_frame,
            text="🧹 Clean and normalize data",
            variable=self.clean_data_var,
            font=("Segoe UI", 10),
            bg=self.theme.colors.background,
            activebackground=self.theme.colors.background
        )
        clean_check.pack(anchor="w", pady=2)
        
        types_check = tk.Checkbutton(
            settings_frame,
            text="🎯 Auto-detect data types",
            variable=self.auto_types_var,
            font=("Segoe UI", 10),
            bg=self.theme.colors.background,
            activebackground=self.theme.colors.background
        )
        types_check.pack(anchor="w", pady=2)
        
        backup_check = tk.Checkbutton(
            settings_frame,
            text="💾 Create backup before import",
            variable=self.backup_var,
            font=("Segoe UI", 10),
            bg=self.theme.colors.background,
            activebackground=self.theme.colors.background
        )
        backup_check.pack(anchor="w", pady=2)
    
    def _create_action_buttons_section(self):
        """Create action buttons section"""
        button_frame = tk.Frame(self.scrollable_frame, bg=self.theme.colors.background)
        button_frame.pack(fill="x", pady=30)
        
        # Import button
        self.import_button = ModernButton(
            button_frame,
            text="🚀 Import to Database",
            icon="",
            style="primary",
            size="large",
            command=self._start_import
        )
        import_widget = self.import_button.get_widget()
        import_widget.pack(pady=10)
        
        # Initially disabled
        self.import_button.set_enabled(False)
        
        # Preview button
        self.preview_button = ModernButton(
            button_frame,
            text="👁️ Preview Data",
            style="secondary",
            size="medium",
            command=self._preview_data
        )
        preview_widget = self.preview_button.get_widget()
        preview_widget.pack(pady=(0, 10))
        
        # Initially disabled
        self.preview_button.set_enabled(False)
    
    def _create_section(self, title: str) -> tk.Frame:
        """Create a section with title"""
        section_frame = tk.Frame(self.scrollable_frame, bg=self.theme.colors.background)
        section_frame.pack(fill="x", pady=(0, 25))
        
        # Section title
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
        # Table name auto-generation
        self.table_name.trace('w', self._on_table_name_changed)
    
    def _on_file_selected(self, file_path: str):
        """Handle file selection"""
        if file_path:
            # Start file analysis
            self.controller.select_file(file_path)
            
            # Auto-generate table name
            self._auto_generate_table_name()
    
    def _on_table_name_changed(self, *args):
        """Handle table name change"""
        self._update_import_button_state()
    
    def _auto_generate_table_name(self):
        """Auto-generate table name from file"""
        if self.file_selector:
            file_path = self.file_selector.get_file()
            if file_path:
                # Generate name from filename
                filename = Path(file_path).stem
                # Clean filename for use as table name
                clean_name = "".join(c if c.isalnum() else "_" for c in filename)
                clean_name = f"imported_{clean_name}_{tk.StringVar().get()}"
                
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M")
                table_name = f"imported_{clean_name}_{timestamp}"
                
                self.table_name.set(table_name[:50])  # Limit length
    
    def _update_import_button_state(self):
        """Update import button enabled state"""
        has_file = bool(self.file_selector and self.file_selector.get_file())
        has_table_name = bool(self.table_name.get().strip())
        is_connected = self.controller.is_connected
        
        can_import = has_file and has_table_name and is_connected
        
        if self.import_button:
            self.import_button.set_enabled(can_import)
        if self.preview_button:
            self.preview_button.set_enabled(has_file)
    
    def _start_import(self):
        """Start import process"""
        if not self.controller.is_connected:
            messagebox.showerror("Import Error", "Database not connected. Please configure database settings first.")
            return
        
        table_name = self.table_name.get().strip()
        if not table_name:
            messagebox.showwarning("Import Error", "Please enter a table name.")
            return
        
        # Prepare import options
        options = {
            'clean_data': self.clean_data_var.get(),
            'auto_detect_types': self.auto_types_var.get(),
            'create_backup': self.backup_var.get()
        }
        
        # Show confirmation dialog
        if messagebox.askyesno(
            "Confirm Import",
            f"Import data to table '{table_name}'?\n\nThis operation may take some time depending on file size."
        ):
            # Start import
            self.controller.import_excel_data(table_name, options)
    
    def _preview_data(self):
        """Preview data before import"""
        file_info = self.controller.get_file_info()
        if file_info and 'sample_data' in file_info:
            self._show_preview_window(file_info['sample_data'])
    
    def _show_preview_window(self, sample_data):
        """Show data preview window"""
        preview_window = tk.Toplevel(self.parent)
        preview_window.title("Data Preview")
        preview_window.geometry("800x600")
        preview_window.grab_set()
        
        # Create treeview for data