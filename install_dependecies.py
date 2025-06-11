#!/usr/bin/env python3
"""
Excel to SSMS - Auto Installation Script
ติดตั้ง dependencies อัตโนมัติพร้อมแก้ไขปัญหาที่พบบ่อย
"""

import subprocess
import sys
import platform
import os
from pathlib import Path


def check_python_version():
    """ตรวจสอบ Python version"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ต้องใช้ Python 3.8 หรือสูงกว่า")
        return False

    print("✅ Python version เหมาะสม")
    return True


def install_core_packages():
    """ติดตั้ง packages หลักทีละตัว"""

    # Core packages ที่จำเป็น (เรียงตามความสำคัญ)
    packages = [
        "pandas>=2.0.0",
        "sqlalchemy>=2.0.0",
        "openpyxl>=3.1.0",
        "python-dotenv>=1.0.0",
        "tqdm>=4.65.0",
        "pyodbc>=4.0.39",  # อาจมีปัญหาในบางระบบ
        "numpy>=1.24.0",
        "xlrd>=2.0.1",
        "psutil>=5.9.0",
    ]

    installed = []
    failed = []

    for package in packages:
        package_name = package.split(">=")[0]
        print(f"\n📦 กำลังติดตั้ง {package_name}...")

        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", package],
                check=True,
                capture_output=True,
                text=True,
            )

            print(f"  ✅ {package_name} ติดตั้งสำเร็จ")
            installed.append(package_name)

        except subprocess.CalledProcessError as e:
            print(f"  ❌ {package_name} ติดตั้งล้มเหลว")
            print(f"     Error: {e.stderr}")
            failed.append(package_name)

    return installed, failed


def handle_pyodbc_issues():
    """แก้ปัญหา pyodbc ที่พบบ่อย"""
    print("\n🔧 กำลังแก้ปัญหา pyodbc...")

    system = platform.system().lower()

    if system == "windows":
        print("  💡 Windows: ตรวจสอบ ODBC Driver 17 for SQL Server")
        print(
            "     Download: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server"
        )

    elif system == "linux":
        print("  💡 Linux: ติดตั้ง ODBC Driver")
        print("     Ubuntu/Debian: apt-get install unixodbc-dev")
        print("     CentOS/RHEL: yum install unixODBC-devel")

    elif system == "darwin":  # macOS
        print("  💡 macOS: ใช้ brew ติดตั้ง")
        print("     brew install unixodbc")

    # ลองติดตั้ง pyodbc หลายวิธี
    methods = [
        [sys.executable, "-m", "pip", "install", "pyodbc"],
        [sys.executable, "-m", "pip", "install", "pyodbc", "--no-cache-dir"],
        [sys.executable, "-m", "pip", "install", "pyodbc", "--force-reinstall"],
    ]

    for i, method in enumerate(methods, 1):
        try:
            print(f"  🔄 ลองวิธีที่ {i}...")
            subprocess.run(method, check=True, capture_output=True)
            print(f"  ✅ pyodbc ติดตั้งสำเร็จด้วยวิธีที่ {i}")
            return True
        except subprocess.CalledProcessError:
            continue

    print("  ❌ ไม่สามารถติดตั้ง pyodbc ได้")
    return False


def test_imports():
    """ทดสอบ import packages"""
    print("\n🧪 ทดสอบ imports...")

    test_packages = [
        ("pandas", "pandas"),
        ("sqlalchemy", "sqlalchemy"),
        ("openpyxl", "openpyxl"),
        ("dotenv", "python-dotenv"),
        ("tqdm", "tqdm"),
        ("pyodbc", "pyodbc"),
        ("numpy", "numpy"),
    ]

    success = 0
    total = len(test_packages)

    for import_name, package_name in test_packages:
        try:
            __import__(import_name)
            print(f"  ✅ {package_name}")
            success += 1
        except ImportError:
            print(f"  ❌ {package_name}")

    print(f"\n📊 ผลการทดสอบ: {success}/{total} packages")
    return success == total


def create_minimal_requirements():
    """สร้าง requirements.txt ขั้นต่ำ"""
    minimal_requirements = """# Excel to SSMS - Minimal Requirements
# ใช้ไฟล์นี้หากมีปัญหาติดตั้ง

