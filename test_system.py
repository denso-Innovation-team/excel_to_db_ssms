#!/usr/bin/env python3
"""
test_system.py - Complete System Testing for DENSO888
ทดสอบระบบครบทุกด้าน ก่อนใช้งานจริง
"""

import sys
import os
import sqlite3
import traceback
from pathlib import Path
from datetime import datetime
import importlib.util


class DENSO888SystemTester:
    """ระบบทดสอบ DENSO888 อย่างครอบคลุม"""

    def __init__(self):
        self.test_results = []
        self.errors = []
        self.warnings = []

    def log_test(
        self, test_name: str, status: str, message: str = "", details: str = ""
    ):
        """บันทึกผลการทดสอบ"""
        result = {
            "test": test_name,
            "status": status,  # PASS, FAIL, WARNING
            "message": message,
            "details": details,
            "timestamp": datetime.now().isoformat(),
        }
        self.test_results.append(result)

        # Print immediate feedback
        status_icon = {"PASS": "✅", "FAIL": "❌", "WARNING": "⚠️"}.get(status, "❓")
        print(f"  {status_icon} {test_name}: {message}")

        if status == "FAIL":
            self.errors.append(result)
        elif status == "WARNING":
            self.warnings.append(result)

    def test_python_environment(self):
        """ทดสอบ Python environment"""
        print("\n🐍 Testing Python Environment...")

        # Python version
        py_version = sys.version_info
        if py_version.major == 3 and py_version.minor >= 8:
            self.log_test(
                "Python Version",
                "PASS",
                f"Python {py_version.major}.{py_version.minor}.{py_version.micro}",
            )
        else:
            self.log_test(
                "Python Version",
                "FAIL",
                f"Python {py_version.major}.{py_version.minor} - Requires 3.8+",
            )

        # Required modules
        required_modules = [
            ("tkinter", "GUI framework"),
            ("pandas", "Data processing"),
            ("sqlalchemy", "Database ORM"),
            ("openpyxl", "Excel processing"),
            ("sqlite3", "SQLite database"),
        ]

        for module_name, description in required_modules:
            try:
                if module_name == "sqlite3":
                    import sqlite3
                elif module_name == "tkinter":
                    import tkinter

                    # Test if tkinter can create windows
                    root = tkinter.Tk()
                    root.withdraw()
                    root.destroy()
                else:
                    importlib.import_module(module_name)

                self.log_test(f"Module: {module_name}", "PASS", description)

            except ImportError as e:
                self.log_test(
                    f"Module: {module_name}", "FAIL", f"Missing: {description}", str(e)
                )
            except Exception as e:
                self.log_test(
                    f"Module: {module_name}",
                    "WARNING",
                    f"Import issue: {description}",
                    str(e),
                )

    def test_project_structure(self):
        """ทดสอบโครงสร้างโปรเจค"""
        print("\n📁 Testing Project Structure...")

        # Required files
        required_files = [
            ("main.py", "Application entry point"),
            ("requirements.txt", "Dependencies list"),
            ("config/settings.py", "Configuration"),
            ("core/database_manager.py", "Database management"),
            ("core/excel_handler.py", "Excel processing"),
            ("core/mock_generator.py", "Mock data generation"),
            ("core/data_processor.py", "Data processing pipeline"),
            ("gui/main_window.py", "Main GUI"),
            ("utils/logger.py", "Logging system"),
            ("utils/error_handler.py", "Error handling"),
            ("utils/settings_manager.py", "Settings management"),
            ("utils/file_utils.py", "File utilities"),
        ]

        for file_path, description in required_files:
            path = Path(file_path)
            if path.exists():
                # Check if file has content
                if path.stat().st_size > 0:
                    self.log_test(f"File: {file_path}", "PASS", description)
                else:
                    self.log_test(
                        f"File: {file_path}", "WARNING", f"{description} (empty)"
                    )
            else:
                self.log_test(f"File: {file_path}", "FAIL", f"Missing: {description}")

        # Required directories
        required_dirs = [
            ("config", "Configuration files"),
            ("core", "Business logic"),
            ("gui", "User interface"),
            ("utils", "Utilities"),
            ("logs", "Log files"),
            ("assets", "Static assets"),
        ]

        for dir_path, description in required_dirs:
            path = Path(dir_path)
            if path.exists() and path.is_dir():
                self.log_test(f"Directory: {dir_path}", "PASS", description)
            else:
                self.log_test(
                    f"Directory: {dir_path}", "FAIL", f"Missing: {description}"
                )

    def test_configuration_loading(self):
        """ทดสอบการโหลด configuration"""
        print("\n⚙️ Testing Configuration Loading...")

        try:
            # Test config loading
            sys.path.insert(0, str(Path.cwd()))
            from config.settings import get_config, DatabaseConfig, AppConfig

            config = get_config()

            if isinstance(config, AppConfig):
                self.log_test("Config Loading", "PASS", "AppConfig loaded successfully")

                # Test database config
                if hasattr(config, "database") and isinstance(
                    config.database, DatabaseConfig
                ):
                    self.log_test("Database Config", "PASS", "DatabaseConfig available")

                    # Test pool settings (the original issue)
                    if hasattr(config.database, "pool_size"):
                        self.log_test(
                            "Pool Settings",
                            "PASS",
                            f"Pool size: {config.database.pool_size}",
                        )
                    else:
                        self.log_test(
                            "Pool Settings", "FAIL", "Missing pool_size attribute"
                        )
                else:
                    self.log_test("Database Config", "FAIL", "DatabaseConfig not found")

                # Test other configs
                if hasattr(config, "ui"):
                    self.log_test("UI Config", "PASS", "UI configuration available")

                if hasattr(config, "auth"):
                    self.log_test(
                        "Auth Config", "PASS", "Authentication configuration available"
                    )

            else:
                self.log_test("Config Loading", "FAIL", "Invalid config type")

        except Exception as e:
            self.log_test(
                "Config Loading", "FAIL", "Configuration import failed", str(e)
            )

    def test_core_modules(self):
        """ทดสอบ core modules"""
        print("\n🔧 Testing Core Modules...")

        try:
            # Test database manager
            from core.database_manager import DatabaseManager

            self.log_test("DatabaseManager", "PASS", "Import successful")

            # Test excel handler
            from core.excel_handler import ExcelHandler

            self.log_test("ExcelHandler", "PASS", "Import successful")

            # Test mock generator
            from core.mock_generator import MockDataGenerator

            mock_gen = MockDataGenerator()

            # Test mock data generation
            test_df = mock_gen.generate_employee_data(10)
            if len(test_df) == 10:
                self.log_test(
                    "Mock Data Generation",
                    "PASS",
                    f"Generated {len(test_df)} employee records",
                )
            else:
                self.log_test(
                    "Mock Data Generation",
                    "FAIL",
                    f"Expected 10 rows, got {len(test_df)}",
                )

            # Test data processor
            from core.data_processor import DataProcessor

            self.log_test("DataProcessor", "PASS", "Import successful")

        except Exception as e:
            self.log_test("Core Modules", "FAIL", "Import failed", str(e))

    def test_database_functionality(self):
        """ทดสอบฟังก์ชัน database"""
        print("\n🗄️ Testing Database Functionality...")

        try:
            from config.settings import DatabaseConfig
            from core.database_manager import DatabaseManager

            # Test SQLite (should always work)
            config = DatabaseConfig()
            config.sqlite_file = "test_denso888.db"

            db_manager = DatabaseManager(config)

            # Test connection
            if db_manager.connect(force_mode="sqlite"):
                self.log_test("SQLite Connection", "PASS", "Connected successfully")

                # Test table creation
                import pandas as pd

                test_data = pd.DataFrame(
                    {
                        "id": [1, 2, 3],
                        "name": ["Test1", "Test2", "Test3"],
                        "value": [100, 200, 300],
                    }
                )

                try:
                    db_manager.create_table_from_dataframe("test_table", test_data)
                    self.log_test("Table Creation", "PASS", "Test table created")

                    # Test data insertion
                    rows_inserted = db_manager.bulk_insert("test_table", test_data)
                    if rows_inserted == 3:
                        self.log_test(
                            "Data Insertion", "PASS", f"Inserted {rows_inserted} rows"
                        )
                    else:
                        self.log_test(
                            "Data Insertion",
                            "WARNING",
                            f"Expected 3 rows, inserted {rows_inserted}",
                        )

                    # Test data retrieval
                    table_info = db_manager.get_table_info("test_table")
                    if table_info.get("row_count", 0) == 3:
                        self.log_test(
                            "Data Retrieval",
                            "PASS",
                            f"Retrieved table info: {table_info['row_count']} rows",
                        )
                    else:
                        self.log_test(
                            "Data Retrieval",
                            "WARNING",
                            f"Unexpected row count: {table_info.get('row_count', 0)}",
                        )

                    # Cleanup
                    db_manager.execute_query("DROP TABLE test_table")

                except Exception as db_error:
                    self.log_test(
                        "Database Operations",
                        "FAIL",
                        "Database operations failed",
                        str(db_error),
                    )

                db_manager.close()

                # Remove test database
                try:
                    Path("test_denso888.db").unlink()
                except:
                    pass

            else:
                self.log_test(
                    "SQLite Connection", "FAIL", "Could not connect to SQLite"
                )

        except Exception as e:
            self.log_test(
                "Database Functionality", "FAIL", "Database test failed", str(e)
            )

    def test_authentication_system(self):
        """ทดสอบระบบ authentication"""
        print("\n🔐 Testing Authentication System...")

        try:
            # Test if we can create auth system
            from gui.main_window import AuthenticationManager

            auth_manager = AuthenticationManager()
            self.log_test(
                "Auth System Init", "PASS", "Authentication system initialized"
            )

            # Test default admin user
            success, message = auth_manager.authenticate("admin", "admin123")
            if success:
                self.log_test(
                    "Default Admin Login", "PASS", "Admin authentication successful"
                )

                # Test permissions
                can_read_sqlite = auth_manager.check_permission("sqlite", "read")
                can_write_sqlite = auth_manager.check_permission("sqlite", "write")

                if can_read_sqlite and can_write_sqlite:
                    self.log_test(
                        "Admin Permissions", "PASS", "Full SQLite permissions"
                    )
                else:
                    self.log_test(
                        "Admin Permissions",
                        "WARNING",
                        f"Limited permissions: R:{can_read_sqlite}, W:{can_write_sqlite}",
                    )

                auth_manager.logout()
            else:
                self.log_test(
                    "Default Admin Login", "FAIL", f"Authentication failed: {message}"
                )

            # Test invalid login
            success, message = auth_manager.authenticate("invalid", "invalid")
            if not success:
                self.log_test(
                    "Invalid Login Protection", "PASS", "Invalid credentials rejected"
                )
            else:
                self.log_test(
                    "Invalid Login Protection",
                    "FAIL",
                    "Security issue: invalid login accepted",
                )

            # Cleanup auth database
            try:
                Path("auth.db").unlink()
            except:
                pass

        except Exception as e:
            self.log_test(
                "Authentication System", "FAIL", "Auth system test failed", str(e)
            )

    def test_gui_components(self):
        """ทดสอบ GUI components"""
        print("\n🖥️ Testing GUI Components...")

        try:
            import tkinter as tk

            # Test basic tkinter functionality
            root = tk.Tk()
            root.withdraw()

            # Test main window import
            from gui.main_window import DENSO888MainWindow

            self.log_test("Main Window Import", "PASS", "GUI main window imported")

            root.destroy()

            # Test GUI utilities
            try:
                from utils.logger import setup_gui_logger

                self.log_test("GUI Logger", "PASS", "GUI logging system available")
            except:
                self.log_test("GUI Logger", "WARNING", "GUI logging system unavailable")

        except Exception as e:
            self.log_test("GUI Components", "FAIL", "GUI test failed", str(e))

    def test_file_operations(self):
        """ทดสอบการทำงานกับไฟล์"""
        print("\n📄 Testing File Operations...")

        try:
            from utils.file_utils import FileUtils

            # Test directory creation
            test_dir = Path("test_temp_dir")
            FileUtils.ensure_directory(test_dir)

            if test_dir.exists():
                self.log_test(
                    "Directory Creation", "PASS", "Directory created successfully"
                )

                # Test file info
                test_file = test_dir / "test.txt"
                test_file.write_text("Test content")

                file_info = FileUtils.get_file_info(test_file)
                if "size_bytes" in file_info:
                    self.log_test(
                        "File Info",
                        "PASS",
                        f"File info retrieved: {file_info['size_bytes']} bytes",
                    )
                else:
                    self.log_test("File Info", "FAIL", "Could not get file info")

                # Cleanup
                test_file.unlink()
                test_dir.rmdir()

            else:
                self.log_test(
                    "Directory Creation", "FAIL", "Could not create directory"
                )

        except Exception as e:
            self.log_test(
                "File Operations", "FAIL", "File operations test failed", str(e)
            )

    def test_sample_data_creation(self):
        """ทดสอบการสร้างข้อมูลตัวอย่าง"""
        print("\n🎲 Testing Sample Data Creation...")

        try:
            from utils.file_utils import FileUtils

            # Test sample Excel creation
            sample_file = Path("test_sample.xlsx")

            success = FileUtils.create_sample_excel(sample_file, "employees", 100)

            if success and sample_file.exists():
                self.log_test(
                    "Sample Excel Creation",
                    "PASS",
                    f"Created {sample_file} with 100 employee records",
                )

                # Test validation
                validation = FileUtils.validate_excel_file(sample_file)
                if validation.get("valid", False):
                    self.log_test(
                        "Excel Validation", "PASS", f"Sample file is valid Excel"
                    )
                else:
                    self.log_test(
                        "Excel Validation", "FAIL", f"Sample file validation failed"
                    )

                # Cleanup
                sample_file.unlink()

            else:
                self.log_test(
                    "Sample Excel Creation",
                    "FAIL",
                    "Could not create sample Excel file",
                )

        except Exception as e:
            self.log_test(
                "Sample Data Creation", "FAIL", "Sample data test failed", str(e)
            )

    def run_full_test_suite(self):
        """รันการทดสอบทั้งหมด"""
        print("🏭 DENSO888 - Complete System Testing")
        print("=" * 60)
        print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🐍 Python: {sys.version}")
        print(f"📁 Working Directory: {Path.cwd()}")
        print("=" * 60)

        # Run all tests
        test_methods = [
            self.test_python_environment,
            self.test_project_structure,
            self.test_configuration_loading,
            self.test_core_modules,
            self.test_database_functionality,
            self.test_authentication_system,
            self.test_gui_components,
            self.test_file_operations,
            self.test_sample_data_creation,
        ]

        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                test_name = (
                    test_method.__name__.replace("test_", "").replace("_", " ").title()
                )
                self.log_test(
                    test_name, "FAIL", f"Test crashed: {str(e)}", traceback.format_exc()
                )

        # Generate summary
        self.generate_test_summary()

    def generate_test_summary(self):
        """สร้างสรุปผลการทดสอบ"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)

        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        warning_tests = len([r for r in self.test_results if r["status"] == "WARNING"])

        print(f"📈 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⚠️ Warnings: {warning_tests}")

        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        print(f"🎯 Success Rate: {success_rate:.1f}%")

        # System status
        if failed_tests == 0:
            if warning_tests == 0:
                print("\n🎉 SYSTEM STATUS: EXCELLENT - Ready for production!")
            else:
                print(
                    f"\n✅ SYSTEM STATUS: GOOD - Ready with {warning_tests} minor issues"
                )
        elif failed_tests <= 2:
            print(
                f"\n⚠️ SYSTEM STATUS: NEEDS ATTENTION - {failed_tests} critical issues"
            )
        else:
            print(
                f"\n❌ SYSTEM STATUS: NOT READY - {failed_tests} critical issues need fixing"
            )

        # Show critical failures
        if self.errors:
            print(f"\n❌ CRITICAL ISSUES ({len(self.errors)}):")
            for error in self.errors:
                print(f"  • {error['test']}: {error['message']}")

        # Show warnings
        if self.warnings:
            print(f"\n⚠️ WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  • {warning['test']}: {warning['message']}")

        # Recommendations
