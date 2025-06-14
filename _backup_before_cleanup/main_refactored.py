# main_refactored.py
"""
🏭 DENSO888 - Refactored Main Entry Point
Simplified, maintainable, and modular approach

Created by: Thammaphon Chittasuwanna (SDM) | Innovation
เฮียตอมจัดหั้ย!!! 🚀
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def setup_environment():
    """Setup application environment"""
    # Ensure required directories exist
    dirs = ["logs", "data", "temp", "exports"]
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)

    # Set environment variables if not set
    if not os.getenv("DENSO888_ENV"):
        os.environ["DENSO888_ENV"] = "development"


def initialize_services() -> bool:
    """Initialize core services"""
    try:
        print("🔧 Initializing services...")

        # Initialize configuration
        from config.manager import get_config_manager

        config_manager = get_config_manager()
        config = config_manager.get_config()

        print(f"📋 Loaded configuration for {config.name} v{config.version}")

        # Validate configuration
        validation = config_manager.validate_config()
        if validation["errors"]:
            print("❌ Configuration errors found:")
            for error in validation["errors"]:
                print(f"  • {error}")
            return False

        if validation["warnings"]:
            print("⚠️ Configuration warnings:")
            for warning in validation["warnings"]:
                print(f"  • {warning}")

        # Initialize core services
        from core.services import init_services

        service_results = init_services()

        # Report service status
        for service, status in service_results.items():
            icon = "✅" if status else "❌"
            print(f"{icon} {service.title()} service: {'OK' if status else 'Failed'}")

        # Check if critical services are running
        critical_services = ["database"]
        critical_ok = all(
            service_results.get(service, False) for service in critical_services
        )

        if not critical_ok:
            print("⚠️ Some critical services failed, but application can still run")

        return True

    except Exception as e:
        print(f"❌ Service initialization failed: {e}")
        return False


def create_application():
    """Create and configure application"""
    try:
        # Get configuration
        from config.manager import get_config

        config = get_config()

        # Create application configuration
        from gui.windows.main_window import AppConfig, create_application

        app_config = AppConfig(
            title=f"🏭 {config.name}",
            version=config.version,
            author=config.author,
            window_size=(config.ui.window_width, config.ui.window_height),
            theme=config.ui.theme,
        )

        # Create application
        app = create_application(app_config)
        return app

    except Exception as e:
        print(f"❌ Application creation failed: {e}")
        return None


def show_startup_info():
    """Show application startup information"""
    from config.manager import get_config

    config = get_config()

    print("=" * 60)
    print(f"🏭 {config.name} v{config.version}")
    print(f"Created by: {config.author}")
    print("เฮียตอมจัดหั้ย!!! 🚀")
    print("=" * 60)
    print(f"Environment: {os.getenv('DENSO888_ENV', 'development')}")
    print(f"Database: {config.database.type}")
    print(f"Theme: {config.ui.theme}")
    print("=" * 60)


def handle_startup_error(error: Exception):
    """Handle startup errors gracefully"""
    print(f"\n❌ Startup Error: {error}")
    print("\n🛠️ Troubleshooting:")
    print("1. Check if all dependencies are installed: pip install -r requirements.txt")
    print("2. Verify database configuration")
    print("3. Check file permissions")
    print("4. Run: python config/manager.py validate")
    print("\n📧 Need help? Contact: Thammaphon Chittasuwanna (SDM)")


def fallback_simple_ui():
    """Fallback to simple UI if modern UI fails"""
    try:
        print("🔄 Loading fallback interface...")

        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.title("🏭 DENSO888 - Simple Mode")
        root.geometry("800x600")

        # Center window
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (400)
        y = (root.winfo_screenheight() // 2) - (300)
        root.geometry(f"+{x}+{y}")

        # Header
        header = tk.Frame(root, bg="#DC0003", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="🏭 DENSO888 - Simple Mode",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#DC0003",
        )
        title.pack(expand=True)

        # Content
        content = tk.Frame(root, bg="white")
        content.pack(fill="both", expand=True, padx=40, pady=40)

        # Welcome message
        welcome = tk.Label(
            content,
            text="Welcome to DENSO888\nExcel to SQL Management System",
            font=("Arial", 14),
            bg="white",
            justify="center",
        )
        welcome.pack(pady=20)

        # Creator info
        creator = tk.Label(
            content,
            text="Created by: Thammaphon Chittasuwanna (SDM)\nเฮียตอมจัดหั้ย!!! 🚀",
            font=("Arial", 12),
            bg="white",
            fg="#666",
            justify="center",
        )
        creator.pack(pady=10)

        # Basic actions
        actions_frame = tk.Frame(content, bg="white")
        actions_frame.pack(pady=30)

        def import_excel():
            from tkinter import filedialog

            file_path = filedialog.askopenfilename(
                title="Select Excel File", filetypes=[("Excel files", "*.xlsx *.xls")]
            )
            if file_path:
                messagebox.showinfo("Selected", f"File: {Path(file_path).name}")

        def show_about():
            about_text = """🏭 DENSO888 v2.0.0 - Refactored Edition

