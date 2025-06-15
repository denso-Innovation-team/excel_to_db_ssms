"""
controllers/app_controller.py
Fixed App Controller with Enhanced Error Handling
"""

import logging
import os
from typing import Optional, Dict, Any, Callable
from datetime import datetime

# Import the fixed database manager
from core.database_manager import DatabaseManager
from core.mock_data_generator import MockDataGenerator
from admin.user_tracker import UserActivityTracker

logger = logging.getLogger(__name__)


class AppController:
    """Enhanced Application Controller with real functionality"""

    def __init__(self, config):
        self.config = config
        self.db_config = None
        self.db_manager: Optional[DatabaseManager] = None
        self.mock_generator = MockDataGenerator()
        self.activity_tracker = UserActivityTracker()

        # File handling
        self.current_file: Optional[str] = None
        self.file_info: Optional[Dict[str, Any]] = None
        self.excel_handler = None

        # State management
        self.is_connected = False
        self.connection_status = "disconnected"

        # Event system
        self.event_callbacks: Dict[str, list] = {
            "db_status_changed": [],
            "file_selected": [],
            "progress_update": [],
            "operation_complete": [],
            "error_occurred": [],
            "log_message": [],
            "achievement_unlocked": [],
        }

        # Initialize components
        self._initialize_components()

    def _initialize_components(self):
        """Initialize core components"""
        try:
            # Initialize database config
            from models.database_config import DatabaseConfig
            self.db_config = DatabaseConfig()

            # Initialize Excel handler
            try:
                from core.excel_handler import ExcelHandler
                self.excel_handler = ExcelHandler()
            except ImportError:
                # Fallback to simple Excel processor
                from core.excel_processor import ExcelProcessor
                self.excel_handler = ExcelProcessor()

            self.log("Application controller initialized successfully")

        except Exception as e:
            self.log(f"Failed to initialize some components: {e}", "WARNING")

    def subscribe(self, event: str, callback: Callable):
        """Subscribe to application events"""
        if event in self.event_callbacks:
            self.event_callbacks[event].append(callback)

    def emit_event(self, event: str, data=None):
        """Emit event to all subscribers"""
        if event in self.event_callbacks:
            for callback in self.event_callbacks[event]:
                try:
                    callback(data)
                except Exception as e:
                    logger.error(f"Event callback error: {e}")

    def log(self, message: str, level: str = "INFO"):
        """Log message and emit to UI"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"

        # Print to console
        if level == "ERROR":
            logger.error(formatted_message)
        elif level == "WARNING":
            logger.warning(formatted_message)
        else:
            logger.info(formatted_message)

        # Emit to UI
        self.emit_event(
            "log_message",
            {"message": formatted_message, "level": level, "timestamp": timestamp},
        )

    # Database Operations
    def update_database_config(self, config_data: Dict[str, Any]):
        """Update database configuration"""
        if self.db_config:
            self.db_config.update_from_dict(config_data)
            self.log(f"Database config updated: {self.db_config.db_type}")

            # Track configuration change
            self.activity_tracker.log_activity(
                "database_config_updated", {"db_type": self.db_config.db_type}
            )

    def test_database_connection(self) -> bool:
        """Test database connection"""
        try:
            if not self.db_config:
                self.log("Database configuration not available", "ERROR")
                return False

            self.log("Testing database connection...")

            # Create temporary manager for testing
            test_params = self.db_config.get_connection_params()
            test_manager = DatabaseManager(test_params)
            success, message = test_manager.test_connection()

            if success:
                self.log(f"✅ Database test successful: {message}")
                self.activity_tracker.log_activity(
                    "database_test_success",
                    {"db_type": self.db_config.db_type, "message": message},
                )
                test_manager.close()
                return True
            else:
                self.log(f"❌ Database test failed: {message}", "ERROR")
                self.activity_tracker.log_activity(
                    "database_test_failed",
                    {"db_type": self.db_config.db_type, "error": message},
                )
                return False

        except Exception as e:
            error_msg = f"Database test error: {e}"
            self.log(error_msg, "ERROR")
            return False

    def connect_database(self) -> bool:
        """Connect to database"""
        try:
            if not self.db_config:
                self.log("Database configuration not available", "ERROR")
                return False

            self.log("Connecting to database...")

            # Create database manager
            connection_params = self.db_config.get_connection_params()
            self.db_manager = DatabaseManager(connection_params)
            success, message = self.db_manager.connect()

            if success:
                self.is_connected = True
                self.connection_status = "connected"
                self.log(f"✅ Database connected: {message}")

                # Show database file location for SQLite
                if self.db_config.db_type == "sqlite":
                    db_path = os.path.abspath(self.db_config.sqlite_file)
                    self.log(f"📁 Database file: {db_path}")

                self.emit_event("db_status_changed", True)

                # Track successful connection
                self.activity_tracker.log_activity(
                    "database_connected",
                    {"db_type": self.db_config.db_type, "message": message},
                )

                # Check for achievement
                self._check_connection_achievement()
                return True
            else:
                self.is_connected = False
                self.connection_status = "failed"
                self.log(f"❌ Database connection failed: {message}", "ERROR")
                self.emit_event("db_status_changed", False)
                return False

        except Exception as e:
            self.is_connected = False
            self.connection_status = "error"
            error_msg = f"Database connection error: {e}"
            self.log(error_msg, "ERROR")
            self.emit_event("error_occurred", error_msg)
            return False

    def get_database_status(self) -> Dict[str, Any]:
        """Get current database status with detailed info"""
        status = {
            "connected": self.is_connected,
            "type": self.db_config.db_type if self.db_config else "unknown",
            "status": self.connection_status,
        }

        if self.db_manager and self.is_connected:
            try:
                # Get database statistics
                stats = self.db_manager.get_database_stats()
                status.update(stats)

                # Get recent operations
                recent_ops = self.db_manager.get_recent_operations(5)
                status["recent_operations"] = recent_ops

            except Exception as e:
                self.log(f"Error getting database status: {e}", "WARNING")

        return status

    def get_database_tables(self) -> list:
        """Get list of database tables"""
        if not self.db_manager or not self.is_connected:
            return []

        try:
            return self.db_manager.get_tables()
        except Exception as e:
            self.log(f"Error getting tables: {e}", "ERROR")
            return []

    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """Get detailed table information"""
        if not self.db_manager or not self.is_connected:
            return {"error": "Database not connected"}

        try:
            return self.db_manager.get_table_info(table_name)
        except Exception as e:
            self.log(f"Error getting table info: {e}", "ERROR")
            return {"error": str(e)}

    # File Operations
    def select_file(self, file_path: str) -> bool:
        """Select and analyze file"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            self.current_file = file_path
            file_name = os.path.basename(file_path)
            self.log(f"📁 File selected: {file_name}")

            # Analyze file
            if self.excel_handler:
                if hasattr(self.excel_handler, "load_file"):
                    # Enhanced Excel handler
                    self.file_info = self.excel_handler.load_file(file_path)
                else:
                    # Simple Excel processor
                    self.file_info = self.excel_handler.get_file_info(file_path)
            else:
                # Fallback file info
                self.file_info = self._get_basic_file_info(file_path)

            if "error" not in self.file_info:
                self.log(
                    f"📊 File analyzed: {self.file_info.get('total_rows', 0)} rows, "
                    f"{self.file_info.get('total_columns', 0)} columns"
                )

                self.emit_event("file_selected", self.file_info)

                # Track file selection
                self.activity_tracker.log_activity(
                    "file_selected",
                    {
                        "file_path": file_path,
                        "file_size": os.path.getsize(file_path),
                        "rows": self.file_info.get("total_rows", 0),
                        "columns": self.file_info.get("total_columns", 0),
                    },
                )
                return True
            else:
                self.log(f"❌ File analysis failed: {self.file_info['error']}", "ERROR")
                return False

        except Exception as e:
            error_msg = f"File selection failed: {str(e)}"
            self.log(error_msg, "ERROR")
            self.emit_event("error_occurred", error_msg)
            return False

    def _get_basic_file_info(self, file_path: str) -> Dict[str, Any]:
        """Get basic file information as fallback"""
        try:
            import pandas as pd

            # Try to read file
            if file_path.lower().endswith((".xlsx", ".xls")):
                df = pd.read_excel(file_path, nrows=5)  # Read sample
                total_df = pd.read_excel(file_path)  # Get row count

                return {
                    "file_name": os.path.basename(file_path),
                    "file_path": file_path,
                    "file_size_mb": os.path.getsize(file_path) / (1024 * 1024),
                    "total_rows": len(total_df),
                    "total_columns": len(df.columns),
                    "columns": list(df.columns),
                    "sample_data": df.head(5),
                    "modified_date": datetime.fromtimestamp(os.path.getmtime(file_path)),
                }
            else:
                return {"error": "Unsupported file format"}

        except Exception as e:
            return {"error": str(e)}

    def get_file_info(self) -> Optional[Dict[str, Any]]:
        """Get current file information"""
        return self.file_info

    def import_excel_data(self, table_name: str, options: Dict[str, Any]) -> bool:
        """Import Excel data to database"""
        if not self.is_connected:
            self.emit_event("error_occurred", "Database not connected")
            return False

        if not self.current_file:
            self.emit_event("error_occurred", "No file selected")
            return False

        try:
            self.log(f"🚀 Starting import to table '{table_name}'")

            # Emit progress start
            self.emit_event(
                "progress_update",
                {
                    "progress": 0,
                    "status": "Starting import...",
                    "details": f"File: {os.path.basename(self.current_file)}",
                },
            )

            # Read Excel file
            import pandas as pd
            df = pd.read_excel(self.current_file)

            # Convert to list of dictionaries
            data = df.to_dict("records")

            self.emit_event(
                "progress_update",
                {
                    "progress": 25,
                    "status": "Data loaded, creating table...",
                    "details": f"Processing {len(data)} rows",
                },
            )

            # Create table
            success, message = self.db_manager.create_table_from_data(table_name, data)
            if not success:
                raise Exception(f"Failed to create table: {message}")

            self.emit_event(
                "progress_update",
                {
                    "progress": 50,
                    "status": "Table created, inserting data...",
                    "details": f"Table: {table_name}",
                },
            )

            # Insert data
            success, message = self.db_manager.insert_data(table_name, data)
            if not success:
                raise Exception(f"Failed to insert data: {message}")

            self.emit_event(
                "progress_update",
                {
                    "progress": 100,
                    "status": "Import completed successfully!",
                    "details": message,
                },
            )

            self.log(f"✅ Import completed: {message}")

            # Track successful import
            self.activity_tracker.log_activity(
                "excel_import_completed",
                {
                    "table_name": table_name,
                    "file_path": self.current_file,
                    "rows_imported": len(data),
                    "options": options,
                },
            )

            # Emit completion event
            self.emit_event(
                "operation_complete",
                {
                    "operation": "excel_import",
                    "success": True,
                    "data": {
                        "table_name": table_name,
                        "rows_imported": len(data),
                        "file_name": os.path.basename(self.current_file),
                    },
                },
            )

            # Check for achievements
            self._check_import_achievement(len(data))
            return True

        except Exception as e:
            error_msg = f"Excel import failed: {str(e)}"
            self.log(error_msg, "ERROR")

            self.emit_event(
                "progress_update",
                {"progress": 0, "status": "Import failed!", "details": error_msg},
            )

            self.emit_event("error_occurred", error_msg)
            return False

    # Mock Data Operations
    def generate_mock_data(self, template: str, count: int, table_name: str = None) -> bool:
        """Generate mock data with progress tracking"""
        if not self.is_connected:
            self.emit_event("error_occurred", "Database not connected")
            return False

        try:
            if not table_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                table_name = f"mock_{template}_{timestamp}"

            self.log(f"🎲 Generating {count:,} rows of {template} data")

            # Emit progress start
            self.emit_event(
                "progress_update",
                {
                    "progress": 0,
                    "status": "Initializing mock data generator...",
                    "details": f"Template: {template}",
                },
            )

            # Generate data based on template
            self.emit_event(
                "progress_update",
                {
                    "progress": 20,
                    "status": f"Generating {template} data...",
                    "details": f"Creating {count:,} records",
                },
            )

            if template == "employees":
                data = self.mock_generator.generate_employees(count)
            elif template == "sales":
                data = self.mock_generator.generate_sales(count)
            elif template == "inventory":
                data = self.mock_generator.generate_inventory(count)
            elif template == "financial":
                data = self.mock_generator.generate_financial(count)
            else:
                raise ValueError(f"Unknown template: {template}")

            self.emit_event(
                "progress_update",
                {
                    "progress": 50,
                    "status": "Creating database table...",
                    "details": f"Table: {table_name}",
                },
            )

            # Create table and insert data
            success, message = self.db_manager.create_table_from_data(table_name, data)
            if not success:
                raise Exception(f"Failed to create table: {message}")

            self.emit_event(
                "progress_update",
                {
                    "progress": 75,
                    "status": "Inserting mock data...",
                    "details": f"Processing {len(data)} records",
                },
            )

            success, message = self.db_manager.insert_data(table_name, data)
            if not success:
                raise Exception(f"Failed to insert data: {message}")

            self.emit_event(
                "progress_update",
                {
                    "progress": 100,
                    "status": "Mock data generation completed!",
                    "details": message,
                },
            )

            self.log(f"✅ Successfully generated {count:,} {template} records")

            # Show database file location for SQLite
            if self.db_config.db_type == "sqlite":
                db_path = os.path.abspath(self.db_config.sqlite_file)
                self.log(f"📁 Data saved to: {db_path}")

            # Track successful generation
            self.activity_tracker.log_activity(
                "mock_data_generated",
                {"template": template, "count": count, "table_name": table_name},
            )

            # Emit completion event
            self.emit_event(
                "operation_complete",
                {
                    "operation": "mock_generation",
                    "success": True,
                    "data": {
                        "table_name": table_name,
                        "rows_generated": count,
                        "template": template,
                        "database_file": (
                            self.db_manager.db_file_path
                            if self.db_config.db_type == "sqlite"
                            else None
                        ),
                    },
                },
            )

            # Check for achievements
            self._check_mock_data_achievement(count, template)
            return True

        except Exception as e:
            error_msg = f"Mock data generation failed: {str(e)}"
            self.log(error_msg, "ERROR")

            self.emit_event(
                "progress_update",
                {"progress": 0, "status": "Generation failed!", "details": error_msg},
            )

            self.emit_event("error_occurred", error_msg)
            return False

    def get_available_templates(self) -> list:
        """Get available mock data templates"""
        return self.mock_generator.get_available_templates()

    # Achievement System
    def _check_connection_achievement(self):
        """Check for database connection achievement"""
        self.emit_event(
            "achievement_unlocked",
            {
                "title": "Database Master",
                "description": "Successfully connected to database!",
                "type": "bronze",
                "icon": "🗄️",
            },
        )

    def _check_import_achievement(self, row_count: int):
        """Check for import achievements"""
        if row_count >= 10000:
            self.emit_event(
                "achievement_unlocked",
                {
                    "title": "Data Titan",
                    "description": f"Imported {row_count:,} rows in one operation!",
                    "type": "gold",
                    "icon": "📊",
                },
            )
        elif row_count >= 1000:
            self.emit_event(
                "achievement_unlocked",
                {
                    "title": "Data Warrior",
                    "description": f"Imported {row_count:,} rows successfully!",
                    "type": "silver",
                    "icon": "📈",
                },
            )

    def _check_mock_data_achievement(self, count: int, template: str):
        """Check for mock data achievements"""
        if count >= 50000:
            self.emit_event(
                "achievement_unlocked",
                {
                    "title": "Mock Data Legend",
                    "description": f"Generated {count:,} {template} records!",
                    "type": "gold",
                    "icon": "🎲",
                },
            )
        elif count >= 10000:
            self.emit_event(
                "achievement_unlocked",
                {
                    "title": "Data Generator",
                    "description": f"Generated {count:,} {template} records!",
                    "type": "silver",
                    "icon": "🎯",
                },
            )

    # Utility Methods
    def get_recent_logs(self, limit: int = 100) -> list:
        """Get recent application logs"""
        try:
            logs = [
                {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "level": "INFO",
                    "message": "Application started successfully",
                    "module": "System",
                },
                {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "level": "INFO",
                    "message": f"Database connection: {self.connection_status}",
                    "module": "Database",
                },
            ]

            # Add database operations if available
            if self.db_manager:
                try:
                    recent_ops = self.db_manager.get_recent_operations(10)
                    for op in recent_ops:
                        logs.append(
                            {
                                "timestamp": op["created_date"],
                                "level": "INFO",
                                "message": f"{op['operation_type']} on table '{op['table_name']}' - {op['record_count']} records",
                                "module": "Database",
                            }
                        )
                except Exception:
                    pass

            return logs[-limit:]

        except Exception as e:
            self.log(f"Error getting recent logs: {e}", "ERROR")
            return []

    def execute_custom_query(self, query: str) -> tuple:
        """Execute custom SQL query"""
        if not self.db_manager or not self.is_connected:
            return False, "Database not connected"

        try:
            self.log(f"🔍 Executing custom query")
            success, result = self.db_manager.execute_query(query)

            if success:
                self.log(f"✅ Query executed successfully")
                self.activity_tracker.log_activity(
                    "custom_query_executed",
                    {
                        "query_preview": (
                            query[:100] + "..." if len(query) > 100 else query
                        )
                    },
                )
            else:
                self.log(f"❌ Query failed: {result}", "ERROR")

            return success, result

        except Exception as e:
            error_msg = f"Query execution error: {str(e)}"
            self.log(error_msg, "ERROR")
            return False, error_msg

    def backup_database(self, backup_path: str = None) -> bool:
        """Create database backup"""
        if not self.db_manager or not self.is_connected:
            self.emit_event("error_occurred", "Database not connected")
            return False

        try:
            if not backup_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = f"backups/denso888_backup_{timestamp}.db"

            # Ensure backup directory exists
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)

            success, message = self.db_manager.backup_database(backup_path)

            if success:
                self.log(f"✅ Database backup created: {backup_path}")
                self.activity_tracker.log_activity(
                    "database_backup_created", {"backup_path": backup_path}
                )
                return True
            else:
                self.log(f"❌ Backup failed: {message}", "ERROR")
                return False

        except Exception as e:
            error_msg = f"Backup error: {str(e)}"
            self.log(error_msg, "ERROR")
            return False

    def get_application_stats(self) -> Dict[str, Any]:
        """Get comprehensive application statistics"""
        stats = {
            "database": self.get_database_status(),
            "files": {"current_file": self.current_file, "file_info": self.file_info},
            "operations": {"total_operations": 0, "recent_operations": []},
        }

        # Add user activity stats
        try:
            activities = self.activity_tracker.get_activities(1000)
            stats["user_activity"] = {
                "total_activities": len(activities),
                "ip_summary": self.activity_tracker.get_ip_summary(),
            }
        except Exception:
            pass

        return stats

    def shutdown(self):
        """Cleanup resources on shutdown"""
        try:
            self.log("🔄 Shutting down application...")

            # Close database connection
            if self.db_manager:
                self.db_manager.close()
                self.log("✅ Database connection closed")

            # Log shutdown
            self.activity_tracker.log_activity("application_shutdown")

            self.log("✅ Application controller shutdown complete")

        except Exception as e:
            logger.error(f"Error during shutdown: {e}")

    def get_database_file_path(self) -> Optional[str]:
        """Get current database file path (for SQLite)"""
        if self.db_config and self.db_config.db_type == "sqlite":
            return os.path.abspath(self.db_config.sqlite_file)
        return None