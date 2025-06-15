"""
tests/test_excel_handler.py
Excel Handler Component Tests
"""

import unittest
import tempfile
import pandas as pd
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.excel_handler import ExcelHandler, TypeDetector, DataCleaner


class TestExcelHandler(unittest.TestCase):
    """Test Excel handler functionality"""

    def setUp(self):
        """Setup test environment"""
        self.handler = ExcelHandler()

        # Create test Excel file
        self.test_data = pd.DataFrame(
            {
                "ID": [1, 2, 3],
                "Name": ["John Doe", "Jane Smith", "Bob Johnson"],
                "Email": ["john@example.com", "jane@example.com", "bob@example.com"],
                "Age": [30, 25, 35],
                "Salary": [50000.0, 60000.0, 55000.0],
                "Active": [True, False, True],
                "Join Date": pd.to_datetime(["2023-01-15", "2023-02-20", "2023-03-10"]),
            }
        )

        self.temp_file = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
        self.temp_file.close()

        # Write test data to Excel
        self.test_data.to_excel(self.temp_file.name, index=False)

    def tearDown(self):
        """Cleanup test environment"""
        try:
            os.unlink(self.temp_file.name)
        except:
            pass

    def test_load_file(self):
        """Test Excel file loading"""
        result = self.handler.load_file(self.temp_file.name)

        self.assertNotIn("error", result)
        self.assertIn("file_name", result)
        self.assertIn("total_rows", result)
        self.assertIn("total_columns", result)
        self.assertEqual(result["total_rows"], 3)
        self.assertEqual(result["total_columns"], 7)

    def test_validate_file(self):
        """Test file validation"""
        result = self.handler.validate_file(self.temp_file.name)

        self.assertTrue(result["valid"])
        self.assertEqual(len(result["errors"]), 0)

    def test_invalid_file(self):
        """Test invalid file handling"""
        result = self.handler.validate_file("nonexistent.xlsx")

        self.assertFalse(result["valid"])
        self.assertGreater(len(result["errors"]), 0)

    def test_get_sheets(self):
        """Test getting sheet names"""
        sheets = self.handler.get_sheets(self.temp_file.name)

        self.assertIsInstance(sheets, list)
        self.assertGreater(len(sheets), 0)

    def test_preview_data(self):
        """Test data preview"""
        self.handler.load_file(self.temp_file.name)
        preview = self.handler.preview_data(2)

        self.assertIsNotNone(preview)
        self.assertEqual(len(preview), 2)

    def test_process_file_chunks(self):
        """Test file processing in chunks"""
        self.handler.load_file(self.temp_file.name)

        chunks = list(self.handler.process_file(chunk_size=2))

        self.assertGreater(len(chunks), 0)

        # Check first chunk
        first_chunk = chunks[0]
        self.assertIn("dataframe", first_chunk)
        self.assertIn("rows_count", first_chunk)


class TestTypeDetector(unittest.TestCase):
    """Test data type detection"""

    def test_detect_types_from_names(self):
        """Test type detection from column names"""
        columns = ["id", "email", "age", "price", "date", "active"]
        types = TypeDetector.detect_types(columns)

        self.assertEqual(types["id"], "integer")
        self.assertEqual(types["email"], "email")
        self.assertEqual(types["age"], "integer")
        self.assertEqual(types["price"], "float")
        self.assertEqual(types["active"], "boolean")

    def test_detect_types_with_data(self):
        """Test type detection with sample data"""
        df = pd.DataFrame(
            {
                "numbers": [1, 2, 3],
                "decimals": [1.1, 2.2, 3.3],
                "dates": ["2023-01-01", "2023-01-02", "2023-01-03"],
                "booleans": ["true", "false", "true"],
                "emails": ["test@example.com", "user@test.com", "admin@site.org"],
            }
        )

        columns = list(df.columns)
        types = TypeDetector.detect_types(columns, df)

        self.assertEqual(types["numbers"], "integer")
        self.assertEqual(types["decimals"], "float")
        self.assertEqual(types["booleans"], "boolean")
        self.assertEqual(types["emails"], "email")


class TestDataCleaner(unittest.TestCase):
    """Test data cleaning functionality"""

    def setUp(self):
        """Setup test environment"""
        self.cleaner = DataCleaner()

    def test_clean_column_names(self):
        """Test column name cleaning"""
        test_cases = [
            ("Name", "name"),
            ("First Name", "first_name"),
            ("Email@Address", "email_address"),
            ("ID#", "id"),
            ("   Spaced   ", "spaced"),
            ("UPPER", "upper"),
            ("mixed_Case", "mixed_case"),
        ]

        for original, expected in test_cases:
            cleaned = self.cleaner.clean_column_name(original)
            self.assertEqual(cleaned, expected)

    def test_clean_dataframe(self):
        """Test dataframe cleaning"""
        # Create messy test data
        df = pd.DataFrame(
            {
                "Name ": ["  John  ", "  Jane  ", None],
                "Email@": ["john@test.com", "", "invalid"],
                "Age#": [30, None, 25],
                "  ID  ": [1, 2, 3],
            }
        )

        cleaned_df = self.cleaner.clean_dataframe(df)

        # Check column names are cleaned
        expected_columns = ["name", "email", "age", "id"]
        self.assertEqual(list(cleaned_df.columns), expected_columns)

        # Check data is cleaned (strings are stripped)
        self.assertEqual(cleaned_df.iloc[0]["name"], "John")
        self.assertEqual(cleaned_df.iloc[1]["name"], "Jane")

    def test_convert_types(self):
        """Test type conversion"""
        df = pd.DataFrame(
            {
                "integers": ["1", "2", "3"],
                "floats": ["1.1", "2.2", "3.3"],
                "booleans": ["true", "false", "yes"],
                "dates": ["2023-01-01", "2023-01-02", "2023-01-03"],
            }
        )

        type_mapping = {
            "integers": "integer",
            "floats": "float",
            "booleans": "boolean",
            "dates": "datetime",
        }

        converted_df = self.cleaner.convert_types(df, type_mapping)

        # Check data types (basic validation)
        self.assertIsNotNone(converted_df)
        self.assertEqual(len(converted_df), 3)


if __name__ == "__main__":
    unittest.main()
