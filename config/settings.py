"""
Configuration settings for the application
แก้ไขปัญหา mutable default และปรับปรุงโครงสร้าง
"""

import os
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


@dataclass
class UIConfig:
    """UI Configuration settings"""

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
            "white": "#FFFFFF",
            "light": "#F8F9FA",
        }
    )


@dataclass
class DatabaseConfig:
    """Database Configuration settings"""

    # SQL Server settings
    server: str = "localhost"
    database: str = "excel_to_db"
    username: str = "sa"
    password: str = ""
    driver: str = "ODBC Driver 17 for SQL Server"
    use_windows_auth: bool = True

    # Connection pool settings
    pool_size: int = 5
    max_overflow: int = 10
    pool_timeout: int = 30
    pool_recycle: int = 3600

    # SQLite fallback
    sqlite_file: str = "denso888_data.db"

    @classmethod
    def from_env(cls) -> "DatabaseConfig":
        """Load configuration from environment variables"""
        return cls(
            server=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "excel_to_db"),
            username=os.getenv("DB_USER", "sa"),
            password=os.getenv("DB_PASSWORD", ""),
            driver=os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server"),
            use_windows_auth=os.getenv("DB_USE_WINDOWS_AUTH", "1") == "1",
            pool_size=int(os.getenv("POOL_SIZE", "5")),
            max_overflow=int(os.getenv("MAX_OVERFLOW", "10")),
            pool_timeout=int(os.getenv("POOL_TIMEOUT", "30")),
            pool_recycle=int(os.getenv("POOL_RECYCLE", "3600")),
            sqlite_file=os.getenv("SQLITE_FILE", "denso888_data.db"),
        )

    def get_connection_url(self) -> str:
        """Get SQLAlchemy connection URL"""
        if self.use_windows_auth:
            return (
                f"mssql+pyodbc://@{self.server}/{self.database}"
                f"?driver={self.driver.replace(' ', '+')}&trusted_connection=yes"
            )
        else:
            return (
                f"mssql+pyodbc://{self.username}:{self.password}@{self.server}"
                f"/{self.database}?driver={self.driver.replace(' ', '+')}"
            )


@dataclass
class ProcessingConfig:
    """Data processing configuration"""

    batch_size: int = 1000
    max_workers: int = 4
    chunk_size: int = 5000
    timeout: int = 300


@dataclass
class LoggingConfig:
    """Logging configuration"""

    level: str = "INFO"
    log_file: str = "logs/denso888.log"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5


@dataclass
class AppConfig:
    """Main application configuration"""

    app_name: str = "DENSO888 - Excel to SQL"
    version: str = "1.0.0"
    author: str = "เฮียตอมจัดหั้ย!!!"

    # Sub-configurations - ใช้ field(default_factory=...) เพื่อหลีกเลี่ยง mutable default
    ui: UIConfig = field(default_factory=UIConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig.from_env)
    processing: ProcessingConfig = field(default_factory=ProcessingConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)


def get_config() -> AppConfig:
    """Get application configuration with environment variable support"""
    try:
        # โหลด .env file ถ้ามี
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        logger.warning("python-dotenv not available, skipping .env file loading")

    # Override บางค่าจาก environment variables
    config = AppConfig()

    # Override processing config from env
    config.processing.batch_size = int(
        os.getenv("BATCH_SIZE", str(config.processing.batch_size))
    )
    config.processing.max_workers = int(
        os.getenv("MAX_WORKERS", str(config.processing.max_workers))
    )
    config.processing.chunk_size = int(
        os.getenv("CHUNK_SIZE", str(config.processing.chunk_size))
    )

    # Override logging config from env
    config.logging.level = os.getenv("LOG_LEVEL", config.logging.level)
    config.logging.log_file = os.getenv("LOG_FILE", config.logging.log_file)

    # Ensure log directory exists
    log_path = Path(config.logging.log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    return config


def validate_config(config: AppConfig) -> bool:
    """Validate configuration settings"""
    try:
        # Validate UI config
        if config.ui.window_width < 800 or config.ui.window_height < 600:
            logger.warning("Window size too small, using minimum values")
            config.ui.window_width = max(config.ui.window_width, 800)
            config.ui.window_height = max(config.ui.window_height, 600)

        # Validate processing config
        if config.processing.batch_size < 100:
            logger.warning("Batch size too small, setting to 100")
            config.processing.batch_size = 100

        if config.processing.max_workers < 1:
            logger.warning("Max workers too small, setting to 1")
            config.processing.max_workers = 1

        if config.processing.chunk_size < 1000:
            logger.warning("Chunk size too small, setting to 1000")
            config.processing.chunk_size = 1000

        return True

    except Exception as e:
        logger.error(f"Configuration validation failed: {e}")
        return False


# สำหรับ backward compatibility
def get_database_config() -> DatabaseConfig:
    """Get database configuration"""
    return DatabaseConfig.from_env()


def get_processing_config() -> ProcessingConfig:
    """Get processing configuration"""
    return ProcessingConfig(
        batch_size=int(os.getenv("BATCH_SIZE", "1000")),
        max_workers=int(os.getenv("MAX_WORKERS", "4")),
        chunk_size=int(os.getenv("CHUNK_SIZE", "5000")),
    )
