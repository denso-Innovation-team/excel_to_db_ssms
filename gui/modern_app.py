"""
gui/modern_app.py
Main Application Entry Point - DENSO888 Modern Edition
"""

import sys
from pathlib import Path

# Setup paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import tkinter as tk
from gui.main_window import MainWindow


class ModernDENSO888App:
    """Main application class"""
    
    def __init__(self):
        self.main_window = None
        
    def run(self):
        """Start the application"""
        try:
            print("🎨 Initializing DENSO888 Modern Edition...")
            
            # Create main window
            self.main_window = MainWindow()
            
            print("✅ DENSO888 Modern Edition started successfully!")
            
            # Start main loop
            self.main_window.run()
            
        except Exception as e:
            print(f"❌ Application startup failed: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    app = ModernDENSO888App()
    app.run()
