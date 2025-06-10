#!/usr/bin/env python3
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
        print(f"📋 Version: {version.split('\n')[0]}")

        # List databases
        cursor.execute(
            """
            SELECT name FROM sys.databases 
            WHERE name NOT IN ('master', 'tempdb', 'model', 'msdb')
            ORDER BY name
        """
        )
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

        print("\n🔍 Testing SQLAlchemy connection...")

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

        print("\n🚀 Quick Excel Import Test...")

        # สร้างข้อมูลทดสอบ
        test_data = {
            "Name": ["สมชาย ใจดี", "สมหญิง รักดี", "วิชัย เจริญ"],
            "Age": [25, 30, 35],
            "Salary": [50000.0, 75000.0, 85000.0],
            "Department": ["IT", "การตลาด", "บัญชี"],
            "JoinDate": ["2023-01-15", "2023-02-20", "2023-03-10"],
        }

        df = pd.DataFrame(test_data)
        test_file = "quick_test.xlsx"
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
            "joindate": "datetime",
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

    print("\n🎉 All Tests Passed!")
    print("🚀 Ready to process Excel files")
    print("\n📋 Usage:")
    print("  python excel_to_sqlserver.py data.xlsx table_name")


if __name__ == "__main__":
    main()
