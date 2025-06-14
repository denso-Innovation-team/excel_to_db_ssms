"""
core/mock_data_generator.py
Enhanced Mock Data Generator for DENSO888 2025
Created by: Thammaphon Chittasuwanna (SDM) | Innovation Department
"""

import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any


class MockDataGenerator:
    """Enhanced mock data generator with realistic Thai/English data"""

    def __init__(self):
        self.thai_first_names = [
            "สมชาย",
            "สมหญิง",
            "วิชาย",
            "วิชุดา",
            "ประยุทธ",
            "ประภา",
            "ธนาคาร",
            "ธนากร",
            "อรรถพล",
            "อรรถศิษฎ์",
            "กิตติ",
            "กิตติยา",
            "ปิยะ",
            "ปิยวดี",
            "เศรษฐา",
            "เศรษฐี",
            "ธีระ",
            "ธีรนุช",
            "นิรันดร์",
            "นิรมล",
            "ปัญญา",
            "ปัญจมา",
            "รัชต",
            "รัชนี",
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
        ]

        self.english_first_names = [
            "John",
            "Jane",
            "Michael",
            "Sarah",
            "David",
            "Lisa",
            "Robert",
            "Jennifer",
            "William",
            "Jessica",
            "James",
            "Ashley",
            "Christopher",
            "Amanda",
            "Daniel",
            "Stephanie",
            "Matthew",
            "Nicole",
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
        ]

        self.departments = [
            "Engineering",
            "Manufacturing",
            "Quality Assurance",
            "R&D",
            "Sales & Marketing",
            "Human Resources",
            "Finance",
            "IT",
            "Supply Chain",
            "Production Planning",
            "Customer Service",
            "Legal",
        ]

        self.positions = {
            "Engineering": [
                "Senior Engineer",
                "Engineer",
                "Junior Engineer",
                "Team Lead",
                "Manager",
            ],
            "Manufacturing": [
                "Production Supervisor",
                "Operator",
                "Technician",
                "Manager",
                "Director",
            ],
            "Quality Assurance": [
                "QA Engineer",
                "QC Inspector",
                "QA Manager",
                "Auditor",
            ],
            "R&D": [
                "Research Scientist",
                "Developer",
                "Innovation Manager",
                "Principal Researcher",
            ],
            "Sales & Marketing": [
                "Sales Representative",
                "Account Manager",
                "Marketing Specialist",
                "Sales Director",
            ],
            "Human Resources": ["HR Specialist", "Recruiter", "HR Manager", "Director"],
            "Finance": ["Accountant", "Financial Analyst", "Controller", "CFO"],
            "IT": ["Developer", "System Administrator", "IT Manager", "CTO"],
            "Supply Chain": [
                "Logistics Coordinator",
                "Procurement Specialist",
                "SCM Manager",
            ],
            "Production Planning": ["Planner", "Scheduler", "Planning Manager"],
            "Customer Service": [
                "Customer Support",
                "Account Coordinator",
                "Service Manager",
            ],
            "Legal": ["Legal Counsel", "Paralegal", "Legal Director"],
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
            "Filter Unit I9",
            "Bearing Set J10",
            "Gasket Kit K11",
            "Wire Harness L12",
        ]

        self.companies = [
            "Toyota Motor Corp",
            "Honda Motor Co",
            "Nissan Motor Co",
            "Mazda Motor Corp",
            "Subaru Corporation",
            "Mitsubishi Motors",
            "BMW Group",
            "Mercedes-Benz",
            "Audi AG",
            "Volkswagen Group",
            "Ford Motor Company",
            "General Motors",
            "Hyundai Motor",
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
            "Chiang Rai",
            "Hua Hin",
            "Rayong",
            "Chonburi",
            "Samut Prakan",
        ]

    def generate_employees(self, count: int = 1000) -> List[Dict[str, Any]]:
        """Generate realistic employee data"""
        employees = []

        for i in range(count):
            # Determine if Thai or English name (70% Thai, 30% English)
            is_thai = random.random() < 0.7

            if is_thai:
                first_name = random.choice(self.thai_first_names)
                last_name = random.choice(self.thai_last_names)
                full_name = f"{first_name} {last_name}"
                email_name = f"{first_name.lower()}.{last_name.lower()}"
            else:
                first_name = random.choice(self.english_first_names)
                last_name = random.choice(self.english_last_names)
                full_name = f"{first_name} {last_name}"
                email_name = f"{first_name.lower()}.{last_name.lower()}"

            department = random.choice(self.departments)
            position = random.choice(self.positions[department])

            # Generate realistic salary based on position
            base_salaries = {
                "Director": (120000, 200000),
                "Manager": (80000, 150000),
                "Senior Engineer": (60000, 100000),
                "Engineer": (45000, 75000),
                "Junior Engineer": (35000, 55000),
                "Team Lead": (70000, 120000),
                "Specialist": (50000, 80000),
                "Coordinator": (40000, 65000),
                "Supervisor": (55000, 85000),
                "Operator": (25000, 40000),
                "Technician": (35000, 55000),
            }

            # Find salary range based on position keywords
            salary_range = (30000, 50000)  # default
            for key, range_val in base_salaries.items():
                if key.lower() in position.lower():
                    salary_range = range_val
                    break

            salary = random.randint(salary_range[0], salary_range[1])

            # Generate hire date (within last 10 years)
            start_date = datetime.now() - timedelta(days=3650)
            hire_date = start_date + timedelta(days=random.randint(0, 3650))

            employee = {
                "employee_id": f"EMP{i+1:05d}",
                "first_name": first_name,
                "last_name": last_name,
                "full_name": full_name,
                "email": f"{email_name}@denso.com",
                "department": department,
                "position": position,
                "salary": salary,
                "hire_date": hire_date.strftime("%Y-%m-%d"),
                "status": random.choice(
                    ["Active", "Active", "Active", "On Leave", "Inactive"]
                ),
                "phone": self._generate_phone(),
                "age": random.randint(22, 65),
                "gender": random.choice(["Male", "Female"]),
                "city": random.choice(self.cities),
                "performance_rating": round(random.uniform(2.5, 5.0), 1),
                "years_of_experience": random.randint(0, 30),
                "education": random.choice(
                    ["Bachelor's", "Master's", "PhD", "Diploma"]
                ),
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            employees.append(employee)

        return employees

    def generate_sales(self, count: int = 5000) -> List[Dict[str, Any]]:
        """Generate realistic sales transaction data"""
        sales = []

        for i in range(count):
            # Generate transaction date (within last 2 years)
            start_date = datetime.now() - timedelta(days=730)
            transaction_date = start_date + timedelta(days=random.randint(0, 730))

            product = random.choice(self.products)
            customer = random.choice(self.companies)

            quantity = random.randint(1, 1000)
            unit_price = round(random.uniform(10.0, 5000.0), 2)
            total_amount = round(quantity * unit_price, 2)

            # Add seasonal variations
            month = transaction_date.month
            if month in [11, 12, 1]:  # High season
                quantity = int(quantity * random.uniform(1.2, 1.8))
                total_amount = quantity * unit_price
            elif month in [6, 7, 8]:  # Low season
                quantity = int(quantity * random.uniform(0.6, 0.9))
                total_amount = quantity * unit_price

            sale = {
                "transaction_id": f"TXN{i+1:07d}",
                "customer_name": customer,
                "customer_code": f"CUST{random.randint(1000, 9999)}",
                "product_name": product,
                "product_code": f"PROD{random.randint(100, 999)}",
                "quantity": quantity,
                "unit_price": unit_price,
                "total_amount": total_amount,
                "currency": "THB",
                "transaction_date": transaction_date.strftime("%Y-%m-%d"),
                "sales_rep": f"{random.choice(self.english_first_names)} {random.choice(self.english_last_names)}",
                "region": random.choice(["North", "South", "East", "West", "Central"]),
                "payment_method": random.choice(
                    ["Credit Card", "Bank Transfer", "Cash", "Check"]
                ),
                "payment_status": random.choice(
                    ["Paid", "Paid", "Paid", "Pending", "Overdue"]
                ),
                "discount_percent": round(random.uniform(0, 15), 1),
                "tax_amount": round(total_amount * 0.07, 2),  # 7% VAT
                "delivery_status": random.choice(
                    ["Delivered", "Delivered", "In Transit", "Pending"]
                ),
                "order_priority": random.choice(["High", "Medium", "Medium", "Low"]),
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            sales.append(sale)

        return sales

    def generate_inventory(self, count: int = 2000) -> List[Dict[str, Any]]:
        """Generate realistic inventory data"""
        inventory = []

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
        ]

        warehouses = [
            "Bangkok Main",
            "Chonburi Plant",
            "Rayong Facility",
            "Ayutthaya Center",
            "Laem Chabang Port",
        ]

        for i in range(count):
            category = random.choice(categories)

            # Generate stock levels with realistic distribution
            max_stock = random.randint(100, 10000)
            current_stock = random.randint(0, max_stock)
            reorder_point = int(max_stock * 0.2)  # 20% of max stock

            # Price based on category
            price_ranges = {
                "Engine Parts": (500, 5000),
                "Brake Systems": (200, 2000),
                "Electrical Components": (50, 1000),
                "Transmission Parts": (300, 3000),
                "Cooling Systems": (150, 1500),
                "Filters": (20, 200),
                "Sensors": (100, 800),
                "Control Units": (1000, 8000),
                "Bearings": (50, 500),
                "Gaskets": (10, 100),
            }

            price_range = price_ranges.get(category, (50, 500))
            unit_price = round(random.uniform(price_range[0], price_range[1]), 2)

            # Status based on stock level
            if current_stock == 0:
                status = "Out of Stock"
            elif current_stock <= reorder_point:
                status = "Low Stock"
            elif current_stock >= max_stock * 0.8:
                status = "Overstocked"
            else:
                status = "In Stock"

            item = {
                "product_id": f"INV{i+1:06d}",
                "product_name": f"{category} - Model {random.randint(100, 999)}",
                "sku": f"SKU{random.randint(100000, 999999)}",
                "category": category,
                "supplier": random.choice(suppliers),
                "supplier_code": f"SUP{random.randint(1000, 9999)}",
                "warehouse": random.choice(warehouses),
                "current_stock": current_stock,
                "max_stock": max_stock,
                "reorder_point": reorder_point,
                "unit_price": unit_price,
                "total_value": round(current_stock * unit_price, 2),
                "status": status,
                "last_updated": (
                    datetime.now() - timedelta(days=random.randint(0, 30))
                ).strftime("%Y-%m-%d"),
                "expiry_date": (
                    (
                        datetime.now() + timedelta(days=random.randint(30, 1800))
                    ).strftime("%Y-%m-%d")
                    if random.random() < 0.3
                    else None
                ),
                "batch_number": f"BATCH{random.randint(1000, 9999)}",
                "quality_grade": random.choice(["A+", "A", "A", "B+", "B"]),
                "location_rack": f"R{random.randint(1, 50):02d}-S{random.randint(1, 10):02d}",
                "weight_kg": round(random.uniform(0.1, 50.0), 2),
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            inventory.append(item)

        return inventory

    def generate_financial(self, count: int = 1000) -> List[Dict[str, Any]]:
        """Generate realistic financial transaction data"""
        financial = []

        account_types = ["Assets", "Liabilities", "Equity", "Revenue", "Expenses"]

        transaction_types = ["Payment", "Receipt", "Transfer", "Adjustment", "Reversal"]

        for i in range(count):
            account_type = random.choice(account_types)

            # Generate amount based on transaction type
            if account_type in ["Revenue", "Assets"]:
                amount = round(random.uniform(1000, 1000000), 2)
            elif account_type == "Expenses":
                amount = round(random.uniform(500, 500000), 2)
            else:
                amount = round(random.uniform(100, 100000), 2)

            # Transaction date within last year
            transaction_date = datetime.now() - timedelta(days=random.randint(0, 365))

            transaction = {
                "transaction_id": f"FIN{i+1:07d}",
                "account_number": f"{random.randint(1000, 9999)}-{random.randint(100, 999)}",
                "account_name": f"{account_type} Account {random.randint(1, 100)}",
                "account_type": account_type,
                "transaction_type": random.choice(transaction_types),
                "amount": amount,
                "currency": "THB",
                "transaction_date": transaction_date.strftime("%Y-%m-%d"),
                "description": f"Transaction for {account_type.lower()} - {random.choice(['Operations', 'Maintenance', 'Investment', 'Sales', 'Purchase'])}",
                "reference_number": f"REF{random.randint(100000, 999999)}",
                "counterparty": random.choice(self.companies),
                "approval_status": random.choice(
                    ["Approved", "Approved", "Pending", "Rejected"]
                ),
                "approved_by": f"{random.choice(self.english_first_names)} {random.choice(self.english_last_names)}",
                "cost_center": f"CC{random.randint(1000, 9999)}",
                "project_code": f"PROJ{random.randint(100, 999)}",
                "fiscal_year": transaction_date.year,
                "quarter": f"Q{((transaction_date.month - 1) // 3) + 1}",
                "tax_code": random.choice(["VAT7", "WHT3", "EXEMPT", "ZERO"]),
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            financial.append(transaction)

        return financial

    def _generate_phone(self) -> str:
        """Generate realistic Thai phone number"""
        # Mobile numbers start with 06, 08, 09
        prefix = random.choice(["06", "08", "09"])
        number = f"{prefix}{random.randint(1000000, 9999999)}"
        return f"{number[:3]}-{number[3:6]}-{number[6:]}"

    def _generate_email(
        self, first_name: str, last_name: str, domain: str = "denso.com"
    ) -> str:
        """Generate email address"""
        return f"{first_name.lower()}.{last_name.lower()}@{domain}"

    def generate_custom_data(
        self, template: Dict[str, Any], count: int = 1000
    ) -> List[Dict[str, Any]]:
        """Generate custom data based on template definition"""
        data = []

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

            data.append(record)

        return data

    def _generate_string_field(self, config: Dict[str, Any]) -> str:
        """Generate string field based on configuration"""
        length = config.get("length", 10)
        pattern = config.get("pattern", "random")

        if pattern == "name":
            return random.choice(self.english_first_names + self.thai_first_names)
        elif pattern == "email":
            name = random.choice(self.english_first_names).lower()
            return f"{name}@example.com"
        elif pattern == "phone":
            return self._generate_phone()
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


# Fixed App Controller with proper error handling
class AppController:
    """Enhanced Application Controller with bug fixes"""

    def __init__(self, config):
        self.config = config
        self.db_config = None
        self.db_manager = None
        self.excel_handler = None
        self.mock_generator = MockDataGenerator()

        # State management
        self.current_file = None
        self.is_connected = False
        self.file_info = None

        # Event system
        self.event_callbacks = {
            "db_status_changed": [],
            "file_selected": [],
            "progress_update": [],
            "operation_complete": [],
            "error_occurred": [],
            "log_message": [],
        }

        self._initialize_components()

    def _initialize_components(self):
        """Initialize core components with error handling"""
        try:
            # Initialize database config
            from models.database_config import DatabaseConfig

            self.db_config = DatabaseConfig()

            # Initialize Excel handler
            from core.excel_handler import ExcelHandler

            self.excel_handler = ExcelHandler()

            self.log("Application controller initialized successfully")

        except Exception as e:
            self.log(f"Failed to initialize some components: {e}", "WARNING")

    def subscribe(self, event: str, callback):
        """Subscribe to application events"""
        if event in self.event_callbacks:
            self.event_callbacks[event].append(callback)

    def emit_event(self, event: str, data=None):
        """Emit event to all subscribers"""
        if event in self.event_callbacks:
            for callback in self.event_callbacks[event]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"Event callback error: {e}")

    def log(self, message: str, level: str = "INFO"):
        """Log message and emit to UI"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        print(f"[{level}] {formatted_message}")

        self.emit_event("log_message", {"message": formatted_message, "level": level})

    def update_database_config(self, config_data):
        """Update database configuration"""
        if self.db_config:
            self.db_config.update_from_dict(config_data)
            self.log(f"Database config updated: {self.db_config.db_type}")

    def test_database_connection(self) -> bool:
        """Test database connection"""
        try:
            if not self.db_config:
                self.log("Database configuration not available", "ERROR")
                return False

            # Import database manager
            from core.database_manager import DatabaseManager

            # Create temporary manager for testing
            test_manager = DatabaseManager(self.db_config.__dict__)
            success, message = test_manager.test_connection()

            if success:
                self.log(f"Database test successful: {message}")
                return True
            else:
                self.log(f"Database test failed: {message}", "ERROR")
                return False

        except Exception as e:
            self.log(f"Database test error: {e}", "ERROR")
            return False

    def connect_database(self) -> bool:
        """Connect to database"""
        try:
            if not self.db_config:
                self.log("Database configuration not available", "ERROR")
                return False

            # Import database manager
            from core.database_manager import DatabaseManager

            # Create database manager
            self.db_manager = DatabaseManager(self.db_config.__dict__)
            success, message = self.db_manager.connect()

            if success:
                self.is_connected = True
                self.log(f"Database connected: {message}")
                self.emit_event("db_status_changed", True)
                return True
            else:
                self.is_connected = False
                self.log(f"Database connection failed: {message}", "ERROR")
                self.emit_event("db_status_changed", False)
                return False

        except Exception as e:
            self.is_connected = False
            self.log(f"Database connection error: {e}", "ERROR")
            self.emit_event("error_occurred", str(e))
            return False

    def get_database_status(self):
        """Get current database status"""
        return {
            "connected": self.is_connected,
            "type": self.db_config.db_type if self.db_config else "unknown",
        }

    def select_file(self, file_path: str) -> bool:
        """Select and analyze Excel file"""
        try:
            if not self.excel_handler:
                self.log("Excel handler not available", "ERROR")
                return False

            self.current_file = file_path
            self.file_info = self.excel_handler.load_file(file_path)

            if "error" in self.file_info:
                self.log(f"Failed to load file: {self.file_info['error']}", "ERROR")
                return False

            self.log(f"File selected: {self.file_info.get('file_name', 'Unknown')}")
            self.emit_event("file_selected", self.file_info)
            return True

        except Exception as e:
            self.log(f"File selection error: {e}", "ERROR")
            return False

    def get_file_info(self):
        """Get current file information"""
        return self.file_info

    def generate_mock_data(
        self, template: str, count: int, table_name: str = None
    ) -> bool:
        """Generate mock data"""
        try:
            if not self.is_connected:
                self.log("Database not connected", "ERROR")
                return False

            self.log(f"Generating {count:,} rows of {template} data")

            # Generate data based on template
            if template == "employees":
                data = self.mock_generator.generate_employees(count)
            elif template == "sales":
                data = self.mock_generator.generate_sales(count)
            elif template == "inventory":
                data = self.mock_generator.generate_inventory(count)
            elif template == "financial":
                data = self.mock_generator.generate_financial(count)
            else:
                self.log(f"Unknown template: {template}", "ERROR")
                return False

            if not table_name:
                table_name = (
                    f"mock_{template}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                )

            # Create table and insert data
            if self.db_manager:
                success, message = self.db_manager.create_table_from_data(
                    table_name, data
                )
                if success:
                    success, message = self.db_manager.insert_data(table_name, data)
                    if success:
                        self.log(f"Successfully generated {count:,} {template} records")
                        self.emit_event(
                            "operation_complete",
                            {
                                "operation": "mock_generation",
                                "success": True,
                                "data": {
                                    "table_name": table_name,
                                    "rows_generated": count,
                                    "template": template,
                                },
                            },
                        )
                        return True

            self.log("Failed to create table or insert data", "ERROR")
            return False

        except Exception as e:
            self.log(f"Mock data generation error: {e}", "ERROR")
            return False

    def get_available_templates(self):
        """Get available mock data templates"""
        return [
            {
                "name": "employees",
                "description": "Employee records with departments and salaries",
                "fields": ["ID", "Name", "Email", "Department", "Position", "Salary"],
            },
            {
                "name": "sales",
                "description": "Sales transactions with products and customers",
                "fields": ["Transaction ID", "Customer", "Product", "Amount", "Date"],
            },
            {
                "name": "inventory",
                "description": "Product inventory with stock levels",
                "fields": ["Product ID", "Name", "Category", "Stock", "Price"],
            },
            {
                "name": "financial",
                "description": "Financial transactions and accounts",
                "fields": ["Account", "Transaction", "Amount", "Type", "Date"],
            },
        ]

    def shutdown(self):
        """Cleanup resources"""
        if self.db_manager:
            try:
                self.db_manager.close()
            except:
                pass

        self.log("Application controller shutdown complete")


# Export classes
__all__ = ["MockDataGenerator", "AppController"]
