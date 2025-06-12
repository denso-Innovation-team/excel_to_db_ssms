#!/usr/bin/env python3
"""
SQL Server Connection Alternatives
ทดสอบทุกแนวทางที่เป็นไปได้
"""

import pyodbc
import socket
import time


def test_connection_scenarios():
    """ทดสอบทุกสถานการณ์ที่เป็นไปได้"""

    print("🎯 SQL Server Connection Troubleshooting")
    print("=" * 60)

    server_ip = "10.73.148.27"

    # รวมทุกแนวทาง connection ที่เป็นไปได้
    scenarios = [
        # Scenario 1: Default Instance - Standard Port
        {
            "name": "Default Instance (Port 1433)",
            "conn_str": f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_ip};DATABASE=master;UID=TS00029;PWD=Thammaphon@TS00029;TrustServerCertificate=yes;Encrypt=no;ConnectRetryCount=1;ConnectRetryInterval=1;LoginTimeout=10;",
        },
        # Scenario 2: TCP Port Explicit
        {
            "name": "TCP Port 1433 Explicit",
            "conn_str": f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_ip},1433;DATABASE=master;UID=TS00029;PWD=Thammaphon@TS00029;TrustServerCertificate=yes;Encrypt=no;ConnectRetryCount=1;ConnectRetryInterval=1;LoginTimeout=10;",
        },
        # Scenario 3: Named Instance (จากภาพ SSMS)
        {
            "name": "Named Instance: MSSQL2S",
            "conn_str": f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_ip}\\MSSQL2S;DATABASE=master;UID=TS00029;PWD=Thammaphon@TS00029;TrustServerCertificate=yes;Encrypt=no;ConnectRetryCount=1;ConnectRetryInterval=1;LoginTimeout=10;",
        },
        # Scenario 4: CAS_Development Database (จากภาพ)
        {
            "name": "CAS_Development Direct",
            "conn_str": f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_ip};DATABASE=CAS_Development;UID=TS00029;PWD=Thammaphon@TS00029;TrustServerCertificate=yes;Encrypt=no;ConnectRetryCount=1;ConnectRetryInterval=1;LoginTimeout=10;",
        },
        # Scenario 5: Alternative Ports
        {
            "name": "Alternative Port 2433",
            "conn_str": f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_ip},2433;DATABASE=master;UID=TS00029;PWD=Thammaphon@TS00029;TrustServerCertificate=yes;Encrypt=no;ConnectRetryCount=1;ConnectRetryInterval=1;LoginTimeout=10;",
        },
        # Scenario 6: Windows Authentication (แบบ fallback)
        {
            "name": "Windows Authentication (if available)",
            "conn_str": f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_ip};DATABASE=master;Trusted_Connection=yes;TrustServerCertificate=yes;Encrypt=no;ConnectRetryCount=1;ConnectRetryInterval=1;LoginTimeout=10;",
        },
        # Scenario 7: ใช้ IP แทน hostname (ป้องกัน DNS issues)
        {
            "name": "IP Direct Connection",
            "conn_str": f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=tcp:{server_ip},1433;DATABASE=master;UID=TS00029;PWD=Thammaphon@TS00029;TrustServerCertificate=yes;Encrypt=no;ConnectRetryCount=1;ConnectRetryInterval=1;LoginTimeout=10;",
        },
    ]

    working_connections = []

    for i, scenario in enumerate(scenarios, 1):
        print(f"\n📋 Scenario {i}: {scenario['name']}")
        print("-" * 40)

        try:
            start_time = time.time()
            conn = pyodbc.connect(scenario["conn_str"])
            connection_time = time.time() - start_time

            cursor = conn.cursor()

            # Basic server info
            cursor.execute(
                "SELECT @@SERVERNAME, @@VERSION, DB_NAME(), SERVERPROPERTY('InstanceName')"
            )
            server_name, version, current_db, instance_name = cursor.fetchone()

            print(f"  ✅ SUCCESS ({connection_time:.2f}s)")
            print(f"  📋 Server: {server_name}")
            print(f"  📋 Instance: {instance_name or 'Default'}")
            print(f"  📋 Database: {current_db}")
            print(
                f"  📋 Version: {version.split()[3] if len(version.split()) > 3 else 'Unknown'}"
            )

            # Test write capabilities
            try:
                cursor.execute("SELECT COUNT(*) FROM sys.databases")
                db_count = cursor.fetchone()[0]
                print(f"  📋 Can access: {db_count} databases")

                # List available databases
                cursor.execute(
                    "SELECT name FROM sys.databases WHERE name NOT IN ('master', 'tempdb', 'model', 'msdb') ORDER BY name"
                )
                user_dbs = [row[0] for row in cursor.fetchall()]
                if user_dbs:
                    print(f"  📋 User databases: {', '.join(user_dbs[:5])}")

            except Exception as e:
                print(f"  ⚠️  Limited access: {e}")

            conn.close()
            working_connections.append((scenario["name"], scenario["conn_str"]))

            # หยุดที่ตัวแรกที่ทำงาน (เพื่อประหยัดเวลา)
            print(f"  🎯 Using this connection for further tests...")
            break

        except Exception as e:
            error_msg = str(e)
            print(f"  ❌ FAILED: {error_msg[:150]}...")

            # วิเคราะห์ error type
            if "login failed" in error_msg.lower():
                print(f"  💡 Authentication issue - check username/password")
            elif "timeout" in error_msg.lower():
                print(f"  💡 Network timeout - check connectivity/firewall")
            elif "instance" in error_msg.lower():
                print(f"  💡 Instance not found - check SQL Browser service")
            elif "network" in error_msg.lower():
                print(f"  💡 Network error - check SQL Server service")

    return working_connections


