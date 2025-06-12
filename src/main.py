#!/usr/bin/env python3
"""
Excel to SQL Server Main Processor
ระบบ import ข้อมูลจาก Excel เข้า SQL Server
"""

import sys
import time
from pathlib import Path
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from config.database import db_manager
from config.settings import settings
from processors.excel_reader import ExcelReader
from processors.data_validator import DataValidator
from processors.database_writer import DatabaseWriter


class ExcelToSQLServerProcessor:
    """Main processor class สำหรับ Excel → SQL Server"""

    def __init__(self, excel_file: str, table_name: str, sheet_name: str = None):
        self.excel_file = excel_file
        self.table_name = table_name
        self.sheet_name = sheet_name

        # Initialize components
        self.reader = ExcelReader(excel_file, sheet_name)
        self.validator = DataValidator()
        self.writer = DatabaseWriter(table_name)

        # Setup logging
        logging.basicConfig(
            level=getattr(logging, settings.LOG_LEVEL),
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger(__name__)

    def process(self, create_table: bool = True, type_mapping: dict = None) -> dict:
        """
        Main processing method

        Args:
            create_table: สร้างตารางใหม่หรือไม่
            type_mapping: การแมป data types

        Returns:
            dict: ผลลัพธ์การประมวลผล
        """
        start_time = time.time()

        try:
            # 1. Get file info
            info = self.reader.get_sheet_info()
            self.logger.info(
                f"Processing {info['total_rows']:,} rows from {self.excel_file}"
            )

            # 2. Auto-detect type mapping if not provided
            if not type_mapping:
                type_mapping = self._auto_detect_types(info["columns"])

            # 3. Process in chunks
            total_inserted = 0
            table_created = False

            for chunk_num, chunk in enumerate(
                self.reader.read_chunks(chunk_size=settings.CHUNK_SIZE)
            ):
                # Clean and validate data
                df_clean = self.validator.clean_dataframe(chunk)
                df_typed = self.validator.validate_data_types(df_clean, type_mapping)

                # Create table on first chunk
                if create_table and not table_created:
                    self.writer.create_table_from_dataframe(
                        df_typed, type_mapping=type_mapping
                    )
                    table_created = True

                # Insert data
                rows_inserted = self.writer.bulk_insert_batch(df_typed)
                total_inserted += rows_inserted

                self.logger.info(
                    f"Chunk {chunk_num + 1}: {total_inserted:,}/{info['total_rows']:,} rows processed"
                )

            # 4. Final results
            processing_time = time.time() - start_time

            results = {
                "success": True,
                "total_rows": info["total_rows"],
                "inserted_rows": total_inserted,
                "processing_time": processing_time,
                "speed_rows_per_sec": (
                    total_inserted / processing_time if processing_time > 0 else 0
                ),
                "table_name": self.table_name,
                "table_info": self.writer.get_table_info(),
            }

            self.logger.info(
                f"✅ SUCCESS: {total_inserted:,} rows in {processing_time:.2f}s"
            )
            return results

        except Exception as e:
            self.logger.error(f"❌ Processing failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "processing_time": time.time() - start_time,
            }

    def _auto_detect_types(self, columns: list) -> dict:
        """Auto-detect data types based on column names"""
        type_mapping = {}

        for col in columns:
            col_lower = col.lower()

            # Datetime patterns
            if any(pattern in col_lower for pattern in ["date", "time", "วันที่", "เวลา"]):
                type_mapping[col] = "datetime"
            # Integer patterns
            elif any(
                pattern in col_lower
                for pattern in ["id", "age", "count", "number", "จำนวน", "อายุ"]
            ):
                type_mapping[col] = "integer"
            # Float patterns
            elif any(
                pattern in col_lower
                for pattern in [
                    "price",
                    "salary",
                    "amount",
                    "total",
                    "ราคา",
                    "เงินเดือน",
                    "ยอด",
                ]
            ):
                type_mapping[col] = "float"
            # Boolean patterns
            elif any(
                pattern in col_lower for pattern in ["active", "enabled", "is_", "has_"]
            ):
                type_mapping[col] = "boolean"
            # Default to string
            else:
                type_mapping[col] = "string"

        return type_mapping


def main():
    """CLI สำหรับ Excel to SQL Server"""

    if len(sys.argv) < 3:
        print(
            """
🎯 Excel to SQL Server Processor

Usage:
  python src/main.py <excel_file> <table_name> [sheet_name]

Examples:
  python src/main.py data.xlsx employees
  python src/main.py sales.xlsx sales_data Sheet1
  python src/main.py "C:/path/data.xlsx" customer_data
        """
        )
        sys.exit(1)

    excel_file = sys.argv[1]
    table_name = sys.argv[2]
    sheet_name = sys.argv[3] if len(sys.argv) > 3 else None

    # Validate file exists
    if not Path(excel_file).exists():
        print(f"❌ File not found: {excel_file}")
        sys.exit(1)

    print(f"🚀 Excel to SQL Server: {excel_file} → {table_name}")
    print("=" * 60)

    # Test connection first
    print("🔍 Testing SQL Server connection...")
    if not db_manager.test_connection():
        print("❌ Cannot connect to SQL Server. Check your .env configuration.")
        sys.exit(1)
    print("✅ SQL Server connection OK")

    # Process
    processor = ExcelToSQLServerProcessor(excel_file, table_name, sheet_name)
    results = processor.process(create_table=True)

    if results["success"]:
        print("\n🎉 Processing Complete!")
        print("=" * 60)
        print(f"📋 Total rows: {results['total_rows']:,}")
        print(f"✅ Inserted: {results['inserted_rows']:,}")
        print(f"⏱️  Time: {results['processing_time']:.2f} seconds")
        print(f"🚀 Speed: {results['speed_rows_per_sec']:.0f} rows/second")
        print(f"\n🔗 Check in SQL Server Management Studio:")
        print(f"   Database: {settings.DB_NAME}")
        print(f"   Table: {table_name}")
    else:
        print(f"\n❌ Processing failed: {results['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
