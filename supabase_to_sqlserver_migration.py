#!/usr/bin/env python3
"""
Custom SQL Server Configuration
ตั้งค่าสำหรับ SQL Server 10.73.148.27 เฉพาะของคุณ
"""

import os
from pathlib import Path


def create_custom_env():
    """สร้าง .env สำหรับ SQL Server ของคุณ"""
    env_content = """# SQL Server Configuration - TS00029
DB_HOST=10.73.148.27
DB_PORT=1433
DB_NAME=ExcelImportDB
DB_USER=TS00029
DB_PASSWORD=Thammaphon@TS00029
DB_TYPE=mssql
DB_DRIVER=ODBC Driver 17 for SQL Server

# Processing Configuration  
BATCH_SIZE=1000
MAX_WORKERS=4
CHUNK_SIZE=5000

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/excel_to_sqlserver.log
"""

    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_content)
    print("✅ สร้าง .env สำหรับ SQL Server 10.73.148.27")


def create_connection_test():
    """สร้าง test script เฉพาะสำหรับ server ของคุณ"""
    test_code = '''#!/usr/bin/env python3
"""
Connection Test for SQL Server 10.73.148.27
ทดสอบการเชื่อมต่อเฉพาะ server ของคุณ
"""

import pyodbc
import sys
from pathlib import Path

# Add src to path  
sys.path.insert(0, str(Path(__file__).parent))

def test_direct_connection():
    """ทดสอบการเชื่อมต่อโดยตรง"""
    print("🔍 Testing SQL Server 10.73.148.27...")
    
    try:
        # Connection string สำหรับ server ของคุณ
        conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=10.73.148.27,1433;"
            "DATABASE=master;"
            "UID=TS00029;"
            "PWD=Thammaphon@TS00029;"
            "TrustServerCertificate=yes;"
            "Encrypt=optional;"
        )
        
        conn = pyodbc.connect(conn_str, timeout=10)
        cursor = conn.cursor()
        
        # Basic info
        cursor.execute("SELECT @@VERSION, @@SERVERNAME, DB_NAME()")
        version, server, current_db = cursor.fetchone()
        
        print(f"✅ Connected to {server}")
        print(f"📋 Database: {current_db}")
        print(f"📋 Version: {version.split('\\n')[0]}")
        
        # List databases
        cursor.execute("""
            SELECT name FROM sys.databases 
            WHERE name NOT IN ('master', 'tempdb', 'model', 'msdb')
            ORDER BY name
        """)
        databases = [row[0] for row in cursor.fetchall()]
        print(f"📋 User Databases: {databases}")
        
        # Check/Create ExcelImportDB
        cursor.execute("SELECT name FROM sys.databases WHERE name = 'ExcelImportDB'")
        if not cursor.fetchone():
            print("📋 Creating ExcelImportDB...")
            cursor.execute("CREATE DATABASE ExcelImportDB")
            conn.commit()
            print("✅ Database ExcelImportDB created")
        else:
            print("✅ Database ExcelImportDB exists")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        
        if "Login failed" in str(e):
            print("💡 ตรวจสอบ username/password")
        elif "network-related" in str(e).lower():
            print("💡 ตรวจสอบ network และ firewall")
        elif "driver" in str(e).lower():
            print("💡 ติดตั้ง ODBC Driver 17 for SQL Server")
            
        return False

def test_sqlalchemy():
    """ทดสอบ SQLAlchemy"""
    try:
        from src.config.database import db_manager
        
        print("\\n🔍 Testing SQLAlchemy connection...")
        
        if db_manager.test_connection():
            print("✅ SQLAlchemy connection OK")
            
            info = db_manager.get_server_info()
            if "error" not in info:
                print(f"📋 Available databases: {info.get('databases', [])}")
            
            return True
        else:
            print("❌ SQLAlchemy connection failed")
            return False
            
    except Exception as e:
        print(f"❌ SQLAlchemy error: {e}")
        return False

def quick_excel_test():
    """ทดสอบ import Excel เล็กๆ"""
    try:
        import pandas as pd
        from src.processors.excel_reader import ExcelReader
        from src.processors.data_validator import DataValidator  
        from src.processors.database_writer import DatabaseWriter
        
        print("\\n🚀 Quick Excel Import Test...")
        
        # สร้างข้อมูลทดสอบ
        test_data = {
            'Name': ['สมชาย ใจดี', 'สมหญิง รักดี', 'วิชัย เจริญ'],
            'Age': [25, 30, 35],
            'Salary': [50000.0, 75000.0, 85000.0],
            'Department': ['IT', 'การตลาด', 'บัญชี'],
            'JoinDate': ['2023-01-15', '2023-02-20', '2023-03-10']
        }
        
        df = pd.DataFrame(test_data)
        test_file = 'quick_test.xlsx'
        df.to_excel(test_file, index=False)
        
        # Import process
        reader = ExcelReader(test_file)
        validator = DataValidator()
        writer = DatabaseWriter("quick_test")
        
        # Type mapping
        type_mapping = {
            "name": "string",
            "age": "integer",
            "salary": "float", 
            "department": "string",
            "joindate": "datetime"
        }
        
        # Process
        df_raw = pd.read_excel(test_file)
        df_clean = validator.clean_dataframe(df_raw)
        df_typed = validator.validate_data_types(df_clean, type_mapping)
        
        # Create table & insert
        writer.create_table_from_dataframe(df_typed, type_mapping=type_mapping)
        rows = writer.bulk_insert_batch(df_typed)
        
        print(f"✅ Imported {rows} rows to table 'quick_test'")
        
        # Cleanup
        os.remove(test_file)
        
        print("🎉 Excel import test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Excel test failed: {e}")
        return False

def main():
    print("🎯 SQL Server Connection Test - TS00029")
    print("=" * 50)
    
    # Test 1: Direct connection
    if not test_direct_connection():
        return
    
    # Test 2: SQLAlchemy  
    if not test_sqlalchemy():
        return
        
    # Test 3: Excel import
    if not quick_excel_test():
        return
    
    print("\\n🎉 All Tests Passed!")
    print("🚀 Ready to process Excel files")
    print("\\n📋 Usage:")
    print("  python excel_to_sqlserver.py data.xlsx table_name")

if __name__ == "__main__":
    main()
'''

    with open("test_your_server.py", "w", encoding="utf-8") as f:
        f.write(test_code)
    print("✅ สร้าง test_your_server.py")