pandas>=2.0.0
sqlalchemy>=2.0.0
openpyxl>=3.1.0
python-dotenv>=1.0.0
tqdm>=4.65.0

# Optional (ติดตั้งแยกหากจำเป็น)
# pyodbc>=4.0.39
# numpy>=1.24.0
# psutil>=5.9.0
"""

    with open("requirements_minimal.txt", "w", encoding="utf-8") as f:
        f.write(minimal_requirements)

    print("  📄 สร้าง requirements_minimal.txt")


def setup_directories():
    """สร้างโฟลเดอร์ที่จำเป็น"""
    print("\n📁 สร้างโฟลเดอร์...")

    directories = ["logs", "data/samples", "src/config", "src/processors", "src/utils"]

    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {dir_path}")


def create_env_template():
    """สร้างไฟล์ .env template"""
    if not os.path.exists(".env"):
        env_template = """# Excel to SSMS Configuration
# กรุณาแก้ไขค่าต่างๆ ให้ถูกต้อง

# SQL Server Configuration
DB_HOST=10.73.148.27
DB_NAME=excel_to_db
DB_USER=TS00029
DB_PASSWORD=Thammaphon@TS00029
DB_TYPE=mssql
DB_DRIVER=ODBC Driver 17 for SQL Server

# Connection Pool Settings
POOL_SIZE=10
MAX_OVERFLOW=20
POOL_TIMEOUT=30
POOL_RECYCLE=3600

# Processing Configuration
BATCH_SIZE=2000
MAX_WORKERS=6
CHUNK_SIZE=10000

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/excel_to_ssms.log
LOG_MAX_SIZE=10485760
LOG_BACKUP_COUNT=5
"""

        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_template)

        print("  📄 สร้าง .env template")
    else:
        print("  ⏭️ .env มีอยู่แล้ว")


def main():
    """Main installation function"""

    print("🚀 Excel to SSMS - Auto Installation")
    print("=" * 50)

    # 1. ตรวจสอบ Python version
    if not check_python_version():
        sys.exit(1)

    # 2. อัปเกรด pip
    print("\n📦 อัปเกรด pip...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
            check=True,
            capture_output=True,
        )
        print("  ✅ pip อัปเกรดสำเร็จ")
    except subprocess.CalledProcessError:
        print("  ⚠️ ไม่สามารถอัปเกรด pip ได้")

    # 3. ติดตั้ง packages
    installed, failed = install_core_packages()

    # 4. แก้ปัญหา pyodbc หากจำเป็น
    if "pyodbc" in failed:
        handle_pyodbc_issues()

    # 5. ทดสอบ imports
    import_success = test_imports()

    # 6. สร้างไฟล์และโฟลเดอร์
    setup_directories()
    create_env_template()
    create_minimal_requirements()

    # 7. สรุปผลลัพธ์
    print("\n" + "=" * 50)
    print("📊 สรุปการติดตั้ง")
    print("=" * 50)

    print(f"✅ ติดตั้งสำเร็จ: {len(installed)} packages")
    if installed:
        print(f"   {', '.join(installed)}")

    if failed:
        print(f"❌ ติดตั้งล้มเหลว: {len(failed)} packages")
        print(f"   {', '.join(failed)}")

    if import_success:
        print("\n🎉 ระบบพร้อมใช้งาน!")
        print("\n📋 ขั้นตอนถัดไป:")
        print("  1. แก้ไข .env file")
        print("  2. python test_connection.py")
        print("  3. python sample_generator.py test")
        print("  4. python excel_to_ssms.py data/samples/test_100.xlsx test_table")
    else:
        print("\n⚠️ มีปัญหาบาง packages")
        print("💡 ลองใช้:")
        print("  pip install -r requirements_minimal.txt")
        print("  หรือติดตั้งทีละตัว")

    if "pyodbc" in failed:
        print(f"\n🔧 สำหรับ pyodbc:")
        print("  - ติดตั้ง ODBC Driver 17 for SQL Server")
        print("  - ตรวจสอบ compiler (Windows: Visual Studio Build Tools)")
        print("  - ลองใช้ conda: conda install pyodbc")


if __name__ == "__main__":
    main()
