#!/usr/bin/env python3
"""
Excel Mockup Data Generator
สร้างไฟล์ Excel พร้อมข้อมูล mockup สำหรับทดสอบ Supabase integration
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from pathlib import Path
import os


class ExcelMockupGenerator:
    """Generator สำหรับสร้างข้อมูล mockup หลากหลายรูปแบบ"""

    def __init__(self):
        self.setup_directories()

        # Sample data pools
        self.first_names = [
            "สมชาย",
            "สมหญิง",
            "นายพร",
            "นางสาวลักษณ์",
            "วิชัย",
            "สุนีย์",
            "ประเสริฐ",
            "จิราพร",
            "อนุชา",
            "พิมพ์ชนก",
        ]
        self.last_names = [
            "ใจดี",
            "รักษ์ดี",
            "สุขสวัสดิ์",
            "เจริญผล",
            "มั่นคง",
            "ยั่งยืน",
            "สมบูรณ์",
            "เจริญรุ่งเรือง",
            "ศรีสุข",
            "ทองดี",
        ]
        self.companies = [
            "บริษัท ABC",
            "บริษัท XYZ",
            "ห้างหุ้นส่วน DEF",
            "บจก. GHI",
            "สหกรณ์ JKL",
            "มหาวิทยาลัย MNO",
        ]
        self.products = [
            "สินค้า A",
            "สินค้า B",
            "บริการ C",
            "อุปกรณ์ D",
            "ซอฟต์แวร์ E",
            "ฮาร์ดแวร์ F",
        ]
        self.departments = ["ขาย", "การตลาด", "IT", "บัญชี", "HR", "การผลิต", "วิจัยพัฒนา"]
        self.provinces = [
            "กรุงเทพฯ",
            "เชียงใหม่",
            "ขอนแก่น",
            "สงขลา",
            "ระยอง",
            "ชลบุรี",
            "นครราชสีมา",
        ]

    def setup_directories(self):
        """สร้าง directories สำหรับเก็บไฟล์"""
        Path("data/samples").mkdir(parents=True, exist_ok=True)

    def generate_sales_data(self, rows: int = 10000) -> pd.DataFrame:
        """สร้างข้อมูลยอดขาย"""

        data = []
        start_date = datetime.now() - timedelta(days=365)

        for i in range(rows):
            record = {
                "id": i + 1,
                "วันที่": start_date + timedelta(days=random.randint(0, 365)),
                "ชื่อลูกค้า": f"{random.choice(self.first_names)} {random.choice(self.last_names)}",
                "บริษัท": random.choice(self.companies),
                "สินค้า": random.choice(self.products),
                "จำนวน": random.randint(1, 100),
                "ราคาต่อหน่วย": round(random.uniform(10, 10000), 2),
                "ยอดรวม": 0,  # จะคำนวณทีหลัง
                "พื้นที่": random.choice(self.provinces),
                "สถานะ": random.choice(["ขายแล้ว", "รอการชำระ", "ยกเลิก", "ส่งมอบแล้ว"]),
                "ช่องทางขาย": random.choice(["Online", "หน้าร้าน", "โทรศัพท์", "ตัวแทนขาย"]),
                "หมายเหตุ": random.choice(
                    ["", "ลูกค้า VIP", "ส่วนลด 10%", "ซื้อครบ 5 ชิ้น", ""]
                ),
            }

            # คำนวณยอดรวม
            record["ยอดรวม"] = record["จำนวน"] * record["ราคาต่อหน่วย"]

            # เพิ่ม discount สำหรับบางรายการ
            if "ส่วนลด" in record["หมายเหตุ"]:
                record["ยอดรวม"] *= 0.9

            data.append(record)

        return pd.DataFrame(data)

    def generate_employee_data(self, rows: int = 1000) -> pd.DataFrame:
        """สร้างข้อมูลพนักงาน"""

        data = []

        for i in range(rows):
            hire_date = datetime.now() - timedelta(days=random.randint(30, 3650))

            record = {
                "รหัสพนักงาน": f"EMP{i+1:04d}",
                "ชื่อ": random.choice(self.first_names),
                "นามสกุล": random.choice(self.last_names),
                "แผนก": random.choice(self.departments),
                "ตำแหน่ง": random.choice(["พนักงาน", "หัวหน้าทีม", "ผู้จัดการ", "ผู้อำนวยการ"]),
                "เงินเดือน": random.randint(15000, 150000),
                "วันที่เริ่มงาน": hire_date,
                "อายุ": random.randint(22, 60),
                "เพศ": random.choice(["ชาย", "หญิง"]),
                "จังหวัด": random.choice(self.provinces),
                "โทรศัพท์": f"08{random.randint(10000000, 99999999)}",
                "อีเมล": f"emp{i+1}@company.co.th",
                "สถานะ": random.choice(["ทำงานอยู่", "ลาออก", "เกษียณ"]),
            }

            data.append(record)

        return pd.DataFrame(data)

    def generate_inventory_data(self, rows: int = 5000) -> pd.DataFrame:
        """สร้างข้อมูลสินค้าคงคลัง"""

        data = []

        for i in range(rows):
            record = {
                "รหัสสินค้า": f"PRD{i+1:05d}",
                "ชื่อสินค้า": f"{random.choice(self.products)} รุ่น {random.choice(['A', 'B', 'C', 'Pro', 'Max'])}",
                "หมวดหมู่": random.choice(
                    ["อิเล็กทรอนิกส์", "เสื้อผ้า", "อาหาร", "ของใช้", "เครื่องมือ"]
                ),
                "คงเหลือ": random.randint(0, 1000),
                "ราคาทุน": round(random.uniform(50, 5000), 2),
                "ราคาขาย": 0,  # จะคำนวณ
                "คลังสินค้า": random.choice(["คลัง A", "คลัง B", "คลัง C"]),
                "วันที่อัพเดท": datetime.now() - timedelta(days=random.randint(0, 30)),
                "ผู้จำหน่าย": random.choice(self.companies),
                "หน่วยนับ": random.choice(["ชิ้น", "กล่อง", "แพ็ค", "โหล"]),
                "จุดสั่งซื้อ": random.randint(10, 100),
                "สถานะ": random.choice(["พร้อมขาย", "หมด", "ใกล้หมด", "ไม่ใช้แล้ว"]),
            }

            # คำนวณราคาขาย (markup 30-100%)
            markup = random.uniform(1.3, 2.0)
            record["ราคาขาย"] = round(record["ราคาทุน"] * markup, 2)

            data.append(record)

        return pd.DataFrame(data)

    def generate_financial_data(self, rows: int = 8000) -> pd.DataFrame:
        """สร้างข้อมูลการเงิน"""

        data = []
        start_date = datetime.now() - timedelta(days=365)

        for i in range(rows):
            record = {
                "เลขที่เอกสาร": f"FIN{datetime.now().year}{i+1:06d}",
                "วันที่": start_date + timedelta(days=random.randint(0, 365)),
                "ประเภท": random.choice(
                    ["รายรับ", "รายจ่าย", "โอนเงิน", "ดอกเบียรับ", "ค่าใช้จ่าย"]
                ),
                "หมวดหมู่": random.choice(
                    ["ขายสินค้า", "ค่าเช่า", "เงินเดือน", "ไฟฟ้า", "การตลาด", "วัตถุดิบ"]
                ),
                "จำนวนเงิน": round(random.uniform(-500000, 1000000), 2),
                "ผู้รับ_ผู้จ่าย": random.choice(self.companies + self.first_names),
                "บัญชี": random.choice(["เงินสด", "ธนาคาร A", "ธนาคาร B", "บัตรเครดิต"]),
                "อ้างอิง": f"REF{random.randint(100000, 999999)}",
                "ผู้อนุมัติ": random.choice(self.first_names),
                "สถานะ": random.choice(["อนุมัติแล้ว", "รอการอนุมัติ", "ยกเลิก"]),
                "หมายเหตุ": random.choice(["", "เงินทอน", "ภาษี 7%", "หัก ณ ที่จ่าย 3%", ""]),
            }

            data.append(record)

        return pd.DataFrame(data)

    def generate_mixed_data_types(self, rows: int = 3000) -> pd.DataFrame:
        """สร้างข้อมูลที่มี data types หลากหลาย (สำหรับทดสอบ type inference)"""

        data = []

        for i in range(rows):
            record = {
                "id": i + 1,
                "text_column": f"ข้อความ {i+1}",
                "number_column": random.randint(1, 1000),
                "float_column": round(random.uniform(0, 100), 3),
                "date_column": datetime.now() - timedelta(days=random.randint(0, 1000)),
                "boolean_column": random.choice([True, False, "Yes", "No", "1", "0"]),
                "mixed_column": random.choice([1, "2", 3.0, "text", None]),
                "percentage": f"{random.randint(0, 100)}%",
                "currency": f"฿{random.randint(100, 100000):,}",
                "phone": f"0{random.randint(10000000, 99999999)}",
                "email": f"user{i+1}@example.com",
                "url": f"https://example.com/page{i+1}",
                "json_like": f'{{"key": "value{i+1}", "number": {random.randint(1, 100)}}}',
                "empty_column": (
                    random.choice([None, "", "N/A", "NULL"])
                    if i % 10 == 0
                    else f"data{i+1}"
                ),
                "unicode_text": f"Unicode: {random.choice(['😀', '🎉', '✅', '❌', '⚡', '🚀'])} ข้อความ",
            }

            data.append(record)

        return pd.DataFrame(data)

    def create_multiple_sheets_file(self) -> str:
        """สร้างไฟล์ Excel ที่มีหลาย sheets"""

        file_path = "data/samples/multiple_sheets_data.xlsx"

        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            # Sheet 1: Sales Data
            sales_df = self.generate_sales_data(2000)
            sales_df.to_excel(writer, sheet_name="Sales", index=False)

            # Sheet 2: Employee Data
            employee_df = self.generate_employee_data(500)
            employee_df.to_excel(writer, sheet_name="Employees", index=False)

            # Sheet 3: Products
            inventory_df = self.generate_inventory_data(1000)
            inventory_df.to_excel(writer, sheet_name="Inventory", index=False)

            # Sheet 4: Summary (aggregated data)
            summary_df = pd.DataFrame(
                {
                    "เดือน": ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย."],
                    "ยอดขาย": [random.randint(100000, 1000000) for _ in range(6)],
                    "ค่าใช้จ่าย": [random.randint(50000, 500000) for _ in range(6)],
                    "กำไร": [random.randint(20000, 200000) for _ in range(6)],
                }
            )
            summary_df.to_excel(writer, sheet_name="Summary", index=False)

        return file_path

    def generate_sample_files(self) -> dict:
        """สร้างไฟล์ตัวอย่างหลากหลายประเภท"""

        files_created = {}

        print("🚀 กำลังสร้างไฟล์ตัวอย่าง...")

        # 1. Sales Data (ขนาดกลาง)
        print("📊 สร้างข้อมูลยอดขาย...")
        sales_df = self.generate_sales_data(15000)
        sales_path = "data/samples/sales_data_15k.xlsx"
        sales_df.to_excel(sales_path, index=False)
        files_created["sales"] = sales_path

        # 2. Employee Data (ขนาดเล็ก)
        print("👥 สร้างข้อมูลพนักงาน...")
        employee_df = self.generate_employee_data(1200)
        employee_path = "data/samples/employee_data_1k.xlsx"
        employee_df.to_excel(employee_path, index=False)
        files_created["employees"] = employee_path

        # 3. Large Dataset (ทดสอบ performance)
        print("🗂️ สร้างข้อมูลขนาดใหญ่...")
        large_df = self.generate_sales_data(50000)
        large_path = "data/samples/large_dataset_50k.xlsx"
        large_df.to_excel(large_path, index=False)
        files_created["large"] = large_path

        # 4. Mixed Data Types (ทดสอบ type inference)
        print("🔀 สร้างข้อมูลประเภทผสม...")
        mixed_df = self.generate_mixed_data_types(5000)
        mixed_path = "data/samples/mixed_types_5k.xlsx"
        mixed_df.to_excel(mixed_path, index=False)
        files_created["mixed"] = mixed_path

        # 5. Financial Data
        print("💰 สร้างข้อมูลการเงิน...")
        financial_df = self.generate_financial_data(8000)
        financial_path = "data/samples/financial_data_8k.xlsx"
        financial_df.to_excel(financial_path, index=False)
        files_created["financial"] = financial_path

        # 6. Multiple Sheets File
        print("📋 สร้างไฟล์หลาย sheets...")
        multi_path = self.create_multiple_sheets_file()
        files_created["multi_sheets"] = multi_path

        # 7. Small Test File (สำหรับทดสอบเร็ว)
        print("⚡ สร้างไฟล์ทดสอบเล็ก...")
        small_df = self.generate_sales_data(100)
        small_path = "data/samples/small_test_100.xlsx"
        small_df.to_excel(small_path, index=False)
        files_created["small"] = small_path

        return files_created


def main():
    """CLI สำหรับสร้างไฟล์ตัวอย่าง"""
    import sys

    generator = ExcelMockupGenerator()

    if len(sys.argv) < 2:
        print(
            """
