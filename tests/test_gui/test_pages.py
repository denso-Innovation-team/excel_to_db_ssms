"""
tests/test_gui/test_pages.py
GUI Pages Tests
"""

import unittest
import tkinter as tk
import sys
import os
from unittest.mock import Mock

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

# Mock dependencies that might not be available during testing
try:
    from gui.pages.dashboard_page import DashboardPage
    from gui.pages.logs_page import LogsPage
except ImportError:
    DashboardPage = None
    LogsPage = None


class TestGUIPages(unittest.TestCase):
    """Test GUI pages functionality"""

    def setUp(self):
        """Setup test environment"""
        self.root = tk.Tk()
        self.root.withdraw()

        # Mock theme and controller
        self.mock_theme = Mock()
        self.mock_theme.colors = Mock()
        self.mock_theme.colors.background = "#FFFFFF"
        self.mock_theme.colors.primary = "#FF0066"
        self.mock_theme.colors.text_primary = "#000000"
        self.mock_theme.fonts = {
            "heading_lg": ("Arial", 16, "bold"),
            "body_md": ("Arial", 10),
            "body_sm": ("Arial", 9),
        }

        self.mock_controller = Mock()
        self.mock_controller.get_database_status.return_value = {
            "connected": False,
            "type": "sqlite",
        }
        self.mock_controller.get_recent_logs.return_value = []

    def tearDown(self):
        """Cleanup test environment"""
        self.root.destroy()

    @unittest.skipIf(DashboardPage is None, "DashboardPage not available")
    def test_dashboard_page_creation(self):
        """Test dashboard page creation"""
        page = DashboardPage(self.root, self.mock_controller, self.mock_theme)

        self.assertIsNotNone(page.main_frame)
        self.assertIsNotNone(page.scrollable_frame)

    @unittest.skipIf(DashboardPage is None, "DashboardPage not available")
    def test_dashboard_page_show_hide(self):
        """Test dashboard page show/hide functionality"""
        page = DashboardPage(self.root, self.mock_controller, self.mock_theme)

        # Test show
        page.show()

        # Test hide
        page.hide()

    @unittest.skipIf(LogsPage is None, "LogsPage not available")
    def test_logs_page_creation(self):
        """Test logs page creation"""
        page = LogsPage(self.root, self.mock_controller, self.mock_theme)

        self.assertIsNotNone(page.main_frame)
        self.assertIsNotNone(page.log_text)

    @unittest.skipIf(LogsPage is None, "LogsPage not available")
    def test_logs_page_filtering(self):
        """Test logs page filtering functionality"""
        page = LogsPage(self.root, self.mock_controller, self.mock_theme)

        # Test filter level changes
        page.filter_level.set("ERROR")
        page._apply_filters()

        # Test auto-scroll toggle
        page.auto_scroll.set(False)
        self.assertFalse(page.auto_scroll.get())


class TestPageIntegration(unittest.TestCase):
    """Test page integration functionality"""

    def setUp(self):
        """Setup test environment"""
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self):
        """Cleanup test environment"""
        self.root.destroy()

    def test_page_navigation_concept(self):
        """Test page navigation concept"""
        # Create container for pages
        container = tk.Frame(self.root)
        container.pack(fill="both", expand=True)

        # Mock page objects
        pages = {}

        class MockPage:
            def __init__(self, name):
                self.name = name
                self.frame = tk.Frame(container)
                self.is_visible = False

            def show(self):
                self.frame.pack(fill="both", expand=True)
                self.is_visible = True

            def hide(self):
                self.frame.pack_forget()
                self.is_visible = False

            def refresh(self):
                pass

        # Create mock pages
        pages["dashboard"] = MockPage("dashboard")
        pages["logs"] = MockPage("logs")

        # Test navigation
        current_page = None

        def show_page(page_id):
            nonlocal current_page

            # Hide current page
            if current_page:
                pages[current_page].hide()

            # Show new page
            if page_id in pages:
                pages[page_id].show()
                current_page = page_id

        # Test page switching
        show_page("dashboard")
        self.assertTrue(pages["dashboard"].is_visible)
        self.assertFalse(pages["logs"].is_visible)

        show_page("logs")
        self.assertFalse(pages["dashboard"].is_visible)
        self.assertTrue(pages["logs"].is_visible)


if __name__ == "__main__":
    unittest.main()
