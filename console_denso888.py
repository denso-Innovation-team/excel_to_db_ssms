#!/usr/bin/env python3
"""
DENSO888 Console Version - ไม่ใช้ GUI
แก้ปัญหา Tkinter โดยใช้ Command Line Interface
"""

import sys
import logging
from pathlib import Path


# Setup logging
def setup_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "denso888.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


logger = logging.getLogger(__name__)


class DENSO888Console:
    """Console version ของ DENSO888"""

    def __init__(self):
        self.auth_user = None
        print("🏭 DENSO888 - Excel to SQL Management System (Console Mode)")
        print("   by เฮียตอมจัดหั้ย!!!")
        print("=" * 60)

    def authenticate(self):
        """Simple authentication"""
        print("\n🔐 Authentication Required")
        username = input("👤 Username [admin]: ").strip() or "admin"
        password = input("🔒 Password: ").strip()

        if username == "admin" and password == "admin123":
            self.auth_user = {"username": username, "role": "admin"}
            print(f"✅ Welcome {username}!")
            return True
        else:
            print("❌ Invalid credentials")
            return False

    def show_menu(self):
        """แสดงเมนูหลัก"""
        while True:
            print("\n" + "=" * 60)
            print("📋 DENSO888 Main Menu")
            print("=" * 60)
            print("1. 🎲 Generate Mock Data")
            print("2. 📁 Import Excel File")
            print("3. 🔐 Test Database Connection")
            print("4. 📊 View Last Results")
            print("5. 🗑️  Clear Logs")
            print("0. 🚪 Exit")
            print("-" * 60)

            choice = input("Select option [0-5]: ").strip()

            if choice == "1":
                self.generate_mock_data()
            elif choice == "2":
                self.import_excel()
            elif choice == "3":
                self.test_database()
            elif choice == "4":
                self.view_results()
            elif choice == "5":
                self.clear_logs()
            elif choice == "0":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid option")

    def generate_mock_data(self):
        """Generate mock data"""
        print("\n🎲 Generate Mock Data")
        print("-" * 40)

        templates = {
            "1": ("employees", "Employee records with HR data"),
            "2": ("sales", "Sales transactions and customers"),
            "3": ("inventory", "Product inventory and stock"),
            "4": ("financial", "Financial transactions"),
        }

        print("Available templates:")
        for key, (name, desc) in templates.items():
            print(f"{key}. {name} - {desc}")

        template_choice = input("Select template [1-4]: ").strip()
        if template_choice not in templates:
            print("❌ Invalid template")
            return

        template_name = templates[template_choice][0]

        try:
            rows = int(input("Number of rows [1000]: ").strip() or "1000")
            if rows > 50000:
                print("⚠️ Large dataset! This may take time.")
        except ValueError:
            rows = 1000

        # Database selection
        db_type = self.select_database()
        if not db_type:
            return

        # Process data
        print(f"\n🚀 Processing {rows:,} rows of {template_name} data...")

        try:
            result = self.process_data(
                {"type": "mock", "template": template_name, "rows": rows}, db_type
            )

            self.show_results(result)

        except Exception as e:
            print(f"❌ Error: {e}")
            logger.error(f"Mock data generation failed: {e}")

    def import_excel(self):
        """Import Excel file"""
        print("\n📁 Import Excel File")
        print("-" * 40)

        file_path = input("Excel file path: ").strip().strip('"')
        if not file_path or not Path(file_path).exists():
            print("❌ File not found")
            return

        # Show sheets
        try:
            from core.excel_handler import ExcelHandler

            handler = ExcelHandler()
            sheets = handler.get_sheets(file_path)

            if not sheets:
                print("❌ No sheets found")
                return

            print(f"Available sheets: {', '.join(sheets)}")
            sheet = input(f"Select sheet [{sheets[0]}]: ").strip() or sheets[0]

        except Exception as e:
            print(f"❌ Excel error: {e}")
            return

        # Database selection
        db_type = self.select_database()
        if not db_type:
            return

        # Process
        print(f"\n🚀 Processing Excel file...")

        try:
            result = self.process_data(
                {"type": "excel", "file_path": file_path, "sheet_name": sheet}, db_type
            )

            self.show_results(result)

        except Exception as e:
            print(f"❌ Error: {e}")
            logger.error(f"Excel import failed: {e}")

    def select_database(self):
        """เลือกประเภทฐานข้อมูล"""
        print("\n🗄️ Database Selection")
        print("1. 📁 SQLite (Local, no setup required)")
        print("2. 🏢 SQL Server (Enterprise database)")

        choice = input("Select database [1-2]: ").strip()

        if choice == "1":
            return self.configure_sqlite()
        elif choice == "2":
            return self.configure_sqlserver()
        else:
            print("❌ Invalid choice")
            return None

    def configure_sqlite(self):
        """Configure SQLite"""
        db_file = (
            input("SQLite file [denso888_data.db]: ").strip() or "denso888_data.db"
        )

        return {"type": "sqlite", "sqlite_file": db_file}

    def configure_sqlserver(self):
        """Configure SQL Server"""
        print("\n🏢 SQL Server Configuration")

        server = input("Server [localhost]: ").strip() or "localhost"
        database = input("Database [excel_to_db]: ").strip() or "excel_to_db"

        print("Authentication:")
        print("1. Windows Authentication (recommended)")
        print("2. SQL Server Authentication")

        auth_choice = input("Select [1-2]: ").strip()

        if auth_choice == "2":
            username = input("Username [sa]: ").strip() or "sa"
            password = input("Password: ").strip()
            use_windows_auth = False
        else:
            username = ""
            password = ""
            use_windows_auth = True

        return {
            "type": "sqlserver",
            "server": server,
            "database": database,
            "username": username,
            "password": password,
            "use_windows_auth": use_windows_auth,
        }

    def process_data(self, data_config, db_config):
        """Process data to database"""
        try:
            from config.settings import DatabaseConfig
            from core.database_manager import DatabaseManager
            from core.data_processor import DataProcessor
            from core.mock_generator import MockDataTemplates

            # Create database config
            if db_config["type"] == "sqlite":
                config = DatabaseConfig()
                config.sqlite_file = db_config["sqlite_file"]
            else:
                config = DatabaseConfig()
                config.server = db_config["server"]
                config.database = db_config["database"]
                config.username = db_config["username"]
                config.password = db_config["password"]
                config.use_windows_auth = db_config["use_windows_auth"]

            # Add table name
            table_name = (
                input("Table name [imported_data]: ").strip() or "imported_data"
            )
            data_config["table_name"] = table_name

            # Create processor
            class ProcessingConfig:
                chunk_size = 5000
                batch_size = 1000

            processor = DataProcessor(data_config, config, ProcessingConfig())

            # Process with progress
            def progress_callback(data):
                progress = data.get("progress", 0)
                message = data.get("message", "Processing...")
                print(f"\r⏳ {message} ({progress:.1f}%)", end="", flush=True)

            def log_callback(message, level="info"):
                if level == "error":
                    print(f"\n❌ {message}")
                elif level == "warning":
                    print(f"\n⚠️ {message}")

            result = processor.process(progress_callback, log_callback)
            print()  # New line after progress

            return result

        except ImportError as e:
            return {"success": False, "error": f"Missing module: {e}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def test_database(self):
        """Test database connection"""
        print("\n🔐 Database Connection Test")
        print("-" * 40)

        db_config = self.select_database()
        if not db_config:
            return

        try:
            from config.settings import DatabaseConfig
            from core.database_manager import DatabaseManager

            if db_config["type"] == "sqlite":
                config = DatabaseConfig()
                config.sqlite_file = db_config["sqlite_file"]
                force_mode = "sqlite"
            else:
                config = DatabaseConfig()
                config.server = db_config["server"]
                config.database = db_config["database"]
                config.username = db_config["username"]
                config.password = db_config["password"]
                config.use_windows_auth = db_config["use_windows_auth"]
                force_mode = "sqlserver"

            print("🔍 Testing connection...")

            db_manager = DatabaseManager(config)
            success = db_manager.connect(force_mode=force_mode)

            if success:
                print("✅ Connection successful!")

                # Show database info
                status = db_manager.get_status()
                print(f"📊 Active database: {status['active_database'].upper()}")

                if db_config["type"] == "sqlite":
                    print(f"📁 File: {db_config['sqlite_file']}")
                else:
                    print(f"🏢 Server: {db_config['server']}")
                    print(f"🗄️ Database: {db_config['database']}")

            else:
                print("❌ Connection failed!")

            db_manager.close()

        except Exception as e:
            print(f"❌ Test failed: {e}")

    def show_results(self, result):
        """แสดงผลลัพธ์"""
        print("\n" + "=" * 60)
        print("📊 Processing Results")
        print("=" * 60)

        if result.get("success"):
            print("✅ Status: SUCCESS")
            print(f"📝 Rows processed: {result.get('rows_processed', 0):,}")
            print(f"⏱️ Duration: {result.get('duration', 0):.2f} seconds")
            print(f"🗄️ Table: {result.get('table_name', 'N/A')}")
            print(f"🏢 Database: {result.get('database_type', 'N/A').upper()}")

            # Performance metrics
            if "metrics" in result:
                rps = result["metrics"].get("rows_per_second", 0)
                print(f"⚡ Speed: {rps:.0f} rows/second")

            # Table info
            if "table_info" in result:
                info = result["table_info"]
                print(f"📊 Table rows: {info.get('row_count', 0):,}")
                print(f"📊 Table columns: {info.get('column_count', 0)}")
                if "size_mb" in info:
                    print(f"💾 Table size: {info['size_mb']} MB")
        else:
            print("❌ Status: FAILED")
            print(f"💥 Error: {result.get('error', 'Unknown error')}")

        print("-" * 60)
        input("Press Enter to continue...")

    def view_results(self):
        """View last results from log"""
        print("\n📄 Last Results")
        print("-" * 40)

        log_file = Path("logs/denso888.log")
        if not log_file.exists():
            print("❌ No log file found")
            return

        try:
            with open(log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Show last 20 lines
            recent_lines = lines[-20:] if len(lines) > 20 else lines

            for line in recent_lines:
                if "ERROR" in line:
                    print(f"❌ {line.strip()}")
                elif "WARNING" in line:
                    print(f"⚠️ {line.strip()}")
                elif "INFO" in line:
                    print(f"ℹ️ {line.strip()}")
                else:
                    print(line.strip())

        except Exception as e:
            print(f"❌ Error reading log: {e}")

        input("Press Enter to continue...")

    def clear_logs(self):
        """Clear log files"""
        print("\n🗑️ Clear Logs")

        confirm = input("Clear all logs? (y/N): ").strip().lower()
        if confirm in ["y", "yes"]:
            try:
                log_file = Path("logs/denso888.log")
                if log_file.exists():
                    log_file.unlink()
                print("✅ Logs cleared")
            except Exception as e:
                print(f"❌ Error: {e}")
        else:
            print("❌ Cancelled")

    def run(self):
        """Run console application"""
        try:
            if self.authenticate():
                self.show_menu()
            else:
                print("❌ Authentication failed")
                return 1
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
        except Exception as e:
            print(f"❌ Fatal error: {e}")
            logger.error(f"Console app error: {e}")
            return 1

        return 0


def main():
    """Main entry point"""
    setup_logging()

    print("🔍 Checking dependencies...")

    # Check core dependencies
    required = ["pandas", "sqlalchemy", "openpyxl"]
    missing = []

    for module in required:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError:
            missing.append(module)
            print(f"  ❌ {module}")

    if missing:
        print(f"❌ Install missing: pip install {' '.join(missing)}")
        return 1

    print("✅ Dependencies OK")

    # Run console app
    app = DENSO888Console()
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
