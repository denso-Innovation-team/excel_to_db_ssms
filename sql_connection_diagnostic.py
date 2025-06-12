#!/usr/bin/env python3
"""
SQL Server Connection Diagnostic & Fix Tool
แก้ปัญหาการเชื่อมต่อ SQL Server อย่างเป็นระบบ
"""

import socket
import subprocess
import platform
import pyodbc
import time
from urllib.parse import quote_plus


class SQLServerDiagnostic:
    def __init__(self, server_ip="10.73.148.27"):
        self.server_ip = server_ip
        self.results = {}

    def ping_test(self) -> bool:
        """ทดสอบ network connectivity"""
        print("🔍 Testing network connectivity...")

        try:
            cmd = (
                ["ping", "-n", "4"]
                if platform.system() == "Windows"
                else ["ping", "-c", "4"]
            )
            cmd.append(self.server_ip)

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)

            if result.returncode == 0:
                print(f"  ✅ Network OK: {self.server_ip} is reachable")
                return True
            else:
                print(f"  ❌ Network FAILED: {self.server_ip} unreachable")
                return False

        except Exception as e:
            print(f"  ❌ Ping error: {e}")
            return False

    def port_scan(self) -> dict:
        """ตรวจสอบ SQL Server ports"""
        print("🔍 Scanning SQL Server ports...")

        ports_to_test = [1433, 1434, 2433, 14333]
        open_ports = []

        for port in ports_to_test:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                result = sock.connect_ex((self.server_ip, port))
                sock.close()

                if result == 0:
                    print(f"  ✅ Port {port}: OPEN")
                    open_ports.append(port)
                else:
                    print(f"  ❌ Port {port}: CLOSED")

            except Exception as e:
                print(f"  ❌ Port {port}: ERROR - {e}")

        return open_ports

    def try_connection_variations(self) -> tuple:
        """ทดสอบ connection strings หลายแบบ"""
        print("🔍 Testing connection string variations...")

        variations = [
            # Default instance
            (
                "Default Instance",
                f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server_ip};DATABASE=master;UID=TS00029;PWD=Thammaphon@TS00029;TrustServerCertificate=yes;Encrypt=no;Timeout=30;",
            ),
            # With port 1433
            (
                "Port 1433",
                f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server_ip},1433;DATABASE=master;UID=TS00029;PWD=Thammaphon@TS00029;TrustServerCertificate=yes;Encrypt=no;Timeout=30;",
            ),
            # Named instance MSSQL2S
            (
                "Named Instance",
                f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server_ip}\\MSSQL2S;DATABASE=master;UID=TS00029;PWD=Thammaphon@TS00029;TrustServerCertificate=yes;Encrypt=no;Timeout=30;",
            ),
            # TCP protocol explicit
            (
                "TCP Protocol",
                f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=tcp:{self.server_ip},1433;DATABASE=master;UID=TS00029;PWD=Thammaphon@TS00029;TrustServerCertificate=yes;Encrypt=no;Timeout=30;",
            ),
            # Alternative database
            (
                "CAS_Development",
                f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server_ip}\\MSSQL2S;DATABASE=CAS_Development;UID=TS00029;PWD=Thammaphon@TS00029;TrustServerCertificate=yes;Encrypt=no;Timeout=30;",
            ),
        ]

        for name, conn_str in variations:
            print(f"  🔄 Testing: {name}")

            try:
                start_time = time.time()
                conn = pyodbc.connect(conn_str, timeout=10)
                connection_time = time.time() - start_time

                cursor = conn.cursor()
                cursor.execute(
                    "SELECT @@SERVERNAME, @@VERSION, DB_NAME(), SERVERPROPERTY('InstanceName')"
                )
                server_name, version, db, instance = cursor.fetchone()

                print(f"    ✅ SUCCESS ({connection_time:.2f}s)")
                print(f"    📋 Server: {server_name}")
                print(f"    📋 Instance: {instance or 'Default'}")
                print(f"    📋 Database: {db}")

                conn.close()
                return name, conn_str

            except Exception as e:
                error_msg = str(e)
                print(f"    ❌ FAILED: {error_msg[:100]}...")

        return None, None

    def generate_fixes(self, working_conn=None):
        """สร้างแนวทางแก้ปัญหา"""
        print("\n🔧 Diagnostic Results & Fixes")
        print("=" * 50)

        if working_conn:
            name, conn_str = working_conn
            print(f"✅ Working Connection Found: {name}")

            # Generate .env
            password_encoded = quote_plus("Thammaphon@TS00029")
            if "MSSQL2S" in conn_str:
                server_format = f"{self.server_ip}\\MSSQL2S"
            elif ",1433" in conn_str:
                server_format = f"{self.server_ip}:1433"
            else:
                server_format = self.server_ip

            env_config = f"""# Working SQL Server Configuration
DB_HOST={server_format}
DB_NAME=excel_to_db
DB_USER=TS00029
DB_PASSWORD=Thammaphon@TS00029
DB_DRIVER=ODBC Driver 17 for SQL Server

POOL_SIZE=3
MAX_OVERFLOW=5
BATCH_SIZE=1000
CHUNK_SIZE=5000
LOG_LEVEL=INFO
"""

            print(f"\n📝 Update your .env file:")
            print(env_config)

            # SQLAlchemy URL
            sqlalchemy_url = f"mssql+pyodbc://TS00029:{password_encoded}@{server_format}/excel_to_db?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes&Encrypt=no"
            print(f"🔗 SQLAlchemy URL:")
            print(f"  {sqlalchemy_url}")

        else:
            print("❌ No working connection found")
            print("\n💡 Troubleshooting Steps:")

            # Network issues
            if not self.results.get("ping_success", False):
                print("\n🌐 Network Issues:")
                print("  1. Check VPN connection")
                print("  2. Verify server IP address")
                print("  3. Test from different network")
                print("  4. Contact network administrator")

            # SQL Server service issues
            print("\n🗄️ SQL Server Service Issues:")
            print("  1. Check if SQL Server service is running")
            print("  2. Verify SQL Server Browser service")
            print("  3. Check SQL Server Configuration Manager")
            print("  4. Enable TCP/IP protocol")

            # Firewall issues
            print("\n🔥 Firewall Issues:")
            print("  1. Windows Firewall exceptions for SQL Server")
            print("  2. Network firewall rules")
            print("  3. Port 1433 and 1434 access")

            # Authentication issues
            print("\n🔐 Authentication Issues:")
            print("  1. Verify username: TS00029")
            print("  2. Check password: Thammaphon@TS00029")
            print("  3. Enable SQL Server authentication")
            print("  4. Check user permissions")

    def run_full_diagnostic(self):
        """รันการวินิจฉัยแบบเต็ม"""
        print("🎯 SQL Server Connection Diagnostic")
        print("=" * 60)

        # 1. Network test
        self.results["ping_success"] = self.ping_test()

        # 2. Port scan
        self.results["open_ports"] = self.port_scan()

        # 3. Connection attempts
        working_conn = None
        if self.results["ping_success"]:
            working_conn = self.try_connection_variations()

        # 4. Generate fixes
        self.generate_fixes(working_conn)

        return working_conn is not None


