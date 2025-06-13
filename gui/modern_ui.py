"""Modern UI implementation"""

import tkinter as tk
from tkinter import ttk, messagebox
from .base_window import BaseWindow

class ModernWindow(BaseWindow):
    """Modern UI with enhanced features"""
    
    def create_ui(self):
        """Create modern UI"""
        # Header
        header = tk.Frame(self.root, bg="#DC0003", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        title = tk.Label(header, text="🏭 DENSO888 Modern", 
                        bg="#DC0003", fg="white",
                        font=("Segoe UI", 14, "bold"))
        title.pack(expand=True)
        
        # Content
        content = tk.Frame(self.root, bg="#F8F9FA")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Welcome
        welcome = tk.Label(content,
                          text="Modern Interface Ready\n\nClick buttons below to test features:",
                          bg="#F8F9FA", fg="#2C3E50",
                          font=("Segoe UI", 12))
        welcome.pack(pady=30)
        
        # Buttons
        btn_frame = tk.Frame(content, bg="#F8F9FA")
        btn_frame.pack()
        
        tk.Button(btn_frame, text="🚀 Process Data",
                 bg="#DC0003", fg="white", font=("Segoe UI", 10),
                 padx=20, pady=10,
                 command=lambda: messagebox.showinfo("Info", "Data processing feature")).pack(side="left", padx=10)
                 
        tk.Button(btn_frame, text="⚙️ Settings",
                 bg="#2C3E50", fg="white", font=("Segoe UI", 10),
                 padx=20, pady=10,
                 command=lambda: messagebox.showinfo("Info", "Settings feature")).pack(side="left", padx=10)