def test_sqlalchemy_integration(working_conn_str):
    """ทดสอบ SQLAlchemy integration ด้วย working connection"""

    print(f"\n🔍 Testing SQLAlchemy Integration")
    print("-" * 40)

    try:
        from sqlalchemy import create_engine, text
        from urllib.parse import quote_plus

        # แปลง pyodbc connection string เป็น SQLAlchemy URL
        if ",1433" in working_conn_str:
            # TCP port format
            sqlalchemy_url = (
                f"mssql+pyodbc://TS00029:{quote_plus('Thammaphon@TS00029')}@"
                f"10.73.148.27:1433/excel_to_db?"
                f"driver=ODBC+Driver+17+for+SQL+Server&"
                f"TrustServerCertificate=yes&Encrypt=no&timeout=30"
            )
        elif "tcp:" in working_conn_str:
            # TCP explicit format
            sqlalchemy_url = (
                f"mssql+pyodbc://TS00029:{quote_plus('Thammaphon@TS00029')}@"
                f"10.73.148.27:1433/excel_to_db?"
                f"driver=ODBC+Driver+17+for+SQL+Server&"
                f"TrustServerCertificate=yes&Encrypt=no&timeout=30"
            )
        else:
            # Default format
            sqlalchemy_url = (
                f"mssql+pyodbc://TS00029:{quote_plus('Thammaphon@TS00029')}@"
                f"10.73.148.27/excel_to_db?"
                f"driver=ODBC+Driver+17+for+SQL+Server&"
                f"TrustServerCertificate=yes&Encrypt=no&timeout=30"
            )

        print(f"  🔗 SQLAlchemy URL: {sqlalchemy_url}")

        # Create engine with minimal config
        engine = create_engine(
            sqlalchemy_url, pool_size=2, max_overflow=3, pool_timeout=30, echo=False
        )

        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT @@SERVERNAME, DB_NAME()"))
            server, db = result.fetchone()
            print(f"  ✅ SQLAlchemy SUCCESS")
            print(f"  📋 Connected to: {server}")
            print(f"  📋 Database: {db}")

        engine.dispose()
        return True, sqlalchemy_url

    except Exception as e:
        print(f"  ❌ SQLAlchemy FAILED: {e}")
        return False, None


