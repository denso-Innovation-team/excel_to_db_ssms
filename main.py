"""
main.py - DENSO888 Gaming Edition Entry Point - Fixed Version
เฮียตอมจัดหั้ย!!! 🎮🚀
"""

import sys
import os
import traceback
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def main():
    """Main entry point for DENSO888 Gaming Edition"""
    try:
        print("🎮" + "=" * 60)
        print("🏭 DENSO888 GAMING EDITION v2.0.0")
        print("📊 Excel to SQL Management System")
        print("👨‍💻 Created by: Thammaphon Chittasuwanna (SDM)")
        print("🏢 Innovation Department | DENSO Corporation")
        print("🎮" + "=" * 60)
        print()

        # Check Python version
        if sys.version_info < (3, 8):
            print("❌ Error: Python 3.8 or higher required")
            print(f"   Current version: {sys.version}")
            return

        print("🔍 Checking dependencies...")

        # Check critical dependencies
        missing_deps = []
        try:
            import tkinter

            print("✅ Tkinter available")
        except ImportError:
            missing_deps.append("tkinter")

        try:
            import pandas

            print("✅ Pandas available")
        except ImportError:
            missing_deps.append("pandas")

        if missing_deps:
            print(f"❌ Missing dependencies: {', '.join(missing_deps)}")
            print("   Please install with: pip install -r requirements.txt")
            return

        print("🚀 Loading DENSO888 Gaming Edition...")
        print()

        # Create required directories
        create_required_directories()

        # Import and start the gaming edition
        from gui.main_window import DENSO888GamingEdition

        # Create and run application
        app = DENSO888GamingEdition()

        print("🎯 Starting gaming interface...")
        app.run()

    except KeyboardInterrupt:
        print("\n⚠️  Application interrupted by user")
        print("👋 Thanks for using DENSO888 Gaming Edition!")

    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("\n💡 Possible solutions:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Check if all required files are present")
        print("   3. Verify Python environment")

        # Fallback to simple version
        print("\n🔄 Attempting to load fallback version...")
        try:
            from fallback_main import DENSO888Simple

            app = DENSO888Simple()
            app.run()
        except Exception as fallback_error:
            print(f"❌ Fallback version also failed: {fallback_error}")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print(f"🔍 Error details: {traceback.format_exc()}")
        print("\n💡 Please report this error to the development team")

        # Try emergency fallback
        print("\n🔄 Attempting emergency fallback...")
        try:
            emergency_fallback()
        except Exception:
            print("❌ All systems failed")


def emergency_fallback():
    """Emergency fallback interface"""
    import tkinter as tk
    from tkinter import messagebox

    root = tk.Tk()
    root.title("🏭 DENSO888 - Emergency Mode")
    root.geometry("600x400")
    root.configure(bg="#0A0A0F")

    # Emergency interface
    frame = tk.Frame(root, bg="#1A1A2E", padx=50, pady=50)
    frame.pack(expand=True)

    # Title
    title_label = tk.Label(
        frame,
        text="🏭 DENSO888 EMERGENCY MODE",
        font=("Arial", 16, "bold"),
        bg="#1A1A2E",
        fg="#FF0066",
    )
    title_label.pack(pady=20)

    # Message
    message_label = tk.Label(
        frame,
        text="The main application encountered an error.\nPlease check the console for details.\n\nContact: Thammaphon Chittasuwanna (SDM)",
        font=("Arial", 12),
        bg="#1A1A2E",
        fg="#FFFFFF",
        justify="center",
    )
    message_label.pack(pady=20)

    # Buttons
    def show_info():
        messagebox.showinfo(
            "DENSO888 Info",
            "DENSO888 Gaming Edition v2.0.0\n\n"
            "Excel to SQL Management System\n"
            "Created by: Thammaphon Chittasuwanna (SDM)\n"
            "Department: Innovation Department\n"
            "Company: DENSO Corporation\n\n"
            "เฮียตอมจัดหั้ย!!! 🚀",
        )

    info_btn = tk.Button(
        frame,
        text="📋 System Info",
        command=show_info,
        font=("Arial", 12),
        bg="#007BFF",
        fg="white",
        relief="flat",
        padx=20,
        pady=10,
    )
    info_btn.pack(pady=10)

    exit_btn = tk.Button(
        frame,
        text="🚪 Exit",
        command=root.quit,
        font=("Arial", 12),
        bg="#DC3545",
        fg="white",
        relief="flat",
        padx=20,
        pady=10,
    )
    exit_btn.pack(pady=5)

    root.mainloop()


def check_environment():
    """Check if environment is properly set up"""
    issues = []

    # Check if running from correct directory
    if not os.path.exists("config"):
        issues.append(
            "Config directory not found - make sure you're running from project root"
        )

    if not os.path.exists("gui"):
        issues.append("GUI directory not found - incomplete installation")

    if not os.path.exists("core"):
        issues.append("Core directory not found - incomplete installation")

    if issues:
        print("⚠️  Environment Issues:")
        for issue in issues:
            print(f"   • {issue}")
        print()

    return len(issues) == 0


def create_required_directories():
    """Create required directories if they don't exist"""
    directories = ["config", "logs", "data", "data/imports", "data/exports", "backups"]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

    print("📁 Directory structure verified")


def show_startup_banner():
    """Show startup banner"""
    banner = """
    🎮 ╔══════════════════════════════════════════════════════════╗
    🏭 ║                 DENSO888 GAMING EDITION                  ║
    📊 ║              Excel to SQL Management System              ║
    ⚡ ║                                                          ║
    🎯 ║  🚀 Level up your data management skills!               ║
    🎲 ║  💾 Transform Excel files into powerful databases!      ║
    🛡️ ║  🏆 Unlock achievements as you master data!             ║
    ✨ ║                                                          ║
    👨‍💻 ║  Created by: Thammaphon Chittasuwanna (SDM)             ║
    🏢 ║  Innovation Department | DENSO Corporation               ║
    🎮 ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)
    print("🎮 เฮียตอมจัดหั้ย!!! Ready to game? 🚀")
    print()


if __name__ == "__main__":
    # Show banner
    show_startup_banner()

    # Create required directories
    create_required_directories()

    # Check environment
    if not check_environment():
        print("⚠️  Please fix environment issues before continuing")
        input("Press Enter to continue anyway...")

    # Run main application
    main()
