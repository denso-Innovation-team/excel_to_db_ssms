"""
Modern Main Window for DENSO888
"""

import tkinter as tk
from tkinter import ttk, messagebox

class ModernDENSO888MainWindow:
    """Modern main window with enhanced UI"""
    
    def __init__(self, theme_manager=None):
        self.theme_manager = theme_manager
        self.root = tk.Tk()
        self._setup_window()
        self._create_ui()
    
    def _setup_window(self):
        """Setup main window"""
        self.root.title("🏭 DENSO888 Modern Edition")
        self.root.geometry("1200x800")
        
        if self.theme_manager:
            self.theme_manager.apply_theme(self.root, "denso_corporate")
    
    def _create_ui(self):
        """Create modern UI"""
        # Header
        header = tk.Frame(self.root, bg="#DC0003", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        title_label = tk.Label(header, 
                              text="🏭 DENSO888 Modern Edition",
                              bg="#DC0003", fg="white",
                              font=("Segoe UI", 16, "bold"))
        title_label.pack(expand=True)
        
        # Content
        content = tk.Frame(self.root, bg="#F8F9FA")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Welcome message
        welcome = tk.Label(content,
                          text="Welcome to DENSO888 Modern Edition!\n\nThis is the new modern interface.\nLegacy features are still available.",
                          bg="#F8F9FA", fg="#2C3E50",
                          font=("Segoe UI", 12),
                          justify="center")
        welcome.pack(expand=True)
        
        # Buttons
        btn_frame = tk.Frame(content, bg="#F8F9FA")
        btn_frame.pack(pady=20)
        
        modern_btn = tk.Button(btn_frame,
                              text="🚀 Modern Features",
                              bg="#DC0003", fg="white",
                              font=("Segoe UI", 10, "bold"),
                              padx=20, pady=10,
                              command=self._show_modern_features)
        modern_btn.pack(side="left", padx=10)
        
        legacy_btn = tk.Button(btn_frame,
                              text="🔄 Legacy Mode", 
                              bg="#2C3E50", fg="white",
                              font=("Segoe UI", 10),
                              padx=20, pady=10,
                              command=self._show_legacy_mode)
        legacy_btn.pack(side="left", padx=10)
        
        # Footer
        footer = tk.Label(self.root,
                         text="Created by Thammaphon Chittasuwanna (SDM) | Innovation",
                         bg="#F8F9FA", fg="#7F8C8D",
                         font=("Segoe UI", 9))
        footer.pack(side="bottom", pady=10)
    
    def _show_modern_features(self):
        """Show modern features info"""
        features = """🎨 Modern Features Available:
        
• Advanced Theme System
• Real-time Dashboard 
• AI-Powered Analytics
• Enhanced Security
• Automation Workflows
• Interactive Visualizations

🚧 Status: Under Development
Some features may not be fully implemented yet."""
        
        messagebox.showinfo("Modern Features", features)
    
    def _show_legacy_mode(self):
        """Switch to legacy mode"""
        result = messagebox.askyesno("Legacy Mode", 
                                   "Switch to legacy DENSO888 interface?\n\nThis will close the modern interface.")
        if result:
            self.root.destroy()
            # Here you could launch legacy app
            print("🔄 Switching to legacy mode...")
    
    def run(self):
        """Run the application"""
        print("🖥️ Starting Modern DENSO888...")
        self.root.mainloop()
        return 0