Excel to SQL Management System

Created by: Thammaphon Chittasuwanna (SDM)
Department: Innovation | DENSO Corporation
Nickname: เฮียตอมจัดหั้ย!!!

Features:
• Clean modular architecture
• Service-based design
• Centralized configuration
• Maintainable code structure

© 2024 DENSO Corporation"""
            messagebox.showinfo("About DENSO888", about_text)

        # Action buttons
        buttons = [
            ("📊 Import Excel", import_excel, "#DC0003"),
            (
                "🎲 Mock Data",
                lambda: messagebox.showinfo("Info", "Mock data generation available"),
                "#28A745",
            ),
            (
                "⚙️ Settings",
                lambda: messagebox.showinfo("Info", "Settings panel available"),
                "#007BFF",
            ),
            ("ℹ️ About", show_about, "#6C757D"),
        ]

        for text, command, color in buttons:
            btn = tk.Button(
                actions_frame,
                text=text,
                command=command,
                font=("Arial", 11, "bold"),
                bg=color,
                fg="white",
                padx=20,
                pady=10,
                relief="flat",
                cursor="hand2",
                width=15,
            )
            btn.pack(pady=5)

        # Status bar
        status_bar = tk.Frame(root, bg="#f0f0f0", height=30)
        status_bar.pack(side="bottom", fill="x")
        status_bar.pack_propagate(False)

        status_label = tk.Label(
            status_bar,
            text="🟢 Simple Mode - Ready",
            font=("Arial", 9),
            bg="#f0f0f0",
            fg="#333",
        )
        status_label.pack(side="left", padx=10, pady=5)

        version_label = tk.Label(
            status_bar,
            text="v2.0.0 - Refactored",
            font=("Arial", 9),
            bg="#f0f0f0",
            fg="#666",
        )
        version_label.pack(side="right", padx=10, pady=5)

        print("✅ Simple interface loaded successfully")
        root.mainloop()

        return True

    except Exception as e:
        print(f"❌ Even simple UI failed: {e}")
        return False


def main():
    """Main application entry point"""
    try:
        # Show startup info
        show_startup_info()

        # Setup environment
        print("🔧 Setting up environment...")
        setup_environment()

        # Initialize services
        if not initialize_services():
            print("⚠️ Service initialization had issues, continuing with fallback...")

        # Try to create modern application
        print("🚀 Creating application...")
        app = create_application()

        if app:
            print("✅ Modern interface loaded successfully")
            print("🎉 Starting DENSO888...")
            app.run()
        else:
            print("⚠️ Modern interface failed, trying fallback...")
            if not fallback_simple_ui():
                print("❌ All UI options failed")
                return 1

        print("👋 DENSO888 closed successfully")
        return 0

    except KeyboardInterrupt:
        print("\n⏹️ Application interrupted by user")
        return 0

    except Exception as e:
        handle_startup_error(e)

        # Try fallback UI as last resort
        print("\n🔄 Attempting fallback interface...")
        if fallback_simple_ui():
            return 0
        else:
            return 1


def cli_mode():
    """Command-line interface mode"""
    import argparse

    parser = argparse.ArgumentParser(description="DENSO888 CLI Tools")
    parser.add_argument(
        "--config",
        choices=["show", "validate", "export"],
        help="Configuration management",
    )
    parser.add_argument(
        "--services", choices=["status", "test"], help="Service management"
    )
    parser.add_argument("--mock", help="Generate mock data (template:rows)")
    parser.add_argument("--process", help="Process Excel file")

    args = parser.parse_args()

    if args.config:
        from config.manager import ConfigCLI

        cli = ConfigCLI()

        if args.config == "show":
            cli.show_config()
        elif args.config == "validate":
            cli.validate_config()
        elif args.config == "export":
            cli.export_config()

    elif args.services:
        if args.services == "status":
            from core.services import get_service_manager

            manager = get_service_manager()
            status = manager.get_status_all()

            print("🔧 Service Status:")
            for name, info in status.items():
                print(f"  {name}: {info.get('status', 'unknown')}")

        elif args.services == "test":
            print("🧪 Testing services...")
            initialize_services()

    elif args.mock:
        template, rows = args.mock.split(":")
        rows = int(rows)

        from core.services import get_mock_service

        mock_service = get_mock_service()

        if mock_service:
            result = mock_service.generate_data(template, rows)
            if result.get("success"):
                print(f"✅ Generated {result['rows_generated']:,} rows")
            else:
                print(f"❌ Generation failed: {result.get('error')}")

    elif args.process:
        from core.services import get_excel_service

        excel_service = get_excel_service()

        if excel_service:
            validation = excel_service.validate_file(args.process)
            if validation["valid"]:
                print(f"✅ File validation successful")
                # Process file here
            else:
                print(f"❌ File validation failed: {validation['errors']}")


if __name__ == "__main__":
    # Check if CLI mode
    if len(sys.argv) > 1:
        cli_mode()
    else:
        sys.exit(main())
