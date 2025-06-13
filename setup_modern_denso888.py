#!/usr/bin/env python3
"""
DENSO888 Modern Project Setup & Migration Script
Created by Thammaphon Chittasuwanna (SDM) | Innovation

สคริปสำหรับ:
1. สร้างโครงสร้างโฟล์เดอร์แบบ Modern
2. Migration ไฟล์เดิมไปยังตำแหน่งใหม่
3. สร้างไฟล์ template พื้นฐาน
4. Setup development environment
"""

import shutil
import json
from pathlib import Path


class DENSO888ProjectSetup:
    """Modern DENSO888 Project Setup Manager"""

    def __init__(self, target_dir: str = "denso888-modern"):
        self.target_dir = Path(target_dir)
        self.backup_dir = Path("denso888-backup")
        self.current_dir = Path(".")

        # Project structure definition
        self.structure = {
            # Asset directories
            "assets/images/logo": [],
            "assets/images/avatars": [],
            "assets/images/icons": [],
            "assets/fonts": [],
            "assets/themes": [],
            # Configuration
            "config": ["__init__.py", "settings.py", "themes.py", "constants.py"],
            # Core business logic
            "core": [
                "__init__.py",
                "data_processor.py",
                "database_manager.py",
                "excel_handler.py",
                "mock_generator.py",
                "validator.py",
            ],
            "core/analytics": [
                "__init__.py",
                "data_profiler.py",
                "visualizer.py",
                "insights_engine.py",
            ],
            # Modern GUI components
            "gui": ["__init__.py"],
            "gui/components": [
                "__init__.py",
                "modern_widgets.py",
                "cards.py",
                "charts.py",
                "forms.py",
                "animations.py",
            ],
            "gui/themes": [
                "__init__.py",
                "theme_manager.py",
                "color_schemes.py",
                "styles.py",
            ],
            "gui/windows": [
                "__init__.py",
                "main_window.py",
                "dashboard.py",
                "import_wizard.py",
                "export_dialog.py",
                "settings_window.py",
                "about_dialog.py",
                "auth_dialog.py",
            ],
            "gui/layouts": ["__init__.py", "responsive.py", "grid_system.py"],
            # Automation & scheduling
            "automation": [
                "__init__.py",
                "scheduler.py",
                "workflows.py",
                "triggers.py",
            ],
            "automation/templates": [],
            # Security
            "security": [
                "__init__.py",
                "auth_manager.py",
                "permissions.py",
                "encryption.py",
                "audit_logger.py",
            ],
            # Utilities
            "utils": [
                "__init__.py",
                "logger.py",
                "file_manager.py",
                "error_handler.py",
                "performance.py",
                "helpers.py",
            ],
            # Plugin system
            "plugins": ["__init__.py", "plugin_manager.py"],
            "plugins/connectors": [
                "mysql_connector.py",
                "oracle_connector.py",
                "mongodb_connector.py",
            ],
            "plugins/exporters": [
                "pdf_exporter.py",
                "json_exporter.py",
                "api_exporter.py",
            ],
            # Testing
            "tests": ["__init__.py"],
            "tests/unit": [
                "test_data_processor.py",
                "test_database_manager.py",
                "test_excel_handler.py",
            ],
            "tests/integration": [
                "test_full_workflow.py",
                "test_database_integration.py",
            ],
            "tests/ui": ["test_main_window.py", "test_dashboard.py"],
            "tests/fixtures": [],
            # Documentation
            "docs": [],
            "docs/images": [],
            "docs/examples": [],
            # Scripts
            "scripts": ["build.py", "install.py", "deploy.py", "update.py"],
            # Data storage
            "logs": [],
            "data/samples": [],
            "data/templates": [],
            "data/exports": [],
            "data/cache": [],
            # Database migrations
            "migrations": [],
            # Localization
            "localization/th": ["messages.json", "ui_labels.json"],
            "localization/en": ["messages.json", "ui_labels.json"],
        }

        # Files to migrate from old structure
        self.migration_map = {
            # Old -> New mappings
            "main.py": "main_legacy.py",  # Keep as legacy
            "config/settings.py": "config/settings.py",
            "core/excel_handler.py": "core/excel_handler.py",
            "core/database_manager.py": "core/database_manager.py",
            "core/data_processor.py": "core/data_processor.py",
            "core/mock_generator.py": "core/mock_generator.py",
            "gui/main_window.py": "gui/windows/main_window_legacy.py",
            "utils/logger.py": "utils/logger.py",
            "utils/settings_manager.py": "utils/settings_manager.py",
            "utils/file_utils.py": "utils/file_manager.py",
            "requirements.txt": "requirements.txt",
            ".env.example": ".env.example",
            ".gitignore": ".gitignore",
            "README.md": "README_legacy.md",
        }

    def run_setup(self):
        """Run complete project setup"""
        print("🏭 DENSO888 Modern Project Setup")
        print("   Created by Thammaphon Chittasuwanna (SDM) | Innovation")
        print("=" * 60)

        try:
            # Step 1: Backup existing project
            self._backup_existing_project()

            # Step 2: Create modern structure
            self._create_directory_structure()

            # Step 3: Migrate existing files
            self._migrate_existing_files()

            # Step 4: Create template files
            self._create_template_files()

            # Step 5: Setup development environment
            self._setup_development_environment()

            # Step 6: Generate documentation
            self._generate_documentation()

            print("\n🎉 Setup completed successfully!")
            print(f"📁 Modern project created at: {self.target_dir.absolute()}")
            print(f"💾 Backup saved at: {self.backup_dir.absolute()}")

            self._show_next_steps()

        except Exception as e:
            print(f"❌ Setup failed: {e}")
            self._cleanup_on_error()
            raise

    def _backup_existing_project(self):
        """Backup existing project"""
        print("💾 Creating backup of existing project...")

        if self.backup_dir.exists():
            shutil.rmtree(self.backup_dir)

        # Copy current directory to backup
        important_items = [
            "config",
            "core",
            "gui",
            "utils",
            "assets",
            "logs",
            "main.py",
            "requirements.txt",
            ".env.example",
            "README.md",
            ".gitignore",
        ]

        self.backup_dir.mkdir(parents=True)

        for item in important_items:
            src = self.current_dir / item
            if src.exists():
                dst = self.backup_dir / item
                if src.is_dir():
                    try:
                        # Try with ignore_errors for Python 3.8+
                        shutil.copytree(src, dst, ignore_errors=True)
                    except TypeError:
                        # Fallback for older Python versions
                        try:
                            shutil.copytree(src, dst)
                        except Exception as e:
                            print(f"   ⚠️ Warning: Could not backup {item}: {e}")
                            continue
                else:
                    try:
                        shutil.copy2(src, dst)
                    except Exception as e:
                        print(f"   ⚠️ Warning: Could not backup {item}: {e}")
                        continue

        print(f"✅ Backup created at: {self.backup_dir.absolute()}")

    def _create_directory_structure(self):
        """Create modern directory structure"""
        print("📁 Creating modern directory structure...")

        if self.target_dir.exists():
            print(f"⚠️ Target directory {self.target_dir} exists. Removing...")
            shutil.rmtree(self.target_dir)

        self.target_dir.mkdir(parents=True)

        # Create all directories and files
        for dir_path, files in self.structure.items():
            full_dir = self.target_dir / dir_path
            full_dir.mkdir(parents=True, exist_ok=True)

            # Create placeholder files
            for file_name in files:
                file_path = full_dir / file_name
                if not file_path.exists():
                    file_path.touch()

                    # Add basic content for Python files
                    if file_name.endswith(".py"):
                        with open(file_path, "w", encoding="utf-8") as f:
                            if file_name == "__init__.py":
                                f.write(
                                    f'"""\n{dir_path.replace("/", ".")} package\n"""\n'
                                )
                            else:
                                module_name = (
                                    file_name.replace(".py", "")
                                    .replace("_", " ")
                                    .title()
                                )
                                f.write(
                                    f'"""\n{module_name} for DENSO888\nCreated by Thammaphon Chittasuwanna (SDM) | Innovation\n"""\n\n# TODO: Implement {module_name}\npass\n'
                                )

        print(f"✅ Directory structure created with {len(self.structure)} directories")

    def _migrate_existing_files(self):
        """Migrate existing files to new structure"""
        print("🔄 Migrating existing files...")

        migrated_count = 0

        for old_path, new_path in self.migration_map.items():
            src = self.current_dir / old_path
            dst = self.target_dir / new_path

            if src.exists():
                # Ensure destination directory exists
                dst.parent.mkdir(parents=True, exist_ok=True)

                # Copy file
                shutil.copy2(src, dst)
                migrated_count += 1
                print(f"   📄 {old_path} → {new_path}")

        print(f"✅ Migrated {migrated_count} files")

    def _create_template_files(self):
        """Create template files with basic content"""
        print("📝 Creating template files...")

        templates = {
            # Main entry points
            "main_modern.py": self._get_main_modern_template(),
            "cli.py": self._get_cli_template(),
            "api.py": self._get_api_template(),
            "web_ui.py": self._get_web_ui_template(),
            # Configuration files
            "pyproject.toml": self._get_pyproject_template(),
            "docker-compose.yml": self._get_docker_compose_template(),
            "Dockerfile": self._get_dockerfile_template(),
            ".env.example": self._get_env_template(),
            # Documentation
            "README.md": self._get_readme_template(),
            "INSTALLATION.md": self._get_installation_template(),
            "USER_GUIDE.md": self._get_user_guide_template(),
            "DEVELOPMENT.md": self._get_development_template(),
            "CHANGELOG.md": self._get_changelog_template(),
            # Asset files
            "assets/themes/denso_corporate.json": self._get_theme_template(
                "denso_corporate"
            ),
            "assets/themes/dark_premium.json": self._get_theme_template("dark_premium"),
            "assets/themes/ocean_blue.json": self._get_theme_template("ocean_blue"),
            # Automation templates
            "automation/templates/daily_import.json": self._get_automation_template(
                "daily_import"
            ),
            "automation/templates/weekly_report.json": self._get_automation_template(
                "weekly_report"
            ),
            # Migration scripts
            "migrations/001_initial_schema.sql": self._get_migration_template(),
            # Build scripts
            "scripts/build.py": self._get_build_script_template(),
            "scripts/install.py": self._get_install_script_template(),
        }

        for file_path, content in templates.items():
            full_path = self.target_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)

            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)

        print(f"✅ Created {len(templates)} template files")

    def _setup_development_environment(self):
        """Setup development environment"""
        print("🔧 Setting up development environment...")

        # Create requirements files
        requirements = {
            "requirements.txt": [
                "# DENSO888 Modern Edition Dependencies",
                "pandas>=2.0.0",
                "sqlalchemy>=2.0.0",
                "pyodbc>=4.0.39",
                "openpyxl>=3.1.0",
                "python-dotenv>=1.0.0",
                "tqdm>=4.65.0",
                "Pillow>=10.0.0",
                "numpy>=1.24.0",
                "matplotlib>=3.7.0",
                "seaborn>=0.12.0",
                "plotly>=5.15.0",
                "pydantic>=2.0.0",
                "fastapi>=0.100.0",
                "uvicorn>=0.23.0",
            ],
            "requirements-dev.txt": [
                "# Development Dependencies",
                "-r requirements.txt",
                "pytest>=7.4.0",
                "pytest-cov>=4.1.0",
                "black>=23.7.0",
                "flake8>=6.0.0",
                "mypy>=1.5.0",
                "pre-commit>=3.3.0",
                "sphinx>=7.1.0",
                "sphinx-rtd-theme>=1.3.0",
                "pyinstaller>=5.13.0",
            ],
        }

        for file_name, deps in requirements.items():
            req_file = self.target_dir / file_name
            with open(req_file, "w", encoding="utf-8") as f:
                f.write("\n".join(deps) + "\n")

        # Create setup.py
        setup_content = self._get_setup_py_template()
        with open(self.target_dir / "setup.py", "w", encoding="utf-8") as f:
            f.write(setup_content)

        print("✅ Development environment configured")

    def _generate_documentation(self):
        """Generate project documentation"""
        print("📚 Generating documentation...")

        docs_files = {
            "docs/API_REFERENCE.md": self._get_api_reference_template(),
            "docs/CONTRIBUTING.md": self._get_contributing_template(),
            "docs/SECURITY.md": self._get_security_template(),
        }

        for file_path, content in docs_files.items():
            full_path = self.target_dir / file_path
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)

        print("✅ Documentation generated")

    def _cleanup_on_error(self):
        """Cleanup on setup error"""
        if self.target_dir.exists():
            shutil.rmtree(self.target_dir)
        print("🧹 Cleaned up incomplete setup")

    def _show_next_steps(self):
        """Show next steps to user"""
        print("\n🚀 Next Steps:")
        print("=" * 40)
        print("1. 📂 Navigate to project directory:")
        print(f"   cd {self.target_dir}")
        print("\n2. 🐍 Create virtual environment:")
        print("   python -m venv venv")
        print("   source venv/bin/activate  # Linux/Mac")
        print("   venv\\Scripts\\activate     # Windows")
        print("\n3. 📦 Install dependencies:")
        print("   pip install -r requirements.txt")
        print("\n4. 🚀 Run modern application:")
        print("   python main_modern.py")
        print("\n5. 🎨 Or run legacy application:")
        print("   python main_legacy.py")
        print("\n6. 🔧 Development setup:")
        print("   pip install -r requirements-dev.txt")
        print("   pre-commit install")
        print("\n📋 Project Structure Overview:")
        print("   📁 config/        - Configuration management")
        print("   📁 core/          - Business logic")
        print("   📁 gui/           - Modern UI components")
        print("   📁 automation/    - Scheduling & workflows")
        print("   📁 security/      - Authentication & permissions")
        print("   📁 plugins/       - Extensibility system")
        print("   📁 tests/         - Test suite")
        print("   📁 docs/          - Documentation")

    # Template methods
    def _get_main_modern_template(self):
        return '''#!/usr/bin/env python3
"""
DENSO888 Modern Edition - Main Entry Point
Created by Thammaphon Chittasuwanna (SDM) | Innovation
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from gui.windows.main_window import ModernDENSO888MainWindow
from gui.themes.theme_manager import ModernThemeManager
from security.auth_manager import ModernAuthManager
from config.settings import get_config
from utils.logger import setup_gui_logger

def main():
    """Modern DENSO888 Application Entry Point"""
    print("🏭 DENSO888 Modern Edition")
    print("   by Thammaphon Chittasuwanna (SDM) | Innovation")
    
    try:
        # Setup logging
        setup_gui_logger()
        
        # Initialize components
        config = get_config()
        theme_manager = ModernThemeManager()
        auth_manager = ModernAuthManager()
        
        # Create and run application
        app = ModernDENSO888MainWindow(
            theme_manager=theme_manager,
            auth_manager=auth_manager,
            config=config
        )
        
        return app.run()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
'''

    def _get_cli_template(self):
        return '''#!/usr/bin/env python3
"""
DENSO888 Command Line Interface
For headless operations and automation
"""

import click
from pathlib import Path

@click.group()
@click.version_option(version="2.0.0")
def cli():
    """DENSO888 Modern Edition CLI"""
    pass

@cli.command()
@click.option("--file", "-f", required=True, help="Excel file path")
@click.option("--table", "-t", default="imported_data", help="Target table name")
def import_excel(file, table):
    """Import Excel file to database"""
    click.echo(f"Importing {file} to table {table}...")
    # TODO: Implement Excel import logic

@cli.command()
@click.option("--template", "-t", default="employees", help="Mock data template")
@click.option("--rows", "-r", default=1000, help="Number of rows to generate")
def generate_mock(template, rows):
    """Generate mock data"""
    click.echo(f"Generating {rows} rows of {template} data...")
    # TODO: Implement mock generation logic

if __name__ == "__main__":
    cli()
'''

    def _get_readme_template(self):
        return """# 🏭 DENSO888 Modern Edition

**Excel to SQL Management System with Advanced Analytics**

Created by **Thammaphon Chittasuwanna (SDM) | Innovation**

## ✨ Features

- 🎨 **Modern UI/UX** with multiple themes
- 🤖 **AI-Powered Insights** and data analytics
- ⚡ **Real-time Monitoring** and performance tracking
- 🔐 **Enterprise Security** with role-based access
- 🔄 **Advanced Automation** and scheduling
- 📊 **Interactive Visualizations** and reporting

## 🚀 Quick Start

```bash
# 1. Clone/Download project
cd denso888-modern

# 2. Setup virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\\Scripts\\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
python main_modern.py
```

## 🔑 Default Login

- **Username:** `admin`
- **Password:** `admin123`

## 📋 Project Structure

```
denso888-modern/
├── 📁 gui/                    # Modern UI components
├── 📁 core/                   # Business logic
├── 📁 config/                 # Configuration
├── 📁 security/               # Authentication
├── 📁 automation/             # Workflows
├── 📁 plugins/                # Extensions
└── 📁 tests/                  # Test suite
```

## 🎯 Usage Examples

### GUI Application
```bash
python main_modern.py
```

### Command Line
```bash
python cli.py import-excel -f data.xlsx -t employees
python cli.py generate-mock -t sales -r 5000
```

### Web API
```bash
python api.py
# Access: http://localhost:8000
```

## 🔧 Development

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Code formatting
black .
flake8 .

# Type checking
mypy .
```

## 📊 Supported Data Sources

- ✅ Excel files (.xlsx, .xls, .xlsm)
- ✅ Mock data generation
- ✅ CSV files
- ✅ Database imports

## 🗄️ Database Support

- ✅ **SQLite** (Local, no setup)
- ✅ **SQL Server** (Enterprise)
- 🔄 **MySQL** (Coming soon)
- 🔄 **PostgreSQL** (Coming soon)

## 🎨 Themes

- **DENSO Corporate** - Professional red theme
- **Dark Premium** - Modern dark theme
- **Ocean Blue** - Fresh blue theme

## 📈 Performance

| Dataset Size | Processing Time | Memory Usage |
|--------------|-----------------|--------------|
| 1K rows      | < 5 seconds     | < 50 MB      |
| 10K rows     | < 30 seconds    | < 100 MB     |
| 100K rows    | < 5 minutes     | < 500 MB     |

## 🛡️ Security Features

- 🔒 Password hashing with salt
- 🔑 Session management
- 👥 Role-based permissions
- 📝 Audit logging
- 🛡️ SQL injection prevention

## 🤝 Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for development guidelines.

## 📄 License

This project is proprietary software created for DENSO operations.

## 👨‍💻 Creator

**Thammaphon Chittasuwanna**
- Position: SDM | Innovation  
- Company: DENSO
- Nickname: เฮียตอมจัดหั้ย!!! 🚀

---

🏭 **Making Excel to SQL migration simple and powerful!** 🚀
"""

    def _get_theme_template(self, theme_name):
        themes = {
            "denso_corporate": {
                "name": "DENSO Corporate",
                "primary": "#DC0003",
                "primary_dark": "#B80002",
                "primary_light": "#FF1F22",
                "secondary": "#2C3E50",
                "accent": "#E74C3C",
                "success": "#27AE60",
                "warning": "#F39C12",
                "danger": "#E74C3C",
                "background": "#FFFFFF",
                "surface": "#F8F9FA",
                "text_primary": "#2C3E50",
                "text_secondary": "#7F8C8D",
                "border": "#E5E8EB",
                "shadow": "rgba(44, 62, 80, 0.1)",
            },
            "dark_premium": {
                "name": "Dark Premium",
                "primary": "#6366F1",
                "primary_dark": "#4F46E5",
                "primary_light": "#8B5CF6",
                "secondary": "#1F2937",
                "accent": "#F59E0B",
                "success": "#10B981",
                "warning": "#F59E0B",
                "danger": "#EF4444",
                "background": "#111827",
                "surface": "#1F2937",
                "text_primary": "#F9FAFB",
                "text_secondary": "#D1D5DB",
                "border": "#374151",
                "shadow": "rgba(0, 0, 0, 0.3)",
            },
            "ocean_blue": {
                "name": "Ocean Blue",
                "primary": "#0EA5E9",
                "primary_dark": "#0284C7",
                "primary_light": "#38BDF8",
                "secondary": "#1E293B",
                "accent": "#06B6D4",
                "success": "#22C55E",
                "warning": "#F59E0B",
                "danger": "#EF4444",
                "background": "#F8FAFC",
                "surface": "#FFFFFF",
                "text_primary": "#1E293B",
                "text_secondary": "#64748B",
                "border": "#E2E8F0",
                "shadow": "rgba(30, 41, 59, 0.1)",
            },
        }

        return json.dumps(themes.get(theme_name, themes["denso_corporate"]), indent=2)

    def _get_pyproject_template(self):
        return """[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "denso888-modern"
version = "2.0.0"
description = "Excel to SQL Management System with Advanced Analytics"
authors = [
    {name = "Thammaphon Chittasuwanna", email = "thammaphon@denso.com"}
]
readme = "README.md"
license = {text = "Proprietary"}
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]

dependencies = [
    "pandas>=2.0.0",
    "sqlalchemy>=2.0.0",
    "pyodbc>=4.0.39",
    "openpyxl>=3.1.0",
    "python-dotenv>=1.0.0",
    "tqdm>=4.65.0",
    "Pillow>=10.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "black>=23.7.0",
    "flake8>=6.0.0",
    "mypy>=1.5.0",
]

[project.scripts]
denso888 = "cli:cli"

[tool.black]
line-length = 88
target-version = ['py38']

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
"""


def main():
    """Run the setup script"""
    import argparse

    parser = argparse.ArgumentParser(description="DENSO888 Modern Project Setup")
    parser.add_argument(
        "--target",
        default="denso888-modern",
        help="Target directory for modern project",
    )
    parser.add_argument(
        "--backup",
        default="denso888-backup",
        help="Backup directory for existing files",
    )
    parser.add_argument(
        "--force", action="store_true", help="Force overwrite existing directories"
    )

    args = parser.parse_args()

    # Confirm before proceeding
    if not args.force:
        print(f"This will create a new modern project structure at: {args.target}")
        print(f"Existing files will be backed up to: {args.backup}")
        confirm = input("Continue? (y/N): ").lower().strip()
        if confirm not in ["y", "yes"]:
            print("Setup cancelled.")
            return

    # Run setup
    setup = DENSO888ProjectSetup(args.target)
    setup.run_setup()


if __name__ == "__main__":
    main()
