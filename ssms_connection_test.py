#!/usr/bin/env python3
"""
SSMS Named Instance Connection Test
ทดสอบเชื่อมต่อตาม Connection Properties จาก SSMS
"""

import pyodbc
import time


def test_named_instance():
    """ทดสอบ Named Instance: 10.73.148.27\MSSQL2S"""

    print("🎯 Testing SSMS Named Instance Connection")
    print("=" * 50)

    connection_formats = [
        # Format 1: Named Instance (ตามภาพ SSMS)
        (
            "Named Instance (SSMS Format)",
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=10.73.148.27\\MSSQL2S;"
            "DATABASE=master;"
            "UID=TS00029;"
            "PWD=Thammaphon@TS00029;"
            "TrustServerCertificate=yes;"
            "Encrypt=no;",
        ),
        # Format 2: ใช้ CAS_Development (ตามภาพ)
        (
            "CAS_Development (From SSMS)",
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=10.73.148.27\\MSSQL2S;"
            "DATABASE=CAS_Development;"
            "UID=TS00029;"
            "PWD=Thammaphon@TS00029;"
            "TrustServerCertificate=yes;"
            "Encrypt=no;",
        ),
        # Format 3: TCP Port ถ้า Named Instance ไม่ได้
        (
            "TCP Port Alternative",
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=10.73.148.27,1433;"
            "DATABASE=master;"
            "UID=TS00029;"
            "PWD=Thammaphon@TS00029;"
            "TrustServerCertificate=yes;"
            "Encrypt=no;",
        ),
    ]

    working_connections = []

    for format_name, conn_str in connection_formats:
        print(f"\n🔍 Testing: {format_name}")
        print("-" * 30)

        try:
            start_time = time.time()
            conn = pyodbc.connect(conn_str, timeout=15)
            connection_time = time.time() - start_time

            cursor = conn.cursor()

            # Get server info
            cursor.execute(
                """
                SELECT 
                    @@SERVERNAME as ServerName,
                    @@VERSION as Version,
                    DB_NAME() as CurrentDB,
                    SERVERPROPERTY('InstanceName') as InstanceName,
                    SERVERPROPERTY('ServerName') as ServerName2
            """
            )

            result = cursor.fetchone()
            server_name = result[0]
            version = result[1]
            current_db = result[2]
            instance_name = result[3] or "Default Instance"

            print(f"  ✅ SUCCESS ({connection_time:.2f}s)")
            print(f"  📋 Server: {server_name}")
            print(f"  📋 Instance: {instance_name}")
            print(f"  📋 Database: {current_db}")
            print(
                f"  📋 Version: {version.split()[3] if len(version.split()) > 3 else 'Unknown'}"
            )

            # Test database operations
            cursor.execute("SELECT COUNT(*) FROM sys.databases")
            db_count = cursor.fetchone()[0]
            print(f"  📋 Available Databases: {db_count}")

            # List some databases
            cursor.execute(
                """
                SELECT TOP 5 name FROM sys.databases 
                WHERE name NOT IN ('master', 'tempdb', 'model', 'msdb')
                ORDER BY name
            """
            )
            user_dbs = [row[0] for row in cursor.fetchall()]
            if user_dbs:
                print(f"  📋 User DBs: {', '.join(user_dbs)}")

            conn.close()
            working_connections.append((format_name, conn_str))

            # หยุดทดสอบเมื่อเจอตัวแรกที่ใช้ได้
            break

        except Exception as e:
            print(f"  ❌ FAILED: {e}")

            # Analyze error type
            error_str = str(e).lower()
            if "login failed" in error_str:
                print("  💡 Hint: ตรวจสอบ username/password")
            elif "network" in error_str or "timeout" in error_str:
                print("  💡 Hint: ตรวจสอบ network/firewall")
            elif "instance" in error_str:
                print("  💡 Hint: Named instance อาจไม่ถูกต้อง")
            elif "driver" in error_str:
                print("  💡 Hint: ติดตั้ง ODBC Driver 17")

    return working_connections


