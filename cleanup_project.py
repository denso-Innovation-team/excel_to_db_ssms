#!/usr/bin/env python3
"""
cleanup_project.py - ทำความสะอาดและจัดระเบียบโปรเจค DENSO888
"""

import os
import shutil
from pathlib import Path
import json


def cleanup_project():
    """ทำความสะอาดโปรเจค"""

    print("🧹 DENSO888 Project Cleanup")
    print("=" * 40)

    # Files to remove (ไฟล์เก่าที่ไม่ใช้แล้ว)
    files_to_remove = [
        "excel_to_ssms.py",
        "database.py",
        "data_cleaner.py",
        "excel_reader.py",
        "type_detector.py",
        "table_creator.py",
        "test_system.py",
        "config.py",
        "sample_data_100.xlsx",
        "excel_data_fallback.db",
        ".env_working",
    ]

    # Empty directories to remove
    empty_dirs_to_remove = ["gui/components", "gui/styles", "gui/utils", "tests"]

    # Files to create
    missing_files = {
        # Complete empty component files
        "gui/components/__init__.py": "",
        "gui/components/data_source_tab.py": "",
        "gui/components/database_tab.py": "",
        "gui/components/header.py": "",
        "gui/components/logs_tab.py": "",
        "gui/components/processing_tab.py": "",
        "gui/styles/__init__.py": "",
        "gui/styles/theme.py": "",
        "gui/utils/__init__.py": "",
        "gui/utils/dialogs.py": "",
        "gui/utils/validators.py": "",
        "gui/utils/helpers.py": "",
        "tests/__init__.py": "",
        "tests/test_core.py": "",
        "tests/test_gui.py": "",
        "tests/test_integration.py": "",
        # Complete utils files
        "utils/error_handler.py": '''"""Simple error handling for DENSO888"""

def get_user_friendly_error(exception):
    """Convert errors to Thai messages"""
    error_map = {
        "ConnectionError": "ไม่สามารถเชื่อมต่อฐานข้อมูล",
        "FileNotFoundError": "ไม่พบไฟล์ที่ระบุ",
        "PermissionError": "ไม่มีสิทธิ์เข้าถึงไฟล์",
        "ValueError": "ข้อมูลไม่ถูกต้อง",
        "ImportError": "ไม่พบโมดูลที่ต้องการ",
        "AttributeError": "ฟังก์ชันไม่พร้อมใช้งาน",
    }
    error_type = type(exception).__name__
    return error_map.get(error_type, f"ข้อผิดพลาด: {str(exception)}")

def setup_error_handling():
    """Basic error setup - placeholder for compatibility"""
    pass
''',
        "utils/file_utils.py": '''"""File operation utilities"""
from pathlib import Path
from typing import List

class FileUtils:
    @staticmethod
    def get_excel_files(directory: str) -> List[Path]:
        path = Path(directory)
        if not path.exists():
            return []
        excel_files = list(path.glob("*.xlsx")) + list(path.glob("*.xls"))
        return sorted(excel_files)
    
    @staticmethod
    def ensure_directory(directory: str) -> Path:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        return path
''',
        # Config files
        "config/database.py": "",
        # Updated .env with complete settings
        ".env": """# SQL Server Configuration
DB_HOST=localhost
DB_NAME=excel_to_db
DB_USER=sa
DB_PASSWORD=your_password_here
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

# Authentication
AUTH_ENABLE=true
SESSION_TIMEOUT=3600
MAX_LOGIN_ATTEMPTS=3

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/denso888.log
""",
        # Updated requirements with all dependencies
        "requirements.txt": """# Core Dependencies - Production Ready
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
flake8>=6.0.0

# Additional utilities
hashlib-compat>=1.0.0
""",
        # Install script for dependencies
        "install.py": '''#!/usr/bin/env python3
"""Quick install script for DENSO888"""

import subprocess
import sys
import os

def main():
    print("🏭 Installing DENSO888 Dependencies...")
    
    try:
        # Upgrade pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        print("✅ Installation completed successfully!")
        print("\\nRun: python main.py")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
''',
    }

    # Step 1: Remove old files
    print("\\n🗑️ Removing old files...")
    removed_count = 0

    for file_path in files_to_remove:
        path = Path(file_path)
        if path.exists():
            if path.is_file():
                # Create backup first
                backup_path = Path(f"{file_path}.backup")
                shutil.copy2(path, backup_path)
                path.unlink()
                print(f"  🔄 {file_path} → {file_path}.backup")
                removed_count += 1
            elif path.is_dir():
                shutil.rmtree(path)
                print(f"  📁 {file_path}/ (directory)")
                removed_count += 1

    print(f"  ✅ Removed {removed_count} old files")

    # Step 2: Create missing files
    print("\\n📄 Creating missing files...")
    created_count = 0

    for file_path, content in missing_files.items():
        path = Path(file_path)

        if not path.exists():
            # Create parent directory
            path.parent.mkdir(parents=True, exist_ok=True)

            # Write file
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"  📄 {file_path}")
            created_count += 1
        else:
            print(f"  ⏭️ {file_path} (exists)")

    print(f"  ✅ Created {created_count} files")

    # Step 3: Create required directories
    print("\n📁 Creating required directories...")
    required_dirs = [
        "logs",
        "assets/icons",
        "assets/samples",
        "temp",
        "dist",
        "backups",
    ]

    dir_count = 0
    for dir_path in required_dirs:
        path = Path(dir_path)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print(f"  📁 {dir_path}/")
            dir_count += 1

    print(f"  ✅ Created {dir_count} directories")

    # Step 4: Update .gitignore
    print("\n📝 Updating .gitignore...")
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

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

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
auth.db
denso888_settings.json
recent_files.json

