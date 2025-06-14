"""
tests/unit/test_basic.py
Basic tests for DENSO888 components
"""

import unittest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config.settings import get_config
from core.mock_generator import MockDataTemplates
from utils.logger import setup_logger


class TestBasicFunctionality(unittest.TestCase):
    """Test basic functionality"""
    
    def test_config_loading(self):
        """Test configuration loading"""
        config = get_config()
        self.assertEqual(config.app_name, "DENSO888")
        self.assertEqual(config.version, "2.0.0")
    
    def test_logger_setup(self):
        """Test logger setup"""
        logger = setup_logger("test")
        self.assertIsNotNone(logger)
    
    def test_mock_templates(self):
        """Test mock data templates"""
        templates = MockDataTemplates.get_template_list()
        self.assertGreater(len(templates), 0)
        
        # Test employee template
        df = MockDataTemplates.generate_by_template("employees", 10)
        self.assertEqual(len(df), 10)
        self.assertGreater(len(df.columns), 5)


if __name__ == "__main__":
    unittest.main()
