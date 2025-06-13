#!/usr/bin/env python3
"""
Enhanced Sample Data Generator for Excel to SSMS Testing
สร้างข้อมูลตัวอย่างสำหรับทดสอบระบบ import
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from pathlib import Path
import sys
import argparse
from typing import Dict, List, Any, Optional


class EnhancedSampleGenerator:
    """Enhanced sample data generator with realistic Thai business data"""

    def __init__(self):
        self.setup_directories()
        self.setup_thai_data()

    def setup_directories(self):
        """Create necessary directories"""
        directories = ["data", "data/samples", "data/test", "data/performance"]
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)

    def setup_thai_data(self):
        """Setup Thai business data for realistic samples"""

        # Thai names
        self.thai_first_names = [
            "สมชาย",
            "สมหญิง",
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
            "นายพร",
            "นางสาวลักษณ์",
            "ธีระชัย",
            "มานิต",
            "สุขสันต์",
            "เกียรติคุณ",
            "บุญเลิศ",
            "วิไลลักษณ์",
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
            "บุญมี",
            "เทพสุดา",
            "พรประสิทธิ์",
            "สุขเกษม",
            "ปิยะวิเศษ",
            "แสงอุทัย",
        ]

        # Companies
        self.companies = [
            "บริษัท เทคโนโลยี สมัยใหม่ จำกัด",
            "บริษัท การค้าระหว่างประเทศ จำกัด",
            "ห้างหุ้นส่วน สมบูรณ์ เทรดดิ้ง",
            "บจก. นวัตกรรม ดิจิทัล",
            "สหกรณ์ เกษตรกรไทย",
            "มหาวิทยาลัย เทคโนโลยี แห่งชาติ",
            "บริษัท ผลิตภัณฑ์ อุตสาหกรรม จำกัด",
            "บริษัท บริการ ธุรกิจ จำกัด",
        ]

        # Products
        self.products = [
            "คอมพิวเตอร์ โน้ตบุ๊ค",
            "โทรศัพท์ สมาร์ทโฟน",
            "เครื่องพิมพ์ เลเซอร์",
            "จอภาพ LED 4K",
            "คีย์บอร์ด เมคานิคัล",
            "เมาส์ ไร้สาย",
            "ซอฟต์แวร์ บัญชี",
            "ระบบ รักษาความปลอดภัย",
            "กล้อง IP",
            "เซิร์ฟเวอร์ แร็ค",
            "อุปกรณ์ เครือข่าย",
            "UPS ไฟสำรอง",
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
            "ฝ่ายคุณภาพ",
            "ฝ่ายจัดซื้อ",
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
            "นครปฐม",
            "สมุทรปราการ",
            "ปทุมธานี",
            "นนทบุรี",
            "สมุทรสาคร",
        ]

    def generate_employees_data(self, rows: int = 1000) -> pd.DataFrame:
        """Generate realistic employee data"""

        data = []

        for i in range(rows):
            # Generate hire date (within last 5 years)
            hire_date = datetime.now() - timedelta(days=random.randint(30, 1825))

            # Position hierarchy with realistic salaries
            positions = {
                "พนักงาน": (25000, 45000, 0.6),
                "หัวหน้าทีม": (45000, 70000, 0.25),
                "ผู้จัดการ": (70000, 120000, 0.12),
                "ผู้อำนวยการ": (120000, 200000, 0.03),
            }

            # Weighted position selection
            position_choices = list(positions.keys())
            position_weights = [positions[p][2] for p in position_choices]
            position = np.random.choice(position_choices, p=position_weights)

            salary_range = positions[position]
            salary = random.randint(salary_range[0], salary_range[1])

            # Calculate bonus and performance based on position
            base_bonus = {"พนักงาน": 5, "หัวหน้าทีม": 10, "ผู้จัดการ": 15, "ผู้อำนวยการ": 20}
            bonus_percent = base_bonus[position] + random.randint(-2, 5)

            performance_score = (
                random.uniform(2.5, 5.0)
                if position in ["ผู้จัดการ", "ผู้อำนวยการ"]
                else random.uniform(1.5, 4.5)
            )

            record = {
                "employee_id": f"EMP{i+1:05d}",
                "first_name": random.choice(self.thai_first_names),
                "last_name": random.choice(self.thai_last_names),
                "email": f"employee{i+1:05d}@company.co.th",
                "department": random.choice(self.departments),
                "position": position,
                "salary": salary,
                "hire_date": hire_date,
                "is_active": random.choice([True, True, True, False]),  # 75% active
                "age": random.randint(22, 60),
                "gender": random.choice(["ชาย", "หญิง"]),
                "province": random.choice(self.provinces),
                "phone": f"0{random.randint(800000000, 999999999)}",
                "bonus_percentage": max(0, bonus_percent),
                "performance_score": round(performance_score, 2),
                "years_of_service": (datetime.now() - hire_date).days // 365,
                "last_updated": datetime.now(),
            }

            # Add full name
            record["full_name"] = f"{record['first_name']} {record['last_name']}"

            data.append(record)

        return pd.DataFrame(data)

    def generate_sales_data(self, rows: int = 5000) -> pd.DataFrame:
        """Generate realistic sales transaction data"""

        data = []
        start_date = datetime.now() - timedelta(days=365)

        for i in range(rows):
            sale_date = start_date + timedelta(days=random.randint(0, 365))

            # Product selection with realistic pricing
            product = random.choice(self.products)

            # Realistic quantity based on product type
            if "คอมพิวเตอร์" in product or "เซิร์ฟเวอร์" in product:
                quantity = random.randint(1, 5)
                unit_price = random.randint(20000, 80000)
            elif "โทรศัพท์" in product:
                quantity = random.randint(1, 10)
                unit_price = random.randint(8000, 40000)
            elif "ซอฟต์แวร์" in product:
                quantity = random.randint(1, 50)
                unit_price = random.randint(2000, 15000)
            else:
                quantity = random.randint(1, 20)
                unit_price = random.randint(1000, 25000)

            # Calculate totals
            subtotal = quantity * unit_price

            # Realistic discount based on amount
            if subtotal > 100000:
                discount_percent = random.choice([10, 15, 20])
            elif subtotal > 50000:
                discount_percent = random.choice([5, 10])
            else:
                discount_percent = random.choice([0, 0, 0, 5])  # Mostly no discount

            discount_amount = subtotal * (discount_percent / 100)
            tax_amount = (subtotal - discount_amount) * 0.07  # VAT 7%
            total_amount = subtotal - discount_amount + tax_amount

            # Customer info
            customer_name = f"{random.choice(self.thai_first_names)} {random.choice(self.thai_last_names)}"

            record = {
                "sale_id": f"SAL{sale_date.year}{i+1:06d}",
                "sale_date": sale_date,
                "customer_name": customer_name,
                "company_name": random.choice(self.companies),
                "product_name": product,
                "product_category": self._get_product_category(product),
                "quantity": quantity,
                "unit_price": unit_price,
                "subtotal": subtotal,
                "discount_percent": discount_percent,
                "discount_amount": discount_amount,
                "tax_amount": round(tax_amount, 2),
                "total_amount": round(total_amount, 2),
                "province": random.choice(self.provinces),
                "sales_channel": random.choice(
                    ["Online", "หน้าร้าน", "โทรศัพท์", "ตัวแทนขาย"]
                ),
                "status": random.choice(["ขายแล้ว", "รอการชำระ", "ยกเลิก", "ส่งมอบแล้ว"]),
                "salesperson_id": f"EMP{random.randint(1, 100):05d}",
                "notes": random.choice(
                    ["", "ลูกค้า VIP", "ส่วนลด พิเศษ", "ซื้อครบตามเป้า", ""]
                ),
                "created_date": datetime.now(),
                "quarter": f"Q{((sale_date.month - 1) // 3) + 1}/{sale_date.year}",
            }

            data.append(record)

        return pd.DataFrame(data)

    def _get_product_category(self, product_name: str) -> str:
        """Categorize products"""
        if any(word in product_name for word in ["คอมพิวเตอร์", "โน้ตบุ๊ค", "เซิร์ฟเวอร์"]):
            return "คอมพิวเตอร์"
        elif any(word in product_name for word in ["โทรศัพท์", "สมาร์ทโฟน"]):
            return "โทรศัพท์"
        elif any(
            word in product_name for word in ["เครื่องพิมพ์", "คีย์บอร์ด", "เมาส์", "จอภาพ"]
        ):
            return "อุปกรณ์"
        elif "ซอฟต์แวร์" in product_name:
            return "ซอฟต์แวร์"
        elif any(word in product_name for word in ["ระบบ", "กล้อง", "UPS"]):
            return "ระบบรักษาความปลอดภัย"
        else:
            return "อื่นๆ"

    def generate_inventory_data(self, rows: int = 2000) -> pd.DataFrame:
        """Generate inventory management data"""

        data = []

        for i in range(rows):
            product = random.choice(self.products)

            # Realistic cost and selling prices
            if "คอมพิวเตอร์" in product or "เซิร์ฟเวอร์" in product:
                cost_price = random.randint(15000, 60000)
                markup = random.uniform(1.15, 1.35)  # 15-35% markup
            elif "โทรศัพท์" in product:
                cost_price = random.randint(6000, 30000)
                markup = random.uniform(1.20, 1.40)  # 20-40% markup
            elif "ซอฟต์แวร์" in product:
                cost_price = random.randint(1500, 12000)
                markup = random.uniform(1.50, 2.50)  # 50-150% markup
            else:
                cost_price = random.randint(800, 20000)
                markup = random.uniform(1.25, 1.80)  # 25-80% markup

            selling_price = cost_price * markup

            # Stock levels based on product type
            if "ซอฟต์แวร์" in product:
                current_stock = random.randint(50, 500)  # Digital products
                min_stock = 10
                max_stock = 1000
            else:
                current_stock = random.randint(0, 200)
                min_stock = random.randint(5, 20)
                max_stock = random.randint(100, 500)

            record = {
                "product_id": f"PRD{i+1:06d}",
                "product_name": f"{product} รุ่น {random.choice(['A', 'B', 'C', 'Pro', 'Max', 'Plus', '2024'])}",
                "product_category": self._get_product_category(product),
                "supplier": random.choice(self.companies),
                "current_stock": current_stock,
                "minimum_stock": min_stock,
                "maximum_stock": max_stock,
                "cost_price": cost_price,
                "selling_price": round(selling_price, 2),
                "profit_margin": round(
                    ((selling_price - cost_price) / cost_price) * 100, 2
                ),
                "warehouse": random.choice(
                    ["คลัง A", "คลัง B", "คลัง C", "คลังหลัก", "คลังสำรอง"]
                ),
                "location": f"แถว {random.randint(1, 25)}-{random.randint(1, 15)}",
                "unit": random.choice(["ชิ้น", "กล่อง", "แพ็ค", "โหล", "ตัว", "ลิขสิทธิ์"]),
                "last_updated": datetime.now() - timedelta(days=random.randint(0, 30)),
                "status": self._get_stock_status(current_stock, min_stock),
                "is_active": random.choice([True, True, True, False]),  # 75% active
                "created_date": datetime.now()
                - timedelta(days=random.randint(30, 730)),
                "reorder_point": min_stock + random.randint(5, 15),
            }

            data.append(record)

        return pd.DataFrame(data)

    def _get_stock_status(self, current: int, minimum: int) -> str:
        """Determine stock status"""
        if current == 0:
            return "หมด"
        elif current <= minimum:
            return "ใกล้หมด"
        elif current <= minimum * 2:
            return "ต่ำ"
        else:
            return "พร้อมขาย"

    def generate_financial_data(self, rows: int = 3000) -> pd.DataFrame:
        """Generate financial transaction data"""

        data = []
        start_date = datetime.now() - timedelta(days=365)

        # Transaction types with realistic amounts
        transaction_types = [
            ("รายรับ", "ขายสินค้า", 5000, 500000, 0.4),
            ("รายรับ", "ดอกเบียรับ", 500, 10000, 0.05),
            ("รายรับ", "รายได้อื่น", 1000, 50000, 0.05),
            ("รายจ่าย", "ค่าเช่า", -30000, -100000, 0.08),
            ("รายจ่าย", "เงินเดือน", -500000, -2000000, 0.15),
            ("รายจ่าย", "ค่าไฟฟ้า", -8000, -30000, 0.05),
            ("รายจ่าย", "ค่าการตลาด", -10000, -200000, 0.08),
            ("รายจ่าย", "วัตถุดิบ", -50000, -800000, 0.1),
            ("รายจ่าย", "ค่าขนส่ง", -5000, -50000, 0.04),
        ]

        for i in range(rows):
            # Weighted selection of transaction type
            choices = [t[:4] for t in transaction_types]
            weights = [t[4] for t in transaction_types]
            selected = np.random.choice(len(choices), p=weights)

            trans_type, category, min_amount, max_amount = choices[selected]
            amount = random.randint(min_amount, max_amount)

            trans_date = start_date + timedelta(days=random.randint(0, 365))

            record = {
                "transaction_id": f"TXN{trans_date.year}{i+1:06d}",
                "transaction_date": trans_date,
                "transaction_type": trans_type,
                "category": category,
                "amount": amount,
                "description": f"{category} - {random.choice(['ปกติ', 'พิเศษ', 'เร่งด่วน', 'รายเดือน', 'รายไตรมาส'])}",
                "payee_receiver": random.choice(self.companies + self.thai_first_names),
                "account_name": random.choice(
                    [
                        "เงินสด",
                        "ธนาคาร กสิกรไทย",
                        "ธนาคาร กรุงเทพ",
                        "ธนาคาร ไทยพาณิชย์",
                        "บัตรเครดิต",
                        "เงินฝากประจำ",
                    ]
                ),
                "reference_number": f"REF{random.randint(100000, 999999)}",
                "approved_by": f"{random.choice(self.thai_first_names)} {random.choice(self.thai_last_names)}",
                "status": random.choice(["อนุมัติแล้ว", "รอการอนุมัติ", "ยกเลิก", "ชำระแล้ว"]),
                "tax_amount": abs(amount) * 0.07 if amount > 0 else 0,
                "notes": random.choice(
                    [
                        "",
                        "เงินทอน",
                        "ภาษี 7%",
                        "หัก ณ ที่จ่าย 3%",
                        "ค่าธรรมเนียม",
                        "ชำระล่วงหน้า",
                        "ผ่อนชำระ",
                    ]
                ),
                "created_date": datetime.now(),
                "month_year": trans_date.strftime("%m/%Y"),
                "quarter": f"Q{((trans_date.month - 1) // 3) + 1}/{trans_date.year}",
            }

            data.append(record)

        return pd.DataFrame(data)

    def create_test_files(self) -> Dict[str, str]:
        """Create various test files for different scenarios"""

        print("🚀 Creating Test Files...")
        files_created = {}

        # 1. Small test file (100 rows)
        print("  📝 Creating small test file (100 rows)...")
        small_df = self.generate_employees_data(100)
        small_path = "data/test/employees_test_100.xlsx"
        small_df.to_excel(small_path, index=False)
        files_created["small_test"] = small_path

        # 2. Medium employee file (1000 rows)
        print("  👥 Creating employee data (1,000 rows)...")
        employee_df = self.generate_employees_data(1000)
        employee_path = "data/samples/employees_1k.xlsx"
        employee_df.to_excel(employee_path, index=False)
        files_created["employees"] = employee_path

        # 3. Sales data (5000 rows)
        print("  💰 Creating sales data (5,000 rows)...")
        sales_df = self.generate_sales_data(5000)
        sales_path = "data/samples/sales_5k.xlsx"
        sales_df.to_excel(sales_path, index=False)
        files_created["sales"] = sales_path

        # 4. Inventory data (2000 rows)
        print("  📦 Creating inventory data (2,000 rows)...")
        inventory_df = self.generate_inventory_data(2000)
        inventory_path = "data/samples/inventory_2k.xlsx"
        inventory_df.to_excel(inventory_path, index=False)
        files_created["inventory"] = inventory_path

        # 5. Financial data (3000 rows)
        print("  💸 Creating financial data (3,000 rows)...")
        financial_df = self.generate_financial_data(3000)
        financial_path = "data/samples/financial_3k.xlsx"
        financial_df.to_excel(financial_path, index=False)
        files_created["financial"] = financial_path

        return files_created

    def create_performance_test_files(self) -> Dict[str, str]:
        """Create files for performance testing"""

        print("⚡ Creating Performance Test Files...")
        perf_files = {}

        sizes = [
            ("tiny", 50, "ทดสอบเชื่อมต่อ"),
            ("small", 500, "ทดสอบเล็ก"),
            ("medium", 5000, "ทดสอบกลาง"),
            ("large", 20000, "ทดสอบใหญ่"),
            ("xlarge", 50000, "ทดสอบใหญ่มาก"),
        ]

        for size_name, row_count, description in sizes:
            print(f"  📊 {description} ({row_count:,} rows)...")

            # Create mixed data (sales transactions)
            df = self.generate_sales_data(row_count)

            filename = f"performance_{size_name}_{row_count}.xlsx"
            filepath = f"data/performance/{filename}"
            df.to_excel(filepath, index=False)

            file_size = Path(filepath).stat().st_size / 1024 / 1024
            print(f"    ✅ {filename} ({file_size:.1f} MB)")

            perf_files[size_name] = filepath

        return perf_files

    def create_multi_sheet_file(self, filename: str = "comprehensive_data.xlsx") -> str:
        """Create Excel file with multiple sheets"""

        print(f"📋 Creating multi-sheet file: {filename}")
        filepath = f"data/samples/{filename}"

        with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
            # Sheet 1: Employees
            emp_df = self.generate_employees_data(500)
            emp_df.to_excel(writer, sheet_name="Employees", index=False)
            print(f"  ✅ Sheet 'Employees': {len(emp_df):,} rows")

            # Sheet 2: Sales
            sales_df = self.generate_sales_data(2000)
            sales_df.to_excel(writer, sheet_name="Sales", index=False)
            print(f"  ✅ Sheet 'Sales': {len(sales_df):,} rows")

            # Sheet 3: Inventory
            inv_df = self.generate_inventory_data(1000)
            inv_df.to_excel(writer, sheet_name="Inventory", index=False)
            print(f"  ✅ Sheet 'Inventory': {len(inv_df):,} rows")

            # Sheet 4: Financial
            fin_df = self.generate_financial_data(1500)
            fin_df.to_excel(writer, sheet_name="Financial", index=False)
            print(f"  ✅ Sheet 'Financial': {len(fin_df):,} rows")

            # Sheet 5: Summary
            summary_data = {
                "metric": [
                    "Total Employees",
                    "Total Sales",
                    "Total Products",
                    "Total Transactions",
                ],
                "count": [len(emp_df), len(sales_df), len(inv_df), len(fin_df)],
                "last_updated": [datetime.now()] * 4,
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name="Summary", index=False)
            print(f"  ✅ Sheet 'Summary': {len(summary_df):,} rows")

        return filepath

    def show_file_summary(self, files: Dict[str, str]):
        """Show summary of created files"""

        print(f"\n✅ Files Created Successfully!")
        print("=" * 50)

        total_size = 0
        for name, filepath in files.items():
            if Path(filepath).exists():
                file_size = Path(filepath).stat().st_size / 1024 / 1024
                total_size += file_size
                print(f"  • {name}: {Path(filepath).name} ({file_size:.1f} MB)")

        print(f"\n📊 Total size: {total_size:.1f} MB")
        print(f"📁 Files location: data/ directory")

    def create_quick_test_script(self):
        """Create a quick test script"""

        test_script = '''#!/usr/bin/env python3
"""
Quick Test Script - Test Excel to SSMS with sample data
"""

import subprocess
import sys
from pathlib import Path

def run_test():
    print("🧪 Running Excel to SSMS Quick Test")
    print("=" * 40)
    
    # Check if test file exists
    test_file = "data/test/employees_test_100.xlsx"
    if not Path(test_file).exists():
        print(f"❌ Test file not found: {test_file}")
        print("💡 Run: python sample_data_generator.py test")
        return False
    
    # Run connection diagnostic first
    print("1. Testing SQL Server connection...")
    try:
        result = subprocess.run([sys.executable, "connection_tester.py"], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            print("⚠️ Connection test failed, but continuing...")
    except:
        print("⚠️ Could not run connection test")
    
    # Run Excel import test
    print("\\n2. Testing Excel import...")
    try:
        cmd = [sys.executable, "excel_to_ssms_fixed.py", test_file, "test_employees"]
        result = subprocess.run(cmd, timeout=120)
        
        if result.returncode == 0:
            print("\\n✅ Test completed successfully!")
            print("💡 Check SQL Server Management Studio:")
            print("   Database: excel_to_db")
            print("   Table: test_employees")
            return True
        else:
            print("\\n❌ Test failed")
            return False
            
    except subprocess.TimeoutExpired:
        print("\\n⏰ Test timed out")
        return False
    except Exception as e:
        print(f"\\n❌ Test error: {e}")
        return False

if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
'''

        with open("quick_test.py", "w", encoding="utf-8") as f:
            f.write(test_script)

        print("  ✅ Created: quick_test.py")


def main():
    """Main function with command line interface"""

    parser = argparse.ArgumentParser(
        description="Enhanced Sample Data Generator for Excel to SSMS"
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="help",
        choices=[
            "test",
            "all",
            "performance",
            "employees",
            "sales",
            "inventory",
            "financial",
            "multi",
            "help",
        ],
        help="Command to execute",
    )
    parser.add_argument("--rows", type=int, help="Number of rows to generate")
    parser.add_argument("--output", type=str, help="Output file path")

    args = parser.parse_args()

    generator = EnhancedSampleGenerator()

    if args.command == "help" or len(sys.argv) == 1:
        print(
            """