🎯 Excel Mockup Generator

Commands:
  all                    - สร้างไฟล์ตัวอย่างทั้งหมด
  sales [rows]          - สร้างข้อมูลยอดขาย
  employee [rows]       - สร้างข้อมูลพนักงาน  
  inventory [rows]      - สร้างข้อมูลสินค้าคงคลัง
  financial [rows]      - สร้างข้อมูลการเงิน
  mixed [rows]          - สร้างข้อมูลประเภทผสม
  test                  - สร้างไฟล์ทดสอบเล็ก (100 rows)

Examples:
  python excel_generator.py all
  python excel_generator.py sales 10000
  python excel_generator.py test
        """
        )
        sys.exit(1)

    command = sys.argv[1]
    rows = int(sys.argv[2]) if len(sys.argv) > 2 else None

    if command == "all":
        files = generator.generate_sample_files()
        print("\n✅ ไฟล์ตัวอย่างที่สร้างแล้ว:")
        for name, path in files.items():
            file_size = os.path.getsize(path) / 1024 / 1024
            print(f"  • {name}: {path} ({file_size:.1f}MB)")

        print(f"\n🚀 ทดสอบได้เลย:")
        print(f"python run_supabase.py {files['small']} test_table")

    elif command == "sales":
        rows = rows or 10000
        df = generator.generate_sales_data(rows)
        path = f"data/samples/sales_{rows}.xlsx"
        df.to_excel(path, index=False)
        print(f"✅ สร้างแล้ว: {path}")

    elif command == "employee":
        rows = rows or 1000
        df = generator.generate_employee_data(rows)
        path = f"data/samples/employee_{rows}.xlsx"
        df.to_excel(path, index=False)
        print(f"✅ สร้างแล้ว: {path}")

    elif command == "inventory":
        rows = rows or 5000
        df = generator.generate_inventory_data(rows)
        path = f"data/samples/inventory_{rows}.xlsx"
        df.to_excel(path, index=False)
        print(f"✅ สร้างแล้ว: {path}")

    elif command == "financial":
        rows = rows or 8000
        df = generator.generate_financial_data(rows)
        path = f"data/samples/financial_{rows}.xlsx"
        df.to_excel(path, index=False)
        print(f"✅ สร้างแล้ว: {path}")

    elif command == "mixed":
        rows = rows or 3000
        df = generator.generate_mixed_data_types(rows)
        path = f"data/samples/mixed_{rows}.xlsx"
        df.to_excel(path, index=False)
        print(f"✅ สร้างแล้ว: {path}")

    elif command == "test":
        df = generator.generate_sales_data(100)
        path = "data/samples/test_100.xlsx"
        df.to_excel(path, index=False)
        print(f"✅ ไฟล์ทดสอบ: {path}")
        print(f"🚀 รันทดสอบ: python run_supabase.py {path} test_table")

    else:
        print(f"❌ Unknown command: {command}")


if __name__ == "__main__":
    main()
