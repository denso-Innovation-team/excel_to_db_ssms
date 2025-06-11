#!/usr/bin/env python3
"""
SQL Server Connection Tester
ทดสอบการเชื่อมต่อ SQL Server และระบบ Excel import
"""

import sys
import os
import time
import pandas as pd
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))


def test_packages():
    """ทดสอบ packages ที่จำเป็น"""
    print("📦 ทดสอบ Python packages...")

    required_packages = [
        ("pandas", "pandas"),
        ("sqlalchemy", "sqlalchemy"),
        ("openpyxl", "openpyxl"),
        ("pyodbc", "pyodbc"),
        ("python-dotenv", "dotenv"),
        ("tqdm", "tqdm"),
    ]

    missing_packages = []

    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"  ✅ {package_name}")
        except ImportError:
            print(f"  ❌ {package_name} - ไม่พบ")
            missing_packages.append(package_name)

    if missing_packages:
        print(f"\n❌ ต้องติดตั้ง packages: {', '.join(missing_packages)}")
        print("🔧 คำสั่งติดตั้ง:")
        for package in missing_packages:
            print(f"  pip install {package}")
        return False

    print("✅ ทุก packages พร้อมใช้งาน")
    return True


def test_direct_connection():
    """ทดสอบการเชื่อมต่อโดยตรงด้วย pyodbc"""
    print("\n🔍 ทดสอบการเชื่อมต่อ SQL Server โดยตรง...")

    try:
        import pyodbc

        # Connection string for your server
        conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=10.73.148.27;"
            "DATABASE=master;"
            "UID=TS00029;"
            "PWD=Thammaphon@TS00029;"
            "TrustServerCertificate=yes;"
            "Encrypt=no;TrustServerCertificate=yes;"
            "Timeout=30;"
        )

        start_time = time.time()
        conn = pyodbc.connect(conn_str)
        connection_time = time.time() - start_time

        cursor = conn.cursor()

        # Server info
        cursor.execute("SELECT @@VERSION, @@SERVERNAME, DB_NAME()")
        version, server_name, current_db = cursor.fetchone()

        print(f"  ✅ เชื่อมต่อสำเร็จ ({connection_time:.2f}s)")
        print(f"  📋 Server: {server_name}")
        print(f"  📋 Database: {current_db}")
        print(f"  📋 Version: {version.split()[3]}")

        # Check databases
        cursor.execute(
            """
            SELECT name FROM sys.databases 
            WHERE name NOT IN ('master', 'tempdb', 'model', 'msdb')
            ORDER BY name
        """
        )
        user_databases = [row[0] for row in cursor.fetchall()]
        print(f"  📋 User Databases: {user_databases}")

        # Create excel_to_db if not exists
        cursor.execute("SELECT name FROM sys.databases WHERE name = 'excel_to_db'")
        if not cursor.fetchone():
            print("  📋 สร้าง database excel_to_db...")
            cursor.execute("CREATE DATABASE excel_to_db")
            conn.commit()
            print("  ✅ สร้าง database สำเร็จ")
        else:
            print("  ✅ Database excel_to_db มีอยู่แล้ว")

        conn.close()
        return True

    except Exception as e:
        print(f"  ❌ การเชื่อมต่อล้มเหลว: {e}")

        error_str = str(e).lower()
        if "login failed" in error_str:
            print("  💡 ตรวจสอบ username/password ใน .env")
        elif "network" in error_str or "timeout" in error_str:
            print("  💡 ตรวจสอบ network connectivity และ firewall")
        elif "driver" in error_str:
            print("  💡 ติดตั้ง ODBC Driver 17 for SQL Server")

        return False


def test_sqlalchemy_pool():
    """ทดสอบ SQLAlchemy และ connection pool"""
    print("\n🔍 ทดสอบ SQLAlchemy connection pool...")

    try:
        from src.config.database import db_manager
        from src.config.settings import settings

        # Test basic connection
        if not db_manager.test_connection():
            print("  ❌ SQLAlchemy connection ล้มเหลว")
            return False

        # Pool information
        pool_status = db_manager.get_pool_status()
        print(f"  ✅ Connection pool พร้อมใช้งาน")
        print(f"  📋 Pool size: {pool_status['pool_size']}")
        print(f"  📋 Total connections: {pool_status['total_connections']}")
        print(f"  📋 Available: {pool_status['checked_in']}")

        # Performance test
        start_time = time.time()
        for i in range(5):
            db_manager.test_connection()
        pool_test_time = time.time() - start_time

        print(f"  ✅ Pool performance test: {pool_test_time:.3f}s (5 connections)")

        return True

    except Exception as e:
        print(f"  ❌ SQLAlchemy error: {e}")
        return False


