"""
controllers/app_controller.py
Main Application Controller
"""

import threading
from typing import Optional, Dict, Any, Callable
from pathlib import Path

from models.app_config import AppConfig
from models.database_config import DatabaseConfig


# Mock classes for core components (since we don't have them yet)
class MockDatabaseManager:
    def __init__(self, config):
        self.config = config

    def connect(self):
        return True

    def get_status(self):
        return {"type": self.config.db_type, "connected": True}

    def close(self):
        pass


class MockExcelHandler:
    def load_file(self, file_path):
        return {"file_path": file_path, "total_rows": 1000}


class MockDataTemplates:
    @staticmethod
    def get_template_list():
        return [
            {"name": "employees", "description": "Employee records"},
            {"name": "sales", "description": "Sales transactions"},
            {"name": "inventory", "description": "Product inventory"},
            {"name": "financial", "description": "Financial transactions"},
        ]


class AppController:
    """Main application controller"""

    def __init__(self, config: AppConfig):
        self.config = config
        self.db_config = DatabaseConfig()

        # Core components (using mocks for now)
        self.db_manager: Optional[MockDatabaseManager] = None
        self.excel_handler = MockExcelHandler()

        # State management
        self.current_file: Optional[str] = None
        self.is_connected = False

        # Event system
        self.event_callbacks: Dict[str, list] = {
            "db_status_changed": [],
            "file_selected": [],
            "progress_update": [],
            "operation_complete": [],
            "error_occurred": [],
            "log_message": [],
        }

        self.cancel_flag = threading.Event()

    def subscribe(self, event: str, callback: Callable):
        """Subscribe to application events"""
        if event in self.event_callbacks:
            self.event_callbacks[event].append(callback)

    def emit_event(self, event: str, data: Any = None):
        """Emit event to all subscribers"""
        if event in self.event_callbacks:
            for callback in self.event_callbacks[event]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"Event callback error: {e}")

    def log(self, message: str, level: str = "INFO"):
        """Log message and emit to UI"""
        print(f"[{level}] {message}")
        self.emit_event("log_message", {"message": message, "level": level})

    # Database Operations
    def update_database_config(self, config_data: Dict[str, Any]):
        """Update database configuration"""
        self.db_config.update_from_dict(config_data)
        self.log(f"Database config updated: {self.db_config.db_type}")

    def connect_database(self) -> bool:
        """Connect to database"""
        try:
            self.db_manager = MockDatabaseManager(self.db_config)
            if self.db_manager.connect():
                self.is_connected = True
                self.log("✅ Database connected successfully")
                self.emit_event("db_status_changed", True)
                return True
            else:
                self.is_connected = False
                self.log("❌ Database connection failed")
                self.emit_event("db_status_changed", False)
                return False
        except Exception as e:
            self.is_connected = False
            error_msg = f"Database connection error: {str(e)}"
            self.log(error_msg, "ERROR")
            self.emit_event("error_occurred", error_msg)
            return False

    def test_database_connection(self) -> bool:
        """Test database connection"""
        try:
            test_manager = MockDatabaseManager(self.db_config)
            result = test_manager.connect()
            if result:
                self.db_manager = test_manager
                self.is_connected = True
                self.emit_event("db_status_changed", True)
            return result
        except Exception as e:
            self.log(f"Connection test failed: {str(e)}", "ERROR")
            return False

    def get_database_status(self) -> Dict[str, Any]:
        """Get current database status"""
        if not self.db_manager:
            return {"connected": False, "type": self.db_config.db_type}

        try:
            status = self.db_manager.get_status()
            status["connected"] = self.is_connected
            return status
        except Exception:
            return {"connected": False, "type": self.db_config.db_type}

    # File Operations
    def select_file(self, file_path: str) -> bool:
        """Select and analyze Excel file"""
        try:
            if not Path(file_path).exists():
                raise FileNotFoundError(f"File not found: {file_path}")

            self.current_file = file_path
            self.log(f"📁 File selected: {Path(file_path).name}")

            # Mock file info
            file_info = {
                "file_path": file_path,
                "file_name": Path(file_path).name,
                "file_size_mb": Path(file_path).stat().st_size / (1024 * 1024),
                "total_rows": 1000,
                "total_columns": 10,
            }

            self.emit_event("file_selected", file_info)
            return True

        except Exception as e:
            error_msg = f"File selection failed: {str(e)}"
            self.log(error_msg, "ERROR")
            self.emit_event("error_occurred", error_msg)
            return False

    def get_file_info(self) -> Optional[Dict[str, Any]]:
        """Get current file information"""
        if self.current_file:
            return {
                "file_path": self.current_file,
                "file_name": Path(self.current_file).name,
            }
        return None

    # Mock Data Operations
    def generate_mock_data(
        self, template_name: str, num_rows: int, table_name: str = None
    ) -> bool:
        """Generate mock data"""
        if not self.is_connected:
            self.emit_event("error_occurred", "Database not connected")
            return False

        try:
            self.log(f"🎲 Generating {num_rows:,} rows of {template_name} data")

            # Mock progress updates
            self.emit_event(
                "progress_update",
                {
                    "progress": 50,
                    "status": "Generating data...",
                    "details": f"Template: {template_name}",
                },
            )

            # Mock completion
            self.emit_event(
                "operation_complete",
                {
                    "operation": "mock_generation",
                    "success": True,
                    "data": {
                        "table_name": table_name or f"mock_{template_name}",
                        "rows_generated": num_rows,
                        "template": template_name,
                    },
                },
            )

            return True
        except Exception as e:
            error_msg = f"Mock data generation failed: {str(e)}"
            self.log(error_msg, "ERROR")
            self.emit_event("error_occurred", error_msg)
            return False

    def get_available_templates(self) -> list:
        """Get available mock data templates"""
        return MockDataTemplates.get_template_list()

    def shutdown(self):
        """Cleanup resources"""
        if self.db_manager:
            try:
                self.db_manager.close()
            except Exception:
                pass
        self.log("Application controller shutdown complete")
