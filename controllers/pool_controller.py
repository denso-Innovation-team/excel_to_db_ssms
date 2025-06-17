"""
Pool Controller - Enhanced Business Logic Layer
Controls Excel to Database operations with validation and error handling
"""

import logging
import threading
from typing import Dict, List, Any, Callable
from pathlib import Path
import pandas as pd
from datetime import datetime

logger = logging.getLogger(__name__)


class PoolController:
    """Enhanced controller for Excel to Database Pool operations"""

    def __init__(self, pool_service):
        self.pool_service = pool_service
        self.current_config = None
        self.current_excel_file = None
        self.field_mappings = {}
        self.validation_rules = {}
        self.event_callbacks = {}

    def register_callback(self, event: str, callback: Callable):
        """Register event callback"""
        if event not in self.event_callbacks:
            self.event_callbacks[event] = []
        self.event_callbacks[event].append(callback)

    def _emit_event(self, event: str, data: Any = None):
        """Emit event to callbacks"""
        for callback in self.event_callbacks.get(event, []):
            try:
                callback(data)
            except Exception as e:
                logger.error(f"Event callback error: {e}")

    def test_database_connection(self, config: Dict[str, Any]) -> tuple[bool, str]:
        """Test database connection"""
        try:
            from services.connection_pool_service import ConnectionConfig

            db_config = ConnectionConfig(
                db_type=config["db_type"],
                host=config.get("host"),
                database=config.get("database"),
                username=config.get("username"),
                password=config.get("password"),
                port=config.get("port", 1433),
                sqlite_path=config.get("sqlite_path"),
            )

            return self.pool_service.test_connection(db_config)

        except Exception as e:
            return False, str(e)

    def connect_database(self, config: Dict[str, Any]) -> tuple[bool, str]:
        """Connect to database and create pool"""
        try:
            from services.connection_pool_service import ConnectionConfig

            db_config = ConnectionConfig(
                db_type=config["db_type"],
                host=config.get("host"),
                database=config.get("database"),
                username=config.get("username"),
                password=config.get("password"),
                port=config.get("port", 1433),
                sqlite_path=config.get("sqlite_path"),
                pool_size=config.get("pool_size", 5),
                max_overflow=config.get("max_overflow", 10),
            )

            success = self.pool_service.create_pool(db_config, "main")
            if success:
                self.current_config = config
                self._emit_event("database_connected", config)
                return True, "Database connected successfully"
            else:
                return False, "Failed to create connection pool"

        except Exception as e:
            return False, str(e)

    def get_databases(self) -> List[str]:
        """Get available databases"""
        try:
            if not self.current_config:
                return []

            if self.current_config["db_type"] == "sqlserver":
                query = "SELECT name FROM sys.databases WHERE database_id > 4"
                results = self.pool_service.execute_query(query, pool_name="main")
                return [row["name"] for row in results]
            else:
                # For SQLite, return local .db files
                db_files = list(Path(".").glob("*.db"))
                return [str(f) for f in db_files]

        except Exception as e:
            logger.error(f"Failed to get databases: {e}")
            return []

    def get_tables(self) -> List[str]:
        """Get tables in current database"""
        try:
            return self.pool_service.get_tables("main")
        except Exception as e:
            logger.error(f"Failed to get tables: {e}")
            return []

    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """Get table schema"""
        try:
            return self.pool_service.get_table_schema(table_name, "main")
        except Exception as e:
            logger.error(f"Failed to get schema: {e}")
            return []

    def load_excel_file(self, file_path: str) -> tuple[bool, Dict[str, Any]]:
        """Load and analyze Excel file"""
        try:
            if not Path(file_path).exists():
                return False, {"error": "File not found"}

            # Read Excel file info
            df = pd.read_excel(file_path, nrows=10)  # Sample for analysis

            file_info = {
                "file_path": file_path,
                "file_name": Path(file_path).name,
                "columns": list(df.columns),
                "sample_rows": len(df),
                "data_types": {col: str(dtype) for col, dtype in df.dtypes.items()},
                "sample_data": df.head(5).to_dict("records"),
            }

            # Get full row count efficiently
            full_df = pd.read_excel(file_path, usecols=[0])
            file_info["total_rows"] = len(full_df)

            self.current_excel_file = file_info
            self._emit_event("excel_loaded", file_info)

            return True, file_info

        except Exception as e:
            error_msg = f"Failed to load Excel file: {str(e)}"
            logger.error(error_msg)
            return False, {"error": error_msg}

    def create_field_mapping(
        self, excel_column: str, db_column: str, transformation: str = None
    ) -> bool:
        """Create field mapping between Excel and database"""
        try:
            self.field_mappings[excel_column] = {
                "db_column": db_column,
                "transformation": transformation,
                "created_at": datetime.now(),
            }
            return True
        except Exception as e:
            logger.error(f"Failed to create field mapping: {e}")
            return False

    def auto_map_fields(self, table_name: str) -> Dict[str, str]:
        """Auto-map fields based on similarity"""
        try:
            if not self.current_excel_file:
                return {}

            excel_columns = self.current_excel_file["columns"]
            db_schema = self.get_table_schema(table_name)
            db_columns = [col["name"] for col in db_schema]

            mappings = {}

            # Simple name matching algorithm
            for excel_col in excel_columns:
                excel_clean = excel_col.lower().strip().replace(" ", "_")

                # Exact match
                for db_col in db_columns:
                    if excel_clean == db_col.lower():
                        mappings[excel_col] = db_col
                        break

                # Partial match if no exact match
                if excel_col not in mappings:
                    for db_col in db_columns:
                        if (
                            excel_clean in db_col.lower()
                            or db_col.lower() in excel_clean
                        ):
                            mappings[excel_col] = db_col
                            break

            # Update field mappings
            for excel_col, db_col in mappings.items():
                self.create_field_mapping(excel_col, db_col)

            return mappings

        except Exception as e:
            logger.error(f"Auto mapping failed: {e}")
            return {}

    def validate_mappings(self) -> tuple[bool, List[str]]:
        """Validate current field mappings"""
        errors = []

        if not self.field_mappings:
            errors.append("No field mappings defined")

        if not self.current_excel_file:
            errors.append("No Excel file loaded")

        # Additional validation logic here

        return len(errors) == 0, errors

    def import_data(self, table_name: str, options: Dict[str, Any] = None) -> bool:
        """Import Excel data to database"""

        def import_async():
            try:
                self._emit_event("import_started", {"table": table_name})

                # Validate prerequisites
                is_valid, errors = self.validate_mappings()
                if not is_valid:
                    raise Exception(f"Validation failed: {', '.join(errors)}")

                # Read Excel data
                self._emit_event(
                    "import_progress", {"progress": 10, "status": "Reading Excel file"}
                )
                df = pd.read_excel(self.current_excel_file["file_path"])

                # Apply field mappings
                self._emit_event(
                    "import_progress", {"progress": 30, "status": "Mapping fields"}
                )
                mapped_data = self._apply_mappings(df)

                # Validate data
                self._emit_event(
                    "import_progress", {"progress": 50, "status": "Validating data"}
                )
                validated_data = self._validate_data(mapped_data)

                # Import to database
                self._emit_event(
                    "import_progress",
                    {"progress": 70, "status": "Importing to database"},
                )
                batch_size = options.get("batch_size", 1000) if options else 1000

                success = self.pool_service.bulk_insert(
                    table_name, validated_data, batch_size=batch_size, pool_name="main"
                )

                if success:
                    self._emit_event(
                        "import_progress",
                        {"progress": 100, "status": "Import completed"},
                    )
                    self._emit_event(
                        "import_completed",
                        {
                            "table": table_name,
                            "rows": len(validated_data),
                            "success": True,
                        },
                    )
                else:
                    raise Exception("Database import failed")

            except Exception as e:
                logger.error(f"Import failed: {e}")
                self._emit_event("import_error", {"error": str(e)})

        # Run import in background thread
        thread = threading.Thread(target=import_async, daemon=True)
        thread.start()
        return True

    def _apply_mappings(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Apply field mappings to dataframe"""
        mapped_data = []

        for _, row in df.iterrows():
            mapped_row = {}

            for excel_col, mapping in self.field_mappings.items():
                if excel_col in row:
                    value = row[excel_col]

                    # Apply transformation if specified
                    if mapping.get("transformation"):
                        value = self._apply_transformation(
                            value, mapping["transformation"]
                        )

                    mapped_row[mapping["db_column"]] = value

            mapped_data.append(mapped_row)

        return mapped_data

    def _apply_transformation(self, value: Any, transformation: str) -> Any:
        """Apply data transformation"""
        try:
            if pd.isna(value):
                return None

            if transformation == "uppercase":
                return str(value).upper()
            elif transformation == "lowercase":
                return str(value).lower()
            elif transformation == "trim":
                return str(value).strip()
            elif transformation == "date_format":
                return pd.to_datetime(value).strftime("%Y-%m-%d") if value else None
            else:
                return value
        except Exception:
            return value

    def _validate_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate data before import"""
        validated_data = []

        for row in data:
            # Apply validation rules
            validated_row = {}

            for column, value in row.items():
                # Basic null handling
                if pd.isna(value):
                    validated_row[column] = None
                else:
                    validated_row[column] = value

            validated_data.append(validated_row)

        return validated_data

    def get_import_preview(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get preview of mapped data"""
        try:
            if not self.current_excel_file:
                return []

            df = pd.read_excel(self.current_excel_file["file_path"], nrows=limit)
            return self._apply_mappings(df)

        except Exception as e:
            logger.error(f"Preview failed: {e}")
            return []

    def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection pool statistics"""
        try:
            return self.pool_service.get_pool_stats("main")
        except Exception:
            return {}

    def disconnect(self):
        """Disconnect from database"""
        try:
            self.pool_service.close_pool("main")
            self.current_config = None
            self._emit_event("database_disconnected", None)
        except Exception as e:
            logger.error(f"Disconnect failed: {e}")

    def cleanup(self):
        """Cleanup resources"""
        try:
            self.pool_service.close_all_pools()
            self.current_config = None
            self.current_excel_file = None
            self.field_mappings.clear()
            self.event_callbacks.clear()
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
