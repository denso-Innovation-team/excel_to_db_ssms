#!/usr/bin/env python3
"""
Excel to SSMS - Fixed Version
"""

import sys
import time
import pandas as pd
from pathlib import Path
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config.database import db_manager
from src.config.settings import settings
from src.processors.excel_reader import ExcelReader
from src.processors.data_validator import DataValidator
from src.processors.database_writer import DatabaseWriter
from src.utils.logger import setup_logger
from src.utils.progress import ProgressTracker


class ExcelToSSMSProcessor:
    """Fixed processor for Excel → SQL Server"""

    def __init__(self, excel_file: str, table_name: str, sheet_name: str = None):
        self.excel_file = Path(excel_file)
        self.table_name = table_name
        self.sheet_name = sheet_name

        # Setup logging
        self.logger = setup_logger()

        # Initialize processors
        self.reader = ExcelReader(str(self.excel_file), sheet_name)
        self.validator = DataValidator()
        self.writer = DatabaseWriter(table_name)

        # Performance metrics
        self.metrics = {
            "start_time": time.time(),
            "file_size_mb": self.excel_file.stat().st_size / (1024 * 1024),
            "total_rows": 0,
            "processed_rows": 0,
            "inserted_rows": 0,
            "failed_rows": 0,
            "processing_stages": {},
        }

    def validate_inputs(self) -> bool:
        """Validate input file and connection"""

        # Check file exists
        if not self.excel_file.exists():
            self.logger.error(f"❌ ไม่พบไฟล์: {self.excel_file}")
            return False

        # Check file format
        if self.excel_file.suffix.lower() not in [".xlsx", ".xls"]:
            self.logger.error("❌ ไฟล์ต้องเป็นรูปแบบ Excel (.xlsx หรือ .xls)")
            return False

        # Test database connection
        if not db_manager.test_connection():
            self.logger.error("❌ ไม่สามารถเชื่อมต่อ SQL Server ได้")
            return False

        return True

    def detect_column_types(self, columns: list) -> dict:
        """Auto-detect column data types from names"""
        type_mapping = {}

        patterns = {
            "datetime": ["date", "time", "วันที่", "เวลา", "created", "updated"],
            "integer": ["id", "age", "count", "number", "จำนวน", "อายุ"],
            "float": ["price", "salary", "amount", "total", "value", "ราคา", "เงินเดือน"],
            "boolean": ["active", "enabled", "is_", "has_", "flag"],
        }

        for column in columns:
            col_lower = column.lower()
            column_type = "string"  # default

            for data_type, pattern_list in patterns.items():
                if any(pattern in col_lower for pattern in pattern_list):
                    column_type = data_type
                    break

            type_mapping[column] = column_type

        return type_mapping

    def process(self, create_table: bool = True, type_mapping: dict = None) -> dict:
        """Fixed processing method"""

        self.logger.info(
            f"Starting process: {self.excel_file.name} → {self.table_name}"
        )

        try:
            # Stage 1: File Analysis
            stage_start = time.time()
            info = self.reader.get_sheet_info()
            self.metrics["total_rows"] = info["total_rows"]
            self.metrics["processing_stages"]["file_analysis"] = (
                time.time() - stage_start
            )

            self.logger.info(
                f"📊 ไฟล์: {info['total_rows']:,} แถว, {len(info['columns'])} คอลัมน์"
            )

            # Stage 2: Type Detection
            stage_start = time.time()
            if not type_mapping:
                type_mapping = self.detect_column_types(info["columns"])
            self.metrics["processing_stages"]["type_detection"] = (
                time.time() - stage_start
            )

            # Stage 3: Database Setup
            stage_start = time.time()
            if create_table:
                # Create table from first chunk sample
                first_chunk = next(self.reader.read_chunks(chunk_size=100))
                sample_df = self.validator.clean_dataframe(first_chunk)
                typed_df = self.validator.validate_data_types(sample_df, type_mapping)
                self.writer.create_table_from_dataframe(
                    typed_df, type_mapping=type_mapping
                )
                self.logger.info(f"✅ Created table '{self.table_name}'")

            self.metrics["processing_stages"]["database_setup"] = (
                time.time() - stage_start
            )

            # Stage 4: Data Processing - FIXED VERSION
            stage_start = time.time()

            # Reset reader to start from beginning
            self.reader = ExcelReader(str(self.excel_file), self.sheet_name)

            with ProgressTracker(
                total=self.metrics["total_rows"],
                description=f"Importing to {self.table_name}",
            ) as progress:

                # Sequential processing instead of parallel (more stable)
                for chunk in self.reader.read_chunks(chunk_size=settings.CHUNK_SIZE):
                    # Clean and validate data
                    clean_chunk = self.validator.clean_dataframe(chunk)
                    typed_chunk = self.validator.validate_data_types(
                        clean_chunk, type_mapping
                    )

                    # Single-threaded insert (more reliable)
                    try:
                        inserted = self.writer.bulk_insert_batch(typed_chunk)
                        self.metrics["inserted_rows"] += inserted
                        self.metrics["processed_rows"] += len(typed_chunk)

                        # Update progress
                        progress.update(len(typed_chunk))

                        # Calculate speed
                        elapsed = time.time() - self.metrics["start_time"]
                        speed = (
                            self.metrics["inserted_rows"] / elapsed
                            if elapsed > 0
                            else 0
                        )

                        progress.set_postfix(
                            {
                                "Speed": f"{speed:.0f} rows/s",
                                "Inserted": f"{self.metrics['inserted_rows']:,}",
                            }
                        )

                    except Exception as e:
                        self.logger.error(f"❌ Chunk insert failed: {e}")
                        self.metrics["failed_rows"] += len(typed_chunk)

            self.metrics["processing_stages"]["data_processing"] = (
                time.time() - stage_start
            )

            # Final calculations
            self.metrics["end_time"] = time.time()
            self.metrics["total_time"] = (
                self.metrics["end_time"] - self.metrics["start_time"]
            )
            self.metrics["rows_per_second"] = (
                self.metrics["inserted_rows"] / self.metrics["total_time"]
                if self.metrics["total_time"] > 0
                else 0
            )

            # Verification
            table_info = self.writer.get_table_info()

            # Success report
            self._print_success_report(table_info)

            return {"success": True, "metrics": self.metrics, "table_info": table_info}

        except Exception as e:
            self.logger.error(f"Processing failed: {e}")
            return {"success": False, "error": str(e), "metrics": self.metrics}

        finally:
            # Cleanup connections
            db_manager.cleanup_connections()

    def _print_success_report(self, table_info: dict):
        """Print detailed success report"""

        print("\n" + "=" * 60)
        print("🎉 การนำเข้าข้อมูลสำเร็จ!")
        print("=" * 60)

        # File info
        print(f"📁 ไฟล์: {self.excel_file.name} ({self.metrics['file_size_mb']:.1f} MB)")
        print(
            f"📊 ข้อมูล: {self.metrics['inserted_rows']:,} แถว จาก {self.metrics['total_rows']:,} แถว"
        )

        # Performance metrics
        success_rate = (
            self.metrics["inserted_rows"] / self.metrics["total_rows"]
        ) * 100
        print(f"✅ อัตราสำเร็จ: {success_rate:.1f}%")
        print(f"⏱️ เวลาทั้งหมด: {self.metrics['total_time']:.2f} วินาที")
        print(f"🚀 ความเร็ว: {self.metrics['rows_per_second']:.0f} แถว/วินาที")

        # Database info
        print(f"\n🗄️ ข้อมูลในฐานข้อมูล:")
        print(f"  • Database: {settings.DB_NAME}")
        print(f"  • Table: {self.table_name}")
        print(f"  • Rows in table: {table_info.get('row_count', 0):,}")


def main():
    """Main CLI function"""

    if len(sys.argv) < 3:
        print(
            """
🎯 Excel to SSMS - Fixed Version

Usage:
  python excel_to_ssms.py <excel_file> <table_name> [sheet_name]

Examples:
  python excel_to_ssms.py sales_50000.xlsx sales_data
        """
        )
        sys.exit(1)

    # Parse arguments
    excel_file = sys.argv[1]
    table_name = sys.argv[2]
    sheet_name = sys.argv[3] if len(sys.argv) > 3 else None

    # Create processor
    processor = ExcelToSSMSProcessor(excel_file, table_name, sheet_name)

    # Validate inputs
    if not processor.validate_inputs():
        sys.exit(1)

    # Process
    print(f"🚀 Excel to SSMS: {Path(excel_file).name} → {table_name}")
    print("=" * 60)

    results = processor.process(create_table=True)

    if results["success"]:
        print(f"\n💡 ตรวจสอบข้อมูลใน SSMS:")
        print(f"   Server: {settings.DB_HOST}")
        print(f"   Database: {settings.DB_NAME}")
        print(f"   Table: {table_name}")
    else:
        print(f"\n❌ การประมวลผลล้มเหลว: {results['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
