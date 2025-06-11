#!/usr/bin/env python3
"""
Sample Data Generator for Excel to SSMS
สร้างข้อมูลตัวอย่างสำหรับทดสอบระบบ import
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from pathlib import Path
import sys


class SSMSSampleGenerator:
    """Sample data generator optimized for SSMS testing"""

    def __init__(self):
        self.setup_directories()
        self.setup_sample_data()

    def setup_directories(self):
        """สร้าง directories สำหรับเก็บไฟล์"""
        Path("data/samples").mkdir(parents=True, exist_ok=True)

    def setup_sample_data(self):
        """ตั้งค่าข้อมูล sample pools"""

        # Thai names
        self.thai_first_names = [
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
            "ธนากร",
            "สุภาพร",
            "รัตนา",
            "เจษฎา",
            "นันทนา",
            "ภานุพงษ์",
            "ธัญญา",
            "กิตติพงษ์",
        ]

        self.thai_last_names = [
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
            "สมใจ",
            "ปราณี",
            "วิไลลักษณ์",
            "ธีระชัย",
            "มานิต",
            "สุขสันต์",
            "เกียรติคุณ",
            "บุญเลิศ",
        ]

        # Company data
        self.companies = [
            "บริษัท เทคโนโลยี จำกัด",
            "บริษัท การค้า จำกัด",
            "ห้างหุ้นส่วน สมบูรณ์",
            "บจก. นวัตกรรม",
            "สหกรณ์ เกษตรกร",
            "มหาวิทยาลัย เทคโนโลยี",
            "บริษัท ผลิตภัณฑ์ จำกัด",
            "บริษัท บริการ จำกัด",
        ]

        # Products
        self.products = [
            "คอมพิวเตอร์ โน้ตบุ๊ค",
            "โทรศัพท์ มือถือ",
            "เครื่องพิมพ์ เลเซอร์",
            "จอภาพ LED",
            "คีย์บอร์ด เมคานิคัล",
            "เมาส์ ไร้สาย",
            "ซอฟต์แวร์ บัญชี",
            "ระบบ รักษาความปลอดภัย",
        ]

        # Departments
        self.departments = [
            "ฝ่ายขาย",
            "ฝ่ายการตลาด",
            "ฝ่ายเทคโนโลยี",
            "ฝ่ายบัญชี",
            "ฝ่ายทรัพยากรบุคคล",
            "ฝ่ายการผลิต",
            "ฝ่ายวิจัยพัฒนา",
            "ฝ่ายสนับสนุน",
        ]

        # Provinces
        self.provinces = [
            "กรุงเทพมหานคร",
            "เชียงใหม่",
            "ขอนแก่น",
            "สงขลา",
            "ระยอง",
            "ชลบุรี",
            "นครราชสีมา",
            "เชียงราย",
            "อุดรธานี",
            "สุราษฎร์ธานี",
        ]

    def generate_employee_data(self, rows: int = 1000) -> pd.DataFrame:
        """สร้างข้อมูลพนักงาน - เหมาะสำหรับ SSMS"""

        data = []

        for i in range(rows):
            hire_date = datetime.now() - timedelta(days=random.randint(30, 3650))

            # สร้างเงินเดือนตามตำแหน่ง
            position_salary_map = {
                "พนักงาน": (25000, 45000),
                "หัวหน้าทีม": (45000, 70000),
                "ผู้จัดการ": (70000, 120000),
                "ผู้อำนวยการ": (120000, 200000),
            }

            position = random.choice(list(position_salary_map.keys()))
            salary_range = position_salary_map[position]
            salary = random.randint(salary_range[0], salary_range[1])

            record = {
                "EmployeeID": f"EMP{i+1:05d}",
                "FirstName": random.choice(self.thai_first_names),
                "LastName": random.choice(self.thai_last_names),
                "FullName": "",  # จะต่อทีหลัง
                "Email": f"employee{i+1:05d}@company.co.th",
                "Department": random.choice(self.departments),
                "Position": position,
                "Salary": salary,
                "HireDate": hire_date,
                "IsActive": random.choice([True, True, True, False]),  # 75% active
                "Age": random.randint(22, 60),
                "Gender": random.choice(["ชาย", "หญิง"]),
                "Province": random.choice(self.provinces),
                "Phone": f"0{random.randint(800000000, 999999999)}",
                "BonusPercentage": random.randint(0, 20),
                "PerformanceScore": round(random.uniform(1.0, 5.0), 2),
                "LastUpdated": datetime.now(),
            }

            # สร้าง FullName
            record["FullName"] = f"{record['FirstName']} {record['LastName']}"

            data.append(record)

        return pd.DataFrame(data)

    def generate_sales_data(self, rows: int = 5000) -> pd.DataFrame:
        """สร้างข้อมูลยอดขาย - เหมาะสำหรับ SSMS"""

        data = []
        start_date = datetime.now() - timedelta(days=365)

        for i in range(rows):
            sale_date = start_date + timedelta(days=random.randint(0, 365))

            # Random product selection
            product = random.choice(self.products)
            quantity = random.randint(1, 50)
            unit_price = random.randint(1000, 50000)

            # Calculate totals
            subtotal = quantity * unit_price
            discount_percent = random.choice([0, 5, 10, 15, 20])
            discount_amount = subtotal * (discount_percent / 100)
            tax_amount = (subtotal - discount_amount) * 0.07  # VAT 7%
            total_amount = subtotal - discount_amount + tax_amount

            record = {
                "SaleID": f"SAL{i+1:06d}",
                "SaleDate": sale_date,
                "CustomerName": f"{random.choice(self.thai_first_names)} {random.choice(self.thai_last_names)}",
                "CompanyName": random.choice(self.companies),
                "ProductName": product,
                "ProductCategory": self._get_product_category(product),
                "Quantity": quantity,
                "UnitPrice": unit_price,
                "Subtotal": subtotal,
                "DiscountPercent": discount_percent,
                "DiscountAmount": discount_amount,
                "TaxAmount": round(tax_amount, 2),
                "TotalAmount": round(total_amount, 2),
                "Province": random.choice(self.provinces),
                "SalesChannel": random.choice(
                    ["Online", "หน้าร้าน", "โทรศัพท์", "ตัวแทนขาย"]
                ),
                "Status": random.choice(["ขายแล้ว", "รอการชำระ", "ยกเลิก", "ส่งมอบแล้ว"]),
                "SalespersonID": f"EMP{random.randint(1, 100):05d}",
                "Notes": random.choice(
                    ["", "ลูกค้า VIP", "ส่วนลด พิเศษ", "ซื้อครบตามเป้า", ""]
                ),
                "CreatedDate": datetime.now(),
            }

            data.append(record)

        return pd.DataFrame(data)

    def _get_product_category(self, product_name: str) -> str:
        """จำแนกหมวดหมู่สินค้า"""
        if any(word in product_name for word in ["คอมพิวเตอร์", "โน้ตบุ๊ค", "จอภาพ"]):
            return "คอมพิวเตอร์"
        elif any(word in product_name for word in ["โทรศัพท์", "มือถือ"]):
            return "มือถือ"
        elif any(word in product_name for word in ["เครื่องพิมพ์", "คีย์บอร์ด", "เมาส์"]):
            return "อุปกรณ์"
        elif "ซอฟต์แวร์" in product_name:
            return "ซอฟต์แวร์"
        else:
            return "อื่นๆ"

    def generate_inventory_data(self, rows: int = 2000) -> pd.DataFrame:
        """สร้างข้อมูลสินค้าคงคลัง"""

        data = []

        for i in range(rows):
            product = random.choice(self.products)
            cost_price = random.randint(500, 25000)
            selling_price = cost_price * random.uniform(1.2, 2.5)  # Markup 20-150%

            record = {
                "ProductID": f"PRD{i+1:06d}",
                "ProductName": f"{product} รุ่น {random.choice(['A', 'B', 'C', 'Pro', 'Max', 'Plus'])}",
                "ProductCategory": self._get_product_category(product),
                "Supplier": random.choice(self.companies),
                "CurrentStock": random.randint(0, 500),
                "MinimumStock": random.randint(10, 50),
                "MaximumStock": random.randint(100, 1000),
                "CostPrice": cost_price,
                "SellingPrice": round(selling_price, 2),
                "ProfitMargin": round(
                    ((selling_price - cost_price) / cost_price) * 100, 2
                ),
                "Warehouse": random.choice(["คลัง A", "คลัง B", "คลัง C", "คลังหลัก"]),
                "Location": f"แถว {random.randint(1, 20)}-{random.randint(1, 10)}",
                "Unit": random.choice(["ชิ้น", "กล่อง", "แพ็ค", "โหล", "ตัว"]),
                "LastUpdated": datetime.now() - timedelta(days=random.randint(0, 30)),
                "Status": random.choice(["พร้อมขาย", "หมด", "ใกล้หมด", "ไม่ใช้แล้ว"]),
                "IsActive": random.choice([True, True, True, False]),
                "CreatedDate": datetime.now() - timedelta(days=random.randint(30, 365)),
            }

            data.append(record)

        return pd.DataFrame(data)

    def generate_financial_data(self, rows: int = 3000) -> pd.DataFrame:
        """สร้างข้อมูลการเงิน"""

        data = []
        start_date = datetime.now() - timedelta(days=365)

        transaction_types = [
            ("รายรับ", "ขายสินค้า", 1000, 500000),
            ("รายรับ", "ดอกเบียรับ", 100, 10000),
            ("รายจ่าย", "ค่าเช่า", -50000, -200000),
            ("รายจ่าย", "เงินเดือน", -100000, -2000000),
            ("รายจ่าย", "ค่าไฟฟ้า", -5000, -50000),
            ("รายจ่าย", "ค่าการตลาด", -10000, -200000),
            ("รายจ่าย", "วัตถุดิบ", -50000, -1000000),
        ]

        for i in range(rows):
            trans_type, category, min_amount, max_amount = random.choice(
                transaction_types
            )
            amount = random.randint(min_amount, max_amount)

            record = {
                "TransactionID": f"TXN{datetime.now().year}{i+1:06d}",
                "TransactionDate": start_date + timedelta(days=random.randint(0, 365)),
                "TransactionType": trans_type,
                "Category": category,
                "Amount": amount,
                "Description": f"{category} - {random.choice(['ปกติ', 'พิเศษ', 'เร่งด่วน'])}",
                "PayeeReceiver": random.choice(self.companies + self.thai_first_names),
                "AccountName": random.choice(
                    ["เงินสด", "ธนาคาร กสิกร", "ธนาคาร กรุงเทพ", "บัตรเครดิต"]
                ),
                "ReferenceNumber": f"REF{random.randint(100000, 999999)}",
                "ApprovedBy": f"{random.choice(self.thai_first_names)} {random.choice(self.thai_last_names)}",
                "Status": random.choice(["อนุมัติแล้ว", "รอการอนุมัติ", "ยกเลิก", "ชำระแล้ว"]),
                "TaxAmount": abs(amount) * 0.07 if amount > 0 else 0,
                "Notes": random.choice(
                    ["", "เงินทอน", "ภาษี 7%", "หัก ณ ที่จ่าย 3%", "ค่าธรรมเนียม"]
                ),
                "CreatedDate": datetime.now(),
            }

            data.append(record)

        return pd.DataFrame(data)

    def create_multi_sheet_file(
        self, filename: str = "multi_sheets_sample.xlsx"
    ) -> str:
        """สร้างไฟล์ Excel หลาย sheets"""

        file_path = f"data/samples/{filename}"

        print(f"📊 สร้างไฟล์หลาย sheets: {filename}")

        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            # Sheet 1: Employees (500 rows)
            employees_df = self.generate_employee_data(500)
            employees_df.to_excel(writer, sheet_name="Employees", index=False)
            print(f"  ✅ Sheet 'Employees': {len(employees_df):,} แถว")

            # Sheet 2: Sales (2000 rows)
            sales_df = self.generate_sales_data(2000)
            sales_df.to_excel(writer, sheet_name="Sales", index=False)
            print(f"  ✅ Sheet 'Sales': {len(sales_df):,} แถว")

            # Sheet 3: Inventory (1000 rows)
            inventory_df = self.generate_inventory_data(1000)
            inventory_df.to_excel(writer, sheet_name="Inventory", index=False)
            print(f"  ✅ Sheet 'Inventory': {len(inventory_df):,} แถว")

            # Sheet 4: Financial (1500 rows)
            financial_df = self.generate_financial_data(1500)
            financial_df.to_excel(writer, sheet_name="Financial", index=False)
            print(f"  ✅ Sheet 'Financial': {len(financial_df):,} แถว")

            # Sheet 5: Summary (สรุปข้อมูล)
            summary_data = {
                "ReportMonth": [
                    "ม.ค.2024",
                    "ก.พ.2024",
                    "มี.ค.2024",
                    "เม.ย.2024",
                    "พ.ค.2024",
                    "มิ.ย.2024",
                ],
                "TotalSales": [random.randint(500000, 2000000) for _ in range(6)],
                "TotalExpenses": [random.randint(300000, 1000000) for _ in range(6)],
                "NetProfit": [random.randint(50000, 500000) for _ in range(6)],
                "EmployeeCount": [random.randint(50, 200) for _ in range(6)],
                "ProductsSold": [random.randint(100, 1000) for _ in range(6)],
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name="Summary", index=False)
            print(f"  ✅ Sheet 'Summary': {len(summary_df):,} แถว")

        return file_path

    def create_sample_files(self) -> dict:
        """สร้างไฟล์ตัวอย่างสำหรับ SSMS"""

        print("🚀 สร้างไฟล์ตัวอย่างสำหรับ SSMS...")

        files_created = {}

        # 1. Small test file (100 rows)
        print("\n📝 ไฟล์ทดสอบเล็ก (100 แถว)...")
        small_df = self.generate_employee_data(100)
        small_path = "data/samples/employees_small_100.xlsx"
        small_df.to_excel(small_path, index=False)
        files_created["small"] = small_path
        print(f"  ✅ {small_path}")

        # 2. Medium employee file (1000 rows)
        print("\n👥 ข้อมูลพนักงาน (1,000 แถว)...")
        employee_df = self.generate_employee_data(1000)
        employee_path = "data/samples/employees_medium_1k.xlsx"
        employee_df.to_excel(employee_path, index=False)
        files_created["employees"] = employee_path
        print(f"  ✅ {employee_path}")

        # 3. Sales data (5000 rows)
        print("\n💰 ข้อมูลยอดขาย (5,000 แถว)...")
        sales_df = self.generate_sales_data(5000)
        sales_path = "data/samples/sales_data_5k.xlsx"
        sales_df.to_excel(sales_path, index=False)
        files_created["sales"] = sales_path
        print(f"  ✅ {sales_path}")

        # 4. Large dataset (10000 rows)
        print("\n📈 ข้อมูลขนาดใหญ่ (10,000 แถว)...")
        large_df = self.generate_sales_data(10000)
        large_path = "data/samples/sales_large_10k.xlsx"
        large_df.to_excel(large_path, index=False)
        files_created["large"] = large_path
        print(f"  ✅ {large_path}")

        # 5. Inventory data
        print("\n📦 ข้อมูลสินค้าคงคลัง (2,000 แถว)...")
        inventory_df = self.generate_inventory_data(2000)
        inventory_path = "data/samples/inventory_data_2k.xlsx"
        inventory_df.to_excel(inventory_path, index=False)
        files_created["inventory"] = inventory_path
        print(f"  ✅ {inventory_path}")

        # 6. Financial data
        print("\n💸 ข้อมูลการเงิน (3,000 แถว)...")
        financial_df = self.generate_financial_data(3000)
        financial_path = "data/samples/financial_data_3k.xlsx"
        financial_df.to_excel(financial_path, index=False)
        files_created["financial"] = financial_path
        print(f"  ✅ {financial_path}")

        # 7. Multi-sheet file
        print("\n📋 ไฟล์หลาย sheets...")
        multi_path = self.create_multi_sheet_file("comprehensive_data.xlsx")
        files_created["multi_sheets"] = multi_path

        return files_created

    def create_performance_test_files(self) -> dict:
        """สร้างไฟล์สำหรับทดสอบประสิทธิภาพ"""

        print("⚡ สร้างไฟล์ทดสอบประสิทธิภาพ...")

        performance_files = {}

        sizes = [
            ("tiny", 50, "ทดสอบเชื่อมต่อ"),
            ("small", 500, "ทดสอบเล็ก"),
            ("medium", 5000, "ทดสอบกลาง"),
            ("large", 20000, "ทดสอบใหญ่"),
            ("xlarge", 50000, "ทดสอบใหญ่มาก"),
        ]

        for size_name, row_count, description in sizes:
            print(f"\n📊 {description} ({row_count:,} แถว)...")

            # สร้างข้อมูลแบบผสม (employees + sales)
            emp_rows = min(row_count // 10, 1000)  # 10% employees หรือ max 1000
            sales_rows = row_count - emp_rows

            # Employee data
            emp_df = self.generate_employee_data(emp_rows)
            emp_df["DataType"] = "Employee"

            # Sales data
            sales_df = self.generate_sales_data(sales_rows)
            # เลือกเฉพาะ columns ที่สำคัญ
            sales_subset = sales_df[
                [
                    "SaleID",
                    "SaleDate",
                    "CustomerName",
                    "ProductName",
                    "Quantity",
                    "UnitPrice",
                    "TotalAmount",
                    "Status",
                ]
            ].copy()
            sales_subset["DataType"] = "Sales"

            # รวมข้อมูล
            filename = f"performance_test_{size_name}_{row_count}.xlsx"
            filepath = f"data/samples/{filename}"

            with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
                emp_df.to_excel(writer, sheet_name="Employees", index=False)
                sales_subset.to_excel(writer, sheet_name="Sales", index=False)

            performance_files[size_name] = filepath
            file_size = Path(filepath).stat().st_size / 1024 / 1024
            print(f"  ✅ {filename} ({file_size:.1f} MB)")

        return performance_files


def main():
    """CLI สำหรับ sample generator"""

    generator = SSMSSampleGenerator()

    if len(sys.argv) < 2:
        print(
            """
