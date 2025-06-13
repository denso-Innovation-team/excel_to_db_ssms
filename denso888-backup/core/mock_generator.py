"""Enhanced mock data generator with realistic data patterns and performance optimization"""

import pandas as pd
import random
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class DataPatterns:
    """Realistic data patterns for mock generation"""

    # Thai and English names
    THAI_FIRST_NAMES = [
        "สมชาย",
        "สิริพร",
        "นิรันดร์",
        "วิภาดา",
        "อาทิตย์",
        "กัญญา",
        "ประชา",
        "สุดา",
        "ธวัช",
        "มาลี",
        "บุญดิษฐ์",
        "เพ็ญศรี",
        "ชัยวัฒน์",
        "ศิริพรรณ",
        "มานพ",
        "วันดี",
        "พิษณุ",
        "อรุณี",
        "เกษม",
        "จิราพร",
        "วีระ",
        "สุภาพร",
        "เดชา",
        "มณีรัตน์",
    ]

    ENGLISH_FIRST_NAMES = [
        "John",
        "Mary",
        "David",
        "Sarah",
        "Michael",
        "Emma",
        "James",
        "Lisa",
        "Robert",
        "Jennifer",
        "William",
        "Jessica",
        "Richard",
        "Ashley",
        "Christopher",
        "Amanda",
        "Matthew",
        "Melissa",
        "Anthony",
        "Deborah",
        "Mark",
        "Stephanie",
        "Donald",
        "Dorothy",
    ]

    THAI_LAST_NAMES = [
        "ใจดี",
        "ศิริโชติ",
        "วรรณกุล",
        "ธนกิจ",
        "ศรีสวัสดิ์",
        "พรหมมิน",
        "เจริญสุข",
        "วงษ์ทอง",
        "กันตพล",
        "ศิริวัฒน์",
        "สุขสันต์",
        "ทองคำ",
        "ปิยะกุล",
        "สมบูรณ์",
        "ราชสีห์",
        "กิตติกุล",
    ]

    ENGLISH_LAST_NAMES = [
        "Smith",
        "Johnson",
        "Brown",
        "Wilson",
        "Davis",
        "Miller",
        "Garcia",
        "Rodriguez",
        "Martinez",
        "Anderson",
        "Taylor",
        "Thomas",
        "Hernandez",
        "Moore",
        "Martin",
        "Jackson",
    ]

    # Company and location data
    DEPARTMENTS = [
        "Sales",
        "Marketing",
        "IT",
        "HR",
        "Finance",
        "Operations",
        "Engineering",
        "Customer Service",
        "Quality Assurance",
        "Procurement",
        "Legal",
        "R&D",
        "Manufacturing",
        "Supply Chain",
        "Business Development",
        "Administration",
    ]

    POSITIONS = [
        "Manager",
        "Senior Manager",
        "Director",
        "Vice President",
        "Analyst",
        "Senior Analyst",
        "Specialist",
        "Senior Specialist",
        "Coordinator",
        "Team Lead",
        "Supervisor",
        "Executive",
        "Assistant",
        "Associate",
        "Officer",
        "Representative",
        "Consultant",
    ]

    THAI_CITIES = [
        "กรุงเทพมหานคร",
        "เชียงใหม่",
        "ภูเก็ต",
        "พัทยา",
        "ขอนแก่น",
        "อุดรธานี",
        "หาดใหญ่",
        "ระยอง",
        "ชลบุรี",
        "นนทบุรี",
        "สมุทรปราการ",
        "ปทุมธานี",
        "นครราชสีมา",
        "อุบลราชธานี",
    ]

    PRODUCT_CATEGORIES = [
        "Electronics",
        "Automotive",
        "Home & Garden",
        "Sports & Recreation",
        "Books & Media",
        "Clothing & Fashion",
        "Food & Beverage",
        "Health & Beauty",
        "Toys & Games",
        "Office Supplies",
        "Industrial Equipment",
        "Software & Technology",
    ]

    PRODUCT_NAMES = [
        "Premium Widget",
        "Smart Device",
        "Essential Tool",
        "Power Unit",
        "Control Module",
        "Safety Component",
        "Performance Part",
        "Quality Assembly",
        "Standard Kit",
        "Advanced System",
        "Professional Grade",
        "Industrial Strength",
        "Heavy Duty",
        "Precision Instrument",
    ]

    # Financial patterns
    EXPENSE_CATEGORIES = [
        "Office Supplies",
        "Travel & Entertainment",
        "Marketing",
        "Utilities",
        "Equipment",
        "Software Licenses",
        "Professional Services",
        "Insurance",
        "Rent",
        "Maintenance",
        "Training & Development",
        "Communications",
        "Legal & Compliance",
    ]

    ACCOUNT_TYPES = [
        "Cash",
        "Bank - SCB",
        "Bank - BBL",
        "Bank - KTB",
        "Accounts Receivable",
        "Accounts Payable",
        "Revenue",
        "Cost of Goods Sold",
        "Operating Expenses",
        "Assets",
        "Liabilities",
        "Equity",
    ]


