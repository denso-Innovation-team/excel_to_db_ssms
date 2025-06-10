#!/usr/bin/env python3
"""
PyODBC Installation Fix & Alternative Connection Methods
แก้ปัญหาการติดตั้ง pyodbc และทดสอบการเชื่อมต่อ SQL Server
"""

import subprocess
import sys
import os
from pathlib import Path


def install_pyodbc():
    """ติดตั้ง pyodbc ด้วยวิธีต่างๆ"""
    print("🔧 Installing pyodbc...")

    methods = [
        ["pip", "install", "pyodbc"],
        ["pip", "install", "--upgrade", "pip", "setuptools", "wheel"],
        ["pip", "install", "pyodbc", "--no-cache-dir"],
        ["pip", "install", "pyodbc", "--force-reinstall"],
    ]

    for i, method in enumerate(methods, 1):
        try:
            print(f"  Method {i}: {' '.join(method)}")
            subprocess.run(method, check=True, capture_output=True)
            print(f"  ✅ Success with method {i}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Method {i} failed: {e}")
            continue

    print("❌ All installation methods failed")
    return False


def test_pyodbc_import():
    """ทดสอบ import pyodbc"""
    try:
        import pyodbc

        print("✅ pyodbc imported successfully")

        # Show available drivers
        drivers = [d for d in pyodbc.drivers() if "SQL Server" in d]
        print(f"📋 Available SQL Server drivers: {drivers}")

        if not drivers:
            print("⚠️ No SQL Server ODBC drivers found")
            print("💡 Install: ODBC Driver 17 for SQL Server")
            return False

        return True
    except ImportError as e:
        print(f"❌ Cannot import pyodbc: {e}")
        return False


def create_alternative_test():
    """สร้าง test script ที่ไม่ต้องใช้ pyodbc"""
    test_code = '''#!/usr/bin/env python3
"""
Alternative SQL Server Test - Without pyodbc dependency
ทดสอบการเชื่อมต่อ SQL Server โดยไม่ต้องใช้ pyodbc
"""

def test_sqlalchemy_only():
    """ทดสอบ SQLAlchemy connection อย่างเดียว"""
    try:
        from sqlalchemy import create_engine, text
        from urllib.parse import quote_plus
        
        print("🔍 Testing SQLAlchemy connection to SQL Server...")
        
        # Connection parameters
        host = "10.73.148.27"
        port = "1433"
        database = "master"
        username = "TS00029"
        password = "Thammaphon@TS00029"
        
        # URL encode password
        password_encoded = quote_plus(password)
        
        # Connection URL
        connection_url = (
            f"mssql+pyodbc://{username}:{password_encoded}@"
            f"{host}:{port}/{database}?"
            f"driver=ODBC+Driver+17+for+SQL+Server&"
            f"TrustServerCertificate=yes&"
            f"Encrypt=optional"
        )
        
        print(f"📋 Connecting to: {host}:{port}")
        
        # Create engine
        engine = create_engine(
            connection_url,
            pool_size=1,
            max_overflow=0,
            pool_pre_ping=True,
            echo=False,
            connect_args={"timeout": 10}
        )
        
        # Test connection
        with engine.connect() as conn:
            # Basic test
            result = conn.execute(text("SELECT 1 as test"))
            test_value = result.fetchone()[0]
            print(f"✅ Connection test: {test_value}")
            
            # Server info
            result = conn.execute(text("SELECT @@VERSION"))
            version = result.fetchone()[0].split('\\n')[0]
            print(f"📋 SQL Server: {version}")
            
            # Check ExcelImportDB
            result = conn.execute(text("""
                SELECT name FROM sys.databases 
                WHERE name = 'ExcelImportDB'
            """))
            
            if not result.fetchone():
                print("📋 Creating ExcelImportDB database...")
                conn.execute(text("CREATE DATABASE ExcelImportDB"))
                conn.commit()
                print("✅ Database created")
            else:
                print("✅ Database ExcelImportDB exists")
        
        print("\\n🎉 SQLAlchemy connection successful!")
        return True
        
    except Exception as e:
        print(f"❌ SQLAlchemy connection failed: {e}")
        
        error_str = str(e).lower()
        if "login failed" in error_str:
            print("💡 Check username/password in .env file")
        elif "driver" in error_str:
            print("💡 Install ODBC Driver 17 for SQL Server")
        elif "network" in error_str:
            print("💡 Check network connectivity to 10.73.148.27")
        
        return False

def test_basic_excel_processing():
    """ทดสอบการประมวลผล Excel โดยไม่ต้องเชื่อมฐานข้อมูล"""
    try:
        import pandas as pd
        
        print("\\n🔍 Testing Excel processing...")
        
        # สร้างข้อมูลทดสอบ
        test_data = {
            'Name': ['สมชาย ใจดี', 'สมหญิง รักดี', 'วิชัย เจริญ'],
            'Age': [25, 30, 35],
            'Salary': [50000.0, 75000.0, 85000.0],
            'Department': ['IT', 'การตลาด', 'บัญชี']
        }
        
        df = pd.DataFrame(test_data)
        test_file = 'test_data.xlsx'
        
        # สร้างไฟล์ Excel
        df.to_excel(test_file, index=False, engine='openpyxl')
        print(f"✅ Created test file: {test_file}")
        
        # อ่านไฟล์กลับ
        df_read = pd.read_excel(test_file, engine='openpyxl')
        print(f"✅ Read back {len(df_read)} rows")
        print(f"📋 Columns: {list(df_read.columns)}")
        
        # ลบไฟล์ทดสอบ
        import os
        os.remove(test_file)
        print("✅ Excel processing works")
        
        return True
        
    except Exception as e:
        print(f"❌ Excel processing failed: {e}")
        return False

def main():
    print("🔧 Alternative SQL Server Test")
    print("=" * 40)
    
    # Test 1: SQLAlchemy connection
    sql_ok = test_sqlalchemy_only()
    
    # Test 2: Excel processing  
    excel_ok = test_basic_excel_processing()
    
    if sql_ok and excel_ok:
        print("\\n🎉 Core functionality works!")
        print("🚀 You can proceed with Excel import")
        print("\\n📋 Usage:")
        print("  python excel_to_sqlserver.py your_file.xlsx table_name")
    else:
        if not sql_ok:
            print("\\n❌ SQL Server connection needs fixing")
        if not excel_ok:
            print("\\n❌ Excel processing needs fixing")

if __name__ == "__main__":
    main()
'''

    with open("test_alternative.py", "w", encoding="utf-8") as f:
        f.write(test_code)
    print("✅ สร้าง test_alternative.py (ไม่ต้องใช้ pyodbc)")