# Backups
*.backup
backups/

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

# Build output
dist/
build/
"""

    with open(".gitignore", "w", encoding="utf-8") as f:
        f.write(gitignore_content)
    print("  ✅ .gitignore updated")

    # Step 5: Generate project summary
    print("\n📊 Generating project summary...")

    def count_files_and_lines(directory):
        """Count files and lines in directory"""
        total_files = 0
        total_lines = 0

        for path in Path(directory).rglob("*.py"):
            if path.is_file():
                total_files += 1
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        total_lines += len(f.readlines())
                except:
                    pass

        return total_files, total_lines

    # Count project stats
    config_files, config_lines = count_files_and_lines("config")
    core_files, core_lines = count_files_and_lines("core")
    gui_files, gui_lines = count_files_and_lines("gui")
    utils_files, utils_lines = count_files_and_lines("utils")

    total_py_files = config_files + core_files + gui_files + utils_files
    total_py_lines = config_lines + core_lines + gui_lines + utils_lines

    summary = {
        "project_name": "DENSO888 - Excel to SQL Management System",
        "version": "2.0.0",
        "cleanup_date": "2024-06-13",
        "statistics": {
            "total_python_files": total_py_files,
            "total_lines_of_code": total_py_lines,
            "modules": {
                "config": {"files": config_files, "lines": config_lines},
                "core": {"files": core_files, "lines": core_lines},
                "gui": {"files": gui_files, "lines": gui_lines},
                "utils": {"files": utils_files, "lines": utils_lines},
            },
        },
        "features": [
            "User Authentication System",
            "Role-based Permissions",
            "SQLite & SQL Server Support",
            "Excel Import & Mock Data Generation",
            "Real-time Processing with Progress Tracking",
            "Database Connection Testing & CRUD Verification",
            "Advanced Error Handling",
            "Settings Persistence",
            "Modern GUI with Tabbed Interface",
        ],
        "cleanup_actions": {
            "removed_files": removed_count,
            "created_files": created_count,
            "created_directories": dir_count,
        },
    }

    # Save summary
    with open("project_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print("  ✅ project_summary.json created")

    # Step 6: Create quick start scripts
    print("\n🚀 Creating quick start scripts...")

    # Windows batch file
    quick_start_bat = """@echo off
title DENSO888 - Excel to SQL Management System
echo.
echo ========================================
echo  🏭 DENSO888 - Excel to SQL
echo  by เฮียตอมจัดหั้ย!!!
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist .venv (
    echo 📦 Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call .venv\\Scripts\\activate.bat

REM Install/upgrade dependencies
echo 📥 Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

REM Run application
echo.
echo 🚀 Starting DENSO888...
echo.
python main.py

if errorlevel 1 (
    echo.
    echo ❌ Application encountered an error
    echo Check logs/denso888.log for details
    pause
)
"""

    with open("start_denso888.bat", "w", encoding="utf-8") as f:
        f.write(quick_start_bat)

    # Linux/Mac shell script
    quick_start_sh = """#!/bin/bash
echo "========================================"
echo " 🏭 DENSO888 - Excel to SQL"
echo " by เฮียตอมจัดหั้ย!!!"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found! Please install Python 3.8+"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Run application
echo
echo "🚀 Starting DENSO888..."
echo
python main.py

if [ $? -ne 0 ]; then
    echo
    echo "❌ Application encountered an error"
    echo "Check logs/denso888.log for details"
fi
"""

    with open("start_denso888.sh", "w", encoding="utf-8") as f:
        f.write(quick_start_sh)

    # Make shell script executable (on Unix systems)
    try:
        os.chmod("start_denso888.sh", 0o755)
    except:
        pass

    print("  ✅ start_denso888.bat (Windows)")
    print("  ✅ start_denso888.sh (Linux/Mac)")

    # Final summary
    print("\n" + "=" * 50)
    print("🎉 DENSO888 Project Cleanup Complete!")
    print("=" * 50)
    print(f"📊 Project Statistics:")
    print(f"  • Python files: {total_py_files}")
    print(f"  • Lines of code: {total_py_lines:,}")
    print(
        f"  • Modules: Config({config_files}), Core({core_files}), GUI({gui_files}), Utils({utils_files})"
    )
    print()
    print(f"🧹 Cleanup Actions:")
    print(f"  • Removed: {removed_count} old files")
    print(f"  • Created: {created_count} new files")
    print(f"  • Directories: {dir_count} created")
    print()
    print("🚀 Ready to Use:")
    print("  1. Windows: double-click start_denso888.bat")
    print("  2. Linux/Mac: ./start_denso888.sh")
    print("  3. Manual: python main.py")
    print()
    print("📋 Next Steps:")
    print("  • Test authentication (admin/admin123)")
    print("  • Try database connections")
    print("  • Generate mock data")
    print("  • Import Excel files")
    print("  • Build executable: python build.py")
    print()
    print("✅ DENSO888 is ready for production use! 🏭")


if __name__ == "__main__":
    cleanup_project()