def test_excel_processing():
    """ทดสอบการประมวลผล Excel"""
    print("\n🔍 ทดสอบการประมวลผล Excel...")

    try:
        from src.processors.excel_reader import ExcelReader
        from src.processors.data_validator import DataValidator
        from src.processors.database_writer import DatabaseWriter

        # สร้างข้อมูลทดสอบ
        test_data = {
            "EmployeeID": ["EMP001", "EMP002", "EMP003"],
            "Name": ["สมชาย ใจดี", "สมหญิง รักดี", "วิชัย เจริญ"],
            "Age": [25, 30, 35],
            "Salary": [50000.0, 75000.0, 85000.0],
            "Department": ["IT", "การตลาด", "บัญชี"],
            "JoinDate": ["2023-01-15", "2023-02-20", "2023-03-10"],
            "IsActive": [True, True, False],
        }

        df = pd.DataFrame(test_data)
        test_file = "connection_test.xlsx"
        df.to_excel(test_file, index=False)
        print(f"  ✅ สร้างไฟล์ทดสอบ: {test_file}")

        # Type mapping
        type_mapping = {
            "employeeid": "string",
            "name": "string",
            "age": "integer",
            "salary": "float",
            "department": "string",
            "joindate": "datetime",
            "isactive": "boolean",
        }

        # Process
        start_time = time.time()

        reader = ExcelReader(test_file)
        validator = DataValidator()
        writer = DatabaseWriter("connection_test")

        # Read and process
        df_raw = pd.read_excel(test_file)
        df_clean = validator.clean_dataframe(df_raw)
        df_typed = validator.validate_data_types(df_clean, type_mapping)

        # Create table and insert
        writer.create_table_from_dataframe(df_typed, type_mapping=type_mapping)
        rows_inserted = writer.bulk_insert_batch(df_typed)

        processing_time = time.time() - start_time

        print(f"  ✅ ประมวลผลสำเร็จ: {rows_inserted} แถว ({processing_time:.2f}s)")

        # Verify data
        table_info = writer.get_table_info()
        print(f"  ✅ ตาราง 'connection_test' มี {table_info.get('row_count', 0)} แถว")

        # Cleanup
        os.remove(test_file)
        print("  ✅ ลบไฟล์ทดสอบแล้ว")

        return True

    except Exception as e:
        print(f"  ❌ Excel processing error: {e}")
        if os.path.exists("connection_test.xlsx"):
            os.remove("connection_test.xlsx")
        return False


def test_performance():
    """ทดสอบประสิทธิภาพระบบ"""
    print("\n🔍 ทดสอบประสิทธิภาพระบบ...")

    try:
        from src.config.settings import settings

        # Configuration check
        print(f"  📋 Batch size: {settings.BATCH_SIZE}")
        print(f"  📋 Max workers: {settings.MAX_WORKERS}")
        print(f"  📋 Chunk size: {settings.CHUNK_SIZE}")
        print(f"  📋 Pool size: {settings.POOL_SIZE}")

        # Memory test (สร้างข้อมูลขนาดกลาง)
        import numpy as np

        print("  🔍 ทดสอบ memory handling...")
        large_data = np.random.rand(settings.CHUNK_SIZE, 5)
        df_test = pd.DataFrame(large_data, columns=["A", "B", "C", "D", "E"])

        # Memory usage
        memory_usage = df_test.memory_usage(deep=True).sum() / 1024 / 1024
        print(
            f"  ✅ Memory test: {memory_usage:.1f} MB for {settings.CHUNK_SIZE:,} rows"
        )

        # CPU cores
        import multiprocessing

        cpu_cores = multiprocessing.cpu_count()
        print(f"  📋 Available CPU cores: {cpu_cores}")

        if settings.MAX_WORKERS > cpu_cores:
            print(f"  ⚠️ MAX_WORKERS ({settings.MAX_WORKERS}) > CPU cores ({cpu_cores})")
        else:
            print(f"  ✅ Worker configuration optimized")

        del large_data, df_test  # Free memory

        return True

    except Exception as e:
        print(f"  ❌ Performance test error: {e}")
        return False


def main():
    """Main test function"""

    print("🎯 Excel to SSMS - Connection & System Test")
    print("=" * 60)

    # Test results
    tests = [
        ("Python Packages", test_packages),
        ("Direct SQL Connection", test_direct_connection),
        ("SQLAlchemy Pool", test_sqlalchemy_pool),
        ("Excel Processing", test_excel_processing),
        ("System Performance", test_performance),
    ]

    passed_tests = 0
    total_tests = len(tests)

    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")

        try:
            if test_func():
                passed_tests += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")

    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Test Summary: {passed_tests}/{total_tests} tests passed")

    if passed_tests == total_tests:
        print("🎉 ระบบพร้อมใช้งาน 100%!")
        print("\n🚀 การใช้งาน:")
        print("  python excel_to_ssms.py your_file.xlsx table_name")
        print("\n💡 ตรวจสอบผลลัพธ์ใน SSMS:")
        print("  Server: 10.73.148.27")
        print("  Database: excel_to_db")
    else:
        failed_tests = total_tests - passed_tests
        print(f"⚠️ มี {failed_tests} tests ที่ล้มเหลว")
        print("💡 แก้ไขปัญหาก่อนใช้งาน")

        if passed_tests == 0:
            print("\n🔧 เริ่มต้นแก้ไข:")
            print("  1. pip install -r requirements.txt")
            print("  2. ตรวจสอบ .env file")
            print("  3. ติดตั้ง ODBC Driver 17 for SQL Server")


if __name__ == "__main__":
    main()
