#!/usr/bin/env python3
"""
setup_denso888.py
Complete project setup script for DENSO888
Creates entire project structure and all required files
"""

import os
import sys
import shutil
from pathlib import Path


def create_project_structure():
    """Create complete DENSO888 project structure"""

    # Project structure
    structure = {
        "config": ["__init__.py", "settings.py", "database.py", "environment.py"],
        "core": [
            "__init__.py",
            "excel_handler.py",
            "database_manager.py",
            "mock_generator.py",
            "data_processor.py",
        ],
        "gui": ["__init__.py", "main_window.py"],
        "gui/components": [
            "__init__.py",
            "header.py",
            "data_source_tab.py",
            "database_tab.py",
            "processing_tab.py",
            "logs_tab.py",
        ],
        "gui/styles": ["__init__.py", "theme.py"],
        "gui/utils": ["__init__.py", "dialogs.py", "validators.py", "helpers.py"],
        "utils": [
            "__init__.py",
            "logger.py",
            "error_handler.py",
            "settings_manager.py",
            "file_utils.py",
        ],
        "assets/icons": [],
        "assets/samples": [],
        "tests": ["__init__.py", "test_core.py", "test_gui.py", "test_integration.py"],
        "logs": [],
        "dist": [],
    }

    print("🏗️ Creating DENSO888 project structure...")

    # Create directories and files
    for folder, files in structure.items():
        Path(folder).mkdir(parents=True, exist_ok=True)
        print(f"  📁 {folder}/")

        for file in files:
            file_path = Path(folder) / file
            if not file_path.exists():
                file_path.touch()
                print(f"    📄 {file}")


def create_main_files():
    """Create main project files"""

    files_content = {
        # Main entry point
        "main.py": '''#!/usr/bin/env python3
"""
main.py - DENSO888 Application Entry Point
Created by เฮียตอมจัดหั้ย!!!
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def setup_environment():
    """Setup application environment"""
    required_dirs = [
        project_root / "logs",
        project_root / "assets" / "icons", 
        project_root / "assets" / "samples"
    ]
    
    for directory in required_dirs:
        directory.mkdir(parents=True, exist_ok=True)
    
    # Load .env if available
    try:
        from dotenv import load_dotenv
        env_file = project_root / ".env"
        if env_file.exists():
            load_dotenv(env_file)
    except ImportError:
        pass

def main():
    """Main application entry point"""
    print("🏭 DENSO888 - Excel to SQL GUI Application")
    print("   by เฮียตอมจัดหั้ย!!!")
    print("=" * 50)
    
    try:
        setup_environment()
        
        from gui.main_window import DENSO888MainWindow
        app = DENSO888MainWindow()
        app.run()
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Please install required packages: pip install -r requirements.txt")
        input("Press Enter to exit...")
        
    except Exception as e:
        print(f"❌ Critical Error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
''',
        # Requirements
        "requirements.txt": """# Core Dependencies
pandas>=2.0.0
sqlalchemy>=2.0.0
pyodbc>=4.0.39
openpyxl>=3.1.0
python-dotenv>=1.0.0
tqdm>=4.65.0

# GUI Dependencies
Pillow>=10.0.0

# Build Dependencies
pyinstaller>=5.10.0

# Development Dependencies (Optional)
pytest>=7.0.0
black>=23.0.0
""",
        # Environment template
        ".env.example": """# SQL Server Configuration
DB_HOST=localhost
DB_NAME=excel_to_db
DB_USER=sa
DB_PASSWORD=your_password
DB_DRIVER=ODBC Driver 17 for SQL Server

# Pool Settings
POOL_SIZE=5
MAX_OVERFLOW=10
POOL_TIMEOUT=30
POOL_RECYCLE=3600

# Processing Settings
BATCH_SIZE=1000
MAX_WORKERS=4
CHUNK_SIZE=5000

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/denso888.log
""",
        # Updated gitignore
        ".gitignore": """# Python
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

# PyInstaller
*.manifest
*.spec

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# DENSO888 specific
logs/*.log
assets/samples/*.xlsx
assets/samples/*.xls
*.tmp
*.temp
*.db

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Build output
dist/
build/
""",
        # Package init files with imports
        "config/__init__.py": '''"""
DENSO888 Configuration Package
"""

from .settings import get_config, AppConfig, DatabaseConfig, ProcessingConfig
from .environment import ensure_environment

__all__ = ['get_config', 'AppConfig', 'DatabaseConfig', 'ProcessingConfig', 'ensure_environment']
''',
        "core/__init__.py": '''"""
DENSO888 Core Business Logic Package
"""

from .excel_handler import ExcelHandler, ExcelReader, DataCleaner, TypeDetector
from .database_manager import DatabaseManager
from .mock_generator import MockDataGenerator, MockDataTemplates
from .data_processor import DataProcessor

__all__ = [
    'ExcelHandler', 'ExcelReader', 'DataCleaner', 'TypeDetector',
    'DatabaseManager', 'MockDataGenerator', 'MockDataTemplates',
    'DataProcessor'
]
''',
        "gui/__init__.py": '''"""
DENSO888 GUI Package
"""

from .main_window import DENSO888MainWindow

__all__ = ['DENSO888MainWindow']
''',
        "utils/__init__.py": '''"""
DENSO888 Utilities Package
"""

from .logger import setup_gui_logger, get_logger
from .error_handler import setup_error_handling
from .settings_manager import SettingsManager
from .file_utils import FileUtils

__all__ = ['setup_gui_logger', 'get_logger', 'setup_error_handling', 'SettingsManager', 'FileUtils']
''',
        # Simple README
        "README.md": """# 🏭 DENSO888 - Excel to SQL GUI Application

**Desktop Application สำหรับนำเข้าข้อมูล Excel เข้าสู่ฐานข้อมูล SQL Server หรือ SQLite**

Created by **เฮียตอมจัดหั้ย!!!** 🚀

## ✨ Features

✅ **Mock data generation** (100 - 50,000 rows)  
✅ **Excel file import** (.xlsx, .xls)  
✅ **SQL Server + SQLite** support with auto-fallback  
✅ **Real-time progress** tracking  
✅ **Modern GUI** interface  
✅ **One-click .exe** building  

## 🚀 Quick Start

### Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

### Build Production
```bash
# Create .exe
python build.py

# Install from dist/
INSTALL_DENSO888.bat
```

## 📁 Project Structure

```
denso888-excel-to-sql/
├── main.py              # Entry point
├── config/              # Configuration
├── core/                # Business logic  
├── gui/                 # GUI components
├── utils/               # Utilities
├── assets/              # Static files
└── tests/               # Test suite
```

## 🔧 Requirements

- Python 3.8+
- ODBC Driver 17 for SQL Server (for SQL Server connections)
- Windows 10/11 (for .exe)

## 📞 Support

Check logs in `logs/denso888.log` for troubleshooting.
""",
    }

    print("\n📄 Creating main project files...")

    for filename, content in files_content.items():
        file_path = Path(filename)

        # Create parent directory if needed
        if file_path.parent != Path("."):
            file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"  ✅ {filename}")


