# config/manager.py
"""
Centralized Configuration Management
รวมการจัดการ config ทั้งหมดไว้ที่เดียว
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class DatabaseConfig:
    """Database configuration"""

    type: str = "sqlite"  # sqlite, sqlserver
    host: str = "localhost"
    port: int = 1433
    database: str = "denso888"
    username: str = "sa"
    password: str = ""
    use_windows_auth: bool = True
    sqlite_file: str = "denso888_data.db"
    connection_timeout: int = 30
    pool_size: int = 5


@dataclass
class UIConfig:
    """UI configuration"""

    theme: str = "denso"
    window_width: int = 1200
    window_height: int = 800
    font_family: str = "Segoe UI"
    font_size: int = 10
    show_splash: bool = True
    remember_window_state: bool = True


@dataclass
class ProcessingConfig:
    """Data processing configuration"""

    batch_size: int = 1000
    max_workers: int = 4
    chunk_size: int = 5000
    auto_detect_types: bool = True
    clean_data: bool = True
    max_file_size_mb: int = 100


@dataclass
class LoggingConfig:
    """Logging configuration"""

    level: str = "INFO"
    file_path: str = "logs/denso888.log"
    max_file_size_mb: int = 10
    backup_count: int = 5
    console_output: bool = True


@dataclass
class SecurityConfig:
    """Security configuration"""

    require_auth: bool = False
    session_timeout_minutes: int = 60
    password_min_length: int = 8
    enable_audit_log: bool = True


@dataclass
class AppConfig:
    """Main application configuration"""

    # Application info
    name: str = "DENSO888"
    version: str = "2.0.0"
    author: str = "Thammaphon Chittasuwanna (SDM)"
    description: str = "Excel to SQL Management System"

    # Sub-configurations
    database: DatabaseConfig = None
    ui: UIConfig = None
    processing: ProcessingConfig = None
    logging: LoggingConfig = None
    security: SecurityConfig = None

    def __post_init__(self):
        """Initialize sub-configs if not provided"""
        if self.database is None:
            self.database = DatabaseConfig()
        if self.ui is None:
            self.ui = UIConfig()
        if self.processing is None:
            self.processing = ProcessingConfig()
        if self.logging is None:
            self.logging = LoggingConfig()
        if self.security is None:
            self.security = SecurityConfig()


class ConfigManager:
    """Centralized configuration manager"""

    def __init__(self, config_file: str = "denso888_config.json"):
        self.config_file = Path(config_file)
        self.config: AppConfig = AppConfig()
        self._env_prefix = "DENSO888_"

        # Load configuration
        self._load_config()

    def _load_config(self):
        """Load configuration from multiple sources"""
        # 1. Load from file if exists
        if self.config_file.exists():
            self._load_from_file()

        # 2. Override with environment variables
        self._load_from_env()

        # 3. Load from .env file
        self._load_from_dotenv()

    def _load_from_file(self):
        """Load configuration from JSON file"""
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Update configuration
            self._update_config_from_dict(data)

        except Exception as e:
            print(f"Warning: Failed to load config from {self.config_file}: {e}")

    def _load_from_env(self):
        """Load configuration from environment variables"""
        env_mappings = {
            # Database
            f"{self._env_prefix}DB_TYPE": ("database", "type"),
            f"{self._env_prefix}DB_HOST": ("database", "host"),
            f"{self._env_prefix}DB_PORT": ("database", "port"),
            f"{self._env_prefix}DB_NAME": ("database", "database"),
            f"{self._env_prefix}DB_USER": ("database", "username"),
            f"{self._env_prefix}DB_PASSWORD": ("database", "password"),
            f"{self._env_prefix}DB_USE_WINDOWS_AUTH": ("database", "use_windows_auth"),
            # UI
            f"{self._env_prefix}UI_THEME": ("ui", "theme"),
            f"{self._env_prefix}UI_WIDTH": ("ui", "window_width"),
            f"{self._env_prefix}UI_HEIGHT": ("ui", "window_height"),
            # Processing
            f"{self._env_prefix}BATCH_SIZE": ("processing", "batch_size"),
            f"{self._env_prefix}MAX_WORKERS": ("processing", "max_workers"),
            # Logging
            f"{self._env_prefix}LOG_LEVEL": ("logging", "level"),
            f"{self._env_prefix}LOG_FILE": ("logging", "file_path"),
        }

        for env_var, (section, key) in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                self._set_config_value(section, key, self._convert_env_value(value))

    def _load_from_dotenv(self):
        """Load from .env file"""
        env_file = Path(".env")
        if env_file.exists():
            try:
                from dotenv import load_dotenv

                load_dotenv(env_file)
                # Re-run environment loading after loading .env
                self._load_from_env()
            except ImportError:
                pass  # python-dotenv not installed

    def _convert_env_value(self, value: str) -> Union[str, int, bool]:
        """Convert environment variable string to appropriate type"""
        # Boolean conversion
        if value.lower() in ("true", "1", "yes", "on"):
            return True
        elif value.lower() in ("false", "0", "no", "off"):
            return False

        # Integer conversion
        try:
            return int(value)
        except ValueError:
            pass

        # Return as string
        return value

    def _update_config_from_dict(self, data: Dict[str, Any]):
        """Update configuration from dictionary"""
        for section, values in data.items():
            if hasattr(self.config, section) and isinstance(values, dict):
                config_section = getattr(self.config, section)
                for key, value in values.items():
                    if hasattr(config_section, key):
                        setattr(config_section, key, value)

    def _set_config_value(self, section: str, key: str, value: Any):
        """Set configuration value"""
        if hasattr(self.config, section):
            config_section = getattr(self.config, section)
            if hasattr(config_section, key):
                setattr(config_section, key, value)

    def save_config(self):
        """Save current configuration to file"""
        try:
            # Ensure directory exists
            self.config_file.parent.mkdir(parents=True, exist_ok=True)

            # Convert to dictionary
            config_dict = {
                "database": asdict(self.config.database),
                "ui": asdict(self.config.ui),
                "processing": asdict(self.config.processing),
                "logging": asdict(self.config.logging),
                "security": asdict(self.config.security),
                "_metadata": {
                    "saved_at": datetime.now().isoformat(),
                    "version": self.config.version,
                },
            }

            # Save to file
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)

            return True

        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    def get_config(self) -> AppConfig:
        """Get current configuration"""
        return self.config

    def update_config(self, updates: Dict[str, Any]):
        """Update configuration with new values"""
        self._update_config_from_dict(updates)

    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self.config = AppConfig()

    def validate_config(self) -> Dict[str, list]:
        """Validate configuration and return issues"""
        issues = {"errors": [], "warnings": []}

        # Database validation
        if self.config.database.type not in ["sqlite", "sqlserver"]:
            issues["errors"].append("Invalid database type")

        if self.config.database.type == "sqlserver":
            if not self.config.database.host:
                issues["errors"].append("SQL Server host is required")
            if not self.config.database.database:
                issues["errors"].append("Database name is required")

        # UI validation
        if self.config.ui.window_width < 800:
            issues["warnings"].append("Window width is very small")
        if self.config.ui.window_height < 600:
            issues["warnings"].append("Window height is very small")

        # Processing validation
        if self.config.processing.batch_size <= 0:
            issues["errors"].append("Batch size must be positive")
        if self.config.processing.max_workers <= 0:
            issues["errors"].append("Max workers must be positive")

        # Logging validation
        if self.config.logging.level not in ["DEBUG", "INFO", "WARNING", "ERROR"]:
            issues["warnings"].append("Invalid log level")

        return issues

    def get_database_url(self) -> Optional[str]:
        """Get database connection URL"""
        db_config = self.config.database

        if db_config.type == "sqlite":
            return f"sqlite:///{db_config.sqlite_file}"

        elif db_config.type == "sqlserver":
            if db_config.use_windows_auth:
                return f"mssql+pyodbc://{db_config.host}:{db_config.port}/{db_config.database}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
            else:
                return f"mssql+pyodbc://{db_config.username}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.database}?driver=ODBC+Driver+17+for+SQL+Server"

        return None

    def export_config(self, file_path: str = None) -> str:
        """Export configuration to file"""
        if file_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = f"denso888_config_export_{timestamp}.json"

        export_data = {
            "export_info": {
                "exported_at": datetime.now().isoformat(),
                "version": self.config.version,
                "exported_by": self.config.author,
            },
            "configuration": {
                "database": asdict(self.config.database),
                "ui": asdict(self.config.ui),
                "processing": asdict(self.config.processing),
                "logging": asdict(self.config.logging),
                "security": asdict(self.config.security),
            },
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        return file_path

    def import_config(self, file_path: str) -> bool:
        """Import configuration from file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Extract configuration part
            config_data = data.get("configuration", data)
            self._update_config_from_dict(config_data)

            # Save the imported configuration
            self.save_config()

            return True

        except Exception as e:
            print(f"Error importing config: {e}")
            return False


