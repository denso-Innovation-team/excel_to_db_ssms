#!/usr/bin/env python3
"""
DENSO888 - Excel to SQL Management System
Main Application Entry Point - Fixed Version
Created by เฮียตอมจัดหั้ย!!!
"""

import sys
import logging
from pathlib import Path


# Setup basic logging with proper error handling
def setup_logging():
    """Setup basic logging with fallback"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    try:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_dir / "denso888.log", encoding="utf-8"),
                logging.StreamHandler(),
            ],
        )
    except Exception:
        # Fallback to console only
        logging.basicConfig(level=logging.INFO)


def ensure_environment():
    """Ensure required directories exist"""
    required_dirs = ["logs", "assets/icons", "assets/samples"]
    for dir_path in required_dirs:
        try:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
        except Exception:
            pass  # Skip if can't create


def check_dependencies():
    """Check essential dependencies with better error handling"""
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
        print(
            "💡 Install with: pip install pandas sqlalchemy pyodbc openpyxl python-dotenv tqdm"
        )
        return False

    return True


def load_environment():
    """Load environment variables if available"""
    try:
        from dotenv import load_dotenv

        env_file = Path(".env")
        if env_file.exists():
            load_dotenv(env_file)
            print("✅ Environment variables loaded")
    except ImportError:
        pass  # python-dotenv not installed


def main():
    """Main application entry point with enhanced error handling"""
    print("🏭 DENSO888 - Excel to SQL Management System")
    print("   by เฮียตอมจัดหั้ย!!!")
    print("=" * 50)

    try:
        # Setup logging first
        setup_logging()

        # Setup environment
        ensure_environment()

        # Check dependencies
        if not check_dependencies():
            input("กด Enter เพื่อออก...")
            return 1

        # Load environment variables
        load_environment()

        # Import and run main application
        try:
            from gui.main_window import DENSO888MainWindow
        except ImportError as import_error:
            print(f"❌ Import Error: {import_error}")
            print("💡 ตรวจสอบว่าไฟล์ gui/main_window.py มีอยู่และถูกต้อง")
            input("กด Enter เพื่อออก...")
            return 1

        # Create and run application
        try:
            app = DENSO888MainWindow()
            if hasattr(app, "root") and app.root.winfo_exists():
                print("🚀 Starting DENSO888 application...")
                app.run()
            else:
                print("❌ Failed to initialize GUI (Authentication cancelled)")
                return 1

        except Exception as app_error:
            logging.error(f"Application error: {app_error}", exc_info=True)
            print(f"❌ Application Error: {app_error}")
            print("📄 ตรวจสอบไฟล์ logs/denso888.log สำหรับรายละเอียด")
            return 1

    except KeyboardInterrupt:
        print("\n👋 ถูกยกเลิกโดยผู้ใช้")
        return 0

    except Exception as e:
        logging.error(f"Fatal application error: {e}", exc_info=True)
        print(f"❌ Critical Error: {e}")
        print("📄 ตรวจสอบไฟล์ logs/denso888.log สำหรับรายละเอียด")
        input("กด Enter เพื่อออก...")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
