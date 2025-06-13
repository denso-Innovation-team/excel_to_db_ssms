import time
import logging
from typing import Dict, Any, Optional, Callable
from datetime import datetime

from .excel_handler import ExcelHandler
from .database_manager import DatabaseManager
from .mock_generator import MockDataGenerator

logger = logging.getLogger(__name__)


class DataProcessor:
    """Main data processing coordinator"""

    def __init__(
        self, data_source_config: Dict[str, Any], database_config, processing_config
    ):
        self.data_source_config = data_source_config
        self.database_config = database_config
        self.processing_config = processing_config

        # Initialize components
        self.excel_handler = ExcelHandler()
        self.db_manager = DatabaseManager(database_config)
        self.mock_generator = MockDataGenerator()

        # Processing state
        self._stop_requested = False
        self._current_progress = 0

    def process(
        self,
        progress_callback: Optional[Callable] = None,
        log_callback: Optional[Callable] = None,
    ) -> Dict[str, Any]:
        """Execute complete data processing pipeline"""

        start_time = time.time()

        try:
            # Step 1: Initialize database connection
            self._update_progress(5, "เชื่อมต่อฐานข้อมูล...", progress_callback)

            if not self.db_manager.connect():
                raise Exception("ไม่สามารถเชื่อมต่อฐานข้อมูลได้")

            self._log("เชื่อมต่อฐานข้อมูลสำเร็จ", "info", log_callback)

            # Step 2: Prepare data source
            self._update_progress(15, "เตรียมข้อมูลต้นทาง...", progress_callback)

            data_info = self._prepare_data_source()
            total_rows = data_info.get("total_rows", 0)

            self._log(f"พบข้อมูล {total_rows:,} แถว", "info", log_callback)

            # Step 3: Create table
            self._update_progress(25, "สร้างตารางในฐานข้อมูล...", progress_callback)

            table_name = self.data_source_config.get("table_name", "imported_data")

            # Step 4: Process data in chunks
            self._update_progress(30, "เริ่มประมวลผลข้อมูล...", progress_callback)

            total_inserted = 0
            table_created = False

            for chunk_data in self._get_data_chunks():
                if self._stop_requested:
                    raise Exception("การประมวลผลถูกยกเลิก")

                df = chunk_data["dataframe"]

                # Create table with first chunk
                if not table_created:
                    type_mapping = chunk_data.get("type_mapping", {})
                    self.db_manager.create_table_from_dataframe(
                        table_name, df, type_mapping
                    )
                    table_created = True
                    self._log(f"สร้างตาราง '{table_name}' สำเร็จ", "info", log_callback)

                # Insert data
                rows_inserted = self.db_manager.bulk_insert(table_name, df)
                total_inserted += rows_inserted

                # Update progress
                progress = (
                    30 + (60 * total_inserted / total_rows) if total_rows > 0 else 90
                )
                self._update_progress(
                    min(progress, 90),
                    f"ประมวลผล: {total_inserted:,}/{total_rows:,} แถว",
                    progress_callback,
                )

                self._log(
                    f"นำเข้า {rows_inserted:,} แถว (รวม {total_inserted:,})",
                    "debug",
                    log_callback,
                )

            # Step 5: Finalize
            self._update_progress(95, "เสร็จสิ้นการประมวลผล...", progress_callback)

            end_time = time.time()
            duration = end_time - start_time

            # Get final table info
            table_info = self.db_manager.get_table_info(table_name)

            self._update_progress(100, "สำเร็จ!", progress_callback)
            self._log(
                f"ประมวลผลเสร็จสิ้น: {total_inserted:,} แถวใน {duration:.2f} วินาที",
                "info",
                log_callback,
            )

            return {
                "success": True,
                "rows_processed": total_inserted,
                "duration": duration,
                "table_name": table_name,
                "database_type": self.db_manager.db_type,
                "table_info": table_info,
                "metrics": {
                    "rows_per_second": total_inserted / duration if duration > 0 else 0,
                    "processing_stages": {
                        "preparation": 25,
                        "data_processing": 65,
                        "finalization": 10,
                    },
                },
            }

        except Exception as e:
            error_msg = str(e)
            self._log(f"เกิดข้อผิดพลาด: {error_msg}", "error", log_callback)

            return {
                "success": False,
                "error": error_msg,
                "rows_processed": getattr(self, "total_inserted", 0),
                "duration": time.time() - start_time,
            }

        finally:
            # Cleanup
            try:
                self.db_manager.close()
            except:
                pass

    def stop(self):
        """Request processing to stop"""
        self._stop_requested = True
        logger.info("Stop requested for data processing")

    def cleanup(self):
        """Cleanup resources"""
        try:
            self.db_manager.close()
        except:
            pass

    def _prepare_data_source(self) -> Dict[str, Any]:
        """Prepare data source based on configuration"""

        source_type = self.data_source_config.get("type", "mock")

        if source_type == "mock":
            template = self.data_source_config.get("template", "employees")
            rows = self.data_source_config.get("rows", 1000)

            return {
                "type": "mock",
                "template": template,
                "total_rows": rows,
                "source_description": f"Mock data: {template} ({rows:,} rows)",
            }

        elif source_type == "excel":
            file_path = self.data_source_config.get("file_path")
            sheet_name = self.data_source_config.get("sheet_name")

            if not file_path:
                raise ValueError("ไม่ได้ระบุไฟล์ Excel")

            file_info = self.excel_handler.load_file(file_path, sheet_name)

            return {
                "type": "excel",
                "file_path": file_path,
                "sheet_name": sheet_name,
                "total_rows": file_info["total_rows"],
                "total_columns": file_info["total_columns"],
                "source_description": f"Excel file: {file_info['file_path']} ({file_info['total_rows']:,} rows)",
            }

        else:
            raise ValueError(f"ประเภทข้อมูลไม่รองรับ: {source_type}")

    def _get_data_chunks(self):
        """Get data chunks based on source type"""

        source_type = self.data_source_config.get("type", "mock")
        chunk_size = self.processing_config.chunk_size

        if source_type == "mock":
            template = self.data_source_config.get("template", "employees")
            rows = self.data_source_config.get("rows", 1000)

            # Generate data in chunks
            remaining_rows = rows
            chunk_number = 0

            while remaining_rows > 0:
                current_chunk_size = min(chunk_size, remaining_rows)

                # Generate chunk data
                if template == "employees":
                    df = self.mock_generator.generate_employee_data(current_chunk_size)
                elif template == "sales":
                    df = self.mock_generator.generate_sales_data(current_chunk_size)
                elif template == "inventory":
                    df = self.mock_generator.generate_inventory_data(current_chunk_size)
                elif template == "financial":
                    df = self.mock_generator.generate_financial_data(current_chunk_size)
                else:
                    df = self.mock_generator.generate_custom_data(current_chunk_size)

                # Auto-detect types for first chunk
                type_mapping = None
                if chunk_number == 0:
                    from .excel_handler import TypeDetector

                    detector = TypeDetector()
                    type_mapping = detector.detect_types(df.columns.tolist())

                yield {
                    "chunk_number": chunk_number + 1,
                    "dataframe": df,
                    "rows_count": len(df),
                    "type_mapping": type_mapping,
                }

                remaining_rows -= current_chunk_size
                chunk_number += 1

        elif source_type == "excel":
            # Process Excel file in chunks
            for chunk_data in self.excel_handler.process_file(chunk_size):
                yield chunk_data

        else:
            raise ValueError(f"ประเภทข้อมูลไม่รองรับ: {source_type}")

    def _update_progress(
        self, progress: float, message: str, callback: Optional[Callable] = None
    ):
        """Update progress with callback"""
        self._current_progress = progress

        if callback:
            try:
                callback(
                    {
                        "progress": progress,
                        "message": message,
                        "timestamp": datetime.now(),
                    }
                )
            except Exception as e:
                logger.warning(f"Progress callback failed: {e}")

    def _log(
        self, message: str, level: str = "info", callback: Optional[Callable] = None
    ):
        """Log message with callback"""
        # Log to Python logger
        getattr(logger, level)(message)

        # Call GUI callback if provided
        if callback:
            try:
                callback(message, level)
            except Exception as e:
                logger.warning(f"Log callback failed: {e}")
