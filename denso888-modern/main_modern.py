#!/usr/bin/env python3
"""
DENSO888 Modern Edition - Main Application Entry Point
Created by Thammaphon Chittasuwanna (SDM) | Innovation

A modern, beautiful, and powerful Excel to SQL management system
with advanced analytics, automation, and stunning UI/UX.
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import json
from datetime import datetime
from typing import Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import configurations and utilities
try:
    from config.settings import get_config
    from utils.logger import setup_gui_logger, get_logger
    from utils.error_handler import setup_error_handling
    from gui.themes.theme_manager import ModernThemeManager
    from gui.windows.main_window import ModernDENSO888MainWindow
    from security.auth_manager import ModernAuthManager
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print(
        "💡 Please ensure all dependencies are installed and project structure is correct"
    )
    sys.exit(1)

logger = get_logger(__name__)


class DENSO888Application:
    """Main application controller with modern architecture"""

    def __init__(self):
        self.config = None
        self.theme_manager = None
        self.auth_manager = None
        self.main_window = None
        self.startup_time = datetime.now()

        # Application metadata
        self.app_info = {
            "name": "DENSO888 Modern Edition",
            "version": "2.0.0",
            "build": "Modern-2024",
            "author": "Thammaphon Chittasuwanna",
            "role": "SDM | Innovation",
            "company": "DENSO",
            "description": "Excel to SQL Management System with Advanced Analytics",
            "features": [
                "🎨 Modern UI/UX with Multiple Themes",
                "🤖 AI-Powered Data Insights",
                "⚡ Real-time Performance Monitoring",
                "🔐 Enterprise Security",
                "🔄 Advanced Automation",
                "📊 Interactive Data Visualization",
            ],
        }

    def initialize(self) -> bool:
        """Initialize application components"""
        try:
            logger.info("🚀 Starting DENSO888 Modern Edition initialization...")

            # Setup environment
            self._setup_environment()

            # Load configuration
            self._load_configuration()

            # Initialize theme system
            self._initialize_themes()

            # Setup authentication
            self._initialize_authentication()

            # Setup error handling
            setup_error_handling()

            logger.info("✅ Application initialization completed successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Initialization failed: {e}", exc_info=True)
            self._show_initialization_error(str(e))
            return False

    def _setup_environment(self):
        """Setup application environment and directories"""
        required_dirs = [
            "logs",
            "assets/images",
            "assets/themes",
            "assets/icons",
            "data/cache",
            "data/exports",
            "data/templates",
            "backups",
        ]

        for dir_path in required_dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)

        logger.info("📁 Environment directories created")

    def _load_configuration(self):
        """Load application configuration"""
        try:
            self.config = get_config()
            logger.info(f"⚙️ Configuration loaded for {self.config.app_name}")
        except Exception as e:
            logger.warning(f"⚠️ Using default configuration: {e}")
            # Create minimal config
            self.config = type(
                "Config",
                (),
                {
                    "app_name": self.app_info["name"],
                    "version": self.app_info["version"],
                    "author": self.app_info["author"],
                },
            )()

    def _initialize_themes(self):
        """Initialize theme management system"""
        self.theme_manager = ModernThemeManager()

        # Load user's preferred theme
        preferred_theme = self._load_user_preference("theme", "denso_corporate")

        logger.info(f"🎨 Theme system initialized with '{preferred_theme}' theme")

    def _initialize_authentication(self):
        """Initialize authentication system"""
        self.auth_manager = ModernAuthManager()
        logger.info("🔐 Authentication system initialized")

    def run(self) -> int:
        """Run the main application"""
        try:
            logger.info("🎬 Starting DENSO888 Modern Edition...")

            # Show splash screen
            self._show_splash_screen()

            # Authentication
            if not self._authenticate_user():
                logger.info("🚪 User authentication cancelled")
                return 0

            # Create main window
            self.main_window = ModernDENSO888MainWindow(
                theme_manager=self.theme_manager,
                auth_manager=self.auth_manager,
                config=self.config,
                app_info=self.app_info,
            )

            # Show welcome message
            self._show_welcome_message()

            # Start main loop
            logger.info("🖥️ Starting GUI main loop...")
            self.main_window.run()

            logger.info("👋 Application closed normally")
            return 0

        except KeyboardInterrupt:
            logger.info("⌨️ Application interrupted by user")
            return 0

        except Exception as e:
            logger.error(f"💥 Fatal application error: {e}", exc_info=True)
            self._show_fatal_error(str(e))
            return 1

        finally:
            self._cleanup()

    def _show_splash_screen(self):
        """Show modern splash screen"""
        splash = tk.Tk()
        splash.title("DENSO888")
        splash.geometry("500x300")
        splash.resizable(False, False)
        splash.overrideredirect(True)  # Remove window decorations

        # Center splash screen
        splash.update_idletasks()
        x = (splash.winfo_screenwidth() // 2) - (500 // 2)
        y = (splash.winfo_screenheight() // 2) - (300 // 2)
        splash.geometry(f"500x300+{x}+{y}")

        # Splash content with gradient background
        splash.configure(bg="#FFFFFF")

        # Main container
        main_frame = tk.Frame(splash, bg="#FFFFFF")
        main_frame.pack(fill="both", expand=True)

        # Header section
        header_frame = tk.Frame(main_frame, bg="#DC0003", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        # DENSO logo and title
        title_frame = tk.Frame(header_frame, bg="#DC0003")
        title_frame.pack(expand=True)

        # Logo (using text for now)
        logo_label = tk.Label(
            title_frame, text="🏭", bg="#DC0003", fg="white", font=("Segoe UI", 24)
        )
        logo_label.pack(pady=10)

        title_label = tk.Label(
            title_frame,
            text="DENSO888",
            bg="#DC0003",
            fg="white",
            font=("Segoe UI", 18, "bold"),
        )
        title_label.pack()

        # Content section
        content_frame = tk.Frame(main_frame, bg="#FFFFFF")
        content_frame.pack(fill="both", expand=True, padx=40, pady=30)

        # App info
        info_label = tk.Label(
            content_frame,
            text=self.app_info["description"],
            bg="#FFFFFF",
            fg="#2C3E50",
            font=("Segoe UI", 12),
        )
        info_label.pack(pady=(0, 20))

        # Version info
        version_label = tk.Label(
            content_frame,
            text=f"Version {self.app_info['version']} - {self.app_info['build']}",
            bg="#FFFFFF",
            fg="#7F8C8D",
            font=("Segoe UI", 10),
        )
        version_label.pack(pady=(0, 10))

        # Loading indicator
        loading_frame = tk.Frame(content_frame, bg="#FFFFFF")
        loading_frame.pack(fill="x", pady=20)

        # Progress bar simulation
        progress_bg = tk.Frame(loading_frame, bg="#E5E8EB", height=4)
        progress_bg.pack(fill="x")

        progress_bar = tk.Frame(progress_bg, bg="#DC0003", height=4)
        progress_bar.pack(side="left", fill="y")

        # Animate progress bar
        def animate_progress(width=0):
            max_width = 400
            if width < max_width:
                progress_bar.configure(width=width)
                splash.after(20, lambda: animate_progress(width + 8))
            else:
                splash.after(1000, splash.destroy)

        loading_label = tk.Label(
            loading_frame,
            text="🔄 Loading DENSO888...",
            bg="#FFFFFF",
            fg="#7F8C8D",
            font=("Segoe UI", 9),
        )
        loading_label.pack(pady=(10, 0))

        # Footer with creator info
        footer_frame = tk.Frame(main_frame, bg="#F8F9FA", height=60)
        footer_frame.pack(fill="x")
        footer_frame.pack_propagate(False)

        creator_frame = tk.Frame(footer_frame, bg="#F8F9FA")
        creator_frame.pack(expand=True)

        creator_label = tk.Label(
            creator_frame,
            text=f"Created by {self.app_info['author']}",
            bg="#F8F9FA",
            fg="#2C3E50",
            font=("Segoe UI", 10, "bold"),
        )
        creator_label.pack(pady=(15, 2))

        role_label = tk.Label(
            creator_frame,
            text=f"{self.app_info['role']} | Innovation",
            bg="#F8F9FA",
            fg="#7F8C8D",
            font=("Segoe UI", 9),
        )
        role_label.pack()

        # Start animation
        animate_progress()

        # Show splash for minimum time
        splash.after(3000, splash.destroy)
        splash.mainloop()

    def _authenticate_user(self) -> bool:
        """Handle user authentication with modern UI"""
        try:
            from gui.windows.auth_dialog import ModernLoginDialog

            auth_dialog = ModernLoginDialog(
                theme_manager=self.theme_manager,
                auth_manager=self.auth_manager,
                app_info=self.app_info,
            )

            return auth_dialog.show()

        except ImportError:
            # Fallback to simple authentication
            logger.warning("Using fallback authentication")
            return self._fallback_authentication()

    def _fallback_authentication(self) -> bool:
        """Simple fallback authentication"""
        root = tk.Tk()
        root.withdraw()  # Hide root window

        # Simple login dialog
        username = tk.simpledialog.askstring("Login", "Username:", initialvalue="admin")
        if not username:
            return False

        password = tk.simpledialog.askstring("Login", "Password:", show="*")
        if not password:
            return False

        # Simple validation
        if username == "admin" and password == "admin123":
            logger.info(f"✅ User authenticated: {username}")
            return True
        else:
            messagebox.showerror("Authentication Failed", "Invalid credentials")
            return False

    def _show_welcome_message(self):
        """Show welcome message with app features"""
        welcome_msg = f"""