class MockDataGenerator:
    """Enhanced mock data generator with realistic patterns"""

    def __init__(self, locale: str = "mixed", seed: Optional[int] = None):
        """
        Initialize generator with locale and optional seed for reproducibility

        Args:
            locale: "thai", "english", or "mixed"
            seed: Random seed for reproducible data
        """
        self.locale = locale
        if seed:
            random.seed(seed)

        self.patterns = DataPatterns()
        self._performance_cache = {}

    def generate_employee_data(
        self, num_rows: int = 1000, include_relationships: bool = False
    ) -> pd.DataFrame:
        """Generate realistic employee data with optional relationships"""

        logger.info(f"Generating {num_rows:,} employee records...")

        data = []

        # Pre-generate some data for better performance
        departments = random.choices(self.patterns.DEPARTMENTS, k=num_rows)
        positions = random.choices(self.patterns.POSITIONS, k=num_rows)
        cities = random.choices(self.patterns.THAI_CITIES, k=num_rows)

        for i in range(num_rows):
            # Generate names based on locale
            first_name, last_name = self._generate_person_name()

            # Department hierarchy logic
            department = departments[i]
            position = positions[i]

            # Realistic salary based on position and department
            base_salary = self._calculate_realistic_salary(position, department)

            # Generate dates
            hire_date = self._generate_hire_date()
            birth_date = self._generate_birth_date(hire_date)

            # Performance and status
            performance_score = self._generate_performance_score(position)
            is_active = self._determine_employee_status(hire_date)

            record = {
                "employee_id": f"EMP{i+1:06d}",
                "first_name": first_name,
                "last_name": last_name,
                "full_name": f"{first_name} {last_name}",
                "email": self._generate_email(first_name, last_name),
                "department": department,
                "position": position,
                "salary": base_salary,
                "hire_date": hire_date,
                "birth_date": birth_date,
                "age": self._calculate_age(birth_date),
                "city": cities[i],
                "phone": self._generate_thai_phone(),
                "active": is_active,
                "performance_score": performance_score,
                "bonus_eligible": performance_score >= 3.5,
                "overtime_hours": random.randint(0, 50) if is_active else 0,
                "manager_id": (
                    self._generate_manager_id(i, position)
                    if include_relationships
                    else None
                ),
                "created_date": hire_date + timedelta(days=random.randint(-30, 0)),
                "updated_date": datetime.now() - timedelta(days=random.randint(0, 30)),
            }

            data.append(record)

        df = pd.DataFrame(data)
        logger.info(
            f"Generated employee data: {len(df)} records, {len(df.columns)} columns"
        )
        return df

    def generate_sales_data(
        self, num_rows: int = 5000, time_period_days: int = 365
    ) -> pd.DataFrame:
        """Generate realistic sales transaction data"""

        logger.info(f"Generating {num_rows:,} sales transactions...")

        data = []

        # Generate customer pool (realistic customer distribution)
        num_customers = min(num_rows // 3, 1000)  # Customers make multiple purchases
        customer_ids = [f"CUST{i+1:06d}" for i in range(num_customers)]

        # Product catalog
        products = self._generate_product_catalog()

        for i in range(num_rows):
            # Customer selection (some customers buy more frequently)
            customer_id = self._select_weighted_customer(customer_ids, i)

            # Product selection
            product = random.choice(products)

            # Transaction timing (realistic patterns)
            transaction_date = self._generate_transaction_date(time_period_days)

            # Quantity and pricing
            quantity = self._generate_realistic_quantity(product["category"])
            unit_price = product["base_price"] * random.uniform(
                0.9, 1.1
            )  # Price variation

            # Discounts (realistic discount patterns)
            discount_percent = self._calculate_discount(
                quantity, unit_price, transaction_date
            )

            # Calculate amounts
            total_amount = quantity * unit_price
            discount_amount = total_amount * (discount_percent / 100)
            final_amount = total_amount - discount_amount

            # Delivery and fulfillment
            delivery_date = transaction_date + timedelta(days=random.randint(1, 14))
            shipped = random.choices([True, False], weights=[85, 15])[0]

            record = {
                "transaction_id": f"TXN{i+1:010d}",
                "customer_id": customer_id,
                "product_id": product["id"],
                "product_name": product["name"],
                "category": product["category"],
                "quantity": quantity,
                "unit_price": round(unit_price, 2),
                "total_amount": round(total_amount, 2),
                "discount_percent": discount_percent,
                "discount_amount": round(discount_amount, 2),
                "final_amount": round(final_amount, 2),
                "payment_method": self._select_payment_method(),
                "sales_rep": f"EMP{random.randint(1, 100):06d}",
                "region": random.choice(["North", "South", "East", "West", "Central"]),
                "transaction_date": transaction_date,
                "delivery_date": delivery_date,
                "shipped": shipped,
                "customer_satisfaction": self._generate_satisfaction_score(),
                "return_flag": random.choices([True, False], weights=[3, 97])[0],
                "created_date": transaction_date,
                "updated_date": transaction_date
                + timedelta(days=random.randint(0, 10)),
            }

            data.append(record)

        df = pd.DataFrame(data)
        logger.info(
            f"Generated sales data: {len(df)} records, {len(df.columns)} columns"
        )
        return df

    def generate_inventory_data(self, num_rows: int = 2000) -> pd.DataFrame:
        """Generate realistic inventory data"""

        logger.info(f"Generating {num_rows:,} inventory items...")

        data = []
        suppliers = [f"SUPP{i+1:04d}" for i in range(50)]

        for i in range(num_rows):
            # Product info
            category = random.choice(self.patterns.PRODUCT_CATEGORIES)
            product_name = f"{random.choice(self.patterns.PRODUCT_NAMES)} {category[:3].upper()}-{i+1:04d}"

            # Stock levels (realistic distribution)
            reorder_level = random.randint(10, 100)
            current_stock = self._generate_realistic_stock_level(reorder_level)
            max_stock = reorder_level * random.randint(3, 8)

            # Pricing
            unit_cost = round(random.uniform(5.0, 500.0), 2)
            markup = random.uniform(1.2, 3.0)  # 20% to 200% markup
            selling_price = round(unit_cost * markup, 2)

            # Dates
            last_restock = datetime.now() - timedelta(days=random.randint(1, 90))
            expiry_date = datetime.now() + timedelta(days=random.randint(30, 730))

            # Quality and condition
            quality_status = random.choices(
                ["Excellent", "Good", "Fair", "Poor"], weights=[40, 35, 20, 5]
            )[0]

            damage_count = (
                0 if quality_status in ["Excellent", "Good"] else random.randint(1, 10)
            )

            record = {
                "sku": f"SKU{i+1:08d}",
                "product_name": product_name,
                "category": category,
                "current_stock": current_stock,
                "reorder_level": reorder_level,
                "max_stock": max_stock,
                "unit_cost": unit_cost,
                "selling_price": selling_price,
                "markup_percentage": round(
                    ((selling_price - unit_cost) / unit_cost) * 100, 1
                ),
                "supplier": random.choice(suppliers),
                "location": self._generate_warehouse_location(),
                "last_restock_date": last_restock,
                "expiry_date": expiry_date,
                "batch_number": f"BATCH{random.randint(100000, 999999)}",
                "quality_status": quality_status,
                "reserved_stock": min(random.randint(0, 50), current_stock),
                "damage_count": damage_count,
                "needs_reorder": current_stock <= reorder_level,
                "days_until_expiry": (expiry_date - datetime.now()).days,
                "turnover_rate": round(random.uniform(0.1, 5.0), 2),
                "created_date": datetime.now()
                - timedelta(days=random.randint(30, 365)),
                "updated_date": datetime.now() - timedelta(days=random.randint(0, 7)),
            }

            data.append(record)

        df = pd.DataFrame(data)
        logger.info(
            f"Generated inventory data: {len(df)} records, {len(df.columns)} columns"
        )
        return df

    def generate_financial_data(
        self, num_rows: int = 1000, time_period_days: int = 365
    ) -> pd.DataFrame:
        """Generate realistic financial transaction data"""

        logger.info(f"Generating {num_rows:,} financial transactions...")

        data = []

        for i in range(num_rows):
            # Transaction timing
            transaction_date = datetime.now() - timedelta(
                days=random.randint(0, time_period_days)
            )

            # Account and transaction type
            account_name = random.choice(self.patterns.ACCOUNT_TYPES)
            transaction_type = self._determine_transaction_type(account_name)

            # Amount based on transaction type and account
            amount = self._generate_financial_amount(account_name, transaction_type)

            # Description
            description = self._generate_transaction_description(
                account_name, transaction_type
            )

            # Tax calculations
            tax_rate = 0.07 if transaction_type in ["Revenue", "Sales"] else 0.0
            tax_amount = amount * tax_rate
            net_amount = amount + tax_amount

            # Approval workflow
            status = random.choices(
                ["Pending", "Approved", "Paid", "Cancelled"], weights=[10, 30, 55, 5]
            )[0]

            record = {
                "transaction_id": f"FIN{i+1:09d}",
                "account_number": f"ACC{random.randint(1000, 9999)}",
                "account_name": account_name,
                "transaction_type": transaction_type,
                "amount": round(amount, 2),
                "currency": "THB",
                "description": description,
                "reference_number": f"REF{random.randint(100000, 999999)}",
                "department": random.choice(self.patterns.DEPARTMENTS),
                "cost_center": f"CC{random.randint(100, 999)}",
                "approved_by": f"EMP{random.randint(1, 50):06d}",
                "transaction_date": transaction_date,
                "due_date": transaction_date + timedelta(days=random.randint(0, 90)),
                "status": status,
                "tax_rate": tax_rate,
                "tax_amount": round(tax_amount, 2),
                "net_amount": round(net_amount, 2),
                "fiscal_year": transaction_date.year,
                "fiscal_quarter": f"Q{((transaction_date.month - 1) // 3) + 1}",
                "created_date": transaction_date,
                "updated_date": transaction_date
                + timedelta(days=random.randint(0, 15)),
            }

            data.append(record)

        df = pd.DataFrame(data)
        logger.info(
            f"Generated financial data: {len(df)} records, {len(df.columns)} columns"
        )
        return df

    def generate_custom_data(
        self, num_rows: int = 1000, schema: Optional[List[Dict[str, Any]]] = None
    ) -> pd.DataFrame:
        """Generate custom data based on schema"""

        if not schema:
            schema = self._get_default_schema()

        logger.info(
            f"Generating {num_rows:,} custom records with {len(schema)} columns..."
        )

        data = []

        for i in range(num_rows):
            record = {}

            for col_spec in schema:
                col_name = col_spec["name"]
                col_type = col_spec["type"]
                col_options = col_spec.get("options", {})

                record[col_name] = self._generate_custom_field_value(
                    col_type, col_options, i
                )

            data.append(record)

        df = pd.DataFrame(data)
        logger.info(
            f"Generated custom data: {len(df)} records, {len(df.columns)} columns"
        )
        return df

    # Helper methods for realistic data generation

    def _generate_person_name(self) -> tuple:
        """Generate realistic person name based on locale"""
        if self.locale == "thai":
            first_name = random.choice(self.patterns.THAI_FIRST_NAMES)
            last_name = random.choice(self.patterns.THAI_LAST_NAMES)
        elif self.locale == "english":
            first_name = random.choice(self.patterns.ENGLISH_FIRST_NAMES)
            last_name = random.choice(self.patterns.ENGLISH_LAST_NAMES)
        else:  # mixed
            if random.choice([True, False]):
                first_name = random.choice(self.patterns.THAI_FIRST_NAMES)
                last_name = random.choice(self.patterns.THAI_LAST_NAMES)
            else:
                first_name = random.choice(self.patterns.ENGLISH_FIRST_NAMES)
                last_name = random.choice(self.patterns.ENGLISH_LAST_NAMES)

        return first_name, last_name

    def _generate_email(self, first_name: str, last_name: str) -> str:
        """Generate realistic email address"""
        # Romanize Thai names for email
        first_clean = self._romanize_name(first_name)
        last_clean = self._romanize_name(last_name)

        domains = ["denso888.com", "company.co.th", "business.com", "enterprise.net"]
        patterns = [
            f"{first_clean}.{last_clean}",
            f"{first_clean}{last_clean}",
            f"{first_clean[0]}{last_clean}",
            f"{first_clean}_{last_clean}",
        ]

        username = random.choice(patterns).lower()
        domain = random.choice(domains)

        return f"{username}@{domain}"

    def _romanize_name(self, name: str) -> str:
        """Simple romanization for Thai names"""
        thai_to_roman = {
            "สมชาย": "somchai",
            "สิริพร": "siriporn",
            "นิรันดร์": "niran",
            "วิภาดา": "wipada",
            "อาทิตย์": "athit",
            "กัญญา": "kanya",
            "ประชา": "pracha",
            "สุดา": "suda",
            "ใจดี": "jaidee",
            "ศิริโชติ": "sirichot",
            "วรรณกุล": "wannakul",
            "ธนกิจ": "thanakit",
        }

        return thai_to_roman.get(name, name)

    def _generate_thai_phone(self) -> str:
        """Generate realistic Thai phone number"""
        prefixes = ["08", "09", "06", "02"]
        prefix = random.choice(prefixes)

        if prefix == "02":  # Bangkok landline
            number = f"{prefix}{random.randint(100, 999)}{random.randint(1000, 9999)}"
        else:  # Mobile
            number = f"{prefix}{random.randint(1, 9)}{random.randint(1000000, 9999999)}"

        return number

    def _calculate_realistic_salary(self, position: str, department: str) -> int:
        """Calculate realistic salary based on position and department"""
        base_salaries = {
            "Manager": 80000,
            "Senior Manager": 120000,
            "Director": 200000,
            "Vice President": 300000,
            "Analyst": 45000,
            "Senior Analyst": 65000,
            "Specialist": 50000,
            "Senior Specialist": 70000,
            "Coordinator": 35000,
            "Team Lead": 75000,
            "Supervisor": 55000,
            "Executive": 85000,
            "Assistant": 30000,
            "Associate": 40000,
            "Officer": 42000,
            "Representative": 38000,
            "Consultant": 90000,
        }

        department_multipliers = {
            "IT": 1.2,
            "Engineering": 1.15,
            "Finance": 1.1,
            "Legal": 1.3,
            "Sales": 1.05,
            "HR": 0.95,
            "Marketing": 1.0,
            "Operations": 1.0,
        }

        base = base_salaries.get(position, 45000)
        multiplier = department_multipliers.get(department, 1.0)

        # Add some randomness
        salary = int(base * multiplier * random.uniform(0.8, 1.2))

        # Round to nearest 1000
        return round(salary / 1000) * 1000

    def _generate_hire_date(self) -> datetime:
        """Generate realistic hire date"""
        # Most hires in recent years, with some long-term employees
        weights = [0.3, 0.4, 0.2, 0.08, 0.02]  # 0-1, 1-3, 3-5, 5-10, 10+ years
        years_back = random.choices([1, 3, 5, 10, 15], weights=weights)[0]

        days_back = random.randint(30, years_back * 365)
        return datetime.now() - timedelta(days=days_back)

    def _generate_birth_date(self, hire_date: datetime) -> datetime:
        """Generate realistic birth date based on hire date"""
        # Minimum age 18, maximum 65 at hire
        min_age_at_hire = 18
        max_age_at_hire = 65

        age_at_hire = random.randint(min_age_at_hire, max_age_at_hire)
        birth_year = hire_date.year - age_at_hire

        return datetime(birth_year, random.randint(1, 12), random.randint(1, 28))

    def _calculate_age(self, birth_date: datetime) -> int:
        """Calculate current age"""
        today = datetime.now()
        return (
            today.year
            - birth_date.year
            - ((today.month, today.day) < (birth_date.month, birth_date.day))
        )

    def _generate_performance_score(self, position: str) -> float:
        """Generate realistic performance score"""
        # Senior positions tend to have higher scores
        if "Senior" in position or "Manager" in position or "Director" in position:
            mean_score = 3.8
        else:
            mean_score = 3.5

        # Normal distribution with realistic bounds
        score = random.gauss(mean_score, 0.6)
        return round(max(1.0, min(5.0, score)), 2)

    def _determine_employee_status(self, hire_date: datetime) -> bool:
        """Determine if employee is active based on hire date"""
        days_employed = (datetime.now() - hire_date).days

        # Higher chance of being inactive for very recent or very old hires
        if days_employed < 90:  # Very new employees
            return random.choices([True, False], weights=[95, 5])[0]
        elif days_employed > 3650:  # 10+ years
            return random.choices([True, False], weights=[85, 15])[0]
        else:
            return random.choices([True, False], weights=[92, 8])[0]

    def _generate_manager_id(self, employee_index: int, position: str) -> Optional[str]:
        """Generate manager ID for organizational hierarchy"""
        if "Manager" in position or "Director" in position or "VP" in position:
            return None  # Top level

        # Assign to a manager (earlier employee with manager title)
        manager_pool = max(
            1, employee_index // 10
        )  # Roughly 1 manager per 10 employees
        return f"EMP{random.randint(1, manager_pool):06d}"

    def _generate_product_catalog(self) -> List[Dict[str, Any]]:
        """Generate realistic product catalog"""
        products = []

        for i, category in enumerate(self.patterns.PRODUCT_CATEGORIES):
            num_products = random.randint(5, 15)

            for j in range(num_products):
                product = {
                    "id": f"PROD{(i * 100 + j + 1):06d}",
                    "name": f"{random.choice(self.patterns.PRODUCT_NAMES)} {category[:3].upper()}{j+1:02d}",
                    "category": category,
                    "base_price": self._generate_product_price(category),
                }
                products.append(product)

        return products

    def _generate_product_price(self, category: str) -> float:
        """Generate realistic product price by category"""
        price_ranges = {
            "Electronics": (100, 5000),
            "Automotive": (500, 15000),
            "Industrial Equipment": (1000, 50000),
            "Software & Technology": (50, 2000),
            "Office Supplies": (5, 500),
            "Health & Beauty": (10, 300),
            "Food & Beverage": (5, 100),
            "Clothing & Fashion": (20, 800),
            "Books & Media": (10, 150),
            "Sports & Recreation": (30, 2000),
            "Home & Garden": (25, 1500),
            "Toys & Games": (15, 400),
        }

        min_price, max_price = price_ranges.get(category, (10, 1000))
        return round(random.uniform(min_price, max_price), 2)

    def _select_weighted_customer(
        self, customer_ids: List[str], transaction_index: int
    ) -> str:
        """Select customer with realistic frequency distribution"""
        # 20% of customers make 80% of purchases
        if transaction_index % 5 == 0:  # Heavy buyers
            heavy_buyers = customer_ids[: len(customer_ids) // 5]
            return random.choice(heavy_buyers)
        else:  # Regular buyers
            return random.choice(customer_ids)

    def _generate_transaction_date(self, time_period_days: int) -> datetime:
        """Generate transaction date with realistic patterns"""
        # More transactions in recent months
        weights = [0.4, 0.3, 0.2, 0.1]  # Last 25%, 50%, 75%, 100% of period

        period_segment = random.choices([0.25, 0.5, 0.75, 1.0], weights=weights)[0]
        max_days_back = int(time_period_days * period_segment)

        days_back = random.randint(0, max_days_back)
        transaction_date = datetime.now() - timedelta(days=days_back)

        # Avoid weekends for B2B transactions
        if transaction_date.weekday() >= 5:  # Saturday or Sunday
            transaction_date = transaction_date - timedelta(
                days=transaction_date.weekday() - 4
            )

        return transaction_date

    def _generate_realistic_quantity(self, category: str) -> int:
        """Generate realistic quantity based on product category"""
        quantity_ranges = {
            "Office Supplies": (1, 100),
            "Electronics": (1, 10),
            "Automotive": (1, 5),
            "Industrial Equipment": (1, 3),
            "Food & Beverage": (1, 50),
            "Clothing & Fashion": (1, 20),
            "Books & Media": (1, 15),
            "Health & Beauty": (1, 25),
        }

        min_qty, max_qty = quantity_ranges.get(category, (1, 20))

        # Most orders are small quantities
        if random.random() < 0.7:
            return random.randint(min_qty, min(max_qty, min_qty + 5))
        else:
            return random.randint(min_qty, max_qty)

    def _calculate_discount(
        self, quantity: int, unit_price: float, transaction_date: datetime
    ) -> float:
        """Calculate realistic discount percentage"""
        discount = 0.0

        # Quantity discounts
        if quantity >= 50:
            discount += 15
        elif quantity >= 20:
            discount += 10
        elif quantity >= 10:
            discount += 5

        # High-value order discounts
        total_value = quantity * unit_price
        if total_value >= 10000:
            discount += 10
        elif total_value >= 5000:
            discount += 5

        # Seasonal discounts (end of quarter)
        if transaction_date.month in [3, 6, 9, 12] and transaction_date.day >= 25:
            discount += random.choice([5, 10, 15])

        # Random promotional discounts
        if random.random() < 0.1:  # 10% chance
            discount += random.choice([5, 10, 15, 20])

        return min(discount, 40)  # Maximum 40% discount

    def _select_payment_method(self) -> str:
        """Select realistic payment method"""
        methods = ["Credit Card", "Bank Transfer", "Cash", "Check", "Online Payment"]
        weights = [40, 30, 15, 10, 5]  # Percentages

        return random.choices(methods, weights=weights)[0]

    def _generate_satisfaction_score(self) -> int:
        """Generate customer satisfaction score (1-5)"""
        # Skewed toward higher satisfaction
        scores = [1, 2, 3, 4, 5]
        weights = [5, 10, 20, 35, 30]

        return random.choices(scores, weights=weights)[0]

    def _generate_realistic_stock_level(self, reorder_level: int) -> int:
        """Generate realistic current stock level"""
        # Stock levels follow patterns
        patterns = [
            ("well_stocked", 0.4, lambda rl: random.randint(rl * 2, rl * 5)),
            ("normal", 0.3, lambda rl: random.randint(rl, rl * 2)),
            ("low", 0.2, lambda rl: random.randint(rl // 2, rl)),
            ("critical", 0.1, lambda rl: random.randint(0, rl // 2)),
        ]

        pattern_names, weights, generators = zip(*patterns)
        selected_pattern = random.choices(range(len(patterns)), weights=weights)[0]

        return generators[selected_pattern](reorder_level)

    def _generate_warehouse_location(self) -> str:
        """Generate warehouse location code"""
        warehouses = ["WH01", "WH02", "WH03", "WH04", "WH05"]
        zones = ["A", "B", "C", "D"]

        warehouse = random.choice(warehouses)
        zone = random.choice(zones)
        aisle = random.randint(1, 20)
        shelf = random.randint(1, 50)

        return f"{warehouse}-{zone}{aisle:02d}-{shelf:02d}"

    def _determine_transaction_type(self, account_name: str) -> str:
        """Determine transaction type based on account"""
        account_types = {
            "Cash": ["Debit", "Credit"],
            "Bank": ["Debit", "Credit"],
            "Accounts Receivable": ["Debit"],
            "Accounts Payable": ["Credit"],
            "Revenue": ["Credit"],
            "Cost of Goods Sold": ["Debit"],
            "Operating Expenses": ["Debit"],
            "Assets": ["Debit"],
            "Liabilities": ["Credit"],
            "Equity": ["Credit"],
        }

        # Find matching account type
        for acc_type, trans_types in account_types.items():
            if acc_type in account_name:
                return random.choice(trans_types)

        return random.choice(["Debit", "Credit"])

    def _generate_financial_amount(
        self, account_name: str, transaction_type: str
    ) -> float:
        """Generate realistic financial amount"""
        amount_ranges = {
            "Cash": (100, 50000),
            "Bank": (1000, 500000),
            "Revenue": (1000, 1000000),
            "Operating Expenses": (500, 100000),
            "Assets": (10000, 5000000),
            "Payroll": (20000, 500000),
            "Utilities": (5000, 50000),
            "Office Supplies": (100, 10000),
        }

        # Find range based on account name
        for acc_type, (min_amt, max_amt) in amount_ranges.items():
            if acc_type in account_name:
                return round(random.uniform(min_amt, max_amt), 2)

        return round(random.uniform(100, 50000), 2)

    def _generate_transaction_description(
        self, account_name: str, transaction_type: str
    ) -> str:
        """Generate realistic transaction description"""
        descriptions = {
            "Revenue": [
                "Sales Revenue",
                "Service Income",
                "Product Sales",
                "Consulting Fees",
            ],
            "Operating Expenses": [
                "Office Rent",
                "Utilities",
                "Software License",
                "Marketing Campaign",
            ],
            "Payroll": [
                "Monthly Salary",
                "Overtime Payment",
                "Bonus Payment",
                "Commission",
            ],
            "Office Supplies": [
                "Stationery Purchase",
                "Printer Supplies",
                "Office Equipment",
            ],
            "Travel": [
                "Business Trip",
                "Client Meeting",
                "Conference Attendance",
                "Training Travel",
            ],
            "Marketing": [
                "Digital Advertising",
                "Print Materials",
                "Event Sponsorship",
                "Website Development",
            ],
        }

        for desc_type, desc_list in descriptions.items():
            if desc_type in account_name or desc_type in account_name:
                return random.choice(desc_list)

        return f"{transaction_type} Transaction"

    def _get_default_schema(self) -> List[Dict[str, Any]]:
        """Default schema for custom data generation"""
        return [
            {"name": "id", "type": "sequence", "options": {"start": 1}},
            {"name": "name", "type": "person_name"},
            {"name": "email", "type": "email"},
            {
                "name": "amount",
                "type": "currency",
                "options": {"min": 100, "max": 10000},
            },
            {"name": "date", "type": "date", "options": {"days_back": 365}},
            {"name": "active", "type": "boolean"},
            {
                "name": "category",
                "type": "choice",
                "options": {"choices": ["A", "B", "C", "D"]},
            },
        ]

    def _generate_custom_field_value(
        self, field_type: str, options: Dict[str, Any], index: int
    ) -> Any:
        """Generate value for custom field based on type"""
        if field_type == "sequence":
            start = options.get("start", 1)
            return start + index

        elif field_type == "person_name":
            first, last = self._generate_person_name()
            return f"{first} {last}"

        elif field_type == "email":
            domain = options.get("domain", "company.com")
            return f"user{index+1:04d}@{domain}"

        elif field_type == "currency":
            min_val = options.get("min", 100)
            max_val = options.get("max", 10000)
            return round(random.uniform(min_val, max_val), 2)

        elif field_type == "date":
            days_back = options.get("days_back", 365)
            return datetime.now() - timedelta(days=random.randint(0, days_back))

        elif field_type == "boolean":
            probability = options.get("true_probability", 0.5)
            return random.random() < probability

        elif field_type == "choice":
            choices = options.get("choices", ["Option A", "Option B"])
            return random.choice(choices)

        elif field_type == "integer":
            min_val = options.get("min", 1)
            max_val = options.get("max", 1000)
            return random.randint(min_val, max_val)

        elif field_type == "text":
            length = options.get("length", 50)
            return f"Sample text {index+1}"[:length]

        else:
            return f"Value {index+1}"


class MockDataTemplates:
    """Enhanced pre-defined mock data templates with metadata"""

    @staticmethod
    def get_template_list() -> List[Dict[str, Any]]:
        """Get comprehensive list of available templates"""
        return [
            {
                "name": "employees",
                "description": "Employee records with HR information and hierarchy",
                "default_rows": 1000,
                "estimated_columns": 18,
                "generator": MockDataGenerator().generate_employee_data,
                "features": [
                    "Realistic salaries",
                    "Department hierarchy",
                    "Performance scores",
                ],
                "use_cases": [
                    "HR Analytics",
                    "Payroll Processing",
                    "Organizational Charts",
                ],
            },
            {
                "name": "sales",
                "description": "Sales transactions with customer and product data",
                "default_rows": 5000,
                "estimated_columns": 20,
                "generator": MockDataGenerator().generate_sales_data,
                "features": ["Customer patterns", "Seasonal trends", "Discount logic"],
                "use_cases": [
                    "Sales Analytics",
                    "Customer Segmentation",
                    "Revenue Forecasting",
                ],
            },
            {
                "name": "inventory",
                "description": "Product inventory with stock levels and locations",
                "default_rows": 2000,
                "estimated_columns": 22,
                "generator": MockDataGenerator().generate_inventory_data,
                "features": ["Stock patterns", "Warehouse locations", "Reorder alerts"],
                "use_cases": [
                    "Inventory Management",
                    "Supply Chain",
                    "Procurement Planning",
                ],
            },
            {
                "name": "financial",
                "description": "Financial transactions and accounting records",
                "default_rows": 1000,
                "estimated_columns": 19,
                "generator": MockDataGenerator().generate_financial_data,
                "features": [
                    "Chart of accounts",
                    "Tax calculations",
                    "Approval workflow",
                ],
                "use_cases": ["Financial Reporting", "Budget Analysis", "Audit Trails"],
            },
            {
                "name": "custom",
                "description": "Customizable data structure with flexible schema",
                "default_rows": 1000,
                "estimated_columns": 7,
                "generator": MockDataGenerator().generate_custom_data,
                "features": [
                    "Flexible schema",
                    "Custom field types",
                    "Configurable patterns",
                ],
                "use_cases": ["Testing", "Prototyping", "Custom Applications"],
            },
        ]

    @staticmethod
    def generate_by_template(
        template_name: str, num_rows: int, **kwargs
    ) -> pd.DataFrame:
        """Generate data using specified template with options"""
        generator = MockDataGenerator(**kwargs)

        generators = {
            "employees": generator.generate_employee_data,
            "sales": generator.generate_sales_data,
            "inventory": generator.generate_inventory_data,
            "financial": generator.generate_financial_data,
            "custom": generator.generate_custom_data,
        }

        if template_name not in generators:
            raise ValueError(
                f"Unknown template: {template_name}. Available: {list(generators.keys())}"
            )

        return generators[template_name](num_rows)

    @staticmethod
    def get_template_info(template_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific template"""
        templates = {t["name"]: t for t in MockDataTemplates.get_template_list()}

        if template_name not in templates:
            raise ValueError(f"Unknown template: {template_name}")

        return templates[template_name]
        """Get template information with metadata"""
        templates = MockDataTemplates.get_template_list()
        for template in templates:
            if template["name"] == template_name:
                return {
                    "name": template["name"],
                    "description": template["description"],
                    "default_rows": template["default_rows"],
                    "estimated_columns": template["estimated_columns"],
                    "features": template["features"],
                    "use_cases": template["use_cases"],
                }
