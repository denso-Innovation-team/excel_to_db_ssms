#!/usr/bin/env python3
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
        print("\n🎉 ระบบพร้อมใช้งาน!")
        print("\n📋 ขั้นตอนถัดไป:")
        print("  1. แก้ไข .env file (database connection)")
        print("  2. python test_connection.py (ทดสอบ SQL Server)")
        print("  3. python sample_generator.py test (สร้างข้อมูลทดสอบ)")
        print("  4. python excel_to_ssms.py data/samples/test_100.xlsx test_table")
    else:
        print("\n❌ มีปัญหาบางอย่าง")
        print("💡 ลองรัน: pip install -r requirements_working.txt")

if __name__ == "__main__":
    main()
