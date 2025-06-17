"""
core/mock_data_generator.py
FIXED: Production-Ready Mock Data Generator
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
import math


class MockDataGenerator:
    """FIXED: High-Performance Mock Data Generator with Real Data Patterns"""

    def __init__(self):
        # Real Thai automotive industry data
        self.thai_names = {
            "first": [
                "สมชาย",
                "วิชาย",
                "ประยุทธ",
                "ธนาคาร",
                "อรรถพล",
                "กิตติ",
                "ปิยะ",
                "เศรษฐา",
                "ธีระ",
                "นิรันดร์",
                "สมหญิง",
                "วิชุดา",
                "ประภา",
                "ธนากร",
                "อรรถศิษฎ์",
                "กิตติยา",
                "ปิยวดี",
                "เศรษฐี",
                "ธีรนุช",
                "นิรมล",
                "สมศักดิ์",
                "วิรัช",
                "ปรีชา",
                "สุรชัย",
                "มานะ",
                "ชาญณรงค์",
                "สมพงษ์",
                "ธนพล",
                "อนุชา",
                "จักรพันธ์",
            ],
            "last": [
                "ใจดี",
                "รักดี",
                "สุขใส",
                "มั่นคง",
                "เจริญ",
                "พัฒนา",
                "สว่าง",
                "สุข",
                "ดีใจ",
                "มีสุข",
                "เก่งดี",
                "ฉลาด",
                "อุดม",
                "สมบูรณ์",
                "เฉลิม",
                "วิจิตร",
                "สุรชัย",
                "สมบัติ",
                "ชาญวิทย์",
                "เฉลิมชัย",
                "กิจเจริญ",
                "วงศ์ใหญ่",
                "ศรีสุข",
                "มณีรัตน์",
                "ทองดี",
                "รุ่งเรือง",
                "เจริญสุข",
                "สมใจ",
                "บุญมา",
                "ศิริ",
            ],
        }

        self.english_names = {
            "first": [
                "John",
                "Michael",
                "David",
                "Robert",
                "William",
                "James",
                "Christopher",
                "Daniel",
                "Matthew",
                "Anthony",
                "Jane",
                "Sarah",
                "Lisa",
                "Jennifer",
                "Jessica",
                "Amanda",
                "Stephanie",
                "Nicole",
                "Ashley",
                "Elizabeth",
                "Mark",
                "Steven",
                "Andrew",
                "Kevin",
                "Brian",
                "George",
                "Edward",
                "Ronald",
                "Timothy",
                "Jason",
            ],
            "last": [
                "Smith",
                "Johnson",
                "Williams",
                "Brown",
                "Jones",
                "Garcia",
                "Miller",
                "Davis",
                "Rodriguez",
                "Martinez",
                "Hernandez",
                "Lopez",
                "Gonzalez",
                "Wilson",
                "Anderson",
                "Thomas",
                "Taylor",
                "Moore",
                "Jackson",
                "Martin",
                "Lee",
                "Perez",
                "Thompson",
                "White",
                "Harris",
                "Sanchez",
                "Clark",
                "Ramirez",
                "Lewis",
                "Robinson",
            ],
        }

        # DENSO-specific departments and roles
        self.departments = {
            "Manufacturing": {
                "positions": [
                    "Production Manager",
                    "Line Supervisor",
                    "Quality Inspector",
                    "Operator",
                    "Maintenance Technician",
                ],
                "salary_range": (28000, 85000),
                "multiplier": 1.0,
            },
            "Engineering": {
                "positions": [
                    "Chief Engineer",
                    "Senior Engineer",
                    "Design Engineer",
                    "Test Engineer",
                    "Junior Engineer",
                ],
                "salary_range": (45000, 120000),
                "multiplier": 1.15,
            },
            "Quality Assurance": {
                "positions": [
                    "QA Director",
                    "QA Manager",
                    "QA Engineer",
                    "QC Inspector",
                    "Quality Analyst",
                ],
                "salary_range": (35000, 95000),
                "multiplier": 1.05,
            },
            "Research & Development": {
                "positions": [
                    "R&D Director",
                    "Research Scientist",
                    "Product Developer",
                    "Innovation Manager",
                ],
                "salary_range": (60000, 150000),
                "multiplier": 1.25,
            },
            "Sales & Marketing": {
                "positions": [
                    "Sales Director",
                    "Regional Manager",
                    "Account Manager",
                    "Sales Representative",
                    "Marketing Specialist",
                ],
                "salary_range": (35000, 110000),
                "multiplier": 1.1,
            },
            "Supply Chain": {
                "positions": [
                    "SCM Director",
                    "Logistics Manager",
                    "Procurement Specialist",
                    "Warehouse Supervisor",
                ],
                "salary_range": (40000, 100000),
                "multiplier": 1.0,
            },
            "Information Technology": {
                "positions": [
                    "IT Director",
                    "System Administrator",
                    "Software Developer",
                    "Network Engineer",
                    "Help Desk",
                ],
                "salary_range": (38000, 115000),
                "multiplier": 1.2,
            },
            "Human Resources": {
                "positions": [
                    "HR Director",
                    "HR Manager",
                    "HR Specialist",
                    "Recruiter",
                    "Training Coordinator",
                ],
                "salary_range": (35000, 90000),
                "multiplier": 1.0,
            },
        }

        # Real automotive parts for DENSO
        self.automotive_products = [
            {
                "name": "Engine Control Unit (ECU)",
                "category": "Electronics",
                "price_range": (15000, 45000),
            },
            {
                "name": "Fuel Injector",
                "category": "Engine Parts",
                "price_range": (2500, 8500),
            },
            {
                "name": "Oxygen Sensor",
                "category": "Sensors",
                "price_range": (1800, 5500),
            },
            {
                "name": "Alternator",
                "category": "Electrical",
                "price_range": (8500, 25000),
            },
            {
                "name": "Starter Motor",
                "category": "Electrical",
                "price_range": (6500, 18000),
            },
            {
                "name": "Air Flow Sensor",
                "category": "Sensors",
                "price_range": (3200, 9500),
            },
            {
                "name": "Radiator",
                "category": "Cooling System",
                "price_range": (4500, 15000),
            },
            {
                "name": "Brake Pad Set",
                "category": "Brake System",
                "price_range": (1200, 4500),
            },
            {"name": "Spark Plug", "category": "Ignition", "price_range": (150, 850)},
            {
                "name": "Timing Belt",
                "category": "Engine Parts",
                "price_range": (800, 2800),
            },
            {
                "name": "Water Pump",
                "category": "Cooling System",
                "price_range": (2800, 8500),
            },
            {
                "name": "Throttle Body",
                "category": "Engine Parts",
                "price_range": (5500, 16500),
            },
            {
                "name": "ABS Module",
                "category": "Electronics",
                "price_range": (12000, 35000),
            },
            {
                "name": "Climate Control Unit",
                "category": "HVAC",
                "price_range": (8500, 28000),
            },
            {
                "name": "Power Window Motor",
                "category": "Electrical",
                "price_range": (1800, 6500),
            },
        ]

        # Real customer companies
        self.customers = [
            {"name": "Toyota Motor Thailand", "type": "OEM", "size": "Large"},
            {"name": "Honda Automobile Thailand", "type": "OEM", "size": "Large"},
            {"name": "Nissan Motor Thailand", "type": "OEM", "size": "Large"},
            {"name": "Isuzu Motors Thailand", "type": "OEM", "size": "Medium"},
            {"name": "Mitsubishi Motors Thailand", "type": "OEM", "size": "Medium"},
            {"name": "AutoParts Central", "type": "Distributor", "size": "Medium"},
            {"name": "Thai Auto Components", "type": "Distributor", "size": "Small"},
            {"name": "Bangkok Auto Parts", "type": "Retailer", "size": "Small"},
            {"name": "Siam Auto Supply", "type": "Distributor", "size": "Medium"},
            {"name": "Eastern Auto Parts", "type": "Retailer", "size": "Small"},
        ]

        # Thai locations (DENSO facilities)
        self.locations = [
            "Bangkok Head Office",
            "Chonburi Manufacturing Plant",
            "Rayong Production Facility",
            "Ayutthaya Technical Center",
            "Pathum Thani Warehouse",
            "Laem Chabang Distribution Center",
        ]

        # Generation tracking
        self.generation_stats = {
            "total_generated": 0,
            "generation_time": 0,
            "templates_used": set(),
        }

    def generate_employees(self, count: int = 1000) -> List[Dict[str, Any]]:
        """Generate realistic employee data with proper distribution"""
        start_time = datetime.now()
        employees = []

        # Calculate realistic department distribution
        dept_distribution = self._calculate_department_distribution(count)

        employee_id = 1
        for dept, dept_count in dept_distribution.items():
            dept_info = self.departments[dept]

            for i in range(dept_count):
                # Mixed Thai/English names (70% Thai, 30% English)
                is_thai = random.random() < 0.7

                if is_thai:
                    first_name = random.choice(self.thai_names["first"])
                    last_name = random.choice(self.thai_names["last"])
                    email_prefix = self._romanize_name(first_name, last_name)
                else:
                    first_name = random.choice(self.english_names["first"])
                    last_name = random.choice(self.english_names["last"])
                    email_prefix = f"{first_name.lower()}.{last_name.lower()}"

                # Realistic position and salary
                position = random.choice(dept_info["positions"])
                base_salary = random.randint(*dept_info["salary_range"])

                # Position-based salary adjustment
                if "Director" in position or "Chief" in position:
                    salary = int(base_salary * random.uniform(1.3, 1.8))
                elif "Manager" in position:
                    salary = int(base_salary * random.uniform(1.1, 1.4))
                elif "Senior" in position:
                    salary = int(base_salary * random.uniform(1.0, 1.2))
                else:
                    salary = int(base_salary * random.uniform(0.8, 1.1))

                # Realistic hire date with proper distribution
                hire_date = self._generate_realistic_hire_date()
                years_service = (datetime.now() - hire_date).days / 365.25

                employee = {
                    "employee_id": f"EMP{employee_id:06d}",
                    "first_name": first_name,
                    "last_name": last_name,
                    "full_name": f"{first_name} {last_name}",
                    "email": f"{email_prefix}@denso.com",
                    "department": dept,
                    "position": position,
                    "salary": salary,
                    "hire_date": hire_date.strftime("%Y-%m-%d"),
                    "employment_status": self._generate_employment_status(
                        years_service
                    ),
                    "phone": self._generate_thai_phone(),
                    "age": random.randint(22, 65),
                    "gender": random.choice(["Male", "Female"]),
                    "location": random.choice(self.locations),
                    "performance_rating": round(random.uniform(2.5, 5.0), 1),
                    "years_experience": max(
                        1, int(years_service) + random.randint(-2, 5)
                    ),
                    "education_level": self._generate_education_level(position),
                    "employee_type": self._generate_employee_type(position),
                    "manager_id": self._assign_manager(employee_id, dept),
                    "badge_number": f"B{employee_id:05d}",
                    "created_at": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat(),
                }

                employees.append(employee)
                employee_id += 1

        self._update_generation_stats("employees", count, start_time)
        return employees

    def generate_sales(self, count: int = 5000) -> List[Dict[str, Any]]:
        """Generate realistic sales data with seasonal patterns"""
        start_time = datetime.now()
        sales = []

        for i in range(count):
            # Select customer and product
            customer = random.choice(self.customers)
            product = random.choice(self.automotive_products)

            # Generate realistic transaction date with seasonal patterns
            transaction_date = self._generate_sales_date_with_seasonality()

            # Quantity based on customer type and product
            base_qty = self._calculate_base_quantity(customer, product)
            seasonal_multiplier = self._get_seasonal_multiplier(transaction_date)
            quantity = max(1, int(base_qty * seasonal_multiplier))

            # Pricing with volume discounts
            unit_price = self._calculate_unit_price(product, quantity, customer)
            total_amount = round(quantity * unit_price, 2)

            # Generate realistic order patterns
            order_priority = self._generate_order_priority(customer, total_amount)

            sale = {
                "transaction_id": f"SO{i+1:08d}",
                "order_number": f"ORD-{transaction_date.strftime('%Y%m')}-{i+1:05d}",
                "customer_name": customer["name"],
                "customer_code": f"CUST{random.randint(10000, 99999)}",
                "customer_type": customer["type"],
                "customer_size": customer["size"],
                "product_name": product["name"],
                "product_code": f"PN{random.randint(100000, 999999)}",
                "product_category": product["category"],
                "quantity": quantity,
                "unit_price": unit_price,
                "discount_percent": self._calculate_discount(
                    customer, quantity, total_amount
                ),
                "total_amount": total_amount,
                "currency": "THB",
                "transaction_date": transaction_date.strftime("%Y-%m-%d"),
                "delivery_date": (
                    transaction_date + timedelta(days=random.randint(7, 30))
                ).strftime("%Y-%m-%d"),
                "sales_rep": self._generate_sales_rep_name(),
                "sales_region": self._assign_sales_region(customer),
                "payment_terms": self._generate_payment_terms(customer),
                "payment_method": self._generate_payment_method(customer),
                "payment_status": self._generate_payment_status(transaction_date),
                "order_status": self._generate_order_status(transaction_date),
                "priority": order_priority,
                "notes": self._generate_order_notes(customer, product),
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
            }

            sales.append(sale)

        self._update_generation_stats("sales", count, start_time)
        return sales

    def generate_inventory(self, count: int = 2000) -> List[Dict[str, Any]]:
        """Generate realistic inventory data with proper stock management"""
        start_time = datetime.now()
        inventory = []

        for i in range(count):
            product = random.choice(self.automotive_products)
            location = random.choice(self.locations)

            # Generate realistic stock levels based on product type
            max_stock, min_stock, current_stock = self._calculate_stock_levels(product)
            reorder_point = min_stock + int((max_stock - min_stock) * 0.3)

            # Calculate costs and prices
            unit_cost = random.uniform(
                product["price_range"][0] * 0.6, product["price_range"][0] * 0.8
            )
            unit_price = random.uniform(*product["price_range"])

            # Determine stock status
            stock_status = self._determine_stock_status(
                current_stock, min_stock, reorder_point, max_stock
            )

            # Generate supplier information
            supplier = self._generate_supplier_info(product["category"])

            item = {
                "product_id": f"INV{i+1:07d}",
                "sku": f"SKU{random.randint(100000, 999999)}",
                "product_name": product["name"],
                "product_description": f"High-quality {product['name']} for automotive applications",
                "category": product["category"],
                "subcategory": self._generate_subcategory(product["category"]),
                "supplier_code": supplier["code"],
                "supplier_name": supplier["name"],
                "supplier_country": supplier["country"],
                "location": location,
                "warehouse_zone": f"Zone-{random.choice(['A', 'B', 'C', 'D'])}{random.randint(1, 20):02d}",
                "current_stock": current_stock,
                "available_stock": max(
                    0, current_stock - random.randint(0, int(current_stock * 0.1))
                ),
                "reserved_stock": random.randint(0, min(50, current_stock)),
                "min_stock": min_stock,
                "max_stock": max_stock,
                "reorder_point": reorder_point,
                "reorder_quantity": max_stock - min_stock,
                "unit_cost": round(unit_cost, 2),
                "unit_price": round(unit_price, 2),
                "total_value": round(current_stock * unit_cost, 2),
                "currency": "THB",
                "stock_status": stock_status,
                "condition": random.choice(
                    ["New", "New", "New", "Refurbished", "Used"]
                ),
                "quality_grade": random.choice(["A", "A", "A", "B", "C"]),
                "lot_number": f"LOT{random.randint(100000, 999999)}",
                "manufacturing_date": (
                    datetime.now() - timedelta(days=random.randint(30, 730))
                ).strftime("%Y-%m-%d"),
                "expiry_date": (
                    datetime.now() + timedelta(days=random.randint(365, 1825))
                ).strftime("%Y-%m-%d"),
                "last_movement_date": (
                    datetime.now() - timedelta(days=random.randint(1, 90))
                ).strftime("%Y-%m-%d"),
                "last_movement_type": random.choice(
                    ["IN", "OUT", "ADJUST", "TRANSFER"]
                ),
                "abc_classification": self._generate_abc_classification(
                    unit_price, current_stock
                ),
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
            }

            inventory.append(item)

        self._update_generation_stats("inventory", count, start_time)
        return inventory

    def generate_financial(self, count: int = 1000) -> List[Dict[str, Any]]:
        """Generate realistic financial transaction data"""
        start_time = datetime.now()
        financial = []

        # Chart of accounts structure
        accounts = {
            "Assets": {
                "1100": "Cash and Cash Equivalents",
                "1200": "Accounts Receivable",
                "1300": "Inventory",
                "1400": "Prepaid Expenses",
                "1500": "Property, Plant & Equipment",
            },
            "Liabilities": {
                "2100": "Accounts Payable",
                "2200": "Accrued Expenses",
                "2300": "Short-term Debt",
                "2400": "Long-term Debt",
            },
            "Equity": {"3100": "Share Capital", "3200": "Retained Earnings"},
            "Revenue": {
                "4100": "Sales Revenue",
                "4200": "Service Revenue",
                "4300": "Other Revenue",
            },
            "Expenses": {
                "5100": "Cost of Goods Sold",
                "5200": "Salaries and Benefits",
                "5300": "Rent and Utilities",
                "5400": "Depreciation",
                "5500": "Other Operating Expenses",
            },
        }

        for i in range(count):
            # Select account type and specific account
            account_type = random.choice(list(accounts.keys()))
            account_code = random.choice(list(accounts[account_type].keys()))
            account_name = accounts[account_type][account_code]

            # Generate realistic transaction amount
            amount = self._generate_financial_amount(account_type, account_name)

            # Generate transaction date with business patterns
            transaction_date = self._generate_financial_date()

            # Determine fiscal period
            fiscal_year = (
                transaction_date.year
                if transaction_date.month >= 4
                else transaction_date.year - 1
            )
            fiscal_quarter = math.ceil((transaction_date.month % 12 + 1) / 3)

            # Generate transaction details
            transaction_type = self._generate_transaction_type(account_type)

            transaction = {
                "transaction_id": f"TXN{i+1:08d}",
                "journal_entry_id": f"JE{i//random.randint(1,5)+1:06d}",
                "account_code": account_code,
                "account_name": account_name,
                "account_type": account_type,
                "transaction_type": transaction_type,
                "debit_amount": amount if random.choice([True, False]) else 0,
                "credit_amount": 0 if amount > 0 else abs(amount),
                "net_amount": amount,
                "currency": "THB",
                "exchange_rate": 1.0,
                "transaction_date": transaction_date.strftime("%Y-%m-%d"),
                "posting_date": transaction_date.strftime("%Y-%m-%d"),
                "due_date": (
                    transaction_date + timedelta(days=random.randint(0, 90))
                ).strftime("%Y-%m-%d"),
                "description": self._generate_transaction_description(
                    account_name, transaction_type
                ),
                "reference_number": f"REF{random.randint(100000, 999999)}",
                "document_number": f"DOC{random.randint(10000, 99999)}",
                "cost_center": random.choice(["CC001", "CC002", "CC003", "CC004"]),
                "department": random.choice(list(self.departments.keys())),
                "project_code": (
                    f"PRJ{random.randint(1000, 9999)}"
                    if random.random() < 0.3
                    else None
                ),
                "vendor_customer_id": (
                    f"VC{random.randint(10000, 99999)}"
                    if account_type in ["Assets", "Liabilities"]
                    else None
                ),
                "approval_status": random.choices(
                    ["Approved", "Pending", "Rejected", "Review"],
                    weights=[85, 10, 3, 2],
                )[0],
                "approved_by": self._generate_approver_name(),
                "approval_date": transaction_date.strftime("%Y-%m-%d"),
                "fiscal_year": fiscal_year,
                "fiscal_quarter": f"Q{fiscal_quarter}",
                "fiscal_period": f"{fiscal_year}-{transaction_date.month:02d}",
                "reconciled": random.choice([True, False]),
                "reconciliation_date": None,
                "notes": self._generate_financial_notes(account_type, amount),
                "created_by": random.choice(["system", "admin", "user"]),
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
            }

            financial.append(transaction)

        self._update_generation_stats("financial", count, start_time)
        return financial

    # ================ HELPER METHODS ================

    def _calculate_department_distribution(self, total_count: int) -> Dict[str, int]:
        """Calculate realistic department distribution"""
        # DENSO-like distribution
        distribution = {
            "Manufacturing": 0.40,
            "Engineering": 0.20,
            "Quality Assurance": 0.15,
            "Research & Development": 0.08,
            "Sales & Marketing": 0.07,
            "Supply Chain": 0.05,
            "Information Technology": 0.03,
            "Human Resources": 0.02,
        }

        result = {}
        remaining = total_count

        for dept, percentage in distribution.items():
            if dept == list(distribution.keys())[-1]:  # Last department gets remainder
                result[dept] = remaining
            else:
                count = int(total_count * percentage)
                result[dept] = count
                remaining -= count

        return result

    def _romanize_name(self, first_name: str, last_name: str) -> str:
        """Convert Thai names to romanized email format"""
        romanization = {
            "สมชาย": "somchai",
            "วิชาย": "wichai",
            "ประยุทธ": "prayuth",
            "ธนาคาร": "thanakon",
            "สมหญิง": "somying",
            "วิชุดา": "wichuda",
            "ใจดี": "jaidee",
            "รักดี": "rakdee",
            "สุขใส": "suksai",
            "มั่นคง": "mankong",
            "เจริญ": "charoen",
            "พัฒนา": "pattana",
        }

        first_roman = romanization.get(first_name, "user")
        last_roman = romanization.get(last_name, "lastname")

        return f"{first_roman}.{last_roman}"

    def _generate_realistic_hire_date(self) -> datetime:
        """Generate hire date with realistic patterns"""
        # Most hires in Q1 and Q3, fewer during holiday seasons
        year_weights = [0.4, 0.25, 0.2, 0.1, 0.05]  # Recent years get higher weight
        years = [datetime.now().year - i for i in range(5)]

        selected_year = random.choices(years, weights=year_weights)[0]

        # Month weights (hiring patterns)
        month_weights = [1.2, 1.0, 1.3, 0.8, 0.9, 0.7, 0.8, 0.9, 1.1, 1.2, 0.6, 0.5]
        selected_month = random.choices(range(1, 13), weights=month_weights)[0]

        # Random day in month
        import calendar

        max_day = calendar.monthrange(selected_year, selected_month)[1]
        selected_day = random.randint(1, max_day)

        return datetime(selected_year, selected_month, selected_day)

    def _generate_employment_status(self, years_service: float) -> str:
        """Generate employment status based on service years"""
        if years_service < 0.25:  # Less than 3 months
            return random.choice(["Active", "Probation"])
        elif years_service > 20:
            return random.choice(["Active", "Active", "Senior", "Retired"])
        else:
            return random.choices(
                ["Active", "On Leave", "Inactive"], weights=[95, 4, 1]
            )[0]

    def _generate_thai_phone(self) -> str:
        """Generate realistic Thai phone number"""
        prefixes = ["06", "08", "09"]  # Common Thai mobile prefixes
        prefix = random.choice(prefixes)
        number = f"{prefix}{random.randint(10000000, 99999999)}"
        return f"{number[:3]}-{number[3:6]}-{number[6:]}"

    def _generate_education_level(self, position: str) -> str:
        """Generate education level based on position"""
        if "Director" in position or "Chief" in position:
            return random.choice(["Master's Degree", "PhD", "Bachelor's Degree"])
        elif "Manager" in position or "Engineer" in position:
            return random.choice(["Bachelor's Degree", "Master's Degree", "Diploma"])
        else:
            return random.choice(["High School", "Diploma", "Bachelor's Degree"])

    def _generate_employee_type(self, position: str) -> str:
        """Generate employee type based on position"""
        if "Director" in position or "Manager" in position:
            return "Full-time"
        else:
            return random.choices(
                ["Full-time", "Part-time", "Contract", "Temporary"],
                weights=[85, 8, 5, 2],
            )[0]

    def _assign_manager(self, employee_id: int, department: str) -> str:
        """Assign manager based on organizational structure"""
        if employee_id <= 5:  # Top executives
            return None
        elif employee_id <= 20:  # Department heads
            return f"EMP{random.randint(1, 5):06d}"
        else:  # Regular employees
            return f"EMP{random.randint(max(1, employee_id//20), employee_id-1):06d}"

    def _generate_sales_date_with_seasonality(self) -> datetime:
        """Generate sales date with automotive industry seasonality"""
        # Automotive industry patterns: Q4 strong, Q2 weak
        base_date = datetime.now() - timedelta(days=random.randint(1, 730))

        # Seasonal adjustment
        month_weights = {
            1: 0.9,
            2: 0.8,
            3: 1.1,
            4: 1.0,
            5: 0.9,
            6: 0.8,
            7: 0.9,
            8: 1.0,
            9: 1.1,
            10: 1.2,
            11: 1.3,
            12: 1.2,
        }

        # Adjust probability based on month
        while True:
            candidate_date = datetime.now() - timedelta(days=random.randint(1, 730))
            weight = month_weights[candidate_date.month]
            if random.random() < weight:
                return candidate_date

    def _calculate_base_quantity(self, customer: Dict, product: Dict) -> int:
        """Calculate base quantity based on customer and product"""
        customer_multipliers = {"Large": 100, "Medium": 50, "Small": 20}
        base = customer_multipliers[customer["size"]]

        # Product-specific adjustments
        if product["category"] in ["Electronics", "Engine Parts"]:
            return random.randint(1, base // 10)  # Lower volume, higher value
        else:
            return random.randint(base // 5, base)

    def _get_seasonal_multiplier(self, date: datetime) -> float:
        """Get seasonal sales multiplier"""
        # Automotive industry seasonality
        month_multipliers = {
            1: 0.9,
            2: 0.8,
            3: 1.1,
            4: 1.0,
            5: 0.9,
            6: 0.8,
            7: 0.9,
            8: 1.0,
            9: 1.1,
            10: 1.2,
            11: 1.3,
            12: 1.2,
        }
        return month_multipliers.get(date.month, 1.0)

    def _calculate_unit_price(
        self, product: Dict, quantity: int, customer: Dict
    ) -> float:
        """Calculate unit price with volume discounts"""
        base_price = random.uniform(*product["price_range"])

        # Volume discounts
        if quantity > 100:
            discount = 0.15
        elif quantity > 50:
            discount = 0.10
        elif quantity > 20:
            discount = 0.05
        else:
            discount = 0.0

        # Customer type discounts
        customer_discounts = {"OEM": 0.20, "Distributor": 0.15, "Retailer": 0.05}
        customer_discount = customer_discounts.get(customer["type"], 0.0)

        final_discount = min(discount + customer_discount, 0.30)  # Max 30% discount
        return round(base_price * (1 - final_discount), 2)

    def _generate_order_priority(self, customer: Dict, total_amount: float) -> str:
        """Generate order priority based on customer and value"""
        if customer["type"] == "OEM" or total_amount > 100000:
            return random.choice(["High", "Critical", "Normal"])
        elif total_amount > 50000:
            return random.choice(["Normal", "High", "Low"])
        else:
            return random.choice(["Normal", "Low", "Low"])

    def _calculate_discount(
        self, customer: Dict, quantity: int, total_amount: float
    ) -> float:
        """Calculate discount percentage"""
        base_discount = 0

        # Volume discounts
        if quantity > 100:
            base_discount += 5
        elif quantity > 50:
            base_discount += 3
        elif quantity > 20:
            base_discount += 1

        # Value discounts
        if total_amount > 100000:
            base_discount += 5
        elif total_amount > 50000:
            base_discount += 3

        # Customer type discounts
        customer_discounts = {"OEM": 10, "Distributor": 7, "Retailer": 3}
        base_discount += customer_discounts.get(customer["type"], 0)

        return min(base_discount, 25)  # Max 25% discount

    def _generate_sales_rep_name(self) -> str:
        """Generate sales representative name"""
        thai_sales_reps = ["สมชาย วงศ์ใหญ่", "วิชาย ศรีสุข", "ประภา เจริญ", "ธนาคาร มั่นคง"]
        english_sales_reps = [
            "John Smith",
            "Sarah Johnson",
            "Michael Chen",
            "Lisa Williams",
        ]

        all_reps = thai_sales_reps + english_sales_reps
        return random.choice(all_reps)

    def _assign_sales_region(self, customer: Dict) -> str:
        """Assign sales region based on customer"""
        regions = ["Central", "Eastern", "Northern", "Southern", "Bangkok Metropolitan"]

        # OEMs typically in industrial areas
        if customer["type"] == "OEM":
            return random.choice(["Eastern", "Central", "Bangkok Metropolitan"])
        else:
            return random.choice(regions)

    def _generate_payment_terms(self, customer: Dict) -> str:
        """Generate payment terms based on customer type"""
        customer_terms = {
            "OEM": ["Net 60", "Net 45", "Net 30"],
            "Distributor": ["Net 30", "Net 45", "2/10 Net 30"],
            "Retailer": ["Net 30", "COD", "2/10 Net 30"],
        }

        terms = customer_terms.get(customer["type"], ["Net 30"])
        return random.choice(terms)

    def _generate_payment_method(self, customer: Dict) -> str:
        """Generate payment method based on customer"""
        if customer["size"] == "Large":
            return random.choice(
                ["Bank Transfer", "Letter of Credit", "Corporate Credit"]
            )
        elif customer["size"] == "Medium":
            return random.choice(["Bank Transfer", "Corporate Credit", "Check"])
        else:
            return random.choice(["Bank Transfer", "Check", "Cash"])

    def _generate_payment_status(self, transaction_date: datetime) -> str:
        """Generate payment status based on transaction age"""
        days_old = (datetime.now() - transaction_date).days

        if days_old > 60:
            return random.choices(["Paid", "Overdue", "Partial"], weights=[85, 10, 5])[
                0
            ]
        elif days_old > 30:
            return random.choices(["Paid", "Pending", "Overdue"], weights=[70, 25, 5])[
                0
            ]
        else:
            return random.choices(
                ["Paid", "Pending", "Processing"], weights=[50, 40, 10]
            )[0]

    def _generate_order_status(self, transaction_date: datetime) -> str:
        """Generate order status based on transaction age"""
        days_old = (datetime.now() - transaction_date).days

        if days_old > 30:
            return random.choices(
                ["Delivered", "Completed", "Cancelled"], weights=[90, 8, 2]
            )[0]
        elif days_old > 7:
            return random.choices(
                ["Shipped", "In Transit", "Delivered"], weights=[30, 40, 30]
            )[0]
        else:
            return random.choices(
                ["Processing", "Confirmed", "Shipped"], weights=[50, 30, 20]
            )[0]

    def _generate_order_notes(self, customer: Dict, product: Dict) -> str:
        """Generate order notes"""
        notes = [
            f"Standard delivery to {customer['name']}",
            f"Special packaging required for {product['name']}",
            f"Customer requested expedited processing",
            f"Quality inspection completed",
            f"Bulk order discount applied",
            "",  # Some orders have no notes
        ]
        return random.choice(notes)

    def _calculate_stock_levels(self, product: Dict) -> tuple[int, int, int]:
        """Calculate realistic stock levels"""
        # Base stock levels on product category
        category_multipliers = {
            "Electronics": (10, 100),
            "Engine Parts": (50, 500),
            "Sensors": (20, 200),
            "Electrical": (30, 300),
            "Cooling System": (25, 250),
            "Brake System": (100, 1000),
            "Ignition": (200, 2000),
            "HVAC": (15, 150),
        }

        min_range, max_range = category_multipliers.get(product["category"], (50, 500))

        max_stock = random.randint(max_range // 2, max_range)
        min_stock = random.randint(min_range, max_stock // 4)
        current_stock = random.randint(0, max_stock + int(max_stock * 0.2))

        return max_stock, min_stock, current_stock

    def _determine_stock_status(
        self, current: int, minimum: int, reorder: int, maximum: int
    ) -> str:
        """Determine stock status based on levels"""
        if current == 0:
            return "Out of Stock"
        elif current <= minimum:
            return "Critical Low"
        elif current <= reorder:
            return "Low Stock"
        elif current >= maximum:
            return "Overstock"
        else:
            return "Normal"

    def _generate_supplier_info(self, category: str) -> Dict[str, str]:
        """Generate supplier information based on category"""
        suppliers = {
            "Electronics": [
                {"code": "SUP001", "name": "Bosch Automotive", "country": "Germany"},
                {"code": "SUP002", "name": "Continental AG", "country": "Germany"},
                {"code": "SUP003", "name": "Delphi Technologies", "country": "UK"},
            ],
            "Engine Parts": [
                {"code": "SUP004", "name": "Mahle Group", "country": "Germany"},
                {"code": "SUP005", "name": "Federal-Mogul", "country": "USA"},
                {
                    "code": "SUP006",
                    "name": "Thai Engine Parts Co.",
                    "country": "Thailand",
                },
            ],
            "Sensors": [
                {"code": "SUP007", "name": "Sensata Technologies", "country": "USA"},
                {
                    "code": "SUP008",
                    "name": "Infineon Technologies",
                    "country": "Germany",
                },
                {
                    "code": "SUP009",
                    "name": "NXP Semiconductors",
                    "country": "Netherlands",
                },
            ],
        }

        category_suppliers = suppliers.get(category, suppliers["Engine Parts"])
        return random.choice(category_suppliers)

    def _generate_subcategory(self, category: str) -> str:
        """Generate subcategory based on main category"""
        subcategories = {
            "Electronics": ["Control Modules", "Sensors", "Actuators", "Displays"],
            "Engine Parts": [
                "Fuel System",
                "Ignition System",
                "Valve Train",
                "Pistons",
            ],
            "Electrical": ["Starters", "Alternators", "Batteries", "Wiring"],
            "Cooling System": ["Radiators", "Water Pumps", "Thermostats", "Fans"],
            "Brake System": ["Brake Pads", "Brake Discs", "Calipers", "ABS Components"],
        }

        category_subs = subcategories.get(category, ["General"])
        return random.choice(category_subs)

    def _generate_abc_classification(
        self, unit_price: float, current_stock: int
    ) -> str:
        """Generate ABC classification based on value"""
        total_value = unit_price * current_stock

        if total_value > 100000:
            return "A"
        elif total_value > 25000:
            return "B"
        else:
            return "C"

    def _generate_financial_amount(self, account_type: str, account_name: str) -> float:
        """Generate realistic financial amounts"""
        amount_ranges = {
            "Assets": {
                "Cash and Cash Equivalents": (1000000, 50000000),
                "Accounts Receivable": (100000, 10000000),
                "Inventory": (500000, 25000000),
                "Property, Plant & Equipment": (10000000, 500000000),
            },
            "Liabilities": {
                "Accounts Payable": (50000, 5000000),
                "Short-term Debt": (1000000, 100000000),
                "Long-term Debt": (10000000, 1000000000),
            },
            "Revenue": {
                "Sales Revenue": (100000, 50000000),
                "Service Revenue": (50000, 5000000),
            },
            "Expenses": {
                "Cost of Goods Sold": (50000, 30000000),
                "Salaries and Benefits": (100000, 10000000),
                "Rent and Utilities": (50000, 2000000),
            },
        }

        ranges = amount_ranges.get(account_type, {})
        min_amount, max_amount = ranges.get(account_name, (10000, 1000000))

        # Generate amount with realistic distribution (more small amounts)
        if random.random() < 0.7:  # 70% smaller amounts
            return round(
                random.uniform(
                    min_amount, min_amount + (max_amount - min_amount) * 0.3
                ),
                2,
            )
        else:  # 30% larger amounts
            return round(
                random.uniform(
                    min_amount + (max_amount - min_amount) * 0.3, max_amount
                ),
                2,
            )

    def _generate_financial_date(self) -> datetime:
        """Generate transaction date with business patterns"""
        # Most transactions on business days, month-end clustering
        base_date = datetime.now() - timedelta(days=random.randint(1, 365))

        # Avoid weekends (simple approximation)
        while base_date.weekday() >= 5:  # Saturday = 5, Sunday = 6
            base_date += timedelta(days=1)

        # Month-end clustering (25-31st gets higher probability)
        if base_date.day >= 25 and random.random() < 0.3:
            # Force to month-end
            import calendar

            last_day = calendar.monthrange(base_date.year, base_date.month)[1]
            base_date = base_date.replace(day=random.randint(25, last_day))

        return base_date

    def _generate_transaction_type(self, account_type: str) -> str:
        """Generate transaction type based on account"""
        types = {
            "Assets": ["Purchase", "Sale", "Transfer", "Adjustment"],
            "Liabilities": ["Payment", "Accrual", "Interest", "Adjustment"],
            "Equity": ["Investment", "Distribution", "Adjustment"],
            "Revenue": ["Sale", "Service", "Other Income"],
            "Expenses": ["Purchase", "Payroll", "Utilities", "Depreciation"],
        }

        account_types = types.get(account_type, ["General"])
        return random.choice(account_types)

    def _generate_transaction_description(
        self, account_name: str, transaction_type: str
    ) -> str:
        """Generate transaction description"""
        descriptions = {
            "Cash and Cash Equivalents": f"{transaction_type} - Cash movement",
            "Accounts Receivable": f"{transaction_type} - Customer payment",
            "Inventory": f"{transaction_type} - Inventory movement",
            "Sales Revenue": f"{transaction_type} - Product sales",
            "Cost of Goods Sold": f"{transaction_type} - COGS allocation",
            "Salaries and Benefits": f"{transaction_type} - Employee compensation",
        }

        return descriptions.get(account_name, f"{transaction_type} - {account_name}")

    def _generate_approver_name(self) -> str:
        """Generate approver name"""
        approvers = [
            "วิชาย ศรีสุข",
            "ประภา เจริญ",
            "ธนาคาร มั่นคง",
            "Michael Johnson",
            "Sarah Chen",
            "David Williams",
        ]
        return random.choice(approvers)

    def _generate_financial_notes(self, account_type: str, amount: float) -> str:
        """Generate financial notes"""
        if amount > 1000000:
            return "Large transaction - requires additional approval"
        elif account_type == "Assets":
            return "Asset transaction processed"
        elif account_type == "Liabilities":
            return "Liability adjustment recorded"
        else:
            return ""

    def _update_generation_stats(self, template: str, count: int, start_time: datetime):
        """Update generation statistics"""
        end_time = datetime.now()
        generation_time = (end_time - start_time).total_seconds()

        self.generation_stats["total_generated"] += count
        self.generation_stats["generation_time"] += generation_time
        self.generation_stats["templates_used"].add(template)

    def get_generation_stats(self) -> Dict[str, Any]:
        """Get generation statistics"""
        return {
            **self.generation_stats,
            "templates_used": list(self.generation_stats["templates_used"]),
            "avg_generation_rate": (
                self.generation_stats["total_generated"]
                / self.generation_stats["generation_time"]
                if self.generation_stats["generation_time"] > 0
                else 0
            ),
        }
