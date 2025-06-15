"""
core/mock_data_generator.py
Fixed Mock Data Generator with Enhanced Error Handling
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any


class MockDataGenerator:
    """Enhanced mock data generator with robust error handling"""

    def __init__(self):
        """Initialize with Thai/English data sets"""
        # Thai names
        self.thai_first_names = [
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
        ]

        self.thai_last_names = [
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
        ]

        self.english_first_names = [
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
        ]

        self.english_last_names = [
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
        ]

        self.departments = [
            "Engineering",
            "Manufacturing",
            "Quality Assurance",
            "Research & Development",
            "Sales & Marketing",
            "Human Resources",
            "Finance & Accounting",
            "Information Technology",
            "Supply Chain Management",
            "Production Planning",
        ]

        self.positions = {
            "Engineering": [
                "Chief Engineer",
                "Senior Engineer",
                "Engineer",
                "Junior Engineer",
            ],
            "Manufacturing": [
                "Manufacturing Director",
                "Production Manager",
                "Supervisor",
                "Operator",
            ],
            "Quality Assurance": [
                "QA Director",
                "QA Manager",
                "QA Engineer",
                "QC Inspector",
            ],
            "Research & Development": [
                "R&D Director",
                "Research Scientist",
                "Developer",
            ],
            "Sales & Marketing": [
                "Sales Director",
                "Marketing Manager",
                "Sales Representative",
            ],
            "Human Resources": [
                "HR Director",
                "HR Manager",
                "HR Specialist",
                "Recruiter",
            ],
            "Finance & Accounting": [
                "CFO",
                "Finance Manager",
                "Accountant",
                "Financial Analyst",
            ],
            "Information Technology": [
                "CTO",
                "IT Manager",
                "Software Developer",
                "System Administrator",
            ],
            "Supply Chain Management": [
                "SCM Director",
                "Logistics Manager",
                "Procurement Specialist",
            ],
            "Production Planning": [
                "Planning Manager",
                "Production Planner",
                "Scheduler",
            ],
        }

        self.products = [
            "Auto Parts A1",
            "Engine Component B2",
            "Brake System C3",
            "Electrical Module D4",
            "Sensor Unit E5",
            "Control Unit F6",
            "Transmission Part G7",
            "Cooling System H8",
            "ECU Module",
            "Ignition Coil",
            "Fuel Injector",
            "Throttle Body",
            "Oxygen Sensor",
            "Hydraulic Pump",
            "Pneumatic Valve",
            "Motor Controller",
        ]

        self.companies = [
            "Toyota Motor Corporation",
            "Honda Motor Co., Ltd.",
            "Nissan Motor Co., Ltd.",
            "BMW Group",
            "Mercedes-Benz Group AG",
            "Ford Motor Company",
            "General Motors",
            "Hyundai Motor Company",
            "Bosch",
            "Continental AG",
            "Magna International",
        ]

        self.cities = [
            "Bangkok",
            "Chiang Mai",
            "Phuket",
            "Pattaya",
            "Ayutthaya",
            "Khon Kaen",
            "Udon Thani",
            "Hat Yai",
            "Nakhon Ratchasima",
            "Chonburi",
            "Rayong",
        ]

        # Generation tracking
        self.generation_log = []

    def _log_generation(self, operation: str, template: str, count: int):
        """Log data generation for tracking"""
        log_entry = {
            "timestamp": datetime.now(),
            "operation": operation,
            "template": template,
            "count": count,
            "status": "completed",
        }
        self.generation_log.append(log_entry)

        # Keep only last 100 entries
        if len(self.generation_log) > 100:
            self.generation_log = self.generation_log[-100:]

    def generate_employees(self, count: int = 1000) -> List[Dict[str, Any]]:
        """Generate realistic employee data"""
        employees = []

        for i in range(count):
            try:
                # Determine if Thai or English name (70% Thai, 30% English)
                is_thai = random.random() < 0.7

                if is_thai:
                    first_name = random.choice(self.thai_first_names)
                    last_name = random.choice(self.thai_last_names)
                    email_name = self._romanize_thai_name(first_name, last_name)
                else:
                    first_name = random.choice(self.english_first_names)
                    last_name = random.choice(self.english_last_names)
                    email_name = f"{first_name.lower()}.{last_name.lower()}"

                department = random.choice(self.departments)
                position = random.choice(self.positions.get(department, ["Employee"]))
                salary = self._calculate_salary(position, department)
                hire_date = self._generate_hire_date()
                years_service = (datetime.now() - hire_date).days / 365.25

                employee = {
                    "employee_id": f"EMP{i+1:06d}",
                    "first_name": first_name,
                    "last_name": last_name,
                    "full_name": f"{first_name} {last_name}",
                    "email": f"{email_name}@denso.com",
                    "department": department,
                    "position": position,
                    "salary": salary,
                    "hire_date": hire_date.strftime("%Y-%m-%d"),
                    "status": self._generate_employee_status(years_service),
                    "phone": self._generate_phone(),
                    "age": random.randint(22, 65),
                    "gender": random.choice(["Male", "Female"]),
                    "city": random.choice(self.cities),
                    "performance_rating": round(random.uniform(2.5, 5.0), 1),
                    "years_of_experience": max(
                        0, int(years_service) + random.randint(-3, 5)
                    ),
                    "education": random.choice(
                        ["High School", "Diploma", "Bachelor's", "Master's", "PhD"]
                    ),
                    "employee_type": random.choice(
                        ["Full-time", "Part-time", "Contract", "Intern"]
                    ),
                    "manager_id": (
                        f"EMP{random.randint(1, max(1, i//10)):06d}" if i > 0 else None
                    ),
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }

                employees.append(employee)

            except Exception as e:
                print(f"Error generating employee {i+1}: {e}")
                continue

        self._log_generation("generate_employees", "employees", len(employees))
        return employees

    def _romanize_thai_name(self, first_name: str, last_name: str) -> str:
        """Convert Thai names to romanized email format"""
        thai_to_roman = {
            "สมชาย": "somchai",
            "วิชาย": "wichai",
            "ประยุทธ": "prayuth",
            "ธนาคาร": "thanakan",
            "สมหญิง": "somying",
            "วิชุดา": "wichuda",
            "ใจดี": "jaidee",
            "รักดี": "rakdee",
            "สุขใส": "suksai",
        }

        first_roman = thai_to_roman.get(first_name, "user")
        last_roman = thai_to_roman.get(last_name, "lastname")
        return f"{first_roman}.{last_roman}"

    def _calculate_salary(self, position: str, department: str) -> int:
        """Calculate realistic salary based on position and department"""
        salary_ranges = {
            "director": (150000, 300000),
            "chief": (200000, 400000),
            "manager": (80000, 180000),
            "senior": (60000, 120000),
            "engineer": (45000, 85000),
            "analyst": (40000, 80000),
            "specialist": (45000, 90000),
            "coordinator": (35000, 70000),
            "junior": (30000, 55000),
            "supervisor": (50000, 90000),
            "operator": (25000, 45000),
            "technician": (35000, 65000),
        }

        position_lower = position.lower()
        salary_range = (40000, 70000)  # default

        for key, range_val in salary_ranges.items():
            if key in position_lower:
                salary_range = range_val
                break

        # Department multipliers
        dept_multipliers = {
            "Research & Development": 1.2,
            "Information Technology": 1.15,
            "Engineering": 1.1,
            "Finance & Accounting": 1.05,
            "Manufacturing": 0.95,
            "Customer Service": 0.9,
        }

        multiplier = dept_multipliers.get(department, 1.0)
        base_salary = random.randint(salary_range[0], salary_range[1])
        return int(base_salary * multiplier)

    def _generate_hire_date(self) -> datetime:
        """Generate realistic hire date"""
        days_ago = random.choices(
            range(30, 7300),  # 1 month to 20 years
            weights=[
                100 if d < 1095 else 50 if d < 3650 else 25 for d in range(30, 7300)
            ],
            k=1,
        )[0]
        return datetime.now() - timedelta(days=days_ago)

    def _generate_employee_status(self, years_service: float) -> str:
        """Generate employee status based on years of service"""
        if years_service < 0.1:
            return random.choice(["Active", "Probation"])
        elif years_service > 15:
            return random.choice(["Active", "Active", "Active", "Senior", "Retired"])
        else:
            return random.choice(
                ["Active", "Active", "Active", "Active", "On Leave", "Inactive"]
            )

    def _generate_phone(self) -> str:
        """Generate realistic Thai phone number"""
        prefix = random.choice(["06", "08", "09"])
        number = f"{prefix}{random.randint(1000000, 9999999)}"
        return f"{number[:3]}-{number[3:6]}-{number[6:]}"

    def generate_sales(self, count: int = 5000) -> List[Dict[str, Any]]:
        """Generate realistic sales transaction data"""
        sales = []

        for i in range(count):
            try:
                transaction_date = self._generate_sales_date()
                product = random.choice(self.products)
                customer = random.choice(self.companies)

                # Quantity based on product type
                if "sensor" in product.lower() or "module" in product.lower():
                    quantity = random.randint(1, 100)
                    unit_price = round(random.uniform(500, 5000), 2)
                elif "filter" in product.lower() or "gasket" in product.lower():
                    quantity = random.randint(10, 1000)
                    unit_price = round(random.uniform(10, 100), 2)
                else:
                    quantity = random.randint(1, 500)
                    unit_price = round(random.uniform(50, 2000), 2)

                total_amount = round(quantity * unit_price, 2)

                # Apply seasonal adjustments
                month = transaction_date.month
                if month in [11, 12, 1]:  # High season
                    quantity = int(quantity * random.uniform(1.2, 1.8))
                    total_amount = quantity * unit_price
                elif month in [6, 7, 8]:  # Low season
                    quantity = int(quantity * random.uniform(0.6, 0.9))
                    total_amount = quantity * unit_price

                sale = {
                    "transaction_id": f"TXN{i+1:08d}",
                    "customer_name": customer,
                    "customer_code": f"CUST{random.randint(10000, 99999)}",
                    "product_name": product,
                    "product_code": f"PROD{random.randint(1000, 9999)}",
                    "category": self._get_product_category(product),
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "total_amount": total_amount,
                    "currency": "THB",
                    "transaction_date": transaction_date.strftime("%Y-%m-%d"),
                    "sales_rep": f"{random.choice(self.english_first_names)} {random.choice(self.english_last_names)}",
                    "region": random.choice(
                        ["North", "South", "East", "West", "Central", "Northeast"]
                    ),
                    "country": random.choice(
                        ["Thailand", "Japan", "Germany", "USA", "China", "India"]
                    ),
                    "payment_method": random.choice(
                        [
                            "Credit Card",
                            "Bank Transfer",
                            "Cash",
                            "Check",
                            "Letter of Credit",
                        ]
                    ),
                    "payment_status": random.choice(
                        ["Paid", "Paid", "Paid", "Pending", "Overdue"]
                    ),
                    "delivery_status": random.choice(
                        ["Delivered", "Delivered", "In Transit", "Pending", "Cancelled"]
                    ),
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }

                sales.append(sale)

            except Exception as e:
                print(f"Error generating sale {i+1}: {e}")
                continue

        self._log_generation("generate_sales", "sales", len(sales))
        return sales

    def _generate_sales_date(self) -> datetime:
        """Generate sales date with realistic distribution"""
        days_ago = random.choices(
            range(1, 730),  # Last 2 years
            weights=[100 if d < 90 else 70 if d < 365 else 30 for d in range(1, 730)],
            k=1,
        )[0]
        return datetime.now() - timedelta(days=days_ago)

    def _get_product_category(self, product_name: str) -> str:
        """Categorize product based on name"""
        product_lower = product_name.lower()

        if any(word in product_lower for word in ["engine", "motor", "pump"]):
            return "Engine Components"
        elif any(word in product_lower for word in ["brake", "clutch"]):
            return "Brake Systems"
        elif any(
            word in product_lower for word in ["electrical", "sensor", "module", "ecu"]
        ):
            return "Electrical Components"
        else:
            return "General Parts"

    def generate_inventory(self, count: int = 2000) -> List[Dict[str, Any]]:
        """Generate realistic inventory data"""
        inventory = []
        categories = [
            "Engine Parts",
            "Brake Systems",
            "Electrical Components",
            "Transmission Parts",
        ]
        suppliers = ["DENSO Corporation", "Bosch", "Continental", "Magna International"]
        warehouses = [
            "Bangkok Main",
            "Chonburi Plant",
            "Rayong Facility",
            "Ayutthaya Center",
        ]

        for i in range(count):
            try:
                category = random.choice(categories)
                supplier = random.choice(suppliers)
                warehouse = random.choice(warehouses)

                max_stock = random.randint(100, 10000)
                current_stock = random.randint(0, max_stock)
                reorder_point = int(max_stock * random.uniform(0.15, 0.25))

                price_ranges = {
                    "Engine Parts": (500, 8000),
                    "Brake Systems": (200, 3000),
                    "Electrical Components": (50, 2000),
                    "Transmission Parts": (300, 5000),
                }

                price_range = price_ranges.get(category, (50, 500))
                unit_price = round(random.uniform(price_range[0], price_range[1]), 2)

                # Status based on stock level
                if current_stock == 0:
                    status = "Out of Stock"
                elif current_stock <= reorder_point:
                    status = "Low Stock"
                elif current_stock >= max_stock * 0.9:
                    status = "Overstocked"
                else:
                    status = "In Stock"

                item = {
                    "product_id": f"INV{i+1:07d}",
                    "product_name": f"{category} - Model {random.randint(100, 999)}",
                    "sku": f"SKU{random.randint(100000, 999999)}",
                    "category": category,
                    "supplier": supplier,
                    "warehouse": warehouse,
                    "current_stock": current_stock,
                    "max_stock": max_stock,
                    "min_stock": random.randint(10, reorder_point),
                    "reorder_point": reorder_point,
                    "unit_price": unit_price,
                    "total_value": round(current_stock * unit_price, 2),
                    "currency": "THB",
                    "status": status,
                    "condition": random.choice(
                        ["New", "New", "New", "Refurbished", "Used"]
                    ),
                    "last_updated": (
                        datetime.now() - timedelta(days=random.randint(0, 30))
                    ).strftime("%Y-%m-%d"),
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }

                inventory.append(item)

            except Exception as e:
                print(f"Error generating inventory item {i+1}: {e}")
                continue

        self._log_generation("generate_inventory", "inventory", len(inventory))
        return inventory

    def generate_financial(self, count: int = 1000) -> List[Dict[str, Any]]:
        """Generate realistic financial transaction data"""
        financial = []
        account_types = ["Assets", "Liabilities", "Equity", "Revenue", "Expenses"]
        transaction_types = [
            "Payment",
            "Receipt",
            "Transfer",
            "Adjustment",
            "Reversal",
            "Accrual",
        ]

        accounts = {
            "Assets": ["Cash", "Accounts Receivable", "Inventory", "Equipment"],
            "Liabilities": ["Accounts Payable", "Loans Payable", "Accrued Expenses"],
            "Equity": ["Capital Stock", "Retained Earnings"],
            "Revenue": ["Sales Revenue", "Service Revenue", "Interest Income"],
            "Expenses": ["Cost of Goods Sold", "Salaries", "Rent", "Utilities"],
        }

        for i in range(count):
            try:
                account_type = random.choice(account_types)
                account_name = random.choice(accounts[account_type])
                transaction_type = random.choice(transaction_types)

                # Generate amount based on account type
                if account_type == "Revenue":
                    amount = round(random.uniform(10000, 1000000), 2)
                elif account_type == "Expenses":
                    amount = round(random.uniform(5000, 500000), 2)
                else:
                    amount = round(random.uniform(1000, 100000), 2)

                transaction_date = datetime.now() - timedelta(
                    days=random.randint(0, 730)
                )
                fiscal_year = (
                    transaction_date.year
                    if transaction_date.month >= 4
                    else transaction_date.year - 1
                )

                transaction = {
                    "transaction_id": f"FIN{i+1:08d}",
                    "account_number": f"{random.randint(1000, 9999)}-{random.randint(100, 999)}",
                    "account_name": account_name,
                    "account_type": account_type,
                    "transaction_type": transaction_type,
                    "amount": amount,
                    "currency": random.choice(["THB", "USD", "EUR", "JPY"]),
                    "transaction_date": transaction_date.strftime("%Y-%m-%d"),
                    "description": f"{account_name} {transaction_type}",
                    "reference_number": f"REF{random.randint(100000, 999999)}",
                    "department": random.choice(self.departments),
                    "approval_status": random.choice(
                        ["Approved", "Approved", "Approved", "Pending", "Rejected"]
                    ),
                    "fiscal_year": fiscal_year,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }

                financial.append(transaction)

            except Exception as e:
                print(f"Error generating financial record {i+1}: {e}")
                continue

        self._log_generation("generate_financial", "financial", len(financial))
        return financial

    def get_available_templates(self) -> List[Dict[str, Any]]:
        """Get available mock data templates"""
        return [
            {
                "name": "employees",
                "title": "👥 Employee Records",
                "description": "Realistic employee data with Thai/English names, departments, and salaries",
                "fields": [
                    "ID",
                    "Name",
                    "Email",
                    "Department",
                    "Position",
                    "Salary",
                    "Hire Date",
                    "Status",
                ],
                "recommended_count": "1,000 - 50,000",
                "color": "#3B82F6",
            },
            {
                "name": "sales",
                "title": "💰 Sales Transactions",
                "description": "Sales data with products, customers, seasonal trends, and payment details",
                "fields": [
                    "Transaction ID",
                    "Customer",
                    "Product",
                    "Quantity",
                    "Price",
                    "Total",
                    "Date",
                ],
                "recommended_count": "5,000 - 100,000",
                "color": "#10B981",
            },
            {
                "name": "inventory",
                "title": "📦 Inventory Items",
                "description": "Product inventory with stock levels, suppliers, and warehouse locations",
                "fields": [
                    "Product ID",
                    "Name",
                    "Category",
                    "Stock",
                    "Price",
                    "Supplier",
                    "Location",
                ],
                "recommended_count": "500 - 10,000",
                "color": "#F59E0B",
            },
            {
                "name": "financial",
                "title": "💳 Financial Records",
                "description": "Financial transactions with accounts, approvals, and fiscal reporting",
                "fields": [
                    "Account",
                    "Transaction",
                    "Amount",
                    "Type",
                    "Date",
                    "Reference",
                    "Balance",
                ],
                "recommended_count": "1,000 - 25,000",
                "color": "#8B5CF6",
            },
        ]

    def get_generation_statistics(self) -> Dict[str, Any]:
        """Get statistics about generated data"""
        if not self.generation_log:
            return {"total_operations": 0, "total_records": 0}

        total_records = sum(entry["count"] for entry in self.generation_log)
        templates_used = list(set(entry["template"] for entry in self.generation_log))

        return {
            "total_operations": len(self.generation_log),
            "total_records": total_records,
            "templates_used": templates_used,
            "last_generation": self.generation_log[-1] if self.generation_log else None,
            "generation_log": self.generation_log[-10:],
        }
