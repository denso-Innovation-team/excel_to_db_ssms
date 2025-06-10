#!/usr/bin/env python3
"""
SQL Server Test Runner for Excel Import
ทดสอบการ import ข้อมูลเข้า SQL Server
"""

import sys
import os
from pathlib import Path
import pandas as pd
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def test_connection():
    """ทดสอบการเชื่อมต่อ SQL Server"""
    try:
        from src.config.database import db_manager
        
        print("🔍 ทดสอบการเชื่อมต่อ SQL Server...")
        
        if db_manager.test_connection():
            print("✅ เชื่อมต่อ SQL Server สำเร็จ")
            return True
        else:
            print("❌ ไม่สามารถเชื่อมต่อ SQL Server ได้")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def quick_test():
    """ทดสอบเร็วด้วยข้อมูลง่ายๆ"""
    
    print("🚀 Quick Test: Excel → SQL Server")
    print("=" * 40)
    
    # ทดสอบการเชื่อมต่อก่อน
    if not test_connection():
        print("💡 ตรวจสอบ:")
        print("  1. SQL Server ทำงานอยู่หรือไม่")
        print("  2. ข้อมูลใน .env ถูกต้องหรือไม่")
        print("  3. pip install pyodbc pymssql")
        return False
    
    # สร้างข้อมูลทดสอบ
    test_data = {
        'Name': ['John Doe', 'Jane Smith', 'Bob Wilson', 'Alice Brown'],
        'Age': [25, 30, 35, 28], 
        'Email': ['john@test.com', 'jane@test.com', 'bob@test.com', 'alice@test.com'],
        'Salary': [50000.0, 75000.0, 85000.0, 60000.0],
        'Active': [True, True, False, True],
        'JoinDate': ['2023-01-15', '2023-02-20', '2023-03-10', '2023-04-05']
    }
    
    df = pd.DataFrame(test_data)
    test_file = 'quick_test.xlsx'
    df.to_excel(test_file, index=False)
    print(f"✅ สร้างไฟล์ทดสอบ: {test_file}")
    
    # Import to SQL Server
    try:
        from src.processors.excel_reader import ExcelReader
        from src.processors.data_validator import DataValidator
        from src.processors.database_writer import DatabaseWriter
        
        # Type mapping
        type_mapping = {
            "name": "string",
            "age": "integer", 
            "email": "string",
            "salary": "float",
            "active": "boolean",
            "joindate": "datetime"
        }
        
        # Process
        reader = ExcelReader(test_file)
        validator = DataValidator()
        writer = DatabaseWriter("quick_test")
        
        # Read and clean data
        df_raw = pd.read_excel(test_file)
        df_clean = validator.clean_dataframe(df_raw)
        df_typed = validator.validate_data_types(df_clean, type_mapping)
        
        # Create table and insert
        writer.create_table_from_dataframe(df_typed, type_mapping=type_mapping)
        rows_inserted = writer.bulk_insert_batch(df_typed)
        
        print("\n" + "="*40)
        print("🎉 SUCCESS!")
        print("="*40) 
        print(f"📊 Import สำเร็จ: {rows_inserted} แถว")
        print(f"\n🔗 ตรวจสอบใน SQL Server:")
        print(f"   → SQL Server Management Studio")
        print(f"   → Database: ExcelImportDB")
        print(f"   → Table: quick_test")
        
        # ลบไฟล์ทดสอบ
        os.remove(test_file)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_with_file(excel_file: str, table_name: str, sheet_name: str = None):
    """ทดสอบกับไฟล์ที่ระบุ"""
    
    print(f"🚀 Testing: {excel_file} → {table_name}")
    print("=" * 50)
    
    if not test_connection():
        return False
    
    # Auto-detect type mapping
    type_mapping = {
        # Thai columns
        "ชื่อ": "string", "นามสกุล": "string", "อายุ": "integer",
        "เงินเดือน": "float", "วันที่": "datetime", "วันที่เริ่มงาน": "datetime",
        "จำนวน": "integer", "ราคา": "float", "ยอดรวม": "float", "สถานะ": "string",
        
        # English columns  
        "name": "string", "email": "string", "age": "integer", 
        "salary": "float", "amount": "float", "price": "float",
        "total": "float", "date": "datetime", "created_at": "datetime",
        "is_active": "boolean", "active": "boolean"
    }
    
    try:
        from src.processors.excel_reader import ExcelReader
        from src.processors.data_validator import DataValidator
        from src.processors.database_writer import DatabaseWriter
        
        # Process
        reader = ExcelReader(excel_file, sheet_name)
        info = reader.get_sheet_info()
        validator = DataValidator()
        writer = DatabaseWriter(table_name)
        
        print(f"📋 ไฟล์: {info['total_rows']:,} แถว, {len(info['columns'])} คอลัมน์")
        
        # Process in chunks
        total_inserted = 0
        for chunk in reader.read_chunks(chunk_size=1000):
            df_clean = validator.clean_dataframe(chunk)
            df_typed = validator.validate_data_types(df_clean, type_mapping)
            
            if total_inserted == 0:
                # Create table on first chunk
                writer.create_table_from_dataframe(df_typed, type_mapping=type_mapping)
            
            rows = writer.bulk_insert_batch(df_typed)
            total_inserted += rows
            print(f"    📊 Processed: {total_inserted:,}/{info['total_rows']:,} rows")
        
        print("\n" + "="*50)
        print("🎉 SUCCESS!")
        print("="*50)
        print(f"✅ Import: {total_inserted:,} แถว") 
        print(f"\n🔗 ตรวจสอบใน SQL Server:")
        print(f"   → SSMS → ExcelImportDB → Tables → {table_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main CLI"""
    
    if len(sys.argv) == 1:
        quick_test()
        
    elif len(sys.argv) == 2 and sys.argv[1] == "test":
        quick_test()
        
    elif len(sys.argv) == 2 and sys.argv[1] == "connect":
        test_connection()
        
    elif len(sys.argv) >= 3:
        excel_file = sys.argv[1]
        table_name = sys.argv[2]
        sheet_name = sys.argv[3] if len(sys.argv) > 3 else None
        
        if not os.path.exists(excel_file):
            print(f"❌ ไม่พบไฟล์: {excel_file}")
            sys.exit(1)
            
        test_with_file(excel_file, table_name, sheet_name)
        
    else:
        print("""
🎯 Excel to SQL Server Test Runner

Usage:
  python test_sqlserver.py                           # Quick test
  python test_sqlserver.py test                      # Quick test
  python test_sqlserver.py connect                   # Test connection only
  python test_sqlserver.py <file.xlsx> <table_name>  # Custom test
  python test_sqlserver.py <file.xlsx> <table_name> <sheet_name>  # With sheet

Examples:
  python test_sqlserver.py                                    # ทดสอบเร็ว
  python test_sqlserver.py connect                            # ทดสอบการเชื่อมต่อ
  python test_sqlserver.py data/samples/sales_1000.xlsx sales # ทดสอบไฟล์ยอดขาย
  python test_sqlserver.py data.xlsx employees Employees      # ระบุ sheet
        """)

if __name__ == "__main__":
    main()
