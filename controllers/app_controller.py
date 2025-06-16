"""
controllers/app_controller.py
Main Application Controller - State Management & Coordination
"""

from typing import Dict, Any, Callable, List
from datetime import datetime
import threading

from services.database_service import DatabaseService
from services.excel_service import ExcelService
from services.notification_service import NotificationService


class AppController:
    """Main application controller managing state and coordination"""

    def __init__(self):
        # Services
        self.db_service = DatabaseService()
        self.excel_service = ExcelService()
        self.notification_service = NotificationService()

        # Application state
        self.app_state = {
            "db_connected": False,
            "current_file": None,
            "selected_table": None,
            "import_progress": 0,
            "last_operation": None,
        }

        # Event system
        self.event_listeners: Dict[str, List[Callable]] = {
            "status_changed": [],
            "db_status_changed": [],
            "notification": [],
            "progress_update": [],
            "operation_complete": [],
        }

        # Statistics
        self.stats = {
            "total_imports": 0,
            "total_records": 0,
            "total_tables": 0,
            "mock_generated": 0,
        }

    # ================ EVENT SYSTEM ================
    def subscribe(self, event: str, callback: Callable):
        """Subscribe to events"""
        if event in self.event_listeners:
            self.event_listeners[event].append(callback)

    def emit(self, event: str, data: Any = None):
        """Emit event to all listeners"""
        if event in self.event_listeners:
            for callback in self.event_listeners[event]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"Event callback error: {e}")

    def update_status(self, text: str, type_: str = "info"):
        """Update application status"""
        self.emit("status_changed", {"text": text, "type": type_})

    def show_notification(
        self, message: str, type_: str = "info", duration: int = 3000
    ):
        """Show notification"""
        self.emit(
            "notification", {"message": message, "type": type_, "duration": duration}
        )

    # ================ DATABASE OPERATIONS ================
    def get_database_config(self) -> Dict[str, Any]:
        """Get current database configuration"""
        return self.db_service.get_config()

    def test_database_connection(self, config: Dict[str, Any]) -> tuple[bool, str]:
        """Test database connection"""

        def test_async():
            self.update_status("🔍 Testing database connection...", "info")
            success, message = self.db_service.test_connection(config)

            if success:
                self.update_status("✅ Connection test successful", "success")
                self.show_notification("Database connection test passed!", "success")
            else:
                self.update_status("❌ Connection test failed", "error")
                self.show_notification(f"Connection test failed: {message}", "error")

            return success, message

        # Run in background thread
        threading.Thread(target=test_async, daemon=True).start()
        return True, "Test started"

    def connect_database(self, config: Dict[str, Any]) -> tuple[bool, str]:
        """Connect to database"""

        def connect_async():
            self.update_status("🔗 Connecting to database...", "info")
            success, message = self.db_service.connect(config)

            if success:
                self.app_state["db_connected"] = True
                self.update_status("✅ Database connected", "success")
                self.emit("db_status_changed", True)
                self.show_notification("Successfully connected to database!", "success")

                # Update table count
                tables = self.db_service.get_tables()
                self.stats["total_tables"] = len(tables)

            else:
                self.app_state["db_connected"] = False
                self.update_status("❌ Database connection failed", "error")
                self.emit("db_status_changed", False)
                self.show_notification(f"Connection failed: {message}", "error")

            return success, message

        threading.Thread(target=connect_async, daemon=True).start()
        return True, "Connection started"

    def get_database_tables(self) -> List[str]:
        """Get list of database tables"""
        if not self.app_state["db_connected"]:
            return []
        return self.db_service.get_tables()

    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """Get table information"""
        if not self.app_state["db_connected"]:
            return {"error": "Database not connected"}
        return self.db_service.get_table_info(table_name)

    # ================ EXCEL OPERATIONS ================
    def select_excel_file(self, file_path: str) -> tuple[bool, Dict[str, Any]]:
        """Select and analyze Excel file"""
        try:
            file_info = self.excel_service.analyze_file(file_path)

            if "error" not in file_info:
                self.app_state["current_file"] = file_path
                self.show_notification(
                    f'File selected: {file_info["file_name"]}', "success"
                )
                return True, file_info
            else:
                self.show_notification(f'File error: {file_info["error"]}', "error")
                return False, file_info

        except Exception as e:
            error_msg = f"Failed to analyze file: {str(e)}"
            self.show_notification(error_msg, "error")
            return False, {"error": error_msg}

    def import_excel_data(self, table_name: str, options: Dict[str, Any]) -> bool:
        """Import Excel data to database"""
        if not self.app_state["db_connected"]:
            self.show_notification("Please connect to database first", "error")
            return False

        if not self.app_state["current_file"]:
            self.show_notification("Please select a file first", "error")
            return False

        def import_async():
            try:
                self.update_status("📁 Starting Excel import...", "info")
                self.emit(
                    "progress_update", {"progress": 0, "status": "Initializing..."}
                )

                # Read Excel file
                self.emit(
                    "progress_update",
                    {"progress": 25, "status": "Reading Excel file..."},
                )
                data = self.excel_service.read_file(
                    self.app_state["current_file"], options
                )

                # Create table
                self.emit(
                    "progress_update", {"progress": 50, "status": "Creating table..."}
                )
                success, message = self.db_service.create_table_from_data(
                    table_name, data
                )

                if not success:
                    raise Exception(f"Failed to create table: {message}")

                # Insert data
                self.emit(
                    "progress_update", {"progress": 75, "status": "Inserting data..."}
                )
                success, message = self.db_service.insert_data(table_name, data)

                if not success:
                    raise Exception(f"Failed to insert data: {message}")

                # Complete
                self.emit(
                    "progress_update", {"progress": 100, "status": "Import completed!"}
                )
                self.update_status("✅ Excel import completed", "success")

                # Update statistics
                self.stats["total_imports"] += 1
                self.stats["total_records"] += len(data)
                self.stats["total_tables"] = len(self.db_service.get_tables())

                self.show_notification(
                    f"Successfully imported {len(data):,} rows to {table_name}",
                    "success",
                )

                # Emit completion
                self.emit(
                    "operation_complete",
                    {
                        "operation": "excel_import",
                        "table_name": table_name,
                        "rows": len(data),
                    },
                )

                return True

            except Exception as e:
                error_msg = f"Import failed: {str(e)}"
                self.update_status("❌ Import failed", "error")
                self.show_notification(error_msg, "error")
                self.emit("progress_update", {"progress": 0, "status": "Import failed"})
                return False

        threading.Thread(target=import_async, daemon=True).start()
        return True

    # ================ MOCK DATA OPERATIONS ================
    def get_mock_templates(self) -> List[Dict[str, Any]]:
        """Get available mock data templates"""
        return [
            {
                "id": "employees",
                "title": "👥 Employee Records",
                "description": "Staff information with departments and roles",
                "recommended_count": "1,000 - 10,000",
            },
            {
                "id": "sales",
                "title": "💰 Sales Transactions",
                "description": "Customer orders and revenue data",
                "recommended_count": "5,000 - 50,000",
            },
            {
                "id": "inventory",
                "title": "📦 Inventory Items",
                "description": "Product stock and supplier information",
                "recommended_count": "500 - 5,000",
            },
            {
                "id": "financial",
                "title": "💳 Financial Records",
                "description": "Accounting transactions and budgets",
                "recommended_count": "1,000 - 25,000",
            },
        ]

    def generate_mock_data(
        self, template: str, count: int, table_name: str = None
    ) -> bool:
        """Generate mock data"""
        if not self.app_state["db_connected"]:
            self.show_notification("Please connect to database first", "error")
            return False

        def generate_async():
            try:
                if not table_name:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    table_name = f"mock_{template}_{timestamp}"

                self.update_status(
                    f"🎲 Generating {count:,} {template} records...", "info"
                )
                self.emit(
                    "progress_update", {"progress": 0, "status": "Generating data..."}
                )

                # Generate data
                from ..core.mock_data_generator import MockDataGenerator

                generator = MockDataGenerator()

                self.emit(
                    "progress_update",
                    {"progress": 25, "status": f"Creating {template} data..."},
                )

                if template == "employees":
                    data = generator.generate_employees(count)
                elif template == "sales":
                    data = generator.generate_sales(count)
                elif template == "inventory":
                    data = generator.generate_inventory(count)
                elif template == "financial":
                    data = generator.generate_financial(count)
                else:
                    raise ValueError(f"Unknown template: {template}")

                # Create table
                self.emit(
                    "progress_update",
                    {"progress": 50, "status": "Creating database table..."},
                )
                success, message = self.db_service.create_table_from_data(
                    table_name, data
                )

                if not success:
                    raise Exception(f"Failed to create table: {message}")

                # Insert data
                self.emit(
                    "progress_update",
                    {"progress": 75, "status": "Inserting records..."},
                )
                success, message = self.db_service.insert_data(table_name, data)

                if not success:
                    raise Exception(f"Failed to insert data: {message}")

                # Complete
                self.emit(
                    "progress_update",
                    {"progress": 100, "status": "Generation completed!"},
                )
                self.update_status("✅ Mock data generated", "success")

                # Update statistics
                self.stats["mock_generated"] += count
                self.stats["total_records"] += count
                self.stats["total_tables"] = len(self.db_service.get_tables())

                self.show_notification(
                    f"Generated {count:,} {template} records in table {table_name}",
                    "success",
                )

                # Emit completion
                self.emit(
                    "operation_complete",
                    {
                        "operation": "mock_generation",
                        "template": template,
                        "table_name": table_name,
                        "count": count,
                    },
                )

                return True

            except Exception as e:
                error_msg = f"Mock data generation failed: {str(e)}"
                self.update_status("❌ Generation failed", "error")
                self.show_notification(error_msg, "error")
                self.emit(
                    "progress_update", {"progress": 0, "status": "Generation failed"}
                )
                return False

        threading.Thread(target=generate_async, daemon=True).start()
        return True

    # ================ ANALYTICS OPERATIONS ================
    def export_data(self, table_name: str, format_type: str, file_path: str) -> bool:
        """Export data to file"""
        if not self.app_state["db_connected"]:
            self.show_notification("Please connect to database first", "error")
            return False

        def export_async():
            try:
                self.update_status(
                    f"📊 Exporting {table_name} to {format_type.upper()}...", "info"
                )

                # Get data from database
                data = self.db_service.get_table_data(table_name)

                if not data:
                    raise Exception("No data found in table")

                # Export using excel service
                success = self.excel_service.export_data(data, file_path, format_type)

                if success:
                    self.update_status("✅ Export completed", "success")
                    self.show_notification(f"Data exported to {file_path}", "success")
                else:
                    raise Exception("Export operation failed")

                return True

            except Exception as e:
                error_msg = f"Export failed: {str(e)}"
                self.update_status("❌ Export failed", "error")
                self.show_notification(error_msg, "error")
                return False

        threading.Thread(target=export_async, daemon=True).start()
        return True

    def get_analytics_data(self) -> Dict[str, Any]:
        """Get analytics data"""
        if not self.app_state["db_connected"]:
            return {"error": "Database not connected"}

        try:
            tables = self.db_service.get_tables()
            analytics = {
                "tables": [],
                "total_records": 0,
                "largest_table": "",
                "latest_table": "",
            }

            for table in tables:
                info = self.db_service.get_table_info(table)
                analytics["tables"].append(
                    {
                        "name": table,
                        "rows": info.get("row_count", 0),
                        "columns": info.get("column_count", 0),
                    }
                )
                analytics["total_records"] += info.get("row_count", 0)

            # Find largest table
            if analytics["tables"]:
                largest = max(analytics["tables"], key=lambda x: x["rows"])
                analytics["largest_table"] = largest["name"]

            return analytics

        except Exception as e:
            return {"error": str(e)}

    # ================ STATE MANAGEMENT ================
    def get_app_state(self) -> Dict[str, Any]:
        """Get current application state"""
        return {**self.app_state, "stats": self.stats}

    def get_statistics(self) -> Dict[str, Any]:
        """Get application statistics"""
        return self.stats.copy()

    def reset_state(self):
        """Reset application state"""
        self.app_state = {
            "db_connected": False,
            "current_file": None,
            "selected_table": None,
            "import_progress": 0,
            "last_operation": None,
        }
        self.emit("db_status_changed", False)
        self.update_status("🔄 Application state reset", "info")