🎯 Enhanced Sample Data Generator for Excel to SSMS

Commands:
  test                 - Create test files (recommended first step)
  all                  - Create all sample files
  performance          - Create performance test files
  employees [--rows N] - Create employee data
  sales [--rows N]     - Create sales data
  inventory [--rows N] - Create inventory data
  financial [--rows N] - Create financial data
  multi                - Create multi-sheet Excel file

Examples:
  python sample_data_generator.py test
  python sample_data_generator.py all
  python sample_data_generator.py employees --rows 2000
  python sample_data_generator.py performance
        """
        )
        return

    if args.command == "test":
        print("🧪 Creating Test Files...")

        # Create small test file
        test_df = generator.generate_employees_data(100)
        test_path = "data/test/employees_test_100.xlsx"
        test_df.to_excel(test_path, index=False)

        # Create quick test script
        generator.create_quick_test_script()

        print(f"✅ Test files created:")
        print(f"  • {test_path}")
        print(f"  • quick_test.py")
        print(f"\n🚀 Next steps:")
        print(f"  1. python connection_tester.py")
        print(f"  2. python quick_test.py")

    elif args.command == "all":
        files = generator.create_test_files()
        multi_file = generator.create_multi_sheet_file()
        files["multi_sheet"] = multi_file
        generator.show_file_summary(files)

        print(f"\n🚀 Usage Examples:")
        print(f"  python excel_to_ssms_fixed.py {files['small_test']} test_table")
        print(f"  python excel_to_ssms_fixed.py {files['employees']} employees")
        print(f"  python excel_to_ssms_fixed.py {files['sales']} sales_data")

    elif args.command == "performance":
        perf_files = generator.create_performance_test_files()
        generator.show_file_summary(perf_files)

        print(f"\n⚡ Performance Testing:")
        print(f"  python excel_to_ssms_fixed.py {perf_files['small']} perf_small")
        print(f"  python excel_to_ssms_fixed.py {perf_files['large']} perf_large")

    elif args.command in ["employees", "sales", "inventory", "financial"]:
        rows = (
            args.rows
            or {"employees": 1000, "sales": 5000, "inventory": 2000, "financial": 3000}[
                args.command
            ]
        )

        if args.command == "employees":
            df = generator.generate_employees_data(rows)
        elif args.command == "sales":
            df = generator.generate_sales_data(rows)
        elif args.command == "inventory":
            df = generator.generate_inventory_data(rows)
        elif args.command == "financial":
            df = generator.generate_financial_data(rows)

        output_path = args.output or f"data/samples/{args.command}_{rows}.xlsx"
        df.to_excel(output_path, index=False)

        file_size = Path(output_path).stat().st_size / 1024 / 1024
        print(f"✅ Created: {output_path} ({file_size:.1f} MB, {len(df):,} rows)")

    elif args.command == "multi":
        multi_file = generator.create_multi_sheet_file()
        file_size = Path(multi_file).stat().st_size / 1024 / 1024
        print(f"✅ Created: {multi_file} ({file_size:.1f} MB)")


if __name__ == "__main__":
    main()