🎉 Welcome to {self.app_info['name']}!

🚀 What's New in This Version:
{chr(10).join(self.app_info['features'])}

💡 Quick Start Tips:
• Use the Dashboard for real-time monitoring
• Try different themes in the header
• Check out the automation features
• Explore the advanced analytics

🏭 Ready to revolutionize your Excel to SQL workflow!
        """

        logger.info("🎉 Application started successfully")
        logger.info(welcome_msg)

    def _show_initialization_error(self, error_message: str):
        """Show initialization error dialog"""
        root = tk.Tk()
        root.withdraw()

        error_dialog = f"""
❌ DENSO888 Initialization Failed

Error: {error_message}

💡 Troubleshooting:
• Check Python version (3.8+ required)
• Verify all dependencies are installed
• Run: pip install -r requirements.txt
• Check file permissions
• Review logs/denso888.log for details

🔧 Need Help?
Contact: {self.app_info['author']} | {self.app_info['role']}
        """

        messagebox.showerror("Initialization Error", error_dialog)

    def _show_fatal_error(self, error_message: str):
        """Show fatal error dialog"""
        root = tk.Tk()
        root.withdraw()

        fatal_dialog = f"""
💥 DENSO888 Fatal Error

An unexpected error occurred:
{error_message}

📋 Error Details:
• Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
• Version: {self.app_info['version']}
• Build: {self.app_info['build']}

