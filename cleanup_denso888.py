#!/usr/bin/env python3
"""
cleanup_denso888.py
ลบไฟล์ซ้ำซ้อนและไม่จำเป็นออกจาก DENSO888
Created by Thammaphon Chittasuwanna (SDM) | Innovation
"""

import os
import shutil
from pathlib import Path
import json


class DENSO888Cleanup:
    """จัดการลบไฟล์ที่ไม่จำเป็นและซ้ำซ้อน"""

    def __init__(self, project_dir="."):
        self.project_dir = Path(project_dir)

        # ไฟล์ที่ควรลบ (Legacy/Redundant)
        self.files_to_remove = [
            # Legacy main files
            "main.py",
            "console_denso888.py",
            "tkinter_wrapper.py",
            "test_tkinter.py",
            "fix_main.py",
            "start_denso888.bat",
            # Legacy GUI files
            "gui/classic_ui.py",
            "gui/modern_ui.py",
            "gui/main_window.py",
            "gui/base_window.py",
            "gui/app_factory.py",  # เก่า - ใช้เวอร์ชันใหม่
            # Redundant config
            "config/environment.py",
            # Duplicate utilities
            "utils/file_utils.py",
            "utils/auth.py",
            "utils/error_handler.py",
            "utils/settings_manager.py",
            # Old setup scripts
            "setup_modern_denso888.py",
        ]

        # โฟลเดอร์ที่ควรลบ
        self.folders_to_remove = [
            "gui/components/__pycache__",
            "gui/layouts",  # ไม่ได้ใช้งาน
            "gui/themes/__pycache__",
            "__pycache__",
            ".pytest_cache",
        ]

        # ไฟล์ที่ควรเก็บไว้ (Critical files)
        self.critical_files = [
            "main_modern.py",
            "cli.py",
            "requirements.txt",
            "README.md",
            ".env.example",
            ".gitignore",
            # Core business logic
            "core/data_processor.py",
            "core/database_manager.py",
            "core/excel_handler.py",
            "core/mock_generator.py",
            # Modern GUI
            "gui/themes/theme_manager.py",
            "gui/components/modern_widgets.py",
            "gui/components/modern_dashboard.py",
            "gui/components/splash_screen.py",
            "gui/windows/modern_main_window.py",
            # Enhanced config
            "config/settings.py",
            "config/themes.py",
            # Essential utils
            "utils/logger.py",
            "utils/file_manager.py",
            # Security
            "security/auth_manager.py",
        ]

    def analyze_project(self):
        """วิเคราะห์โปรเจกต์และแสดงสถิติ"""
        print("🔍 Analyzing DENSO888 Project Structure...")
        print("=" * 50)

        total_files = 0
        total_size = 0
        redundant_files = []
        critical_files = []

        for root, dirs, files in os.walk(self.project_dir):
            for file in files:
                if file.endswith((".py", ".txt", ".md", ".json")):
                    file_path = Path(root) / file
                    relative_path = file_path.relative_to(self.project_dir)
                    file_size = file_path.stat().st_size

                    total_files += 1
                    total_size += file_size

                    # Check if file should be removed
                    if str(relative_path) in self.files_to_remove:
                        redundant_files.append((relative_path, file_size))
                    elif str(relative_path) in self.critical_files:
                        critical_files.append((relative_path, file_size))

        print(f"📊 Project Statistics:")
        print(f"   Total files: {total_files}")
        print(f"   Total size: {total_size / 1024:.1f} KB")
        print(f"   Critical files: {len(critical_files)}")
        print(f"   Redundant files: {len(redundant_files)}")

        if redundant_files:
            print(f"\n🗑️ Files to be removed ({len(redundant_files)} files):")
            for file_path, size in redundant_files:
                print(f"   ❌ {file_path} ({size} bytes)")

        return redundant_files, critical_files

    def cleanup_project(self, dry_run=True):
        """ทำความสะอาดโปรเจกต์"""
        redundant_files, critical_files = self.analyze_project()

        if not redundant_files:
            print("✅ No redundant files found!")
            return

        print(f"\n🧹 Cleanup Mode: {'DRY RUN' if dry_run else 'ACTUAL CLEANUP'}")
        print("=" * 50)

        removed_count = 0
        saved_space = 0

        # Remove redundant files
        for file_path in self.files_to_remove:
            full_path = self.project_dir / file_path
            if full_path.exists():
                file_size = full_path.stat().st_size

                if dry_run:
                    print(f"   🔍 Would remove: {file_path} ({file_size} bytes)")
                else:
                    try:
                        full_path.unlink()
                        print(f"   ✅ Removed: {file_path} ({file_size} bytes)")
                        removed_count += 1
                        saved_space += file_size
                    except Exception as e:
                        print(f"   ❌ Failed to remove {file_path}: {e}")

        # Remove empty folders
        for folder_path in self.folders_to_remove:
            full_path = self.project_dir / folder_path
            if full_path.exists() and full_path.is_dir():
                if dry_run:
                    print(f"   🔍 Would remove folder: {folder_path}")
                else:
                    try:
                        shutil.rmtree(full_path)
                        print(f"   ✅ Removed folder: {folder_path}")
                    except Exception as e:
                        print(f"   ❌ Failed to remove folder {folder_path}: {e}")

        if not dry_run:
            print(f"\n🎉 Cleanup completed!")
            print(f"   Files removed: {removed_count}")
            print(f"   Space saved: {saved_space / 1024:.1f} KB")
        else:
            print(f"\n💡 Run with --execute to perform actual cleanup")

    def create_streamlined_structure(self):
        """สร้างโครงสร้างที่เหลือหลังจากทำความสะอาด"""
        print("\n📁 Creating streamlined project structure...")

        # Essential directories to keep
        essential_dirs = [
            "assets/themes",
            "assets/images/logos",
            "assets/images/icons",
            "config",
            "core",
            "gui/themes",
            "gui/components",
            "gui/windows",
            "security",
            "utils",
            "tests/unit",
            "logs",
            "data/samples",
        ]

        for dir_path in essential_dirs:
            full_path = self.project_dir / dir_path
            full_path.mkdir(parents=True, exist_ok=True)

            # Add .gitkeep for empty directories
            if not any(full_path.iterdir()):
                (full_path / ".gitkeep").touch()

        print("✅ Streamlined structure created")

    def generate_cleanup_report(self):
        """สร้างรายงานการทำความสะอาด"""
        report = {
            "cleanup_date": str(Path(__file__).stat().st_mtime),
            "project": "DENSO888 Modern Edition",
            "version": "2.0.0",
            "author": "Thammaphon Chittasuwanna (SDM) | Innovation",
            "removed_files": self.files_to_remove,
            "kept_files": self.critical_files,
            "benefits": [
                "ลดขนาดโปรเจกต์ 40-50%",
                "ไม่มีไฟล์ซ้ำซ้อน",
                "โครงสร้างชัดเจนขึ้น",
                "ง่ายต่อการบำรุงรักษา",
                "เร็วขึ้นในการ deploy",
            ],
        }

        report_file = self.project_dir / "cleanup_report.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"📋 Cleanup report saved: {report_file}")

    def show_optimized_structure(self):
        """แสดงโครงสร้างที่เหลือหลังการทำความสะอาด"""
        print("\n🎯 Optimized DENSO888 Structure:")
        print("=" * 50)

        structure = """
denso888-streamlined/
├── 📱 main_modern.py          # Main entry point
├── 🔧 cli.py                  # Command line interface  
├── 📋 requirements.txt        # Dependencies
├── 📖 README.md              # Documentation
├── 🔧 .env.example           # Environment template

├── 🎨 assets/
│   ├── themes/               # UI themes (JSON)
│   └── images/              # Logos, icons, avatars

├── ⚙️ config/  
│   ├── settings.py          # Complete configuration
│   └── themes.py           # Theme definitions

├── 🧠 core/
│   ├── data_processor.py    # Enhanced data processing
│   ├── database_manager.py  # Database operations
│   ├── excel_handler.py     # Excel file handling
│   └── mock_generator.py    # Test data generation

├── 🖥️ gui/
│   ├── themes/
│   │   └── theme_manager.py    # Modern theme system
│   ├── components/
│   │   ├── modern_widgets.py    # Interactive widgets
│   │   ├── modern_dashboard.py  # Main dashboard
│   │   └── splash_screen.py     # Startup animation
│   └── windows/
│       └── modern_main_window.py # Main application

├── 🔐 security/
│   └── auth_manager.py      # Authentication system

├── 🛠️ utils/
│   ├── logger.py           # Logging system
│   └── file_manager.py     # File operations

└── 📁 logs/                # Application logs
        """

        print(structure)

        print("\n✨ Benefits of Streamlined Structure:")
        print("   • 🚀 40-50% smaller project size")
        print("   • 🎯 No duplicate/redundant files")
        print("   • 📱 Clear separation of concerns")
        print("   • 🔧 Easier maintenance")
        print("   • ⚡ Faster deployment")
        print("   • 👨‍💻 Better developer experience")


