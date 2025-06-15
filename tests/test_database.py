"""
tests/test_database.py
Database Component Tests
"""

import unittest
import sys
import os
import os
from core.mock_data_generator import MockDataGenerator

# === FIX 5: Fix tests/test_excel_handler.py imports ===
# Update imports section in tests/test_excel_handler.py:


# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestDatabaseManager(unittest.TestCase):
    """Test database manager functionality"""

    def setUp(self):
        """Setup test environment"""
        self.generator = MockDataGenerator()

    def test_generate_employees(self):
        """Test employee data generation"""
        employees = self.generator.generate_employees(10)

        self.assertEqual(len(employees), 10)

        # Check required fields
        for emp in employees:
            self.assertIn("employee_id", emp)
            self.assertIn("first_name", emp)
            self.assertIn("last_name", emp)
            self.assertIn("email", emp)
            self.assertIn("department", emp)
            self.assertIn("position", emp)
            self.assertIn("salary", emp)
            self.assertIn("hire_date", emp)

            # Validate data types
            self.assertIsInstance(emp["salary"], int)
            self.assertTrue(emp["salary"] > 0)
            self.assertIn("@", emp["email"])

    def test_generate_sales(self):
        """Test sales data generation"""
        sales = self.generator.generate_sales(5)

        self.assertEqual(len(sales), 5)

        # Check required fields
        for sale in sales:
            self.assertIn("transaction_id", sale)
            self.assertIn("customer_name", sale)
            self.assertIn("product_name", sale)
            self.assertIn("quantity", sale)
            self.assertIn("unit_price", sale)
            self.assertIn("total_amount", sale)
            self.assertIn("transaction_date", sale)

            # Validate calculations
            expected_total = sale["quantity"] * sale["unit_price"]
            self.assertAlmostEqual(sale["total_amount"], expected_total, places=2)

    def test_generate_inventory(self):
        """Test inventory data generation"""
        inventory = self.generator.generate_inventory(8)

        self.assertEqual(len(inventory), 8)

        # Check required fields
        for item in inventory:
            self.assertIn("product_id", item)
            self.assertIn("product_name", item)
            self.assertIn("category", item)
            self.assertIn("current_stock", item)
            self.assertIn("max_stock", item)
            self.assertIn("unit_price", item)
            self.assertIn("supplier", item)

            # Validate stock logic
            self.assertLessEqual(item["current_stock"], item["max_stock"])
            self.assertGreaterEqual(item["current_stock"], 0)

    def test_generate_financial(self):
        """Test financial data generation"""
        financial = self.generator.generate_financial(6)

        self.assertEqual(len(financial), 6)

        # Check required fields
        for record in financial:
            self.assertIn("transaction_id", record)
            self.assertIn("account_name", record)
            self.assertIn("account_type", record)
            self.assertIn("amount", record)
            self.assertIn("transaction_date", record)
            self.assertIn("currency", record)

            # Validate amount
            self.assertGreater(record["amount"], 0)

    def test_get_available_templates(self):
        """Test getting available templates"""
        templates = self.generator.get_available_templates()

        self.assertIsInstance(templates, list)
        self.assertGreater(len(templates), 0)

        # Check template structure
        for template in templates:
            self.assertIn("name", template)
            self.assertIn("title", template)
            self.assertIn("description", template)
            self.assertIn("fields", template)
            self.assertIn("color", template)

    def test_generation_statistics(self):
        """Test generation statistics tracking"""
        # Generate some data
        self.generator.generate_employees(100)
        self.generator.generate_sales(50)

        stats = self.generator.get_generation_statistics()

        self.assertIn("total_operations", stats)
        self.assertIn("total_records", stats)
        self.assertIn("templates_used", stats)

        self.assertEqual(stats["total_operations"], 2)
        self.assertEqual(stats["total_records"], 150)
        self.assertIn("employees", stats["templates_used"])
        self.assertIn("sales", stats["templates_used"])

    def test_custom_data_generation(self):
        """Test custom data template generation"""
        custom_template = {
            "id": {"type": "integer", "min": 1, "max": 1000},
            "name": {"type": "string", "pattern": "name"},
            "price": {"type": "float", "min": 10.0, "max": 100.0, "decimals": 2},
            "active": {"type": "boolean", "true_probability": 0.7},
            "category": {"type": "choice", "choices": ["A", "B", "C"]},
        }

        data = self.generator.generate_custom_data(custom_template, 5)

        self.assertEqual(len(data), 5)

        # Check custom fields
        for record in data:
            self.assertIn("id", record)
            self.assertIn("name", record)
            self.assertIn("price", record)
            self.assertIn("active", record)
            self.assertIn("category", record)

            # Validate types
            self.assertIsInstance(record["id"], int)
            self.assertIsInstance(record["price"], float)
            self.assertIsInstance(record["active"], bool)
            self.assertIn(record["category"], ["A", "B", "C"])


if __name__ == "__main__":
    unittest.main()
