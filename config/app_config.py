from pathlib import Path
from typing import Dict, Any, Optional
import json
import os
from dataclasses import dataclass, field


@dataclass
class DatabaseConfig:
    """Database configuration"""

    type: str = "sqlite"
    host: str = "localhost"
    database: str = "denso888.db"
    username: Optional[str] = None
    password: Optional[str] = None
    pool_size: int = 5
    timeout: int = 30
    use_ssl: bool = False
    encrypt_password: bool = True


@dataclass
class ExcelConfig:
    """Excel processing configuration"""

    chunk_size: int = 5000
    max_file_size_mb: int = 100
    temp_dir: str = "temp"
    cleanup_temp: bool = True


@dataclass
class BackupConfig:
    """Backup configuration"""

    enabled: bool = True
    interval_minutes: int = 60
    backup_dir: str = "backups"
    keep_days: int = 7
    compress: bool = True


@dataclass
class UIConfig:
    """UI configuration"""

    theme: str = "modern"
    language: str = "en"
    animations: bool = True
    window_size: tuple = (1200, 800)


@dataclass
class AppConfig:
    """Main application configuration"""

    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    excel: ExcelConfig = field(default_factory=ExcelConfig)
    backup: BackupConfig = field(default_factory=BackupConfig)
    ui: UIConfig = field(default_factory=UIConfig)
    debug: bool = False

    @classmethod
    def load(cls) -> "AppConfig":
        """Load configuration from file or environment"""
        config_path = Path("config/config.json")

        # Load from file if exists
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)
        else:
            config_data = {}

        # Override with environment variables
        cls._update_from_env(config_data)

        # Create config instance
        return cls(**config_data)

    @staticmethod
    def _update_from_env(config: Dict[str, Any]):
        """Update config from environment variables"""
        mappings = {
            "DB_TYPE": ("database", "type"),
            "DB_HOST": ("database", "host"),
            "DB_NAME": ("database", "database"),
            "DB_USER": ("database", "username"),
            "DB_PASS": ("database", "password"),
            "BACKUP_ENABLED": ("backup", "enabled"),
            "DEBUG": (None, "debug"),
        }

        for env_key, config_path in mappings.items():
            if env_key in os.environ:
                value = os.environ[env_key]

                # Convert types
                if isinstance(value, str):
                    if value.lower() in ("true", "false"):
                        value = value.lower() == "true"
                    elif value.isdigit():
                        value = int(value)

                # Update config
                if len(config_path) == 2:
                    section, key = config_path
                    if section not in config:
                        config[section] = {}
                    config[section][key] = value
                else:
                    config[config_path[0]] = value
