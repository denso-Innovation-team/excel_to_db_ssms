"""
main.py - DENSO888 Modern Application Entry Point (Fixed)
Excel to SQL Management System with Modern UI 2025
Created by: Thammaphon Chittasuwanna (SDM) | Innovation Department
เฮียตอมจัดหั้ย!!! 🚀
"""

import sys
import os
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import traceback

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Suppress tkinter deprecation warnings
os.environ["TK_SILENCE_DEPRECATION"] = "1"


def setup_environment():
    """Setup application environment and create necessary directories"""
    try:
        print("🔧 Setting up environment...")

        # Create required directories
        directories = [
            "config",
            "logs",
            "data/imports",
            "data/exports",
            "data/samples",
            "assets/icons",
            "assets/images",
            "assets/themes",
            "temp",
            "gui/pages",
            "gui/components",
            "gui/themes",
            "controllers",
            "core",
            "models",
            "features",
            "utils",
        ]

        for directory in directories:
            dir_path = project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)

        print("✅ Environment setup completed")
        return True

    except Exception as e:
        print(f"❌ Environment setup failed: {e}")
        return False


def check_dependencies():
    """Check required Python modules"""
    print("🔍 Checking dependencies...")

    required_modules = {
        "tkinter": "GUI framework",
        "sqlite3": "Database support",
        "pathlib": "File path handling",
        "datetime": "Date/time operations",
        "threading": "Background tasks",
        "json": "Configuration files",
    }

    missing_modules = []

    for module, description in required_modules.items():
        try:
            __import__(module)
            print(f"  ✅ {module} - {description}")
        except ImportError:
            print(f"  ❌ {module} - {description} (MISSING)")
            missing_modules.append(module)

    if missing_modules:
        print(f"\n❌ Missing required modules: {', '.join(missing_modules)}")
        return False

    print("✅ All dependencies satisfied")
    return True


def create_minimal_files():
    """Create minimal required files if they don't exist"""
    try:
        print("📁 Creating minimal required files...")

        # Create __init__.py files
        init_files = [
            "gui/__init__.py",
            "gui/pages/__init__.py",
            "gui/components/__init__.py",
            "gui/themes/__init__.py",
            "controllers/__init__.py",
            "core/__init__.py",
            "models/__init__.py",
            "features/__init__.py",
            "utils/__init__.py",
        ]

        for init_file in init_files:
            file_path = project_root / init_file
            if not file_path.exists():
                file_path.write_text('"""Package init file"""')

        # Create basic config file
        config_file = project_root / "config" / "settings.json"
        if not config_file.exists():
            config_data = {
                "app_name": "DENSO888",
                "version": "2.0.0",
                "theme": "modern",
                "language": "th",
                "window_width": 1400,
                "window_height": 900,
            }
            import json

            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)

        print("✅ Minimal files created")
        return True

    except Exception as e:
        print(f"❌ Failed to create minimal files: {e}")
        return False


