"""Base window implementation"""

import tkinter as tk
from abc import ABC, abstractmethod

class BaseWindow(ABC):
    """Base class for all GUI windows"""
    
    def __init__(self, config=None):
        self.config = config
        self.root = None
        self.is_running = False
        
    def setup_window(self):
        """Common window setup"""
        self.root = tk.Tk()
        self.root.title("🏭 DENSO888")
        self.root.geometry("1200x800")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def on_close(self):
        """Handle window close"""
        self.is_running = False
        if self.root:
            self.root.destroy()
            
    @abstractmethod
    def create_ui(self):
        """Create UI elements - implement in subclass"""
        pass
        
    def run(self) -> int:
        """Run the application"""
        try:
            self.setup_window()
            self.create_ui()
            self.is_running = True
            self.root.mainloop()
            return 0
        except Exception as e:
            print(f"Error: {e}")
            return 1
