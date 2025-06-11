#!/usr/bin/env python3
"""
Excel to SSMS - Main CLI Interface
นำเข้าข้อมูลจาก Excel เข้า SQL Server Management Studio อย่างมีประสิทธิภาพ
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
    """Main processor for Excel → SQL Server with connection pooling"""

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
            print("\n💡 แนวทางแก้ไข:")
            print("  1. ตรวจสอบ SQL Server ทำงานอยู่หรือไม่")
            print("  2. ตรวจสอบข้อมูลใน .env file")
            print("  3. ติดตั้ง ODBC Driver 17 for SQL Server")
            print("  4. รัน: python test_connection.py")
            return False

        return True

    def detect_column_types(self, columns: list) -> dict:
        """Auto-detect column data types from names"""
        type_mapping = {}

        # Thai and English patterns
        patterns = {
            "datetime": ["date", "time", "วันที่", "เวลา", "created", "updated", "join"],
            "integer": ["id", "age", "count", "number", "จำนวน", "อายุ", "เลขที่"],
            "float": [
                "price",
                "salary",
                "amount",
                "total",
                "value",
                "ราคา",
                "เงินเดือน",
                "ยอด",
                "จำนวนเงิน",
            ],
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
        """Main processing method with optimized performance"""

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

            self.logger.info(f"Type detection: {len(type_mapping)} คอลัมน์")

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
                self.logger.info(f"Created table '{self.table_name}' เรียบร้อย")

            self.metrics["processing_stages"]["database_setup"] = (
                time.time() - stage_start
            )

            # Stage 4: Data Processing with Progress Tracking
            stage_start = time.time()

            with ProgressTracker(
                total=self.metrics["total_rows"],
                description=f"Importing to {self.table_name}",
            ) as progress:

                # Process in optimized chunks
                batch_chunks = []
                chunk_count = 0

                for chunk in self.reader.read_chunks(chunk_size=settings.CHUNK_SIZE):
                    chunk_count += 1

                    # Clean and validate data
                    clean_chunk = self.validator.clean_dataframe(chunk)
                    typed_chunk = self.validator.validate_data_types(
                        clean_chunk, type_mapping
                    )

                    batch_chunks.append(typed_chunk)
                    self.metrics["processed_rows"] += len(typed_chunk)

                    # Process batches in parallel when we have enough chunks
                    if len(batch_chunks) >= settings.MAX_WORKERS:
                        inserted = self.writer.parallel_insert(batch_chunks)
                        self.metrics["inserted_rows"] += inserted

                        # Update progress
                        progress.update(sum(len(chunk) for chunk in batch_chunks))
                        progress.set_postfix(
                            {
                                "Speed": f"{inserted/settings.CHUNK_SIZE:.0f} rows/s",
                                "Pool": str(
                                    db_manager.get_pool_status()["checked_out"]
                                ),
                            }
                        )

                        batch_chunks = []

                # Process remaining chunks
                if batch_chunks:
                    inserted = self.writer.parallel_insert(batch_chunks)
                    self.metrics["inserted_rows"] += inserted
                    progress.update(sum(len(chunk) for chunk in batch_chunks))

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

        # Stage breakdown
        print(f"\n📈 การแบ่งเวลาตามขั้นตอน:")
        for stage, duration in self.metrics["processing_stages"].items():
            percentage = (duration / self.metrics["total_time"]) * 100
            print(f"  • {stage}: {duration:.2f}s ({percentage:.1f}%)")

        # Database info
        print(f"\n🗄️ ข้อมูลในฐานข้อมูล:")
        print(f"  • Database: {settings.DB_NAME}")
        print(f"  • Table: {self.table_name}")
        print(f"  • Rows in table: {table_info.get('row_count', 0):,}")

        # Connection pool status
        pool_status = db_manager.get_pool_status()
        print(f"\n🔗 Connection Pool Status:")
        print(f"  • Total connections: {pool_status['total_connections']}")
        print(f"  • Active: {pool_status['checked_out']}")
        print(f"  • Available: {pool_status['checked_in']}")


def main():
    """Main CLI function"""

    if len(sys.argv) < 3:
        print(
            """
🎯 Excel to SSMS - Advanced Excel Import System

Usage:
  python excel_to_ssms.py <excel_file> <table_name> [sheet_name]

Examples:
  python excel_to_ssms.py data.xlsx employees
  python excel_to_ssms.py sales.xlsx sales_data "Sheet1"
  python excel_to_ssms.py "C:/path/data.xlsx" customer_data

Features:
  ✅ Connection pooling สำหรับประสิทธิภาพสูง
  ✅ Parallel processing หลาย threads
  ✅ Auto-detect column types (Thai/English)
  ✅ Progress tracking แบบ real-time
  ✅ Error handling ครอบคลุม
  ✅ Unicode support (ภาษาไทย)

Requirements:
  • SQL Server พร้อม SSMS
  • ODBC Driver 17 for SQL Server
  • Python packages ตาม requirements.txt
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

    # Process with performance monitoring
    print(f"🚀 Excel to SSMS: {Path(excel_file).name} → {table_name}")
    print("=" * 60)

    # Show pool status
    pool_status = db_manager.get_pool_status()
    print(f"🔗 Connection Pool: {pool_status['total_connections']} connections ready")

    # Process
    results = processor.process(create_table=True)

    if results["success"]:
        print(f"\n💡 ตรวจสอบข้อมูลใน SSMS:")
        print(f"   1. เปิด SQL Server Management Studio")
        print(f"   2. Connect to: {settings.DB_HOST}")
        print(f"   3. Database: {settings.DB_NAME}")
        print(f"   4. Tables → {table_name}")
        print(f"   5. Right-click → Select Top 1000 Rows")
    else:
        print(f"\n❌ การประมวลผลล้มเหลว: {results['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
