"""
Configuration settings for the application
"""

import os
from dataclasses import dataclass, field
from typing import Dict, Any
from pathlib import Path


@dataclass
class UIConfig:
    window_width: int = 1200
    window_height: int = 800
    min_width: int = 1000
    min_height: int = 700
    theme_colors: Dict[str, str] = field(
        default_factory=lambda: {
            "primary": "#DC0003",
            "secondary": "#F5F5F5",
            "success": "#28A745",
            "warning": "#FFC107",
            "danger": "#DC3545",
            "accent": "#333333",
        }
    )


@dataclass
class DatabaseConfig:
    server: str = "localhost"
    database: str = "master"
    username: str = "sa"
    password: str = ""
    use_windows_auth: bool = True

    @classmethod
    def from_env(cls) -> "DatabaseConfig":
        return cls(
            server=os.getenv("DB_SERVER", "localhost"),
            database=os.getenv("DB_NAME", "master"),
            username=os.getenv("DB_USER", "sa"),
            password=os.getenv("DB_PASSWORD", ""),
            use_windows_auth=os.getenv("DB_USE_WINDOWS_AUTH", "1") == "1",
        )


@dataclass
class AppConfig:
    app_name: str = "DENSO888 - Excel to SQL"
    version: str = "1.0.0"
    author: str = "เฮียตอมจัดหั้ย!!!"
    ui: UIConfig = field(default_factory=UIConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    log_file: Path = field(default_factory=lambda: Path("app.log"))


def get_config() -> AppConfig:
    """Get application configuration"""
    return AppConfig()
