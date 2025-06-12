#!/usr/bin/env python3
"""
Excel to SSMS - Hybrid Version (SQL Server + SQLite Fallback)
"""

import sys
from pathlib import Path
from tqdm import tqdm

from config import DatabaseConfig
from hybrid_database import HybridDatabaseManager
from excel_reader import ExcelReader
from data_cleaner import DataCleaner
from type_detector import TypeDetector


def main():
    if len(sys.argv) < 3:
        print(
            """
🎯 Excel to SSMS - Hybrid Version

Features:
  ✅ Primary: SQL Server
  ✅ Fallback: SQLite (auto-switch if SQL Server unavailable)
  ✅ Full compatibility with both databases

Usage:
  python excel_to_ssms.py <excel_file> <table_name> [sheet_name]

Examples:
  python excel_to_ssms.py data.xlsx employees
  python excel_to_ssms.py sales.xlsx sales_data Sheet1
        """
        )
        sys.exit(1)

    excel_file = sys.argv[1]
    table_name = sys.argv[2]
    sheet_name = sys.argv[3] if len(sys.argv) > 3 else None

    if not Path(excel_file).exists():
        print(f"❌ File not found: {excel_file}")
        sys.exit(1)

    # Load environment config
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        pass

    # Initialize hybrid components
    config = DatabaseConfig.from_env()
    db_manager = HybridDatabaseManager(config)
    reader = ExcelReader(excel_file, sheet_name)
    cleaner = DataCleaner()
    detector = TypeDetector()

    print(f"🚀 Excel to SSMS: {Path(excel_file).name} → {table_name}")
    print("=" * 60)

    # Connect with fallback logic
    if not db_manager.connect():
        print("❌ No database available (SQL Server or SQLite)")
        sys.exit(1)

    # Show active database
    status = db_manager.get_status()
    print(f"📊 Active Database: {status['active_database'].upper()}")

    if status["active_database"] == "sqlite":
        print(f"💾 SQLite File: {status['sqlite_fallback']}")
        print("💡 Data will be saved locally and can be migrated to SQL Server later")

    # Analyze file
    file_info = reader.get_info()
    print(
        f"📋 File: {file_info['total_rows']:,} rows, {file_info['file_size_mb']:.1f} MB"
    )

    # Auto-detect types
    type_mapping = detector.detect_types(file_info["columns"])

    # Process data
    total_inserted = 0
    table_created = False

    with tqdm(total=file_info["total_rows"], desc="Processing", unit="rows") as pbar:
        for chunk in reader.read_chunks(5000):
            # Clean and validate
            df_clean = cleaner.clean_dataframe(chunk)
            df_typed = cleaner.convert_types(df_clean, type_mapping)

            # Create table on first chunk
            if not table_created:
                db_manager.create_table_from_dataframe(
                    table_name, df_typed, type_mapping
                )
                table_created = True
                # First chunk is included in table creation
                total_inserted += len(df_typed)
            else:
                # Insert subsequent chunks
                rows_inserted = db_manager.bulk_insert(table_name, df_typed)
                total_inserted += rows_inserted

            pbar.update(len(chunk))
            pbar.set_postfix({"Inserted": f"{total_inserted:,}"})

    # Final results
    print(f"\n🎉 SUCCESS: {total_inserted:,} rows imported!")
    print(f"🎯 Database: {status['active_database'].upper()}")

    if status["active_database"] == "sqlite":
        print(f"\n📁 SQLite Database: {status['sqlite_fallback']}")
        print(f"🔍 Query data: sqlite3 {status['sqlite_fallback']}")
        print(f"   SELECT * FROM {table_name} LIMIT 10;")
        print(f"\n🔄 Migrate to SQL Server later:")
        print(f"   1. Fix SQL Server connection")
        print(f"   2. Export from SQLite: .dump {table_name}")
        print(f"   3. Import to SQL Server")
    else:
        print(f"\n🔗 SQL Server Table: {table_name}")
        print(f"📊 Connect with SSMS to view data")


if __name__ == "__main__":
    main()
