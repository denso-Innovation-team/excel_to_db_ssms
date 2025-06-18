"""
controllers/app_controller.py
Main Application Controller - DENSO888 Professional
"""

import logging
from typing import Dict, Any, List, Tuple
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class AppController:
    """Main application controller orchestrating all services"""

    def __init__(
        self,
        connection_service=None,
        excel_service=None,
        backup_service=None,
        ui_service=None,
        config=None,
    ):
        # Core services
        self.connection_service = connection_service
        self.excel_service = excel_service
        self.backup_service = backup_service
        self.ui_service = ui_service
        self.config = config

        # Additional services (loaded lazily)
        self.validation_service = None
        self.cache_service = None

        # Application state
        self.is_connected = False
        self.current_excel_file = None
        self.current_database_config = None

        # Statistics
        self.stats = {
            "app_start_time": datetime.now(),
            "total_imports": 0,
            "total_exports": 0,
            "errors_count": 0,
        }

    def set_validation_service(self, validation_service):
        """Set validation service"""
        self.validation_service = validation_service

    def set_cache_service(self, cache_service):
        """Set cache service"""
        self.cache_service = cache_service

    # Database Operations
    def get_database_config(self) -> Dict[str, Any]:
        """Get current database configuration"""
        return self.current_database_config or {}

    def test_database_connection(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """Test database connection"""
        try:
            if not self.connection_service:
                return False, "Connection service not available"

            # Use connection service to test
            return self.connection_service.test_connection(config)

        except Exception as e:
            logger.error(f"Database test failed: {e}")
            return False, str(e)

    def connect_database(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """Connect to database"""
        try:
            if not self.connection_service:
                return False, "Connection service not available"

            success = self.connection_service.connect_database(config)

            if success:
                self.is_connected = True
                self.current_database_config = config
                return True, "Connected successfully"
            else:
                return False, "Connection failed"

        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False, str(e)

    def get_database_tables(self) -> List[str]:
        """Get list of database tables"""
        try:
            if not self.connection_service or not self.is_connected:
                return []

            return self.connection_service.get_tables()

        except Exception as e:
            logger.error(f"Failed to get tables: {e}")
            return []

    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """Get table information"""
        try:
            if not self.connection_service or not self.is_connected:
                return {"error": "Not connected to database"}

            # Get basic table info
            schema = self.connection_service.get_table_schema(table_name)

            # Get row count
            query = f"SELECT COUNT(*) as count FROM [{table_name}]"
            success, result = self.connection_service.execute_query(query)
            row_count = result[0].get("count", 0) if success and result else 0

            return {
                "table_name": table_name,
                "row_count": row_count,
                "column_count": len(schema),
                "columns": schema,
            }

        except Exception as e:
            logger.error(f"Failed to get table info: {e}")
            return {"error": str(e)}

    # Excel Operations
    def select_excel_file(self, file_path: str) -> Tuple[bool, Dict[str, Any]]:
        """Select and analyze Excel file"""
        try:
            if not self.excel_service:
                return False, {"error": "Excel service not available"}

            # Validate file
            success, message = self.excel_service.validate_file(file_path)
            if not success:
                return False, {"error": message}

            # Analyze file
            file_info = self.excel_service.analyze_file(file_path)

            if "error" in file_info:
                return False, file_info

            self.current_excel_file = file_info
            return True, file_info

        except Exception as e:
            logger.error(f"Excel file selection failed: {e}")
            return False, {"error": str(e)}

    def get_excel_sheets(self, file_path: str) -> List[str]:
        """Get Excel sheet names"""
        try:
            if not self.excel_service:
                return []

            return self.excel_service.get_sheet_names(file_path)

        except Exception as e:
            logger.error(f"Failed to get Excel sheets: {e}")
            return []

    # Import Operations
    def import_excel_data(self, table_name: str, options: Dict[str, Any]) -> bool:
        """Import Excel data to database"""
        try:
            if not self.is_connected:
                logger.error("Database not connected")
                return False

            if not self.current_excel_file:
                logger.error("No Excel file selected")
                return False

            # Read Excel data
            data = self.excel_service.read_file(
                self.current_excel_file["file_path"], options
            )

            if not data:
                logger.error("No data found in Excel file")
                return False

            # Validate data if validation service available
            if self.validation_service and options.get("validate_data", True):
                validation_rules = self._generate_validation_rules(data[0])
                validation_result = self.validation_service.validate_dataframe(
                    self._convert_to_dataframe(data), validation_rules
                )

                if not validation_result["valid"]:
                    logger.warning(
                        f"Validation warnings: {validation_result['warnings']}"
                    )

            # Import data using connection service
            success = self.connection_service.bulk_insert(
                table_name, data, options.get("batch_size", 1000)
            )

            if success:
                self.stats["total_imports"] += 1
                logger.info(f"Successfully imported {len(data)} rows to {table_name}")

            return success

        except Exception as e:
            self.stats["errors_count"] += 1
            logger.error(f"Import failed: {e}")
            return False

    # Export Operations
    def export_data(self, table_name: str, format_type: str, output_path: str) -> bool:
        """Export table data"""
        try:
            if not self.is_connected:
                return False

            # Get table data
            query = f"SELECT * FROM [{table_name}]"
            success, result = self.connection_service.execute_query(query)

            if not success or not result:
                return False

            # Export using excel service
            if self.excel_service:
                success = self.excel_service.export_data(
                    result, output_path, format_type
                )
                if success:
                    self.stats["total_exports"] += 1
                return success

            return False

        except Exception as e:
            logger.error(f"Export failed: {e}")
            return False

    # Mock Data Operations
    def get_mock_templates(self) -> List[Dict[str, Any]]:
        """Get available mock data templates"""
        return [
            {
                "id": "employees",
                "title": "👥 Employee Records",
                "description": "Staff data with departments, salaries, contact info",
                "recommended_count": "1,000 - 10,000",
            },
            {
                "id": "sales",
                "title": "💰 Sales Transactions",
                "description": "Customer orders with products, quantities, revenue",
                "recommended_count": "5,000 - 50,000",
            },
            {
                "id": "inventory",
                "title": "📦 Inventory Items",
                "description": "Product catalog with stock levels, supplier info",
                "recommended_count": "500 - 5,000",
            },
            {
                "id": "financial",
                "title": "💳 Financial Records",
                "description": "Accounting transactions with approvals, fiscal data",
                "recommended_count": "1,000 - 25,000",
            },
        ]

    def generate_mock_data(self, template_id: str, count: int, table_name: str) -> bool:
        """Generate mock data"""
        try:
            # Import mock data generator
            from core.mock_data_generator import MockDataGenerator

            generator = MockDataGenerator()

            # Generate data based on template
            if template_id == "employees":
                data = generator.generate_employees(count)
            elif template_id == "sales":
                data = generator.generate_sales(count)
            elif template_id == "inventory":
                data = generator.generate_inventory(count)
            elif template_id == "financial":
                data = generator.generate_financial(count)
            else:
                return False

            # Import to database
            if self.connection_service:
                success = self.connection_service.bulk_insert(table_name, data)
                if success:
                    logger.info(f"Generated {len(data)} {template_id} records")
                return success

            return False

        except Exception as e:
            logger.error(f"Mock data generation failed: {e}")
            return False

    # Analytics Operations
    def get_analytics_data(self) -> Dict[str, Any]:
        """Get analytics data"""
        try:
            if not self.is_connected:
                return {"error": "Not connected to database"}

            tables = self.get_database_tables()
            total_records = 0

            # Get record counts for each table
            table_stats = []
            for table in tables:
                try:
                    query = f"SELECT COUNT(*) as count FROM [{table}]"
                    success, result = self.connection_service.execute_query(query)
                    count = result[0].get("count", 0) if success and result else 0
                    total_records += count

                    table_stats.append(
                        {
                            "name": table,
                            "rows": count,
                        }
                    )
                except:
                    pass

            return {
                "tables": table_stats,
                "total_tables": len(tables),
                "total_records": total_records,
                "database_type": (
                    self.current_database_config.get("type", "unknown")
                    if self.current_database_config
                    else "unknown"
                ),
            }

        except Exception as e:
            logger.error(f"Analytics data failed: {e}")
            return {"error": str(e)}

    # Recent Operations
    def get_recent_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent application logs"""
        try:
            log_file = (
                Path("logs") / f"denso888_{datetime.now().strftime('%Y%m%d')}.log"
            )

            if not log_file.exists():
                return []

            logs = []
            with open(log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Parse recent log lines
            for line in lines[-limit:]:
                if " - " in line:
                    parts = line.strip().split(" - ", 3)
                    if len(parts) >= 4:
                        logs.append(
                            {
                                "timestamp": parts[0],
                                "level": parts[2],
                                "message": parts[3],
                                "module": parts[1],
                            }
                        )

            return logs

        except Exception as e:
            logger.error(f"Failed to get recent logs: {e}")
            return []

    # Utility Methods
    def _generate_validation_rules(
        self, sample_row: Dict[str, Any]
    ) -> Dict[str, Dict[str, Any]]:
        """Generate validation rules from sample data"""
        rules = {}

        for column, value in sample_row.items():
            rule = {"required": False}

            if isinstance(value, int):
                rule["min_value"] = 0
            elif isinstance(value, str) and "@" in value:
                rule["format"] = "email"

            rules[column] = rule

        return rules

    def _convert_to_dataframe(self, data: List[Dict]):
        """Convert data to pandas DataFrame"""
        try:
            import pandas as pd

            return pd.DataFrame(data)
        except ImportError:
            return None

    def get_application_stats(self) -> Dict[str, Any]:
        """Get application statistics"""
        uptime = datetime.now() - self.stats["app_start_time"]

        return {
            **self.stats,
            "uptime_seconds": uptime.total_seconds(),
            "is_connected": self.is_connected,
            "excel_file_loaded": self.current_excel_file is not None,
            "services_available": {
                "connection": self.connection_service is not None,
                "excel": self.excel_service is not None,
                "backup": self.backup_service is not None,
                "ui": self.ui_service is not None,
                "validation": self.validation_service is not None,
                "cache": self.cache_service is not None,
            },
        }

    def cleanup(self):
        """Cleanup application resources"""
        try:
            if self.connection_service:
                self.connection_service.close_all_pools()

            if self.backup_service:
                self.backup_service.stop()

            logger.info("Application cleanup completed")

        except Exception as e:
            logger.error(f"Cleanup error: {e}")
