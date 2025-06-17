"""
controllers/pool_controller.py
Main Controller for Excel to Database Pool Operations
"""

import threading
from typing import Dict, List, Any, Callable
from datetime import datetime
import pandas as pd

from services.connection_pool_service import ConnectionPoolService
from services.excel_service import ExcelService
from services.notification_service import NotificationService
from core.field_mapper import FieldMapper
from core.data_validator import DataValidator
from core.import_logger import ImportLogger


class PoolController:
    """Enhanced controller สำหรับการจัดการ Excel to Database operations"""

    def __init__(self, pool_service: ConnectionPoolService):
        self.pool_service = pool_service
        self.excel_service = ExcelService()
        self.notification_service = NotificationService()
        self.field_mapper = FieldMapper()
        self.validator = DataValidator()
        self.import_logger = ImportLogger()

        # State management
        self.current_excel_file = None
        self.current_database = None
        self.current_table = None
        self.field_mappings = {}
        self.validation_rules = {}

        # Event listeners
        self.event_listeners = {
            "database_connected": [],
            "excel_loaded": [],
            "import_progress": [],
            "import_complete": [],
            "error_occurred": [],
        }

    # ================ Database Operations ================
    def get_available_databases(self, db_type: str = "sqlserver") -> List[str]:
        """ดึงรายการฐานข้อมูลที่มีอยู่"""
        try:
            if db_type == "sqlserver":
                return self.pool_service.get_sqlserver_databases()
            else:  # sqlite
                return self.pool_service.get_sqlite_databases()
        except Exception as e:
            self._emit_event("error_occurred", str(e))
            return []

    def connect_to_database(self, db_config: Dict[str, Any]) -> bool:
        """เชื่อมต่อกับฐานข้อมูล"""
        try:
            success = self.pool_service.connect_database(db_config)
            if success:
                self.current_database = db_config
                self._emit_event("database_connected", db_config)
                self.notification_service.success(
                    f"เชื่อมต่อฐานข้อมูลสำเร็จ: {db_config.get('database', 'SQLite')}"
                )
            return success
        except Exception as e:
            self._emit_event("error_occurred", str(e))
            return False

    def get_database_tables(self) -> List[str]:
        """ดึงรายการตารางในฐานข้อมูล"""
        try:
            if not self.current_database:
                return []
            return self.pool_service.get_tables()
        except Exception as e:
            self._emit_event("error_occurred", str(e))
            return []

    def get_table_columns(self, table_name: str) -> List[Dict[str, Any]]:
        """ดึงรายการคอลัมน์ในตาราง"""
        try:
            return self.pool_service.get_table_schema(table_name)
        except Exception as e:
            self._emit_event("error_occurred", str(e))
            return []

    # ================ Excel Operations ================
    def load_excel_file(self, file_path: str) -> bool:
        """โหลดไฟล์ Excel และวิเคราะห์ข้อมูล"""
        try:
            file_info = self.excel_service.analyze_file(file_path)
            if "error" in file_info:
                self._emit_event("error_occurred", file_info["error"])
                return False

            self.current_excel_file = {"path": file_path, "info": file_info}

            self._emit_event("excel_loaded", file_info)
            self.notification_service.success(
                f"โหลดไฟล์ Excel สำเร็จ: {file_info['file_name']}"
            )
            return True

        except Exception as e:
            self._emit_event("error_occurred", str(e))
            return False

    def get_excel_columns(self) -> List[str]:
        """ดึงรายการคอลัมน์จากไฟล์ Excel"""
        if not self.current_excel_file:
            return []
        return self.current_excel_file["info"].get("columns", [])

    def preview_excel_data(self, rows: int = 10) -> List[Dict]:
        """แสดงตัวอย่างข้อมูลจาก Excel"""
        if not self.current_excel_file:
            return []
        return self.current_excel_file["info"].get("sample_data", [])[:rows]

    # ================ Field Mapping Operations ================
    def create_field_mapping(
        self, excel_column: str, db_column: str, transformation: str = None
    ) -> bool:
        """สร้างการแมพฟิลด์ระหว่าง Excel และ Database"""
        try:
            self.field_mappings[excel_column] = {
                "db_column": db_column,
                "transformation": transformation,
                "created_at": datetime.now(),
            }
            return True
        except Exception as e:
            self._emit_event("error_occurred", str(e))
            return False

    def get_field_mappings(self) -> Dict[str, Any]:
        """ดึงการแมพฟิลด์ปัจจุบัน"""
        return self.field_mappings.copy()

    def auto_map_fields(self, table_name: str) -> Dict[str, str]:
        """แมพฟิลด์อัตโนมัติตามชื่อที่คล้ายกัน"""
        try:
            excel_columns = self.get_excel_columns()
            db_columns = [col["name"] for col in self.get_table_columns(table_name)]

            auto_mapping = self.field_mapper.auto_map(excel_columns, db_columns)

            # Update current mappings
            for excel_col, db_col in auto_mapping.items():
                self.create_field_mapping(excel_col, db_col)

            return auto_mapping
        except Exception as e:
            self._emit_event("error_occurred", str(e))
            return {}

    # ================ Validation Operations ================
    def set_validation_rule(self, column: str, rule_type: str, rule_value: Any):
        """ตั้งค่ากฎการตรวจสอบข้อมูล"""
        if column not in self.validation_rules:
            self.validation_rules[column] = {}
        self.validation_rules[column][rule_type] = rule_value

    def validate_data_preview(self, data: List[Dict]) -> Dict[str, Any]:
        """ตรวจสอบความถูกต้องของข้อมูลตัวอย่าง"""
        try:
            df = pd.DataFrame(data)
            return self.validator.validate_dataframe(df, self.validation_rules)
        except Exception as e:
            return {"valid": False, "errors": [str(e)]}

    # ================ Import Operations ================
    def import_data(self, options: Dict[str, Any] = None) -> bool:
        """นำเข้าข้อมูลจาก Excel ไปยังฐานข้อมูล"""
        if not self._validate_import_ready():
            return False

        def import_async():
            try:
                self._emit_event(
                    "import_progress", {"progress": 0, "status": "เริ่มต้นการนำเข้า"}
                )

                # 1. Read Excel data
                self._emit_event(
                    "import_progress", {"progress": 10, "status": "อ่านข้อมูลจาก Excel"}
                )
                data = self.excel_service.read_file(
                    self.current_excel_file["path"], options or {}
                )

                # 2. Apply field mappings
                self._emit_event(
                    "import_progress", {"progress": 30, "status": "จับคู่ฟิลด์ข้อมูล"}
                )
                mapped_data = self._apply_field_mappings(data)

                # 3. Validate data
                self._emit_event(
                    "import_progress", {"progress": 50, "status": "ตรวจสอบความถูกต้อง"}
                )
                validation_result = self.validate_data_preview(
                    mapped_data[:100]
                )  # Sample validation

                if not validation_result.get("valid", False):
                    raise Exception(
                        f"Data validation failed: {validation_result.get('errors', [])}"
                    )

                # 4. Import to database
                self._emit_event(
                    "import_progress", {"progress": 70, "status": "นำเข้าสู่ฐานข้อมูล"}
                )
                success = self.pool_service.bulk_insert(
                    self.current_table,
                    mapped_data,
                    batch_size=options.get("batch_size", 1000),
                )

                if not success:
                    raise Exception("Database import failed")

                # 5. Log import operation
                self._emit_event(
                    "import_progress", {"progress": 90, "status": "บันทึกประวัติการนำเข้า"}
                )
                self.import_logger.log_import(
                    excel_file=self.current_excel_file["path"],
                    database=self.current_database.get("database", "SQLite"),
                    table=self.current_table,
                    records_count=len(mapped_data),
                    field_mappings=self.field_mappings,
                    status="success",
                )

                # 6. Complete
                self._emit_event(
                    "import_progress", {"progress": 100, "status": "นำเข้าข้อมูลสำเร็จ"}
                )
                self._emit_event(
                    "import_complete",
                    {
                        "records": len(mapped_data),
                        "table": self.current_table,
                        "duration": "calculated_duration",
                    },
                )

                self.notification_service.success(
                    f"นำเข้าข้อมูลสำเร็จ {len(mapped_data):,} รายการ"
                )

            except Exception as e:
                self.import_logger.log_import(
                    excel_file=(
                        self.current_excel_file["path"]
                        if self.current_excel_file
                        else "Unknown"
                    ),
                    database=(
                        self.current_database.get("database", "Unknown")
                        if self.current_database
                        else "Unknown"
                    ),
                    table=self.current_table or "Unknown",
                    records_count=0,
                    field_mappings=self.field_mappings,
                    status="failed",
                    error_message=str(e),
                )

                self._emit_event("error_occurred", str(e))
                self.notification_service.error(f"การนำเข้าข้อมูลล้มเหลว: {str(e)}")

        # Run import in background thread
        import_thread = threading.Thread(target=import_async, daemon=True)
        import_thread.start()
        return True

    def _validate_import_ready(self) -> bool:
        """ตรวจสอบความพร้อมสำหรับการนำเข้า"""
        if not self.current_excel_file:
            self.notification_service.error("กรุณาเลือกไฟล์ Excel ก่อน")
            return False

        if not self.current_database:
            self.notification_service.error("กรุณาเชื่อมต่อฐานข้อมูลก่อน")
            return False

        if not self.current_table:
            self.notification_service.error("กรุณาเลือกตารางก่อน")
            return False

        if not self.field_mappings:
            self.notification_service.error("กรุณาแมพฟิลด์ข้อมูลก่อน")
            return False

        return True

    def _apply_field_mappings(self, data: List[Dict]) -> List[Dict]:
        """ใช้การแมพฟิลด์กับข้อมูล"""
        mapped_data = []

        for row in data:
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
        """ใช้การแปลงข้อมูลตามที่กำหนด"""
        try:
            if transformation == "uppercase":
                return str(value).upper() if value else value
            elif transformation == "lowercase":
                return str(value).lower() if value else value
            elif transformation == "trim":
                return str(value).strip() if value else value
            elif transformation == "date_format":
                return pd.to_datetime(value).strftime("%Y-%m-%d") if value else None
            else:
                return value
        except:
            return value

    # ================ Import History ================
    def get_import_history(self, limit: int = 50) -> List[Dict]:
        """ดึงประวัติการนำเข้าข้อมูล"""
        return self.import_logger.get_import_history(limit)

    def get_import_statistics(self) -> Dict[str, Any]:
        """ดึงสстатистิกการนำเข้าข้อมูล"""
        return self.import_logger.get_statistics()

    # ================ Event System ================
    def subscribe(self, event: str, callback: Callable):
        """สมัครรับ event"""
        if event in self.event_listeners:
            self.event_listeners[event].append(callback)

    def _emit_event(self, event: str, data: Any = None):
        """ส่ง event ไปยัง listeners"""
        for callback in self.event_listeners.get(event, []):
            try:
                callback(data)
            except Exception as e:
                print(f"Event callback error: {e}")

    # ================ Utility Methods ================
    def set_current_table(self, table_name: str):
        """ตั้งค่าตารางปัจจุบัน"""
        self.current_table = table_name

    def reset_session(self):
        """รีเซ็ต session ปัจจุบัน"""
        self.current_excel_file = None
        self.current_table = None
        self.field_mappings = {}
        self.validation_rules = {}

    def get_session_info(self) -> Dict[str, Any]:
        """ดึงข้อมูล session ปัจจุบัน"""
        return {
            "excel_file": self.current_excel_file,
            "database": self.current_database,
            "table": self.current_table,
            "field_mappings": self.field_mappings,
            "validation_rules": self.validation_rules,
        }
