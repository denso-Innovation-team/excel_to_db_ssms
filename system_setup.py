#!/usr/bin/env python3
"""
Complete System Setup & Installation Script
ติดตั้งและตั้งค่าระบบ Excel to SSMS ให้พร้อมใช้งาน
"""

import subprocess
import sys
import os
import platform
import urllib.request
import zipfile
import shutil
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import logging


class SystemSetup:
    """Complete system setup and installation"""

    def __init__(self):
        self.setup_logging()
        self.python_version = sys.version_info
        self.platform = platform.system().lower()
        self.requirements_installed = []
        self.requirements_failed = []

    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)

    def check_python_version(self) -> bool:
        """Check if Python version is compatible"""
        print("🐍 Checking Python Version...")

        if self.python_version >= (3, 8):
            print(
                f"  ✅ Python {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro} - OK"
            )
            return True
        else:
            print(
                f"  ❌ Python {self.python_version.major}.{self.python_version.minor} - Requires Python 3.8+"
            )
            return False

    def upgrade_pip(self) -> bool:
        """Upgrade pip to latest version"""
        print("\n📦 Upgrading pip...")

        try:
            cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "pip"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print("  ✅ pip upgraded successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"  ⚠️ pip upgrade failed: {e}")
            return False

    def install_core_packages(self) -> Dict[str, bool]:
        """Install core Python packages"""
        print("\n📦 Installing Core Packages...")

        # Core packages that are essential
        core_packages = [
            "pandas>=2.0.0",
            "sqlalchemy>=2.0.0",
            "openpyxl>=3.1.0",
            "python-dotenv>=1.0.0",
            "tqdm>=4.65.0",
        ]

        # Optional packages (nice to have)
        optional_packages = [
            "pyodbc>=4.0.39",
            "numpy>=1.24.0",
            "xlrd>=2.0.1",
            "psutil>=5.9.0",
        ]

        results = {}

        # Install core packages first
        for package in core_packages:
            package_name = package.split(">=")[0]
            print(f"  Installing {package_name}...")

            try:
                cmd = [sys.executable, "-m", "pip", "install", package]
                subprocess.run(cmd, capture_output=True, text=True, check=True)
                print(f"    ✅ {package_name} installed")
                results[package_name] = True
                self.requirements_installed.append(package_name)
            except subprocess.CalledProcessError as e:
                print(f"    ❌ {package_name} failed: {e}")
                results[package_name] = False
                self.requirements_failed.append(package_name)

        # Install optional packages
        for package in optional_packages:
            package_name = package.split(">=")[0]
            print(f"  Installing {package_name} (optional)...")

            try:
                cmd = [sys.executable, "-m", "pip", "install", package]
                subprocess.run(cmd, capture_output=True, text=True, check=True)
                print(f"    ✅ {package_name} installed")
                results[package_name] = True
                self.requirements_installed.append(package_name)
            except subprocess.CalledProcessError as e:
                print(f"    ⚠️ {package_name} failed (optional): {e}")
                results[package_name] = False

        return results

    def check_odbc_driver(self) -> bool:
        """Check if ODBC Driver 17 for SQL Server is installed"""
        print("\n🔍 Checking ODBC Driver for SQL Server...")

        try:
            import pyodbc

            drivers = pyodbc.drivers()
            sql_server_drivers = [d for d in drivers if "SQL Server" in d]

            if sql_server_drivers:
                print(f"  ✅ Found SQL Server drivers:")
                for driver in sql_server_drivers:
                    print(f"    • {driver}")
                return True
            else:
                print(f"  ❌ No SQL Server ODBC drivers found")
                return False

        except ImportError:
            print(f"  ⚠️ pyodbc not available for checking")
            return False
        except Exception as e:
            print(f"  ❌ Error checking ODBC drivers: {e}")
            return False

    def create_project_structure(self) -> bool:
        """Create project directory structure"""
        print("\n📁 Creating Project Structure...")

        directories = [
            "data",
            "data/samples",
            "data/test",
            "data/performance",
            "logs",
            "config",
            "backup",
        ]

        try:
            for directory in directories:
                Path(directory).mkdir(parents=True, exist_ok=True)
                print(f"  ✅ Created: {directory}/")

            return True
        except Exception as e:
            print(f"  ❌ Error creating directories: {e}")
            return False

    def create_configuration_files(self) -> bool:
        """Create default configuration files"""
        print("\n⚙️ Creating Configuration Files...")

        try:
            # 1. Create .env template
            env_template = """# Excel to SSMS Configuration
# Edit these values for your SQL Server

# Database Connection
DB_HOST=10.73.148.27
DB_NAME=excel_to_db
DB_USER=TS00029
DB_PASSWORD=Thammaphon@TS00029
DB_DRIVER=ODBC Driver 17 for SQL Server

# Connection Pool Settings (Conservative for stability)
POOL_SIZE=3
MAX_OVERFLOW=5
POOL_TIMEOUT=30
POOL_RECYCLE=3600

# Processing Settings
BATCH_SIZE=500
MAX_WORKERS=2
CHUNK_SIZE=2000

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/excel_to_ssms.log
"""

            with open(".env.template", "w", encoding="utf-8") as f:
                f.write(env_template)
            print("  ✅ Created: .env.template")

            # 2. Create requirements.txt
            requirements_content = """# Excel to SSMS Requirements
# Core packages (required)
pandas>=2.0.0
sqlalchemy>=2.0.0
openpyxl>=3.1.0
python-dotenv>=1.0.0
tqdm>=4.65.0

# Optional packages (recommended)
pyodbc>=4.0.39
numpy>=1.24.0
xlrd>=2.0.1
psutil>=5.9.0

# Development packages (optional)
pytest>=7.4.0
"""

            with open("requirements.txt", "w", encoding="utf-8") as f:
                f.write(requirements_content)
            print("  ✅ Created: requirements.txt")

            # 3. Create .gitignore
            gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Excel to SSMS specific
logs/*.log
data/samples/*.xlsx
data/samples/*.xls
data/test/*.xlsx
data/performance/*.xlsx
*.tmp
*.temp
backup/*.bak

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# SQL Server
*.bak
*.ldf
*.mdf

# Configuration (keep template)
.env
!.env.template
"""

            with open(".gitignore", "w", encoding="utf-8") as f:
                f.write(gitignore_content)
            print("  ✅ Created: .gitignore")

            return True

        except Exception as e:
            print(f"  ❌ Error creating config files: {e}")
            return False

    def create_startup_scripts(self) -> bool:
        """Create convenient startup scripts"""
        print("\n🚀 Creating Startup Scripts...")

        try:
            # 1. Setup script for first-time users
            setup_script = """@echo off
echo 🎯 Excel to SSMS - First Time Setup
echo =====================================

echo 1. Installing Python packages...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo 2. Testing installation...
python -c "import pandas, sqlalchemy, openpyxl; print('✅ Core packages OK')"

echo.
echo 3. Creating sample data...
python sample_data_generator.py test

echo.
echo 4. Testing SQL Server connection...
python connection_tester.py

echo.
echo 🎉 Setup complete!
echo.
echo Next steps:
echo   1. Copy .env.template to .env and edit your database settings
echo   2. Run: python quick_test.py
echo.
pause
"""

            if self.platform == "windows":
                with open("setup.bat", "w", encoding="utf-8") as f:
                    f.write(setup_script)
                print("  ✅ Created: setup.bat (Windows)")

            # Linux/Mac version
            setup_sh = """#!/bin/bash
echo "🎯 Excel to SSMS - First Time Setup"
echo "====================================="

echo "1. Installing Python packages..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo ""
echo "2. Testing installation..."
python3 -c "import pandas, sqlalchemy, openpyxl; print('✅ Core packages OK')"

echo ""
echo "3. Creating sample data..."
python3 sample_data_generator.py test

echo ""
echo "4. Testing SQL Server connection..."
python3 connection_tester.py

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Copy .env.template to .env and edit your database settings"
echo "  2. Run: python3 quick_test.py"
"""

            with open("setup.sh", "w", encoding="utf-8") as f:
                f.write(setup_sh)

            # Make executable on Unix systems
            if self.platform in ["linux", "darwin"]:
                os.chmod("setup.sh", 0o755)
                print("  ✅ Created: setup.sh (Linux/Mac)")

            # 2. Quick start script
            quickstart_script = '''#!/usr/bin/env python3
"""
Quick Start - Get up and running fast
"""

import subprocess
import sys
from pathlib import Path

def main():
    print("🚀 Excel to SSMS - Quick Start")
    print("=" * 40)
    
    # Check .env file
    if not Path(".env").exists():
        if Path(".env.template").exists():
            print("⚠️  No .env file found")
            print("💡 Copy .env.template to .env and edit your database settings")
            print("   cp .env.template .env")
            return
        else:
            print("❌ No configuration file found")
            return
    
    # Check test data
    test_file = "data/test/employees_test_100.xlsx"
    if not Path(test_file).exists():
        print("📊 Creating test data...")
        subprocess.run([sys.executable, "sample_data_generator.py", "test"])
    
    # Run connection test
    print("🔍 Testing SQL Server connection...")
    try:
        result = subprocess.run([sys.executable, "connection_tester.py"], timeout=60)
        if result.returncode != 0:
            print("⚠️  Connection test failed")
            print("💡 Check your .env configuration")
            return
    except:
        print("⚠️  Could not run connection test")
    
    # Run quick test
    print("🧪 Running quick test...")
    try:
        result = subprocess.run([
            sys.executable, "excel_to_ssms_fixed.py", 
            test_file, "test_import"
        ], timeout=120)
        
        if result.returncode == 0:
            print("\\n✅ Quick start completed successfully!")
            print("💡 Check SQL Server Management Studio:")
            print("   Database: excel_to_db")
            print("   Table: test_import")
        else:
            print("\\n❌ Quick test failed")
    except:
        print("\\n❌ Quick test error")

if __name__ == "__main__":
    main()
'''

            with open("quickstart.py", "w", encoding="utf-8") as f:
                f.write(quickstart_script)
            print("  ✅ Created: quickstart.py")

            return True

        except Exception as e:
            print(f"  ❌ Error creating startup scripts: {e}")
            return False

    def test_installation(self) -> Dict[str, bool]:
        """Test the complete installation"""
        print("\n🧪 Testing Installation...")

        tests = {}

        # Test 1: Import core packages
        print("  Testing core package imports...")
        try:
            import pandas as pd
            import sqlalchemy
            import openpyxl
            from dotenv import load_dotenv
            from tqdm import tqdm

            print("    ✅ Core packages import OK")
            tests["imports"] = True
        except ImportError as e:
            print(f"    ❌ Import failed: {e}")
            tests["imports"] = False

        # Test 2: Excel file operations
        print("  Testing Excel operations...")
        try:
            import pandas as pd

            test_data = {"Name": ["Test"], "Value": [123]}
            df = pd.DataFrame(test_data)
            test_file = "test_excel.xlsx"
            df.to_excel(test_file, index=False)
            df_read = pd.read_excel(test_file)
            Path(test_file).unlink()  # Delete test file
            print("    ✅ Excel operations OK")
            tests["excel"] = True
        except Exception as e:
            print(f"    ❌ Excel test failed: {e}")
            tests["excel"] = False

        # Test 3: SQL Server driver (optional)
        print("  Testing SQL Server driver...")
        try:
            import pyodbc

            drivers = pyodbc.drivers()
            sql_drivers = [d for d in drivers if "SQL Server" in d]
            if sql_drivers:
                print("    ✅ SQL Server drivers available")
                tests["sql_driver"] = True
            else:
                print("    ⚠️  No SQL Server drivers found")
                tests["sql_driver"] = False
        except Exception:
            print("    ⚠️  Cannot test SQL Server drivers")
            tests["sql_driver"] = False

        return tests

    def provide_installation_summary(self, test_results: Dict[str, bool]):
        """Provide installation summary and next steps"""
        print("\n📊 Installation Summary")
        print("=" * 40)

        # Show test results
        all_core_passed = test_results.get("imports", False) and test_results.get(
            "excel", False
        )

        print(
            f"✅ Core packages: {'OK' if test_results.get('imports', False) else 'FAILED'}"
        )
        print(
            f"✅ Excel operations: {'OK' if test_results.get('excel', False) else 'FAILED'}"
        )
        print(
            f"✅ SQL Server driver: {'OK' if test_results.get('sql_driver', False) else 'NOT FOUND'}"
        )

        print(f"\n📦 Packages installed: {len(self.requirements_installed)}")
        for package in self.requirements_installed:
            print(f"  ✅ {package}")

        if self.requirements_failed:
            print(f"\n❌ Packages failed: {len(self.requirements_failed)}")
            for package in self.requirements_failed:
                print(f"  ❌ {package}")

        # System status
        if all_core_passed:
            print(f"\n🎉 System Ready!")
            print(f"✅ Excel to SSMS system is ready to use")

            print(f"\n🚀 Next Steps:")
            print(f"  1. Edit .env file with your SQL Server settings:")
            print(f"     cp .env.template .env")
            print(f"     # Edit .env with your database details")
            print(f"  2. Test SQL Server connection:")
            print(f"     python connection_tester.py")
            print(f"  3. Create sample data:")
            print(f"     python sample_data_generator.py test")
            print(f"  4. Run quick test:")
            print(f"     python quickstart.py")
            print(f"  5. Import your Excel files:")
            print(f"     python excel_to_ssms_fixed.py your_file.xlsx table_name")

        else:
            print(f"\n⚠️  System Issues")
            print(f"❌ Some components failed installation")

            if not test_results.get("imports", False):
                print(f"\n💡 Core package issues:")
                print(f"  • Try: pip install --upgrade pandas sqlalchemy openpyxl")
                print(f"  • Use virtual environment: python -m venv venv")

            if not test_results.get("excel", False):
                print(f"\n💡 Excel operation issues:")
                print(f"  • Try: pip install --upgrade openpyxl xlrd")

            if not test_results.get("sql_driver", False):
                print(f"\n💡 SQL Server driver issues:")
                print(f"  • Download and install: ODBC Driver 17 for SQL Server")
                print(
                    f"  • URL: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server"
                )

        # Files created
        print(f"\n📁 Files Created:")
        files_created = [
            ".env.template",
            "requirements.txt",
            ".gitignore",
            "quickstart.py",
        ]

        if self.platform == "windows":
            files_created.append("setup.bat")
        files_created.append("setup.sh")

        for file in files_created:
            if Path(file).exists():
                print(f"  ✅ {file}")

    def run_complete_setup(self) -> bool:
        """Run the complete system setup"""
        print("🎯 Excel to SSMS - Complete System Setup")
        print("=" * 60)
        print("Setting up your Excel to SQL Server import system...")
        print("=" * 60)

        # Step 1: Check Python version
        if not self.check_python_version():
            print("\n❌ Setup failed: Python version too old")
            print("💡 Please upgrade to Python 3.8 or newer")
            return False

        # Step 2: Upgrade pip
        self.upgrade_pip()

        # Step 3: Install packages
        package_results = self.install_core_packages()

        # Step 4: Check ODBC driver
        self.check_odbc_driver()

        # Step 5: Create project structure
        if not self.create_project_structure():
            print("\n❌ Setup failed: Could not create directories")
            return False

        # Step 6: Create configuration files
        if not self.create_configuration_files():
            print("\n❌ Setup failed: Could not create config files")
            return False

        # Step 7: Create startup scripts
        if not self.create_startup_scripts():
            print("\n❌ Setup failed: Could not create startup scripts")
            return False

        # Step 8: Test installation
        test_results = self.test_installation()

        # Step 9: Provide summary
        self.provide_installation_summary(test_results)

        # Determine success
        core_success = test_results.get("imports", False) and test_results.get(
            "excel", False
        )

        if core_success:
            print(f"\n✅ Setup completed successfully!")
            return True
        else:
            print(f"\n⚠️  Setup completed with issues")
            print(f"💡 See troubleshooting steps above")
            return False


def main():
    """Main setup function"""
    setup = SystemSetup()
    success = setup.run_complete_setup()

    if success:
        print(f"\n🎊 Welcome to Excel to SSMS!")
        print(f"Your system is ready for importing Excel data to SQL Server.")
    else:
        print(f"\n🔧 Setup needs attention")
        print(f"Please resolve the issues above before proceeding.")

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