# ===== Global Configuration Manager =====
_config_manager: Optional[ConfigManager] = None


def get_config_manager() -> ConfigManager:
    """Get global configuration manager"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


def get_config() -> AppConfig:
    """Get application configuration"""
    return get_config_manager().get_config()


def save_config() -> bool:
    """Save current configuration"""
    return get_config_manager().save_config()


def update_config(updates: Dict[str, Any]) -> bool:
    """Update configuration"""
    try:
        get_config_manager().update_config(updates)
        return save_config()
    except Exception:
        return False


# ===== Configuration Validation =====
class ConfigValidator:
    """Configuration validation utility"""

    @staticmethod
    def validate_database_connection(config: DatabaseConfig) -> Dict[str, Any]:
        """Validate database connection"""
        result = {"valid": True, "errors": [], "warnings": []}

        if config.type == "sqlserver":
            # Test SQL Server connection
            try:
                import pyodbc

                if config.use_windows_auth:
                    conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={config.host},{config.port};DATABASE={config.database};Trusted_Connection=yes;"
                else:
                    conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={config.host},{config.port};DATABASE={config.database};UID={config.username};PWD={config.password};"

                conn = pyodbc.connect(conn_str, timeout=config.connection_timeout)
                conn.close()

            except ImportError:
                result["valid"] = False
                result["errors"].append("pyodbc not installed")
            except Exception as e:
                result["valid"] = False
                result["errors"].append(f"SQL Server connection failed: {e}")

        elif config.type == "sqlite":
            # Test SQLite file access
            try:
                import sqlite3

                db_path = Path(config.sqlite_file)

                # Check if directory is writable
                db_path.parent.mkdir(parents=True, exist_ok=True)

                # Test connection
                conn = sqlite3.connect(str(db_path))
                conn.close()

            except Exception as e:
                result["valid"] = False
                result["errors"].append(f"SQLite connection failed: {e}")

        return result

    @staticmethod
    def validate_paths(config: AppConfig) -> Dict[str, Any]:
        """Validate file paths in configuration"""
        result = {"valid": True, "errors": [], "warnings": []}

        # Log file path
        log_path = Path(config.logging.file_path)
        try:
            log_path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            result["warnings"].append(f"Cannot create log directory: {e}")

        # SQLite database path
        if config.database.type == "sqlite":
            db_path = Path(config.database.sqlite_file)
            try:
                db_path.parent.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                result["errors"].append(f"Cannot create database directory: {e}")
                result["valid"] = False

        return result


# ===== Configuration Templates =====
class ConfigTemplates:
    """Pre-defined configuration templates"""

    @staticmethod
    def development_config() -> AppConfig:
        """Development environment configuration"""
        config = AppConfig()
        config.database.type = "sqlite"
        config.database.sqlite_file = "dev_denso888.db"
        config.logging.level = "DEBUG"
        config.logging.console_output = True
        config.ui.show_splash = False
        config.processing.batch_size = 100  # Smaller for testing
        return config

    @staticmethod
    def production_config() -> AppConfig:
        """Production environment configuration"""
        config = AppConfig()
        config.database.type = "sqlserver"
        config.database.use_windows_auth = True
        config.logging.level = "INFO"
        config.logging.console_output = False
        config.security.require_auth = True
        config.security.enable_audit_log = True
        config.processing.batch_size = 5000  # Larger for performance
        return config

    @staticmethod
    def demo_config() -> AppConfig:
        """Demo/presentation configuration"""
        config = AppConfig()
        config.database.type = "sqlite"
        config.database.sqlite_file = "demo_denso888.db"
        config.ui.theme = "denso"
        config.ui.show_splash = True
        config.processing.batch_size = 1000
        config.logging.level = "INFO"
        return config


# ===== Environment Detection =====
class EnvironmentDetector:
    """Detect and configure for different environments"""

    @staticmethod
    def detect_environment() -> str:
        """Detect current environment"""
        # Check environment variable
        env = os.getenv("DENSO888_ENV", "").lower()
        if env in ["development", "dev"]:
            return "development"
        elif env in ["production", "prod"]:
            return "production"
        elif env in ["demo", "demo"]:
            return "demo"

        # Auto-detect based on system
        if os.path.exists(".git") or os.path.exists("dev.py"):
            return "development"
        elif os.path.exists("production.flag"):
            return "production"

        return "development"  # Default

    @staticmethod
    def get_environment_config() -> AppConfig:
        """Get configuration for detected environment"""
        env = EnvironmentDetector.detect_environment()

        if env == "development":
            return ConfigTemplates.development_config()
        elif env == "production":
            return ConfigTemplates.production_config()
        elif env == "demo":
            return ConfigTemplates.demo_config()

        return AppConfig()  # Default


# ===== Configuration CLI =====
class ConfigCLI:
    """Command-line interface for configuration management"""

    def __init__(self):
        self.config_manager = get_config_manager()

    def show_config(self):
        """Show current configuration"""
        config = self.config_manager.get_config()

        print("🏭 DENSO888 Configuration")
        print("=" * 50)
        print(f"App: {config.name} v{config.version}")
        print(f"Author: {config.author}")
        print()

        print("Database Configuration:")
        print(f"  Type: {config.database.type}")
        if config.database.type == "sqlserver":
            print(f"  Host: {config.database.host}:{config.database.port}")
            print(f"  Database: {config.database.database}")
            print(
                f"  Auth: {'Windows' if config.database.use_windows_auth else 'SQL Server'}"
            )
        else:
            print(f"  File: {config.database.sqlite_file}")
        print()

        print("UI Configuration:")
        print(f"  Theme: {config.ui.theme}")
        print(f"  Window: {config.ui.window_width}x{config.ui.window_height}")
        print(f"  Font: {config.ui.font_family} {config.ui.font_size}pt")
        print()

        print("Processing Configuration:")
        print(f"  Batch Size: {config.processing.batch_size:,}")
        print(f"  Max Workers: {config.processing.max_workers}")
        print(f"  Max File Size: {config.processing.max_file_size_mb} MB")
        print()

        print("Logging Configuration:")
        print(f"  Level: {config.logging.level}")
        print(f"  File: {config.logging.file_path}")
        print(f"  Console: {config.logging.console_output}")

    def validate_config(self):
        """Validate current configuration"""
        print("🔍 Validating Configuration...")

        # General validation
        issues = self.config_manager.validate_config()

        # Database validation
        config = self.config_manager.get_config()
        db_validation = ConfigValidator.validate_database_connection(config.database)

        # Path validation
        path_validation = ConfigValidator.validate_paths(config)

        # Report results
        all_errors = (
            issues["errors"]
            + db_validation.get("errors", [])
            + path_validation.get("errors", [])
        )
        all_warnings = (
            issues["warnings"]
            + db_validation.get("warnings", [])
            + path_validation.get("warnings", [])
        )

        if all_errors:
            print("❌ Errors found:")
            for error in all_errors:
                print(f"  • {error}")

        if all_warnings:
            print("⚠️ Warnings:")
            for warning in all_warnings:
                print(f"  • {warning}")

        if not all_errors and not all_warnings:
            print("✅ Configuration is valid!")

        return len(all_errors) == 0

    def export_config(self, file_path: str = None):
        """Export configuration"""
        try:
            exported_file = self.config_manager.export_config(file_path)
            print(f"✅ Configuration exported to: {exported_file}")
            return True
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return False

    def import_config(self, file_path: str):
        """Import configuration"""
        if not Path(file_path).exists():
            print(f"❌ File not found: {file_path}")
            return False

        try:
            if self.config_manager.import_config(file_path):
                print(f"✅ Configuration imported from: {file_path}")
                return True
            else:
                print(f"❌ Import failed")
                return False
        except Exception as e:
            print(f"❌ Import failed: {e}")
            return False


# ===== Usage Examples =====
def main():
    """CLI entry point for configuration management"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python config/manager.py <command>")
        print("Commands:")
        print("  show      - Show current configuration")
        print("  validate  - Validate configuration")
        print("  export    - Export configuration")
        print("  import    - Import configuration from file")
        return

    cli = ConfigCLI()
    command = sys.argv[1].lower()

    if command == "show":
        cli.show_config()
    elif command == "validate":
        cli.validate_config()
    elif command == "export":
        file_path = sys.argv[2] if len(sys.argv) > 2 else None
        cli.export_config(file_path)
    elif command == "import":
        if len(sys.argv) < 3:
            print("Error: Import requires file path")
            return
        cli.import_config(sys.argv[2])
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