def create_requirements_check():
    """ตรวจสอบ packages ที่จำเป็น"""
    check_code = '''#!/usr/bin/env python3
"""
Requirements Checker
ตรวจสอบ packages ที่จำเป็นสำหรับ Excel to SQL Server
"""

def check_package(package_name, import_name=None):
    """ตรวจสอบ package"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"✅ {package_name}: OK")
        return True
    except ImportError:
        print(f"❌ {package_name}: Missing")
        return False

def main():
    print("📦 Checking Required Packages")
    print("=" * 30)
    
    packages = [
        ("pandas", "pandas"),
        ("sqlalchemy", "sqlalchemy"), 
        ("openpyxl", "openpyxl"),
        ("pyodbc", "pyodbc"),
        ("python-dotenv", "dotenv"),
        ("tqdm", "tqdm")
    ]
    
    missing = []
    
    for package, import_name in packages:
        if not check_package(package, import_name):
            missing.append(package)
    
    if missing:
        print(f"\\n❌ Missing packages: {missing}")
        print("\\n🔧 Install commands:")
        for package in missing:
            print(f"  pip install {package}")
        
        # Special case for pyodbc
        if "pyodbc" in missing:
            print("\\n💡 If pyodbc fails to install:")
            print("  1. Download Microsoft C++ Build Tools")
            print("  2. Or use conda: conda install pyodbc")
            print("  3. Or use pre-compiled wheel")
    else:
        print("\\n🎉 All packages are installed!")

if __name__ == "__main__":
    main()
'''

    with open("check_requirements.py", "w", encoding="utf-8") as f:
        f.write(check_code)
    print("✅ สร้าง check_requirements.py")


def main():
    print("🔧 PyODBC Installation & Testing")
    print("=" * 40)

    # Step 1: Try to install pyodbc
    if not test_pyodbc_import():
        print("\n🔧 Attempting to install pyodbc...")
        if install_pyodbc():
            test_pyodbc_import()

    # Step 2: Create alternative test
    create_alternative_test()
    create_requirements_check()

    print("\n✅ Setup Complete!")
    print("=" * 40)
    print("📋 Next Steps:")
    print("  1. python check_requirements.py  # ตรวจสอบ packages")
    print("  2. python test_alternative.py    # ทดสอบไม่ใช้ pyodbc")
    print("  3. หาก pyodbc ยังติดตั้งไม่ได้:")
    print("     - ลองใช้ conda install pyodbc")
    print("     - หรือดาวน์โหลด pre-compiled wheel")


if __name__ == "__main__":
    main()
