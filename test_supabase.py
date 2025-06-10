#!/usr/bin/env python3
"""
Quick Test Runner for Excel to Supabase
ทดสอบการ import ข้อมูลเข้า Supabase
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.main import ExcelToDatabaseProcessor

def quick_test():
    """ทดสอบเร็วด้วยข้อมูลง่ายๆ"""
    
    # Import pandas for creating test data
    import pandas as pd
    from datetime import datetime
    
    print("🚀 Quick Test: Excel → Supabase")
    print("=" * 40)
    
    # สร้างข้อมูลทดสอบเล็กๆ
    test_data = {
        'Name': ['John Doe', 'Jane Smith', 'Bob Wilson', 'Alice Brown'],
        'Age': [25, 30, 35, 28], 
        'Email': ['john@test.com', 'jane@test.com', 'bob@test.com', 'alice@test.com'],
        'Salary': [50000.0, 75000.0, 85000.0, 60000.0],
        'Active': [True, True, False, True],
        'Join Date': ['2023-01-15', '2023-02-20', '2023-03-10', '2023-04-05']
    }
    
    df = pd.DataFrame(test_data)
    test_file = 'quick_test.xlsx'
    df.to_excel(test_file, index=False)
    print(f"✅ สร้างไฟล์ทดสอบ: {test_file}")
    
    # กำหนด type mapping
    type_mapping = {
        "name": "string",
        "age": "integer", 
        "email": "string",
        "salary": "float",
        "active": "boolean",
        "join_date": "datetime"
    }
    
    # ทดสอบ import
    processor = ExcelToDatabaseProcessor(
        excel_file=test_file,
        table_name="quick_test",
        type_mapping=type_mapping
    )
    
    try:
        results = processor.process(create_table=True)
        print("\n" + "="*40)
        print("🎉 SUCCESS!")
        print("="*40) 
        print(f"📊 Import สำเร็จ: {results['inserted_rows']} แถว")
        print(f"⏱️  เวลา: {results['processing_time']:.2f} วินาที")
        print(f"\n🔗 ตรวจสอบใน Supabase:")
        print(f"   → Table Editor → quick_test")
        
        # ลบไฟล์ทดสอบ
        os.remove(test_file)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_with_file(excel_file: str, table_name: str, sheet_name: str = None):
    """ทดสอบกับไฟล์ที่ระบุ"""
    
    print(f"🚀 Testing: {excel_file} → {table_name}")
    print("=" * 50)
    
    # Auto-detect type mapping สำหรับไฟล์ทั่วไป
    type_mapping = {
        # ชื่อ columns ภาษาไทย
        "ชื่อ": "string",
        "นามสกุล": "string", 
        "อายุ": "integer",
        "เงินเดือน": "float",
        "วันที่": "datetime",
        "วันที่เริ่มงาน": "datetime",
        "จำนวน": "integer",
        "ราคา": "float",
        "ยอดรวม": "float",
        "สถานะ": "string",
        
        # ชื่อ columns ภาษาอังกฤษ  
        "name": "string",
        "email": "string",
        "age": "integer", 
        "salary": "float",
        "amount": "float",
        "price": "float",
        "total": "float",
        "date": "datetime",
        "created_at": "datetime",
        "is_active": "boolean",
        "active": "boolean"
    }
    
    processor = ExcelToDatabaseProcessor(
        excel_file=excel_file,
        table_name=table_name,
        sheet_name=sheet_name,
        type_mapping=type_mapping
    )
    
    try:
        results = processor.process(create_table=True)
        
        print("\n" + "="*50)
        print("🎉 SUCCESS!")
        print("="*50)
        print(f"📋 รวม: {results['total_rows']:,} แถว")
        print(f"✅ Import: {results['inserted_rows']:,} แถว") 
        print(f"⏱️  เวลา: {results['processing_time']:.2f} วินาที")
        print(f"🚀 ความเร็ว: {results['inserted_rows']/results['processing_time']:.0f} แถว/วินาที")
        
        print(f"\n🔗 ตรวจสอบใน Supabase:")
        print(f"   → Table Editor → {table_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main CLI"""
    
    if len(sys.argv) == 1:
        # No arguments - run quick test
        quick_test()
        
    elif len(sys.argv) == 2 and sys.argv[1] == "test":
        # Quick test mode
        quick_test()
        
    elif len(sys.argv) >= 3:
        # Custom file test
        excel_file = sys.argv[1]
        table_name = sys.argv[2]
        sheet_name = sys.argv[3] if len(sys.argv) > 3 else None
        
        if not os.path.exists(excel_file):
            print(f"❌ ไม่พบไฟล์: {excel_file}")
            sys.exit(1)
            
        test_with_file(excel_file, table_name, sheet_name)
        
    else:
        print("""
🎯 Excel to Supabase Test Runner

Usage:
  python test_supabase.py                           # Quick test
  python test_supabase.py test                      # Quick test  
  python test_supabase.py <file.xlsx> <table_name>  # Custom test
  python test_supabase.py <file.xlsx> <table_name> <sheet_name>  # With sheet

Examples:
  python test_supabase.py                                    # ทดสอบเร็ว
  python test_supabase.py data/samples/sales_1000.xlsx sales # ทดสอบไฟล์ยอดขาย
  python test_supabase.py data.xlsx employees Employees      # ระบุ sheet
        """)

if __name__ == "__main__":
    main()
