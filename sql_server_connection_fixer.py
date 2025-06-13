#!/usr/bin/env python3
"""
SQL Server Connection Tester & Diagnostic Tool
เครื่องมือวินิจฉัยและแก้ปัญหาการเชื่อมต่อ SQL Server
"""

import socket
import subprocess
import platform
import time
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging

# Optional imports
try:
    import pyodbc

    PYODBC_AVAILABLE = True
except ImportError:
    PYODBC_AVAILABLE = False

try:
    import sqlalchemy
    from sqlalchemy import create_engine, text

    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False

try:
    from dotenv import load_dotenv

    load_dotenv()
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

import os


class SQLServerDiagnostic:
    """Comprehensive SQL Server diagnostic tool"""

    def __init__(self):
        self.server_ip = os.getenv("DB_HOST", "10.73.148.27")
        self.db_name = os.getenv("DB_NAME", "excel_to_db")
        self.username = os.getenv("DB_USER", "TS00029")
        self.password = os.getenv("DB_PASSWORD", "Thammaphon@TS00029")

        self.results = {}
        self.setup_logging()

    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)

    def check_prerequisites(self) -> Dict[str, bool]:
        """Check if required packages are installed"""
        print("🔍 Checking Prerequisites...")

        checks = {
            "python_version": sys.version_info >= (3, 8),
            "pyodbc": PYODBC_AVAILABLE,
            "sqlalchemy": SQLALCHEMY_AVAILABLE,
            "dotenv": DOTENV_AVAILABLE,
        }

        for check, status in checks.items():
            status_icon = "✅" if status else "❌"
            print(f"  {status_icon} {check}: {'OK' if status else 'MISSING'}")

        if not checks["pyodbc"]:
            print("    💡 Install: pip install pyodbc")
        if not checks["sqlalchemy"]:
            print("    💡 Install: pip install sqlalchemy")
        if not checks["dotenv"]:
            print("    💡 Install: pip install python-dotenv")

        return checks

    def check_odbc_drivers(self) -> List[str]:
        """Check available ODBC drivers"""
        print("\n🔍 Checking ODBC Drivers...")

        if not PYODBC_AVAILABLE:
            print("  ❌ pyodbc not available")
            return []

        try:
            drivers = pyodbc.drivers()
            sql_server_drivers = [d for d in drivers if "SQL Server" in d]

            print(f"  📋 Total drivers: {len(drivers)}")
            print(f"  📋 SQL Server drivers: {len(sql_server_drivers)}")

            for driver in sql_server_drivers:
                print(f"    ✅ {driver}")

            if not sql_server_drivers:
                print("  ❌ No SQL Server drivers found!")
                print("    💡 Install ODBC Driver 17 for SQL Server")

            return sql_server_drivers

        except Exception as e:
            print(f"  ❌ Error checking drivers: {e}")
            return []

    def test_network_connectivity(self) -> bool:
        """Test basic network connectivity"""
        print(f"\n🔍 Testing Network Connectivity to {self.server_ip}...")

        # Ping test
        try:
            if platform.system().lower() == "windows":
                cmd = ["ping", "-n", "4", self.server_ip]
            else:
                cmd = ["ping", "-c", "4", self.server_ip]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)

            if result.returncode == 0:
                print(f"  ✅ Ping successful to {self.server_ip}")
                ping_success = True
            else:
                print(f"  ❌ Ping failed to {self.server_ip}")
                ping_success = False

        except Exception as e:
            print(f"  ❌ Ping error: {e}")
            ping_success = False

        # Port connectivity test
        ports_tested = self.test_port_connectivity()

        return ping_success and len(ports_tested) > 0

    def test_port_connectivity(self) -> List[int]:
        """Test SQL Server port connectivity"""
        print(f"  🔍 Testing SQL Server ports...")

        ports_to_test = [1433, 1434, 2433, 14333]
        open_ports = []

        for port in ports_to_test:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex((self.server_ip, port))
                sock.close()

                if result == 0:
                    print(f"    ✅ Port {port}: OPEN")
                    open_ports.append(port)
                else:
                    print(f"    ❌ Port {port}: CLOSED")

            except Exception as e:
                print(f"    ❌ Port {port}: ERROR - {e}")

        return open_ports

    def test_connection_strings(self) -> Optional[Tuple[str, str]]:
        """Test various connection string formats"""
        print(f"\n🔍 Testing Connection Strings...")

        if not PYODBC_AVAILABLE:
            print("  ❌ pyodbc not available for testing")
            return None

        connection_variations = [
            (
                "Default Instance",
                f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server_ip};DATABASE={self.db_name};UID={self.username};PWD={self.password};TrustServerCertificate=yes;Encrypt=no;Timeout=30;",
            ),
            (
                "Port 1433",
                f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server_ip},1433;DATABASE={self.db_name};UID={self.username};PWD={self.password};TrustServerCertificate=yes;Encrypt=no;Timeout=30;",
            ),
            (
                "Named Instance MSSQL2S",
                f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server_ip}\\MSSQL2S;DATABASE={self.db_name};UID={self.username};PWD={self.password};TrustServerCertificate=yes;Encrypt=no;Timeout=30;",
            ),
            (
                "TCP Protocol",
                f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=tcp:{self.server_ip},1433;DATABASE={self.db_name};UID={self.username};PWD={self.password};TrustServerCertificate=yes;Encrypt=no;Timeout=30;",
            ),
            (
                "Master Database",
                f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server_ip};DATABASE=master;UID={self.username};PWD={self.password};TrustServerCertificate=yes;Encrypt=no;Timeout=30;",
            ),
        ]

        for name, conn_str in connection_variations:
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
                print(f"      Server: {server_name}")
                print(f"      Instance: {instance or 'Default'}")
                print(f"      Database: {db}")
                print(
                    f"      Version: {version.split('-')[0] if version else 'Unknown'}"
                )

                conn.close()
                return name, conn_str

            except Exception as e:
                error_msg = str(e)
                print(f"    ❌ FAILED: {error_msg[:80]}...")

        return None

    def test_sqlalchemy_connection(self, working_conn_str: str = None) -> bool:
        """Test SQLAlchemy connection"""
        print(f"\n🔍 Testing SQLAlchemy Connection...")

        if not SQLALCHEMY_AVAILABLE:
            print("  ❌ sqlalchemy not available")
            return False

        if not working_conn_str:
            print("  ⚠️ No working pyodbc connection to test with")
            return False

        try:
            from urllib.parse import quote_plus

            # Convert pyodbc connection string to SQLAlchemy URL
            password_encoded = quote_plus(self.password)

            if "MSSQL2S" in working_conn_str:
                server_part = f"{self.server_ip}\\MSSQL2S"
            elif ",1433" in working_conn_str:
                server_part = f"{self.server_ip}:1433"
            else:
                server_part = self.server_ip

            sqlalchemy_url = (
                f"mssql+pyodbc://{self.username}:{password_encoded}@"
                f"{server_part}/{self.db_name}?"
                f"driver=ODBC+Driver+17+for+SQL+Server&"
                f"TrustServerCertificate=yes&Encrypt=no"
            )

            engine = create_engine(sqlalchemy_url, pool_size=1, max_overflow=1)

            with engine.connect() as conn:
                result = conn.execute(text("SELECT @@SERVERNAME, DB_NAME()"))
                server, database = result.fetchone()
                print(f"  ✅ SQLAlchemy connection successful")
                print(f"    Server: {server}")
                print(f"    Database: {database}")

            engine.dispose()
            return True

        except Exception as e:
            print(f"  ❌ SQLAlchemy connection failed: {e}")
            return False

    def generate_working_configuration(self, working_conn: Tuple[str, str]) -> None:
        """Generate working configuration files"""
        print(f"\n🔧 Generating Working Configuration...")

        name, conn_str = working_conn

        # Determine server format for .env
        if "MSSQL2S" in conn_str:
            db_host = f"{self.server_ip}\\MSSQL2S"
        elif ",1433" in conn_str:
            db_host = f"{self.server_ip}:1433"
        else:
            db_host = self.server_ip

        # Generate .env content
        env_content = f"""# Working SQL Server Configuration - {name}
# Generated by diagnostic tool

DB_HOST={db_host}
DB_NAME={self.db_name}
DB_USER={self.username}
DB_PASSWORD={self.password}
DB_DRIVER=ODBC Driver 17 for SQL Server

# Pool Settings (Conservative for stability)
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

        # Write .env file
        env_file = Path(".env_working")
        with open(env_file, "w", encoding="utf-8") as f:
            f.write(env_content)

        print(f"  ✅ Created: {env_file}")
        print(f"  💡 Copy to .env to use: cp {env_file} .env")

        # Generate test script
        test_script = f'''#!/usr/bin/env python3
"""
Quick connection test using working configuration
"""

import os
os.environ["DB_HOST"] = "{db_host}"
os.environ["DB_NAME"] = "{self.db_name}"
os.environ["DB_USER"] = "{self.username}"
os.environ["DB_PASSWORD"] = "{self.password}"

try:
    import pyodbc
    
    conn_str = "{conn_str}"
    conn = pyodbc.connect(conn_str, timeout=10)
    cursor = conn.cursor()
    cursor.execute("SELECT @@SERVERNAME, DB_NAME(), COUNT(*) FROM INFORMATION_SCHEMA.TABLES")
    server, database, table_count = cursor.fetchone()
    
    print(f"✅ Connection successful!")
    print(f"   Server: {{server}}")
    print(f"   Database: {{database}}")
    print(f"   Tables: {{table_count}}")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Connection failed: {{e}}")
'''

        test_file = Path("test_working_connection.py")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(test_script)

        print(f"  ✅ Created: {test_file}")
        print(f"  🔄 Test with: python {test_file}")

    def provide_troubleshooting_guide(self) -> None:
        """Provide comprehensive troubleshooting guide"""
        print(f"\n🔧 Troubleshooting Guide")
        print("=" * 50)

        print("\n🌐 Network Issues:")
        print("  1. Check VPN connection if required")
        print("  2. Verify server IP address is correct")
        print("  3. Test from different network/location")
        print("  4. Contact network administrator")
        print("  5. Check Windows Firewall settings")

        print("\n🗄️ SQL Server Issues:")
        print("  1. Verify SQL Server service is running")
        print("  2. Check SQL Server Browser service")
        print("  3. Enable TCP/IP protocol in SQL Server Configuration Manager")
        print("  4. Verify SQL Server is listening on port 1433")
        print("  5. Check SQL Server error logs")

        print("\n🔐 Authentication Issues:")
        print("  1. Verify username and password")
        print("  2. Enable SQL Server authentication (mixed mode)")
        print("  3. Check user permissions and database access")
        print("  4. Verify user is not locked out")
        print("  5. Check password expiration policy")

        print("\n🔧 Driver Issues:")
        print("  1. Install ODBC Driver 17 for SQL Server")
        print("  2. Update to latest driver version")
        print("  3. Check driver architecture (32-bit vs 64-bit)")
        print("  4. Restart application after driver installation")

        print("\n📦 Python Package Issues:")
        print("  1. pip install pyodbc sqlalchemy python-dotenv")
        print("  2. Upgrade packages: pip install --upgrade pyodbc")
        print("  3. Check Python architecture matches ODBC driver")
        print("  4. Use virtual environment to avoid conflicts")

    def run_comprehensive_diagnostic(self) -> bool:
        """Run complete diagnostic sequence"""
        print("🎯 SQL Server Connection Diagnostic Tool")
        print("=" * 60)
        print(f"Target: {self.username}@{self.server_ip}/{self.db_name}")
        print("=" * 60)

        # 1. Prerequisites
        prereq_ok = all(self.check_prerequisites().values())

        # 2. ODBC Drivers
        drivers = self.check_odbc_drivers()
        drivers_ok = len(drivers) > 0

        # 3. Network connectivity
        network_ok = self.test_network_connectivity()

        # 4. Connection strings
        working_conn = None
        if network_ok and drivers_ok:
            working_conn = self.test_connection_strings()

        # 5. SQLAlchemy test
        sqlalchemy_ok = False
        if working_conn:
            sqlalchemy_ok = self.test_sqlalchemy_connection(working_conn[1])

        # 6. Results and recommendations
        print(f"\n📊 Diagnostic Summary")
        print("=" * 30)
        print(f"✅ Prerequisites: {'OK' if prereq_ok else 'ISSUES'}")
        print(f"✅ ODBC Drivers: {'OK' if drivers_ok else 'MISSING'}")
        print(f"✅ Network: {'OK' if network_ok else 'FAILED'}")
        print(f"✅ SQL Connection: {'OK' if working_conn else 'FAILED'}")
        print(f"✅ SQLAlchemy: {'OK' if sqlalchemy_ok else 'FAILED'}")

        if working_conn:
            print(f"\n🎉 Working Connection Found!")
            print(f"   Method: {working_conn[0]}")
            self.generate_working_configuration(working_conn)

            print(f"\n🚀 Next Steps:")
            print(f"  1. Copy .env_working to .env")
            print(f"  2. Test: python test_working_connection.py")
            print(f"  3. Run: python excel_to_ssms_fixed.py your_file.xlsx table_name")

            return True
        else:
            print(f"\n❌ No working connection found")
            self.provide_troubleshooting_guide()
            return False


def main():
    """Main diagnostic function"""
    diagnostic = SQLServerDiagnostic()
    success = diagnostic.run_comprehensive_diagnostic()

    if success:
        print(f"\n✅ Diagnostic completed successfully!")
    else:
        print(f"\n❌ Diagnostic found issues that need to be resolved.")
        print(f"💡 Follow the troubleshooting guide above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
