#!/usr/bin/env python3
"""
DENSO888 - Excel to SQL Management System
Main Application Entry Point
Created by เฮียตอมจัดหั้ย!!!
"""

import sys
import os
import logging
from pathlib import Path

# Setup basic logging
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/denso888.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def ensure_environment():
    """Ensure required directories exist"""
    required_dirs = ["logs", "assets/icons", "assets/samples"]
    for dir_path in required_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)

def check_dependencies():
    """Check essential dependencies"""
    required_modules = ["tkinter", "pandas", "sqlalchemy", "openpyxl"]
    missing = []
    
    for module in required_modules:
        try:
            if module == "tkinter":
                import tkinter
                # Test GUI capability
                root = tkinter.Tk()
                root.withdraw()
                root.destroy()
            else:
                __import__(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main application entry point"""
    print("🏭 DENSO888 - Excel to SQL Management System")
    print("   by เฮียตอมจัดหั้ย!!!")
    print("=" * 50)
    
    try:
        # Setup environment
        ensure_environment()
        
        # Check dependencies
        if not check_dependencies():
            input("Press Enter to exit...")
            return
        
        # Load environment variables
        try:
            from dotenv import load_dotenv
            env_file = Path(".env")
            if env_file.exists():
                load_dotenv(env_file)
        except ImportError:
            pass  # python-dotenv not installed
        
        # Import and run main application
        from gui.main_window import DENSO888MainWindow
        
        app = DENSO888MainWindow()
        app.run()
        
    except ImportError as e:
        print(f"❌ Module Import Error: {e}")
        print("Please check your installation and requirements.txt")
        input("Press Enter to exit...")
        
    except Exception as e:
        logging.error(f"Fatal application error: {e}", exc_info=True)
        print(f"❌ Critical Error: {e}")
        print("Check logs/denso888.log for details")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