📄 Full error log saved to: logs/denso888.log

🛠️ Recovery Options:
• Restart the application
• Check system resources
• Update dependencies
• Contact technical support

Created by: {self.app_info['author']} | {self.app_info['role']}
        """

        messagebox.showerror("Fatal Error", fatal_dialog)

    def _load_user_preference(self, key: str, default: Any) -> Any:
        """Load user preference from settings file"""
        try:
            settings_file = Path("data/user_preferences.json")
            if settings_file.exists():
                with open(settings_file, "r", encoding="utf-8") as f:
                    preferences = json.load(f)
                return preferences.get(key, default)
        except Exception as e:
            logger.warning(f"Could not load user preferences: {e}")

        return default

    def _save_user_preference(self, key: str, value: Any):
        """Save user preference to settings file"""
        try:
            settings_file = Path("data/user_preferences.json")

            # Load existing preferences
            preferences = {}
            if settings_file.exists():
                with open(settings_file, "r", encoding="utf-8") as f:
                    preferences = json.load(f)

            # Update preference
            preferences[key] = value

            # Save back
            with open(settings_file, "w", encoding="utf-8") as f:
                json.dump(preferences, f, indent=2, ensure_ascii=False)

        except Exception as e:
            logger.warning(f"Could not save user preferences: {e}")

    def _cleanup(self):
        """Cleanup application resources"""
        try:
            # Save user preferences
            if self.theme_manager:
                self._save_user_preference("theme", self.theme_manager.current_theme)

            # Close any open connections
            if self.main_window:
                self.main_window.cleanup()

            # Log shutdown
            runtime = datetime.now() - self.startup_time
            logger.info(f"🏁 Application cleanup completed. Runtime: {runtime}")

        except Exception as e:
            logger.error(f"Cleanup error: {e}")


def check_system_requirements() -> bool:
    """Check if system meets requirements"""
    requirements = {
        "python_version": (3, 8),
        "required_modules": [
            "tkinter",
            "pandas",
            "sqlalchemy",
            "openpyxl",
            "PIL",
            "numpy",
        ],
        "min_memory_mb": 512,
        "min_disk_space_mb": 100,
    }

    # Check Python version
    if sys.version_info < requirements["python_version"]:
        print(
            f"❌ Python {requirements['python_version'][0]}.{requirements['python_version'][1]}+ required"
        )
        return False

    # Check required modules
    missing_modules = []
    for module in requirements["required_modules"]:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)

    if missing_modules:
        print(f"❌ Missing required modules: {', '.join(missing_modules)}")
        print("💡 Install with: pip install -r requirements.txt")
        return False

    print("✅ System requirements met")
    return True


def setup_logging():
    """Setup application logging"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Setup GUI logger
    setup_gui_logger()

    logger = get_logger(__name__)
    logger.info("=" * 60)
    logger.info("🏭 DENSO888 Modern Edition Starting")
    logger.info("=" * 60)

    return logger


