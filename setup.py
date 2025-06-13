#!/usr/bin/env python3
"""
Quick setup script for DENSO888 development environment
"""

import os
import sys
from pathlib import Path


def create_directories():
    """Create required directories"""
    dirs = [
        "logs",
        "assets/icons",
        "assets/samples",
        "config",
        "core",
        "gui",
        "utils",
        "tests",
    ]

    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"📁 {dir_path}/")


def create_missing_files():
    """Create missing essential files"""

    # Missing utility files
    files = {
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
        "config/environment.py": '''"""Environment setup utilities"""
import os
from pathlib import Path

def ensure_environment():
    """Ensure application environment is ready"""
    required_dirs = ["logs", "assets/icons", "assets/samples"]
    for dir_name in required_dirs:
        Path(dir_name).mkdir(parents=True, exist_ok=True)
    print("✅ Environment ready")
''',
        "check_env.py": '''"""Quick environment check"""
import sys

def check_tcl():
    try:
        import tkinter
        root = tkinter.Tk()
        root.withdraw()
        root.destroy()
        return True
    except Exception as e:
        print(f"❌ Tkinter error: {e}")
        return False

def main():
    if not check_tcl():
        print("❌ GUI environment not available")
        sys.exit(1)
    print("✅ Environment check passed")

if __name__ == "__main__":
    main()
''',
        "run.bat": """@echo off
echo Starting DENSO888...
python main.py
if errorlevel 1 (
    echo Failed to start application
    pause
)
""",
        "setup.bat": """@echo off
echo Setting up DENSO888...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo Setup complete!
pause
""",
    }

    for file_path, content in files.items():
        path = Path(file_path)
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"📄 {file_path}")


def main():
    """Setup main function"""
    print("🏭 DENSO888 Quick Setup")
    print("=" * 30)

    print("\n📁 Creating directories...")
    create_directories()

    print("\n📄 Creating missing files...")
    create_missing_files()

    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. pip install -r requirements.txt")
    print("2. python main.py")
    print("3. python build.py (for .exe)")


if __name__ == "__main__":
    main()
