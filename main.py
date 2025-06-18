#!/usr/bin/env python3
"""
DENSO888 Excel to Database Pool System - Professional Edition
Production-Ready Entry Point with Enhanced Error Handling
"""

import sys
from pathlib import Path
import logging
from datetime import datetime

# Setup project paths FIRST
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))


def setup_environment():
    """Setup enhanced logging and project structure"""
    # Create required directories
    dirs = ["logs", "data", "backups", "exports", "temp", "config", "cache"]

    for dir_name in dirs:
        dir_path = PROJECT_ROOT / dir_name
        dir_path.mkdir(exist_ok=True)
        try:
            dir_path.chmod(0o755)
        except:
            pass

    # Setup logging
    log_file = (
        PROJECT_ROOT / "logs" / f'denso888_{datetime.now().strftime("%Y%m%d")}.log'
    )

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

    logger = logging.getLogger(__name__)
    logger.info("🏭 DENSO888 Professional System Starting...")
    return logger


def check_dependencies():
    """Enhanced dependency checker"""
    required = {
        "pandas": ("Excel processing", "2.0.0"),
        "openpyxl": ("Excel reading", "3.1.0"),
        "tkinter": ("GUI framework", None),
        "pyodbc": ("SQL Server connectivity", "4.0.39"),
        "python-dotenv": ("Configuration", "1.0.0"),
    }

    missing = []

    for package, (desc, min_version) in required.items():
        try:
            if package == "tkinter":
                import tkinter
            else:
                __import__(package)
        except ImportError:
            missing.append(f"{package} ({desc})")

    if missing:
        print("\n❌ Missing Dependencies:")
        for item in missing:
            print(f"   - {item}")
        print("\n💡 Fix with: pip install -r requirements.txt")
        return False

    return True


def main():
    """Enhanced main application entry point"""
    try:
        # Setup environment
        logger = setup_environment()

        # Check dependencies
        if not check_dependencies():
            input("Press Enter to exit...")
            sys.exit(1)

        logger.info("✅ Dependencies OK - Initializing System")

        # Import core application components
        try:
            from services.connection_pool_service import ConnectionPoolService
            from controllers.pool_controller import PoolController
            from controllers.app_controller import AppController
            from services.ui_service import UIService
            from services.excel_service import ExcelService
            from services.backup_service import BackupService
            from gui.main_window import MainWindow

        except ImportError as e:
            logger.error(f"Failed to import core modules: {e}")
            print("❌ Import failed. Please check file structure.")
            input("Press Enter to exit...")
            sys.exit(1)

        # Initialize services with proper dependency injection
        logger.info("🔧 Initializing Services...")

        # Core services
        connection_service = ConnectionPoolService()
        excel_service = ExcelService()
        backup_service = BackupService()
        ui_service = UIService()

        # Controllers
        app_controller = AppController(
            connection_service=connection_service,
            excel_service=excel_service,
            backup_service=backup_service,
            ui_service=ui_service,
        )

        pool_controller = PoolController(connection_service)

        # Link services
        ui_service.set_main_window(None)  # Will be set by MainWindow

        logger.info("🖥️ Creating Main Window...")

        # Create and run main window with both controllers
        main_window = MainWindow(
            controller=app_controller, pool_controller=pool_controller
        )

        # Link UI service to main window
        ui_service.set_main_window(main_window)

        # Start services
        logger.info("🚀 Starting Services...")
        backup_service.start()

        logger.info("✅ System Ready - Launching GUI")

        # Run application
        main_window.run()

    except KeyboardInterrupt:
        logger.info("User interrupted application")

    except Exception as e:
        logger.error(f"❌ Critical Application Error: {e}", exc_info=True)
        print(f"❌ Critical Error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

    finally:
        # Cleanup
        try:
            if "backup_service" in locals():
                backup_service.stop()
            if "connection_service" in locals():
                connection_service.close_all_pools()
            logger.info("🏁 Application shutdown complete")
        except Exception as e:
            logger.error(f"Cleanup error: {e}")


if __name__ == "__main__":
    main()
