"""
core/mock_data_generator.py
Enhanced Mock Data Generator with Clear File Output Information
พัฒนาให้บอกชัดเจนว่าไฟล์ถูกสร้างที่ไหน
"""

import random
import string
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any


class MockDataGenerator:
    """Enhanced mock data generator with file path tracking"""

    def __init__(self):
        """Initialize with enhanced Thai/English data sets"""

        # Enhanced Thai names with more variety
        self.thai_first_names = [
            # Male names
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
            "ปัญญา",
            "รัชต",
            "วีระ",
            "ชัยยา",
            "อนันต์",
            "สุรชัย",
            "นพดล",
            "วรรณ",
            "ธวัช",
            "พิเชษฐ",
            "ณัฐพล",
            "ภัทร",
            "ธนา",
            "วิทยา",
            # Female names
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
            "ปัญจมา",
            "รัชนี",
            "วีรา",
            "ชัยญา",
            "อนันตา",
            "สุรนารี",
            "นงลักษณ์",
            "วรรณา",
            "ธวัลย์",
            "พิมพ์",
            "ณัฐชา",
            "ภัทรา",
            "ธนาพร",
            "วิทยากร",
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
            "วิวัฒนา",
            "ศิลปกร",
            "เทพวรรณ",
            "รัตนชัย",
            "สุวรรณ",
            "ทองคำ",
            "รุ่งเรือง",
            "เปรมจิต",
            "บุณยเกียรติ",
            "เลิศล้ำ",
            "วิสุทธิ์",
            "ไชยา",
            "ศักดิ์ดา",
            "อมรเทพ",
        ]

        # Enhanced English names
        self.english_first_names = [
            # Male names
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
            "Mark",
            "Donald",
            "Steven",
            "Paul",
            "Andrew",
            "Joshua",
            "Kenneth",
            "Kevin",
            "Brian",
            "George",
            "Timothy",
            "Ronald",
            "Jason",
            "Edward",
            "Jeffrey",
            "Ryan",
            "Jacob",
            "Gary",
            "Nicholas",
            "Eric",
            "Jonathan",
            "Stephen",
            # Female names
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
            "Michelle",
            "Emily",
            "Kimberly",
            "Donna",
            "Margaret",
            "Carol",
            "Laura",
            "Sandra",
            "Maria",
            "Ruth",
            "Sharon",
            "Helen",
            "Nancy",
            "Betty",
            "Dorothy",
            "Lisa",
            "Nancy",
            "Karen",
            "Betty",
            "Helen",
            "Sandra",
            "Donna",
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
            "Walker",
            "Young",
            "Allen",
            "King",
            "Wright",
            "Scott",
            "Torres",
            "Nguyen",
            "Hill",
            "Flores",
        ]

        # Enhanced department structure
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
            "Customer Service",
            "Legal Affairs",
            "Operations",
            "Procurement",
            "Logistics",
            "Safety & Environmental",
            "Training & Development",
        ]

        # Enhanced position hierarchy
        self.positions = {
            "Engineering": [
                "Chief Engineer",
                "Senior Engineer",
                "Engineer",
                "Junior Engineer",
                "Design Engineer",
                "Project Engineer",
                "Systems Engineer",
                "Test Engineer",
                "Development Engineer",
            ],
            "Manufacturing": [
                "Manufacturing Director",
                "Production Manager",
                "Supervisor",
                "Operator",
                "Technician",
                "Quality Controller",
                "Maintenance Engineer",
                "Production Planner",
                "Team Leader",
            ],
            "Quality Assurance": [
                "QA Director",
                "QA Manager",
                "QA Engineer",
                "QC Inspector",
                "Auditor",
                "Quality Analyst",
                "Compliance Officer",
                "Standards Specialist",
            ],
            "Research & Development": [
                "R&D Director",
                "Research Scientist",
                "Developer",
                "Innovation Manager",
                "Principal Researcher",
                "Product Designer",
                "Test Engineer",
                "Research Associate",
                "Lab Technician",
            ],
            "Sales & Marketing": [
                "Sales Director",
                "Marketing Manager",
                "Sales Representative",
                "Account Manager",
                "Marketing Specialist",
                "Business Development",
                "Customer Relations",
                "Sales Engineer",
            ],
            "Human Resources": [
                "HR Director",
                "HR Manager",
                "HR Specialist",
                "Recruiter",
                "Training Coordinator",
                "Compensation Analyst",
                "Employee Relations",
                "HR Generalist",
            ],
            "Finance & Accounting": [
                "CFO",
                "Finance Manager",
                "Accountant",
                "Financial Analyst",
                "Controller",
                "Budget Analyst",
                "Accounts Payable",
                "Accounts Receivable",
                "Tax Specialist",
            ],
            "Information Technology": [
                "CTO",
                "IT Manager",
                "Software Developer",
                "System Administrator",
                "Database Administrator",
                "Network Engineer",
                "Security Analyst",
                "Help Desk",
                "DevOps Engineer",
            ],
            "Supply Chain Management": [
                "SCM Director",
                "Logistics Manager",
                "Procurement Specialist",
                "Supply Planner",
                "Warehouse Manager",
                "Inventory Analyst",
                "Shipping Coordinator",
            ],
            "Production Planning": [
                "Planning Manager",
                "Production Planner",
                "Scheduler",
                "Demand Planner",
                "Capacity Planner",
                "Material Planner",
                "Production Analyst",
            ],
            "Customer Service": [
                "Customer Service Manager",
                "Customer Support Representative",
                "Account Coordinator",
                "Technical Support",
                "Customer Success Manager",
                "Service Specialist",
            ],
            "Legal Affairs": [
                "Chief Legal Officer",
                "Legal Counsel",
                "Paralegal",
                "Compliance Manager",
                "Contract Specialist",
                "Intellectual Property Specialist",
            ],
            "Operations": [
                "Operations Director",
                "Operations Manager",
                "Process Engineer",
                "Operations Analyst",
                "Facility Manager",
                "Operations Coordinator",
                "Process Specialist",
            ],
            "Procurement": [
                "Procurement Director",
                "Procurement Manager",
                "Buyer",
                "Sourcing Specialist",
                "Vendor Manager",
                "Contract Manager",
                "Cost Analyst",
            ],
            "Logistics": [
                "Logistics Director",
                "Logistics Manager",
                "Transportation Manager",
                "Distribution Manager",
                "Logistics Coordinator",
                "Freight Specialist",
                "Customs Specialist",
            ],
            "Safety & Environmental": [
                "Safety Director",
                "Safety Manager",
                "Safety Engineer",
                "Environmental Specialist",
                "Safety Coordinator",
                "EHS Manager",
                "Compliance Officer",
            ],
            "Training & Development": [
                "Training Director",
                "Training Manager",
                "Training Specialist",
                "L&D Coordinator",
                "Instructor",
                "Curriculum Developer",
                "Performance Analyst",
            ],
        }

        # Enhanced product categories
        self.products = [
            # Automotive parts
            "Auto Parts A1",
            "Engine Component B2",
            "Brake System C3",
            "Electrical Module D4",
            "Sensor Unit E5",
            "Control Unit F6",
            "Transmission Part G7",
            "Cooling System H8",
            "Filter Unit I9",
            "Bearing Set J10",
            "Gasket Kit K11",
            "Wire Harness L12",
            # Electronic components
            "ECU Module",
            "Ignition Coil",
            "Fuel Injector",
            "Throttle Body",
            "Mass Air Flow Sensor",
            "Oxygen Sensor",
            "Catalytic Converter",
            "Radiator",
            "Water Pump",
            "Alternator",
            "Starter Motor",
            "Battery",
            "Spark Plug",
            "Air Filter",
            "Oil Filter",
            # Industrial equipment
            "Hydraulic Pump",
            "Pneumatic Valve",
            "Motor Controller",
            "Drive Belt",
            "Coupling",
            "Gearbox",
            "Servo Motor",
            "Encoder",
            "Relay",
            "Circuit Breaker",
        ]

        # Enhanced company names
        self.companies = [
            # Japanese automotive
            "Toyota Motor Corporation",
            "Honda Motor Co., Ltd.",
            "Nissan Motor Co., Ltd.",
            "Mazda Motor Corporation",
            "Subaru Corporation",
            "Mitsubishi Motors Corporation",
            "Suzuki Motor Corporation",
            "Isuzu Motors Limited",
            "Daihatsu Motor Co., Ltd.",
            # German automotive
            "BMW Group",
            "Mercedes-Benz Group AG",
            "Audi AG",
            "Volkswagen Group",
            "Porsche AG",
            "Opel Automobile GmbH",
            # American automotive
            "Ford Motor Company",
            "General Motors Company",
            "Chrysler LLC",
            "Tesla, Inc.",
            "Rivian Automotive",
            # Korean automotive
            "Hyundai Motor Company",
            "Kia Corporation",
            # Suppliers
            "Bosch",
            "Continental AG",
            "Magna International",
            "ZF Friedrichshafen",
            "Aisin Seiki Co.",
            "Valeo",
            "Delphi Technologies",
            "Aptiv PLC",
        ]

        # Thai cities and provinces
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
            "Chiang Rai",
            "Hua Hin",
            "Rayong",
            "Chonburi",
            "Samut Prakan",
            "Nonthaburi",
            "Pathum Thani",
            "Lopburi",
            "Saraburi",
            "Nakhon Pathom",
            "Samut Sakhon",
            "Ratchaburi",
            "Kanchanaburi",
            "Suphan Buri",
            "Sing Buri",
            "Ang Thong",
            "Chai Nat",
        ]

        # File output tracking
        self.last_generated_file = None
        self.generation_log = []

    def _log_generation(
        self, operation: str, template: str, count: int, file_path: str = None
    ):
        """Log data generation for tracking"""
        log_entry = {
            "timestamp": datetime.now(),
            "operation": operation,
            "template": template,
            "count": count,
            "file_path": file_path,
            "status": "completed",
        }
        self.generation_log.append(log_entry)
        self.last_generated_file = file_path

        # Keep only last 100 entries
        if len(self.generation_log) > 100:
            self.generation_log = self.generation_log[-100:]

    def get_last_generated_info(self) -> Dict[str, Any]:
        """Get information about the last generated data"""
        if not self.generation_log:
            return {"error": "No data generated yet"}

        last_entry = self.generation_log[-1]
        return {
            "timestamp": last_entry["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
            "template": last_entry["template"],
            "count": last_entry["count"],
            "file_path": last_entry["file_path"],
            "operation": last_entry["operation"],
        }

    def generate_employees(self, count: int = 1000) -> List[Dict[str, Any]]:
        """Generate realistic employee data with enhanced variety"""
        employees = []

        print(f"🎲 Generating {count:,} employee records...")

        for i in range(count):
            # Determine if Thai or English name (70% Thai, 30% English)
            is_thai = random.random() < 0.7

            if is_thai:
                first_name = random.choice(self.thai_first_names)
                last_name = random.choice(self.thai_last_names)
                full_name = f"{first_name} {last_name}"
                email_name = self._romanize_thai_name(first_name, last_name)
            else:
                first_name = random.choice(self.english_first_names)
                last_name = random.choice(self.english_last_names)
                full_name = f"{first_name} {last_name}"
                email_name = f"{first_name.lower()}.{last_name.lower()}"

            department = random.choice(self.departments)
            position = random.choice(self.positions.get(department, ["Employee"]))

            # Generate realistic salary based on position hierarchy
            salary = self._calculate_salary(position, department)

            # Generate hire date (within last 20 years, weighted towards recent years)
            hire_date = self._generate_hire_date()

            # Calculate years of service
            years_service = (datetime.now() - hire_date).days / 365.25

            employee = {
                "employee_id": f"EMP{i+1:06d}",
                "first_name": first_name,
                "last_name": last_name,
                "full_name": full_name,
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
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            employees.append(employee)

        # Log generation
        self._log_generation("generate_employees", "employees", count)
        print(f"✅ Generated {count:,} employee records successfully!")

        return employees

    def _romanize_thai_name(self, first_name: str, last_name: str) -> str:
        """Convert Thai names to romanized email format"""
        # Simple romanization mapping
        thai_to_roman = {
            "สมชาย": "somchai",
            "วิชาย": "wichai",
            "ประยุทธ": "prayuth",
            "ธนาคาร": "thanakan",
            "อรรถพล": "atthaphon",
            "กิตติ": "kitti",
            "สมหญิง": "somying",
            "วิชุดา": "wichuda",
            "ประภา": "prapha",
            "ใจดี": "jaidee",
            "รักดี": "rakdee",
            "สุขใส": "suksai",
            "มั่นคง": "mankhong",
            "เจริญ": "charoen",
            "พัฒนา": "phattana",
        }

        first_roman = thai_to_roman.get(first_name, first_name.lower())
        last_roman = thai_to_roman.get(last_name, last_name.lower())

        return f"{first_roman}.{last_roman}"

    def _calculate_salary(self, position: str, department: str) -> int:
        """Calculate realistic salary based on position and department"""
        # Base salary ranges by position level
        salary_ranges = {
            # Executive level
            "director": (150000, 300000),
            "chief": (200000, 400000),
            "cfo": (250000, 500000),
            "cto": (200000, 400000),
            # Management level
            "manager": (80000, 180000),
            # Senior level
            "senior": (60000, 120000),
            "principal": (70000, 140000),
            "lead": (65000, 130000),
            # Regular level
            "engineer": (45000, 85000),
            "analyst": (40000, 80000),
            "specialist": (45000, 90000),
            "coordinator": (35000, 70000),
            # Entry level
            "junior": (30000, 55000),
            "associate": (32000, 58000),
            "trainee": (25000, 45000),
            "intern": (20000, 35000),
            # Operations
            "supervisor": (50000, 90000),
            "operator": (25000, 45000),
            "technician": (35000, 65000),
        }

        # Find matching salary range
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
            "Legal Affairs": 1.1,
            "Manufacturing": 0.95,
            "Customer Service": 0.9,
        }

        multiplier = dept_multipliers.get(department, 1.0)
        base_salary = random.randint(salary_range[0], salary_range[1])

        return int(base_salary * multiplier)

    def _generate_hire_date(self) -> datetime:
        """Generate realistic hire date with weighted distribution"""
        # Weight towards more recent hires
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
        if years_service < 0.1:  # Less than 1 month
            return random.choice(["Active", "Probation"])
        elif years_service > 15:  # Long service
            return random.choice(["Active", "Active", "Active", "Senior", "Retired"])
        else:
            return random.choice(
                ["Active", "Active", "Active", "Active", "On Leave", "Inactive"]
            )

    def generate_sales(self, count: int = 5000) -> List[Dict[str, Any]]:
        """Generate realistic sales transaction data"""
        sales = []

        print(f"🎲 Generating {count:,} sales records...")

        for i in range(count):
            # Generate transaction date with seasonal patterns
            transaction_date = self._generate_sales_date()

            product = random.choice(self.products)
            customer = random.choice(self.companies)

            # Quantity based on product type
            if "sensor" in product.lower() or "module" in product.lower():
                quantity = random.randint(1, 100)  # High-value, low quantity
                unit_price = round(random.uniform(500, 5000), 2)
            elif "filter" in product.lower() or "gasket" in product.lower():
                quantity = random.randint(10, 1000)  # Consumables
                unit_price = round(random.uniform(10, 100), 2)
            else:
                quantity = random.randint(1, 500)  # Standard parts
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

            # Generate realistic customer code
            customer_code = f"CUST{random.randint(10000, 99999)}"

            sale = {
                "transaction_id": f"TXN{i+1:08d}",
                "customer_name": customer,
                "customer_code": customer_code,
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
                "payment_terms": random.choice(
                    ["Net 30", "Net 45", "Net 60", "COD", "Prepaid"]
                ),
                "discount_percent": round(random.uniform(0, 15), 1),
                "tax_amount": round(total_amount * 0.07, 2),  # 7% VAT
                "delivery_status": random.choice(
                    ["Delivered", "Delivered", "In Transit", "Pending", "Cancelled"]
                ),
                "delivery_date": (
                    transaction_date + timedelta(days=random.randint(1, 30))
                ).strftime("%Y-%m-%d"),
                "order_priority": random.choice(["High", "Medium", "Medium", "Low"]),
                "sales_channel": random.choice(
                    ["Direct", "Distributor", "Online", "Retail"]
                ),
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "created_by": f"sales{random.randint(1, 50):02d}@denso.com",
            }

            sales.append(sale)

        # Log generation
        self._log_generation("generate_sales", "sales", count)
        print(f"✅ Generated {count:,} sales records successfully!")

        return sales

    def _generate_sales_date(self) -> datetime:
        """Generate sales date with realistic distribution"""
        # Weight towards recent dates
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
        elif any(word in product_lower for word in ["transmission", "gear"]):
            return "Transmission Parts"
        elif any(word in product_lower for word in ["cooling", "radiator", "fan"]):
            return "Cooling Systems"
        elif any(word in product_lower for word in ["filter", "air", "oil"]):
            return "Filters"
        elif any(word in product_lower for word in ["bearing", "gasket", "seal"]):
            return "Mechanical Parts"
        else:
            return "General Parts"

    def generate_inventory(self, count: int = 2000) -> List[Dict[str, Any]]:
        """Generate realistic inventory data"""
        inventory = []

        print(f"🎲 Generating {count:,} inventory records...")

        categories = [
            "Engine Parts",
            "Brake Systems",
            "Electrical Components",
            "Transmission Parts",
            "Cooling Systems",
            "Filters",
            "Sensors",
            "Control Units",
            "Bearings",
            "Gaskets",
            "Hydraulic Parts",
            "Pneumatic Components",
            "Safety Equipment",
            "Tools & Equipment",
        ]

        suppliers = [
            "DENSO Corporation",
            "Bosch",
            "Continental",
            "Magna International",
            "ZF Friedrichshafen",
            "Aisin Seiki",
            "Valeo",
            "Delphi Technologies",
            "Aptiv",
            "Mahle",
            "Schaeffler",
            "BorgWarner",
            "Tenneco",
            "Federal-Mogul",
        ]

        warehouses = [
            "Bangkok Main",
            "Chonburi Plant",
            "Rayong Facility",
            "Ayutthaya Center",
            "Laem Chabang Port",
            "Sriracha Warehouse",
            "Map Ta Phut",
            "Eastern Seaboard",
            "Northern Distribution",
            "Southern Hub",
        ]

        for i in range(count):
            category = random.choice(categories)
            supplier = random.choice(suppliers)
            warehouse = random.choice(warehouses)

            # Generate realistic stock levels
            max_stock = random.randint(100, 10000)
            current_stock = random.randint(0, max_stock)
            reorder_point = int(max_stock * random.uniform(0.15, 0.25))

            # Price based on category and complexity
            price_ranges = {
                "Engine Parts": (500, 8000),
                "Brake Systems": (200, 3000),
                "Electrical Components": (50, 2000),
                "Transmission Parts": (300, 5000),
                "Cooling Systems": (150, 2500),
                "Filters": (20, 300),
                "Sensors": (100, 1500),
                "Control Units": (1000, 15000),
                "Bearings": (50, 800),
                "Gaskets": (10, 200),
                "Hydraulic Parts": (200, 4000),
                "Pneumatic Components": (100, 2000),
                "Safety Equipment": (50, 1000),
                "Tools & Equipment": (100, 5000),
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

            # Generate expiry date for relevant items
            expiry_date = None
            if category in ["Filters", "Gaskets", "Safety Equipment"]:
                if random.random() < 0.3:  # 30% chance of having expiry
                    expiry_date = (
                        datetime.now() + timedelta(days=random.randint(180, 1800))
                    ).strftime("%Y-%m-%d")

            item = {
                "product_id": f"INV{i+1:07d}",
                "product_name": f"{category} - {random.choice(['Model', 'Type', 'Series'])} {random.randint(100, 999)}",
                "sku": f"SKU{random.randint(100000, 999999)}",
                "barcode": f"{random.randint(100000000000, 999999999999)}",
                "category": category,
                "subcategory": self._get_subcategory(category),
                "supplier": supplier,
                "supplier_code": f"SUP{random.randint(10000, 99999)}",
                "manufacturer": random.choice(["DENSO", "OEM Partner", "Third Party"]),
                "warehouse": warehouse,
                "location_rack": f"R{random.randint(1, 50):02d}-S{random.randint(1, 20):02d}-B{random.randint(1, 10):02d}",
                "current_stock": current_stock,
                "max_stock": max_stock,
                "min_stock": random.randint(10, reorder_point),
                "reorder_point": reorder_point,
                "reorder_quantity": random.randint(reorder_point, max_stock // 2),
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
                "last_movement": random.choice(["In", "Out", "Transfer", "Adjustment"]),
                "expiry_date": expiry_date,
                "batch_number": f"BATCH{datetime.now().strftime('%Y%m')}{random.randint(1000, 9999)}",
                "lot_number": f"LOT{random.randint(100000, 999999)}",
                "quality_grade": random.choice(["A+", "A", "A", "B+", "B"]),
                "weight_kg": round(random.uniform(0.1, 50.0), 2),
                "dimensions": f"{random.randint(10, 100)}x{random.randint(10, 100)}x{random.randint(5, 50)}mm",
                "temperature_range": f"{random.randint(-20, 0)}°C to {random.randint(80, 150)}°C",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "created_by": f"inventory{random.randint(1, 20):02d}@denso.com",
            }

            inventory.append(item)

        # Log generation
        self._log_generation("generate_inventory", "inventory", count)
        print(f"✅ Generated {count:,} inventory records successfully!")

        return inventory

    def _get_subcategory(self, category: str) -> str:
        """Get subcategory based on main category"""
        subcategories = {
            "Engine Parts": [
                "Pistons",
                "Valves",
                "Camshafts",
                "Crankshafts",
                "Timing Belts",
            ],
            "Brake Systems": [
                "Brake Pads",
                "Brake Discs",
                "Calipers",
                "Master Cylinders",
                "ABS Units",
            ],
            "Electrical Components": [
                "Sensors",
                "Modules",
                "Wiring",
                "Connectors",
                "Fuses",
            ],
            "Transmission Parts": [
                "Gears",
                "Clutches",
                "Torque Converters",
                "Filters",
                "Fluids",
            ],
            "Cooling Systems": ["Radiators", "Fans", "Pumps", "Thermostats", "Hoses"],
            "Filters": [
                "Air Filters",
                "Oil Filters",
                "Fuel Filters",
                "Cabin Filters",
                "Hydraulic Filters",
            ],
            "Sensors": ["Temperature", "Pressure", "Position", "Speed", "Flow"],
            "Control Units": [
                "ECUs",
                "TCUs",
                "BCMs",
                "ABS Controllers",
                "HVAC Controllers",
            ],
            "Bearings": [
                "Ball Bearings",
                "Roller Bearings",
                "Thrust Bearings",
                "Needle Bearings",
            ],
            "Gaskets": [
                "Head Gaskets",
                "Manifold Gaskets",
                "Oil Pan Gaskets",
                "Water Pump Gaskets",
            ],
        }

        return random.choice(
            subcategories.get(category, ["Standard", "Premium", "OEM"])
        )

    def generate_financial(self, count: int = 1000) -> List[Dict[str, Any]]:
        """Generate realistic financial transaction data"""
        financial = []

        print(f"🎲 Generating {count:,} financial records...")

        account_types = ["Assets", "Liabilities", "Equity", "Revenue", "Expenses"]
        transaction_types = [
            "Payment",
            "Receipt",
            "Transfer",
            "Adjustment",
            "Reversal",
            "Accrual",
        ]

        # Chart of accounts
        accounts = {
            "Assets": [
                "Cash",
                "Accounts Receivable",
                "Inventory",
                "Equipment",
                "Buildings",
                "Investments",
            ],
            "Liabilities": [
                "Accounts Payable",
                "Loans Payable",
                "Accrued Expenses",
                "Deferred Revenue",
            ],
            "Equity": [
                "Capital Stock",
                "Retained Earnings",
                "Additional Paid-in Capital",
            ],
            "Revenue": [
                "Sales Revenue",
                "Service Revenue",
                "Interest Income",
                "Other Income",
            ],
            "Expenses": [
                "Cost of Goods Sold",
                "Salaries",
                "Rent",
                "Utilities",
                "Depreciation",
                "Interest Expense",
            ],
        }

        for i in range(count):
            account_type = random.choice(account_types)
            account_name = random.choice(accounts[account_type])
            transaction_type = random.choice(transaction_types)

            # Generate amount based on account type and transaction type
            if account_type == "Revenue":
                amount = round(random.uniform(10000, 1000000), 2)
            elif account_type == "Assets" and "Inventory" in account_name:
                amount = round(random.uniform(50000, 5000000), 2)
            elif account_type == "Expenses":
                if "Salaries" in account_name:
                    amount = round(random.uniform(100000, 2000000), 2)
                else:
                    amount = round(random.uniform(5000, 500000), 2)
            else:
                amount = round(random.uniform(1000, 100000), 2)

            # Transaction date within last 2 years
            transaction_date = datetime.now() - timedelta(days=random.randint(0, 730))

            # Fiscal period
            fiscal_year = (
                transaction_date.year
                if transaction_date.month >= 4
                else transaction_date.year - 1
            )
            quarter = f"Q{((transaction_date.month - 1) // 3) + 1}"

            transaction = {
                "transaction_id": f"FIN{i+1:08d}",
                "account_number": f"{random.randint(1000, 9999)}-{random.randint(100, 999)}-{random.randint(10, 99)}",
                "account_name": f"{account_name}",
                "account_type": account_type,
                "transaction_type": transaction_type,
                "amount": amount,
                "currency": random.choice(["THB", "USD", "EUR", "JPY"]),
                "exchange_rate": (
                    round(random.uniform(0.8, 1.2), 4)
                    if random.choice(["THB"]) != "THB"
                    else 1.0
                ),
                "amount_thb": amount,  # Simplified for this example
                "transaction_date": transaction_date.strftime("%Y-%m-%d"),
                "posting_date": (
                    transaction_date + timedelta(days=random.randint(0, 3))
                ).strftime("%Y-%m-%d"),
                "description": self._generate_transaction_description(
                    account_type, account_name, transaction_type
                ),
                "reference_number": f"REF{random.randint(100000, 999999)}",
                "document_number": f"DOC{random.randint(100000, 999999)}",
                "counterparty": (
                    random.choice(self.companies)
                    if random.random() < 0.7
                    else "Internal"
                ),
                "department": random.choice(self.departments),
                "cost_center": f"CC{random.randint(1000, 9999)}",
                "project_code": (
                    f"PROJ{random.randint(100, 999)}" if random.random() < 0.3 else None
                ),
                "approval_status": random.choice(
                    ["Approved", "Approved", "Approved", "Pending", "Rejected"]
                ),
                "approved_by": f"{random.choice(self.english_first_names)} {random.choice(self.english_last_names)}",
                "approved_date": (
                    transaction_date + timedelta(days=random.randint(0, 5))
                ).strftime("%Y-%m-%d"),
                "fiscal_year": fiscal_year,
                "fiscal_period": f"{fiscal_year}-{quarter}",
                "quarter": quarter,
                "tax_code": random.choice(["VAT7", "WHT3", "EXEMPT", "ZERO", "IMPORT"]),
                "tax_amount": (
                    round(amount * random.uniform(0, 0.07), 2)
                    if random.random() < 0.5
                    else 0
                ),
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "created_by": f"finance{random.randint(1, 15):02d}@denso.com",
                "last_modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            financial.append(transaction)

        # Log generation
        self._log_generation("generate_financial", "financial", count)
        print(f"✅ Generated {count:,} financial records successfully!")

        return financial

    def _generate_transaction_description(
        self, account_type: str, account_name: str, transaction_type: str
    ) -> str:
        """Generate realistic transaction descriptions"""
        descriptions = {
            "Revenue": [
                f"Sales {transaction_type.lower()} for automotive parts",
                f"Service {transaction_type.lower()} - customer support",
                f"Licensing {transaction_type.lower()} - technology transfer",
            ],
            "Expenses": [
                f"Employee {account_name.lower()} {transaction_type.lower()}",
                f"Facility {account_name.lower()} payment",
                f"Operational {account_name.lower()} expense",
            ],
            "Assets": [
                f"{account_name} {transaction_type.lower()} - operational",
                f"Asset {transaction_type.lower()} - {account_name.lower()}",
            ],
        }

        desc_list = descriptions.get(
            account_type, [f"{account_name} {transaction_type}"]
        )
        return random.choice(desc_list)

    def _generate_phone(self) -> str:
        """Generate realistic Thai phone number"""
        # Mobile numbers start with 06, 08, 09
        prefix = random.choice(["06", "08", "09"])
        number = f"{prefix}{random.randint(1000000, 9999999)}"
        return f"{number[:3]}-{number[3:6]}-{number[6:]}"

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
            "last_generation": self.get_last_generated_info(),
            "generation_log": self.generation_log[-10:],  # Last 10 operations
        }

    def generate_custom_data(
        self, template: Dict[str, Any], count: int = 1000
    ) -> List[Dict[str, Any]]:
        """Generate custom data based on template definition"""
        data = []

        print(f"🎲 Generating {count:,} custom records...")

        for i in range(count):
            record = {}

            for field_name, field_config in template.items():
                field_type = field_config.get("type", "string")

                if field_type == "string":
                    record[field_name] = self._generate_string_field(field_config)
                elif field_type == "integer":
                    record[field_name] = self._generate_integer_field(field_config)
                elif field_type == "float":
                    record[field_name] = self._generate_float_field(field_config)
                elif field_type == "date":
                    record[field_name] = self._generate_date_field(field_config)
                elif field_type == "boolean":
                    record[field_name] = self._generate_boolean_field(field_config)
                elif field_type == "choice":
                    record[field_name] = self._generate_choice_field(field_config)
                else:
                    record[field_name] = f"Value_{i+1}"

            record["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data.append(record)

        # Log generation
        self._log_generation("generate_custom", "custom", count)
        print(f"✅ Generated {count:,} custom records successfully!")

        return data

    def _generate_string_field(self, config: Dict[str, Any]) -> str:
        """Generate string field based on configuration"""
        length = config.get("length", 10)
        pattern = config.get("pattern", "random")

        if pattern == "name":
            return random.choice(self.english_first_names + self.thai_first_names)
        elif pattern == "email":
            name = random.choice(self.english_first_names).lower()
            domain = random.choice(["denso.com", "example.com", "company.co.th"])
            return f"{name}@{domain}"
        elif pattern == "phone":
            return self._generate_phone()
        elif pattern == "company":
            return random.choice(self.companies)
        elif pattern == "city":
            return random.choice(self.cities)
        else:
            return "".join(
                random.choices(string.ascii_letters + string.digits, k=length)
            )

    def _generate_integer_field(self, config: Dict[str, Any]) -> int:
        """Generate integer field based on configuration"""
        min_val = config.get("min", 0)
        max_val = config.get("max", 1000)
        return random.randint(min_val, max_val)

    def _generate_float_field(self, config: Dict[str, Any]) -> float:
        """Generate float field based on configuration"""
        min_val = config.get("min", 0.0)
        max_val = config.get("max", 1000.0)
        decimals = config.get("decimals", 2)
        return round(random.uniform(min_val, max_val), decimals)

    def _generate_date_field(self, config: Dict[str, Any]) -> str:
        """Generate date field based on configuration"""
        start_date = config.get("start_date", datetime.now() - timedelta(days=365))
        end_date = config.get("end_date", datetime.now())

        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

        random_date = start_date + timedelta(
            days=random.randint(0, (end_date - start_date).days)
        )

        return random_date.strftime("%Y-%m-%d")

    def _generate_boolean_field(self, config: Dict[str, Any]) -> bool:
        """Generate boolean field based on configuration"""
        true_probability = config.get("true_probability", 0.5)
        return random.random() < true_probability

    def _generate_choice_field(self, config: Dict[str, Any]) -> str:
        """Generate choice field based on configuration"""
        choices = config.get("choices", ["Option1", "Option2", "Option3"])
        return random.choice(choices)

    def clear_generation_log(self):
        """Clear the generation log"""
        self.generation_log.clear()
        self.last_generated_file = None
        print("🗑️ Generation log cleared")

    def export_generation_log(self, file_path: str = None) -> str:
        """Export generation log to file"""
        if not file_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = f"logs/mock_generation_log_{timestamp}.json"

        # Ensure logs directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        try:
            import json

            # Convert datetime objects to strings for JSON serialization
            export_data = []
            for entry in self.generation_log:
                export_entry = entry.copy()
                export_entry["timestamp"] = entry["timestamp"].isoformat()
                export_data.append(export_entry)

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "export_date": datetime.now().isoformat(),
                        "total_operations": len(export_data),
                        "operations": export_data,
                    },
                    f,
                    indent=2,
                    ensure_ascii=False,
                )

            print(f"📊 Generation log exported to: {file_path}")
            return file_path

        except Exception as e:
            print(f"❌ Failed to export generation log: {e}")
            return ""