def test_sqlalchemy_with_working_connection(conn_str):
    """ทดสอบ SQLAlchemy ด้วย connection ที่ใช้งานได้"""

    print(f"\n🔍 Testing SQLAlchemy Integration")
    print("-" * 30)

    try:
        from sqlalchemy import create_engine, text
        from urllib.parse import quote_plus

        # แปลง pyodbc connection string เป็น SQLAlchemy URL
        if "MSSQL2S" in conn_str:
            # Named Instance format
            sqlalchemy_url = (
                f"mssql+pyodbc://TS00029:{quote_plus('Thammaphon@TS00029')}@"
                f"10.73.148.27\\MSSQL2S/excel_to_db?"
                f"driver=ODBC+Driver+17+for+SQL+Server&"
                f"TrustServerCertificate=yes&"
                f"Encrypt=no"
            )
        else:
            # TCP format
            sqlalchemy_url = (
                f"mssql+pyodbc://TS00029:{quote_plus('Thammaphon@TS00029')}@"
                f"10.73.148.27:1433/excel_to_db?"
                f"driver=ODBC+Driver+17+for+SQL+Server&"
                f"TrustServerCertificate=yes&"
                f"Encrypt=no"
            )

        print(f"  🔗 URL: {sqlalchemy_url}")

        engine = create_engine(
            sqlalchemy_url, pool_size=3, max_overflow=5, pool_timeout=30, echo=False
        )

        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT @@SERVERNAME, DB_NAME()"))
            server, db = result.fetchone()
            print(f"  ✅ SQLAlchemy SUCCESS")
            print(f"  📋 Connected to: {server} / {db}")

        engine.dispose()
        return True, sqlalchemy_url

    except Exception as e:
        print(f"  ❌ SQLAlchemy FAILED: {e}")
        return False, None


def create_database_if_needed(working_conn_str):
    """สร้าง excel_to_db database หากยังไม่มี"""

    print(f"\n🔍 Creating excel_to_db Database")
    print("-" * 30)

    try:
        # เปลี่ยนเป็น master database
        master_conn_str = working_conn_str.replace(
            "DATABASE=CAS_Development;", "DATABASE=master;"
        )

        conn = pyodbc.connect(master_conn_str)
        cursor = conn.cursor()

        # Check if database exists
        cursor.execute("SELECT COUNT(*) FROM sys.databases WHERE name = 'excel_to_db'")
        exists = cursor.fetchone()[0]

        if exists == 0:
            print("  📋 Creating excel_to_db database...")
            cursor.execute("CREATE DATABASE excel_to_db")
            cursor.commit()
            print("  ✅ Database created successfully")
        else:
            print("  ✅ excel_to_db already exists")

        conn.close()
        return True

    except Exception as e:
        print(f"  ❌ Database creation failed: {e}")
        return False


def main():
    """Main test function"""

    # 1. Test connections
    working_connections = test_named_instance()

    if not working_connections:
        print("\n❌ ไม่สามารถเชื่อมต่อได้ด้วยรูปแบบใดๆ")
        print("💡 ตรวจสอบ:")
        print("  1. SQL Server Browser Service ทำงานอยู่หรือไม่")
        print("  2. Named Instance 'MSSQL2S' ถูกต้องหรือไม่")
        print("  3. Network connectivity (ping 10.73.148.27)")
        print("  4. Firewall settings")
        return

    # 2. Test SQLAlchemy
    format_name, working_conn_str = working_connections[0]
    print(f"\n✅ Using working connection: {format_name}")

    sqlalchemy_ok, sqlalchemy_url = test_sqlalchemy_with_working_connection(
        working_conn_str
    )

    # 3. Create database
    if sqlalchemy_ok:
        create_database_if_needed(working_conn_str)

    # 4. Final summary
    print("\n" + "=" * 50)
    print("📊 Connection Test Summary")
    print("=" * 50)

    print(f"✅ Direct Connection: {format_name}")
    print(f"✅ SQLAlchemy: {'OK' if sqlalchemy_ok else 'FAILED'}")

    if sqlalchemy_ok:
        print(f"\n🎉 ระบบพร้อมใช้งาน!")
        print(f"\n🔧 ใช้ Connection String นี้:")
        print(f"  {sqlalchemy_url}")
        print(f"\n🚀 ทดสอบ Excel import:")
        print(f"  python sample_generator.py test")
        print(f"  python excel_to_ssms.py data/samples/test_100.xlsx test_table")
    else:
        print(f"\n⚠️ SQLAlchemy ยังมีปัญหา - ใช้ direct connection ได้แล้ว")


if __name__ == "__main__":
    main()
