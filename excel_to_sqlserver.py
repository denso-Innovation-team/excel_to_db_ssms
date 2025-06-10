#!/usr/bin/env python3
"""
Excel to SQL Server - Main Script
Import Excel files to SQL Server 10.73.148.27
"""

import sys
import time
import pandas as pd
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.processors.excel_reader import ExcelReader
from src.processors.data_validator import DataValidator
from src.processors.database_writer import DatabaseWriter

def process_excel_file(excel_file: str, table_name: str, sheet_name: str = None):
    """Process Excel file to SQL Server"""
    
    print(f"🚀 Excel → SQL Server: {excel_file} → {table_name}")
    print("=" * 60)
    
    # Validate file
    if not Path(excel_file).exists():
        print(f"❌ File not found: {excel_file}")
        return False
    
    try:
        start_time = time.time()
        
        # Initialize processors
        reader = ExcelReader(excel_file, sheet_name)
        validator = DataValidator()
        writer = DatabaseWriter(table_name)
        
        # Get file info
        info = reader.get_sheet_info()
        print(f"📋 File: {info['total_rows']:,} rows, {len(info['columns'])} columns")
        print(f"📋 Columns: {info['columns'][:5]}{'...' if len(info['columns']) > 5 else ''}")
        
        # Auto-detect types
        type_mapping = auto_detect_types(info['columns'])
        print(f"📋 Type mapping: {len(type_mapping)} columns detected")
        
        # Process in chunks
        total_inserted = 0
        table_created = False
        
        for chunk_num, chunk in enumerate(reader.read_chunks(chunk_size=1000)):
            # Clean and validate
            df_clean = validator.clean_dataframe(chunk)
            df_typed = validator.validate_data_types(df_clean, type_mapping)
            
            # Create table on first chunk
            if not table_created:
                writer.create_table_from_dataframe(df_typed, type_mapping=type_mapping)
                table_created = True
                print(f"✅ Table '{table_name}' created")
            
            # Insert data
            rows_inserted = writer.bulk_insert_batch(df_typed)
            total_inserted += rows_inserted
            
            print(f"📊 Chunk {chunk_num + 1}: {total_inserted:,}/{info['total_rows']:,} rows")
        
        # Results
        processing_time = time.time() - start_time
        speed = total_inserted / processing_time if processing_time > 0 else 0
        
        print("\n🎉 Import Complete!")
        print("=" * 60)
        print(f"✅ Inserted: {total_inserted:,} rows")
        print(f"⏱️  Time: {processing_time:.2f} seconds")
        print(f"🚀 Speed: {speed:.0f} rows/second")
        print(f"\n🔗 Check in SSMS:")
        print(f"   Server: 10.73.148.27")
        print(f"   Database: ExcelImportDB")
        print(f"   Table: {table_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def auto_detect_types(columns):
    """Auto-detect data types from column names"""
    type_mapping = {}
    
    for col in columns:
        col_lower = col.lower()
        
        # Datetime patterns
        if any(p in col_lower for p in ['date', 'time', 'วันที่', 'เวลา']):
            type_mapping[col] = 'datetime'
        # Integer patterns
        elif any(p in col_lower for p in ['id', 'age', 'count', 'จำนวน', 'อายุ']):
            type_mapping[col] = 'integer'
        # Float patterns  
        elif any(p in col_lower for p in ['price', 'salary', 'amount', 'total', 'ราคา', 'เงินเดือน', 'ยอด']):
            type_mapping[col] = 'float'
        # Boolean patterns
        elif any(p in col_lower for p in ['active', 'enabled', 'is_', 'has_']):
            type_mapping[col] = 'boolean'
        # Default to string
        else:
            type_mapping[col] = 'string'
    
    return type_mapping

def main():
    if len(sys.argv) < 3:
        print("""
🎯 Excel to SQL Server Processor

Usage:
  python excel_to_sqlserver.py <excel_file> <table_name> [sheet_name]

Examples:
  python excel_to_sqlserver.py data.xlsx employees
  python excel_to_sqlserver.py sales.xlsx sales_data Sheet1
  python excel_to_sqlserver.py "path/data.xlsx" customer_data
        """)
        sys.exit(1)
    
    excel_file = sys.argv[1]
    table_name = sys.argv[2] 
    sheet_name = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Process file
    success = process_excel_file(excel_file, table_name, sheet_name)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
