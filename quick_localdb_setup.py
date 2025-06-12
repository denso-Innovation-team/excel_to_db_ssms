#!/usr/bin/env python3
import os
import pandas as pd
from pathlib import Path


def setup_localdb():
    """Setup LocalDB configuration"""

    # 1. Create .env for LocalDB
    env_content = """# LocalDB Configuration
DB_HOST=(LocalDB)\\MSSQLLocalDB
DB_NAME=excel_to_db
TRUSTED_CONNECTION=yes
DB_DRIVER=ODBC Driver 17 for SQL Server

POOL_SIZE=3
MAX_OVERFLOW=5
BATCH_SIZE=500
MAX_WORKERS=2
CHUNK_SIZE=2000

LOG_LEVEL=INFO
LOG_FILE=logs/excel_to_ssms.log
"""

    with open(".env", "w") as f:
        f.write(env_content)
    print("✅ .env updated for LocalDB")

    # 2. Replace settings.py
    settings_code = """import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

class Settings:
    def __init__(self):
        self.DB_HOST = "(LocalDB)\\\\MSSQLLocalDB"
        self.DB_NAME = "excel_to_db"
        self.DB_DRIVER = "ODBC Driver 17 for SQL Server"
        
        self.POOL_SIZE = 3
        self.MAX_OVERFLOW = 5
        self.POOL_TIMEOUT = 30
        self.POOL_RECYCLE = 3600
        
        self.BATCH_SIZE = 500
        self.MAX_WORKERS = 2
        self.CHUNK_SIZE = 2000
        
        self.LOG_LEVEL = "INFO"
        self.LOG_FILE = "logs/excel_to_ssms.log"
    
    def get_database_url(self):
        return (
            f"mssql+pyodbc://@{quote_plus(self.DB_HOST)}/{self.DB_NAME}?"
            f"driver=ODBC+Driver+17+for+SQL+Server&"
            f"Trusted_Connection=yes"
        )
    
    def get_direct_connection_string(self):
        return (
            f"DRIVER={{{self.DB_DRIVER}}};"
            f"SERVER={self.DB_HOST};"
            f"DATABASE={self.DB_NAME};"
            f"Trusted_Connection=yes;"
        )

settings = Settings()"""

    with open("src/config/settings.py", "w") as f:
        f.write(settings_code)
    print("✅ settings.py updated for LocalDB")

    # 3. Create sample Excel data
    Path("data/samples").mkdir(parents=True, exist_ok=True)

    data = {
        "EmployeeID": ["EMP001", "EMP002", "EMP003", "EMP004", "EMP005"],
        "Name": ["สมชาย ใจดี", "สมหญิง รักดี", "วิชัย เจริญ", "นารี สุขใส", "ประเสริฐ มั่นคง"],
        "Department": ["IT", "การตลาด", "บัญชี", "HR", "ขาย"],
        "Salary": [50000, 45000, 40000, 35000, 30000],
        "HireDate": [
            "2023-01-15",
            "2023-02-20",
            "2023-03-10",
            "2023-04-05",
            "2023-05-12",
        ],
        "IsActive": [True, True, False, True, True],
    }

    df = pd.DataFrame(data)
    excel_file = "data/samples/test_employees.xlsx"
    df.to_excel(excel_file, index=False)
    print(f"✅ Sample data: {excel_file}")

    return excel_file


def test_localdb_connection():
    """Test LocalDB connection"""
    try:
        import pyodbc

        conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=(LocalDB)\\MSSQLLocalDB;"
            "DATABASE=master;"
            "Trusted_Connection=yes;"
        )

        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT @@SERVERNAME")
        server = cursor.fetchone()[0]
        print(f"✅ LocalDB connection: {server}")

        # Create database
        cursor.execute(
            "IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'excel_to_db') CREATE DATABASE excel_to_db"
        )
        cursor.commit()
        print("✅ Database excel_to_db ready")

        conn.close()
        return True

    except Exception as e:
        print(f"❌ LocalDB test failed: {e}")
        return False


def main():
    print("🚀 LocalDB Quick Setup")
    print("=" * 30)

    # Setup configuration
    excel_file = setup_localdb()

    # Test connection
    if test_localdb_connection():
        print("\n✅ LocalDB setup complete!")
        print("\n🚀 Test Excel import:")
        print(f"  python excel_to_ssms.py {excel_file} employees")
    else:
        print("\n❌ LocalDB setup failed")
        print("💡 Install SQL Server Express LocalDB")


if __name__ == "__main__":
    main()
