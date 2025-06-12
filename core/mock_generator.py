import pandas as pd
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import uuid


class MockDataGenerator:
    """Generate realistic mock data for testing"""

    # Sample data sets
    FIRST_NAMES = [
        "Somchai",
        "Siriporn",
        "Niran",
        "Wipada",
        "Arthit",
        "Kannika",
        "Preecha",
        "Suda",
        "Thawat",
        "Malee",
        "Bundit",
        "Pensri",
        "Chaiwat",
        "Siripan",
        "Manop",
        "Wandee",
        "John",
        "Mary",
        "David",
        "Sarah",
        "Michael",
        "Emma",
        "James",
        "Lisa",
    ]

    LAST_NAMES = [
        "Jaidee",
        "Sirichote",
        "Wannakul",
        "Thanakit",
        "Srisawat",
        "Phrommin",
        "Charoensuk",
        "Wongthong",
        "Kantapon",
        "Siriwat",
        "Smith",
        "Johnson",
        "Brown",
        "Wilson",
        "Davis",
    ]

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
    ]

    POSITIONS = [
        "Manager",
        "Analyst",
        "Specialist",
        "Coordinator",
        "Director",
        "Senior Analyst",
        "Team Lead",
        "Assistant Manager",
        "Executive",
        "Supervisor",
        "Officer",
        "Associate",
    ]

    CITIES = [
        "Bangkok",
        "Chiang Mai",
        "Phuket",
        "Pattaya",
        "Khon Kaen",
        "Udon Thani",
        "Hat Yai",
        "Rayong",
        "Chonburi",
        "Nonthaburi",
        "Samut Prakan",
        "Pathum Thani",
    ]

    PRODUCT_CATEGORIES = [
        "Electronics",
        "Automotive",
        "Home & Garden",
        "Sports",
        "Books",
        "Clothing",
        "Food & Beverage",
        "Health & Beauty",
        "Toys",
        "Office Supplies",
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
    ]

    @staticmethod
    def generate_employee_data(num_rows: int = 1000) -> pd.DataFrame:
        """Generate employee mock data"""
        data = []

        for i in range(num_rows):
            first_name = random.choice(MockDataGenerator.FIRST_NAMES)
            last_name = random.choice(MockDataGenerator.LAST_NAMES)

            data.append(
                {
                    "employee_id": f"EMP{i+1:05d}",
                    "first_name": first_name,
                    "last_name": last_name,
                    "full_name": f"{first_name} {last_name}",
                    "email": f"{first_name.lower()}.{last_name.lower()}@denso888.com",
                    "department": random.choice(MockDataGenerator.DEPARTMENTS),
                    "position": random.choice(MockDataGenerator.POSITIONS),
                    "salary": random.randint(25000, 120000),
                    "hire_date": datetime.now()
                    - timedelta(days=random.randint(30, 3650)),
                    "birth_date": datetime.now()
                    - timedelta(days=random.randint(7300, 18250)),  # 20-50 years old
                    "age": random.randint(22, 65),
                    "city": random.choice(MockDataGenerator.CITIES),
                    "phone": f"0{random.randint(8, 9)}{random.randint(10000000, 99999999)}",
                    "active": random.choices([True, False], weights=[85, 15])[
                        0
                    ],  # 85% active
                    "performance_score": round(random.uniform(1.0, 5.0), 2),
                    "bonus_eligible": random.choice([True, False]),
                    "overtime_hours": random.randint(0, 50),
                    "created_date": datetime.now()
                    - timedelta(days=random.randint(1, 30)),
                    "updated_date": datetime.now()
                    - timedelta(days=random.randint(0, 7)),
                }
            )

        return pd.DataFrame(data)

    @staticmethod
    def generate_sales_data(num_rows: int = 5000) -> pd.DataFrame:
        """Generate sales transaction mock data"""
        data = []

        for i in range(num_rows):
            transaction_date = datetime.now() - timedelta(days=random.randint(0, 365))

            data.append(
                {
                    "transaction_id": f"TXN{i+1:08d}",
                    "customer_id": f"CUST{random.randint(1, 1000):05d}",
                    "product_id": f"PROD{random.randint(1, 500):04d}",
                    "product_name": random.choice(MockDataGenerator.PRODUCT_NAMES),
                    "category": random.choice(MockDataGenerator.PRODUCT_CATEGORIES),
                    "quantity": random.randint(1, 100),
                    "unit_price": round(random.uniform(10.0, 1000.0), 2),
                    "total_amount": 0,  # Will be calculated
                    "discount_percent": random.choices(
                        [0, 5, 10, 15, 20], weights=[60, 20, 10, 7, 3]
                    )[0],
                    "discount_amount": 0,  # Will be calculated
                    "final_amount": 0,  # Will be calculated
                    "payment_method": random.choice(
                        ["Cash", "Credit Card", "Bank Transfer", "Check"]
                    ),
                    "sales_rep": f"EMP{random.randint(1, 100):05d}",
                    "region": random.choice(
                        ["North", "South", "East", "West", "Central"]
                    ),
                    "transaction_date": transaction_date,
                    "delivery_date": transaction_date
                    + timedelta(days=random.randint(1, 14)),
                    "shipped": random.choice([True, False]),
                    "customer_satisfaction": random.randint(1, 5),
                    "return_flag": random.choices([True, False], weights=[5, 95])[
                        0
                    ],  # 5% returns
                    "created_date": transaction_date,
                    "updated_date": transaction_date
                    + timedelta(days=random.randint(0, 30)),
                }
            )

        # Calculate derived fields
        for record in data:
            record["total_amount"] = record["quantity"] * record["unit_price"]
            record["discount_amount"] = record["total_amount"] * (
                record["discount_percent"] / 100
            )
            record["final_amount"] = record["total_amount"] - record["discount_amount"]

        return pd.DataFrame(data)

    @staticmethod
    def generate_inventory_data(num_rows: int = 2000) -> pd.DataFrame:
        """Generate inventory mock data"""
        data = []

        for i in range(num_rows):
            reorder_level = random.randint(10, 100)
            current_stock = random.randint(0, 500)

            data.append(
                {
                    "sku": f"SKU{i+1:06d}",
                    "product_name": random.choice(MockDataGenerator.PRODUCT_NAMES),
                    "category": random.choice(MockDataGenerator.PRODUCT_CATEGORIES),
                    "current_stock": current_stock,
                    "reorder_level": reorder_level,
                    "max_stock": reorder_level * 5,
                    "unit_cost": round(random.uniform(5.0, 500.0), 2),
                    "selling_price": round(random.uniform(10.0, 1000.0), 2),
                    "supplier": f"SUPP{random.randint(1, 50):03d}",
                    "location": f"WH{random.randint(1, 10):02d}-{random.choice(['A', 'B', 'C'])}{random.randint(1, 99):02d}",
                    "last_restock_date": datetime.now()
                    - timedelta(days=random.randint(1, 90)),
                    "expiry_date": datetime.now()
                    + timedelta(days=random.randint(30, 730)),
                    "batch_number": f"BATCH{random.randint(100000, 999999)}",
                    "quality_status": random.choice(["Good", "Fair", "Excellent"]),
                    "reserved_stock": random.randint(0, min(current_stock, 50)),
                    "damage_count": random.randint(0, 10),
                    "needs_reorder": current_stock <= reorder_level,
                    "created_date": datetime.now()
                    - timedelta(days=random.randint(30, 365)),
                    "updated_date": datetime.now()
                    - timedelta(days=random.randint(0, 7)),
                }
            )

        return pd.DataFrame(data)

    @staticmethod
    def generate_financial_data(num_rows: int = 1000) -> pd.DataFrame:
        """Generate financial transaction mock data"""
        data = []

        for i in range(num_rows):
            transaction_date = datetime.now() - timedelta(days=random.randint(0, 365))

            data.append(
                {
                    "transaction_id": f"FIN{i+1:07d}",
                    "account_number": f"ACC{random.randint(1000, 9999)}",
                    "account_name": random.choice(
                        [
                            "Cash",
                            "Bank - SCB",
                            "Bank - BBL",
                            "Accounts Receivable",
                            "Accounts Payable",
                            "Revenue",
                            "Expenses",
                            "Assets",
                        ]
                    ),
                    "transaction_type": random.choice(["Debit", "Credit"]),
                    "amount": round(random.uniform(100.0, 100000.0), 2),
                    "currency": "THB",
                    "description": random.choice(
                        [
                            "Sales Revenue",
                            "Office Supplies",
                            "Salary Payment",
                            "Utility Bills",
                            "Equipment Purchase",
                            "Marketing Expense",
                            "Travel Expense",
                            "Maintenance",
                        ]
                    ),
                    "reference_number": f"REF{random.randint(100000, 999999)}",
                    "department": random.choice(MockDataGenerator.DEPARTMENTS),
                    "cost_center": f"CC{random.randint(100, 999)}",
                    "approved_by": f"EMP{random.randint(1, 50):05d}",
                    "transaction_date": transaction_date,
                    "due_date": transaction_date
                    + timedelta(days=random.randint(0, 90)),
                    "status": random.choice(
                        ["Pending", "Approved", "Paid", "Cancelled"]
                    ),
                    "tax_amount": 0,  # Will be calculated
                    "net_amount": 0,  # Will be calculated
                    "created_date": transaction_date,
                    "updated_date": transaction_date
                    + timedelta(days=random.randint(0, 15)),
                }
            )

        # Calculate tax and net amounts
        for record in data:
            record["tax_amount"] = record["amount"] * 0.07  # 7% VAT
            record["net_amount"] = record["amount"] + record["tax_amount"]

        return pd.DataFrame(data)

    @staticmethod
    def generate_custom_data(
        num_rows: int = 1000, columns: Optional[List[Dict[str, Any]]] = None
    ) -> pd.DataFrame:
        """Generate custom mock data based on column specifications"""

        if not columns:
            # Default simple structure
            columns = [
                {"name": "id", "type": "sequence"},
                {"name": "name", "type": "person_name"},
                {"name": "email", "type": "email"},
                {"name": "amount", "type": "currency"},
                {"name": "date", "type": "date"},
                {"name": "active", "type": "boolean"},
            ]

        data = []

        for i in range(num_rows):
            record = {}

            for col in columns:
                col_name = col["name"]
                col_type = col["type"]

                if col_type == "sequence":
                    record[col_name] = i + 1
                elif col_type == "person_name":
                    record[col_name] = (
                        f"{random.choice(MockDataGenerator.FIRST_NAMES)} {random.choice(MockDataGenerator.LAST_NAMES)}"
                    )
                elif col_type == "email":
                    record[col_name] = f"user{i+1:04d}@denso888.com"
                elif col_type == "currency":
                    record[col_name] = round(random.uniform(100.0, 10000.0), 2)
                elif col_type == "date":
                    record[col_name] = datetime.now() - timedelta(
                        days=random.randint(0, 365)
                    )
                elif col_type == "boolean":
                    record[col_name] = random.choice([True, False])
                elif col_type == "integer":
                    record[col_name] = random.randint(1, 1000)
                elif col_type == "text":
                    record[col_name] = f"Sample text {random.randint(1, 1000)}"
                else:
                    record[col_name] = f"Value {i+1}"

            data.append(record)

        return pd.DataFrame(data)