def create_main_script():
    """สร้าง main script สำหรับ Excel import"""
    main_code = '''#!/usr/bin/env python3
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
        
        print("\\n🎉 Import Complete!")
        print("=" * 60)
        print(f"✅ Inserted: {total_inserted:,} rows")
        print(f"⏱️  Time: {processing_time:.2f} seconds")
        print(f"🚀 Speed: {speed:.0f} rows/second")
        print(f"\\n🔗 Check in SSMS:")
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
'''

    with open("excel_to_sqlserver.py", "w", encoding="utf-8") as f:
        f.write(main_code)
    print("✅ สร้าง excel_to_sqlserver.py")


def main():
    """Setup สำหรับ SQL Server ของคุณ"""
    print("🎯 Custom SQL Server Setup - TS00029")
    print("=" * 50)

    # Create directories
    Path("logs").mkdir(exist_ok=True)

    # Create files
    create_custom_env()
    create_connection_test()
    create_main_script()

    print("\n✅ Setup Complete!")
    print("=" * 50)
    print("📋 Next Steps:")
    print("  1. python test_your_server.py")
    print("  2. python excel_to_sqlserver.py your_file.xlsx table_name")

    print("\n🔗 Your SQL Server:")
    print("  Server: 10.73.148.27")
    print("  User: TS00029")
    print("  Database: ExcelImportDB (will be created)")


if __name__ == "__main__":
    main()