def main() -> int:
    """Main application entry point"""
    print("🏭 DENSO888 Modern Edition")
    print("   Created by Thammaphon Chittasuwanna (SDM) | Innovation")
    print("=" * 60)

    try:
        # Check system requirements
        if not check_system_requirements():
            input("Press Enter to exit...")
            return 1

        # Setup logging
        logger = setup_logging()

        # Create and initialize application
        app = DENSO888Application()

        if not app.initialize():
            logger.error("❌ Application initialization failed")
            return 1

        # Run application
        return app.run()

    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
        return 0

    except Exception as e:
        print(f"💥 Fatal error: {e}")

        # Try to log error if possible
        try:
            logger = get_logger(__name__)
            logger.error(f"Fatal error in main: {e}", exc_info=True)
        except:
            pass

        return 1


def create_desktop_shortcut():
    """Create desktop shortcut for easy access"""
    try:
        import winshell
        from win32com.client import Dispatch

        desktop = winshell.desktop()
        path = os.path.join(desktop, "DENSO888 Modern.lnk")
        target = sys.executable
        wDir = str(Path(__file__).parent)
        icon = str(Path(__file__).parent / "assets" / "images" / "favicon.ico")

        shell = Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.Arguments = str(Path(__file__))
        shortcut.WorkingDirectory = wDir
        shortcut.IconLocation = icon
        shortcut.Description = "DENSO888 Modern Edition - Excel to SQL Management"
        shortcut.save()

        print("🔗 Desktop shortcut created")

    except ImportError:
        print("💡 Install pywin32 to create desktop shortcuts")
    except Exception as e:
        print(f"⚠️ Could not create desktop shortcut: {e}")


def print_system_info():
    """Print system information for debugging"""
    import platform

    print("\n📋 System Information:")
    print(f"   OS: {platform.system()} {platform.release()}")
    print(f"   Python: {sys.version}")
    print(f"   Architecture: {platform.architecture()[0]}")
    print(f"   Processor: {platform.processor()}")
    print(f"   Working Directory: {os.getcwd()}")
    print()


if __name__ == "__main__":
    # Handle command line arguments
    if len(sys.argv) > 1:
        if "--info" in sys.argv:
            print_system_info()
            sys.exit(0)
        elif "--shortcut" in sys.argv:
            create_desktop_shortcut()
            sys.exit(0)
        elif "--help" in sys.argv:
            print(
                """
🏭 DENSO888 Modern Edition - Command Line Options

Usage: python main_modern.py [options]

Options:
  --info      Show system information
  --shortcut  Create desktop shortcut
  --help      Show this help message

Examples:
  python main_modern.py           # Start application
  python main_modern.py --info    # Show system info
  python main_modern.py --shortcut # Create shortcut

Created by Thammaphon Chittasuwanna (SDM) | Innovation
            """
            )
            sys.exit(0)

    # Run main application
    sys.exit(main())
