"""
controllers/app_controller.py
FIXED: Real Working Application Controller
"""

from typing import Dict, Any, Callable, List
from datetime import datetime
import threading
import queue
import logging

# Import working services
from services.database_service import DatabaseService
from services.excel_service import ExcelService
from services.notification_service import NotificationService

logger = logging.getLogger(__name__)


class AppController:
    """FIXED: Functional Application Controller with Real State Management"""

    def __init__(self):
        # Initialize services with error handling
        try:
            self.db_service = DatabaseService()
            self.excel_service = ExcelService()
            self.notification_service = NotificationService()
        except Exception as e:
            logger.error(f"Service initialization failed: {e}")
            # Create fallback services
            self.db_service = None
            self.excel_service = None
            self.notification_service = None

        # Real application state
        self.app_state = {
            "db_connected": False,
            "current_file": None,
            "selected_table": None,
            "import_progress": 0,
            "last_operation": None,
            "operation_status": "ready",
        }

        # Working event system
        self.event_listeners: Dict[str, List[Callable]] = {
            "status_changed": [],
            "db_status_changed": [],
            "notification": [],
            "progress_update": [],
            "operation_complete": [],
        }

        # Real statistics
        self.stats = {
            "total_imports": 0,
            "total_records": 0,
            "total_tables": 0,
            "mock_generated": 0,
            "session_start": datetime.now(),
        }

        # Event queue for async processing
        self.event_queue = queue.Queue()
        self.is_running = True

        # Start event processor
        self._start_event_processor()

    def _start_event_processor(self):
        """Start background event processor"""

        def process_events():
            while self.is_running:
                try:
                    event = self.event_queue.get(timeout=1)
                    self._process_event(event)
                except queue.Empty:
                    continue
                except Exception as e:
                    logger.error(f"Event processing error: {e}")

        thread = threading.Thread(target=process_events, daemon=True)
        thread.start()

    def _process_event(self, event: Dict[str, Any]):
        """Process queued events"""
        event_type = event.get("type")
        data = event.get("data")

        if event_type in self.event_listeners:
            for callback in self.event_listeners[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    logger.error(f"Event callback error: {e}")

    # ================ WORKING EVENT SYSTEM ================
    def subscribe(self, event: str, callback: Callable):
        """Subscribe to events with validation"""
        if event not in self.event_listeners:
            self.event_listeners[event] = []

        if callback not in self.event_listeners[event]:
            self.event_listeners[event].append(callback)
            logger.debug(f"Subscribed to {event}")

    def emit(self, event: str, data: Any = None):
        """Emit event to queue for processing"""
        try:
            self.event_queue.put(
                {"type": event, "data": data, "timestamp": datetime.now()}
            )
        except Exception as e:
            logger.error(f"Event emission failed: {e}")

    def update_status(self, text: str, type_: str = "info"):
        """Update application status with real state"""
        self.app_state["last_operation"] = text
        self.app_state["operation_status"] = type_

        self.emit(
            "status_changed",
            {"text": text, "type": type_, "timestamp": datetime.now().isoformat()},
        )

    def show_notification(
        self, message: str, type_: str = "info", duration: int = 3000
    ):
        """Show notification with fallback"""
        self.emit(
            "notification", {"message": message, "type": type_, "duration": duration}
        )

    # ================ REAL DATABASE OPERATIONS ================
    def get_database_config(self) -> Dict[str, Any]:
        """Get working database configuration"""
        if self.db_service:
            return self.db_service.get_config()
        return {"type": "sqlite", "file": "denso888_data.db"}

    def test_database_connection(self, config: Dict[str, Any]) -> tuple[bool, str]:
        """Test database connection with real validation"""
        if not self.db_service:
            return False, "Database service not available"

        def test_async():
            try:
                self.update_status("🔍 Testing database connection...", "info")
                success, message = self.db_service.test_connection(config)

                if success:
                    self.update_status("✅ Connection test successful", "success")
                    self.show_notification(
                        "Database connection test passed!", "success"
                    )
                else:
                    self.update_status("❌ Connection test failed", "error")
                    self.show_notification(f"Connection failed: {message}", "error")

                return success, message
            except Exception as e:
                error_msg = f"Connection test error: {str(e)}"
                self.update_status("❌ Connection test error", "error")
                self.show_notification(error_msg, "error")
                return False, error_msg

        # Run async for UI responsiveness
        threading.Thread(target=test_async, daemon=True).start()
        return True, "Test started"

    def connect_database(self, config: Dict[str, Any]) -> tuple[bool, str]:
        """Connect to database with real state updates"""
        if not self.db_service:
            return False, "Database service not available"

        def connect_async():
            try:
                self.update_status("🔗 Connecting to database...", "info")
                success, message = self.db_service.connect(config)

                if success:
                    self.app_state["db_connected"] = True
                    self.update_status("✅ Database connected", "success")
                    self.emit("db_status_changed", True)
                    self.show_notification(
                        "Successfully connected to database!", "success"
                    )

                    # Update real statistics
                    tables = self.get_database_tables()
                    self.stats["total_tables"] = len(tables)

                    # Get total records across all tables
                    total_records = 0
                    for table in tables:
                        try:
                            info = self.get_table_info(table)
                            total_records += info.get("row_count", 0)
                        except:
                            pass
                    self.stats["total_records"] = total_records

                else:
                    self.app_state["db_connected"] = False
                    self.update_status("❌ Database connection failed", "error")
                    self.emit("db_status_changed", False)
                    self.show_notification(f"Connection failed: {message}", "error")

                return success, message
            except Exception as e:
                error_msg = f"Connection error: {str(e)}"
                self.app_state["db_connected"] = False
                self.update_status("❌ Connection error", "error")
                self.emit("db_status_changed", False)
                self.show_notification(error_msg, "error")
                return False, error_msg

        threading.Thread(target=connect_async, daemon=True).start()
        return True, "Connection started"

    def get_database_tables(self) -> List[str]:
        """Get real database tables"""
        if not self.app_state["db_connected"] or not self.db_service:
            return []

        try:
            return self.db_service.get_tables()
        except Exception as e:
            logger.error(f"Error getting tables: {e}")
            return []

    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """Get real table information"""
        if not self.app_state["db_connected"] or not self.db_service:
            return {"error": "Database not connected"}

        try:
            return self.db_service.get_table_info(table_name)
        except Exception as e:
            logger.error(f"Error getting table info: {e}")
            return {"error": str(e)}

    # ================ WORKING EXCEL OPERATIONS ================
    def select_excel_file(self, file_path: str) -> tuple[bool, Dict[str, Any]]:
        """Select and analyze Excel file with real validation"""
        if not self.excel_service:
            return False, {"error": "Excel service not available"}

        try:
            file_info = self.excel_service.analyze_file(file_path)

            if "error" not in file_info:
                self.app_state["current_file"] = file_path
                self.show_notification(
                    f'File selected: {file_info.get("file_name", "Unknown")}', "success"
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
        """Import Excel data with real progress tracking"""
        if not self.app_state["db_connected"]:
            self.show_notification("Please connect to database first", "error")
            return False

        if not self.app_state["current_file"]:
            self.show_notification("Please select a file first", "error")
            return False

        if not self.excel_service or not self.db_service:
            self.show_notification("Required services not available", "error")
            return False

        def import_async():
            try:
                self.update_status("📁 Starting Excel import...", "info")
                self.emit(
                    "progress_update", {"progress": 0, "status": "Initializing..."}
                )

                # Read Excel file with progress
                self.emit(
                    "progress_update",
                    {"progress": 25, "status": "Reading Excel file..."},
                )
                data = self.excel_service.read_file(
                    self.app_state["current_file"], options
                )

                if not data:
                    raise Exception("No data found in Excel file")

                # Create table with progress
                self.emit(
                    "progress_update", {"progress": 50, "status": "Creating table..."}
                )
                success, message = self.db_service.create_table_from_data(
                    table_name, data
                )

                if not success:
                    raise Exception(f"Failed to create table: {message}")

                # Insert data with progress
                self.emit(
                    "progress_update", {"progress": 75, "status": "Inserting data..."}
                )
                success, message = self.db_service.insert_data(table_name, data)

                if not success:
                    raise Exception(f"Failed to insert data: {message}")

                # Complete with real statistics update
                self.emit(
                    "progress_update", {"progress": 100, "status": "Import completed!"}
                )
                self.update_status("✅ Excel import completed", "success")

                # Update real statistics
                self.stats["total_imports"] += 1
                self.stats["total_records"] += len(data)

                # Refresh table count
                tables = self.get_database_tables()
                self.stats["total_tables"] = len(tables)

                self.show_notification(
                    f"Successfully imported {len(data):,} rows to {table_name}",
                    "success",
                )

                # Emit completion with real data
                self.emit(
                    "operation_complete",
                    {
                        "operation": "excel_import",
                        "table_name": table_name,
                        "rows": len(data),
                        "timestamp": datetime.now().isoformat(),
                    },
                )

                return True

            except Exception as e:
                error_msg = f"Import failed: {str(e)}"
                self.update_status("❌ Import failed", "error")
                self.show_notification(error_msg, "error")
                self.emit("progress_update", {"progress": 0, "status": "Import failed"})
                logger.error(f"Import error: {e}")
                return False

        threading.Thread(target=import_async, daemon=True).start()
        return True

    # ================ WORKING MOCK DATA OPERATIONS ================
    def get_mock_templates(self) -> List[Dict[str, Any]]:
        """Get working mock data templates"""
        return [
            {
                "id": "employees",
                "title": "👥 Employee Records",
                "description": "Staff information with Thai/English names, departments, and salaries",
                "recommended_count": "1,000 - 10,000",
                "fields": [
                    "ID",
                    "Name",
                    "Email",
                    "Department",
                    "Position",
                    "Salary",
                    "Hire Date",
                    "Status",
                ],
                "color": "#3B82F6",
            },
            {
                "id": "sales",
                "title": "💰 Sales Transactions",
                "description": "Customer orders with seasonal patterns and automotive parts focus",
                "recommended_count": "5,000 - 50,000",
                "fields": [
                    "Transaction ID",
                    "Customer",
                    "Product",
                    "Quantity",
                    "Price",
                    "Total",
                    "Date",
                ],
                "color": "#10B981",
            },
            {
                "id": "inventory",
                "title": "📦 Inventory Items",
                "description": "Automotive parts inventory with suppliers and stock levels",
                "recommended_count": "500 - 5,000",
                "fields": [
                    "Product ID",
                    "Name",
                    "Category",
                    "Stock",
                    "Price",
                    "Supplier",
                    "Location",
                ],
                "color": "#F59E0B",
            },
            {
                "id": "financial",
                "title": "💳 Financial Records",
                "description": "Accounting transactions with approval workflows and fiscal reporting",
                "recommended_count": "1,000 - 25,000",
                "fields": [
                    "Account",
                    "Transaction",
                    "Amount",
                    "Type",
                    "Date",
                    "Reference",
                    "Balance",
                ],
                "color": "#8B5CF6",
            },
        ]

    def generate_mock_data(
        self, template: str, count: int, table_name: str = None
    ) -> bool:
        """Generate mock data with real database integration"""
        if not self.app_state["db_connected"]:
            self.show_notification("Please connect to database first", "error")
            return False

        if not self.db_service:
            self.show_notification("Database service not available", "error")
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

                # Import and use real mock data generator
                from core.mock_data_generator import MockDataGenerator

                generator = MockDataGenerator()

                self.emit(
                    "progress_update",
                    {"progress": 25, "status": f"Creating {template} data..."},
                )

                # Generate real data based on template
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

                if not data:
                    raise Exception("Failed to generate data")

                # Create table with real data
                self.emit(
                    "progress_update",
                    {"progress": 50, "status": "Creating database table..."},
                )
                success, message = self.db_service.create_table_from_data(
                    table_name, data
                )

                if not success:
                    raise Exception(f"Failed to create table: {message}")

                # Insert real data
                self.emit(
                    "progress_update",
                    {"progress": 75, "status": "Inserting records..."},
                )
                success, message = self.db_service.insert_data(table_name, data)

                if not success:
                    raise Exception(f"Failed to insert data: {message}")

                # Complete with real statistics
                self.emit(
                    "progress_update",
                    {"progress": 100, "status": "Generation completed!"},
                )
                self.update_status("✅ Mock data generated", "success")

                # Update real statistics
                self.stats["mock_generated"] += count
                self.stats["total_records"] += count

                # Refresh table count
                tables = self.get_database_tables()
                self.stats["total_tables"] = len(tables)

                self.show_notification(
                    f"Generated {count:,} {template} records in table {table_name}",
                    "success",
                )

                # Emit completion with real data
                self.emit(
                    "operation_complete",
                    {
                        "operation": "mock_generation",
                        "template": template,
                        "table_name": table_name,
                        "count": count,
                        "timestamp": datetime.now().isoformat(),
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
                logger.error(f"Mock generation error: {e}")
                return False

        threading.Thread(target=generate_async, daemon=True).start()
        return True

    # ================ WORKING ANALYTICS OPERATIONS ================
    def export_data(self, table_name: str, format_type: str, file_path: str) -> bool:
        """Export data with real file generation"""
        if not self.app_state["db_connected"] or not self.db_service:
            self.show_notification("Please connect to database first", "error")
            return False

        if not self.excel_service:
            self.show_notification("Excel service not available", "error")
            return False

        def export_async():
            try:
                self.update_status(
                    f"📊 Exporting {table_name} to {format_type.upper()}...", "info"
                )

                # Get real data from database
                data = self.db_service.get_table_data(table_name)

                if not data:
                    raise Exception("No data found in table")

                # Export using real excel service
                success = self.excel_service.export_data(data, file_path, format_type)

                if success:
                    self.update_status("✅ Export completed", "success")
                    self.show_notification(f"Data exported to {file_path}", "success")
                    return True
                else:
                    raise Exception("Export operation failed")

            except Exception as e:
                error_msg = f"Export failed: {str(e)}"
                self.update_status("❌ Export failed", "error")
                self.show_notification(error_msg, "error")
                logger.error(f"Export error: {e}")
                return False

        threading.Thread(target=export_async, daemon=True).start()
        return True

    def get_analytics_data(self) -> Dict[str, Any]:
        """Get real analytics data from database"""
        if not self.app_state["db_connected"] or not self.db_service:
            return {"error": "Database not connected"}

        try:
            tables = self.get_database_tables()
            analytics = {
                "tables": [],
                "total_records": 0,
                "largest_table": "",
                "latest_table": "",
                "database_stats": {},
            }

            for table in tables:
                try:
                    info = self.get_table_info(table)
                    row_count = info.get("row_count", 0)

                    analytics["tables"].append(
                        {
                            "name": table,
                            "rows": row_count,
                            "columns": info.get("column_count", 0),
                        }
                    )
                    analytics["total_records"] += row_count
                except Exception as e:
                    logger.error(f"Error getting info for table {table}: {e}")

            # Find largest table
            if analytics["tables"]:
                largest = max(analytics["tables"], key=lambda x: x["rows"])
                analytics["largest_table"] = largest["name"]

            # Get database statistics
            try:
                analytics["database_stats"] = self.db_service.get_database_stats()
            except Exception as e:
                logger.error(f"Error getting database stats: {e}")

            return analytics

        except Exception as e:
            logger.error(f"Analytics error: {e}")
            return {"error": str(e)}

    # ================ REAL STATE MANAGEMENT ================
    def get_app_state(self) -> Dict[str, Any]:
        """Get current real application state"""
        return {
            **self.app_state,
            "stats": self.stats,
            "uptime": str(datetime.now() - self.stats["session_start"]),
            "services_status": {
                "database": self.db_service is not None,
                "excel": self.excel_service is not None,
                "notifications": self.notification_service is not None,
            },
        }

    def get_statistics(self) -> Dict[str, Any]:
        """Get real application statistics"""
        stats = self.stats.copy()

        # Add calculated metrics
        uptime = datetime.now() - stats["session_start"]
        stats["uptime_hours"] = round(uptime.total_seconds() / 3600, 2)

        if stats["total_imports"] > 0:
            stats["avg_records_per_import"] = round(
                stats["total_records"] / stats["total_imports"]
            )
        else:
            stats["avg_records_per_import"] = 0

        return stats

    def reset_state(self):
        """Reset application state properly"""
        # Disconnect database if connected
        if self.app_state["db_connected"] and self.db_service:
            try:
                self.db_service.close()
            except:
                pass

        # Reset state
        self.app_state = {
            "db_connected": False,
            "current_file": None,
            "selected_table": None,
            "import_progress": 0,
            "last_operation": None,
            "operation_status": "ready",
        }

        # Reset statistics except session start
        session_start = self.stats["session_start"]
        self.stats = {
            "total_imports": 0,
            "total_records": 0,
            "total_tables": 0,
            "mock_generated": 0,
            "session_start": session_start,
        }

        self.emit("db_status_changed", False)
        self.update_status("🔄 Application state reset", "info")

    def close(self):
        """Properly close controller and services"""
        self.is_running = False

        if self.db_service:
            try:
                self.db_service.close()
            except:
                pass

        logger.info("Application controller closed")