def create_fallback_application():
    """Create fallback application if main components fail to load"""

    class FallbackApp:
        def __init__(self):
            self.root = tk.Tk()
            self.root.title("🏭 DENSO888 v2.0.0 - Fallback Mode")
            self.root.geometry("800x600")
            self.root.configure(bg="#F8FAFC")

            self._create_fallback_ui()

        def _create_fallback_ui(self):
            """Create simple fallback UI"""
            # Header
            header_frame = tk.Frame(self.root, bg="#DC0003", height=80)
            header_frame.pack(fill="x")
            header_frame.pack_propagate(False)

            header_content = tk.Frame(header_frame, bg="#DC0003")
            header_content.pack(expand=True)

            title_label = tk.Label(
                header_content,
                text="🏭 DENSO888 - Fallback Mode",
                font=("Segoe UI", 18, "bold"),
                bg="#DC0003",
                fg="white",
            )
            title_label.pack(pady=20)

            # Main content
            main_frame = tk.Frame(self.root, bg="#F8FAFC")
            main_frame.pack(fill="both", expand=True, padx=40, pady=40)

            # Error message
            error_frame = tk.Frame(main_frame, bg="white", relief="solid", bd=1)
            error_frame.pack(expand=True, fill="both", padx=20, pady=20)

            content_frame = tk.Frame(error_frame, bg="white")
            content_frame.pack(expand=True)

            # Icon
            icon_label = tk.Label(
                content_frame, text="⚠️", font=("Segoe UI", 48), bg="white", fg="#FFC107"
            )
            icon_label.pack(pady=(40, 20))

            # Title
            title_label = tk.Label(
                content_frame,
                text="Application Running in Fallback Mode",
                font=("Segoe UI", 16, "bold"),
                bg="white",
                fg="#2C3E50",
            )
            title_label.pack(pady=(0, 15))

            # Message
            message_label = tk.Label(
                content_frame,
                text="Some components couldn't load properly.\nThe application is running with basic functionality.",
                font=("Segoe UI", 12),
                bg="white",
                fg="#64748B",
                justify="center",
            )
            message_label.pack(pady=(0, 30))

            # Button
            restart_btn = tk.Button(
                content_frame,
                text="🔄 Restart Application",
                font=("Segoe UI", 12, "bold"),
                bg="#DC0003",
                fg="white",
                relief="flat",
                bd=0,
                padx=30,
                pady=10,
                cursor="hand2",
                command=self._restart_app,
            )
            restart_btn.pack()

        def _restart_app(self):
            """Restart application"""
            self.root.quit()
            python = sys.executable
            os.execl(python, python, *sys.argv)

        def run(self):
            """Run fallback application"""
            try:
                self.root.mainloop()
            except KeyboardInterrupt:
                print("\n⚠️ Application interrupted by user")
            except Exception as e:
                print(f"❌ Fallback application error: {e}")

    return FallbackApp()


def main():
    """Main application entry point with enhanced error handling"""
    try:
        print("=" * 60)
        print("🏭 DENSO888 Modern Edition v2.0.0")
        print("Excel to SQL Management System")
        print("Created by: Thammaphon Chittasuwanna (SDM)")
        print("Innovation Department | DENSO Corporation")
        print("เฮียตอมจัดหั้ย!!! 🚀")
        print("=" * 60)

        # Environment setup
        if not check_dependencies():
            print("\n⚠️ Some dependencies are missing, but trying to continue...")

        if not setup_environment():
            print("⚠️ Environment setup had issues, but continuing...")

        if not create_minimal_files():
            print("⚠️ Could not create all required files, but continuing...")

        print("\n🚀 Starting application...")

        # Try to import and run the modern application
        try:
            print("📦 Loading modern UI components...")

            # Import the modern application
            try:
                from gui.main_application import DENSO888Application

                print("✅ Modern application loaded successfully")

                app = DENSO888Application()
                print("✅ Application initialized")

                app.run()
                print("✅ Application started successfully")

            except ImportError as e:
                print(f"⚠️ Could not import modern application: {e}")
                print("📦 Trying fallback mode...")

                # Try fallback mode
                app = create_fallback_application()
                app.run()

        except Exception as e:
            print(f"❌ Failed to start main application: {e}")
            print(f"🔍 Error details: {traceback.format_exc()}")

            # Show error dialog and try fallback
            try:
                root = tk.Tk()
                root.withdraw()

                error_msg = (
                    f"Application startup error:\n\n{str(e)}\n\nTrying fallback mode..."
                )
                messagebox.showerror("DENSO888 Startup Error", error_msg)
                root.destroy()

                # Start fallback application
                app = create_fallback_application()
                app.run()

            except Exception as fallback_error:
                print(f"❌ Even fallback mode failed: {fallback_error}")
                input("Press Enter to exit...")
                return 1

        return 0

    except KeyboardInterrupt:
        print("\n⚠️ Application interrupted by user")
        return 0

    except Exception as e:
        print(f"❌ Critical application error: {e}")
        print(f"🔍 Stack trace: {traceback.format_exc()}")

        try:
            root = tk.Tk()
            root.withdraw()
            error_msg = (
                f"Critical error:\n\n{str(e)}\n\nPlease check the console for details."
            )
            messagebox.showerror("DENSO888 Critical Error", error_msg)
            root.destroy()
        except:
            pass

        input("Press Enter to exit...")
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
