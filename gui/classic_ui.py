"""Classic UI implementation"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from .base_window import BaseWindow

class ClassicWindow(BaseWindow):
    """Classic UI with essential features"""
    
    def __init__(self, config=None):
        super().__init__(config)
        self.data_source_type = tk.StringVar(value="mock")
        self.db_type = tk.StringVar(value="sqlite")
        
    def create_ui(self):
        """Create classic UI"""
        # Main container
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left panel - Configuration
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side="left", fill="y", padx=(0, 10))
        
        self._create_data_source_config(left_frame)
        self._create_database_config(left_frame) 
        self._create_controls(left_frame)
        
        # Right panel - Results
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True)
        
        self._create_results_panel(right_frame)
        
    def _create_data_source_config(self, parent):
        """Data source configuration"""
        frame = ttk.LabelFrame(parent, text="📊 Data Source", padding=10)
        frame.pack(fill="x", pady=(0, 10))
        
        ttk.Radiobutton(frame, text="🎲 Mock Data", 
                       variable=self.data_source_type, value="mock").pack(anchor="w")
        ttk.Radiobutton(frame, text="📁 Excel File",
                       variable=self.data_source_type, value="excel").pack(anchor="w")
                       
    def _create_database_config(self, parent):
        """Database configuration"""
        frame = ttk.LabelFrame(parent, text="🗄️ Database", padding=10)
        frame.pack(fill="x", pady=(0, 10))
        
        ttk.Radiobutton(frame, text="📁 SQLite", 
                       variable=self.db_type, value="sqlite").pack(anchor="w")
        ttk.Radiobutton(frame, text="🏢 SQL Server",
                       variable=self.db_type, value="sqlserver").pack(anchor="w")
                       
    def _create_controls(self, parent):
        """Control buttons"""
        frame = ttk.LabelFrame(parent, text="⚙️ Controls", padding=10)
        frame.pack(fill="x", pady=(0, 10))
        
        ttk.Button(frame, text="🚀 Start Processing",
                  command=self._start_processing).pack(fill="x", pady=2)
        ttk.Button(frame, text="🔐 Test DB",
                  command=self._test_db).pack(fill="x", pady=2)
                  
    def _create_results_panel(self, parent):
        """Results display"""
        frame = ttk.LabelFrame(parent, text="📊 Results", padding=10)
        frame.pack(fill="both", expand=True)
        
        self.results_text = tk.Text(frame, wrap="word", font=("Consolas", 10))
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.results_text.yview)
        
        self.results_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
    def _start_processing(self):
        """Start data processing"""
        source = self.data_source_type.get()
        db = self.db_type.get()
        
        self.results_text.insert(tk.END, f"Processing {source} data to {db}...\n")
        messagebox.showinfo("Processing", f"Would process {source} → {db}")
        
    def _test_db(self):
        """Test database connection"""
        db = self.db_type.get()
        self.results_text.insert(tk.END, f"Testing {db} connection...\n")
        messagebox.showinfo("DB Test", f"Testing {db} connection")
