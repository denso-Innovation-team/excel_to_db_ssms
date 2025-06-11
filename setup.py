#!/usr/bin/env python3
"""
Excel to SSMS - Complete System Setup
ติดตั้งและตั้งค่าระบบให้พร้อมใช้งานในครั้งเดียว
"""

import subprocess
import sys
import os
import platform
from pathlib import Path


def run_command(cmd, description=""):
    """รันคำสั่งพร้อม error handling"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, check=True
        )
        print(f"✅ {description}")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description}: {e.stderr}")
        return False, e.stderr


def install_fixed_requirements():
    """ติดตั้ง packages ที่แก้ไขแล้ว"""

    print("📦 ติดตั้ง Python packages...")

    # Core packages (แน่นอนว่าใช้ได้)
    core_packages = [
        "pandas>=2.0.0",
        "sqlalchemy>=2.0.0",
        "openpyxl>=3.1.0",
        "python-dotenv>=1.0.0",
        "tqdm>=4.65.0",
    ]

    # Optional packages (อาจมีปัญหาในบางระบบ)
    optional_packages = [
        "pyodbc>=4.0.39",
        "numpy>=1.24.0",
        "xlrd>=2.0.1",
        "psutil>=5.9.0",
    ]

    installed = []
    failed = []

    # ติดตั้ง core packages ก่อน
    for package in core_packages:
        name = package.split(">=")[0]
        success, output = run_command(
            f"{sys.executable} -m pip install {package}", f"Installing {name}"
        )
        if success:
            installed.append(name)
        else:
            failed.append(name)

    # ติดตั้ง optional packages
    for package in optional_packages:
        name = package.split(">=")[0]
        success, output = run_command(
            f"{sys.executable} -m pip install {package}",
            f"Installing {name} (optional)",
        )
        if success:
            installed.append(name)
        else:
            print(f"⚠️ {name} ติดตั้งไม่ได้ (ไม่จำเป็น)")

    return installed, failed


def create_project_structure():
    """สร้างโครงสร้างโปรเจค"""

    print("\n📁 สร้างโครงสร้างโปรเจค...")

    directories = ["src/config", "src/processors", "src/utils", "logs", "data/samples"]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

        # สร้าง __init__.py files
        if directory.startswith("src"):
            init_file = Path(directory) / "__init__.py"
            init_file.touch()

    print("✅ โครงสร้างโปรเจคพร้อม")


def create_configuration_files():
    """สร้างไฟล์ configuration"""

    print("\n⚙️ สร้างไฟล์ configuration...")

    # .env file
    if not Path(".env").exists():
        env_content = """# Excel to SSMS Configuration
DB_HOST=10.73.148.27
DB_NAME=excel_to_db
DB_USER=TS00029
DB_PASSWORD=Thammaphon@TS00029
DB_TYPE=mssql
DB_DRIVER=ODBC Driver 17 for SQL Server

# Connection Pool
POOL_SIZE=10
MAX_OVERFLOW=20
POOL_TIMEOUT=30
POOL_RECYCLE=3600

# Processing
BATCH_SIZE=2000
MAX_WORKERS=6
CHUNK_SIZE=10000

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/excel_to_ssms.log
"""

        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        print("✅ สร้าง .env file")

    # requirements_working.txt (ที่แน่ใจว่าใช้ได้)
    requirements_content = """# Excel to SSMS - Working Requirements
pandas>=2.0.0
sqlalchemy>=2.0.0
openpyxl>=3.1.0
python-dotenv>=1.0.0
tqdm>=4.65.0

