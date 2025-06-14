"""
main.py - DENSO888 Complete Application Entry Point
Excel to SQL Management System with Full Features
Created by: Thammaphon Chittasuwanna (SDM) | Innovation Department
เฮียตอมจัดหั้ย!!! 🚀
"""

import sys
import os
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))
os.environ["TK_SILENCE_DEPRECATION"] = "1"


def setup_environment():
    """Setup application environment"""
    try:
        directories = [
            "config",
            "logs",
            "data/imports",
            "data/exports",
            "assets/icons",
            "assets/images",
            "temp",
        ]

        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)

        return True
    except Exception as e:
        print(f"Environment setup failed: {e}")
        return False


def check_dependencies():
    """Check required dependencies"""
    required_modules = ["tkinter", "sqlite3"]
    missing_modules = []

    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)

    if missing_modules:
        print("❌ Missing dependencies:")
        for module in missing_modules:
            print(f"   - {module}")
        return False

    return True


def main():
    """Main application entry point"""
    try:
        print("🏭 Starting DENSO888...")
        print("Created by: Thammaphon Chittasuwanna (SDM)")
        print("Innovation Department | DENSO Corporation")
        print("เฮียตอมจัดหั้ย!!! 🚀")
        print("=" * 50)

        if not check_dependencies():
            input("Press Enter to exit...")
            return 1

        if not setup_environment():
            print("❌ Failed to setup application environment")
            input("Press Enter to exit...")
            return 1

        # Import and run main GUI
        from gui.main_application import DENSO888Application

        print("✅ Starting GUI application...")
        app = DENSO888Application()
        app.run()

        return 0

    except KeyboardInterrupt:
        print("\n⚠️ Application interrupted by user")
        return 0
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("DENSO888 Error", f"Application error:\n\n{str(e)}")
        except:
            pass
        input("Press Enter to exit...")
        return 1


if __name__ == "__main__":
    sys.exit(main())
