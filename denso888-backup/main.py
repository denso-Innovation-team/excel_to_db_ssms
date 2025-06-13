#!/usr/bin/env python3
"""
DENSO888 - Excel to SQL Management System  
Main Application Entry Point - Tkinter Fixed Version
"""

import sys
import logging
from pathlib import Path


def setup_logging():
    """Setup basic logging"""
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
        logging.basicConfig(level=logging.INFO)


def ensure_environment():
    """Ensure required directories exist"""
    required_dirs = ["logs", "assets/icons", "assets/samples"]
    for dir_path in required_dirs:
        try:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
        except Exception:
            pass


def check_dependencies():
    """Check essential dependencies - FIXED VERSION"""
    required_modules = ["pandas", "sqlalchemy", "openpyxl"]
    missing = []

    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError:
            missing.append(module)
            print(f"  ❌ {module}")

    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("💡 Install: pip install pandas sqlalchemy pyodbc openpyxl python-dotenv tqdm")
        return False

    # Test Tkinter separately - better error handling
    try:
        import tkinter as tk
        # Quick test without full initialization
        root = tk.Tk()
        root.withdraw()
        root.quit()
        root.destroy()
        print("  ✅ tkinter (GUI ready)")
        return True
    except Exception as e:
        print(f"  ⚠️ tkinter issue: {e}")
        print("💡 GUI may not work - check Python installation")
        
        # Ask user if they want to continue
        try:
            choice = input("Continue anyway? (y/N): ").lower()
            return choice in ['y', 'yes']
        except KeyboardInterrupt:
            return False


def load_environment():
    """Load environment variables"""
    try:
        from dotenv import load_dotenv
        env_file = Path(".env")
        if env_file.exists():
            load_dotenv(env_file)
            print("✅ Environment variables loaded")
    except ImportError:
        pass


def main():
    """Main application entry point - Enhanced"""
    print("🏭 DENSO888 - Excel to SQL Management System")
    print("   by เฮียตอมจัดหั้ย!!!")
    print("=" * 50)

    try:
        setup_logging()
        ensure_environment()

        print("📦 Checking dependencies...")
        if not check_dependencies():
            input("กด Enter เพื่อออก...")
            return 1

        load_environment()

        # Import GUI application
        try:
            from gui.main_window import DENSO888MainWindow
            print("📱 Importing GUI components...")
        except ImportError as import_error:
            print(f"❌ Import Error: {import_error}")
            print("💡 ตรวจสอบโฟลเดอร์ gui/ และไฟล์ที่เกี่ยวข้อง")
            input("กด Enter เพื่อออก...")
            return 1

        # Create and run application
        try:
            print("🚀 Starting DENSO888 application...")
            app = DENSO888MainWindow()
            
            if hasattr(app, "root") and app.root:
                app.run()
                return 0
            else:
                print("❌ Failed to initialize GUI (Authentication cancelled)")
                return 1

        except Exception as app_error:
            logging.error(f"Application error: {app_error}", exc_info=True)
            print(f"❌ Application Error: {app_error}")
            print("📄 Check logs/denso888.log for details")
            
            # Show common solutions
            print("\n💡 Common solutions:")
            print("1. Reinstall Python with Tkinter support")
            print("2. Use system Python instead of virtual environment")
            print("3. Install tkinter package separately")
            
            return 1

    except KeyboardInterrupt:
        print("\n👋 Cancelled by user")
        return 0

    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        print(f"❌ Critical Error: {e}")
        print("📄 Check logs/denso888.log for details")
        input("กด Enter เพื่อออก...")
        return 1


if __name__ == "__main__":
    sys.exit(main())
