"""
controllers/pool_controller.py
Enhanced Pool Controller - Production Ready Implementation
Created by: Thammaphon Chittasuwanna (SDM) | Innovation Department
"""

import threading
from typing import Dict, Any, Callable, List, Optional, Tuple
from datetime import datetime
import logging
import queue

logger = logging.getLogger(__name__)


class PoolController:
    """Enhanced Pool Controller with comprehensive functionality"""

    def __init__(self, pool_service):
        self.pool_service = pool_service
        self.event_callbacks: Dict[str, List[Callable]] = {}
        self.current_excel_file: Optional[Dict[str, Any]] = None
        self.field_mappings: Dict[str, str] = {}
        self.is_connected = False
        self._lock = threading.Lock()  # Add thread lock
        self._operation_queue = queue.Queue()
        self._processing_thread = None
        self._shutdown = False
        self._should_stop = False

        # Status tracking
        self.last_operation = {
            "type": None,
            "status": "idle",
            "progress": 0,
            "message": "",
            "timestamp": None,
        }

        # Statistics
        self.stats = {
            "connections_made": 0,
            "files_processed": 0,
            "records_imported": 0,
            "errors_encountered": 0,
            "start_time": datetime.now(),
        }

        self._start_processing_thread()

    def _start_processing_thread(self):
        """Start background processing thread"""

        def process_operations():
            while not self._shutdown:
                try:
                    operation = self._operation_queue.get(timeout=1)
                    self._execute_operation(operation)
                except queue.Empty:
                    continue
                except Exception as e:
                    logger.error(f"Operation processing error: {e}")

        self._processing_thread = threading.Thread(
            target=process_operations, daemon=True
        )
        self._processing_thread.start()

    def _execute_operation(self, operation: Dict[str, Any]):
        """Execute queued operation"""
        try:
            op_type = operation.get("type")
            callback = operation.get("callback")
            args = operation.get("args", ())
            kwargs = operation.get("kwargs", {})

            if hasattr(self, f"_execute_{op_type}"):
                method = getattr(self, f"_execute_{op_type}")
                result = method(*args, **kwargs)
                if callback:
                    callback(result)
            else:
                logger.error(f"Unknown operation type: {op_type}")

        except Exception as e:
            logger.error(f"Operation execution failed: {e}")
            self.emit_event("operation_error", {"error": str(e)})

    # ================ EVENT SYSTEM ================
    def register_callback(self, event: str, callback: Callable):
        """Register event callback with validation"""
        if not callable(callback):
            raise ValueError("Callback must be callable")

        if event not in self.event_callbacks:
            self.event_callbacks[event] = []

        if callback not in self.event_callbacks[event]:
            self.event_callbacks[event].append(callback)
            logger.debug(f"Registered callback for event: {event}")

    def unregister_callback(self, event: str, callback: Callable):
        """Unregister event callback"""
        if event in self.event_callbacks:
            try:
                self.event_callbacks[event].remove(callback)
            except ValueError:
                pass

    def emit_event(self, event: str, data: Any = None):
        """Emit event to all registered callbacks"""
        if event in self.event_callbacks:
            for callback in self.event_callbacks[event]:
                try:
                    # Run callback in separate thread to avoid blocking
                    threading.Thread(target=callback, args=(data,), daemon=True).start()
                except Exception as e:
                    logger.error(f"Event callback error for {event}: {e}")

    # ================ DATABASE OPERATIONS ================
    def test_database_connection(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """Test database connection asynchronously"""
        self._update_operation_status(
            "connection_test", "testing", 0, "Testing connection..."
        )

        def test_async():
            try:
                # Create temporary connection pool service for testing
                from services.connection_pool_service import ConnectionPoolService

                temp_service = ConnectionPoolService()

                # Test connection
                success = temp_service.connect_database(config)

                if success:
                    # Test basic query
                    test_result = temp_service.execute_query("SELECT 1")
                    temp_service.close_all_pools()

                    if test_result[0]:
                        self._update_operation_status(
                            "connection_test",
                            "completed",
                            100,
                            "Connection test successful",
                        )
                        return True, "Connection test successful"
                    else:
                        self._update_operation_status(
                            "connection_test", "failed", 0, "Query test failed"
                        )
                        return False, "Query test failed"
                else:
                    self._update_operation_status(
                        "connection_test", "failed", 0, "Connection failed"
                    )
                    return False, "Connection failed"

            except Exception as e:
                error_msg = f"Connection test error: {str(e)}"
                self._update_operation_status("connection_test", "failed", 0, error_msg)
                return False, error_msg

        # Execute immediately for connection test
        try:
            return test_async()
        except Exception as e:
            return False, str(e)

    def _execute_test_connection(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """Execute connection test"""
        try:
            from services.connection_pool_service import ConnectionPoolService

            temp_service = ConnectionPoolService()

            success = temp_service.connect_database(config)
            if success:
                test_result = temp_service.execute_query("SELECT 1")
                temp_service.close_all_pools()
                return test_result[0], (
                    "Connection test successful" if test_result[0] else test_result[1]
                )
            else:
                return False, "Connection failed"
        except Exception as e:
            return False, str(e)

    def connect_database(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """Connect to database with comprehensive validation"""
        try:
            self._update_operation_status(
                "database_connection", "connecting", 25, "Connecting to database..."
            )

            # Validate configuration
            if not self._validate_database_config(config):
                return False, "Invalid database configuration"

            # Connect using pool service
            success = self.pool_service.connect_database(config)

            if success:
                self.is_connected = True
                self.stats["connections_made"] += 1
                self._update_operation_status(
                    "database_connection", "completed", 100, "Connected successfully"
                )

                # Test basic operations
                tables = self.get_tables()
                logger.info(f"Connected to database with {len(tables)} tables")

                self.emit_event(
                    "database_connected",
                    {
                        "config": config,
                        "tables_count": len(tables),
                        "timestamp": datetime.now().isoformat(),
                    },
                )

                return True, f"Connected successfully. Found {len(tables)} tables."
            else:
                self.is_connected = False
                self._update_operation_status(
                    "database_connection", "failed", 0, "Connection failed"
                )
                return False, "Failed to connect to database"

        except Exception as e:
            self.is_connected = False
            self.stats["errors_encountered"] += 1
            error_msg = f"Connection error: {str(e)}"
            self._update_operation_status("database_connection", "failed", 0, error_msg)
            return False, error_msg

    def _validate_database_config(self, config: Dict[str, Any]) -> bool:
        """Validate database configuration"""
        if not isinstance(config, dict):
            return False

        db_type = config.get("type")
        if not db_type:
            return False

        if db_type == "sqlite":
            return True  # SQLite requires minimal config
        elif db_type == "sqlserver":
            required = ["server", "database"]
            return all(config.get(field) for field in required)
        else:
            return False

    def disconnect(self):
        """Disconnect from database"""
        try:
            if self.pool_service:
                self.pool_service.close_all_pools()
            self.is_connected = False
            self.current_excel_file = None
            self.field_mappings.clear()

            self.emit_event(
                "database_disconnected", {"timestamp": datetime.now().isoformat()}
            )

            logger.info("Disconnected from database")
        except Exception as e:
            logger.error(f"Disconnect error: {e}")

    def get_tables(self) -> List[str]:
        """Get database tables with error handling"""
        if not self.is_connected:
            return []
        try:
            return self.pool_service.get_tables()
        except Exception as e:
            logger.error(f"Error getting tables: {e}")
            return []

    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """Get table schema information"""
        if not self.is_connected or not table_name:
            return []

        try:
            # Get table schema using SQL queries
            if (
                hasattr(self.pool_service, "current_config")
                and self.pool_service.current_config
            ):
                db_type = self.pool_service.current_config.get("type", "sqlite")

                if db_type == "sqlite":
                    query = f"PRAGMA table_info([{table_name}])"
                    success, result = self.pool_service.execute_query(query)

                    if success and isinstance(result, list):
                        schema = []
                        for row in result:
                            schema.append(
                                {
                                    "name": row.get("name", ""),
                                    "type": row.get("type", "TEXT"),
                                    "nullable": not row.get("notnull", 0),
                                    "default": row.get("dflt_value"),
                                    "primary_key": bool(row.get("pk", 0)),
                                }
                            )
                        return schema
                else:  # SQL Server
                    query = """
                        SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
                        FROM INFORMATION_SCHEMA.COLUMNS 
                        WHERE TABLE_NAME = ?
                        ORDER BY ORDINAL_POSITION
                    """
                    success, result = self.pool_service.execute_query(
                        query, (table_name,)
                    )

                    if success and isinstance(result, list):
                        schema = []
                        for row in result:
                            schema.append(
                                {
                                    "name": row.get("COLUMN_NAME", ""),
                                    "type": row.get("DATA_TYPE", "VARCHAR"),
                                    "nullable": row.get("IS_NULLABLE", "YES") == "YES",
                                    "default": row.get("COLUMN_DEFAULT"),
                                    "primary_key": False,
                                }
                            )
                        return schema

            return []
        except Exception as e:
            logger.error(f"Error getting table schema for {table_name}: {e}")
            return []

    # ================ EXCEL OPERATIONS ================
    def load_excel_file(self, file_path: str) -> Tuple[bool, Dict[str, Any]]:
        """Load and analyze Excel file"""
        try:
            self._update_operation_status(
                "excel_load", "loading", 25, "Loading Excel file..."
            )

            # Validate file path
            from pathlib import Path

            if not Path(file_path).exists():
                return False, {"error": "File not found"}

            # Use Excel service to analyze file
            from services.excel_service import ExcelService

            excel_service = ExcelService()

            self._update_operation_status(
                "excel_load", "analyzing", 50, "Analyzing file structure..."
            )

            # Analyze file
            file_info = excel_service.analyze_file(file_path)

            if "error" in file_info:
                self._update_operation_status(
                    "excel_load", "failed", 0, f"Analysis failed: {file_info['error']}"
                )
                return False, file_info

            # Store file info
            self.current_excel_file = file_info
            self.stats["files_processed"] += 1

            self._update_operation_status(
                "excel_load", "completed", 100, "File loaded successfully"
            )

            self.emit_event(
                "excel_loaded",
                {"file_info": file_info, "timestamp": datetime.now().isoformat()},
            )

            logger.info(
                f"Loaded Excel file: {file_info.get('file_name', 'Unknown')} with {file_info.get('total_rows', 0)} rows"
            )
            return True, file_info

        except Exception as e:
            self.stats["errors_encountered"] += 1
            error_msg = f"Excel load error: {str(e)}"
            self._update_operation_status("excel_load", "failed", 0, error_msg)
            logger.error(error_msg)
            return False, {"error": error_msg}

    def auto_map_fields(self, table_name: str) -> Dict[str, str]:
        """Auto-map Excel fields to database columns"""
        if not self.current_excel_file or not table_name:
            return {}

        try:
            excel_columns = self.current_excel_file.get("columns", [])
            db_schema = self.get_table_schema(table_name)
            db_columns = [col["name"] for col in db_schema]

            mappings = {}

            # Simple similarity matching
            for excel_col in excel_columns:
                excel_clean = self._normalize_column_name(excel_col)

                # Exact match first
                for db_col in db_columns:
                    db_clean = self._normalize_column_name(db_col)
                    if excel_clean == db_clean:
                        mappings[excel_col] = db_col
                        break

                # Partial match if no exact match
                if excel_col not in mappings:
                    for db_col in db_columns:
                        db_clean = self._normalize_column_name(db_col)
                        if excel_clean in db_clean or db_clean in excel_clean:
                            mappings[excel_col] = db_col
                            break

            self.field_mappings = mappings
            logger.info(f"Auto-mapped {len(mappings)} fields for table {table_name}")
            return mappings

        except Exception as e:
            logger.error(f"Auto-mapping error: {e}")
            return {}

    def _normalize_column_name(self, name: str) -> str:
        """Normalize column name for comparison"""
        import re

        normalized = str(name).lower().strip()
        normalized = re.sub(r"[^\w]", "_", normalized)
        normalized = re.sub(r"_+", "_", normalized)
        return normalized.strip("_")

    def get_import_preview(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get preview of import data with field mappings applied"""
        if not self.current_excel_file:
            return []

        try:
            sample_data = self.current_excel_file.get("sample_data", [])
            preview_data = []

            for row in sample_data[:limit]:
                mapped_row = {}
                for excel_col, value in row.items():
                    db_col = self.field_mappings.get(excel_col, excel_col)
                    mapped_row[db_col] = value
                preview_data.append(mapped_row)

            return preview_data
        except Exception as e:
            logger.error(f"Preview generation error: {e}")
            return []

    # ================ IMPORT OPERATIONS ================
    def import_data(self, table_name: str, options: Dict[str, Any]) -> bool:
        """Import Excel data to database with progress tracking"""
        if not self.is_connected or not self.current_excel_file:
            logger.error("Cannot import: not connected or no file loaded")
            return False

        with self._lock:

            def import_job():
                try:
                    self._update_operation_status(
                        "data_import", "starting", 5, "Starting data import..."
                    )
                    self.emit_event(
                        "import_progress",
                        {"progress": 5, "status": "Starting import..."},
                    )

                    # Read Excel file completely
                    from services.excel_service import ExcelService

                    excel_service = ExcelService()

                    self._update_operation_status(
                        "data_import", "reading", 20, "Reading Excel file..."
                    )
                    self.emit_event(
                        "import_progress",
                        {"progress": 20, "status": "Reading Excel file..."},
                    )

                    data = excel_service.read_file(
                        self.current_excel_file["file_path"], options
                    )

                    if not data:
                        raise Exception("No data found in Excel file")

                    self._update_operation_status(
                        "data_import", "processing", 40, "Processing data..."
                    )
                    self.emit_event(
                        "import_progress",
                        {"progress": 40, "status": "Processing data..."},
                    )

                    # Apply field mappings
                    if self.field_mappings:
                        mapped_data = []
                        for row in data:
                            mapped_row = {}
                            for excel_col, value in row.items():
                                db_col = self.field_mappings.get(excel_col, excel_col)
                                mapped_row[db_col] = value
                            mapped_data.append(mapped_row)
                        data = mapped_data

                    self._update_operation_status(
                        "data_import",
                        "creating_table",
                        60,
                        "Creating/updating table...",
                    )
                    self.emit_event(
                        "import_progress",
                        {"progress": 60, "status": "Creating table..."},
                    )

                    # Create table if needed
                    if options.get("mode") == "replace":
                        # For replace mode, we'll let bulk_insert handle table creation
                        pass

                    self._update_operation_status(
                        "data_import", "inserting", 80, "Inserting data..."
                    )
                    self.emit_event(
                        "import_progress",
                        {"progress": 80, "status": "Inserting data..."},
                    )

                    # Bulk insert data
                    batch_size = options.get("batch_size", 1000)
                    success = self.pool_service.bulk_insert(
                        table_name, data, batch_size
                    )

                    if success:
                        self.stats["records_imported"] += len(data)
                        self._update_operation_status(
                            "data_import",
                            "completed",
                            100,
                            "Import completed successfully",
                        )

                        self.emit_event(
                            "import_progress",
                            {"progress": 100, "status": "Import completed!"},
                        )
                        self.emit_event(
                            "import_completed",
                            {
                                "table": table_name,
                                "rows": len(data),
                                "timestamp": datetime.now().isoformat(),
                            },
                        )

                        logger.info(
                            f"Successfully imported {len(data)} rows to {table_name}"
                        )
                        return True
                    else:
                        raise Exception("Bulk insert operation failed")

                except Exception as e:
                    self.stats["errors_encountered"] += 1
                    error_msg = f"Import failed: {str(e)}"
                    self._update_operation_status("data_import", "failed", 0, error_msg)

                    self.emit_event(
                        "import_progress", {"progress": 0, "status": "Import failed"}
                    )
                    self.emit_event("import_error", {"error": error_msg})

                    logger.error(error_msg)
                    return False

            # Start import thread
            self._should_stop = False
            thread = threading.Thread(target=import_job, daemon=True)
            thread.start()
            return True

    def stop_import(self):
        """Stop ongoing import"""
        self._should_stop = True

    # ================ STATUS AND STATISTICS ================
    def _update_operation_status(
        self, op_type: str, status: str, progress: int, message: str
    ):
        """Update current operation status"""
        self.last_operation = {
            "type": op_type,
            "status": status,
            "progress": progress,
            "message": message,
            "timestamp": datetime.now().isoformat(),
        }

    def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection pool statistics"""
        if self.pool_service:
            return self.pool_service.get_service_stats()
        else:
            return {
                "connected": self.is_connected,
                "total_connections": 0,
                "in_use_connections": 0,
                "available_connections": 0,
            }

    def get_controller_stats(self) -> Dict[str, Any]:
        """Get controller statistics"""
        uptime = datetime.now() - self.stats["start_time"]

        return {
            **self.stats,
            "uptime_seconds": uptime.total_seconds(),
            "is_connected": self.is_connected,
            "excel_file_loaded": self.current_excel_file is not None,
            "field_mappings_count": len(self.field_mappings),
            "last_operation": self.last_operation,
            "service_stats": self.get_connection_stats(),
        }

    def get_operation_status(self) -> Dict[str, Any]:
        """Get current operation status"""
        return self.last_operation.copy()

    # ================ CLEANUP ================
    def cleanup(self):
        """Cleanup resources"""
        try:
            self._shutdown = True

            # Disconnect from database
            if self.is_connected:
                self.disconnect()

            # Clear data
            self.current_excel_file = None
            self.field_mappings.clear()
            self.event_callbacks.clear()

            # Wait for processing thread to finish
            if self._processing_thread and self._processing_thread.is_alive():
                self._processing_thread.join(timeout=5)

            logger.info("Pool controller cleanup completed")

        except Exception as e:
            logger.error(f"Cleanup error: {e}")

    def __del__(self):
        """Destructor"""
        try:
            self.cleanup()
        except:
            pass
