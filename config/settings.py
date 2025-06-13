"""
Streamlined configuration system
"""

import os
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class DatabaseConfig:
    """Database configuration"""

    server: str = "localhost"
    database: str = "excel_to_db"
    username: str = "sa"
    password: str = ""
    driver: str = "ODBC Driver 17 for SQL Server"
    use_windows_auth: bool = True
    sqlite_file: str = "denso888_data.db"

    @classmethod
    def from_env(cls):
        return cls(
            server=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "excel_to_db"),
            username=os.getenv("DB_USER", "sa"),
            password=os.getenv("DB_PASSWORD", ""),
            use_windows_auth=os.getenv("DB_USE_WINDOWS_AUTH", "1") == "1",
            sqlite_file=os.getenv("SQLITE_FILE", "denso888_data.db"),
        )

    def get_connection_url(self) -> str:
        """Get SQLAlchemy connection URL with error handling"""
        try:
            if self.use_windows_auth:
                return f"mssql+pyodbc://@{self.server}/{self.database}?driver={self.driver.replace(' ', '+')}&trusted_connection=yes"
            else:
                return f"mssql+pyodbc://{self.username}:{self.password}@{self.server}/{self.database}?driver={self.driver.replace(' ', '+')}"
        except Exception as e:
            print(f"Connection URL error: {e}")
            return ""


@dataclass
class ProcessingConfig:
    """Processing configuration"""

    batch_size: int = 1000
    max_workers: int = 4
    chunk_size: int = 5000


@dataclass
class UIConfig:
    """UI configuration"""

    window_width: int = 1200
    window_height: int = 800
    theme_colors: Dict[str, str] = field(
        default_factory=lambda: {
            "primary": "#DC0003",
            "secondary": "#F5F5F5",
            "success": "#28A745",
            "warning": "#FFC107",
            "danger": "#DC3545",
        }
    )


@dataclass
class AppConfig:
    """Main application configuration"""

    app_name: str = "DENSO888 - Excel to SQL"
    version: str = "1.0.0"
    author: str = "เฮียตอมจัดหั้ย!!!"

    ui: UIConfig = field(default_factory=UIConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig.from_env)
    processing: ProcessingConfig = field(default_factory=ProcessingConfig)


def get_config() -> AppConfig:
    """Get application configuration"""
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        pass

    config = AppConfig()

    # Override from environment
    config.processing.batch_size = int(
        os.getenv("BATCH_SIZE", str(config.processing.batch_size))
    )
    config.processing.max_workers = int(
        os.getenv("MAX_WORKERS", str(config.processing.max_workers))
    )
    config.processing.chunk_size = int(
        os.getenv("CHUNK_SIZE", str(config.processing.chunk_size))
    )

    return config
