import sys
import logging
from pathlib import Path
from typing import Optional
from datetime import datetime

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# Local imports
from config.app_config import AppConfig
from services.ui_service import UIService
from services.connection_pool_service import ConnectionPoolService
from services.excel_service import ExcelService
from services.backup_service import BackupService
from utils.error_handler import ErrorHandler, setup_error_handling
from controllers.app_controller import AppController
from gui.main_window import MainWindow
from services.validation_service import ValidationService
from services.cache_service import CacheService


class Application:
    """Main application class"""

    def __init__(self):
        self.config: Optional[AppConfig] = None
        self.error_handler: Optional[ErrorHandler] = None
        self.ui_service: Optional[UIService] = None
        self.connection_service: Optional[ConnectionPoolService] = None
        self.excel_service: Optional[ExcelService] = None
        self.backup_service: Optional[BackupService] = None
        self.controller: Optional[AppController] = None
        self.main_window: Optional[MainWindow] = None
        self.preferences_service = None
        self.export_service = None
        self.validation_service: Optional[ValidationService] = None
        self.cache_service: Optional[CacheService] = None

    def initialize(self) -> bool:
        """Initialize application and services"""
        try:
            # Setup logging
            self._setup_logging()

            # Load configuration
            self.config = AppConfig.load()

            # Initialize error handling
            self.error_handler = setup_error_handling(self.config)

            # Initialize services
            self.connection_service = ConnectionPoolService(self.config.database)
            self.excel_service = ExcelService(self.config.excel)
            self.backup_service = BackupService(self.config.backup)
            self.ui_service = UIService()

            # Initialize additional services
            from services.preferences_service import PreferencesService
            from services.export_service import ExportService

            self.preferences_service = PreferencesService()
            self.export_service = ExportService()
            self.validation_service = ValidationService(self.config.validation)
            self.cache_service = CacheService()

            # Initialize controller
            self.controller = AppController(
                connection_service=self.connection_service,
                excel_service=self.excel_service,
                backup_service=self.backup_service,
                ui_service=self.ui_service,
                config=self.config,
            )

            # Initialize UI
            self.main_window = MainWindow(self.controller)
            self.ui_service.set_main_window(self.main_window)

            # Update UI service with preferences
            self.ui_service.apply_preferences(self.preferences_service)

            # Apply user preferences
            window_size = self.preferences_service.get("window_size")
            if window_size:
                self.main_window.root.geometry(f"{window_size[0]}x{window_size[1]}")

            # Update controller with new services
            self.controller.set_validation_service(self.validation_service)
            self.controller.set_cache_service(self.cache_service)

            return True

        except Exception as e:
            self._handle_startup_error(e)
            return False

    def _setup_logging(self):
        """Setup application logging"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / f"denso888_{datetime.now().strftime('%Y%m%d')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_file, encoding="utf-8"),
                logging.StreamHandler(),
            ],
        )

    def _handle_startup_error(self, error: Exception):
        """Handle application startup errors"""
        import tkinter.messagebox as msgbox

        error_msg = f"Failed to start application: {str(error)}"
        logging.error(error_msg, exc_info=True)

        msgbox.showerror(
            "Startup Error",
            "Failed to start DENSO888 application.\n\n"
            f"Error: {error_msg}\n\n"
            "Please check the logs for more details.",
        )

    def run(self):
        """Run the application"""
        if self.initialize():
            try:
                # Start backup service
                self.backup_service.start()

                # Start UI
                self.main_window.run()

            except Exception as e:
                logging.error("Runtime error", exc_info=True)
                self.error_handler.handle_error(e)

            finally:
                self.cleanup()

    def cleanup(self):
        """Cleanup application resources"""
        try:
            # Save current window size
            if self.main_window and self.preferences_service:
                geometry = self.main_window.root.geometry()
                width = self.main_window.root.winfo_width()
                height = self.main_window.root.winfo_height()
                self.preferences_service.set("window_size", (width, height))

            if self.backup_service:
                self.backup_service.stop()

            if self.connection_service:
                self.connection_service.cleanup()

            if self.excel_service:
                self.excel_service.cleanup()

            # Clear cache on exit
            if self.cache_service:
                self.cache_service.clear()

            logging.info("Application shutdown complete")

        except Exception as e:
            logging.error(f"Error during cleanup: {e}", exc_info=True)


def main():
    """Application entry point"""
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