def cleanup_old_files():
    """Remove old files that are being replaced"""

    old_files = [
        "excel_to_ssms.py",
        "database.py",
        "data_cleaner.py",
        "excel_reader.py",
        "type_detector.py",
        "table_creator.py",
        "test_system.py",
        "config.py",
    ]

    print("\n🗑️ Cleaning up old files...")

    for old_file in old_files:
        file_path = Path(old_file)
        if file_path.exists():
            # Create backup before deletion
            backup_path = Path(f"{old_file}.backup")
            shutil.copy2(file_path, backup_path)
            file_path.unlink()
            print(f"  🔄 {old_file} → {old_file}.backup")
        else:
            print(f"  ⏭️ {old_file} (not found)")


def move_existing_files():
    """Move existing files to new locations"""

    moves = [
        ("sample_data_100.xlsx", "assets/samples/sample_data_100.xlsx"),
        ("excel_data_fallback.db", "assets/samples/excel_data_fallback.db"),
        (".env_working", ".env"),
    ]

    print("\n📦 Moving existing files...")

    for src, dst in moves:
        src_path = Path(src)
        dst_path = Path(dst)

        if src_path.exists():
            # Create destination directory
            dst_path.parent.mkdir(parents=True, exist_ok=True)

            # Move file
            shutil.move(str(src_path), str(dst_path))
            print(f"  📋 {src} → {dst}")
        else:
            print(f"  ⏭️ {src} (not found)")


