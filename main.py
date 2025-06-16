"""
main.py - DENSO888 Modern Edition Entry Point
Clean and simple entry point that delegates to proper modules
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def create_required_directories():
    """Create necessary directories"""
    directories = ["config", "logs", "data", "backups"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)


def check_dependencies():
    """Check if required dependencies are available"""
    required_modules = ["tkinter", "pandas"]
    missing = []

    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)

    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("   Install with: pip install pandas")
        return False

    return True


def main():
    """Main entry point"""
    try:
        print("🏭 DENSO888 Modern Edition v3.0")
        print("Created by: Thammaphon Chittasuwanna (SDM)")
        print("=" * 50)

        # Check environment
        if not check_dependencies():
            return

        # Create directories
        create_required_directories()

        # Import and run the modern app
        from gui.modern_app import ModernDENSO888App

        app = ModernDENSO888App()
        app.run()

    except KeyboardInterrupt:
        print("\n👋 Application interrupted by user")
    except Exception as e:
        print(f"❌ Application error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
