from typing import Dict, List, Any
from datetime import datetime
from core.mock_data_generator import MockDataGenerator


class MockDataService:
    """Service for generating mock data"""

    def __init__(self):
        self.generator = MockDataGenerator()
        self.current_template = None
        self.generation_stats = {"total_generated": 0, "last_generation": None}

    def generate_mock_data(self, template_type: str, count: int) -> Dict[str, Any]:
        """Generate mock data based on template"""
        try:
            if template_type == "employees":
                data = self.generator.generate_employees(count)
            elif template_type == "sales":
                data = self.generator.generate_sales(count)
            elif template_type == "inventory":
                data = self.generator.generate_inventory(count)
            else:
                raise ValueError(f"Unknown template type: {template_type}")

            self.generation_stats["total_generated"] += len(data)
            self.generation_stats["last_generation"] = datetime.now()

            return {
                "success": True,
                "data": data,
                "count": len(data),
                "template": template_type,
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_available_templates(self) -> List[Dict[str, Any]]:
        """Get available mock data templates"""
        return [
            {
                "id": "employees",
                "name": "Employee Records",
                "description": "Generate realistic employee data",
                "fields": [
                    "employee_id",
                    "first_name",
                    "last_name",
                    "email",
                    "department",
                ],
            },
            {
                "id": "sales",
                "name": "Sales Transactions",
                "description": "Generate sales transaction records",
                "fields": ["transaction_id", "customer_name", "product", "amount"],
            },
            {
                "id": "inventory",
                "name": "Inventory Items",
                "description": "Generate inventory and stock data",
                "fields": ["product_id", "name", "category", "quantity"],
            },
        ]
