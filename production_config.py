#!/usr/bin/env python3
import os
from urllib.parse import quote_plus


# Production Configuration
def setup_production_config():
    """Setup config สำหรับ excel_to_db database"""

    # .env สำหรับ production
    env_content = """# Production SQL Server - excel_to_db
DB_HOST=10.73.148.27
DB_PORT=1433
DB_NAME=excel_to_db
DB_USER=TS00029
DB_PASSWORD=Thammaphon@TS00029

# Performance Settings
POOL_SIZE=5
MAX_OVERFLOW=10
BATCH_SIZE=2000
MAX_WORKERS=6
CHUNK_SIZE=10000

LOG_LEVEL=INFO
LOG_FILE=logs/excel_to_ssms.log
"""

    with open(".env", "w") as f:
        f.write(env_content)

    # settings.py สำหรับ production
    settings_code = """import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

class Settings:
    def __init__(self):
        self.DB_HOST = os.getenv("DB_HOST", "10.73.148.27")
        self.DB_PORT = os.getenv("DB_PORT", "1433") 
        self.DB_NAME = os.getenv("DB_NAME", "excel_to_db")
        self.DB_USER = os.getenv("DB_USER", "TS00029")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD", "Thammaphon@TS00029")
        self.DB_DRIVER = "ODBC Driver 17 for SQL Server"
        
        self.POOL_SIZE = int(os.getenv("POOL_SIZE", "5"))
        self.MAX_OVERFLOW = int(os.getenv("MAX_OVERFLOW", "10"))
        self.POOL_TIMEOUT = 30
        self.POOL_RECYCLE = 3600
        
        self.BATCH_SIZE = int(os.getenv("BATCH_SIZE", "2000"))
        self.MAX_WORKERS = int(os.getenv("MAX_WORKERS", "6"))
        self.CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "10000"))
        
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FILE = os.getenv("LOG_FILE", "logs/excel_to_ssms.log")
    
    def get_database_url(self):
        password_encoded = quote_plus(self.DB_PASSWORD)
        return (
            f"mssql+pyodbc://{self.DB_USER}:{password_encoded}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?"
            f"driver=ODBC+Driver+17+for+SQL+Server&"
            f"TrustServerCertificate=yes&Encrypt=no"
        )
    
    def get_direct_connection_string(self):
        return (
            f"DRIVER={{{self.DB_DRIVER}}};"
            f"SERVER={self.DB_HOST},{self.DB_PORT};"
            f"DATABASE={self.DB_NAME};"
            f"UID={self.DB_USER};"
            f"PWD={self.DB_PASSWORD};"
            f"TrustServerCertificate=yes;Encrypt=no;"
        )

settings = Settings()"""

    with open("src/config/settings.py", "w") as f:
        f.write(settings_code)

    print("✅ Production config updated")
    print("📋 Database: excel_to_db")
    print("🔗 Server: 10.73.148.27:1433")


def test_production_connection():
    """ทดสอบ production connection"""
    try:
        import pyodbc

        conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=10.73.148.27,1433;"
            "DATABASE=excel_to_db;"
            "UID=TS00029;"
            "PWD=Thammaphon@TS00029;"
            "TrustServerCertificate=yes;Encrypt=no;"
        )

        conn = pyodbc.connect(conn_str, timeout=10)
        cursor = conn.cursor()
        cursor.execute("SELECT @@SERVERNAME, DB_NAME()")
        server, db = cursor.fetchone()

        print(f"✅ Connected: {server}/{db}")

        # Check existing tables
        cursor.execute("SELECT name FROM sys.tables ORDER BY name")
        tables = [row[0] for row in cursor.fetchall()]
        if tables:
            print(f"📋 Existing tables: {', '.join(tables)}")
        else:
            print("📋 No tables yet")

        conn.close()
        return True

    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Production Setup for excel_to_db")
    print("=" * 40)

    setup_production_config()

    if test_production_connection():
        print("\n✅ Ready for production!")
        print("\n🚀 Import sales data:")
        print("python excel_to_ssms.py data/samples/sales_50000.xlsx sales_50k")
    else:
        print("\n❌ Connection issue - check server status")