🎯 SSMS Sample Data Generator

Commands:
  all                    - สร้างไฟล์ตัวอย่างทั้งหมด
  performance           - สร้างไฟล์ทดสอบประสิทธิภาพ
  employees [rows]      - สร้างข้อมูลพนักงาน
  sales [rows]          - สร้างข้อมูลยอดขาย
  inventory [rows]      - สร้างข้อมูลสินค้าคงคลัง
  financial [rows]      - สร้างข้อมูลการเงิน
  multi                 - สร้างไฟล์หลาย sheets
  test                  - สร้างไฟล์ทดสอบเล็ก (100 rows)

Examples:
  python sample_generator.py all
  python sample_generator.py employees 1000
  python sample_generator.py test
  python sample_generator.py performance
        """
        )
        sys.exit(1)

    command = sys.argv[1]
    rows = int(sys.argv[2]) if len(sys.argv) > 2 else None

    if command == "all":
        files = generator.create_sample_files()

        print("\n✅ ไฟล์ตัวอย่างที่สร้างแล้ว:")
        total_size = 0
        for name, path in files.items():
            file_size = Path(path).stat().st_size / 1024 / 1024
            total_size += file_size
            print(f"  • {name}: {Path(path).name} ({file_size:.1f}MB)")

        print(f"\n📊 รวมขนาดไฟล์: {total_size:.1f} MB")
        print(f"\n🚀 ทดสอบ:")
        print(f"  python test_connection.py")
        print(f"  python excel_to_ssms.py {files['small']} test_employees")

    elif command == "performance":
        files = generator.create_performance_test_files()

        print("\n✅ ไฟล์ทดสอบประสิทธิภาพ:")
        for size, path in files.items():
            file_size = Path(path).stat().st_size / 1024 / 1024
            print(f"  • {size}: {Path(path).name} ({file_size:.1f}MB)")

        print(f"\n⚡ ทดสอบประสิทธิภาพ:")
        print(f"  python excel_to_ssms.py {files['small']} perf_test_small")
        print(f"  python excel_to_ssms.py {files['large']} perf_test_large")

    elif command == "employees":
        rows = rows or 1000
        df = generator.generate_employee_data(rows)
        path = f"data/samples/employees_{rows}.xlsx"
        df.to_excel(path, index=False)
        file_size = Path(path).stat().st_size / 1024 / 1024
        print(f"✅ สร้างแล้ว: {path} ({file_size:.1f}MB)")

    elif command == "sales":
        rows = rows or 5000
        df = generator.generate_sales_data(rows)
        path = f"data/samples/sales_{rows}.xlsx"
        df.to_excel(path, index=False)
        file_size = Path(path).stat().st_size / 1024 / 1024
        print(f"✅ สร้างแล้ว: {path} ({file_size:.1f}MB)")

    elif command == "inventory":
        rows = rows or 2000
        df = generator.generate_inventory_data(rows)
        path = f"data/samples/inventory_{rows}.xlsx"
        df.to_excel(path, index=False)
        file_size = Path(path).stat().st_size / 1024 / 1024
        print(f"✅ สร้างแล้ว: {path} ({file_size:.1f}MB)")

    elif command == "financial":
        rows = rows or 3000
        df = generator.generate_financial_data(rows)
        path = f"data/samples/financial_{rows}.xlsx"
        df.to_excel(path, index=False)
        file_size = Path(path).stat().st_size / 1024 / 1024
        print(f"✅ สร้างแล้ว: {path} ({file_size:.1f}MB)")

    elif command == "multi":
        path = generator.create_multi_sheet_file()
        file_size = Path(path).stat().st_size / 1024 / 1024
        print(f"✅ ไฟล์หลาย sheets: {path} ({file_size:.1f}MB)")

    elif command == "test":
        df = generator.generate_employee_data(100)
        path = "data/samples/test_100.xlsx"
        df.to_excel(path, index=False)
        print(f"✅ ไฟล์ทดสอบ: {path}")
        print(f"🚀 ทดสอบ: python excel_to_ssms.py {path} test_table")

    else:
        print(f"❌ Unknown command: {command}")


if __name__ == "__main__":
    main()