def create_working_config(working_conn_str, sqlalchemy_url=None):
    """สร้าง configuration files ที่ใช้งานได้"""

    print(f"\n🎯 Creating Working Configuration")
    print("-" * 40)

    # วิเคราะห์ connection string
    if ",1433" in working_conn_str:
        connection_type = "TCP Port 1433"
        host_config = "DB_HOST=10.73.148.27\nDB_PORT=1433"
    elif "\\MSSQL2S" in working_conn_str:
        connection_type = "Named Instance"
        host_config = "DB_HOST=10.73.148.27\nDB_INSTANCE=MSSQL2S"
    else:
        connection_type = "Default Instance"
        host_config = "DB_HOST=10.73.148.27"

    # สร้าง .env file
    env_content = f"""# Working SQL Server Configuration
# Connection Type: {connection_type}

{host_config}
DB_NAME=excel_to_db
DB_USER=TS00029
DB_PASSWORD=Thammaphon@TS00029
DB_DRIVER=ODBC Driver 17 for SQL Server

# Pool Settings (ปรับลงเพื่อความเสถียร)
POOL_SIZE=3
MAX_OVERFLOW=5
POOL_TIMEOUT=30
POOL_RECYCLE=3600

# Processing Settings
BATCH_SIZE=500
MAX_WORKERS=2
CHUNK_SIZE=2000

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/excel_to_ssms.log
"""

    with open(".env_working", "w", encoding="utf-8") as f:
        f.write(env_content)

    print(f"  ✅ Created .env_working file")
    print(f"  📋 Connection type: {connection_type}")

    # สร้าง test script
    test_script = f'''#!/usr/bin/env python3
"""
Generated Test Script - Working Configuration
"""

import pyodbc

def test_working_connection():
    """ทดสอบ connection ที่ทำงานได้"""
    
    conn_str = """{working_conn_str}"""
    
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT @@SERVERNAME, DB_NAME()")
        server, db = cursor.fetchone()
        
        print(f"✅ Connection successful: {{server}} / {{db}}")
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {{e}}")
        return False

if __name__ == "__main__":
    test_working_connection()
'''

    with open("test_working_connection.py", "w", encoding="utf-8") as f:
        f.write(test_script)

    print(f"  ✅ Created test_working_connection.py")

    if sqlalchemy_url:
        print(f"\n💻 Working SQLAlchemy URL:")
        print(f"  {sqlalchemy_url}")


def main():
    """Main troubleshooting process"""

    # 1. ทดสอบทุก scenarios
    working_connections = test_connection_scenarios()

    if not working_connections:
        print(f"\n❌ ไม่พบ connection ที่ใช้งานได้")
        print(f"\n🔧 Troubleshooting Steps:")
        print(f"  1. ตรวจสอบ SQL Server service status")
        print(f"  2. เปิด SQL Server Configuration Manager")
        print(f"  3. Enable TCP/IP protocol")
        print(f"  4. Start SQL Server Browser service")
        print(f"  5. Configure Windows Firewall")
        print(f"  6. ตรวจสอบ network connectivity")
        return

    # 2. ทดสอบ SQLAlchemy
    working_name, working_conn_str = working_connections[0]
    print(f"\n✅ Found working connection: {working_name}")

    sqlalchemy_ok, sqlalchemy_url = test_sqlalchemy_integration(working_conn_str)

    # 3. สร้าง working configuration
    create_working_config(working_conn_str, sqlalchemy_url if sqlalchemy_ok else None)

    # 4. สรุปผล
    print(f"\n" + "=" * 60)
    print(f"🎉 CONNECTION TROUBLESHOOTING COMPLETE")
    print(f"=" * 60)

    print(f"✅ Working Connection: {working_name}")
    print(f"✅ SQLAlchemy: {'OK' if sqlalchemy_ok else 'Manual setup needed'}")

    print(f"\n🚀 Next Steps:")
    print(f"  1. cp .env_working .env")
    print(f"  2. python test_working_connection.py")
    print(f"  3. python sample_generator.py test")
    print(f"  4. python excel_to_ssms.py data/samples/test_100.xlsx test_table")


if __name__ == "__main__":
    main()
