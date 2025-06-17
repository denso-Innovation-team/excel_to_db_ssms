#!/usr/bin/env python3
"""
<<<<<<< HEAD
DENSO888 Excel to Database Pool System - Fixed Version
Enhanced Excel to SQL Server Import System with Connection Pooling
Created by: Thammaphon Chittasuwanna (SDM) | Innovation Department
Version: 3.0.0
=======
main.py
Enhanced Excel to Database Pool System Entry Point
>>>>>>> 1f635ed4a112b37ae7a89b809261dfeb1fe63138
"""

import sys
from pathlib import Path
import logging
from datetime import datetime

<<<<<<< HEAD
# Setup project paths FIRST
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))


def setup_environment():
    """Setup logging and required directories"""
    # Create required directories
    dirs = ["logs", "data", "backups", "exports", "temp", "config"]
    for dir_name in dirs:
        (PROJECT_ROOT / dir_name).mkdir(exist_ok=True)

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
    logger.info("🏭 DENSO888 Pool System Starting...")
    return logger


def create_missing_files():
    """Create missing files with basic implementations"""

    # Create basic pool_controller if missing
    pool_controller_path = Path("controllers/pool_controller.py")
    if not pool_controller_path.exists():
        pool_controller_path.parent.mkdir(exist_ok=True)
        with open(pool_controller_path, "w", encoding="utf-8") as f:
            f.write(
                '''"""
Basic Pool Controller - Minimal Implementation
"""

class PoolController:
    def __init__(self, pool_service):
        self.pool_service = pool_service
        self.event_callbacks = {}
        self.current_excel_file = None
        
    def register_callback(self, event, callback):
        if event not in self.event_callbacks:
            self.event_callbacks[event] = []
        self.event_callbacks[event].append(callback)
    
    def test_database_connection(self, config):
        return False, "Not implemented"
    
    def connect_database(self, config):
        return False, "Not implemented"
        
    def disconnect(self):
        pass
        
    def cleanup(self):
        pass
        
    def load_excel_file(self, file_path):
        return False, {"error": "Not implemented"}
        
    def get_tables(self):
        return []
        
    def get_table_schema(self, table_name):
        return []
        
    def auto_map_fields(self, table_name):
        return {}
        
    def get_import_preview(self, limit=5):
        return []
        
    def import_data(self, table_name, options):
        return False
        
    def get_connection_stats(self):
        return {}
'''
            )

    # Create basic main_window if missing
    main_window_path = Path("gui/main_window.py")
    if not main_window_path.exists():
        main_window_path.parent.mkdir(exist_ok=True)
        with open(main_window_path, "w", encoding="utf-8") as f:
            f.write(
                '''"""
Basic Main Window - Minimal Implementation
"""
import tkinter as tk
from tkinter import messagebox

class MainWindow:
    def __init__(self, controller=None, pool_controller=None):
        self.controller = controller
        self.pool_controller = pool_controller
        self.root = tk.Tk()
        self.setup_window()
        
    def setup_window(self):
        self.root.title("DENSO888 - Excel to Database System")
        self.root.geometry("800x600")
        
        label = tk.Label(self.root, text="🏭 DENSO888 System\\nMinimal Implementation\\nCheck console for instructions", 
                        font=("Arial", 14), justify="center")
        label.pack(expand=True)
        
    def run(self):
        print("🚀 DENSO888 System Started")
        print("📋 Available files:")
        for file in ["main.py", "services/connection_pool_service.py"]:
            if Path(file).exists():
                print(f"✅ {file}")
            else:
                print(f"❌ {file}")
        
        self.root.mainloop()
'''
            )


def ensure_basic_structure():
    """Ensure basic project structure exists"""
    dirs = ["controllers", "gui", "services", "core", "logs", "data"]
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)

    # Create __init__.py files
    for dir_name in ["controllers", "gui", "services", "core"]:
        init_file = Path(dir_name) / "__init__.py"
        if not init_file.exists():
            init_file.touch()

    """Check critical dependencies"""
    required = {
        "pandas": "Excel processing",
        "openpyxl": "Excel reading",
        "sqlalchemy": "Database connectivity",
        "tkinter": "GUI framework",
    }

    missing = []
    for package, desc in required.items():
        try:
            if package == "tkinter":
                import tkinter
            else:
                __import__(package)
        except ImportError:
            missing.append(f"{package} ({desc})")

    if missing:
        print("❌ Missing dependencies:")
        for item in missing:
            print(f"   - {item}")
        print("\n💡 Install with: pip install pandas openpyxl sqlalchemy")
        return False
    return True


def main():
    """Main application entry point"""
    try:
        # Setup environment first
        logger = setup_environment()

        # Ensure basic structure
        ensure_basic_structure()

        # Check dependencies
        if not check_dependencies():
            input("Press Enter to exit...")
            sys.exit(1)

        # Import main application (after dependency check)
        try:
            from gui.main_window import MainWindow
            from services.connection_pool_service import ConnectionPoolService
            from controllers.pool_controller import PoolController
            from controllers.app_controller import AppController
        except ImportError as e:
            logger.error(f"Failed to import modules: {e}")
            print("❌ Import failed. Creating missing files...")
            create_missing_files()
            return

        logger.info("✅ Dependencies OK - Initializing System")

        # Initialize services
        pool_service = ConnectionPoolService()
        pool_controller = PoolController(pool_service)

        # Try to create app controller (fallback if not available)
        try:
            app_controller = AppController()
        except Exception as e:
            logger.warning(f"AppController not available: {e}")
            app_controller = None

        # Create and run main window
        app = MainWindow(controller=app_controller, pool_controller=pool_controller)
        logger.info("🚀 Starting DENSO888 System GUI")
        app.run()

    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("🔧 Please check file structure and dependencies")
        input("Press Enter to exit...")
        sys.exit(1)
=======
# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from gui.enhanced_main_window import EnhancedMainWindow
from controllers.pool_controller import PoolController
from services.connection_pool_service import ConnectionPoolService
from utils.logger import setup_logger


def main():
    """เริ่มต้นระบบ Excel to Database Pool"""
    try:
        # Setup logging
        logger = setup_logger("excel_db_pool", "INFO")
        logger.info("🚀 Starting Excel to Database Pool System...")

        # Initialize services
        pool_service = ConnectionPoolService()
        controller = PoolController(pool_service)

        # Create and run main window
        app = EnhancedMainWindow(controller)
        app.run()

    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        import traceback
>>>>>>> 1f635ed4a112b37ae7a89b809261dfeb1fe63138

    except Exception as e:
        logger.error(f"❌ Application Error: {e}")
        print(f"❌ Error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    main()
