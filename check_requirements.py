#!/usr/bin/env python3
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
        print(f"\n❌ Missing packages: {missing}")
        print("\n🔧 Install commands:")
        for package in missing:
            print(f"  pip install {package}")
        
        # Special case for pyodbc
        if "pyodbc" in missing:
            print("\n💡 If pyodbc fails to install:")
            print("  1. Download Microsoft C++ Build Tools")
            print("  2. Or use conda: conda install pyodbc")
            print("  3. Or use pre-compiled wheel")
    else:
        print("\n🎉 All packages are installed!")

if __name__ == "__main__":
    main()
