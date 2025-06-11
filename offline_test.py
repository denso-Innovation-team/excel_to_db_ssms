#!/usr/bin/env python3
"""
Offline Excel Processing Test
ทดสอบการประมวลผล Excel โดยไม่ต้องใช้ database
"""

import pandas as pd
from pathlib import Path

def test_excel_only():
    """ทดสอบ Excel processing อย่างเดียว"""
    print("📊 ทดสอบ Excel processing...")
    
    # สร้างข้อมูลทดสอบ
    data = {
        "EmployeeID": ["EMP001", "EMP002", "EMP003"],
        "Name": ["สมชาย ใจดี", "สมหญิง รักดี", "วิชัย เจริญ"],
        "Department": ["IT", "การตลาด", "บัญชี"],
        "Salary": [50000, 75000, 85000]
    }
    
    df = pd.DataFrame(data)
    
    # เขียนไฟล์
    test_file = "offline_test.xlsx"
    df.to_excel(test_file, index=False)
    print(f"✅ สร้างไฟล์: {test_file}")
    
    # อ่านไฟล์
    df_read = pd.read_excel(test_file)
    print(f"✅ อ่านไฟล์: {len(df_read)} แถว")
    
    # แสดงข้อมูล
    print("\n📋 ข้อมูลตัวอย่าง:")
    print(df_read.to_string(index=False))
    
    # ลบไฟล์
    Path(test_file).unlink()
    print(f"✅ ลบไฟล์ทดสอบ")
    
    return True

if __name__ == "__main__":
    test_excel_only()