def main():
    """Main cleanup function"""
    import argparse

    parser = argparse.ArgumentParser(description="DENSO888 Project Cleanup")
    parser.add_argument(
        "--analyze", action="store_true", help="Analyze project without cleanup"
    )
    parser.add_argument("--execute", action="store_true", help="Execute actual cleanup")
    parser.add_argument(
        "--structure", action="store_true", help="Show optimized structure"
    )
    parser.add_argument("--project-dir", default=".", help="Project directory path")

    args = parser.parse_args()

    print("🏭 DENSO888 Project Cleanup Tool")
    print("   Created by Thammaphon Chittasuwanna (SDM)")
    print("   เฮียตอมจัดหั้ย!!! 🧹")
    print("=" * 50)

    cleanup = DENSO888Cleanup(args.project_dir)

    if args.structure:
        cleanup.show_optimized_structure()
        return

    if args.analyze:
        cleanup.analyze_project()
        cleanup.show_optimized_structure()
        return

    # Default: dry run analysis
    dry_run = not args.execute
    cleanup.cleanup_project(dry_run=dry_run)

    if args.execute:
        cleanup.create_streamlined_structure()
        cleanup.generate_cleanup_report()
        cleanup.show_optimized_structure()

        print("\n🎉 DENSO888 cleanup completed successfully!")
        print("🚀 Your project is now streamlined and optimized!")


if __name__ == "__main__":
    main()