def create_placeholder_files():
    """Create placeholder files for missing components"""

    placeholders = {
        "config/environment.py": '''"""Environment setup utilities"""

import os
from pathlib import Path

def ensure_environment():
    """Ensure application environment is ready"""
    # Create required directories
    required_dirs = ["logs", "assets/icons", "assets/samples", "temp"]
    
    for dir_name in required_dirs:
        Path(dir_name).mkdir(parents=True, exist_ok=True)
    
    print("✅ Environment ready")
''',
        "utils/file_utils.py": '''"""File operation utilities"""

from pathlib import Path
from typing import List, Optional

class FileUtils:
    """File operation utilities"""
    
    @staticmethod
    def get_excel_files(directory: str) -> List[Path]:
        """Get all Excel files in directory"""
        path = Path(directory)
        if not path.exists():
            return []
        
        excel_files = []
        excel_files.extend(path.glob("*.xlsx"))
        excel_files.extend(path.glob("*.xls"))
        
        return sorted(excel_files)
    
    @staticmethod
    def ensure_directory(directory: str) -> Path:
        """Ensure directory exists"""
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        return path
''',
        "utils/error_handler.py": '''"""Global error handling"""

import sys
import traceback
import logging

logger = logging.getLogger(__name__)

def setup_error_handling():
    """Setup global error handling"""
    
    def handle_exception(exc_type, exc_value, exc_traceback):
        """Global exception handler"""
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
        
        # Show user-friendly error for GUI
        try:
            import tkinter.messagebox as messagebox
            error_msg = f"เกิดข้อผิดพลาดร้ายแรง:\\n{exc_type.__name__}: {exc_value}"
            messagebox.showerror("ข้อผิดพลาด", error_msg)
        except:
            pass
    
    sys.excepthook = handle_exception
''',
        "tests/test_core.py": '''"""Core functionality tests"""

import unittest
import pandas as pd
from pathlib import Path

class TestCoreComponents(unittest.TestCase):
    """Test core business logic"""
    
    def setUp(self):
        """Test setup"""
        self.test_data = pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['Test1', 'Test2', 'Test3'],
            'value': [100, 200, 300]
        })
    
    def test_mock_data_generation(self):
        """Test mock data generation"""
        try:
            from core.mock_generator import MockDataGenerator
            
            # Test employee data generation
            df = MockDataGenerator.generate_employee_data(100)
            
            self.assertEqual(len(df), 100)
            self.assertIn('employee_id', df.columns)
            self.assertIn('first_name', df.columns)
            
        except ImportError:
            self.skipTest("Mock generator not implemented yet")
    
    def test_excel_handler(self):
        """Test Excel handling"""
        try:
            from core.excel_handler import DataCleaner
            
            cleaner = DataCleaner()
            cleaned_df = cleaner.clean_dataframe(self.test_data)
            
            self.assertIsNotNone(cleaned_df)
            
        except ImportError:
            self.skipTest("Excel handler not implemented yet")

if __name__ == '__main__':
    unittest.main()
''',
    }

    print("\n📝 Creating placeholder files...")

    for filename, content in placeholders.items():
        file_path = Path(filename)

        if not file_path.exists():
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"  📄 {filename}")


def main():
    """Main setup function"""
    print("🏭 DENSO888 Complete Project Setup")
    print("   by เฮียตอมจัดหั้ย!!!")
    print("=" * 50)

    try:
        # Step 1: Create project structure
        create_project_structure()

        # Step 2: Create main files
        create_main_files()

        # Step 3: Move existing files
        move_existing_files()

        # Step 4: Create placeholders
        create_placeholder_files()

        # Step 5: Cleanup (optional)
        response = input("\n❓ ต้องการลบไฟล์เก่าหรือไม่? (y/N): ")
        if response.lower() == "y":
            cleanup_old_files()

        # Success summary
        print("\n" + "=" * 50)
        print("🎉 Setup เสร็จสิ้น!")
        print("=" * 50)
        print("📂 โครงสร้างโปรเจคพร้อมใช้งาน")
        print("📄 ไฟล์หลักครบถ้วน")
        print("📦 Package structure พร้อม")
        print()
        print("🚀 ขั้นตอนต่อไป:")
        print("1. pip install -r requirements.txt")
        print("2. python main.py (ทดสอบ)")
        print("3. สร้าง GUI components ตาม checklist")
        print("4. python build.py (สร้าง .exe)")

        return True

    except Exception as e:
        print(f"\n❌ Setup ล้มเหลว: {e}")
        return False


if __name__ == "__main__":
    success = main()

    if not success:
        input("\nกด Enter เพื่อปิด...")
        sys.exit(1)
    else:
        input("\n✅ Setup สำเร็จ! กด Enter เพื่อปิด...")