# Optional - ติดตั้งแยกหากต้องการ
# pyodbc>=4.0.39
# numpy>=1.24.0
# psutil>=5.9.0
"""

    with open("requirements_working.txt", "w", encoding="utf-8") as f:
        f.write(requirements_content)
    print("✅ สร้าง requirements_working.txt")


def test_basic_functionality():
    """ทดสอบฟังก์ชันพื้นฐาน"""

    print("\n🧪 ทดสอบระบบ...")

    # Test imports
    test_packages = ["pandas", "sqlalchemy", "openpyxl", "dotenv", "tqdm"]
    working_packages = []

    for package in test_packages:
        try:
            __import__(package)
            working_packages.append(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")

    # Test optional packages
    optional_packages = ["pyodbc", "numpy", "psutil"]
    for package in optional_packages:
        try:
            __import__(package)
            working_packages.append(package)
            print(f"✅ {package} (optional)")
        except ImportError:
            print(f"⚠️ {package} (optional - ไม่มีก็ได้)")

    return len(working_packages) >= 5  # ต้องมีอย่างน้อย 5 packages หลัก


def create_quick_test():
    """สร้างไฟล์ทดสอบเร็ว"""

    print("\n🚀 สร้างไฟล์ทดสอบ...")

    test_content = '''#!/usr/bin/env python3
"""
Quick Test - ทดสอบระบบว่าใช้งานได้หรือไม่
"""

def test_imports():
    """ทดสอบ imports"""
    try:
        import pandas as pd
        import sqlalchemy
        import openpyxl
        from dotenv import load_dotenv
        from tqdm import tqdm
        print("✅ Core packages ใช้งานได้")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_excel_basic():
    """ทดสอบการสร้างและอ่าน Excel"""
    try:
        import pandas as pd
        
        # สร้างข้อมูลทดสอบ
        data = {
            "Name": ["John", "Jane", "Bob"],
            "Age": [25, 30, 35],
            "Salary": [50000, 75000, 85000]
        }
        
        df = pd.DataFrame(data)
        test_file = "quick_test.xlsx"
        
        # เขียนไฟล์
        df.to_excel(test_file, index=False)
        
        # อ่านไฟล์
        df_read = pd.read_excel(test_file)
        
        # ลบไฟล์
        import os
        os.remove(test_file)
        
        print("✅ Excel processing ใช้งานได้")
        return True
        
    except Exception as e:
        print(f"❌ Excel test error: {e}")
        return False

def main():
    print("🎯 Excel to SSMS - Quick Test")
    print("=" * 40)
    
    # Test imports
    import_ok = test_imports()
    
    # Test Excel
    excel_ok = test_excel_basic()
    
    if import_ok and excel_ok:
        print("\\n🎉 ระบบพร้อมใช้งาน!")
        print("\\n📋 ขั้นตอนถัดไป:")
        print("  1. แก้ไข .env file (database connection)")
        print("  2. python test_connection.py (ทดสอบ SQL Server)")
        print("  3. python sample_generator.py test (สร้างข้อมูลทดสอบ)")
        print("  4. python excel_to_ssms.py data/samples/test_100.xlsx test_table")
    else:
        print("\\n❌ มีปัญหาบางอย่าง")
        print("💡 ลองรัน: pip install -r requirements_working.txt")

if __name__ == "__main__":
    main()
'''

    with open("quick_test.py", "w", encoding="utf-8") as f:
        f.write(test_content)
    print("✅ สร้าง quick_test.py")


def show_final_instructions():
    """แสดงคำแนะนำสุดท้าย"""

    print("\n" + "=" * 60)
    print("🎊 Excel to SSMS System Setup Complete!")
    print("=" * 60)

    print("\n📋 ขั้นตอนการใช้งาน:")
    print("1. ทดสอบระบบ:")
    print("   python quick_test.py")

    print("\n2. แก้ไข configuration:")
    print("   แก้ไข .env file (database connection info)")

    print("\n3. ทดสอบการเชื่อมต่อ:")
    print("   python test_connection.py")

    print("\n4. สร้างข้อมูลทดสอบ:")
    print("   python sample_generator.py test")

    print("\n5. ทดสอบ import:")
    print("   python excel_to_ssms.py data/samples/test_100.xlsx employees")

    print("\n💡 หากมีปัญหา:")
    print("- ดู logs ใน logs/excel_to_ssms.log")
    print("- รัน python quick_test.py เพื่อดู error")
    print("- ติดตั้ง ODBC Driver 17 for SQL Server")

    print(f"\n🔗 SQL Server Connection:")
    print(f"   Server: 10.73.148.27:1433")
    print(f"   Database: excel_to_db")
    print(f"   User: TS00029")


def main():
    """Main setup function"""

    print("🚀 Excel to SSMS - Complete System Setup")
    print("=" * 60)
    print("กำลังติดตั้งและตั้งค่าระบบให้พร้อมใช้งาน...")

    # 1. ตรวจสอบ Python version
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ต้องใช้ Python 3.8+")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")

    # 2. อัปเกรด pip
    run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip")

    # 3. ติดตั้ง packages
    installed, failed = install_fixed_requirements()

    # 4. สร้างโครงสร้างโปรเจค
    create_project_structure()

    # 5. สร้างไฟล์ configuration
    create_configuration_files()

    # 6. สร้างไฟล์ทดสอบ
    create_quick_test()

    # 7. ทดสอบระบบ
    system_working = test_basic_functionality()

    # 8. แสดงผลลัพธ์
    print(f"\n📊 สรุปการติดตั้ง:")
    print(f"✅ Packages ติดตั้งสำเร็จ: {len(installed)}")
    if failed:
        print(f"❌ Packages ที่ล้มเหลว: {len(failed)} ({', '.join(failed)})")

    if system_working:
        show_final_instructions()
    else:
        print("\n⚠️ ระบบยังไม่พร้อมใช้งาน")
        print("💡 ลองรัน: python quick_test.py เพื่อดูปัญหา")


if __name__ == "__main__":
    main()