class MockDataTemplates:
    """Pre-defined mock data templates"""

    @staticmethod
    def get_template_list() -> List[Dict[str, Any]]:
        """Get list of available templates"""
        return [
            {
                "name": "employees",
                "description": "Employee records with HR information",
                "default_rows": 1000,
                "generator": MockDataGenerator.generate_employee_data,
            },
            {
                "name": "sales",
                "description": "Sales transactions and customer data",
                "default_rows": 5000,
                "generator": MockDataGenerator.generate_sales_data,
            },
            {
                "name": "inventory",
                "description": "Product inventory and stock levels",
                "default_rows": 2000,
                "generator": MockDataGenerator.generate_inventory_data,
            },
            {
                "name": "financial",
                "description": "Financial transactions and accounting",
                "default_rows": 1000,
                "generator": MockDataGenerator.generate_financial_data,
            },
            {
                "name": "custom",
                "description": "Customizable data structure",
                "default_rows": 1000,
                "generator": MockDataGenerator.generate_custom_data,
            },
        ]

    @staticmethod
    def generate_by_template(template_name: str, num_rows: int) -> pd.DataFrame:
        """Generate data using template"""
        templates = {
            t["name"]: t["generator"] for t in MockDataTemplates.get_template_list()
        }

        if template_name not in templates:
            raise ValueError(f"Unknown template: {template_name}")

        return templates[template_name](num_rows)