def create_fallback_solution():
    """สร้าง fallback solution สำหรับใช้กับ LocalDB"""
    print("\n🔄 Creating LocalDB Fallback Solution")
    print("=" * 50)

    localdb_script = '''#!/usr/bin/env python3
"""
LocalDB Fallback - สำหรับใช้งานเมื่อ SQL Server ไม่สามารถเชื่อมต่อได้
"""

import pandas as pd
import sqlite3
from pathlib import Path
import time

class LocalDBProcessor:
    def __init__(self, db_file="local_excel_data.db"):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)
    
    def process_excel(self, excel_file, table_name):
        """ประมวลผล Excel ด้วย SQLite"""
        print(f"📊 Processing {excel_file} → {table_name}")
        
        # Read Excel
        df = pd.read_excel(excel_file)
        print(f"✅ Read {len(df)} rows")
        
        # Clean column names
        df.columns = [col.replace(' ', '_').lower() for col in df.columns]
        
        # Insert to SQLite
        df.to_sql(table_name, self.conn, if_exists='replace', index=False)
        print(f"✅ Inserted to local database: {table_name}")
        
        # Verify
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"✅ Verified: {count} rows in {table_name}")
        
        return count
    
    def list_tables(self):
        """แสดงรายการตาราง"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        return tables

# Usage example
if __name__ == "__main__":
    processor = LocalDBProcessor()
    
    # สร้างข้อมูลทดสอบ
    test_data = {
        'id': [1, 2, 3],
        'name': ['Test 1', 'Test 2', 'Test 3'],
        'value': [100, 200, 300]
    }
    df = pd.DataFrame(test_data)
    df.to_excel('test_data.xlsx', index=False)
    
    # ประมวลผล
    processor.process_excel('test_data.xlsx', 'test_table')
    
    print(f"📋 Available tables: {processor.list_tables()}")
'''

    with open("localdb_fallback.py", "w", encoding="utf-8") as f:
        f.write(localdb_script)

    print("✅ Created: localdb_fallback.py")
    print("📋 Usage: python localdb_fallback.py")


def main():
    """Main diagnostic function"""
    diagnostic = SQLServerDiagnostic()
    success = diagnostic.run_full_diagnostic()

    if not success:
        print("\n🔄 SQL Server connection failed - creating fallback solution...")
        create_fallback_solution()

        print("\n💡 Alternative Solutions:")
        print("1. Use LocalDB fallback: python localdb_fallback.py")
        print("2. Setup SQL Server Express LocalDB")
        print("3. Use cloud database (Azure SQL, AWS RDS)")
        print("4. Contact system administrator for SQL Server access")


if __name__ == "__main__":
    main()
