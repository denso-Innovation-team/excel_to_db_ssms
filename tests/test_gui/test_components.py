"""
tests/test_gui/test_components.py
GUI Components Tests
"""

import unittest
import tkinter as tk
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from gui.components.modern_components import ModernButton, BaseComponent
from gui.components.file_selector import FileSelector


class TestModernComponents(unittest.TestCase):
    """Test modern UI components"""

    def setUp(self):
        """Setup test environment"""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during tests

    def tearDown(self):
        """Cleanup test environment"""
        self.root.destroy()

    def test_modern_button_creation(self):
        """Test modern button creation"""
        button = ModernButton(
            self.root, text="Test Button", style="primary", size="medium"
        )

        widget = button.get_widget()
        self.assertIsInstance(widget, tk.Button)
        self.assertEqual(widget.cget("text"), "Test Button")

    def test_modern_button_styles(self):
        """Test different button styles"""
        styles = ["primary", "secondary", "success", "danger", "info"]

        for style in styles:
            button = ModernButton(self.root, text=f"Test {style}", style=style)
            widget = button.get_widget()
            self.assertIsInstance(widget, tk.Button)

    def test_modern_button_sizes(self):
        """Test different button sizes"""
        sizes = ["small", "medium", "large"]

        for size in sizes:
            button = ModernButton(self.root, text=f"Test {size}", size=size)
            widget = button.get_widget()
            self.assertIsInstance(widget, tk.Button)

    def test_modern_button_command(self):
        """Test button command functionality"""
        clicked = [False]

        def on_click():
            clicked[0] = True

        button = ModernButton(self.root, text="Click me", command=on_click)

        widget = button.get_widget()
        widget.invoke()  # Simulate click

        self.assertTrue(clicked[0])

    def test_file_selector_creation(self):
        """Test file selector creation"""
        selector = FileSelector(self.root, title="Test File Selector")

        widget = selector.get_widget()
        self.assertIsInstance(widget, tk.Frame)

    def test_file_selector_events(self):
        """Test file selector event binding"""
        selector = FileSelector(self.root)

        event_triggered = [False]

        def on_file_selected(file_path):
            event_triggered[0] = True

        selector.bind_event("file_selected", on_file_selected)

        # Simulate file selection
        selector._set_file("test_file.txt")

        self.assertTrue(event_triggered[0])


class TestBaseComponent(unittest.TestCase):
    """Test base component functionality"""

    def setUp(self):
        """Setup test environment"""
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self):
        """Cleanup test environment"""
        self.root.destroy()

    def test_base_component_abstract(self):
        """Test that BaseComponent cannot be instantiated directly"""
        with self.assertRaises(TypeError):
            BaseComponent(self.root)


if __name__ == "__main__":
    unittest.main()
